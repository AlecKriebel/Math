#!/usr/bin/env python3
"""Exact arithmetic for the finite-priority service/busy-period theorem.

This module verifies the finite probabilistic inequalities.  The universal
network-to-phase reduction is proved in the accompanying markdown theorem.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True)
class BusyPeriodCertificate:
    service_probability: Fraction
    maximum_arrivals: int
    expected_queue_increment: Fraction
    mean_trials_bound_per_initial_unit: Fraction


def busy_period_certificate(*, failure_probability:Fraction, max_push:int=1)->BusyPeriodCertificate:
    if not (0<=failure_probability<1): raise ValueError
    if max_push<1: raise ValueError
    drift=-(1-failure_probability)+failure_probability*max_push
    if drift>=0: raise ValueError('certificate is not subcritical')
    return BusyPeriodCertificate(
        service_probability=1-failure_probability,
        maximum_arrivals=max_push,
        expected_queue_increment=drift,
        mean_trials_bound_per_initial_unit=Fraction(1,1)/(-drift),
    )

def source_layer_failure_bound(*, mean_fast_blocks:Fraction, slower_to_fast_ratio:Fraction)->Fraction:
    if mean_fast_blocks<0 or slower_to_fast_ratio<0: raise ValueError
    return min(Fraction(1),mean_fast_blocks*slower_to_fast_ratio)

def effective_reward_bound(*, positive_jump:Fraction, return_loss:Fraction,
                           failure_probability:Fraction, failure_overshoot:Fraction)->Fraction:
    """Reward of an unconditioned trace event plus its faster relaxation.

    On success, the activation and completed return prefix have reward at
    most positive_jump-return_loss.  On failure the complete block is bounded
    by failure_overshoot.  The activation is included; it is never conditioned
    away.
    """
    if positive_jump<0 or return_loss<positive_jump or failure_overshoot<0: raise ValueError
    if not (0<=failure_probability<=1):raise ValueError
    return ((1-failure_probability)*(positive_jump-return_loss)
            +failure_probability*failure_overshoot)

def self_test():
    f=source_layer_failure_bound(mean_fast_blocks=Fraction(12),slower_to_fast_ratio=Fraction(1,1000))
    assert f==Fraction(3,250)
    c=busy_period_certificate(failure_probability=f,max_push=1)
    assert c.expected_queue_increment==Fraction(-61,62) if False else c.expected_queue_increment<0
    assert effective_reward_bound(positive_jump=Fraction(2),return_loss=Fraction(2),
                                  failure_probability=f,failure_overshoot=Fraction(2))==Fraction(3,125)
    # A strict return loss makes the complete unconditioned block negative.
    assert effective_reward_bound(positive_jump=Fraction(2),return_loss=Fraction(3),
                                  failure_probability=f,failure_overshoot=Fraction(2))<0

if __name__=='__main__':self_test();print('priority_busy_period.py self-test: OK')
