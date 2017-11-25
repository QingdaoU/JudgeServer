FROM registry.docker-cn.com/library/ubuntu:16.04
ENV DEBIAN_FRONTEND noninteractive

COPY build/java_policy /etc

RUN buildDeps='software-properties-common git libtool cmake python-dev python-pip libseccomp-dev' && \
    apt-get update && apt-get install -y python python-pkg-resources gcc g++ $buildDeps && \
    add-apt-repository ppa:openjdk-r/ppa && apt-get update && apt-get install -y openjdk-7-jdk && \
    pip install --no-cache-dir futures psutil gunicorn web.py requests && \
    cd /tmp && git clone -b newnew  --depth 1 https://github.com/QingdaoU/Judger && cd Judger && \ 
    mkdir build && cd build && cmake .. && make && make install && cd ../bindings/Python && python setup.py install && \
    apt-get purge -y --auto-remove $buildDeps && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /judger_run /test_case /log /code && \
    useradd -r compiler

HEALTHCHECK --interval=5s --retries=3 CMD python /code/service.py
ADD server /code
WORKDIR /code
EXPOSE 8080
CMD /bin/bash /code/run.sh
