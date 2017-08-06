#!/bin/bash
rm /tmp/nzhuts-celerybeat.pid
set -ex
celery beat \
    -A nzhuts.taskapp \
    -l INFO \
    --pidfile=/tmp/nzhuts-celerybeat.pid \
    -s /tmp/nzhuts-celerybeat-schedule \
    "$@"
