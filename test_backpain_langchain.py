import unittest
from unittest.mock import patch, MagicMock
import warnings
import sys
import os

# Add the current directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestBackpainLangchain(unittest.TestCase):
    """Test suite for the Backpain Langchain notebook functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        warnings.filterwarnings('ignore')
        
    def tearDown(self):
        """Clean up after each test method."""
        pass

    @patch('builtins.input')
    @patch('langchain.chat_models.ChatOpenAI')
    @patch('langchain.chains.LLMChain')
    def test_symptom_checker_basic_functionality(self, mock_llm_chain, mock_chat_openai, mock_input):
        """Test the basic functionality of the symptom checker."""
        # Mock user input
        mock_input.return_value = "back pain, stiffness"
        
        # Mock LLM response
        mock_chain_instance = MagicMock()
        mock_chain_instance.run.return_value = "Based on your symptoms of back pain and stiffness, this could indicate muscle strain or poor posture. Consider rest, gentle stretching, and if symptoms persist, consult a healthcare provider."
        mock_llm_chain.return_value = mock_chain_instance
        
        # Mock ChatOpenAI
        mock_llm_instance = MagicMock()
        mock_chat_openai.return_value = mock_llm_instance
        
        # Import and execute the symptom checker logic
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate
        from langchain.chains import LLMChain
        
        llm = ChatOpenAI(temperature=0)
        
        backpain_template = """You are a professional doctor. \
You are great at answering questions about various diagnosis in a concise \
and easy to understand manner. \
If you are asked for a particular type of symptom you answer it with its description, possible diagnosis, symptoms, causes, risk factors, and treatments. \
When you don't know the answer to a question, you admit that you don't know.

Here is a question:
{input}"""
        
        prompt_template = backpain_template
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Test the symptom checker function logic
        selected_symptoms = mock_input.return_value
        input_text = " ".join(selected_symptoms.split(","))
        
        # Verify the chain was created correctly
        self.assertIsNotNone(chain)
        mock_chat_openai.assert_called_once_with(temperature=0)
        
        # Test input processing
        expected_input = "back pain  stiffness"
        self.assertEqual(input_text, expected_input)

    @patch('langchain.chat_models.ChatOpenAI')
    def test_llm_initialization(self, mock_chat_openai):
        """Test that the LLM is initialized correctly."""
        from langchain.chat_models import ChatOpenAI
        
        llm = ChatOpenAI(temperature=0)
        
        mock_chat_openai.assert_called_once_with(temperature=0)
        self.assertIsNotNone(llm)

    def test_prompt_template_creation(self):
        """Test that the prompt template is created correctly."""
        from langchain.prompts import ChatPromptTemplate
        
        backpain_template = """You are a professional doctor. \
You are great at answering questions about various diagnosis in a concise \
and easy to understand manner. \
If you are asked for a particular type of symptom you answer it with its description, possible diagnosis, symptoms, causes, risk factors, and treatments. \
When you don't know the answer to a question, you admit that you don't know.

Here is a question:
{input}"""
        
        prompt = ChatPromptTemplate.from_template(template=backpain_template)
        
        self.assertIsNotNone(prompt)
        self.assertIn("{input}", backpain_template)

    @patch('langchain.chat_models.ChatOpenAI')
    @patch('langchain.chains.LLMChain')
    def test_chain_creation(self, mock_llm_chain, mock_chat_openai):
        """Test that the LLM chain is created correctly."""
        from langchain.chat_models import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate
        from langchain.chains import LLMChain
        
        # Mock the LLM
        mock_llm_instance = MagicMock()
        mock_chat_openai.return_value = mock_llm_instance
        
        # Mock the chain
        mock_chain_instance = MagicMock()
        mock_llm_chain.return_value = mock_chain_instance
        
        llm = ChatOpenAI(temperature=0)
        
        backpain_template = """You are a professional doctor. \
You are great at answering questions about various diagnosis in a concise \
and easy to understand manner. \
If you are asked for a particular type of symptom you answer it with its description, possible diagnosis, symptoms, causes, risk factors, and treatments. \
When you don't know the answer to a question, you admit that you don't know.

Here is a question:
{input}"""
        
        prompt = ChatPromptTemplate.from_template(template=backpain_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Verify chain creation
        mock_llm_chain.assert_called_once()
        self.assertIsNotNone(chain)

    def test_input_processing(self):
        """Test that user input is processed correctly."""
        # Test various input formats
        test_cases = [
            ("back pain, stiffness", "back pain  stiffness"),
            ("headache,nausea,dizziness", "headache nausea dizziness"),
            ("fever", "fever"),
            ("joint pain, swelling, redness", "joint pain  swelling  redness")
        ]
        
        for input_symptoms, expected_output in test_cases:
            with self.subTest(input_symptoms=input_symptoms):
                processed_input = " ".join(input_symptoms.split(","))
                self.assertEqual(processed_input, expected_output)

    def test_template_contains_required_elements(self):
        """Test that the template contains all required elements for medical diagnosis."""
        backpain_template = """You are a professional doctor. \
You are great at answering questions about various diagnosis in a concise \
and easy to understand manner. \
If you are asked for a particular type of symptom you answer it with its description, possible diagnosis, symptoms, causes, risk factors, and treatments. \
When you don't know the answer to a question, you admit that you don't know.

Here is a question:
{input}"""
        
        # Check that template contains key medical elements
        self.assertIn("professional doctor", backpain_template)
        self.assertIn("diagnosis", backpain_template)
        self.assertIn("symptoms", backpain_template)
        self.assertIn("causes", backpain_template)
        self.assertIn("risk factors", backpain_template)
        self.assertIn("treatments", backpain_template)
        self.assertIn("{input}", backpain_template)
        self.assertIn("don't know", backpain_template)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
