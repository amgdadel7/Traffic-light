#!/usr/bin/env python3
"""
Test script to verify port binding works correctly
"""

import os
import sys
import time
import threading
import requests
from main import app
import uvicorn

def test_port_binding():
    """Test if the server binds to the correct port"""
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Testing port binding on port {port}...")
    
    # Start server in a separate thread
    def run_server():
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Server successfully bound to port {port}")
            print(f"✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to server on port {port}: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("Testing environment...")
    
    port = os.environ.get("PORT", "8000")
    print(f"PORT environment variable: {port}")
    
    python_version = os.environ.get("PYTHON_VERSION", "Not set")
    print(f"PYTHON_VERSION: {python_version}")
    
    render_env = os.environ.get("RENDER", "Not set")
    print(f"RENDER environment: {render_env}")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Port Binding Test")
    print("=" * 50)
    
    # Test environment
    test_environment()
    print()
    
    # Test port binding
    success = test_port_binding()
    
    print("=" * 50)
    if success:
        print("✅ All tests passed! Ready for Render deployment.")
    else:
        print("❌ Tests failed. Check the issues above.")
    print("=" * 50)