# Traffic Light Detection FastAPI

This FastAPI application provides traffic light detection and color recognition functionality. It receives base64-encoded images and returns "Go" or "Stop" commands based on the detected traffic light colors.

## Features

- **Single Image Detection**: Send one image and get Go/Stop command
- **Batch Detection**: Send multiple images at once
- **Base64 Support**: Accepts base64-encoded images
- **Health Check**: Monitor API status and model loading
- **Automatic Model Download**: Downloads and extracts TensorFlow model automatically

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Health Check
- **GET** `/health`
- Returns API status and model loading status

### 2. Single Image Detection
- **POST** `/detect`
- **Request Body**:
```json
{
  "image_base64": "base64_encoded_image_string",
  "description": "Optional description"
}
```
- **Response**:
```json
{
  "command": "Go" or "Stop",
  "confidence": 0.95,
  "message": "Description of detection result"
}
```

### 3. Batch Image Detection
- **POST** `/detect-batch`
- **Request Body**:
```json
[
  {
    "image_base64": "base64_encoded_image_string_1",
    "description": "Image 1"
  },
  {
    "image_base64": "base64_encoded_image_string_2", 
    "description": "Image 2"
  }
]
```
- **Response**:
```json
{
  "results": [
    {
      "image_index": 0,
      "command": "Go",
      "confidence": 0.95,
      "message": "No red or yellow traffic light detected"
    }
  ]
}
```

## Usage Examples

### Python Example
```python
import base64
import requests

# Convert image to base64
with open("test_image.jpg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

# Send request
payload = {
    "image_base64": image_base64,
    "description": "Test image"
}

response = requests.post("http://localhost:8000/detect", json=payload)
result = response.json()

print(f"Command: {result['command']}")
print(f"Confidence: {result['confidence']}")
```

### cURL Example
```bash
# Convert image to base64 first
IMAGE_BASE64=$(base64 -i test_image.jpg)

# Send request
curl -X POST "http://localhost:8000/detect" \
     -H "Content-Type: application/json" \
     -d "{\"image_base64\": \"$IMAGE_BASE64\", \"description\": \"Test image\"}"
```

### JavaScript Example
```javascript
// Convert image to base64
function imageToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = error => reject(error);
    });
}

// Send request
async function detectTrafficLight(imageFile) {
    const imageBase64 = await imageToBase64(imageFile);
    
    const response = await fetch('http://localhost:8000/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            image_base64: imageBase64,
            description: 'Web image'
        })
    });
    
    const result = await response.json();
    console.log('Command:', result.command);
    console.log('Confidence:', result.confidence);
}
```

## Testing

Run the test script to verify the API functionality:

```bash
python test_api.py
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Model Information

The API uses the Faster R-CNN ResNet101 COCO model for object detection. The model is automatically downloaded on first run if not present.

## Error Handling

The API includes comprehensive error handling:
- Invalid base64 images
- Model loading failures
- Network connectivity issues
- Image processing errors

## Notes

- The API detects red and yellow traffic lights and returns "Stop"
- Green traffic lights or no traffic lights return "Go"
- Images are automatically converted to RGB format
- The model supports various image formats (JPEG, PNG, etc.)