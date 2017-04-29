FROM ubuntu:16.04
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get -y install software-properties-common python-software-properties python python-dev gcc g++ git libtool python-pip libseccomp-dev cmake
RUN add-apt-repository ppa:openjdk-r/ppa
RUN apt-get update
RUN apt-get install -y openjdk-7-jdk
RUN cd /tmp && git clone https://github.com/QingdaoU/Judger && cd Judger && git checkout newnew && mkdir build && cd build && cmake .. && make && make install && cd ../bindings/Python && python setup.py install
RUN mkdir -p /judger_run /test_case /log /code
COPY java_policy /etc
RUN pip install futures psutil gunicorn web.py requests
RUN useradd -r compiler
HEALTHCHECK --interval=5s --retries=3 CMD python /code/service.py
WORKDIR /code
EXPOSE 8080
CMD /bin/bash /code/run.sh