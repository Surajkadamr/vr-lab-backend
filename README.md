# VR Image Generation Flask Backend

This backend provides an API for generating VR-related images using Google's Generative AI (Imagen).

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

3. Run the server:
   ```
   python app.py
   ```

The server will start on http://localhost:5000 by default.

## API Endpoints

### Generate Image
- **URL**: `/api/generate-image`
- **Method**: POST
- **Body**:
  ```json
  {
    "prompt": "Your image generation prompt here"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "imageData": "data:image/jpeg;base64,base64_encoded_image",
    "text": "Image generated successfully with Google Imagen"
  }
  ```

### Health Check
- **URL**: `/api/health`
- **Method**: GET
- **Response**:
  ```json
  {
    "status": "healthy",
    "message": "VR Image Generation API is running"
  }
  ```

### Test API Key
- **URL**: `/api/test`
- **Method**: GET
- **Response**:
  ```json
  {
    "status": "success",
    "message": "API key is working correctly",
    "text_response": "Response from Gemini"
  }
  ```

## Frontend Integration

Update your frontend fetch URL to point to this backend:

```javascript
// Example: Modify your frontend code to use this backend
const response = await fetch('http://localhost:5000/api/generate-image', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ prompt }),
});
``` 