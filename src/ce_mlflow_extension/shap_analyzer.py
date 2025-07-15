class ShapAnalyzer:
    def __init__(self, shap_values, feature_names):
        self.shap_values = shap_values
        self.feature_names = feature_names
        self.importance_scores = self.compute_importance_scores()

    def compute_importance_scores(self):
        """Compute importance scores based on SHAP values."""
        importance = self.shap_values.mean(axis=0)
        return dict(zip(self.feature_names, importance))

    def prepare_data_for_visualization(self):
        """Prepare data for visualization."""
        return {
            "shap_values": self.shap_values.tolist(),
            "importance_scores": self.importance_scores,
            "feature_names": self.feature_names
        }