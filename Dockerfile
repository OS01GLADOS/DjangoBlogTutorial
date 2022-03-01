FROM python:3.8

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./docker-backend /code
RUN pip install -r requirements.txt