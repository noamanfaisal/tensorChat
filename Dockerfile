FROM ubuntu:24.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV TZ="UTC"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sudo \
        curl \
        wget \
        ffmpeg \
        python3 \
        python3-pip \
        net-tools \
        curl \
        build-essential \
        ssh \
        gcc \
        git \
        openssh-server \
        python3.12-venv \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user 'ubuntu' safely
RUN id -u ubuntu &>/dev/null || adduser --disabled-password --gecos '' ubuntu && \
    usermod -aG sudo ubuntu && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    mkdir -p /home/ubuntu && \
    chmod a+rwx /home/ubuntu

USER ubuntu
WORKDIR /home/ubuntu

COPY personal_github_id_ed25519 /home/ubuntu/.ssh/personal_github_id_ed25519
RUN sudo chown ubuntu /home/ubuntu/.ssh/ -R && \
chmod 600 /home/ubuntu/.ssh/personal_github_id_ed25519 && \
touch /home/ubuntu/.ssh/known_hosts && \
ssh-keyscan github.com >> /home/ubuntu/.ssh/known_hosts
# copy ssh key git configuration
COPY config /home/ubuntu/.ssh/config
RUN sudo chown ubuntu /home/ubuntu/.ssh/ -R && \
chmod 600 /home/ubuntu/.ssh/config


RUN git clone git@personal_github:noamanfaisal/tensorChat.git /home/ubuntu/tensorchat
WORKDIR /home/ubuntu/tensorchat
RUN git fetch --all && git checkout origin/staging

# Create Python virtual environment
RUN python3 -m venv /home/ubuntu/envs/tensorchat

# Use virtualenv Python/PIP as default
ENV PATH="/home/ubuntu/envs/tensorchat/bin:$PATH"
RUN pip install -r requirements.txt
