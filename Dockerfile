FROM python:3.7-alpine

RUN apk update \
    && apk add \
      gcc \
      make \
      libc-dev \
    && rm -rf /var/cache/apk/*

RUN pip install pipenv

WORKDIR /tmp/docker/pipenv

COPY Pipfile Pipfile.lock /tmp/docker/pipenv/

RUN pipenv install --dev --system

WORKDIR /usr/src/app

CMD [ "tail", "-f", "/dev/null" ]
