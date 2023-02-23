"""Simple script that accumulates Fibonacci numbers and prints the Nth."""

import argparse
import datetime
import pathlib
import pickle
import sys
import time

from typing import List, Optional, Tuple


def fib(
    n: int,
    sleepy: bool = False,
    checkpoint_dir: Optional[str] = None,
) -> int:
    """Returns the `n_th` Fibonacci number.

    Args:
        n: The Fibonacci number to return.
        sleepy: If ``True``, sleeps for 1 second per iteration `i` in
            calculation.
        checkpoint_dir: If provided, directory to write checkpoints to.

    Returns:
        The `n_th` Fibonacci number.
    """

    if n < 2:
        return n
    i = 1
    priors = [0, 1]
    if checkpoint_dir:
        try:
            i, priors = load_checkpoint(checkpoint_dir)
            print(f'Loaded latest checkpoint from {checkpoint_dir}')
        except Exception as exc:
            print(f'No loadable checkpoint in {checkpoint_dir}')
    if checkpoint_dir:
        write_checkpoint(i, priors, checkpoint_dir)
    while i < n:
        if sleepy:
            print(f'Fibonacci number {i}: {priors[1]}; sleeping...')
            time.sleep(1)
        i += 1
        priors = [priors[1], sum(priors)]
        if checkpoint_dir:
            write_checkpoint(i, priors, checkpoint_dir)
    return priors[1]


def load_checkpoint(
    checkpoint_dir: str,
) -> dict:
    """Loads a checkpoint from `checkpoint_dir`.

    Args:
        checkpoint_dir: The directory to write checkpoint to.
    """

    ckpt_dir = pathlib.Path(checkpoint_dir)
    if not ckpt_dir.exists():
        raise Exception(f'{checkpoint_dir} checkpoint directory DNE')

    pkl_files = ckpt_dir.glob('*.pkl')
    # Try to load checkpoints in reverse chronological order
    # Alphabetical sort is chronological sort here
    ckpt = None
    for pkl_file in sorted(pkl_files, reverse=True):
        try:
            with open(pkl_file, 'rb') as pkl_fh:
                ckpt = pickle.load(pkl_fh)
            break
        except Exception:
            pass
    if ckpt is None:
        raise Exception(f'Unable to load checkpoint from {checkpoint_dir}')
    return ckpt


def write_checkpoint(
    i: int,
    priors: Tuple[int, int],
    checkpoint_dir: str,
):
    """Writes a checkpoint for Fibonacci number `i` to `checkpoint_dir`.

    Args:
        i: The Fibonacci number index.
        priors: The `i minus 1th` and `i_th` Fibonacci number.
        checkpoint_dir: The directory to write checkpoint to.
    """

    stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    ckpt_dir = pathlib.Path(checkpoint_dir)
    ckpt_dir.mkdir(exist_ok=True)
    pkl_file = ckpt_dir.joinpath(f'fib.{stamp}.pkl')
    with open(pkl_file, 'wb') as pkl_fh:
        pickle.dump((i, priors), pkl_fh)


def get_parser() -> argparse.ArgumentParser:
    """Gets the fib script CLI argument parser.

    Returns:
        The argument parser.
    """

    parser = argparse.ArgumentParser(description='Calculate Fibonacci numbers')
    parser.add_argument('n', type=int, help='The Fibonacci number to print')
    parser.add_argument('-s', '--sleepy', action='store_true',
                        help='Iterate with 1s sleeps')
    parser.add_argument('-c', '--checkpoint-dir',
                        help='Directory to write checkpoints')
    return parser


def main(argv: List[str] = sys.argv[1:]):
    """Runs the fib script.

    Args:
        argv: The command line arguments.
    """

    args = get_parser().parse_args(argv)
    fib_number = fib(
            args.n, sleepy=args.sleepy, checkpoint_dir=args.checkpoint_dir)
    print(f'Fibonacci number {args.n}: {fib_number}')


if __name__ == '__main__':
    main()

