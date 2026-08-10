#!/usr/bin/env python3
"""Deterministic calibration search; never used as a universal proof."""
from __future__ import annotations
from fractions import Fraction

def weighted_zero_stationary(h,l):
    # H <-> 2L, 0 <-> L, all rates one.
    from math import factorial
    return Fraction(1,factorial(h)*factorial(l))

def weighted_zero_detailed_balance(h,l):
    if h<1:return True
    left=weighted_zero_stationary(h,l)*h
    right=weighted_zero_stationary(h-1,l+2)*(l+2)*(l+1)
    return left==right

def critical_queue(mean_service,mean_arrival,variance):
    drift=Fraction(mean_arrival)-Fraction(mean_service)
    if drift<0:return "positive_return"
    if drift>0:return "escape_candidate"
    xi=Fraction(variance)
    return "critical_nonzero_variance" if xi else "zero_invariant"

def exact_rate_separation():
    # A strict source remains positive for arbitrary rational rate separation;
    # only the chart threshold changes.
    rates=(Fraction(1,10**12),Fraction(10**12),Fraction(1,10**6))
    return min(rates)>0 and max(rates)/min(rates)==10**24

def self_test():
    for h in range(1,8):
        for l in range(0,8):assert weighted_zero_detailed_balance(h,l)
    assert critical_queue(1,1,2)=="critical_nonzero_variance"
    assert critical_queue(2,1,7)=="positive_return"
    assert exact_rate_separation()
if __name__=="__main__":
    self_test();print("counterexample_search.py self-test: OK; no C3 certificate found")
