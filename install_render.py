#!/usr/bin/env python3
"""
Render Deployment Installation Script
This script helps prepare your environment for Render deployment
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Render requires Python 3.7 or higher")
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "main.py",
        "requirements-render.txt", 
        "render.yaml",
        "mscoco_label_map.pbtxt",
        "utils/label_map_util.py",
        "utils/visualization_utils.py"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def install_dependencies():
    """Install dependencies for local testing"""
    try:
        print("\nInstalling dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-render.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_imports():
    """Test if critical imports work"""
    try:
        print("\nTesting imports...")
        import fastapi
        import uvicorn
        import tensorflow as tf
        import cv2
        import numpy as np
        from PIL import Image
        print("✅ All critical imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def create_gitignore():
    """Create .gitignore for deployment"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Model files
*.tar.gz
faster_rcnn_resnet101_coco_11_06_2017/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment
.env
.venv
env/
venv/
"""
    
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore file")
    else:
        print("✅ .gitignore already exists")

def main():
    print("=" * 60)
    print("Render Deployment Preparation")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check required files
    files_ok, missing = check_required_files()
    if not files_ok:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        print("Please ensure all required files are present before deploying")
        sys.exit(1)
    
    # Create .gitignore
    create_gitignore()
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Dependency installation failed, but you can still deploy")
        print("   Render will install dependencies during build")
    
    # Test imports
    if not test_imports():
        print("\n⚠️  Some imports failed, but you can still deploy")
        print("   Render will install dependencies during build")
    
    print("\n" + "=" * 60)
    print("✅ Render deployment preparation completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Push your code to GitHub")
    print("2. Go to https://render.com")
    print("3. Create a new Web Service")
    print("4. Connect your GitHub repository")
    print("5. Use the following settings:")
    print("   - Build Command: pip install -r requirements-render.txt")
    print("   - Start Command: python main.py")
    print("   - Health Check Path: /health")
    print("\nYour API will be available at: https://your-app-name.onrender.com")

if __name__ == "__main__":
    main()