FROM        python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY        ./requirements.txt /app/requirements.txt

COPY        . /app/

WORKDIR     /app

RUN         pip install -r requirements.txt


EXPOSE      8000

CMD         ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]