#!/usr/bin/env python3
"""Exact/numerical audit of a false activation-plus-target charging lemma.

Network (all rates one):
  linkage 0: A <-> 2A
  linkage 1: 0 -> A+B -> B -> 0.
At (n,0) with current target 2A, condition on 0->A+B and append the
A+B->B->0 current-target episode.  The combined conditional reward is
asymptotic to +log n, even though the honest episode started at the already
carried target 2A is negative.
"""
from __future__ import annotations
from fractions import Fraction
from math import log

from model import Channel
from current_target_episode import PathPolicy,episode_value,exact_increment

CHANNELS=(
    Channel((1,0),(2,0),Fraction(1),'A_to_2A',0),
    Channel((2,0),(1,0),Fraction(1),'2A_to_A',0),
    Channel((0,0),(1,1),Fraction(1),'zero_to_AB',1),
    Channel((1,1),(0,1),Fraction(1),'AB_to_B',1),
    Channel((0,1),(0,0),Fraction(1),'B_to_zero',1),
)

def conditioned_activation_plus_episode(n:int)->float:
    x=(n,0);target=(2,0);birth=CHANNELS[2]
    activation=exact_increment(x,target,birth)
    y=birth.fire(x)
    service_episode=episode_value(y,(1,1),CHANNELS,PathPolicy((3,4)))
    return activation+service_episode

def honest_current_target_episode(n:int)->float:
    # Starts before any future activation is selected.
    return episode_value((n,0),(2,0),CHANNELS,PathPolicy((1,)))

def self_test()->None:
    vals=[]
    for n in (100,1000,10000,100000):
        bad=conditioned_activation_plus_episode(n)
        good=honest_current_target_episode(n)
        assert bad>0 and good<0
        vals.append(bad/log(n))
    # The ratio tends to one; these deterministic checks are regression only.
    assert all(Fraction(4,5)<Fraction.from_float(v)<Fraction(6,5) for v in vals[1:])

if __name__=='__main__':
    self_test()
    for n in (100,1000,10000,100000):
        print(n,conditioned_activation_plus_episode(n),honest_current_target_episode(n),conditioned_activation_plus_episode(n)/log(n))
    print('activation_pair_counterexample.py self-test: OK')
