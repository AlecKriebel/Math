#!/usr/bin/env python3
"""Noncertifying direct matrix-product quadrature for printed Table 1 decimals."""
import argparse
import cmath
import json
import math
import time


def sample(n, cells):
    total = 0.0
    for j in range(cells):
        z = cmath.exp(2j * math.pi * ((j + 0.5) / cells))
        a, b, c, d = 1 + 0j, 0j, 0j, 1 + 0j
        for _ in range(n):
            a, b, c, d = a + z * b, 1j * a - z * b, c + z * d, 1j * c - z * d
            z *= z
        S = abs(a) ** 2 + abs(b) ** 2 + abs(c) ** 2 + abs(d) ** 2
        total += math.log(S)
    return total / (n * cells)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cells', type=int, default=65536)
    args = parser.parse_args()
    start = time.monotonic()
    print(json.dumps({'status': 'NONCERTIFYING_REPRODUCTION', 'cells': args.cells,
                      'forward_direct_product_midpoint_estimates': {
                          str(n): sample(n, args.cells) for n in (10, 11, 12, 13)},
                      'elapsed_seconds': time.monotonic() - start}, indent=2))


if __name__ == '__main__':
    main()
