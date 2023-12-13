FROM python:3.11-alpine
LABEL maintainer="ysahu.dev"

# Set env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apk update \
    && apk add postgresql-dev gcc build-base musl-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code to the container
COPY . .

# Create tmp and tmp/images directories
RUN mkdir tmp tmp/images

# Set the exposed port
EXPOSE 8000