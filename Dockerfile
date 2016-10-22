FROM ubuntu:14.04
ENV DEBIAN_FRONTEND noninteractive
RUN rm /etc/apt/sources.list
COPY deploy/sources.list /etc/apt/
RUN apt-get update
RUN apt-get -y install software-properties-common python-software-properties python python-dev gcc g++ git libtool python-pip libseccomp-dev cmake openjdk-7-jdk
RUN cd /tmp && git clone https://github.com/QingdaoU/Judger && cd Judger && git checkout newnew && mkdir build && cd build && cmake .. && make && make install && cd ../bindings/Python && python setup.py install
RUN pip install psutil gunicorn web.py requests
RUN mkdir -p /judger_run /test_case /log /code
COPY deploy/java_policy /etc
RUN pip install futures psutil gunicorn web.py
RUN useradd -r compiler
HEALTHCHECK --interval=5s --retries=3 CMD python /code/service.py
WORKDIR /code
EXPOSE 8080
CMD chown compiler:compiler /spj; echo 0 > /tmp/counter; gunicorn --workers 4 --threads 4 --error-logfile /log/gunicorn.log --bind 0.0.0.0:8080 server:wsgiapp
