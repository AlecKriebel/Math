#!/usr/bin/env python3
"""Exact scalar aggregate-debt Foster theorem."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True,slots=True)
class DebtCertificate:
    service_probability:Fraction
    mean_arrival_bound:Fraction
    drift_margin:Fraction
    expected_trials_per_initial_unit:Fraction
    mean_trial_duration_bound:Fraction|None=None

def certify(*,service_probability:Fraction,mean_arrival_bound:Fraction,
            mean_trial_duration_bound:Fraction|None=None)->DebtCertificate:
    p=Fraction(service_probability);a=Fraction(mean_arrival_bound)
    if not (0<p<=1):raise ValueError("p must lie in (0,1]")
    if not (0<=a<p):raise ValueError("arrival mean must be strictly below service probability")
    if mean_trial_duration_bound is not None and mean_trial_duration_bound<0:raise ValueError
    margin=p-a
    return DebtCertificate(p,a,margin,Fraction(1,1)/margin,mean_trial_duration_bound)

def one_step_upper_bound(debt:int,service:int,arrival:int)->int:
    if min(debt,service,arrival)<0:raise ValueError
    return max(debt-service,0)+arrival

def drift_bound(*,debt:int,service_probability:Fraction,mean_arrival_bound:Fraction)->Fraction:
    if debt<=0:raise ValueError("drift statement is for positive debt")
    return -Fraction(service_probability)+Fraction(mean_arrival_bound)

def expected_hitting_trials(initial_debt:int,certificate:DebtCertificate)->Fraction:
    if initial_debt<0:raise ValueError
    return Fraction(initial_debt,1)/certificate.drift_margin

def expected_hitting_time(initial_debt:int,certificate:DebtCertificate)->Fraction:
    if certificate.mean_trial_duration_bound is None:raise ValueError
    return expected_hitting_trials(initial_debt,certificate)*certificate.mean_trial_duration_bound

def self_test():
    c=certify(service_probability=Fraction(3,4),mean_arrival_bound=Fraction(1,8),
              mean_trial_duration_bound=Fraction(5,2))
    assert c.drift_margin==Fraction(5,8)
    assert expected_hitting_trials(5,c)==8
    assert expected_hitting_time(5,c)==20
    assert one_step_upper_bound(4,1,2)==5
    assert drift_bound(debt=2,service_probability=c.service_probability,
                       mean_arrival_bound=c.mean_arrival_bound)==-c.drift_margin
if __name__=="__main__":
    self_test();print("aggregate_debt.py self-test: OK")
