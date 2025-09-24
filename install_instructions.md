# Installation Instructions

This document provides detailed installation instructions for the Traffic Light Detection and Color Recognition project.

## Prerequisites

- Python 3.7 or higher
- Conda (recommended) or pip
- Git
- CUDA-compatible GPU (optional, for GPU acceleration)

## Dependencies

The project requires the following dependencies:

- **Protobuf 3.0.0+** - For protocol buffer support
- **Python-tk** - For GUI support
- **Pillow 1.0+** - For image processing
- **lxml** - For XML processing
- **tf Slim** - Included in TensorFlow models
- **Jupyter notebook** - For interactive development
- **Matplotlib** - For plotting and visualization
- **TensorFlow (>=1.12.0)** - Core deep learning framework
- **Cython** - For C extensions
- **contextlib2** - For context management
- **cocoapi** - For COCO dataset support

## Installation Methods

### Method 1: Conda Environment (Recommended)

1. **Create the conda environment:**
   ```bash
   conda env create -f environment-gpu.yml
   ```

2. **Activate the environment:**
   ```bash
   conda activate traffic-light-detection
   ```

### Method 2: Pip Installation

1. **Create a virtual environment (recommended):**
   ```bash
   python -m venv traffic-light-env
   source traffic-light-env/bin/activate  # On Windows: traffic-light-env\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Method 3: Automated Setup

Run the setup script:
```bash
python setup_environment.py
```

## TensorFlow Models Setup

1. **Clone the TensorFlow models repository:**
   ```bash
   git clone https://github.com/tensorflow/models.git
   ```

2. **Navigate to the models directory:**
   ```bash
   cd models/research
   ```

3. **Install protobuf and compile proto files:**
   ```bash
   # Install protobuf
   conda install protobuf
   # or
   pip install protobuf

   # Compile proto files (Windows)
   for /f %i in ('dir /b object_detection\protos\*.proto') do protoc object_detection\protos\%i --python_out=.

   # Compile proto files (Linux/Mac)
   protoc object_detection/protos/*.proto --python_out=.
   ```

4. **Add to PYTHONPATH:**
   ```bash
   # Windows
   set PYTHONPATH=%PYTHONPATH%;C:\path\to\models\research;C:\path\to\models\research\slim

   # Linux/Mac
   export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
   ```

## Verification

1. **Test the installation:**
   ```bash
   python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
   ```

2. **Run the main script:**
   ```bash
   python main.py
   ```

## Troubleshooting

### Common Issues

1. **Protobuf version conflicts:**
   - Ensure you're using protobuf 3.20.0 or compatible version
   - Recompile proto files after updating protobuf

2. **TensorFlow compatibility:**
   - The code has been updated for TensorFlow 2.x compatibility
   - Uses `tf.compat.v1` for backward compatibility

3. **CUDA/GPU issues:**
   - Install CUDA toolkit if using GPU
   - Install cuDNN for optimal performance
   - Use `tensorflow-gpu` for GPU support

4. **Import errors:**
   - Ensure PYTHONPATH includes the models/research directory
   - Check that all proto files are compiled
   - Verify all dependencies are installed

### Getting Help

If you encounter issues:

1. Check the error messages carefully
2. Verify all dependencies are installed correctly
3. Ensure Python version compatibility
4. Check TensorFlow installation: `python -c "import tensorflow as tf; print(tf.__version__)"`

## Project Structure

After installation, your project should have this structure:

```
Traffic-Light-Detection-And-Color-Recognition/
├── environment-gpu.yml          # Conda environment file
├── requirements.txt             # Pip requirements
├── setup_environment.py        # Automated setup script
├── main.py                     # Main detection script
├── mscoco_label_map.pbtxt      # COCO label map
├── test_images/                # Test images directory
├── output_images/              # Output images directory
├── utils/                      # Utility functions
└── models/                     # TensorFlow models (after setup)
    └── research/
        └── object_detection/
```

## Next Steps

1. Place your test images in the `test_images/` directory
2. Modify `main.py` to adjust detection parameters
3. Run the detection: `python main.py`
4. Check results in the `output_images/` directory