#!/usr/bin/env python3
"""Combined strict-capacity certificate for aggregate workload debt."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from aggregate_debt import DebtCertificate,certify as certify_debt
from carrier_race_bounds import RaceCertificate,certify_path
from slower_arrival_bound import ArrivalCertificate,certify as certify_arrival

@dataclass(frozen=True,slots=True)
class QueueCertificate:
    race:RaceCertificate
    arrivals:ArrivalCertificate
    debt:DebtCertificate

def certify(*,path_length:int,edge_probability_lower_bound:Fraction,
            slower_to_carrier_ratio:Fraction,maximum_single_arrival:int,
            mean_trial_duration_bound:Fraction)->QueueCertificate:
    race=certify_path(path_length=path_length,
                      edge_probability_lower_bound=edge_probability_lower_bound,
                      slower_to_carrier_hazard_ratio=slower_to_carrier_ratio)
    arrivals=certify_arrival(mean_carrier_changes=race.mean_carrier_changes,
                            slower_to_carrier_ratio=slower_to_carrier_ratio,
                            maximum_single_arrival=maximum_single_arrival)
    # A successful carrier block is one service.  A finite strict phase may
    # require several blocks; its minorization is represented by race.block_success_probability.
    debt=certify_debt(service_probability=race.block_success_probability,
                      mean_arrival_bound=arrivals.mean_arrival_bound,
                      mean_trial_duration_bound=mean_trial_duration_bound)
    return QueueCertificate(race,arrivals,debt)

def threshold_for_capacity(*,path_length:int,q:Fraction,max_arrival:int)->Fraction:
    """Sufficient epsilon ensuring K*epsilon*max_arrival < q^L/2."""
    success=Fraction(q)**path_length
    mean_changes=Fraction(path_length,1)/success
    return success/(2*mean_changes*max(1,max_arrival))

def workload_shell_overshoot(maximum_reaction_increment:int)->int:
    """A reaction killed on first upper-shell crossing overshoots by at most Δ+."""
    if maximum_reaction_increment<0:raise ValueError
    return maximum_reaction_increment

def self_test():
    eps=Fraction(1,10000)
    q=certify(path_length=2,edge_probability_lower_bound=Fraction(1,2),
              slower_to_carrier_ratio=eps,maximum_single_arrival=2,
              mean_trial_duration_bound=Fraction(10))
    assert q.debt.drift_margin>0
    assert eps<threshold_for_capacity(path_length=2,q=Fraction(1,2),max_arrival=2)
    assert workload_shell_overshoot(3)==3
if __name__=="__main__":
    self_test();print("debt_queue_foster.py self-test: OK")
