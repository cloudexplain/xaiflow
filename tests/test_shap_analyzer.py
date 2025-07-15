import unittest
from ce_mlflow_extension.shap_analyzer import ShapAnalyzer

class TestShapAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = ShapAnalyzer()

    def test_process_shap_values(self):
        shap_values = [0.1, 0.2, 0.3]
        metadata = {'feature_names': ['feature1', 'feature2', 'feature3']}
        processed_data = self.analyzer.process_shap_values(shap_values, metadata)
        self.assertEqual(len(processed_data), 3)
        self.assertIn('feature1', processed_data)
        self.assertIn('feature2', processed_data)
        self.assertIn('feature3', processed_data)

    def test_compute_importance_scores(self):
        shap_values = [0.1, 0.2, 0.3]
        importance_scores = self.analyzer.compute_importance_scores(shap_values)
        self.assertEqual(len(importance_scores), 3)
        self.assertAlmostEqual(importance_scores[0], 0.1)
        self.assertAlmostEqual(importance_scores[1], 0.2)
        self.assertAlmostEqual(importance_scores[2], 0.3)

    def test_prepare_data_for_visualization(self):
        shap_values = [0.1, 0.2, 0.3]
        metadata = {'feature_names': ['feature1', 'feature2', 'feature3']}
        visualization_data = self.analyzer.prepare_data_for_visualization(shap_values, metadata)
        self.assertEqual(len(visualization_data['shap_values']), 3)
        self.assertEqual(visualization_data['feature_names'], ['feature1', 'feature2', 'feature3'])

if __name__ == '__main__':
    unittest.main()