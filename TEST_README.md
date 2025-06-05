# Unit Tests for front.html

This directory contains unit tests for the `front.html` file in the RedFlagsBITS project.

## Overview

The test suite (`test_front_html.py`) provides comprehensive testing for the front.html file, which is a symptom checker form. The tests verify:

- HTML structure and validity
- Bootstrap CSS and JavaScript integration
- Form elements and their attributes
- Accessibility features
- Responsive design elements
- Content validation

## Test Coverage

The test suite includes the following test categories:

### 1. File and Structure Tests
- `test_file_exists`: Verifies the HTML file exists
- `test_html_content_not_empty`: Ensures the file is not empty
- `test_valid_html_structure`: Validates basic HTML structure (DOCTYPE, html, head, body tags)

### 2. Content Tests
- `test_page_title`: Verifies the page title is "Symptom Checker"
- `test_main_heading`: Checks the main H1 heading
- `test_bootstrap_css_included`: Ensures Bootstrap CSS is properly linked
- `test_javascript_libraries`: Verifies jQuery, Popper.js, and Bootstrap JS are included

### 3. Form Tests
- `test_form_exists`: Validates the form element and its attributes
- `test_form_group_exists`: Checks for Bootstrap form group structure
- `test_label_exists`: Verifies the label for the select element
- `test_select_element`: Tests the select dropdown attributes
- `test_option_elements`: Validates all 5 symptom options (Back Pain, Headache, Fever, Cough, Chest Pain)
- `test_submit_button`: Checks the submit button and its Bootstrap classes

### 4. Design and Accessibility Tests
- `test_container_div`: Verifies Bootstrap container structure
- `test_form_accessibility`: Checks proper label-input associations
- `test_responsive_design`: Validates Bootstrap responsive classes
- `test_html_validation`: Tests proper HTML nesting
- `test_no_inline_styles`: Ensures no inline styles are used (best practice)

## Prerequisites

Before running the tests, install the required dependencies:

```bash
pip install -r test-requirements.txt
```

The test dependencies include:
- `beautifulsoup4`: For HTML parsing and validation
- `lxml`: XML/HTML parser
- `html5lib`: HTML5 parser

## Running the Tests

### Run all tests:
```bash
python test_front_html.py
```

### Run with unittest module:
```bash
python -m unittest test_front_html.py -v
```

### Run specific test:
```bash
python -m unittest test_front_html.TestFrontHTML.test_form_exists -v
```

## Test Output

The test runner provides detailed output including:
- Individual test results
- Test summary with pass/fail counts
- Success rate percentage
- Detailed error messages for any failing tests

## Expected Results

All tests should pass if the `front.html` file is properly structured. The test suite validates that the HTML file:
- Contains all required elements
- Uses proper Bootstrap classes
- Has correct form structure
- Includes necessary JavaScript libraries
- Follows accessibility best practices

## Troubleshooting

If tests fail:
1. Check that `front.html` exists in the same directory as the test file
2. Verify the HTML structure matches the expected format
3. Ensure all required Bootstrap classes and attributes are present
4. Check that all 5 symptom options are correctly defined

## Contributing

When modifying `front.html`, ensure all tests continue to pass. If you add new features to the HTML file, consider adding corresponding tests to maintain coverage.