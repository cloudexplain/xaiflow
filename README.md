# xaiflow

**Interactive Explainable AI Reports for MLflow**

> **Note**: This library is in early development and the API may change. Use with caution in production environments.

xaiflow integrates seamlessly with MLflow to generate interactive HTML reports for SHAP analysis. Instead of static charts and images, you get rich, interactive visualizations that stakeholders can explore and understand.

Here should the video go:
<video src="video/feature_showcase.mp4" controls width="600">
  Your browser does not support the video tag.
</video>

## What We're Trying to Achieve

Most ML workflows produce explanations as static images or basic charts, which creates several problems:
- Stakeholders can't interactively explore feature importance
- It's difficult to understand how different features contribute to predictions
- You can't dive deep into individual predictions and their explanations
- Sharing comprehensive model insights with non-technical teams is challenging

xaiflow solves this by providing a simple integration with MLflow that automatically generates interactive HTML reports. You get:
- Interactive feature importance charts that respond to clicks and filters
- SHAP value visualizations that show exactly how each feature contributes
- Deep dive analysis for specific predictions and feature interactions
- Professional HTML reports that work in any browser
- Zero configuration - works with existing MLflow workflows

## Quick Start

```python
import mlflow
from xaiflow import XaiflowPlugin

# Your existing MLflow training code
with mlflow.start_run():
    # Train your model...
    model = train_model(X, y)
    
    # Generate SHAP values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X)
    
    # Add interactive explainable AI reports
    plugin = XaiflowPlugin()
    plugin.log_xai_report(
        feature_names=X.columns.tolist(),
        shap_values=shap_values,
    )
```

That's it. Your MLflow experiment now includes an interactive HTML report that stakeholders can explore directly in their browser.

Or take a look at the [examples](examples).

## Project Structure

```
xaiflow/
├── src/xaiflow/                          # Main package
│   ├── __init__.py                     # Package exports
│   ├── mlflow_plugin.py                # MLflow integration
│   ├── report_generator.py             # HTML report generation
│   └── templates/                      # Frontend components
│       ├── report.html                 # Main HTML template
│       ├── assets/                     # Compiled frontend assets
│       │   ├── bundle.js               # Svelte + Chart.js bundle
│       │   ├── bundle.js.map           # Source mapping
│       │   └── cloudexplain_no_bg-2.png # Logo
│       ├── components/                 # Svelte components
│       │   ├── ChartManager.svelte     # Chart orchestration
│       │   ├── ImportanceChart2.svelte # Feature importance charts
│       │   ├── ScatterShapValues.svelte # SHAP scatter plots
│       │   ├── DeepDiveChart.svelte    # Deep dive analysis
│       │   └── DeepDiveManager.svelte  # Deep dive orchestration
│       └── utils/                      # Utilities
│           ├── utils.ts                # Helper functions
│           └── colormap.ts             # Color mapping utilities
├── tests/                              # Test suites
├── pyproject.toml                      # Package configuration
├── MANIFEST.in                         # Package file inclusion
└── README.md                           # This file
```

### Core Components

**MLflow Integration** (`mlflow_plugin.py`)
The `CEMLflowPlugin` class handles the integration with MLflow. The main method `log_xai_report()` processes SHAP values, manages feature encodings, and stores the generated reports as MLflow artifacts.

**Report Generation** (`report_generator.py`)
The `ReportGenerator` class converts SHAP data into interactive HTML reports using Jinja2 templating. It handles template loading, asset bundling, and data injection into the frontend components.

**Frontend Components**
Built with Svelte and Chart.js, these components create the interactive visualizations. The charts respond to user interactions like clicking, hovering, and filtering. The design is responsive and works across desktop, tablet, and mobile devices.

## Features

**Interactive Feature Importance**
Bar charts showing feature importance values with clickable features for filtering and exploration. Hover tooltips provide detailed information, and you can sort and filter the results.

**SHAP Value Visualizations**
Scatter plots show feature values versus SHAP values with color-coded points indicating feature impact. You can zoom and pan to explore specific regions and drill down into individual predictions.

**Deep Dive Analysis**
Feature interaction charts show how features work together. You can break down predictions for individual samples, compare across different predictions, and export results for further analysis.

**Stakeholder-Friendly Reports**
The HTML output works in any browser without dependencies. Reports are self-contained, print-friendly for presentations, and mobile-responsive.

## Installation

```bash
pip install xaiflow
```

For development:
```bash
git clone https://github.com/cloudexplain/xaiflow
cd xaiflow
pip install -e .
```

## Advanced Usage

**Custom Feature Encodings**
Handle categorical features with custom encodings:

```python
feature_encodings = {
    'category_feature': {0: 'Low', 1: 'Medium', 2: 'High'},
    'region': {0: 'North', 1: 'South', 2: 'East', 3: 'West'}
}

plugin.log_xai_report(
    feature_names=feature_names,
    shap_values=shap_values,
    feature_encodings=feature_encodings,
)
```

## Use Cases

- **Model Validation**: Ensure your model makes decisions for the right reasons
- **Stakeholder Communication**: Share model insights with non-technical teams
- **Model Debugging**: Identify and fix issues in model behavior
- **Feature Engineering**: Understand which features drive predictions

## Limitations

**Performance with Large Datasets**
The interactive reports are rendered entirely in the browser using JavaScript. If you pass very large SHAP value arrays (thousands of samples), the browser may become slow or unresponsive. For best performance, consider:
- Sampling your data to a reasonable size (typically 1000-5000 samples work well)
- Using representative subsets for stakeholder reports
- Creating separate technical reports with full datasets for detailed analysis

**Browser Compatibility**
The reports use modern JavaScript features and work best in recent versions of Chrome, Firefox, Safari, and Edge. Older browsers may not display charts correctly.

## Contributing

We welcome contributions. Please see our [Contributing Guide](CONTRIBUTING.md) for details.

If something is missing or you have further questions, feel free to reach out to: info@cloudexplain.eu

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Built on top of [MLflow](https://mlflow.org/) for experiment tracking, [SHAP](https://shap.readthedocs.io/) for model explanations, and powered by [Svelte](https://svelte.dev/) and [Chart.js](https://www.chartjs.org/) on the frontend.

---

Made by the [CloudExplain Team](https://cloudexplain.eu)

## Development Notes

- **All styling must go in `report.html`**: Do not use inline styles or Svelte `<style>` blocks for the main report UI. This is required because styles are not reliably handed over or injected from Svelte to the final HTML report. Always update or add CSS in `src/xaiflow/templates/report.html` for any UI/UX changes.
- **Always rebuild the frontend bundle before running Python tests**: The Svelte/JS bundle (`bundle.js`) must be up-to-date for the Python tests to work correctly. Before running any Python tests (e.g., Playwright or integration tests), always run:

  ```bash
  make build && python -m pytest tests/test_mlflow_plugin.py
  ```
  or, for all tests:
  ```bash
  make build && python -m pytest
  ```
- **Frontend changes require a rebuild**: Any change to Svelte components or frontend logic requires a new build of `bundle.js` to be reflected in the generated reports and tests.
- **UI/UX review**: When making UI changes, always check the result in the browser and ensure the layout matches the design intent. Use only relative units (rem, em, %) for all sizing and spacing in CSS.