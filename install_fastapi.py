"""
Installation script for FastAPI dependencies
Run this script to install the required FastAPI packages
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    print("Installing FastAPI dependencies...")
    print("=" * 50)
    
    packages = [
        "fastapi>=0.68.0,<0.100.0",
        "uvicorn[standard]>=0.15.0,<0.25.0", 
        "python-multipart>=0.0.5,<0.1.0",
        "requests>=2.25.0"  # For testing
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("=" * 50)
    print(f"Installation completed: {success_count}/{len(packages)} packages installed successfully")
    
    if success_count == len(packages):
        print("\n🎉 All dependencies installed successfully!")
        print("You can now run the API server with: python main.py")
    else:
        print("\n⚠️  Some packages failed to install. Please check the errors above.")

if __name__ == "__main__":
    main()