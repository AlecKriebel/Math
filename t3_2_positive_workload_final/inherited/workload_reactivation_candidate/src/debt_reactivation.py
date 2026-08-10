#!/usr/bin/env python3
"""Markovian reactivation of aggregate debt from the current physical phase."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from physical_carrier_reactivation import ComponentCertificate,reactivation_alternative
from aggregate_debt import DebtCertificate,expected_hitting_trials

@dataclass(frozen=True,slots=True)
class ReactivationCertificate:
    phase_classification:str
    service_probability:Fraction
    debt_certificate:DebtCertificate|None

def certify(component:ComponentCertificate,service_probability:Fraction,
            debt_certificate:DebtCertificate|None)->ReactivationCertificate:
    alt=reactivation_alternative(component)
    p=Fraction(service_probability)
    if alt=="service":
        if not (0<p<=1) or debt_certificate is None:raise ValueError
    else:
        if p!=0 or debt_certificate is not None:raise ValueError
    return ReactivationCertificate(alt,p,debt_certificate)

def restart_bound(debt:int,cert:ReactivationCertificate):
    if cert.phase_classification=="service":
        return expected_hitting_trials(debt,cert.debt_certificate)
    return None

def self_test():
    from physical_carrier_reactivation import ComponentCertificate
    from aggregate_debt import certify as dc
    c=ComponentCertificate(("a",),"strict",(0,),())
    d=dc(service_probability=Fraction(3,4),mean_arrival_bound=Fraction(1,4))
    r=certify(c,Fraction(3,4),d)
    assert restart_bound(3,r)==6
if __name__=="__main__":
    self_test();print("debt_reactivation.py self-test: OK")
