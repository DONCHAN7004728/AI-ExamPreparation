# Start from a base Node.js image with Python support
FROM node:18

# Install Python and tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv build-essential

# Set working directory
WORKDIR /app

# Copy and install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy Python requirements
COPY requirements.txt ./

# ✅ Create virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# ✅ Install Python packages inside virtual env
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Start your Node.js server
CMD ["node", "server.js"]
