FROM --platform=linux/amd64 bitnami/python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update -y &&  \
    apt-get install -y apt-transport-https && \
    apt-get install -y telnet

ADD requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ADD . /app

ENTRYPOINT ["make", "run"]
