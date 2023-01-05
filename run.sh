#!/bin/sh

cd docker

openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365 \
    -subj "/C=PL/ST=Warsaw/L=Warsaw/O=Zuzanna/OU=IT/CN=safenotes.com"

docker build . -t my_app

docker-compose up
