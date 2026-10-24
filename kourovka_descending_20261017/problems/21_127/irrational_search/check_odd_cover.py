#!/usr/bin/env python3
"""Exact bounded sanity check for the general odd-degree covering proof.
No scl value is inferred from this finite computation; see the analytic proof.
"""
from datetime import datetime, timezone
from fractions import Fraction
import hashlib, json
from pathlib import Path

def compose(first, second):
    return [first[x] for x in second]

def inverse(permutation):
    result=[0]*len(permutation)
    for x,y in enumerate(permutation): result[y]=x
    return result

def check(n):
    a=[(x+1)%n for x in range(n)]
    b=[(-x)%n for x in range(n)]
    comm=compose(compose(compose(a,b),inverse(a)),inverse(b))
    expected=[(x+2)%n for x in range(n)]
    assert comm==expected
    orbit=[]; x=0
    while x not in orbit:
        orbit.append(x); x=comm[x]
    assert x==0 and len(orbit)==n
    genus=(n+1)//2
    assert 1-2*genus==-n
    return {'n':n,'boundary_cycles':1,'genus':genus,'upper_cl_over_n':str(Fraction(genus,n))}

if __name__=='__main__':
    rows=[check(n) for n in range(1,200,2)]
    result={'checked_utc':datetime.now(timezone.utc).isoformat(),
      'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'scope':'Finite sanity check only; all-odd proof is in DYNAMICAL_IRRATIONALITY_FILTER.md.',
      'cases':len(rows),'points':sum(x['n'] for x in rows),'rows':rows}
    print(json.dumps(result,indent=2))
