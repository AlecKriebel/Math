#!/usr/bin/env python3
"""Supplementary exact algebra check with weaker commutation than the tensor model.

No Lean invocation. Coefficient arithmetic is shared with exact_preflight;
word algebra is a different implementation: cancellation and explicitly allowed
adjacent commutations only. A does NOT commute with any Bob generator here.
Every reduction step is a group relation; no dimension or finite order is used.
"""
from __future__ import annotations
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
from datetime import datetime, timezone
import json
import sys
from exact_preflight import Cyclo, ZERO, ONE, zeta

# Signed generators: A=1, U=2, B0..B3=3..6, Bstar=7.
# The theorem requires U to commute with B0..B3 ONLY.
def allowed(a: int, b: int) -> bool:
    return (abs(a) == 2 and 3 <= abs(b) <= 6) or (abs(b) == 2 and 3 <= abs(a) <= 6)

@lru_cache(None)
def normal(word: tuple[int, ...]) -> tuple[int, ...]:
    seen, todo = {word}, [word]
    while todo:
        w = todo.pop()
        for j in range(len(w)-1):
            nxt = None
            if w[j] == -w[j+1]:
                nxt = w[:j] + w[j+2:]
            elif allowed(w[j], w[j+1]):
                nxt = w[:j] + (w[j+1], w[j]) + w[j+2:]
            if nxt is not None and nxt not in seen:
                seen.add(nxt); todo.append(nxt)
    return min(seen, key=lambda w: (len(w), w))

def plus(*terms):
    out = {}
    for p in terms:
        for w,c in p.items():
            nw=normal(w); out[nw]=out.get(nw,ZERO)+c
    return {w:c for w,c in out.items() if c != ZERO}

def times(*terms):
    out={():ONE}
    for p in terms:
        out=plus(*({a+b:c*d} for a,c in out.items() for b,d in p.items()))
    return out

def scale(c, p):
    c=Cyclo.coerce(c)
    return {w:c*v for w,v in p.items() if c*v != ZERO}

def adj(p):return plus(*({tuple(-x for x in reversed(w)):c.conj()} for w,c in p.items()))
def square(p):return times(adj(p),p)
def gen(j):return {(j,):ONE}

def run():
    one={():ONE};A=gen(1);U=gen(2);B=[gen(i+3) for i in range(5)]
    k=zeta(2)+zeta(-2);s=(zeta(1)-zeta(-1))/(2*zeta(4));M=2/s
    lhs=scale(M,one);rhs={};checks=[]
    def eq(name,a,b):
        if a != b: raise AssertionError(name)
        checks.append(name)
    for y in range(4):
        T=scale(zeta(4*y),U);T2=times(T,T);T3=times(T2,T)
        P=scale(s,plus(one,scale(2+k,T),T2))
        Q=scale(s/2,plus(scale(-k,one),scale(2+k,T),scale(2+k,T2),scale(-k,T3)))
        F=plus(times(plus(one,T),adj(A)),scale(-1,times(P,B[y])))
        G=plus(times(T,adj(A)),scale(-1,times(Q,B[y])))
        raw=times(A,plus(one,T),B[y])
        lhs=plus(lhs,scale(Fraction(-1,2),plus(raw,adj(raw))))
        rhs=plus(rhs,scale(s/2,plus(square(F),scale(k,square(G)))))
    eq('first reduced SOS with ONLY U/By commutation',lhs,rhs)
    ab=times(A,B[4]);R=plus(one,scale(-1,ab))
    auglhs=plus(lhs,one,scale(Fraction(-1,2),plus(ab,adj(ab))))
    augrhs=plus(rhs,scale(Fraction(1,2),square(R)))
    eq('first augmented SOS with no A/Bstar commutation',auglhs,augrhs)
    for label,x,y in [('A and B0',A,B[0]),('A and U',A,U),('B0 and B1',B[0],B[1]),('U and Bstar',U,B[4])]:
        if times(x,y) == times(y,x): raise AssertionError('unintended commutation: '+label)
        checks.append('noncommutation retained: '+label)
    eq('only required U/B0 commutation',times(U,B[0]),times(B[0],U))
    if lhs == scale(2,rhs):raise AssertionError('wrong prefactor accepted')
    checks.append('wrong prefactor rejected')
    return {'status':'supplementary_exact_checks_passed_NOT_LEAN','kernel_checked':False,
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),'checks_passed':len(checks),
        'check_names':checks,'word_reductions_cached':normal.cache_info().currsize,
        'allowed_commutations':'U with B0,B1,B2,B3 only; A, Bstar and distinct Bob generators remain free',
        'limitation':'Shared cyclotomic coefficient implementation; distinct word-algebra self-check, not an independent agent or kernel audit.'}

if __name__=='__main__':
    r=run(); dest=Path(sys.argv[1]);dest.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
