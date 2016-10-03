FROM ubuntu:14.04
ENV DEBIAN_FRONTEND noninteractive
RUN rm /etc/apt/sources.list
COPY deploy/sources.list /etc/apt/
RUN apt-get update
RUN apt-get -y install software-properties-common python-software-properties python python-dev gcc g++ git libtool python-pip libseccomp-dev cmake
RUN add-apt-repository -y ppa:webupd8team/java
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
RUN apt-get update
RUN apt-get install -y oracle-java7-installer
RUN cd /tmp && git clone https://github.com/QingdaoU/Judger && cd Judger && git checkout newnew && mkdir build && cd build && cmake .. && make && make install && cd ../bindings/Python && python setup.py install
RUN mkdir /var/wp
RUN pip install psutil gunicorn web.py requests
RUN mkdir -p /judger_run /test_case /log /code
COPY deploy/java_policy /etc
COPY deploy/supervisord.conf /etc
RUN chmod -R 777 /judger_run
RUN pip install supervisor psutil gunicorn web.py
EXPOSE 8080
HEALTHCHECK --interval=5s --retries=3 CMD python /code/service.py
CMD exec supervisord
