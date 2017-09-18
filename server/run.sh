#!/usr/bin/env bash
chown compiler:compiler /spj
echo 0 > /tmp/counter
core=$(grep --count ^processor /proc/cpuinfo)
n=$(($core*2))
chmod 400 /tmp/counter
chmod -R 400 /test_case
gunicorn --workers $n --threads $n --error-logfile /log/gunicorn.log --time 600 --bind 0.0.0.0:8080 server:wsgiapp
