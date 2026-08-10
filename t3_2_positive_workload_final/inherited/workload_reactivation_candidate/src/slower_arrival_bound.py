#!/usr/bin/env python3
"""Exact bounds for workload accumulated by slower reactions during a service trial."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True,slots=True)
class ArrivalCertificate:
    interruption_probability:Fraction
    maximum_single_arrival:int
    mean_arrival_bound:Fraction
    exponential_moment_bound:Fraction

def certify(*,mean_carrier_changes:Fraction,slower_to_carrier_ratio:Fraction,
            maximum_single_arrival:int,zeta:Fraction=Fraction(2))->ArrivalCertificate:
    K=Fraction(mean_carrier_changes);eps=Fraction(slower_to_carrier_ratio)
    if K<0 or eps<0 or maximum_single_arrival<0 or zeta<=1:raise ValueError
    p=min(Fraction(1),K*eps)
    mean=p*maximum_single_arrival
    exp=1+p*(zeta**maximum_single_arrival-1)
    return ArrivalCertificate(p,maximum_single_arrival,mean,exp)

def self_test():
    c=certify(mean_carrier_changes=Fraction(18),slower_to_carrier_ratio=Fraction(1,1000),
              maximum_single_arrival=2)
    assert c.interruption_probability==Fraction(9,500)
    assert c.mean_arrival_bound==Fraction(9,250)
    assert c.exponential_moment_bound==Fraction(527,500)
if __name__=="__main__":
    self_test();print("slower_arrival_bound.py self-test: OK")
