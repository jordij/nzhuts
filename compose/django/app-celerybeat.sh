#!/bin/bash
set -ex
celery beat \
    -A nzhuts.taskapp \
    -l INFO \
    --pidfile=/tmp/nzhuts-celerybeat.pid \
    -s /tmp/nzhuts-celerybeat-schedule \
    "$@"
