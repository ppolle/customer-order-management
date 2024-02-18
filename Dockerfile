# FROM python:3.10

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# WORKDIR /usr/src/savanna

# COPY . .

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt



# CMD [ "python", "./your-daemon-or-script.py" ]

# # The first instruction is what image we want to base our container on
# # We Use an official Python runtime as a parent image
# FROM python:3.6

# # The enviroment variable ensures that the python output is set straight
# # to the terminal with out buffering it first
# ENV PYTHONUNBUFFERED 1

# # create root directory for our project in the container
# RUN mkdir /music_service

# # Set the working directory to /music_service
# WORKDIR /music_service

# # Copy the current directory contents into the container at /music_service
# ADD . /music_service/

# # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /usr/src/savanna

COPY . .