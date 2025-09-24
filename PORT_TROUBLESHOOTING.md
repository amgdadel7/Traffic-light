# Port Detection Troubleshooting Guide

## Issue: "No open ports detected" on Render

This error occurs when Render cannot detect which port your application is listening on. Here are the solutions:

## ✅ **Solution 1: Use the Updated Files**

I've updated your files to fix this issue:

1. **`main.py`** - Updated with proper port binding
2. **`start_server.py`** - Alternative startup script with explicit logging
3. **`render.yaml`** - Updated configuration

## 🔧 **Solution 2: Manual Render Configuration**

If using manual setup in Render dashboard:

### Build Command:
```bash
pip install --upgrade pip && pip install -r requirements-render.txt
```

### Start Command:
```bash
python start_server.py
```

### Health Check Path:
```
/health
```

### Environment Variables:
- `PYTHON_VERSION`: `3.7.9`
- (Don't set PORT - Render sets this automatically)

## 🧪 **Solution 3: Test Locally First**

Before deploying, test locally:

```bash
# Test port binding
python test_port.py

# Test with specific port
PORT=8000 python start_server.py

# Test health endpoint
curl http://localhost:8000/health
```

## 🔍 **Solution 4: Debug Steps**

### 1. Check Render Logs
- Go to your Render dashboard
- Click on your service
- Check the "Logs" tab
- Look for port binding messages

### 2. Verify Port Binding
Your app should show:
```
Starting Traffic Light Detection FastAPI Server on port 8000...
Server will be available at: http://0.0.0.0:8000
```

### 3. Check Health Endpoint
Test: `https://your-app-name.onrender.com/health`

Should return:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## 🚨 **Common Issues & Fixes**

### Issue 1: App starts but port not detected
**Fix:** Ensure you're using `host="0.0.0.0"` not `host="localhost"`

### Issue 2: Port environment variable not set
**Fix:** Render sets PORT automatically, don't override it

### Issue 3: App crashes before binding
**Fix:** Check model download and dependencies

### Issue 4: Health check fails
**Fix:** Ensure `/health` endpoint returns 200 status

## 📋 **Complete Working Configuration**

### render.yaml:
```yaml
services:
  - type: web
    name: traffic-light-detection-api
    env: python
    region: oregon
    plan: starter
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements-render.txt
    startCommand: python start_server.py
    healthCheckPath: /health
    autoDeploy: true
```

### start_server.py:
```python
import os
import uvicorn
from main import app

port = int(os.environ.get("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
```

## 🔄 **Deployment Steps**

1. **Push all files to GitHub**
2. **Create new Web Service on Render**
3. **Connect GitHub repository**
4. **Use the configuration above**
5. **Deploy and monitor logs**

## 📞 **If Still Not Working**

1. **Check Render logs** for specific error messages
2. **Try the alternative startup script** (`start_server.py`)
3. **Verify all dependencies** are installed correctly
4. **Test locally** with the same configuration

## 🎯 **Expected Behavior**

When working correctly, you should see:
- ✅ Build completes successfully
- ✅ App starts and binds to port
- ✅ Health check passes
- ✅ API endpoints respond
- ✅ Swagger UI available at `/docs`

## 📊 **Monitoring**

- **Render Dashboard**: Monitor resource usage
- **Logs**: Check for errors and warnings
- **Health Check**: Verify `/health` endpoint
- **API Docs**: Test at `/docs` endpoint