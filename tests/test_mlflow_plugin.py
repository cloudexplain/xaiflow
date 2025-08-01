import pytest
from pathlib import Path
from xaiflow.mlflow_plugin import XaiflowPlugin
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import shap
from typing import Callable
import mlflow

from playwright.sync_api import sync_playwright


def js_find_colorset() -> str:
    return """
        (node) => {
            const ctx = node.getContext('2d');
            const data = ctx.getImageData(0, 0, node.width, node.height).data;
            const colorSet = new Set();
            for (let i = 0; i < data.length; i += 4) {
                const r = data[i], g = data[i+1], b = data[i+2], a = data[i+3];
                colorSet.add(`${r},${g},${b},${a}`);
            }
            return Array.from(colorSet);
        }
    """

def store_report(html_content, filename="test_report.html"):
    """Helper function to store HTML content to a file."""
    outputs_dir = Path("tests/outputs")
    outputs_dir.mkdir(parents=True, exist_ok=True)
    html_path = outputs_dir / filename
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return html_path

def html_content_click_test(html_path: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir="tests/outputs/videos/")
        page = context.new_page()
        page.goto(f"file://{html_path.resolve()}")
        page.wait_for_selector(".importance-chart-container canvas")
        canvas = page.query_selector(".importance-chart-container canvas")
        assert canvas is not None, "Canvas not found in importance chart container"
        assert canvas.is_visible(), "Canvas is not visible"
        box = canvas.bounding_box()
        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2
        page.mouse.click(x, y)
        page.wait_for_timeout(1000)
        # Check if canvas is not empty
        is_empty = canvas.evaluate("""
        (node) => {
          const ctx = node.getContext('2d');
          const data = ctx.getImageData(0, 0, node.width, node.height).data;
          const totalPixels = data.length / 4;
          if (totalPixels === 0) return true;
          // Get first pixel color
          const r0 = data[0], g0 = data[1], b0 = data[2], a0 = data[3];
          let sameCount = 0;
          for (let i = 0; i < data.length; i += 4) {
            const r = data[i], g = data[i+1], b = data[i+2], a = data[i+3];
            if (r === r0 && g === g0 && b === b0 && a === a0) {
              sameCount++;
            }
          }
          return (sameCount / totalPixels) >= 0.9;
        }
        """)
        assert not is_empty, "Canvas is empty or nearly empty: 99% of pixels have the same color"
        # click "deepdive-button"
        page.wait_for_selector("#deepdive-button")
        page.click("#deepdive-button")
        # --- NEW: Check canvas by id 'deepdive-canvas' and get unique colors ---
        page.wait_for_selector("#deepdive-canvas")
        deepdive_canvas = page.query_selector("#deepdive-canvas")
        assert deepdive_canvas is not None, "Canvas with id 'deepdive-canvas' not found"
        assert deepdive_canvas.is_visible(), "Deepdive canvas is not visible"
        unique_colors = deepdive_canvas.evaluate(js_find_colorset())
        print(f"Unique colors in deepdive-canvas: {len(unique_colors)}")
        # For some reasons so many different colors were found, no bars shown 248, with bars 400 something
        assert len(unique_colors) > 300, "Deepdive canvas does not have multiple unique colors"

def save_and_click_canvas_wrapper(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        html_content = func(*args, **kwargs)
        html_path = store_report(html_content, func.__name__ + ".html")
        html_content_click_test(html_path)
    return wrapper

@save_and_click_canvas_wrapper
def test_categorical_feature_encodings():
    data = fetch_openml(data_id=196, as_frame=True)
    X = data.data.copy()[:100]
    y = data.target[:100]

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
    html_content = plugin._generate_html_content(
        importance_data={'features': list(X.columns), 'values': np.abs(shap_values.values).mean(axis=0).tolist()},
        shap_values=shap_values.values,
        feature_values=shap_values.data,
        base_values=shap_values.base_values[0],
        feature_encodings=feature_encodings,
        feature_names=list(X.columns),
    )
    return html_content

def test_categorical_feature_encodings2(mocker):
    data = fetch_openml(data_id=196, as_frame=True)
    X = data.data.copy()[:100]
    y = data.target[:100]

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
    experiment_name = "dummytest"
    mlflow.set_experiment(experiment_name=experiment_name)

    output_path = f"tests/outputs/test_categorical_feature_encodings.html"
    class DummyTmpFile:
        name = output_path
        def __enter__(self):
            self.name = output_path
            # import pdb; pdb.set_trace()  # Debugging breakpoint
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    mocker.patch("tempfile.NamedTemporaryFile", return_value=DummyTmpFile())
    mocker.patch("os.unlink")  # Prevent deletion

    # Optionally patch mlflow.log_artifact if you want to avoid real logging
    mocker.patch("mlflow.log_artifact")

    with mlflow.start_run(run_name="auto_mpg_test"):
        plugin.log_xai_report(
            shap_values=shap_values,
            feature_encodings=feature_encodings,
            feature_names=list(X.columns),
        )
        html_content_click_test(Path(output_path))


@save_and_click_canvas_wrapper
def test_no_feature_encodings():
    plugin = XaiflowPlugin()
    html_content = plugin._generate_html_content(
        importance_data={'features': ['Feature 1', 'Feature 2', 'Feature 3'], 'values': [0.1, 0.2, 0.3]},
        shap_values=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
        feature_values=[1.0, 2.0, 3.0],
        feature_encodings=None,
        feature_names=['Feature 1', 'Feature 2', 'Feature 3'],
    )
    return html_content


def test_classification_case(mocker):
    X, y = shap.datasets.adult(n_points=200)

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
    rfc = RandomForestClassifier()
    rfc.fit(X, y)
    ex = shap.TreeExplainer(rfc)
    shap_values = ex(X)
    plugin = XaiflowPlugin()

    feature_encodings = {}
    for col in categorical_cols:
        feature_encodings[col + '_encoded'] = dict(zip(range(len(label_encoders[col].classes_)), label_encoders[col].classes_))
    html_content = plugin._generate_html_content(
        importance_data={'features': list(X.columns), 'values': np.abs(shap_values.values).mean(axis=0).tolist()},
        shap_values=shap_values.values,
        feature_values=shap_values.data,
        base_values=shap_values.base_values[0],
        feature_encodings=feature_encodings,
        feature_names=list(X.columns),
    )
    experiment_name = "dummytest"
    mlflow.set_experiment(experiment_name=experiment_name)

    output_path = f"tests/outputs/test_classification_case.html"
    class DummyTmpFile:
        name = output_path
        def __enter__(self):
            self.name = output_path
            # import pdb; pdb.set_trace()  # Debugging breakpoint
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    mocker.patch("tempfile.NamedTemporaryFile", return_value=DummyTmpFile())
    mocker.patch("os.unlink")  # Prevent deletion

    # Optionally patch mlflow.log_artifact if you want to avoid real logging
    mocker.patch("mlflow.log_artifact")

    with mlflow.start_run(run_name="auto_mpg_test"):
        plugin.log_xai_report(
            shap_values=shap_values,
            feature_encodings=feature_encodings,
            feature_names=list(X.columns),
        )
        html_content_click_test(Path(output_path))
    # return html_content


def test_classification_case_check_list_feature(mocker):
    X, y = shap.datasets.adult(n_points=200)

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
    rfc = RandomForestClassifier()
    rfc.fit(X, y)
    ex = shap.TreeExplainer(rfc)
    shap_values = ex(X)
    plugin = XaiflowPlugin()

    feature_encodings = {}
    for col in categorical_cols:
        feature_encodings[col + '_encoded'] = dict(zip(range(len(label_encoders[col].classes_)), label_encoders[col].classes_))
    experiment_name = "dummytest"
    mlflow.set_experiment(experiment_name=experiment_name)

    output_path = f"tests/outputs/test_classification_case_check_list_feature.html"
    class DummyTmpFile:
        name = output_path
        def __enter__(self):
            self.name = output_path
            # import pdb; pdb.set_trace()  # Debugging breakpoint
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    mocker.patch("tempfile.NamedTemporaryFile", return_value=DummyTmpFile())
    mocker.patch("os.unlink")  # Prevent deletion

    # Optionally patch mlflow.log_artifact if you want to avoid real logging
    mocker.patch("mlflow.log_artifact")

    with mlflow.start_run(run_name="auto_mpg_test"):
        plugin.log_xai_report(
            shap_values=shap_values,
            feature_encodings=feature_encodings,
            feature_names=list(X.columns),
            group_labels=["Group 1", "Group 2", "Group 3", "Group 4"] * int(len(shap_values) / 4)  # Example group labels
        )
        html_content_click_test(Path(output_path))