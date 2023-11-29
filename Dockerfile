FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
COPY . .

RUN pip3 install -r requirements.txt

CMD [ "uvicorn" "--port" "$PORT" "--host" "0.0.0.0" "main:app" ]
