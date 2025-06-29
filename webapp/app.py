import sys
import os
from flask import Flask, render_template, request, jsonify

# --- System Path Setup ---
# This ensures that the application can find and import modules from the parent 'app' directory.
# It adds the project's root directory to Python's path.
# For example, '.../story-idea-generator/webapp/app.py' needs to import from '.../story-idea-generator/app/'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Application Imports ---
# Import the necessary functions from your other Python modules.
from app.generator import create_story_prompt, load_data
from app.ai_integration import generate_story_idea

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Route to Serve the Main HTML Page ---
@app.route('/')
def index():
    """
    Renders the main user interface from the index.html template.
    """
    return render_template('index.html')

# --- API Route to Get Options for Dropdowns ---
@app.route('/get-options')
def get_options():
    """
    Loads the content for the dropdown menus from the JSON data files
    and returns it as a JSON object to the frontend.
    """
    try:
        genres = load_data('genres.json')
        themes = load_data('themes.json')
        characters = load_data('characters.json')
        
        # Check if data loaded correctly
        if not all([genres, themes, characters]):
            return jsonify({"error": "Failed to load one or more data files."}), 500
            
        return jsonify({
            'genres': genres,
            'themes': themes,
            'characters': characters
        })
    except Exception as e:
        print(f"Error in /get-options: {e}")
        return jsonify({"error": "An internal error occurred while fetching options."}), 500

# --- API Route to Generate the Story Idea ---
@app.route('/generate', methods=['POST'])
def generate():
    """
    Receives user selections from the frontend, creates a prompt,
    sends it to the Gemini API, and returns the generated story idea.
    """
    if not request.is_json:
        return jsonify({"error": "Invalid request: Content-Type must be application/json"}), 400

    data = request.get_json()
    genre = data.get('genre')
    theme = data.get('theme')
    character = data.get('character')

    if not all([genre, theme, character]):
        return jsonify({"error": "Missing required fields: genre, theme, and character are required."}), 400

    try:
        # 1. Create the detailed prompt using the generator module
        prompt = create_story_prompt(genre, theme, character)
        if "Error" in prompt:
             return jsonify({"error": prompt}), 500

        # 2. Get the story idea from the AI integration module
        story_idea = generate_story_idea(prompt)
        if "Error" in story_idea:
            return jsonify({"error": story_idea}), 500

        # 3. Return the successful result
        return jsonify({'story_idea': story_idea})
        
    except Exception as e:
        print(f"Error in /generate: {e}")
        return jsonify({"error": "An unexpected error occurred during story generation."}), 500

# --- Main Execution Block ---
if __name__ == '__main__':
    """
    Runs the Flask application.
    Setting debug=True enables auto-reloading when code changes.
    """
    app.run(debug=True)
