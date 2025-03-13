# Use a multi stage build to first download and compile all the necessary dependencies
# and packages in the FIRST STAGE. In the SECOND STAGE, create the real container image
# which contains only the needed packages and dependencies to run the application.



# ----- FIRST STAGE -----

FROM python:alpine AS builder

# Update to newest versions and install packages to build/compile the needed packages
RUN apk update &&\
    apk add --no-cache --upgrade apk-tools
# RUN apk add --no-cache --virtual g++
#mariadb-dev musl-dev gcc make p7zip g++

# Install the python packages from the /requirements.txt into /compiled-pip-packages
COPY requirements.txt /requirements.txt
RUN mkdir /compiled-pip-packages &&\
    pip install --upgrade pip &&\
    pip install --no-cache-dir -t /compiled-pip-packages -r /requirements.txt



# ----- SECOND STAGE -----

FROM python:alpine

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

# Update and install packages that are needed during runtime
RUN apk update &&\
    apk add --no-cache --upgrade apk-tools &&\
    apk add --no-cache bash mariadb-connector-c libstdc++

# Copy the created packages of the builder and move them in their corresponding place
COPY --from=builder /compiled-pip-packages /compiled-pip-packages
RUN cp -r /compiled-pip-packages/* $(python -m pip -V | grep -Eo '(\/usr\/local\/lib\/python[0-9]+\.[0-9]+\/site-packages\/)') &&\
    rm -r /compiled-pip-packages

# Create a nonroot user and set it as default; use default values (1000) if not provided
ARG GID=1000
ARG UID=1000
RUN addgroup -g ${GID} -S nonroot &&\
    adduser -u ${UID} -S nonroot -G nonroot
USER nonroot

# Create a working directory and navigate into it
WORKDIR /home/nonroot/app
RUN cd /home/nonroot/app

# Copy files into the container and set the appropriate permissions
COPY --chown=nonroot:nonroot . .
RUN chmod -R 755 /home/nonroot/app

# Indicate what port the server is running on
EXPOSE 80

# Executes the init.sh script (its content is only available on the
# first run) and starts the server (reachable on http://127.0.0.1:5000)
CMD /bin/bash -c "\
    python -m flask --app app run --host=0.0.0.0 --debug;\
"
