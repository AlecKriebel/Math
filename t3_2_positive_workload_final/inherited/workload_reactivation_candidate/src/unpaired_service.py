#!/usr/bin/env python3
"""Finite-mean genuine descent after aggregate debt reaches zero."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from aggregate_debt import DebtCertificate,expected_hitting_trials

@dataclass(frozen=True,slots=True)
class ZeroDebtCertificate:
    strict_service_probability:Fraction
    failed_trial_probability:Fraction
    maximum_failed_debt:int
    mean_trial_duration:Fraction
    debt_certificate:DebtCertificate
    mean_cycles:Fraction
    physical_time_bound:Fraction

def certify(*,strict_service_probability:Fraction,failed_trial_probability:Fraction,
            maximum_failed_debt:int,mean_trial_duration:Fraction,
            debt_certificate:DebtCertificate)->ZeroDebtCertificate:
    p=Fraction(strict_service_probability);f=Fraction(failed_trial_probability)
    T=Fraction(mean_trial_duration)
    if not (0<p<=1) or not (0<=f<1) or p+f>1 or maximum_failed_debt<0 or T<0:
        raise ValueError
    # Each cycle succeeds with probability p. Failed positive trials create at
    # most M debt, which is cleared before the next zero-debt attempt.
    cycles=Fraction(1,1)/p
    clear=expected_hitting_trials(maximum_failed_debt,debt_certificate)
    time=cycles*(T+f*clear*T)
    return ZeroDebtCertificate(p,f,maximum_failed_debt,T,debt_certificate,cycles,time)

def self_test():
    from aggregate_debt import certify as debt
    d=debt(service_probability=Fraction(3,4),mean_arrival_bound=Fraction(1,4))
    z=certify(strict_service_probability=Fraction(1,3),failed_trial_probability=Fraction(1,3),
              maximum_failed_debt=2,mean_trial_duration=Fraction(2),debt_certificate=d)
    assert z.mean_cycles==3 and z.physical_time_bound>0
if __name__=="__main__":
    self_test();print("unpaired_service.py self-test: OK")
