#!/usr/bin/env python3
"""Exact polynomial-rate generator for one active coordinate A."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Sequence
from .model import Channel, falling

Phase=tuple[int,int]

@dataclass(frozen=True,slots=True)
class PolynomialTransition:
    source_phase: Phase
    target_phase: Phase | None  # None is box exit
    level_jump: int
    channel_index: int
    degree: int
    coefficient: Fraction

@dataclass(frozen=True,slots=True)
class OneActiveGenerator:
    phases: tuple[Phase,...]
    transitions: tuple[PolynomialTransition,...]
    bmax: int
    cmax: int


def build(channels: Sequence[Channel],bmax:int,cmax:int)->OneActiveGenerator:
    phases=tuple(product(range(bmax+1),range(cmax+1)))
    tr=[]
    for ph in phases:
        b,c=ph
        for i,e in enumerate(channels):
            ya,yb,yc=e.source
            if b<yb or c<yc:continue
            coeff=e.rate*falling(b,yb)*falling(c,yc)
            if coeff==0:continue
            bt=b+e.displacement[1];ct=c+e.displacement[2]
            target=(bt,ct) if 0<=bt<=bmax and 0<=ct<=cmax else None
            tr.append(PolynomialTransition(ph,target,e.displacement[0],i,ya,coeff))
    return OneActiveGenerator(phases,tuple(tr),bmax,cmax)


def rate_at(t: PolynomialTransition,n:int)->Fraction:
    return t.coefficient*falling(n,t.degree)


def generator_level_drift(g:OneActiveGenerator,n:int,phase:Phase)->Fraction:
    return sum((rate_at(t,n)*t.level_jump for t in g.transitions if t.source_phase==phase),Fraction(0))


def self_test()->None:
    ch=(Channel('birth',(0,0,0),(1,1,0),Fraction(2),0),
        Channel('death',(1,1,0),(0,1,0),Fraction(3),0))
    g=build(ch,2,0)
    assert generator_level_drift(g,10,(1,0))==2-30
    assert all(t.degree in (0,1,2) for t in g.transitions)

if __name__=='__main__':self_test();print('one_active_generator.py self-test: OK')
