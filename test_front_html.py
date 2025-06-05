import unittest
import os
from bs4 import BeautifulSoup


class TestFrontHTML(unittest.TestCase):
    """Unit tests for front.html file"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests"""
        cls.html_file_path = 'front.html'
        
        # Read the HTML file
        try:
            with open(cls.html_file_path, 'r', encoding='utf-8') as file:
                cls.html_content = file.read()
            cls.soup = BeautifulSoup(cls.html_content, 'html.parser')
        except FileNotFoundError:
            cls.html_content = None
            cls.soup = None
    
    def test_file_exists(self):
        """Test that front.html file exists"""
        self.assertTrue(os.path.exists(self.html_file_path), 
                       f"{self.html_file_path} file should exist")
    
    def test_html_content_not_empty(self):
        """Test that the HTML file is not empty"""
        self.assertIsNotNone(self.html_content, "HTML content should not be None")
        self.assertTrue(len(self.html_content.strip()) > 0, 
                       "HTML file should not be empty")
    
    def test_valid_html_structure(self):
        """Test that the HTML has valid basic structure"""
        self.assertIsNotNone(self.soup, "HTML should be parseable")
        
        # Check for DOCTYPE
        self.assertTrue(self.html_content.strip().startswith('<!DOCTYPE html>'), 
                       "HTML should start with DOCTYPE declaration")
        
        # Check for html tag
        html_tag = self.soup.find('html')
        self.assertIsNotNone(html_tag, "HTML should have <html> tag")
        
        # Check for head tag
        head_tag = self.soup.find('head')
        self.assertIsNotNone(head_tag, "HTML should have <head> tag")
        
        # Check for body tag
        body_tag = self.soup.find('body')
        self.assertIsNotNone(body_tag, "HTML should have <body> tag")
    
    def test_page_title(self):
        """Test that the page has a proper title"""
        title_tag = self.soup.find('title')
        self.assertIsNotNone(title_tag, "HTML should have a <title> tag")
        self.assertEqual(title_tag.text.strip(), "Symptom Checker", 
                        "Title should be 'Symptom Checker'")
    
    def test_bootstrap_css_included(self):
        """Test that Bootstrap CSS is properly included"""
        css_links = self.soup.find_all('link', {'rel': 'stylesheet'})
        bootstrap_css_found = False
        
        for link in css_links:
            href = link.get('href', '')
            if 'bootstrap' in href and 'css' in href:
                bootstrap_css_found = True
                break
        
        self.assertTrue(bootstrap_css_found, 
                       "Bootstrap CSS should be included")
    
    def test_main_heading(self):
        """Test that the main heading exists and is correct"""
        h1_tag = self.soup.find('h1')
        self.assertIsNotNone(h1_tag, "Page should have an <h1> tag")
        self.assertEqual(h1_tag.text.strip(), "Symptom Checker", 
                        "Main heading should be 'Symptom Checker'")
    
    def test_form_exists(self):
        """Test that the form element exists with correct attributes"""
        form_tag = self.soup.find('form')
        self.assertIsNotNone(form_tag, "Page should have a <form> tag")
        
        # Check form attributes
        self.assertEqual(form_tag.get('action'), 'diagnosis.html', 
                        "Form action should be 'diagnosis.html'")
        self.assertEqual(form_tag.get('method'), 'post', 
                        "Form method should be 'post'")
    
    def test_form_group_exists(self):
        """Test that the form group div exists"""
        form_group = self.soup.find('div', class_='form-group')
        self.assertIsNotNone(form_group, 
                           "Form should have a div with class 'form-group'")
    
    def test_label_exists(self):
        """Test that the label for the select element exists"""
        label_tag = self.soup.find('label', {'for': 'primary_problem'})
        self.assertIsNotNone(label_tag, 
                           "Form should have a label for 'primary_problem'")
        self.assertEqual(label_tag.text.strip(), "Select your primary problem:", 
                        "Label text should be 'Select your primary problem:'")
    
    def test_select_element(self):
        """Test that the select element exists with correct attributes"""
        select_tag = self.soup.find('select')
        self.assertIsNotNone(select_tag, "Form should have a <select> element")
        
        # Check select attributes
        self.assertEqual(select_tag.get('id'), 'primary_problem', 
                        "Select should have id 'primary_problem'")
        self.assertEqual(select_tag.get('name'), 'primary_problem', 
                        "Select should have name 'primary_problem'")
        self.assertIn('form-control', select_tag.get('class', []), 
                     "Select should have 'form-control' class")
    
    def test_option_elements(self):
        """Test that all required option elements exist"""
        select_tag = self.soup.find('select')
        options = select_tag.find_all('option') if select_tag else []
        
        self.assertEqual(len(options), 5, "Select should have 5 options")
        
        expected_options = [
            ('back_pain', 'Back Pain'),
            ('headache', 'Headache'),
            ('fever', 'Fever'),
            ('cough', 'Cough'),
            ('chest_pain', 'Chest Pain')
        ]
        
        for i, (expected_value, expected_text) in enumerate(expected_options):
            self.assertEqual(options[i].get('value'), expected_value, 
                           f"Option {i+1} should have value '{expected_value}'")
            self.assertEqual(options[i].text.strip(), expected_text, 
                           f"Option {i+1} should have text '{expected_text}'")
    
    def test_submit_button(self):
        """Test that the submit button exists with correct attributes"""
        submit_button = self.soup.find('button', {'type': 'submit'})
        self.assertIsNotNone(submit_button, 
                           "Form should have a submit button")
        
        # Check button classes
        button_classes = submit_button.get('class', [])
        self.assertIn('btn', button_classes, 
                     "Submit button should have 'btn' class")
        self.assertIn('btn-primary', button_classes, 
                     "Submit button should have 'btn-primary' class")
        
        # Check button text
        self.assertEqual(submit_button.text.strip(), "Submit", 
                        "Submit button text should be 'Submit'")
    
    def test_container_div(self):
        """Test that the main container div exists"""
        container_div = self.soup.find('div', class_='container')
        self.assertIsNotNone(container_div, 
                           "Page should have a div with class 'container'")
        
        # Check for mt-5 class
        container_classes = container_div.get('class', [])
        self.assertIn('mt-5', container_classes, 
                     "Container should have 'mt-5' class")
    
    def test_javascript_libraries(self):
        """Test that required JavaScript libraries are included"""
        script_tags = self.soup.find_all('script')
        
        # Check for jQuery
        jquery_found = False
        popper_found = False
        bootstrap_js_found = False
        
        for script in script_tags:
            src = script.get('src', '')
            if 'jquery' in src:
                jquery_found = True
            elif 'popper' in src:
                popper_found = True
            elif 'bootstrap' in src and 'js' in src:
                bootstrap_js_found = True
        
        self.assertTrue(jquery_found, "jQuery should be included")
        self.assertTrue(popper_found, "Popper.js should be included")
        self.assertTrue(bootstrap_js_found, "Bootstrap JS should be included")
    
    def test_form_accessibility(self):
        """Test form accessibility features"""
        # Check that label is properly associated with select
        label_tag = self.soup.find('label', {'for': 'primary_problem'})
        select_tag = self.soup.find('select', {'id': 'primary_problem'})
        
        self.assertIsNotNone(label_tag, "Label should exist")
        self.assertIsNotNone(select_tag, "Select should exist")
        self.assertEqual(label_tag.get('for'), select_tag.get('id'), 
                        "Label 'for' attribute should match select 'id'")
    
    def test_responsive_design(self):
        """Test that the page uses Bootstrap responsive classes"""
        container_div = self.soup.find('div', class_='container')
        self.assertIsNotNone(container_div, "Container div should exist")
        
        # Check for Bootstrap responsive classes
        form_group = self.soup.find('div', class_='form-group')
        self.assertIsNotNone(form_group, "Form group should exist")
        
        select_tag = self.soup.find('select', class_='form-control')
        self.assertIsNotNone(select_tag, "Select should have form-control class")
    
    def test_html_validation(self):
        """Test basic HTML validation rules"""
        # Check for proper nesting
        form_tag = self.soup.find('form')
        container_div = self.soup.find('div', class_='container')
        
        # Form should be inside container
        self.assertTrue(container_div.find('form') is not None, 
                       "Form should be inside container div")
        
        # Select should be inside form
        self.assertTrue(form_tag.find('select') is not None, 
                       "Select should be inside form")
    
    def test_no_inline_styles(self):
        """Test that no inline styles are used (good practice)"""
        elements_with_style = self.soup.find_all(attrs={'style': True})
        self.assertEqual(len(elements_with_style), 0, 
                        "No elements should have inline styles")


if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFrontHTML)
    
    # Run the tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")