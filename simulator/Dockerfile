FROM python:3.6
WORKDIR /tmp

ADD ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install libgl1 freeglut3-dev libosmesa6

ADD ./data data
ADD ./main.py .
ADD ./mjpeg_server.py .


ENV PYOPENGL_PLATFORM=osmesa
ENTRYPOINT ./main.py
