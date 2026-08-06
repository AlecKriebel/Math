#!/usr/bin/env python3
"""Audit symbolic sign claims for illicit comparisons of rate monomials."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import sympy as sp

@dataclass(frozen=True,slots=True)
class MonomialAudit:
    positive_monomials:tuple[tuple[int,...],...]
    negative_monomials:tuple[tuple[int,...],...]
    mixed_monomials:tuple[tuple[int,...],...]
    coefficientwise_nonpositive:bool


def audit_polynomial(expr:sp.Expr,rate_symbols:Iterable[sp.Symbol])->MonomialAudit:
    syms=tuple(rate_symbols);P=sp.Poly(sp.expand(expr),*syms)
    pos=[];neg=[];mix=[]
    for mon,coef in P.terms():
      sign=sp.signsimp(coef)
      if sign.is_positive:pos.append(mon)
      elif sign.is_negative:neg.append(mon)
      else:mix.append(mon)
    return MonomialAudit(tuple(pos),tuple(neg),tuple(mix),not pos and not mix)


def require_coefficientwise_nonpositive(expr:sp.Expr,rate_symbols:Iterable[sp.Symbol])->None:
    a=audit_polynomial(expr,rate_symbols)
    if not a.coefficientwise_nonpositive:
      raise ValueError(f'sign is not coefficientwise nonpositive; positive={a.positive_monomials}, undecided={a.mixed_monomials}')


def self_test()->None:
    a,b=sp.symbols('a b',positive=True)
    require_coefficientwise_nonpositive(-a**2-3*a*b,[a,b])
    try:require_coefficientwise_nonpositive(a-b,[a,b])
    except ValueError:pass
    else:raise AssertionError('audit missed unrelated monomial comparison')

if __name__=='__main__':self_test();print('rate_monomial_audit.py self-test: OK')
