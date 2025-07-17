import os
import json
import random
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


class ReportGenerator:
    def __init__(self):
        # Get the directory where this file is located
        self.template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        # Set up Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
    
    def generate_simple_report(self, output_path="report.html"):
        """
        Generate a simple HTML report with a random number.
        
        Args:
            output_path (str): Path where the HTML file should be saved
        """
        # Generate some test data
        random_number = random.randint(1, 1000)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Load the template
        template = self.env.get_template('report.html')
        
        # Render the template with data
        html_content = template.render(
            random_number=random_number,
            timestamp=current_time
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Report generated successfully!")
        print(f"Random number: {random_number}")
        print(f"Output file: {output_path}")
        
        return output_path
    
    def generate_importance_report(self, output_path="importance_report.html"):
        """
        Generate an HTML report with feature importance data.
        
        Args:
            output_path (str): Path where the HTML file should be saved
        """
        # Generate some test importance data
        random_number = random.randint(1, 1000)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Sample feature importance data
        feature_names = [
            "Age", "Income", "Credit_Score", "Debt_Ratio", 
            "Employment_Years", "Loan_Amount", "Property_Value"
        ]

        shap_values = [
            [0.2, 0.4, 0.5, 0.6, 0.1, 0.2, 1],
            [-0.2, -0.4, -0.5, -0.6, -0.1, -0.2, -1],
            [-0.2, -0.4, -0.5, -0.6, -0.1, -0.2, -1]
        ]
        
        # Generate random importance values (normalized to sum to 1)
        importance_values = [random.uniform(0, 1) for _ in feature_names]
        # Normalize so they sum to 1 (typical for importance scores)
        total = sum(importance_values)
        importance_values = [v/total for v in importance_values]
        
        # Prepare data for JavaScript (JSON format)
        importance_data = {
            "features": feature_names,
            "values": importance_values
        }
        
        # Load the template
        template = self.env.get_template('report.html')
        
        # Render the template with data
        html_content = template.render(
            random_number=random_number,
            timestamp=current_time,
            importance_data=json.dumps(importance_data),  # Convert to JSON string
            shap_values=json.dumps(shap_values),  # Convert to JSON string
            importance_values=json.dumps(importance_values),  # Convert to JSON string
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        import pdb; pdb.set_trace()
        with open('test_report.hmtl', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Importance report generated successfully!")
        print(f"Random number: {random_number}")
        print(f"Features: {feature_names}")
        print(f"Output file: {output_path}")
        
        return output_path


# Simple test function
def test_report():
    """Test function to quickly generate a report"""
    generator = ReportGenerator()
    output_file = "test_report.html"
    generator.generate_simple_report(output_file)
    print(f"Open {output_file} in your browser to see the result!")


if __name__ == "__main__":
    test_report()