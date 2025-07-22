import mlflow
import shap
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import LabelEncoder


from xaiflow import XaiflowPlugin

# Load the Auto MPG dataset
data = fetch_openml(data_id=196, as_frame=True)
X = data.data.copy()
y = data.target

experiment_name = "Xaiflow_Auto_MPG_Test"
mlflow.set_experiment(experiment_name=experiment_name)
with mlflow.start_run(run_name="auto_mpg_test"):
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

    feature_encodings = {}
    for col in categorical_cols:
        feature_encodings[col + '_encoded'] = dict(zip(range(len(label_encoders[col].classes_)), label_encoders[col].classes_))
    feature_encodings = {'cylinders_encoded': {0: '3', 1: '4', 2: '5', 3: '6', 4: '8'},
                            'model_encoded': {0: 'Super 70', 1: 'Super 71', 2: 'Low 72', 3: 'Nice 73', 4: 'Great 74', 5: 'Lame 75', 6: 'High 76', 7: '77', 8: '78', 9: '79', 10: '80', 11: '81', 12: '82'},
                            'origin_encoded': {0: 'Afghanistan', 1: 'Bangladesh', 2: 'Maui'}}
    artifact_path = plugin.log_xai_report(
        feature_names=list(X.columns),
        shap_values=shap_values,
        feature_encodings=feature_encodings,
        group_labels=["Custom Group " + str(i % 4) for i in range(len(X))],
    )
    run_id = mlflow.active_run().info.run_id
    print(f"Run ID: {run_id}. If you are running mlflow locally use:\npython -m mlflow ui --port 5000\nThen open http://localhost:5000/#/experiments/{mlflow.get_experiment_by_name(experiment_name).experiment_id}/runs/{run_id} to view the report.",
          "Note: it's important to start mlflow in the directory in which you execute the notebook.")