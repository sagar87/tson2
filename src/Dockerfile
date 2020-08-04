# pull official base image
FROM python:3.8.3-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

RUN pip install --upgrade pip setuptools wheel 
# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt 
RUN rm -rf /root/.cache/pip

# copy project
COPY . /usr/src/app/