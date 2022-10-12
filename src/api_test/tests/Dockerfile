# pull base image
FROM python:3.9.5-slim-buster as base

FROM base as builder

RUN pip install pipenv
RUN pip install --upgrade pip

COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# install system dependencies
RUN apt-get update && apt-get install -y netcat

FROM builder as final

# Grab packages from builder
COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# switch to non-root user
RUN useradd -u 420 worker
USER worker
WORKDIR /home/worker/src/app

COPY --chown=worker:worker . /home/worker/src/app
