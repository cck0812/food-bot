FROM cck0812/kafka:v1

RUN echo "root:1234" | chpasswd

RUN apt update && apt install -y openssh-server

ADD id_rsa.pub /tmp/

RUN cat /tmp/id_rsa.pub >> ~/.ssh/authorized_keys