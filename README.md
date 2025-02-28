# Deploying and Running a Python Flask Application on Amazon Linux

## 1. Setting up the environment

### Install Python and Pip
Ensure Python and pip are installed on your Amazon Linux instance:

```bash
sudo yum install python3 -y
sudo yum install python3-pip -y
```

### Verify installation
Check the installed versions:

```bash
python3 --version
pip3 --version
```

## 2. Preparing the Flask application

### Sample Flask Application
Create a directory for your application:

```bash
mkdir sample-python
cd sample-python
```

Create the `app.py` file:

```bash
cat > app.py <<EOL
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
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

@app.route('/myapp/')
def get_system_info():
    node_ip = socket.gethostbyname(socket.gethostname())
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = platform.system() + " " + platform.release()
    cpu_count = os.cpu_count()
    memory_info = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    hostname = socket.gethostname()

    data = {
        "node_ip": node_ip,
        "date": current_date,
        "os": os_info,
        "cpu_count": cpu_count,
        "total_memory_bytes": memory_info,
        "message": "Hello from Amazon Linux EC2 instance!",
        "version": APP_VERSION,
        "hostname": hostname
    }
    app.logger.info(f"Request received. Response: {data}")
    return jsonify(data)

@app.route('/health')
def health_check():
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    app.logger.info(f"Health check request received. Response: {health_data}")
    return jsonify(health_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOL
```

### Create a requirements file

```bash
cat > requirements.txt <<EOL
Flask==2.3.2
EOL
```

## 3. Installing dependencies

Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

### Verify installed dependencies

To check installed packages:

```bash
pip3 freeze
```

Ensure `Flask==2.3.2` is listed.

## 4. Running the application

### Run the Flask application

Start the app using:

```bash
python3 app.py
```

### Access the application

Open your browser and use your EC2 instance's public IP and port 5000:

- **System Info Endpoint:** `http://<public-ip>:5000/myapp/`
- **Health Check Endpoint:** `http://<public-ip>:5000/health`

#### Example outputs:

- **System Info (`/myapp/`):**

```json
{
    "node_ip": "172.31.38.137",
    "date": "2025-02-28 12:34:56",
    "os": "Linux 4.14.256-197.484.amzn2.x86_64",
    "cpu_count": 2,
    "total_memory_bytes": 8123456000,
    "message": "Hello from Amazon Linux EC2 instance!",
    "version": "1.0.0",
    "hostname": "ip-172-31-38-137"
}
```

- **Health Check (`/health`):**

```json
{
    "status": "healthy",
    "timestamp": "2025-02-28 12:34:56"
}
```

## 5. Running the application in the background (nohup)

Run the Flask app using `nohup` to keep it running in the background:

```bash
nohup python3 app.py > app.log 2>&1 &
```

- `nohup`: Keeps the process running after logging out.
- `app.log`: Logs both stdout and stderr.
- `&`: Runs the process in the background.

### Check logs

View real-time logs:

```bash
tail -f app.log
```

## 6. Managing the Flask process

### Check running Python processes

Find the process ID (PID):

```bash
ps aux | grep app.py
```

### Kill the process

Using `kill`:

```bash
kill -9 <pid>
```

Or use `pkill` to kill by process name:

```bash
pkill -f app.py
```

### Kill the process using `grep` and `awk`

You can also kill the process directly by extracting the PID in one command:

```bash
kill -9 $(ps aux | grep app.py | grep -v grep | awk '{print $2}')
```

#### Explanation:
- `ps aux`: Lists all running processes.
- `grep app.py`: Filters the processes to only show those running `app.py`.
- `grep -v grep`: Excludes the `grep app.py` process itself from the results.
- `awk '{print $2}'`: Extracts the second column, which is the PID.
- `kill -9 $(...)`: Kills the process by passing the PID.

## 7. Additional commands

- **List all running processes:**

```bash
ps aux
```

- **Check open ports (to confirm Flask is listening on port 5000):**

```bash
sudo netstat -tuln | grep 5000
```

- **Validate EC2 instance IP (needed to access Flask in browser):**

```bash
curl http://checkip.amazonaws.com
```

## 8. Security Considerations

Ensure port 5000 is open in the EC2 security group:

1. Go to **EC2 Dashboard** > **Instances**.
2. Select your instance.
3. Click **Security** > **Security Groups**.
4. Edit **Inbound rules** and add:
   - Type: **Custom TCP**
   - Port Range: **5000**
   - Source: **0.0.0.0/0** (or restrict to your IP)

## 9. Conclusion

You have now set up a Flask application, verified dependencies, and managed processes on an Amazon Linux EC2 instance.

---
---
---

# User Data Script to Deploy Flask Application on Amazon Linux

## Introduction
This user data script automates the setup of a Flask application on a fresh Amazon Linux EC2 instance. It performs the following tasks:

- Installs necessary packages (Python, pip, git)
- Clones the Flask app from a public GitHub repository
- Installs dependencies
- Runs the Flask app using `nohup`

## User Data Script

Replace `<your-github-repo-url>` with the URL of your public GitHub repository.

```bash
#!/bin/bash
# Update packages
sudo yum update -y

# Install Python3, pip, and git
sudo yum install -y python3 python3-pip git

# Verify installations
python3 --version
pip3 --version
git --version

# Clone the Flask application from GitHub
cd /home/ec2-user
git clone <your-github-repo-url>

# Change to the app directory
cd sample-python

# Install Python dependencies
pip3 install -r requirements.txt

# Run the Flask application in the background
nohup python3 app.py > app.log 2>&1 &

# Ensure the application runs on startup (optional)
echo "cd /home/ec2-user/sample-python && nohup python3 app.py > app.log 2>&1 &" >> /etc/rc.local
chmod +x /etc/rc.local
```

## How to use the user data script

1. Launch a new EC2 instance.
2. In the **Configure instance** step, scroll down to the **Advanced details** section.
3. Paste the user data script into the **User data** text box.
4. Ensure the security group allows inbound traffic on port 5000.
5. Launch the instance.

## Verifying the deployment

Once the instance is running:

- SSH into the instance:

```bash
ssh -i <your-key.pem> ec2-user@<public-ip>
```

- Check if the app is running:

```bash
ps aux | grep app.py
```

- View logs:

```bash
tail -f /home/ec2-user/sample-python/app.log
```

## Access the application

Open a browser and go to:

- **System Info:** `http://<public-ip>:5000/myapp/`
- **Health Check:** `http://<public-ip>:5000/health`

Ensure port 5000 is open in the instance's security group.

## Conclusion
This user data script automates the deployment of your Flask application on Amazon Linux EC2 instances. Let me know if you want to enhance this with more automation steps, like adding a reverse proxy (Nginx) or using a process manager (like Supervisor)!


