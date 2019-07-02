# 
# HPC Base image
# 
# Contents:
#   GNU compilers (upstream)
#   OpenMPI version 2.1.2
# 

FROM ubuntu:18.04 AS devel

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        wget && \
    rm -rf /var/lib/apt/lists/*

# GNU compiler
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        gfortran && \
    rm -rf /var/lib/apt/lists/*

# OpenMPI version 2.1.2
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bzip2 \
        file \
        hwloc \
        libnuma-dev \
        make \
        openssh-client \
        perl \
        tar \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/tmp && wget -q -nc --no-check-certificate -P /var/tmp https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.2.tar.bz2 && \
    mkdir -p /var/tmp && tar -x -f /var/tmp/openmpi-2.1.2.tar.bz2 -C /var/tmp -j && \
    cd /var/tmp/openmpi-2.1.2 &&  CC=gcc CXX=g++ F77=gfortran F90=gfortran FC=gfortran ./configure --prefix=/usr/local/openmpi --enable-mpi-cxx --without-cuda --without-verbs && \
    make -j$(nproc) && \
    make -j$(nproc) install && \
    rm -rf /var/tmp/openmpi-2.1.2.tar.bz2 /var/tmp/openmpi-2.1.2
ENV LD_LIBRARY_PATH=/usr/local/openmpi/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/openmpi/bin:$PATH

COPY ./mpi_hello.cpp /workspace/mpi_hello.cpp

RUN cd /workspace && \
    mpicxx mpi_hello.cpp -o mpi_hello

FROM ubuntu:18.04 AS runtime

# GNU compiler runtime
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libgfortran3 \
        libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# OpenMPI
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        hwloc \
        openssh-client && \
    rm -rf /var/lib/apt/lists/*
COPY --from=devel /usr/local/openmpi /usr/local/openmpi
ENV LD_LIBRARY_PATH=/usr/local/openmpi/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/openmpi/bin:$PATH

WORKDIR /workspace

COPY --from=devel /workspace/mpi_hello /workspace/mpi_hello

ENV PATH=$PATH:/workspace
