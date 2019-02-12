from jdeathe/centos-ssh:latest
MAINTAINER Kiha <kiha@kiha.com>

WORKDIR /var

RUN yum install wget -y
RUN yum install which -y
RUN yum install java-1.8.0-openjdk-devel.x86_64 -y
RUN yum install gcc python36 python36-devel python36-libs python36u-pip -y
RUN rpm --import http://archive.cloudera.com/cdh5/redhat/6/x86_64/cdh/RPM-GPG-KEY-cloudera
RUN rpm -ivh http://archive.cloudera.com/cdh5/one-click-install/redhat/6/x86_64/cloudera-cdh-5-0.x86_64.rpm
RUN sed -i 's/x86_64\/cdh\/5\//x86_64\/cdh\/5.4\//g' /etc/yum.repos.d/cloudera-cdh5.repo
RUN yum clean all

RUN ln -s /usr/local/bin/pip3.6 /usr/local/bin/pip3
RUN pip3.6 install numpy pandas 
#pyspark 

COPY spark/spark-2.3.1-bin-hadoop2.6.tgz /var/spark-2.3.1-bin-hadoop2.6.tgz
RUN tar zxvf /var/spark-2.3.1-bin-hadoop2.6.tgz -C /opt/
RUN ln -s /opt/spark-2.3.1-bin-hadoop2.6 /opt/spark

#RUN yum install python2-devel python2-libs python-pip -y
#RUN pip install numpy pandas pyspark 

RUN touch /etc/profile.d/spark.sh
RUN echo "export SPARK_HOME=/opt/spark" >> /etc/profile.d/spark.sh
RUN source /etc/profile

ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.191.b12-1.el7_6.x86_64
ENV PATH $PATH:$JAVA_HOME/bin
ENV container docker
ENV SPARK_HOME /opt/spark 

RUN yum install -y hadoop-hdfs hadoop-yarn

RUN \
  ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
  chmod 0600 ~/.ssh/authorized_keys

RUN rm -f /usr/bin/python
RUN ln -s /usr/bin/python36 /usr/bin/python

RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
	rm -f /lib/systemd/system/multi-user.target.wants/*; \
	rm -f /etc/systemd/system/*.wants/*; \
	rm -f /lib/systemd/system/local-fs.target.wants/*; \
	rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
	rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
	rm -f /lib/systemd/system/basic.target.wants/*; \
	rm -f /lib/systemd/system/anaconda.target.wants/*;

RUN mkdir /hadoop
RUN touch $SPARK_HOME/conf/spark-env.sh;\ 
	echo "HADOOP_CONF_DIR=/etc/hadoop/conf" >> $SPARK_HOME/conf/spark-env.sh;
RUN mkdir /var/shDir 

EXPOSE 22 8020
#VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]
