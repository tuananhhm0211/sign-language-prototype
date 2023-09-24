# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.8.5
FROM python:3.8-slim
COPY --from=openjdk:8-jdk-slim /usr/local/openjdk-8 /usr/local/openjdk-8

ENV JAVA_HOME=/usr/local/openjdk-8

RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1


# RUN apt-get update && apt-get install -y default-jre
# ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $PATH:$JAVA_HOME/bin

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN pip install openai
# Creating a virtual environment just for poetry and install it with pip
# RUN pip install -U pip setuptools \
#     && pip install poetry==${POETRY_VERSION}
RUN pip install poetry==${POETRY_VERSION}
ENV PATH="/root/.local/bin:$PATH"

#RUN apt-get -y install curl

# Downloading gcloud package
#RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
# RUN mkdir -p /usr/local/gcloud \
#   && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
#   && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
# ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# COPY application_default_credentials.json /root/.config/gcloud/
COPY key.json /app/key.json
ARG OPENAI_API_KEY
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json
RUN --mount=type=secret,id=OPENAI_API_KEY \
   export OPENAI_API_KEY=$(cat /run/secrets/OPENAI_API_KEY) && \
   yarn gen

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

RUN apt-get update && apt-get install -y build-essential
# Copy Dependencies
COPY poetry.lock pyproject.toml ./

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

RUN poetry config virtualenvs.create false
# Install Dependencies
RUN poetry install --no-root

# Switch to the non-privileged user to run the application.
# USER appuser

# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json
# RUN export GOOGLE_APPLICATION_CREDENTIALS=/app/key.json

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python spl2videos.py
