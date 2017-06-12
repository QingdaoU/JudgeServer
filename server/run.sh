#!/usr/bin/env bash
chown compiler:compiler /spj
core=$(grep --count ^processor /proc/cpuinfo)
n=$(($core*4))
chmod -R 400 /test_case
gunicorn --workers $n --threads $n --error-logfile /log/gunicorn.log --time 600 --bind 0.0.0.0:8080 server:wsgiapp