FROM python:3.8-slim-buster

ENV PATH /usr/local/lib/python3.8/site-packages:$PATH

COPY requirements.txt /requirements.txt

COPY run.sh /run.sh

RUN pip3 install -r requirements.txt
COPY . .

RUN chmod u+x run.sh

ENTRYPOINT [ "/run.sh" ]