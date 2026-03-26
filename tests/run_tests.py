"""
Test runner script for Infrastructure Health Agent
"""

import unittest
import sys
import os
from io import StringIO

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_all_tests():
    """Run all test cases and return results"""
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
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
    
    # Get the output
    output = stream.getvalue()
    
    return result, output


def print_test_summary(result, output):
    """Print a summary of test results"""
    print("=" * 70)
    print("INFRASTRUCTURE HEALTH AGENT - TEST RESULTS")
    print("=" * 70)
    
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED!")
    
    print("\n" + "=" * 70)
    print("DETAILED OUTPUT:")
    print("=" * 70)
    print(output)
    
    # Print failures and errors if any
    if result.failures:
        print("\n" + "=" * 70)
        print("FAILURES:")
        print("=" * 70)
        for test, traceback in result.failures:
            print(f"\nFAIL: {test}")
            print("-" * 50)
            print(traceback)
    
    if result.errors:
        print("\n" + "=" * 70)
        print("ERRORS:")
        print("=" * 70)
        for test, traceback in result.errors:
            print(f"\nERROR: {test}")
            print("-" * 50)
            print(traceback)


def run_specific_test_module(module_name):
    """Run tests for a specific module"""
    try:
        suite = unittest.TestLoader().loadTestsFromName(module_name)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return result.wasSuccessful()
    except Exception as e:
        print(f"Error running tests for {module_name}: {e}")
        return False


def main():
    """Main function to run tests"""
    if len(sys.argv) > 1:
        # Run specific test module
        module_name = sys.argv[1]
        print(f"Running tests for module: {module_name}")
        success = run_specific_test_module(module_name)
        sys.exit(0 if success else 1)
    else:
        # Run all tests
        result, output = run_all_tests()
        print_test_summary(result, output)
        sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
