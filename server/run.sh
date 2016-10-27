#!/usr/bin/env bash
chown compiler:compiler /spj
echo 0 > /tmp/counter
gunicorn --workers 4 --threads 4 --error-logfile /log/gunicorn.log --bind 0.0.0.0:8080 server:wsgiapp
