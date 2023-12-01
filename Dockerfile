FROM python:3.9-buster
WORKDIR ./
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT [ "uvicorn", "--host","0.0.0.0","main:app" ]
