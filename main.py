##### Author - Nilesh Chopda (Modified for FastAPI)
##### Project - Traffic Light Detection and Color Recognition using Tensorflow Object Detection API

### Import Important Libraries
import numpy as np
import os
import urllib.request
import tarfile
import tensorflow as tf
from PIL import Image
from os import path
from utils import label_map_util
from utils import visualization_utils as vis_util
import cv2
import base64
import io
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn

# FastAPI app instance
app = FastAPI(title="Traffic Light Detection API", 
              description="API for detecting traffic lights and determining Go/Stop commands",
              version="1.0.0")

# Global variables for model
detection_graph = None
category_index = None
sess = None

### Function To Detect Red and Yellow Color
def detect_red_and_yellow(img, Threshold=0.01):
    """
    detect red and yellow
    :param img:
    :param Threshold:
    :return:
    """
    desired_dim = (30, 90)  # width, height
    img = cv2.resize(np.array(img), desired_dim, interpolation=cv2.INTER_LINEAR)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # lower mask (0-10)
    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red1 = np.array([170, 70, 50])
    upper_red1 = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)

    # defining the Range of yellow color
    lower_yellow = np.array([21, 39, 64])
    upper_yellow = np.array([40, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    # red pixels' mask
    mask = mask0 + mask1 + mask2

    # Compare the percentage of red values
    rate = np.count_nonzero(mask) / (desired_dim[0] * desired_dim[1])

    if rate > Threshold:
        return True
    else:
        return False

### Loading Image Into Numpy Array
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

### Read Traffic Light objects
def read_traffic_lights_object(image, boxes, scores, classes, max_boxes_to_draw=20, min_score_thresh=0.5,
                               traffic_ligth_label=10):
    im_width, im_height = image.size
    stop_flag = False
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores[i] > min_score_thresh and classes[i] == traffic_ligth_label:
            ymin, xmin, ymax, xmax = tuple(boxes[i].tolist())
            (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                          ymin * im_height, ymax * im_height)
            crop_img = image.crop((left, top, right, bottom))

            if detect_red_and_yellow(crop_img):
                stop_flag = True

    return stop_flag

### Pydantic models for API
class ImageRequest(BaseModel):
    image_base64: str
    description: str = "Base64 encoded image for traffic light detection"

class DetectionResponse(BaseModel):
    command: str
    confidence: float
    message: str

### Initialize model function
def initialize_model():
    global detection_graph, category_index, sess
    
    MODEL_NAME = 'faster_rcnn_resnet101_coco_11_06_2017'
    MODEL_FILE = MODEL_NAME + '.tar.gz'
    DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    PATH_TO_LABELS = 'mscoco_label_map.pbtxt'
    NUM_CLASSES = 90

    # Download and extract model if needed
    if path.isdir(MODEL_NAME) is False:
        if not path.exists(MODEL_FILE):
            print(f"Downloading {MODEL_FILE}...")
            
            # Try multiple download URLs
            download_urls = [
                DOWNLOAD_BASE + MODEL_FILE,
                f"https://storage.googleapis.com/download.tensorflow.org/models/object_detection/{MODEL_FILE}",
                f"https://github.com/tensorflow/models/raw/master/research/object_detection/test_images/{MODEL_FILE}"
            ]
            
            download_success = False
            for i, url in enumerate(download_urls):
                try:
                    print(f"Trying download URL {i+1}: {url}")
                    urllib.request.urlretrieve(url, MODEL_FILE)
                    print("Download completed!")
                    download_success = True
                    break
                except Exception as e:
                    print(f"Download attempt {i+1} failed: {e}")
                    if i < len(download_urls) - 1:
                        print("Trying next URL...")
                    continue
            
            if not download_success:
                print("\n" + "="*60)
                print("AUTOMATIC DOWNLOAD FAILED")
                print("="*60)
                print("Please manually download the model file:")
                print(f"1. Go to: https://github.com/tensorflow/models")
                print(f"2. Search for: {MODEL_FILE}")
                print(f"3. Or try: https://storage.googleapis.com/download.tensorflow.org/models/object_detection/{MODEL_FILE}")
                print(f"4. Download the file and place it in: {os.getcwd()}")
                print(f"5. Then restart the API")
                print("="*60)
                return False
        else:
            print(f"Model file {MODEL_FILE} already exists, skipping download...")
        
        # Extract the model
        print(f"Extracting {MODEL_FILE}...")
        try:
            tar_file = tarfile.open(MODEL_FILE)
            for file in tar_file.getmembers():
                file_name = os.path.basename(file.name)
                if 'frozen_inference_graph.pb' in file_name:
                    tar_file.extract(file, os.getcwd())
            tar_file.close()
            print("Model extraction completed!")
        except Exception as e:
            print(f"Extraction failed: {e}")
            print("The tar.gz file might be corrupted. Please delete it and try again.")
            return False

    # Load the model
    print("Loading TensorFlow model...")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    # Load label map
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    # Create session
    tf.compat.v1.disable_eager_execution()
    print("Model loaded successfully!")
    return True

### FastAPI Routes
@app.get("/")
async def root():
    return {"message": "Traffic Light Detection API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": detection_graph is not None}

@app.post("/detect", response_model=DetectionResponse)
async def detect_traffic_light(request: ImageRequest):
    """
    Detect traffic light in base64 encoded image and return Go/Stop command
    """
    global detection_graph, category_index, sess
    
    if detection_graph is None or category_index is None or sess is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please check server logs.")
    
    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        image_np = load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)
        
        # Get model tensors
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        
        # Run detection
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
        
        # Check for traffic lights
        stop_flag = read_traffic_lights_object(image, np.squeeze(boxes), np.squeeze(scores),
                                               np.squeeze(classes).astype(np.int32))
        
        # Determine command
        if stop_flag:
            command = "Stop"
            message = "Red or yellow traffic light detected"
            confidence = float(np.max(scores))
        else:
            command = "Go"
            message = "No red or yellow traffic light detected"
            confidence = float(np.max(scores))
        
        return DetectionResponse(
            command=command,
            confidence=confidence,
            message=message
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@app.post("/detect-batch")
async def detect_traffic_lights_batch(images: List[ImageRequest]):
    """
    Detect traffic lights in multiple base64 encoded images
    """
    results = []
    for i, img_request in enumerate(images):
        try:
            result = await detect_traffic_light(img_request)
            results.append({
                "image_index": i,
                "command": result.command,
                "confidence": result.confidence,
                "message": result.message
            })
        except Exception as e:
            results.append({
                "image_index": i,
                "error": str(e)
            })
    
    return {"results": results}

### Startup event
@app.on_event("startup")
async def startup_event():
    print("Starting Traffic Light Detection API...")
    success = initialize_model()
    if not success:
        print("Failed to initialize model. API will not function properly.")
    else:
        print("API ready to accept requests!")

### Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    global sess
    if sess is not None:
        sess.close()
        print("Model session closed.")

if __name__ == "__main__":
    print("Starting Traffic Light Detection FastAPI Server...")

    uvicorn.run(app, host="0.0.0.0", port=8000)
