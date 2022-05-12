FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY . /tweetor
WORKDIR /tweetor

RUN apt-get -y update \
    && apt-get -y install nano \
    && pip install -r requirements.txt

CMD [ "python3", "app/main.py"]