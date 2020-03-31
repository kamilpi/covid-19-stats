FROM python:alpine3.10

LABEL MAINTAINER normander

WORKDIR /app
ADD main.py /app/main.py
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 8000
CMD ["python3", "main.py"]
