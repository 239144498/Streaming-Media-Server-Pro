FROM python:3.9

RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
ENV LC_ALL zh_CN.UTF-8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app


EXPOSE 8080

USER 1000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]