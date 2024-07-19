#!/bin/bash

exec > /var/log/user-data.log 2>&1

# Update the package repository and install Docker
sudo yum update -y
sudo yum install -y docker

# Start and enable Docker service
sudo service docker start
sudo systemctl enable docker
sudo yum install -y libxcrypt-compat

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add the current user to the Docker group
sudo usermod -aG docker ec2-user

# Give necessary permissions to the Docker socket
sudo chmod 666 /var/run/docker.sock

# Change to the home directory
cd /home/ec2-user

# Create the application directory and move there
mkdir recipe-api-app
cd recipe-api-app

# Create necessary directories for Django application
mkdir -p code/myapp

# Download and extract your application code
aws s3 cp s3://recipeapi/recipeapi.zip recipe-api-app.zip
sudo yum install -y unzip
unzip recipe-api-app.zip -d .

# Give necessary permissions to the ec2-user for the application directory
sudo chown -R ec2-user:ec2-user /home/ec2-user/recipe-api-app
cd /home/ec2-user/recipe-api-app

docker-compose up -d 
