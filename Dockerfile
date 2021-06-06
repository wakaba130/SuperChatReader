FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
    vim unzip byobu wget tree git cmake build-essential \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Python
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    python3-dev python3-pip python3-tk \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN pip3 install -U pip

ENV CFLAGS=-DTCL_UTF_MAX=6
ENV MAKEFLAGS=-j5

RUN mkdir workspace
WORKDIR /workspace

RUN wget -c https://prdownloads.sourceforge.net/tcl/tcl8.6.11-src.tar.gz
RUN tar -xvf tcl8.6.11-src.tar.gz && cd tcl8.6.11/unix/ \
    && ./configure --enable-threads --enable-shared --enable-symbols \
        --enable-64bit --enable-langinfo --enable-man-symlinks \
    && make && make install

RUN git clone https://github.com/python/cpython \
    && cd cpython && git checkout -b 3.6 remotes/origin/3.6 && ./configure --enable-shared --enable-optimizations \
    --enable-ipv6 --enable-unicode=ucs4 --with-lto --with-signal-module \
    --with-pth --with-wctype-functions --with-tcltk-includes=/usr/local/include/ \
    --with-tcltk-libs=/usr/local/lib/ && make && make install