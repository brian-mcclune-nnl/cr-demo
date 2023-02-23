#!/bin/sh
#SBATCH --time=5
/usr/bin/python "$(realpath $(dirname $0))/fib.py" 120 --sleepy
