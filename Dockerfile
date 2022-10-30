FROM python:3.10-slim

ENV ENV=${ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/src/ \
  POETRY_VERSION=1.2.2

COPY ./poetry.lock ./pyproject.toml /

RUN apt-get update && apt-get install -y \
    build-essential \
    # install poetry
    && pip install "poetry==$POETRY_VERSION" \
    # project initialization
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    # clean cache
    && apt-get -y autoremove && apt-get -y clean

COPY ./setup.cfg ./black.toml ./.pylintrc /
ADD ./src /src
ADD ./docs /docs
WORKDIR /src

# root is used as a hotfix for package introspection problem
# https://intellij-support.jetbrains.com/hc/en-us/community/posts/115000373944/comments/7286554132370
USER root
