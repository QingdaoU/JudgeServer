#!/usr/bin/env bash
chown compiler:compiler /spj
core=$(grep --count ^processor /proc/cpuinfo)
n=$(($core*4))
chown -R root:root /test_case /token.txt
chmod -R 400 /test_case /token.txt
gunicorn --workers $n --threads $n --error-logfile /log/gunicorn.log --time 600 --bind 0.0.0.0:8080 server:wsgiapp
