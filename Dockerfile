# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install the requirements
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . .

# initialize the database (create DB, tables, populate)

EXPOSE 5000/tcp

CMD ["uvicorn", "--port",  "$PORT", "--host", "0.0.0.0", "main:app"]
