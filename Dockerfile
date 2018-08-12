FROM python:3.7-slim-stretch

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    make \
    nkf \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

#
# Install pipenv
#
RUN pip install pipenv

#
# Install python packages
#
WORKDIR /tmp/docker/pipenv

COPY Pipfile Pipfile.lock /tmp/docker/pipenv/

RUN pipenv install --dev --system

#
# Finalize
#
WORKDIR /usr/src/app

CMD [ "tail", "-f", "/dev/null" ]
