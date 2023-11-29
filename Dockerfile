FROM python:3.9.2

COPY requirements.txt .
RUN pip install -r /requirements.txt

COPY . . 

CMD [ "uvicorn" "--port" "$PORT" "--host" "0.0.0.0" "main:app" ]
