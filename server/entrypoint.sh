#!/usr/bin/env bash
chown compiler:compiler /spj
core=$(grep --count ^processor /proc/cpuinfo)
n=$(($core*2))
exec gunicorn --workers $n --threads $n --error-logfile /log/gunicorn.log --time 600 --bind 0.0.0.0:8080 server:app
