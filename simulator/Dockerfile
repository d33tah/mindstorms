FROM python:3.6
WORKDIR /tmp

ADD ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install libgl1 freeglut3-dev xvfb

ADD ./data data
ADD ./main.py .
ADD ./mjpeg_server.py .

EXPOSE 5112
ENTRYPOINT xvfb-run -s '-screen 0 1024x768x24 +extension GLX +render' ./main.py
