FROM python:3.9-slim
LABEL maintainer="Naihe <239144498@qq.com>"
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update -y && \
    apt-get install libffi-dev -y
# cryptography库需要gcc编译，导致镜像体积过大，默认不安装
#RUN apt-get update -y && \
#    apt-get install build-essential libssl-dev libffi-dev \
#    python3-dev cargo -y
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo 'Asia/Shanghai' >/etc/timezone && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
