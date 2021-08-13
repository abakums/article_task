FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/articles_and_comments

COPY ./requirements.txt  /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/articles_and_comments

EXPOSE 8000