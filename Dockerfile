FROM node:18


RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean


WORKDIR /app


COPY package*.json ./
RUN npm install


COPY requirements.txt ./


RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


ENV PATH="/opt/venv/bin:$PATH"


COPY . .


EXPOSE 3000


CMD ["node", "server.js"]
