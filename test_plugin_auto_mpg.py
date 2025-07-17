#!/usr/bin/env python3
"""
Simple test for the CE MLflow Extension Plugin using the Auto MPG dataset
"""

import mlflow
import numpy as np
import sys
import os
import shap
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import LabelEncoder


try:
    from xaiflow import XaiflowPlugin
    print("✅ Successfully imported CEMLflowPlugin")
except Exception as e:
    print(f"❌ Error importing plugin: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

def test_plugin():
    """Test the MLflow plugin functionality with Auto MPG dataset"""
    mlflow.set_experiment("Plugin_Test_AutoMPG")
    with mlflow.start_run(run_name="auto_mpg_test"):
        # Load Auto MPG dataset
        # data = fetch_openml(data_id=40999, as_frame=True)
        data = fetch_openml(data_id=196, as_frame=True)
        X = data.data.copy()
        y = data.target

        # Identify categorical columns
        categorical_cols = [col for col in X.columns if X[col].dtype == 'category' or X[col].dtype == 'object']
        numeric_cols = [col for col in X.columns if col not in categorical_cols]

        label_encoders = {}
        # Fill missing values manually
        for col in numeric_cols:
            X[col] = X[col].astype(float).fillna(X[col].mean())
        for col in categorical_cols:
            le = LabelEncoder()
            X[col + '_encoded'] = le.fit_transform(X[col].astype(str))  # convert to string in case of NaNs
            label_encoders[col] = le  # Save encoder if needed later

        # Train model
        rfc = RandomForestRegressor()
        rfc.fit(X, y)
        ex = shap.TreeExplainer(rfc)
        shap_values = ex(X)
        
        plugin = XaiflowPlugin()
        print("✅ Plugin initialized successfully")

        feature_encodings = {}
        for col in categorical_cols:
            feature_encodings[col + '_encoded'] = dict(zip(range(len(label_encoders[col].classes_)), label_encoders[col].classes_))
        feature_encodings = {'cylinders_encoded': {0: '3', 1: '4', 2: '5', 3: '6', 4: '8'},
                             'model_encoded': {0: 'Super 70', 1: 'Super 71', 2: 'Low 72', 3: 'Nice 73', 4: 'Great 74', 5: 'Lame 75', 6: 'High 76', 7: '77', 8: '78', 9: '79', 10: '80', 11: '81', 12: '82'},
                             'origin_encoded': {0: 'Afghanistan', 1: 'Bangladesh', 2: 'Maui'}}
        try:
            artifact_path = plugin.log_feature_importance_report(
                feature_names=list(X.columns),
                shap_values=shap_values,
                report_name="test_report_auto_mpg.html",
                feature_encodings=feature_encodings
            )
            print(f"✅ Report logged successfully: {artifact_path}")
            run_id = mlflow.active_run().info.run_id
            print(f"✅ Run ID: {run_id}")
        except Exception as e:
            print(f"❌ Error logging report: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_plugin()
