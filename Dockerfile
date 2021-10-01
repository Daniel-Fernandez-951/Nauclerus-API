FROM tiangolo/uvicorn-gunicorn:python3.8
EXPOSE 443

RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/Daniel-Fernandez-951/Nauclerus-API

# Get project specific requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy application
COPY ./app /app
COPY ./images /app/images
