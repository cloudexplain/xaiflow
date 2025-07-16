#!/usr/bin/env python3
"""
Simple test for the CE MLflow Extension Plugin
"""

import mlflow
import numpy as np
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ce_mlflow_extension.mlflow_plugin import CEMLflowPlugin
    print("✅ Successfully imported CEMLflowPlugin")
except Exception as e:
    print(f"❌ Error importing plugin: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

def test_plugin():
    """Test the MLflow plugin functionality"""
    
    # Set up experiment
    mlflow.set_experiment("Plugin_Test")
    
    with mlflow.start_run(run_name="simple_test"):
        # Initialize plugin
        plugin = CEMLflowPlugin()
        print("✅ Plugin initialized successfully")
        
        # Sample data
        feature_names = ["feature_1", "feature_2", "feature_3"]
        importance_values = [0.5, 0.3, 0.2]
        
        # Log feature importance report
        try:
            artifact_path = plugin.log_feature_importance_report(
                feature_names=feature_names,
                importance_values=importance_values,
                report_name="test_report.html"
            )
            print(f"✅ Report logged successfully: {artifact_path}")
            
            # Get run info
            run_id = mlflow.active_run().info.run_id
            print(f"✅ Run ID: {run_id}")
            
        except Exception as e:
            print(f"❌ Error logging report: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_plugin()
