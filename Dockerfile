FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -yq && echo Y | apt-get install gettext


WORKDIR /code/deprem
COPY . /code/deprem

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["bash","/code/deprem/docker-entrypoint.sh"]