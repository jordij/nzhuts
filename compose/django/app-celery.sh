#!/bin/bash
set -ex
celery -A nzhuts.taskapp worker -l INFO "$@"
