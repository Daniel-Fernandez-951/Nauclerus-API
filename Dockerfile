FROM tiangolo/uvicorn-gunicorn:python3.8

# Get project specific requirements
COPY requirements.txt ./
RUN apt-get update && apt-get install -y git
RUN pip install -r requirements.txt

RUN git clone https://github.com/Daniel-Fernandez-951/Nauclerus-API

# Copy application
COPY ./app /app
COPY ./images /app/images
COPY .env /app
