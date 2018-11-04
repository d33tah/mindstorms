FROM python:3.6
WORKDIR /tmp

ADD ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install libgl1 freeglut3-dev xvfb

ADD ./data data
ADD ./main.py .
ADD ./mjpeg_server.py .

EXPOSE 5112
ENTRYPOINT xvfb-run -s '-screen 0 640x480x24' ./main.py
