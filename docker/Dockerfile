FROM ubuntu:16.04
MAINTAINER Jonas Allmann <jallmann@mozilla.com>

RUN useradd -d /home/worker -s /bin/bash -m worker
WORKDIR /home/worker

# Add canary script.
ADD bin /home/worker/bin
RUN chmod +x /home/worker/bin/*

# Install dependencies and canary.
ADD setup.sh /tmp/setup.sh
RUN bash /tmp/setup.sh

# Change user.
USER worker

# Env variables.
ENV HOME /home/worker
ENV SHELL /bin/bash
ENV USER worker
ENV LOGNAME worker
ENV HOSTNAME taskcluster-worker
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV HOST localhost
ENV DOMSUF localdomain

# Set a default command for debugging.
CMD ["/bin/bash", "--login"]
