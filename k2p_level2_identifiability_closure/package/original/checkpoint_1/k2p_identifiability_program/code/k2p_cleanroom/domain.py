from __future__ import annotations
from typing import Any,Iterable,Mapping
import sympy as sp

def transition_probabilities(s:Any,g:Any):
 return ((1+2*s+g)/4,(1-g)/4,(1-2*s+g)/4,(1-g)/4)

def is_strict_rational_edge(s:sp.Rational,g:sp.Rational,*,nonsingular=True,positive_eigenvalues=False,continuous_time=False)->bool:
 ps=transition_probabilities(s,g)
 if not all(bool(x>0) for x in ps):return False
 if nonsingular and (s==0 or g==0):return False
 if positive_eigenvalues and not (s>0 and g>0):return False
 if continuous_time and not (0<s<1 and s*s<g<1):return False
 return True

def is_strict_inheritance(weights:Iterable[sp.Rational])->bool:
 ws=list(weights);return bool(ws) and sum(ws)==1 and all(0<w<1 for w in ws)
