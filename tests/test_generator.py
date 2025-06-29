import unittest
import sys
import os
import json

# Add the parent directory to the Python path to allow sibling imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.generator import create_story_prompt, get_prompt_template, load_data

# Create dummy data and prompt files for testing to isolate tests from actual file system state
TEST_DATA_DIR = 'test_data'
TEST_PROMPTS_DIR = 'test_prompts'

class TestGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up dummy directories and files for tests."""
        # Create test directories
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        os.makedirs(TEST_PROMPTS_DIR, exist_ok=True)

        # Create dummy genres.json
        with open(os.path.join(TEST_DATA_DIR, 'genres.json'), 'w') as f:
            json.dump(["Sci-Fi", "Fantasy"], f)

        # Create dummy templates.json
        with open(os.path.join(TEST_PROMPTS_DIR, 'templates.json'), 'w') as f:
            json.dump({"story_idea_prompt": "Genre: {genre}, Theme: {theme}, Character: {character}"}, f)

    @classmethod
    def tearDownClass(cls):
        """Clean up dummy files and directories after tests."""
        # Remove dummy files
        os.remove(os.path.join(TEST_DATA_DIR, 'genres.json'))
        os.remove(os.path.join(TEST_PROMPTS_DIR, 'templates.json'))
        # Remove dummy directories
        os.rmdir(TEST_DATA_DIR)
        os.rmdir(TEST_PROMPTS_DIR)

    def test_load_data(self):
        """Tests that data files are loaded correctly."""
        # Temporarily mock the path construction in load_data to use our test directory
        original_dirname = os.path.dirname
        os.path.dirname = lambda path: TEST_DATA_DIR if 'data' in path else original_dirname(path)
        
        genres = load_data('genres.json')
        self.assertIsInstance(genres, list)
        self.assertEqual(genres, ["Sci-Fi", "Fantasy"])
        
        # Restore the original function
        os.path.dirname = original_dirname


    def test_get_prompt_template(self):
        """Tests that the prompt template is loaded correctly."""
        original_dirname = os.path.dirname
        os.path.dirname = lambda path: TEST_PROMPTS_DIR if 'prompts' in path else original_dirname(path)

        template = get_prompt_template()
        self.assertIsInstance(template, str)
        self.assertIn("{genre}", template)
        self.assertIn("{theme}", template)
        self.assertIn("{character}", template)
        
        os.path.dirname = original_dirname


    def test_create_story_prompt(self):
        """Tests that the story prompt is created correctly."""
        original_dirname = os.path.dirname
        os.path.dirname = lambda path: TEST_PROMPTS_DIR if 'prompts' in path else original_dirname(path)
        
        genre = "Fantasy"
        theme = "Betrayal"
        character = "A reluctant hero"
        
        prompt = create_story_prompt(genre, theme, character)
        
        expected_prompt = f"Genre: {genre}, Theme: {theme}, Character: {character}"
        self.assertEqual(prompt, expected_prompt)

        os.path.dirname = original_dirname
        
    def test_load_data_file_not_found(self):
        """Tests that loading a non-existent file returns an empty list."""
        data = load_data('non_existent_file.json')
        self.assertEqual(data, [])

    def test_get_prompt_template_file_not_found(self):
        """Tests that loading a non-existent template returns an empty string."""
        original_dirname = os.path.dirname
        # Point to a directory that exists but doesn't contain the file
        os.path.dirname = lambda path: 'tests' if 'prompts' in path else original_dirname(path)
        
        template = get_prompt_template()
        self.assertEqual(template, "")
        
        os.path.dirname = original_dirname


if __name__ == '__main__':
    unittest.main()
