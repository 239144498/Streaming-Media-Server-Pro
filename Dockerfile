FROM python:3.9

#设置编码
ENV LANG C.UTF-8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get dist-upgrade -y \
    && apt-get install build-essential python-dev python-setuptools python-pip python-smbus -y \
    && apt-get install build-essential libncursesw5-dev libgdbm-dev libc6-dev -y \
    && apt-get install zlib1g-dev libsqlite3-dev tk-dev -y \
    && apt-get install libssl-dev openssl -y \
    && apt-get install libffi-dev -y \
    && python -m pip install --upgrade pip \
    && pip3 install pep517 \
    && pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

EXPOSE 8080

USER 1000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]