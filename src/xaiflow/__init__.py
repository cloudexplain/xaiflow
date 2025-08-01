"""
xaiflow Package

This package provides MLflow integration for generating interactive HTML reports
with SHAP analysis using Svelte and Chart.js.
"""

from .mlflow_plugin import XaiflowPlugin

__version__ = "0.1.0"
__author__ = "CloudExplain Team"
__email__ = "tobias@cloudexplain.eu"

__all__ = ["CEMLflowPlugin"]