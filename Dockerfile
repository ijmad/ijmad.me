FROM python:latest

WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD ijmad/ /app/ijmad

ENV PYTHONPATH /app/
EXPOSE 8080
CMD gunicorn --bind 0.0.0.0:8080 ijmad.app:app
