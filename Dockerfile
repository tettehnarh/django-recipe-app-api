# Use the official Python 3.9 image based on Alpine Linux 3.13, which is lightweight and optimized for Docker
FROM python:3.9-alpine3.13

# Set a label for the image to define the maintainer
LABEL maintainer="Leslie Narh"

# Set an environment variable to avoid buffering output, ensuring logs appear instantly
ENV PYTHONUNBUFFERED=1

# Copy the requirements.txt file into a temporary directory in the container for installing dependencies
COPY ./requirements.txt /tmp/requirements.txt
# Copy the requirements-dev.txt file into a temporary directory in the container for installing development dependencies
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the application code into the /app directory in the container
COPY ./app /app

# Set the working directory to /app, where the application code is stored
WORKDIR /app

# Expose port 8000, which the application will use to communicate outside the container
EXPOSE 8000

ARG DEV=false
# Run a series of commands to set up the Python environment and install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Set the PATH to include the /py/bin directory so we can use the virtual environment’s Python and pip directly
ENV PATH="/py/bin:$PATH"

# Switch to using the newly created "django-user" for running the application, improving container security
USER django-user
