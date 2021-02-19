# base ===========================================================

FROM python:3.9.1-buster AS base

EXPOSE $SERVER_PORT
WORKDIR /app

RUN pip install --no-cache-dir sanic==20.12.2
RUN pip install --no-cache-dir sanic_openapi==0.6.2
RUN pip install --no-cache-dir boto3==1.17.7

# TODO when you know what you are doing - remove assimilation
RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html

# TODO install depenedencices for the service here
COPY apps/requirements.txt /opt/requirements.txt
RUN python -m pip install -r /opt/requirements.txt

# development ====================================================

FROM base AS dev
RUN pip install --no-cache-dir watchdog[watchmedo]==2.0.0

FROM dev AS test
RUN pip install --no-cache-dir pytest==6.2.2
RUN pip install --no-cache-dir pytest-asyncio==0.14.0
RUN pip install --no-cache-dir pytest-cov==2.11.1

# documentation ==================================================

FROM test AS docs
RUN apt-get update -y && apt-get install -y python-sphinx graphviz
RUN pip install --no-cache-dir recommonmark==0.7.1
RUN pip install --no-cache-dir sphinx-rtd-theme==0.5.1
RUN pip install --no-cache-dir pydeps==1.9.13

# production =====================================================

FROM base AS prod
ENTRYPOINT python -m nitrogen
ADD nitrogen /app/nitrogen
