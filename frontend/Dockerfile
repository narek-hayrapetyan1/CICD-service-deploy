FROM node:18-alpine

WORKDIR /frontend

COPY . .

RUN npm install -g http-server

CMD ["http-server", "-p", "3000"]

