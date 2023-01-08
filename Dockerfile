FROM python:3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY ./app /app
WORKDIR /app

COPY conf/requirements.txt .
COPY conf/uwsgi.ini .
COPY conf/start.sh .
RUN mkdir -p /root/ssl


RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential\
    && apt-get -y install openssl

RUN python -m pip install -r requirements.txt

RUN openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365 \
    -subj "/C=PL/ST=Warsaw/L=Warsaw/O=Zuzanna/OU=IT/CN=safenotes.com"
RUN cp key.pem /root/ssl/key.pem
RUN cp cert.pem /root/ssl/cert.pem

COPY conf/nginx.conf /etc/nginx/

RUN chmod +x ./start.sh
RUN chmod 777 ./notes_app.db
RUN chmod 777 ../app

CMD ["./start.sh"]
