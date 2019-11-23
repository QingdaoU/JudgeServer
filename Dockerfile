FROM ubuntu:18.04

COPY build/java_policy /etc

RUN apt-get update && apt-get install -y wget && wget https://github.com/Harry-zklcdc/JudgeServer/raw/18.04/sources.list && mv sources.list /etc/apt/sources.list && \
    buildDeps='software-properties-common git libtool cmake python-dev python3-pip python-pip libseccomp-dev' && \
    apt-get update && apt-get install -y python python3.6 python-pkg-resources python3-pkg-resources gcc-8 g++-8 openjdk-8-jdk $buildDeps && \
    rm /usr/bin/gcc /usr/bin/g++ && ln -s /usr/bin/gcc-8 /usr/bin/gcc && ln -s /usr/bin/g++-8 /usr/bin/g++ && \
    pip3 install --no-cache-dir psutil gunicorn flask requests -i https://mirrors.aliyun.com/pypi/simple/ && \
    pip3 uninstall idna -y && pip install --no-cache-dir idna -i https://mirrors.aliyun.com/pypi/simple/ && \
    cd /tmp && git clone -b newnew  --depth 1 https://github.com/QingdaoU/Judger && cd Judger && \
    mkdir build && cd build && cmake .. && make && make install && cd ../bindings/Python && python3 setup.py install && \
    apt-get purge -y --auto-remove wget $buildDeps && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/gcc-8 /usr/bin/gcc && ln -s /usr/bin/g++-8 /usr/bin/g++ && \
    mkdir -p /code && \
    useradd -u 12001 compiler && useradd -u 12002 code && useradd -u 12003 spj && usermod -a -G code spj

HEALTHCHECK --interval=5s --retries=3 CMD python3 /code/service.py
ADD server /code
WORKDIR /code
RUN gcc -shared -fPIC -o unbuffer.so unbuffer.c
EXPOSE 8080
ENTRYPOINT /code/entrypoint.sh
