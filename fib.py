"""Simple script that accumulates Fibonacci numbers and prints the Nth."""

import argparse
import sys
import time

from typing import List, Optional, Tuple


def fib(
    n: int,
    priors: Optional[Tuple[int, int]] = None,
    sleepy: bool = False,
) -> int:
    """Returns the `n_th` Fibonacci number.

    Args:
        n: The Fibonacci number to return.
        priors: If provided, the `n minus 1_th` and `n minus 2_th` Fibonacci
            numbers.
        sleepy: If ``True``, sleeps for 1 second per iteration `i` in
            calculation.

    Returns:
        The `n_th` Fibonacci number.
    """

    if priors:
        return sum(priors)
    if n < 2:
        return n
    i = 1
    priors = [0, 1]
    while i < n:
        if sleepy:
            print(f'Fibonacci number {i}: {priors[1]}; sleeping...')
            time.sleep(1)
        i += 1
        priors = [priors[1], sum(priors)]
    return priors[1]


def get_parser() -> argparse.ArgumentParser:
    """Gets the fib script CLI argument parser.

    Returns:
        The argument parser.
    """

    parser = argparse.ArgumentParser(description='Calculate Fibonacci numbers')
    parser.add_argument('n', type=int, help='The Fibonacci number to print')
    parser.add_argument('-s', '--sleepy', action='store_true',
                        help='Iterate with 1s sleeps')
    return parser


def main(argv: List[str] = sys.argv[1:]):
    """Runs the fib script.

    Args:
        argv: The command line arguments.
    """

    args = get_parser().parse_args(argv)
    print(f'Fibonacci number {args.n}: {fib(args.n, sleepy=args.sleepy)}')


if __name__ == '__main__':
    main()

