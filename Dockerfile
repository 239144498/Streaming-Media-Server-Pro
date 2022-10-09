FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo 'Asia/Shanghai' >/etc/timezone && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
