# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.8.5
FROM python:3.8-slim
COPY --from=openjdk:8-jdk-slim /usr/local/openjdk-8 /usr/local/openjdk-8

ENV JAVA_HOME=/usr/local/openjdk-8

RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

ENV PATH $PATH:$JAVA_HOME/bin

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

ENV PYTHONUNBUFFERED=1

RUN pip install openai
RUN pip install poetry==${POETRY_VERSION}
ENV PATH="/root/.local/bin:$PATH"


COPY /home/runner/work/sign-language-prototype/sign-language-prototype/gha-creds-ff0f93a0a81dd6b5.json /app/key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json


WORKDIR /app

RUN apt-get update && apt-get install -y build-essential
# Copy Dependencies
COPY poetry.lock pyproject.toml ./

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

RUN poetry config virtualenvs.create false
# Install Dependencies
RUN poetry install --no-root


# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python spl2videos.py
