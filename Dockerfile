# Base image with Node.js and Python
FROM node:18

# Install system dependencies: Python, pip, venv, and build tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv build-essential && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy Node.js files and install dependencies
COPY package*.json ./
RUN npm install

# Copy Python requirements and set up virtual environment
COPY requirements.txt ./
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Add the virtual environment to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy the rest of the application code
COPY . .

# Expose port if your app runs on a specific one (optional)
EXPOSE 3000

# Start the Node.js server
CMD ["node", "server.js"]
