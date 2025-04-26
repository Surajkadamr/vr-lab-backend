"""
VR Image Generation Flask Backend
This application provides API endpoints for generating images and text using Google's Generative AI
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import json
import re

# Load environment variables
load_dotenv()

# Configure API key
api_key = 'AIzaSyChPNLGqiMKC7-GVsrrgiWL8Sdx7IGNA-A'


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """API endpoint to generate images using Google's Generative AI"""
    try:
        # Get the prompt from the request
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400
            
        prompt = data['prompt']
        
        print(f"Generating image for prompt: {prompt}...")
        
        # Generate content with the image generation model
        try:
            # Initialize the client
            client = genai.Client(api_key=api_key)
            
            # Generate the image
            response = client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="16:9"
                ),
            )
            
            # Process the response
            if response.generated_images:
                # Get the first generated image
                generated_image = response.generated_images[0]
                
                # Convert the image bytes to base64 for sending over HTTP
                image_bytes = generated_image.image.image_bytes
                mime_type = generated_image.image.mime_type or 'image/png'
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                
                # Return the image data as base64
                return jsonify({
                    'success': True,
                    'imageData': f"data:{mime_type};base64,{base64_image}",
                    'text': 'Image generated successfully with Google Gemini'
                })
            else:
                return jsonify({'error': 'No images generated'}), 500
                
        except Exception as model_error:
            print(f"Model error: {str(model_error)}")
            
            # Fallback to text model
            text_model = genai.GenerativeModel('gemini-1.5-pro')
            text_response = text_model.generate_content(
                f"I couldn't generate an image for '{prompt}', but here's a description of what it might look like:"
            )
            
            return jsonify({
                'success': False,
                'text': text_response.text,
                'error': f"Image generation failed: {str(model_error)}. Using text description instead."
            }), 400
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return jsonify({
            'error': 'Failed to generate image',
            'message': str(e)
        }), 500


@app.route('/api/generate-image-prompt', methods=['POST'])
def generate_image_prompt():
    """API endpoint to generate an image prompt from a paragraph"""
    try:
        # Get the paragraph from the request
        data = request.get_json()
        if not data or 'experimentDetails' not in data:
            return jsonify({'error': 'Paragraph is required'}), 400
        
        experimentDetails = data['experimentDetails']
        
        # Initialize the client
        client = genai.Client(api_key=api_key)
        
        # Prepare the prompt
        prompt_request = f"""
        Imagine an interactive vr lab station where the student stands inside a circular table with an open entryway. The table is filled with various experiment-related items, each corresponding to specific chapters of study. The user can reach out, grab objects, and interact with them to conduct hands-on experiments. The setup should support multiple experiments covering the key intents of the chapters, ensuring an immersive and educational experience. If a circular table is not feasible, AI can suggest an alternative rectangular table with an open entry design that maintains accessibility and engagement.generate a prompt for an image generation AI to illustrate the following paragraph from an lab experiment content:
        
        "{experimentDetails}"
        
        Imagen usage guidelines:
        - Images must adhere to safety guidelines and avoid harmful content
        - Images should be accurate, detailed, and educational
        - Content should be appropriate for students
        
        Your prompt should be short and concise, accurate.
        It should be in the style of a vr lab experiments.
        Return ONLY the prompt text, nothing else.
        """
        
        # Generate the prompt using Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt_request)
        
        # Return the generated prompt
        return jsonify({
            'success': True,
            'prompt': response.text.strip()
        })
    
    except Exception as e:
        print(f"Error generating image prompt: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running"""
    return jsonify({
        'status': 'healthy',
        'message': 'VR Image Generation API is running'
    })

# Add a simple test endpoint to verify the API key is working
@app.route('/api/test', methods=['GET'])
def test_api():
    """Test endpoint to verify the API key is working"""
    try:
        # Test text generation
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello, world!")
        
        return jsonify({
            'status': 'success',
            'message': 'API key is working correctly',
            'text_response': response.text
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'API key test failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
