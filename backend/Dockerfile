# syntax=docker/dockerfile:1


FROM python:3.8-slim-buster
WORKDIR /app

SHELL ["/bin/bash", "-c"]
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

ENV CHROMEDRIVER_DIR /chromedriver
ENV PATH $CHROMEDRIVER_DIR:$PATH
ENV PATH /usr/local/lib/python3.8/site-packages:$PATH

COPY requirements.txt requirements.txt

COPY run.sh run.sh

RUN pip3 install -r requirements.txt
COPY . .

RUN chmod u+x run.sh

CMD ./run.sh