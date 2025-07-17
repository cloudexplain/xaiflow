#!/usr/bin/env python3
"""
Simple test script to demonstrate Python to HTML data passing.
"""

import sys
import os

# Add the src directory to Python path so we can import our module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from xaiflow.report_generator import ReportGenerator


def main():
    print("Testing Python to HTML data passing...")
    
    # Create report generator
    generator = ReportGenerator()
    
    # Generate a simple report
    output_file = "simple_test_report.html"
    generator.generate_simple_report(output_file)
    
    print("\n" + "="*50)
    print("SUCCESS! Report generated.")
    print(f"Open '{output_file}' in your web browser to see the result.")
    print("You should see a random number that was passed from Python!")
    print("="*50)


if __name__ == "__main__":
    main()
