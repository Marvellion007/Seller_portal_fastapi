FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./build/Docker_Fastapi/requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN pip install InvoiceGenerator

RUN pip install pycountry

RUN pip install boto3

WORKDIR /code

COPY ./config ./config

COPY ./core ./core

COPY ./build/Docker_Fastapi/docker-entrypoint.sh .

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
