#!/bin/sh

if [ $# -ne 1 ]
then
	echo "You need to pass email password as argument"
	exit
fi

echo "EMAIL_PASS=\"$1\"" > conf/.env

matches="$(grep "safenotes.com"  /etc/hosts)"
n=${#matches}

if [ $n -gt 0 ]
then
	echo "Domena juz dopisana"
else
	echo "Dopisywanie domeny do /ect/hosts"
	echo "127.0.0.1	safenotes.com" >> /etc/hosts
fi

docker-compose up --build
