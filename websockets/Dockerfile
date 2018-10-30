FROM python:3.6
ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD ./websockets.py .
EXPOSE 8001
ENTRYPOINT ["./websockets.py"]
