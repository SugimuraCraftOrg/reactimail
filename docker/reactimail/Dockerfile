FROM python:3.13

LABEL maintainer="SugimuraCraft <sugimuracraft@gmail.com>"
LABEL description="Reactimail Django application"

# Upgrade base packages.
RUN apt update \
    && apt upgrade -y \
    && apt clean \
    && pip install --upgrade pip

# Create base directory.
RUN mkdir /opt/reactimail \
    && cd /opt/reactimail
WORKDIR /opt/reactimail

# Setup application.
# - packages
# RUN apt install -y libleveldb-dev \
#     && apt clean
# - python
COPY ./requirements.lock /opt/reactimail/requirements.lock
RUN pip install -r requirements.lock \
    && rm -rf ~/.cache/pip
# COPY ./requirements.txt /opt/reactimail/requirements.txt
# RUN pip install -r requirements.txt \
#     && rm -rf ~/.cache/pip

# Create non-root user
RUN useradd -m -s /bin/bash app
RUN chown -R app:app /opt/reactimail
USER app

# - startup
# CMD python
