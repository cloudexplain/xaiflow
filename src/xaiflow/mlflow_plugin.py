"""
MLflow Plugin for CE MLflow Extension
Integrates the report generator with MLflow for storing HTML reports as artifacts
"""

import os
import json
import tempfile
import shutil
import mlflow
from mlflow.tracking import MlflowClient
from typing import Dict, List, Optional, Any
import numpy as np
from shap import Explanation
from jinja2 import Environment, FileSystemLoader


class XaiflowPlugin:
    """
    CE MLflow Extension Plugin for generating and storing interactive HTML reports
    """
    
    def __init__(self):
        self.client = MlflowClient()
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def log_feature_importance_report(
        self,
        feature_names: List[str],
        shap_values: Explanation,
        feature_encodings: Optional[Dict[str, Dict[int, str]]] = None,
        importance_values: List[float] | np.ndarray = None,
        run_id: Optional[str] = None,
        artifact_path: str = "reports",
        report_name: str = "feature_importance_report.html"
    ) -> str:
        """
        Log an interactive feature importance report as an MLflow artifact
        
        Args:
            feature_names: List of feature names
            importance_values: List of importance values corresponding to features
            shap_values: Optional SHAP values matrix (samples x features)
            run_id: MLflow run ID (uses active run if None)
            artifact_path: Path within MLflow artifacts to store the report
            report_name: Name of the HTML report file
            
        Returns:
            str: Path to the logged artifact
        """
        
        if not isinstance(shap_values, Explanation):
            raise ValueError("shap_values must be an instance of shap.Explanation. Pls call explainer(X) or similar to get a valid Explanation object.")
        feature_values = shap_values.data
        base_values = shap_values.base_values
        shap_values = shap_values.values
        # Use active run if no run_id provided
        if run_id is None:
            active_run = mlflow.active_run()
            if active_run is None:
                raise ValueError("No active MLflow run found. Please start a run or provide run_id.")
            run_id = active_run.info.run_id
        
        # Normalize importance values to sum to 1
        if importance_values is None:
            importance_values = np.abs(shap_values).mean(axis=0).tolist()
        total_importance = sum(importance_values)
        if total_importance > 0:
            normalized_importance = [v / total_importance for v in importance_values]
        else:
            normalized_importance = importance_values
        
        # Prepare data for the report
        importance_data = {
            "features": feature_names,
            "values": normalized_importance
        }
        
        # Create temporary file for the HTML report (with inlined JS)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        try:
            # Generate the HTML report with inlined bundle.js
            html_content = self._generate_html_content(
                importance_data=importance_data,
                shap_values=shap_values,
                feature_values=feature_values,
                base_values=base_values,
                feature_encodings=feature_encodings,
                feature_names=feature_names,
            )

            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            with open('test_report.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Log the report as an MLflow artifact
            artifact_full_path = f"{artifact_path}/{report_name}"
            mlflow.log_artifact(temp_path, artifact_path)
            
            # Log metadata about the report
            # mlflow.log_param("report_type", "feature_importance")
            # mlflow.log_param("num_features", len(feature_names))
            mlflow.log_param("report_artifact_path", artifact_full_path)
            
            # Log feature importance as metrics
            # for feature, importance in zip(feature_names, normalized_importance):
            #     mlflow.log_metric(f"importance_{feature}", importance)
            
            print(f"Feature importance report logged to MLflow: {artifact_full_path}")
            return artifact_full_path
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def log_model_explanation_report(
        self,
        model,
        X_test: np.ndarray,
        y_test: np.ndarray,
        feature_names: List[str],
        model_name: str = "model",
        run_id: Optional[str] = None,
        artifact_path: str = "reports",
        report_name: str = "model_explanation_report.html"
    ) -> str:
        """
        Log a comprehensive model explanation report with SHAP analysis
        
        Args:
            model: Trained model object
            X_test: Test data features
            y_test: Test data targets
            feature_names: List of feature names
            model_name: Name of the model
            run_id: MLflow run ID (uses active run if None)
            artifact_path: Path within MLflow artifacts to store the report
            report_name: Name of the HTML report file
            
        Returns:
            str: Path to the logged artifact
        """
        
        try:
            import shap
        except ImportError:
            raise ImportError("SHAP is required for model explanation reports. Install with: pip install shap")
        
        # Use active run if no run_id provided
        if run_id is None:
            active_run = mlflow.active_run()
            if active_run is None:
                raise ValueError("No active MLflow run found. Please start a run or provide run_id.")
            run_id = active_run.info.run_id
        
        # Calculate feature importance (if model supports it)
        try:
            if hasattr(model, 'feature_importances_'):
                importance_values = model.feature_importances_.tolist()
            elif hasattr(model, 'coef_'):
                importance_values = np.abs(model.coef_).flatten().tolist()
            else:
                # Use permutation importance as fallback
                from sklearn.inspection import permutation_importance
                perm_importance = permutation_importance(model, X_test, y_test, random_state=42)
                importance_values = perm_importance.importances_mean.tolist()
        except Exception as e:
            print(f"Warning: Could not calculate feature importance: {e}")
            importance_values = [1.0 / len(feature_names)] * len(feature_names)
        
        # Calculate SHAP values
        try:
            # Use TreeExplainer for tree-based models, LinearExplainer for linear models
            if hasattr(model, 'tree_'):
                explainer = shap.TreeExplainer(model)
            else:
                explainer = shap.LinearExplainer(model, X_test)
            
            # Calculate SHAP values for a subset of test data (for performance)
            sample_size = min(100, len(X_test))
            sample_indices = np.random.choice(len(X_test), sample_size, replace=False)
            X_sample = X_test[sample_indices]
            
            shap_values_matrix = explainer.shap_values(X_sample)
            
            # Handle multi-class case (take first class for now)
            if isinstance(shap_values_matrix, list):
                shap_values_matrix = shap_values_matrix[0]
            
            shap_values = shap_values_matrix.tolist()
            
        except Exception as e:
            print(f"Warning: Could not calculate SHAP values: {e}")
            # Generate dummy SHAP values
            sample_size = min(100, len(X_test))
            shap_values = []
            for _ in range(sample_size):
                sample_shap = [
                    np.random.normal(0, abs(imp_val) * 0.1) 
                    for imp_val in importance_values
                ]
                shap_values.append(sample_shap)
        
        # Log the report
        return self.log_feature_importance_report(
            feature_names=feature_names,
            importance_values=importance_values,
            shap_values=shap_values,
            run_id=run_id,
            artifact_path=artifact_path,
            report_name=report_name
        )
    
    def _generate_html_content(
        self,
        importance_data: Dict[str, Any],
        shap_values: List[List[float]],
        feature_values: List[float] = None,
        base_values: List[float] = None,
        feature_encodings: Optional[Dict[str, Dict[int, str]]] = None,
        feature_names: List[str] = None
    ):
        """
        Generate a custom HTML report with the provided data, inlining the bundle.js
        
        Args:
            output_path: Path where to save the HTML report
            importance_data: Dictionary containing feature names and importance values
            shap_values: SHAP values matrix
        """
        
        # Load the template
        template = self.env.get_template('report.html')
        
        # Read the bundle.js content to inline it
        bundle_js_content = ""
        bundle_path = os.path.join(
            os.path.dirname(__file__), 'templates', 'assets', 'bundle.js'
        )
        
        if os.path.exists(bundle_path):
            with open(bundle_path, 'r', encoding='utf-8') as f:
                bundle_js_content = f.read()
            print(f"Loaded bundle.js content ({len(bundle_js_content)} characters)")
        else:
            print(f"Warning: bundle.js not found at {bundle_path}")
        
        # Generate metadata
        import random
        from datetime import datetime
        random_number = random.randint(1, 1000)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Convert numpy arrays to Python lists for JSON serialization
        if isinstance(shap_values, np.ndarray):
            shap_values = shap_values.tolist()
        elif hasattr(shap_values, 'tolist'):
            shap_values = shap_values.tolist()
        
        if feature_values is not None:
            if isinstance(feature_values, np.ndarray):
                feature_values = feature_values.tolist()
            elif hasattr(feature_values, 'tolist'):
                feature_values = feature_values.tolist()
        
        if base_values is not None:
            if isinstance(base_values, np.ndarray):
                base_values = base_values.tolist()
            elif hasattr(base_values, 'tolist'):
                base_values = base_values.tolist()
        
        # Render the template with data (no json.dumps needed since Jinja2 handles it)
        html_content = template.render(
            random_number=random_number,
            timestamp=current_time,
            importance_data=importance_data,  # Pass as Python dict
            shap_values=shap_values,  # Pass as Python list
            feature_values=feature_values,  # Pass as Python list or None
            base_values=base_values or [0] * 10,  # Todo: fix this once we hand over numpy arrays
            feature_encodings=feature_encodings or {},  # Pass as optional dict
            feature_names=feature_names,  # Pass as list
            bundle_js_content=bundle_js_content  # Pass the bundle content
        )
        
        return html_content
        # Write to file
    
    def get_report_url(self, run_id: str, artifact_path: str = "reports", report_name: str = "feature_importance_report.html") -> str:
        """
        Get the MLflow UI URL for viewing the report
        
        Args:
            run_id: MLflow run ID
            artifact_path: Path within MLflow artifacts where the report is stored
            report_name: Name of the HTML report file
            
        Returns:
            str: URL to view the report in MLflow UI
        """
        
        # Get the MLflow tracking URI
        tracking_uri = mlflow.get_tracking_uri()
        
        # Construct the artifact URL
        artifact_full_path = f"{artifact_path}/{report_name}"
        
        if tracking_uri.startswith("http"):
            # Remote MLflow server
            base_url = tracking_uri.rstrip('/')
            url = f"{base_url}/#/experiments/runs/{run_id}/artifacts/{artifact_full_path}"
        else:
            # Local MLflow server (assume default port 5000)
            url = f"http://localhost:5000/#/experiments/runs/{run_id}/artifacts/{artifact_full_path}"
        
        return url


# Convenience functions for easy usage
def log_feature_importance(
    feature_names: List[str],
    importance_values: List[float],
    shap_values: Optional[List[List[float]]] = None,
    **kwargs
) -> str:
    """
    Convenience function to log feature importance report to MLflow
    """
    plugin = XaiflowPlugin()
    return plugin.log_feature_importance_report(
        feature_names=feature_names,
        importance_values=importance_values,
        shap_values=shap_values,
        **kwargs
    )


def log_model_explanation(
    model,
    X_test: np.ndarray,
    y_test: np.ndarray,
    feature_names: List[str],
    **kwargs
) -> str:
    """
    Convenience function to log model explanation report to MLflow
    """
    plugin = XaiflowPlugin()
    return plugin.log_model_explanation_report(
        model=model,
        X_test=X_test,
        y_test=y_test,
        feature_names=feature_names,
        **kwargs
    )
