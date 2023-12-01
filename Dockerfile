FROM python:3.10-slim

# set the working dir.
WORKDIR ./

# copy the app dir.
COPY requirements.txt ./

# install libraries.
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn

# expose the port.
EXPOSE 8080

# command to run the app using uvicorn.
CMD ["uvicorn","main.main:app","--host","0.0.0.0","--port","8080"]
