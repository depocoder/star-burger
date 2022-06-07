FROM node:12.22-buster-slim

WORKDIR /frontend

COPY package.json package-lock.json /frontend/

RUN npm install --also=dev && npm audit fix

RUN npm install -g parcel@2.0.0-beta.2

COPY bundles/ /frontend/bundles/
COPY bundles-src/ /frontend/bundles-src/

RUN parcel build bundles-src/index.js --dist-dir bundles --public-url="./"