FROM python:3.13

# Upgrade base packages.
RUN apt update \
    && apt upgrade -y \
    && pip install --upgrade pip

# Setup application.
# - packages
# RUN apt install -y libleveldb-dev \
#     && apt clean
# - python
RUN pip install awscli pre-commit
RUN mkdir /code \
    && cd /code
WORKDIR /code
COPY ./requirements.lock /code/requirements.lock
RUN pip install -r requirements.lock \
    && rm -rf ~/.cache/pip
# COPY ./requirements.txt /code/requirements.txt
# RUN pip install -r requirements.txt \
#     && rm -rf ~/.cache/pip
# - startup
# CMD python
