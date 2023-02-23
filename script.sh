#!/bin/bash

set -m
CHECKPOINT_DIR=$1
PID_FILE="$CHECKPOINT_DIR/$(date +%Y%m%d%H%M%S%N).pid"
if [[ -e $CHECKPOINT_DIR ]] && [[ ! -z "$(ls $CHECKPOINT_DIR | grep fib)" ]]; then
    LAST_CHECKPOINT_DIR=$CHECKPOINT_DIR/$(ls -tr $CHECKPOINT_DIR | grep fib | tail -1)
    sudo criu restore -vvvv --shell-job -D $LAST_CHECKPOINT_DIR \
	--pidfile $PID_FILE
else
    /usr/bin/python "$(realpath $(dirname $0))/fib.py" 100 --sleepy &
    echo -n $! > $PID_FILE
    fg 1
fi
