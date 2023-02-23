#!/bin/bash

CHECKPOINT_DIR=$1
sleep $2

LAST_PID_FILE=$(ls -tr $CHECKPOINT_DIR/*.pid | tail -1)
FIB_PID=$(sudo cat $LAST_PID_FILE)

# If this script is killed, kill fib.py
trap "kill $FIB_PID 2> /dev/null" EXIT

# While fib.py is running, write checkpoints
while kill -0 $FIB_PID 2> /dev/null; do
    CUR_CHECKPOINT_DIR="$CHECKPOINT_DIR/fib.$(date +%Y%m%d%H%M%S%N)"
    mkdir -p $CUR_CHECKPOINT_DIR
    sudo criu dump -vvvv -t $FIB_PID --shell-job --leave-running \
        -D $CUR_CHECKPOINT_DIR \
	-o dump.log

    sleep 1
done

# Disable the trap on a normal exit.
trap - EXIT

