FROM node:18

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev build-essential

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Node.js dependencies
RUN npm install

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Start server
CMD ["node", "server.js"]
