FROM python:3.9

#设置编码
ENV LANG C.UTF-8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN sudo apt-get update \
    && sudo apt-get upgrade \
    && sudo apt-get dist-upgrade \
    && sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus \
    && sudo apt-get install build-essential libncursesw5-dev libgdbm-dev libc6-dev \
    && sudo apt-get install zlib1g-dev libsqlite3-dev tk-dev \
    && sudo apt-get install libssl-dev openssl \
    && sudo apt-get install libffi-dev \
    && python -m pip install --upgrade pip \
    && pip install pep517 \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

EXPOSE 8080

USER 1000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]