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

#RUN ln -s /usr/bin/pip3.6 /usr/bin/pip3
RUN pip3.6 install numpy pandas 

RUN yum install -y hadoop-yarn-nodemanager

ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.191.b12-1.el7_6.x86_64 
ENV PATH $PATH:$JAVA_HOME/bin
ENV container docker

RUN \
  ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
  chmod 0600 ~/.ssh/authorized_keys

RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
	rm -f /lib/systemd/system/multi-user.target.wants/*; \
	rm -f /etc/systemd/system/*.wants/*; \
	rm -f /lib/systemd/system/local-fs.target.wants/*; \
	rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
	rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
	rm -f /lib/systemd/system/basic.target.wants/*; \
	rm -f /lib/systemd/system/anaconda.target.wants/*;

RUN rm -f /usr/bin/python
RUN ln -s /usr/bin/python36 /usr/bin/python

RUN mkdir /hadoop
RUN mkdir /hadoop/hdfs
RUN chown hdfs:hadoop /hadoop/hdfs
RUN chmod 775 /hadoop/hdfs
RUN mkdir /hadoop/yarn
RUN chown yarn:hadoop /hadoop/yarn
RUN chmod 775 /hadoop/yarn
RUN mkdir /hadoop/tmp
RUN chmod 777 /hadoop/tmp

EXPOSE 22 8020
#VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]
