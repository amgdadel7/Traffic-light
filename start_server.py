#!/usr/bin/env python3
"""
Alternative startup script for Render deployment
This script ensures proper port binding and logging
"""

import os
import sys
import uvicorn
from main import app

def main():
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    
    print("=" * 60)
    print("Traffic Light Detection FastAPI Server")
    print("=" * 60)
    print(f"Port: {port}")
    print(f"Host: 0.0.0.0")
    print(f"Environment: {os.environ.get('RENDER', 'local')}")
    print("=" * 60)
    
    # Start the server
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True,
            server_header=False,
            date_header=False
        )
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()