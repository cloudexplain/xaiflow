# ce-mlflow-extension

## Overview
The `ce-mlflow-extension` is a Python library designed to generate HTML reports that visualize SHAP values and associated metadata. It leverages Svelte for the frontend and Chart.js for rendering interactive charts.

## Features
- Generates HTML reports displaying SHAP values.
- Includes an importance chart to highlight feature significance.
- Presents metadata in a structured format.

## Project Structure
```
ce-mlflow-extension
├── src
│   └── ce_mlflow_extension
│       ├── __init__.py
│       ├── report_generator.py
│       ├── shap_analyzer.py
│       └── templates
│           ├── report.html
│           ├── components
│           │   ├── ImportanceChart.svelte
│           │   ├── ShapChart.svelte
│           │   └── MetadataTable.svelte
│           └── assets
│               ├── app.js
│               └── styles.css
├── tests
│   ├── __init__.py
│   ├── test_report_generator.py
│   └── test_shap_analyzer.py
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

## Installation
To install the required dependencies, run:
```
pip install -r requirements.txt
```

## Usage
1. Import the `ReportGenerator` and `ShapAnalyzer` classes from the library.
2. Use `ShapAnalyzer` to process SHAP values and extract metadata.
3. Generate a report using `ReportGenerator` and render it in your web application.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.