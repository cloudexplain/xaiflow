import os
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


# Simple test function
def test_report():
    """Test function to quickly generate a report"""
    generator = ReportGenerator()
    output_file = "test_report.html"
    generator.generate_simple_report(output_file)
    print(f"Open {output_file} in your browser to see the result!")


if __name__ == "__main__":
    test_report()