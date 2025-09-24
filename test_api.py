"""
Test script for Traffic Light Detection FastAPI
This script demonstrates how to use the API with base64 encoded images
"""

import base64
import requests
import json
from PIL import Image
import io

def image_to_base64(image_path):
    """Convert image file to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_single_image(api_url, image_path):
    """Test single image detection"""
    print(f"Testing image: {image_path}")
    
    # Convert image to base64
    image_base64 = image_to_base64(image_path)
    
    # Prepare request
    payload = {
        "image_base64": image_base64,
        "description": f"Test image: {image_path}"
    }
    
    try:
        # Send request
        response = requests.post(f"{api_url}/detect", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Result: {result['command']}")
            print(f"   Confidence: {result['confidence']:.2f}")
            print(f"   Message: {result['message']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_batch_images(api_url, image_paths):
    """Test batch image detection"""
    print(f"Testing batch of {len(image_paths)} images")
    
    # Prepare batch request
    images_data = []
    for image_path in image_paths:
        image_base64 = image_to_base64(image_path)
        images_data.append({
            "image_base64": image_base64,
            "description": f"Batch test: {image_path}"
        })
    
    try:
        # Send batch request
        response = requests.post(f"{api_url}/detect-batch", json=images_data)
        
        if response.status_code == 200:
            results = response.json()["results"]
            for i, result in enumerate(results):
                if "error" in result:
                    print(f"❌ Image {i}: Error - {result['error']}")
                else:
                    print(f"✅ Image {i}: {result['command']} (confidence: {result['confidence']:.2f})")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
    
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_health_check(api_url):
    """Test API health"""
    try:
        response = requests.get(f"{api_url}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Health: {result['status']}")
            print(f"   Model loaded: {result['model_loaded']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check exception: {e}")

if __name__ == "__main__":
    # API URL
    API_URL = "http://localhost:8000"
    
    print("=" * 60)
    print("Traffic Light Detection API Test")
    print("=" * 60)
    
    # Test health check
    print("\n1. Testing API Health...")
    test_health_check(API_URL)
    
    # Test single images
    print("\n2. Testing single images...")
    test_images = [
        "test_images/img_1.jpg",
        "test_images/img_2.jpg",
        "test_images/img_3.jpg"
    ]
    
    for img_path in test_images:
        test_single_image(API_URL, img_path)
        print()
    
    # Test batch detection
    print("\n3. Testing batch detection...")
    test_batch_images(API_URL, test_images)
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)