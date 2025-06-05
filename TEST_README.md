# Langchain Backpain Notebook Tests

This directory contains comprehensive tests for the Langchain backpain notebook functionality, including both the basic symptom checker and the advanced SOAP note generation system.

## Test Files Overview

### 1. `test_backpain_langchain.py`
Tests for the basic backpain symptom checker functionality from `Backpain_langchain.ipynb`:
- LLM initialization and configuration
- Prompt template creation and validation
- Chain creation and setup
- Input processing and formatting
- Template content validation

### 2. `test_langchain_integration.py`
Integration tests for the more complex SOAP note system from `Lang_Soap.ipynb`:
- Complete symptom checker workflow
- SOAP note stage analyzer chain
- Medical conversation chain creation
- Conversation stage mapping
- Error handling scenarios

### 3. `run_tests.py`
Test runner script that:
- Discovers and runs all test files
- Provides detailed test output
- Generates comprehensive test reports
- Returns appropriate exit codes for CI/CD

## Setup and Installation

### Prerequisites
```bash
# Install test dependencies
pip install -r test_requirements.txt

# Or install individual packages
pip install pytest pytest-mock pytest-cov langchain openai python-dotenv mock
```

### Environment Setup
For tests that require OpenAI API access (optional):
```bash
# Create a .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

**Note**: The tests are designed to work with mocked dependencies, so an actual OpenAI API key is not required for running the test suite.

## Running Tests

### Option 1: Using the test runner script
```bash
python run_tests.py
```

### Option 2: Using pytest directly
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_backpain_langchain.py

# Run with coverage report
pytest --cov=. --cov-report=html
```

### Option 3: Using unittest
```bash
# Run specific test file
python -m unittest test_backpain_langchain.py -v

# Run all tests
python -m unittest discover -v
```

## Test Coverage

The test suite covers:

### Core Functionality
- ✅ LLM initialization with correct parameters
- ✅ Prompt template creation and validation
- ✅ Chain setup and configuration
- ✅ Input processing and formatting
- ✅ Complete workflow execution

### SOAP Note System
- ✅ Stage analyzer chain creation
- ✅ Medical conversation chain setup
- ✅ Conversation stage transitions
- ✅ Multi-stage workflow handling

### Error Handling
- ✅ Missing API key scenarios
- ✅ Invalid input handling
- ✅ Import error management

## Continuous Integration

To integrate these tests into your CI/CD pipeline, add the following to your workflow:

```yaml
- name: Run Langchain Tests
  run: |
    pip install -r test_requirements.txt
    python run_tests.py
```

## Contributing

When adding new functionality to the langchain notebooks:
1. Add corresponding tests to the appropriate test file
2. Ensure all tests pass before submitting changes
3. Update this README if new test categories are added
4. Maintain test coverage above 80%

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed via `test_requirements.txt`
2. **API Key Warnings**: These are expected when running without actual OpenAI credentials
3. **Mock Failures**: Verify that the langchain API hasn't changed significantly

### Getting Help

If you encounter issues with the tests:
1. Check that all dependencies are properly installed
2. Verify that the notebook files haven't been modified significantly
3. Review the test output for specific error messages
4. Consider updating the mock configurations if the langchain API has changed
