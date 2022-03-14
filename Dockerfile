FROM tiangolo/uvicorn-gunicorn:python3.8

ARG elastic
ARG moesif

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/Daniel-Fernandez-951/Nauclerus-API && \
    mv -v Nauclerus-API/* /app && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    rm -rf Nauclerus-API \

RUN if [ "$elastic" = true ] ; then pip install elastic-apm==6.8.1 ; else echo Elastic off ; fi
RUN if [ "$moesif" = true] ; then pip install moesifasgi==0.0.3 ;  else echo Moesif off ; fi
