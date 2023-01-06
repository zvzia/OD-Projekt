FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip requirements
COPY conf/requirements.txt .
RUN python -m pip install -r requirements.txt


COPY ./app /app

CMD ["python", "server.py"]
