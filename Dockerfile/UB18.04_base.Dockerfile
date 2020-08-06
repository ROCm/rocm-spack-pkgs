FROM ubuntu:18.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        g++ \
        gcc \
        git \
        make \
        curl \
        patch \
        unzip \
        python3 \
        xz-utils \
        python3-pip \
        libnuma-dev \
#        libpci-dev \
#        rpm \
        && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    apt-get autoremove --purge && \
    apt-get clean

CMD ["bash"]
