#!/bin/sh

matches="$(grep "safenotes.com"  /etc/hosts)"
n=${#matches}

if [ $n -gt 0 ]
then
	echo "Domena juz dopisana"
else
	echo "Dopisywanie domeny do /ect/hosts"
	echo "127.0.0.1	safenotes.com" >> /etc/hosts
fi

openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365 \
    -subj "/C=PL/ST=Warsaw/L=Warsaw/O=Zuzanna/OU=IT/CN=safenotes.com"

docker-compose up --build
