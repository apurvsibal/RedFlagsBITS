#!/usr/bin/env python3
"""
Test runner for the Langchain Backpain notebook tests.

This script runs all tests related to the langchain backpain functionality
and provides a comprehensive test report.
"""

import unittest
import sys
import os
from io import StringIO


def run_all_tests():
    """Run all test suites and return results."""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load test suites
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Create a test runner with detailed output
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        descriptions=True,
        failfast=False
    )
    
    # Run the tests
    result = runner.run(suite)
    
    # Print results
    output = stream.getvalue()
    print(output)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    print("Running Langchain Backpain Notebook Tests...")
    print("="*70)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
