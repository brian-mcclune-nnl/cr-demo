#!/bin/sh

CHECKPOINT_DIR=$1
FIB_N=$2
mkdir -p $CHECKPOINT_DIR
"$(realpath $(dirname $0))/checkpointer.sh" $CHECKPOINT_DIR 1 &
"$(realpath $(dirname $0))/script.sh" $CHECKPOINT_DIR $FIB_N

