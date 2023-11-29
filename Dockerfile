FROM python:3.8-slim-buster

RUN pip install -r requirements.txt

COPY . .

CMD [ "uvicorn" "--port" "$PORT" "--host" "0.0.0.0" "main:app" ]
