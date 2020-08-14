FROM centos:7.7.1908
RUN yum install -y epel-release centos-release-scl
RUN yum install -y git \
patch \
lbzip2 \
file \
numactl-devel \
python3

ARG DEVTOOLSET_VERSION=7
ARG RELEASE=v0.15

RUN yum install -y \
devtoolset-$DEVTOOLSET_VERSION \
devtoolset-${DEVTOOLSET_VERSION}-libatomic-devel \
devtoolset-${DEVTOOLSET_VERSION}-elfutils-libelf-devel \
scl-utils
RUN git clone https://github.com/spack/spack
WORKDIR spack
RUN git checkout releases/${RELEASE}

CMD ["/bin/bash"] 

