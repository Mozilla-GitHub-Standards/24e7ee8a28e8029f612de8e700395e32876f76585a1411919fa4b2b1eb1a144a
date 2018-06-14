#!/usr/bin/env bash

set -v -e -x

export DEBIAN_FRONTEND=noninteractive
apt-get -y update && apt-get -y upgrade

# AWS Ubuntu linux bootstrap from tlscanary/bootstrap/linux_bootstrap.sh
apt-get -y install \
    gcc \
    git \
    golang-go \
    libasound2 \
    libffi-dev \
    libgtk-3-0 \
    libssl-dev \
    libxt6 \
    libdbus-glib-1-2 \
    p7zip-full \
    python \
    python-dev \
    python-pip \
    curl

# The virtualenv package is not consistently named across distros
apt-get -y install virtualenv \
	|| apt-get -y install python-virtualenv

apt-get remove python-six -y # Native six module causes version conflict

#pip install --user --upgrade pip
pip install tlscanary
