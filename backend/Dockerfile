# syntax=docker/dockerfile:1


FROM python:3.8-slim-buster
WORKDIR /app

ENV PATH /usr/local/lib/python3.8/site-packages:$PATH

COPY requirements.txt requirements.txt

COPY run.sh run.sh

RUN pip3 install -r requirements.txt
COPY . .

RUN chmod u+x run.sh

CMD ./run.sh