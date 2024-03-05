# # Use the official lightweight Node.js 16 image.
# # https://hub.docker.com/_/node
# FROM node:17-slim

# # Create and change to the app directory.
# WORKDIR /usr/src/app

# # Copy application dependency manifests to the container image.
# # A wildcard is used to ensure both package.json AND package-lock.json are copied.
# # Copying this separately prevents re-running npm install on every code change.
# COPY package*.json ./

# # Install production dependencies.
# RUN npm install --omit=dev

# # Copy local code to the container image.
# COPY . ./ 

# # Run the web service on container startup.
# CMD [ "npm", "start" ]


# Use the official Node.js 17 slim-bullseye image with Python pre-installed.
FROM node:17-slim

# Create and change to the app directory.
WORKDIR /usr/src/app

# Copy application dependency manifests to the container image.
COPY package*.json ./
COPY requirements.txt ./

# Install Node.js production dependencies.
RUN npm install --only=production

# Install Python and Python dependencies.
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Install additional Node.js dependency.
RUN npm install uuid

# Copy local code to the container image.
COPY . ./

# Run the web service on container startup.
CMD [ "npm", "start" ]
