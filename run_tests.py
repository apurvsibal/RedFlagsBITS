#!/usr/bin/env python3
"""
Test runner script for front.html unit tests

This script runs the unit tests for front.html and provides a summary of results.
"""

import unittest
import sys
import os

def run_front_html_tests():
    """Run the front.html unit tests and display results"""
    
    # Check if test file exists
    if not os.path.exists('test_front_html.py'):
        print("Error: test_front_html.py not found!")
        print("Please ensure the test file is in the current directory.")
        return False
    
    # Check if front.html exists
    if not os.path.exists('front.html'):
        print("Warning: front.html not found!")
        print("Tests will fail if the target file doesn't exist.")
    
    print("Running front.html unit tests...")
    print("=" * 50)
    
    # Import and run tests
    try:
        from test_front_html import TestFrontHTML
        
        # Create test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(TestFrontHTML)
        
        # Run tests with verbose output
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Return success status
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"Error importing test module: {e}")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == '__main__':
    success = run_front_html_tests()
    sys.exit(0 if success else 1)