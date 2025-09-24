# Render Deployment Guide

This guide will help you deploy the Traffic Light Detection FastAPI to Render.

## Prerequisites

1. A GitHub repository with your code
2. A Render account (free tier available)
3. Python 3.7 environment

## Deployment Steps

### Method 1: Using render.yaml (Recommended)

1. **Push your code to GitHub** with the following files:
   - `main.py` (FastAPI application)
   - `requirements-render.txt` (Render-optimized dependencies)
   - `render.yaml` (Render configuration)
   - `utils/` folder (utility functions)
   - `mscoco_label_map.pbtxt` (label map file)

2. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Sign up/Login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure the service:**
   - **Name**: `traffic-light-detection-api`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (or specify if in subfolder)
   - **Build Command**: `pip install -r requirements-render.txt`
   - **Start Command**: `python main.py`

4. **Environment Variables** (Optional):
   - `PYTHON_VERSION`: `3.7.9`
   - `PORT`: `8000` (Render will override this)

5. **Click "Create Web Service"**

### Method 2: Manual Configuration

If you prefer manual setup:

1. **Build Command:**
   ```bash
   pip install --upgrade pip && pip install -r requirements-render.txt
   ```

2. **Start Command:**
   ```bash
   python main.py
   ```

3. **Health Check Path:**
   ```
   /health
   ```

## Important Notes for Render

### Model Download
- The model will be downloaded automatically on first startup
- This may take 5-10 minutes during initial deployment
- The model file is ~77MB, so ensure you have sufficient storage

### Memory Requirements
- **Minimum**: 512MB RAM (Starter plan)
- **Recommended**: 1GB+ RAM for better performance
- The TensorFlow model requires significant memory

### Build Time
- Initial build may take 10-15 minutes
- Subsequent deployments will be faster (2-5 minutes)

## Testing Your Deployment

Once deployed, test your API:

1. **Health Check:**
   ```bash
   curl https://your-app-name.onrender.com/health
   ```

2. **API Documentation:**
   - Swagger UI: `https://your-app-name.onrender.com/docs`
   - ReDoc: `https://your-app-name.onrender.com/redoc`

3. **Test Detection:**
   ```python
   import requests
   import base64
   
   # Convert image to base64
   with open("test_image.jpg", "rb") as f:
       image_base64 = base64.b64encode(f.read()).decode('utf-8')
   
   # Test API
   response = requests.post("https://your-app-name.onrender.com/detect", json={
       "image_base64": image_base64,
       "description": "Test image"
   })
   
   print(response.json())
   ```

## Troubleshooting

### Common Issues:

1. **Build Fails:**
   - Check Python version compatibility
   - Ensure all dependencies are in requirements-render.txt
   - Check build logs for specific errors

2. **Model Download Fails:**
   - Check internet connectivity during build
   - Verify model URLs are accessible
   - Check build logs for download errors

3. **Memory Issues:**
   - Upgrade to a higher plan if needed
   - Consider using a lighter model
   - Check memory usage in Render dashboard

4. **Slow Response:**
   - Model loading takes time on first request
   - Consider implementing model caching
   - Monitor CPU and memory usage

### Logs and Monitoring:
- Check Render dashboard for logs
- Monitor resource usage
- Set up alerts for failures

## Cost Optimization

### Free Tier Limitations:
- 750 hours/month
- Sleeps after 15 minutes of inactivity
- Cold start takes 30-60 seconds

### Paid Plans:
- Always-on service
- Better performance
- More resources

## Security Considerations

1. **API Keys**: Don't hardcode sensitive information
2. **Rate Limiting**: Consider implementing rate limiting
3. **Input Validation**: API validates base64 input
4. **CORS**: Configure if needed for web applications

## Performance Tips

1. **Model Caching**: Model loads once and stays in memory
2. **Image Optimization**: Resize images before sending
3. **Batch Processing**: Use batch endpoint for multiple images
4. **Connection Pooling**: Reuse HTTP connections

## Support

- Render Documentation: https://render.com/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- TensorFlow Documentation: https://tensorflow.org/docs

## Example Environment Variables

```bash
# Optional environment variables
PYTHON_VERSION=3.7.9
PORT=8000
TF_CPP_MIN_LOG_LEVEL=2  # Reduce TensorFlow logging
```

## File Structure for Deployment

```
your-repo/
├── main.py                    # FastAPI application
├── requirements-render.txt    # Render dependencies
├── render.yaml               # Render configuration
├── Procfile                  # Alternative deployment
├── utils/                    # Utility functions
│   ├── label_map_util.py
│   └── visualization_utils.py
├── mscoco_label_map.pbtxt    # Label map
└── test_images/              # Test images (optional)
```