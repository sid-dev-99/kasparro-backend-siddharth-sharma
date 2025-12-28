#!/bin/bash

# setup_cloud_vm.sh
# Run this script on your fresh Ubuntu Cloud Server (AWS EC2, DigitalOcean, etc.)
# Usage: sudo ./setup_cloud_vm.sh

set -e

echo ">>> Updating system..."
apt-get update && apt-get upgrade -y

echo ">>> Installing Docker..."
apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce

echo ">>> Installing Docker Compose..."
curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo ">>> Docker setup complete!"

# Check if we are in the project directory
if [ -f "docker-compose.yml" ]; then
    echo ">>> Starting the application..."
    docker-compose up --build -d
    echo ">>> Application started!"
    echo ">>> API is available at http://$(curl -s ifconfig.me):8000"
    echo ">>> API Key: test-key (Default)"
else
    echo ">>> WARNING: docker-compose.yml not found."
    echo ">>> Please upload your project files to this server and run 'docker-compose up --build -d'"
fi
