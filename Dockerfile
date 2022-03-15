FROM tiangolo/uvicorn-gunicorn:python3.8

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/Daniel-Fernandez-951/Nauclerus-API && \
    mv -v Nauclerus-API/* /app && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    rm -rf Nauclerus-API && \
    rm /app/.env.sample
