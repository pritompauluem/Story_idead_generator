import json
import os

def load_data(filename):
    """Loads JSON data from the data directory."""
    # Construct the full path to the file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(base_dir), 'data')
    filepath = os.path.join(data_dir, filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}.")
        return []

def get_prompt_template():
    """Loads the prompt template from the prompts directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_dir = os.path.join(os.path.dirname(base_dir), 'prompts')
    filepath = os.path.join(prompts_dir, 'templates.json')
    try:
        with open(filepath, 'r') as f:
            templates = json.load(f)
            return templates.get("story_idea_prompt", "")
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return ""
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}.")
        return ""


def create_story_prompt(genre, theme, character):
    """Creates a story prompt by filling the template with the given elements."""
    template = get_prompt_template()
    if not template:
        return "Error: Could not load prompt template."
    
    return template.format(genre=genre, theme=theme, character=character)

