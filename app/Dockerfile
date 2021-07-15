
FROM node:12.18.0-alpine as build
WORKDIR /app
COPY package.json .
COPY yarn.lock .
RUN yarn install
COPY . .
CMD ["yarn", "start"]