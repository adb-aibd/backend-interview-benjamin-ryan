FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

ENV PYTHONUNBUFFERED 1

WORKDIR /workspace

COPY requirements*.txt /workspace/
RUN pip3 install --no-cache-dir -r requirements-dev.txt

COPY . /workspace

EXPOSE 8080
