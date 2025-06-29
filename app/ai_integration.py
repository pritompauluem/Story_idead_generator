import os
import google.generativeai as genai

def configure_ai():
    """Configures the Generative AI model with the API key."""
    # The API key is hardcoded here as requested.
    api_key = "Enter YOUR Gemini API key"
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")
    genai.configure(api_key=api_key)

def generate_story_idea(prompt):
    """Generates a story idea using the Gemini API."""
    try:
        configure_ai()
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        # Handle cases where the response might not have text
        if response.parts:
            return response.text
        else:
            # Check for safety ratings or other reasons for no content
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return f"Content blocked due to: {response.prompt_feedback.block_reason.name}"
            return "The model did not generate any content. Please try a different prompt."
            
    except Exception as e:
        print(f"An error occurred during AI generation: {e}")
        return f"Error: Could not generate a story idea. {e}"

