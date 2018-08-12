FROM python:3.7-alpine

RUN apk update \
    && apk add \
      curl \
      gcc \
      make \
      libc-dev \
    && rm -rf /var/cache/apk/*

#
# Install nkf
#
ENV NKF_VERSION 2.1.4

RUN curl -fSL "https://osdn.jp/dl/nkf/nkf-${NKF_VERSION}.tar.gz" | tar vxz \
  && cd "nkf-${NKF_VERSION}" \
  && make \
  && make install \
  && cd .. \
  && rm -rf "nkf-${NKF_VERSION}"

#
# Install pip
#
RUN pip install pipenv

WORKDIR /tmp/docker/pipenv

#
# Install nkf
#
COPY Pipfile Pipfile.lock /tmp/docker/pipenv/

RUN pipenv install --dev --system

#
# Finalize
#
WORKDIR /usr/src/app

CMD [ "tail", "-f", "/dev/null" ]
