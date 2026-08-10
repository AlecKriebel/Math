#!/usr/bin/env python3
"""Exact physical carrier-race and finite path minorization bounds."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True,slots=True)
class RaceCertificate:
    path_length:int
    edge_probability_lower_bound:Fraction
    block_success_probability:Fraction
    mean_blocks:Fraction
    mean_carrier_changes:Fraction
    slower_interruption_probability:Fraction

def certify_path(*,path_length:int,edge_probability_lower_bound:Fraction,
                 slower_to_carrier_hazard_ratio:Fraction)->RaceCertificate:
    if path_length<1:raise ValueError
    q=Fraction(edge_probability_lower_bound);eps=Fraction(slower_to_carrier_hazard_ratio)
    if not (0<q<=1) or eps<0:raise ValueError
    s=q**path_length
    blocks=Fraction(1,1)/s
    changes=path_length*blocks
    interrupt=min(Fraction(1),changes*eps)
    return RaceCertificate(path_length,q,s,blocks,changes,interrupt)

def direct_clock(*,service_rate_lower:Fraction,slower_rate_upper:Fraction):
    a=Fraction(service_rate_lower);b=Fraction(slower_rate_upper)
    if a<=0 or b<0:raise ValueError
    return {
        "service_first_lower":a/(a+b),
        "slower_first_upper":b/(a+b),
        "mean_race_time_upper":Fraction(1,1)/a,
    }

def self_test():
    c=certify_path(path_length=2,edge_probability_lower_bound=Fraction(1,3),
                   slower_to_carrier_hazard_ratio=Fraction(1,1000))
    assert c.block_success_probability==Fraction(1,9)
    assert c.mean_carrier_changes==18
    assert c.slower_interruption_probability==Fraction(9,500)
    d=direct_clock(service_rate_lower=Fraction(9),slower_rate_upper=Fraction(1))
    assert d["service_first_lower"]==Fraction(9,10)
if __name__=="__main__":
    self_test();print("carrier_race_bounds.py self-test: OK")
