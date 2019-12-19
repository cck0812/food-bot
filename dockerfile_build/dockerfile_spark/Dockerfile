FROM cck0812/centos7_conda_spark_hadoop

RUN yum -y install openssh-clients openssh-server

RUN mkdir /root/.ssh

RUN echo "root:1234" | chpasswd

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 600 ~/.ssh/authorized_keys

RUN /usr/sbin/sshd-keygen

ENV SPARK_HOME=/root/spark-2.4.4-bin-hadoop2.6

ADD conf/slaves $SPARK_HOME/conf/slaves
ADD id_rsa.pub /tmp/

RUN cat /tmp/id_rsa.pub >> ~/.ssh/authorized_keys

CMD /usr/sbin/sshd -D

EXPOSE "8080"
