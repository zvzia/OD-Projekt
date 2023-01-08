FROM python:3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY ./app /app
WORKDIR /app

COPY conf/requirements.txt .
#RUN python -m pip install -r requirements.txt
COPY conf/uwsgi.ini .
COPY conf/start.sh .
COPY key.pem /root/ssl/key.pem
COPY cert.pem /root/ssl/cert.pem


RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

RUN python -m pip install -r requirements.txt


COPY conf/nginx.conf /etc/nginx/
#COPY conf/default.conf /etc/nginx/conf.d/default.conf

RUN chmod +x ./start.sh
RUN chmod 777 ./notes_app.db
RUN chmod 777 ../app
#RUN chown www-data:www-data /notes_app.db
#RUN chown www-data:www-data ../app

CMD ["./start.sh"]
