#!/usr/bin/env python3

from src.ce_mlflow_extension.report_generator import ReportGenerator

def test_importance_report():
    """Test generating an HTML report with feature importance chart."""
    print("Testing ImportanceChart integration...")
    
    # Create report generator
    generator = ReportGenerator()
    
    # Generate report with importance data
    output_file = generator.generate_importance_report("test_importance_report.html")
    
    print("\n" + "="*50)
    print("SUCCESS! ImportanceChart report generated.")
    print(f"Open '{output_file}' in your web browser to see:")
    print("1. Random number displayed in traditional HTML")
    print("2. Interactive feature importance chart (Svelte + Chart.js)")
    print("3. Simple Svelte component")
    print("="*50)

if __name__ == "__main__":
    test_importance_report()
