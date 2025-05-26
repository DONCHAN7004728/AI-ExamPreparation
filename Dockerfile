# Use Node.js as the base image (includes npm)
FROM node:18

# Install Python 3, pip, and venv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy Node.js files and install npm dependencies
COPY package*.json ./
RUN npm install

# Copy Python requirements
COPY requirements.txt ./

# Create Python virtual environment and install dependencies inside it
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Add the virtual environment to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy the rest of the project files
COPY . .

# Expose your app port (optional)
EXPOSE 3000

# Start your Node.js app
CMD ["node", "server.js"]
