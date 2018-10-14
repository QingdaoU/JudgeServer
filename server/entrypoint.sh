#!/bin/bash
useradd -u 12001 compiler
useradd -u 12002 code
useradd -u 12003 spj
usermod -a -G code spj

rm -rf /judger/*
mkdir -p /judger/run /judger/spj

chown compiler:code /judger/run
# 71[1] allow spj user to read user output
chmod 711 /judger/run

chown compiler:spj /judger/spj
chmod 710 /judger/spj

core=$(grep --count ^processor /proc/cpuinfo)
n=$(($core*2))
exec gunicorn --workers $n --threads $n --error-logfile /log/gunicorn.log --time 600 --bind 0.0.0.0:8080 server:app
