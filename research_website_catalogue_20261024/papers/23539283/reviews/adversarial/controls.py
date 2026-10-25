#!/usr/bin/env python3
"""Bounded symbolic controls, not verification of any infinite measure claim."""
from dataclasses import dataclass
from itertools import product
import json

@dataclass(frozen=True)
class Tail:
    ident: str
    offset: int = 0

@dataclass(frozen=True)
class Block:
    prefix: tuple
    tail: Tail

@dataclass(frozen=True)
class Word:
    blocks: tuple
    suffix: tuple

def check(ok, msg):
    if not ok:
        raise RuntimeError(msg)

def build(n, m, tag):
    return Word(tuple(Block((), Tail(f'{tag}.B{i}')) for i in range(n)),
                tuple(f'{tag}.S{j}' for j in range(m)))

def concatenate(a, b):
    if b.blocks:
        first = b.blocks[0]
        return Word(a.blocks + (Block(a.suffix + first.prefix, first.tail),) + b.blocks[1:], b.suffix)
    return Word(a.blocks, a.suffix + b.suffix)

def split(w, left_grade, right_grade):
    n, m = left_grade
    p, q = right_grade
    if p:
        absorbed = w.blocks[n]
        # Test words from the forward map retain the entire absorbed prefix.
        check(len(absorbed.prefix) >= m, 'missing retained prefix')
        return (Word(w.blocks[:n], absorbed.prefix[:m]),
                Word((Block(absorbed.prefix[m:], absorbed.tail),) + w.blocks[n+1:], w.suffix))
    return Word(w.blocks, w.suffix[:m]), Word((), w.suffix[m:])

counts = {'coordinate_associativity': 0, 'coordinate_inverse': 0, 'density_scale_chain': 0,
          'finite_cut_core': 0, 'negative_controls': 0}
grades = list(product(range(3), repeat=2))
for g, h in product(grades, repeat=2):
    a, b = build(*g, 'A'), build(*h, 'B')
    check(split(concatenate(a, b), g, h) == (a, b), f'inverse {g,h}')
    counts['coordinate_inverse'] += 1
for g, h, j in product(grades, repeat=3):
    a,b,c = build(*g,'A'),build(*h,'B'),build(*j,'C')
    check(concatenate(concatenate(a,b),c)==concatenate(a,concatenate(b,c)), f'assoc {g,h,j}')
    counts['coordinate_associativity'] += 1
for k,l in product(range(21), repeat=2):
    full = tuple(2 ** (k+l-j) for j in range(k+l))
    grouped = tuple((2 ** (k-j)) * (2 ** l) for j in range(k)) + tuple(2 ** (l-j) for j in range(l))
    check(full == grouped, 'incorrect Gaussian conditional scales')
    counts['density_scale_chain'] += 1
# All finite color words, including ties, satisfy the same inversion-versus-cut condition.
for length in range(7):
    for word in product(range(4), repeat=length):
        monotone = all(word[i] >= word[i+1] for i in range(length-1))
        allcuts = all(all(not (word[i] <= cut < word[j]) for i in range(length) for j in range(i+1,length)) for cut in range(3))
        check(monotone == allcuts, 'cut test missed an inversion')
        counts['finite_cut_core'] += 1
# Negative controls: deleting absorbed coordinates is not the actual concatenation;
# forgetting the tail-scale shift changes the conditional law.
a,b = build(1,2,'A'),build(1,1,'B')
broken = Word(a.blocks + b.blocks, b.suffix)
check(broken != concatenate(a,b), 'coordinate-loss mutation escaped')
counts['negative_controls'] += 1
k,l=3,2
bad = tuple(2**(k-j) for j in range(k)) + tuple(2**(l-j) for j in range(l))
check(bad != tuple(2**(k+l-j) for j in range(k+l)), 'scale mutation escaped')
counts['negative_controls'] += 1
print(json.dumps({'passed': True, 'counts': counts,
                  'scope': 'Bounded symbolic coordinate retention, regrouping, conditional scales, and finite cut detection only; no infinite-dimensional proof certification.'}, indent=2))
