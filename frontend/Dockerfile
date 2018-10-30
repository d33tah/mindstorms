FROM python:3.6
ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD ./main.py .
EXPOSE 8080
ENTRYPOINT ["./main.py"]
