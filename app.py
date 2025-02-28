from flask import Flask, jsonify
from datetime import datetime
import socket
import platform
import os
import logging

app = Flask(__name__)

# Application version
APP_VERSION = "1.0.0"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Write logs to a file
        logging.StreamHandler()         # Print logs to the terminal
    ]
)

@app.route('/myapp/')
def get_system_info():
    # Get system information
    node_ip = socket.gethostbyname(socket.gethostname())
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = platform.system() + " " + platform.release()
    cpu_count = os.cpu_count()
    memory_info = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # Total physical memory in bytes
    hostname = socket.gethostname()  # Get the hostname

    # Create JSON response
    data = {
        "node_ip": node_ip,
        "date": current_date,
        "os": os_info,
        "cpu_count": cpu_count,
        "total_memory_bytes": memory_info,
        "message": "Hello from Amazon Linux EC2 instance!",
        "version": APP_VERSION,  # Add application version
        "hostname": hostname     # Add hostname
    }

    # Log the request
    app.logger.info(f"Request received. Response: {data}")

    return jsonify(data)

@app.route('/health')
def health_check():
    # Simple health check response
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Log the health check request
    app.logger.info(f"Health check request received. Response: {health_data}")

    return jsonify(health_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
