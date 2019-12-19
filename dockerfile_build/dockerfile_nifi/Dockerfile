FROM apache/nifi

USER root

RUN apt update && apt install -y openssh-server

RUN echo "root:1234" | chpasswd

RUN mkdir /root/.ssh

ADD ./id_rsa /root/.ssh/id_rsa
ADD ./id_rsa.pub /root/.ssh/id_rsa.pub

RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 600 ~/.ssh/authorized_keys
