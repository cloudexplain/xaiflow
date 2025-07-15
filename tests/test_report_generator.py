import unittest
from ce_mlflow_extension.report_generator import ReportGenerator

class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.report_generator = ReportGenerator()

    def test_generate_report(self):
        # Sample SHAP values and metadata for testing
        shap_values = [0.1, 0.2, 0.3]
        metadata = {'feature_names': ['Feature 1', 'Feature 2', 'Feature 3']}
        
        # Generate the report
        report = self.report_generator.generate_report(shap_values, metadata)
        
        # Check if the report is generated correctly
        self.assertIn('<html>', report)
        self.assertIn('Feature 1', report)
        self.assertIn('Feature 2', report)
        self.assertIn('Feature 3', report)

    def test_invalid_shap_values(self):
        # Test with invalid SHAP values
        shap_values = None
        metadata = {'feature_names': []}
        
        with self.assertRaises(ValueError):
            self.report_generator.generate_report(shap_values, metadata)

    def test_empty_metadata(self):
        # Test with empty metadata
        shap_values = [0.1, 0.2, 0.3]
        metadata = {'feature_names': []}
        
        report = self.report_generator.generate_report(shap_values, metadata)
        
        # Check if the report handles empty metadata gracefully
        self.assertIn('No features available', report)

if __name__ == '__main__':
    unittest.main()