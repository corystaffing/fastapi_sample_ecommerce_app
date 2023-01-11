
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim
# above image is looking for variable app in main.py

#workdir = cd in linux
WORKDIR /app
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY . /app
