FROM ubuntu:22.04

# docker build -t tunel-django .

ENV PYTHONUNBUFFERED 1
ENV PATH /opt/conda/bin:${PATH}
ENV LANG C.UTF-8
ENV SHELL /bin/bash
RUN apt-get update && \
    apt-get install -y wget \
        curl \
        bzip2 \
        ca-certificates \
        openssl \
        gnupg2 \
        git \
        vim \
        python3 \
        python3-pip \
        python3-dev \
        gcc \
        pkg-config \
        nginx
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apt-get autoremove -y && apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

WORKDIR /code
COPY . /code/

# For filebrowsing - can be bound from container
RUN mkdir -p /var/www/data
COPY ./scripts/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./scripts/nginx/uwsgi_params.par /etc/nginx/uwsgi_params.par
CMD /code/scripts/run_uwsgi.sh

EXPOSE 8000
