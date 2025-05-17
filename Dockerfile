FROM node:18


RUN apt-get update && apt-get install -y python3 python3-pip

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY requirements.txt ./
RUN pip3 install --break-system-packages -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["node", "server.js"]