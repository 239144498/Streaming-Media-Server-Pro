FROM python:3.9

#设置编码
ENV LANG C.UTF-8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN apt-get update \
    && apt-get upgrade \
    && apt-get dist-upgrade \
    && apt-get install build-essential python-dev python-setuptools python-pip python-smbus \
    && apt-get install build-essential libncursesw5-dev libgdbm-dev libc6-dev \
    && apt-get install zlib1g-dev libsqlite3-dev tk-dev \
    && apt-get install libssl-dev openssl \
    && apt-get install libffi-dev \
    && python -m pip install --upgrade pip \
    && pip install pep517 \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

EXPOSE 8080

USER 1000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]