#!/usr/bin/env python3
"""Physical workload excursion bookkeeping."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction

@dataclass(frozen=True,slots=True)
class Workload:
    coefficients:tuple[int,...]
    phase_bound:int=0
    def __post_init__(self):
        if any(c<0 for c in self.coefficients) or not any(self.coefficients):
            raise ValueError
    def value(self,x):return sum(c*n for c,n in zip(self.coefficients,x))
    def increment(self,source,target):return self.value(target)-self.value(source)

@dataclass(frozen=True,slots=True)
class ExcursionState:
    baseline:int
    workload:int
    debt:int

def begin(workload:Workload,x)->ExcursionState:
    b=workload.value(x)
    return ExcursionState(b,b,0)

def update(state:ExcursionState,delta:int)->ExcursionState:
    w=state.workload+delta
    return ExcursionState(state.baseline,w,max(w-state.baseline,0))

def self_test():
    h=Workload((2,1,0))
    s=begin(h,(3,4,9));assert s.baseline==10
    s=update(s,3);assert s.debt==3
    s=update(s,-2);assert s.debt==1
    s=update(s,-2);assert s.debt==0 and s.workload==9
if __name__=="__main__":
    self_test();print("workload_excursion.py self-test: OK")
