# C/R: A demo

This repository includes a simple Fibonacci number calculator program, used
to demonstrate two forms of Checkpoint/Restart, or C/R:

1. Application-level
2. User-/kernel-level

## Application-level

The application-level checkpointing is implemented explicitly in `fib.py`.
Users can instruct the running program to checkpoint per iteration to
a given checkpoint directory as follows:

```shell
# Print the 10th Fibonacci number with 1s sleeps between iterations
# Checkpoint to /mnt/pishare/fib-ckpts
python fib.py 10 --sleepy --checkpoint-dir /mnt/pishare/fib-ckpts
```

The application can be interrupted at any point:

```shell
$ python fib.py 10 --sleepy --checkpoint-dir /mnt/pishare/fib-ckpts
No loadable checkpoint in /mnt/pishare/fib-ckpts
Fibonacci number 1: 1; sleeping...
Fibonacci number 2: 1; sleeping...
Fibonacci number 3: 2; sleeping...
Fibonacci number 4: 3; sleeping...
Fibonacci number 5: 5; sleeping...
Fibonacci number 6: 8; sleeping...
^CKeyboardInterrupt, exiting
```

And will restart from the latest checkpoint if rerun:

```shell
$ python fib.py 10 --sleepy --checkpoint-dir /mnt/pishare/fib-ckpts
Loaded latest checkpoint from /mnt/pishare/fib-ckpts
Fibonacci number 6: 8; sleeping...
Fibonacci number 7: 13; sleeping...
Fibonacci number 8: 21; sleeping...
Fibonacci number 9: 34; sleeping...
Fibonacci number 10: 55
```

## User-/Kernel-level

The user-level checkpointing is implemented using CRIU. The demo
is composed of three files:

1. `script.sh`: Checks for an existing CRIU checkpoint. If so, it
   resumes a job. Otherwise, it runs a new job.
2. `checkpointer.sh`: Watches a running job and writes periodic
   CRIU checkpoints to timestamped directories.
3. `run.sh`: The launcher, which starts the checkpointer to begin
   watching and then executes `script.sh`.

```shell
# Print the 10th Fibonacci number with 1s sleeps between iterations
# Checkpoint to /mnt/pishare/fib-criu-ckpts
./run.sh /mnt/pishare/fib-criu-ckpts 10
```

As before, the application can be interrupted at any point:

```shell
$ ./run.sh /mnt/pishare/fib-criu-ckpts 10
/usr/bin/python "$(realpath $(dirname $0))/fib.py" 10 --sleepy
Fibonacci number 1: 1; sleeping...
Fibonacci number 2: 1; sleeping...
Fibonacci number 3: 2; sleeping...
Fibonacci number 4: 3; sleeping...
Fibonacci number 5: 5; sleeping...
^CKeyboardInterrupt, exiting
```

And will restart from the latest checkpoint if rerun:

```shell
$ ./run.sh /mnt/pishare/fib-criu-ckpts 10
Fibonacci number 6: 8; sleeping...
Fibonacci number 7: 13; sleeping...
Fibonacci number 8: 21; sleeping...
Fibonacci number 9: 34; sleeping...
Fibonacci number 10: 55
```

## Bonus: Podman demo

The following borrows from
[docker checkpoint](https://docs.docker.com/engine/reference/commandline/checkpoint/)
for an example to run, but uses Podman.

```shell
# Start a counting container that runs forever
sudo podman run --name cr -d busybox /bin/sh -c 'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done'

# Confirm it is running by following its logs
sudo podman logs -f cr

# Checkpoint the container (which stops it by default)
sudo podman container checkpoint cr

# Confirm it is no longer running by following its logs
sudo podman logs -f cr

# Restore the container
sudo podman container restore cr

# Confirm it is resumed by following its logs
sudo podman logs -f cr

# Terminate and remove the container
sudo podman kill cr
sudo podman rm cr
```
