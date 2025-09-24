#!/usr/bin/env python3
"""
Setup script for Traffic Light Detection and Color Recognition project.
This script helps set up the environment and install dependencies.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible. Please use Python 3.7+")
        return False

def install_conda_environment():
    """Install conda environment from yml file."""
    if not os.path.exists("environment-gpu.yml"):
        print("✗ environment-gpu.yml not found")
        return False
    
    return run_command("conda env create -f environment-gpu.yml", "Creating conda environment")

def install_pip_requirements():
    """Install pip requirements."""
    if not os.path.exists("requirements.txt"):
        print("✗ requirements.txt not found")
        return False
    
    return run_command("pip install -r requirements.txt", "Installing pip requirements")

def setup_tensorflow_models():
    """Setup TensorFlow models directory structure."""
    print("\nSetting up TensorFlow models directory...")
    
    # Create models directory structure
    models_dir = "models"
    research_dir = os.path.join(models_dir, "research")
    object_detection_dir = os.path.join(research_dir, "object_detection")
    
    try:
        os.makedirs(object_detection_dir, exist_ok=True)
        print("✓ Created models directory structure")
        
        # Note: User needs to clone the TensorFlow models repository
        print("\n⚠️  IMPORTANT: You need to clone the TensorFlow models repository:")
        print("git clone https://github.com/tensorflow/models.git")
        print("Then copy the object_detection directory to models/research/")
        
        return True
    except Exception as e:
        print(f"✗ Failed to create directory structure: {e}")
        return False

def main():
    """Main setup function."""
    print("Traffic Light Detection and Color Recognition - Environment Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\nChoose installation method:")
    print("1. Conda environment (recommended)")
    print("2. Pip requirements only")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    success = True
    
    if choice in ["1", "3"]:
        success &= install_conda_environment()
    
    if choice in ["2", "3"]:
        success &= install_pip_requirements()
    
    # Setup TensorFlow models
    setup_tensorflow_models()
    
    if success:
        print("\n" + "=" * 60)
        print("✓ Environment setup completed successfully!")
        print("\nNext steps:")
        print("1. Clone TensorFlow models repository:")
        print("   git clone https://github.com/tensorflow/models.git")
        print("2. Copy object_detection directory to models/research/")
        print("3. Install protobuf and compile proto files")
        print("4. Add models/research to your PYTHONPATH")
        print("5. Run: python main.py")
    else:
        print("\n" + "=" * 60)
        print("✗ Environment setup encountered errors. Please check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()