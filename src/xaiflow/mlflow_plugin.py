"""
MLflow Plugin for CE MLflow Extension
Integrates the report generator with MLflow for storing HTML reports as artifacts
"""

import os
import json
import warnings
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
        report_name: str = "feature_importance_report.html",
        round_decimals: int = 4
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
            round_decimals: Number of decimals to round feature values and SHAP values
            
        Returns:
            str: Path to the logged artifact
        """
        
        if not isinstance(shap_values, Explanation):
            raise ValueError("shap_values must be an instance of shap.Explanation. Pls call explainer(X) or similar to get a valid Explanation object.")
        if np.issubdtype(shap_values.data.dtype, np.floating):
            feature_values = np.round(shap_values.data, round_decimals)
        else:
            feature_values = shap_values.data
        base_values = np.round(shap_values.base_values, round_decimals)[0]
        shap_values = np.round(shap_values.values, round_decimals)
        if feature_values.ndim != shap_values.ndim:
            if shap_values.ndim - feature_values.ndim > 1:
                NotImplementedError("It looks like you're using multi-target regression or multi-output classification. Currently we don't support this."
                              " You can still use the plugin, just hand over shap_values[..., <target_index>] to get the SHAP values for a specific target/class."
                              " Please ensure that the shap_values.dim - feature_values.dim is 1 or less.")
            else:
                warnings.warn("Feature values and SHAP values dimensions do not match. This can be due to multi-target regression or (multi-target) classification."
                              " If you want a specific target/class, please hand over shap_values[..., <target_index>] to get the SHAP values for that target/class."
                              " We fall back to shap_values[..., -1] in this case."
                )
                shap_values = shap_values[..., -1]
                base_values = float(base_values[-1])

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

            # with open('test_report.html', 'w', encoding='utf-8') as f:
            #     f.write(html_content)
            
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
