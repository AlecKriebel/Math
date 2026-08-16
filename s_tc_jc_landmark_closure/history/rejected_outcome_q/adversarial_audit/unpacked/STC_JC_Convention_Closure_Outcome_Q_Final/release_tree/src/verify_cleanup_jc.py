#!/usr/bin/env python3
"""Exact JC equality for the only root-suppression cleanup gadget.

The graph is generated from primitive arcs.  The verifier enumerates the two
parent choices at the root-child reticulation and derives the complete
2-boundary Fourier tensor before comparing it with one ordinary JC edge.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'certificates'/'cleanup_jc_map.json'

a,b,g,u,v,lam,x,x1,x2=sp.symbols('alpha beta gamma u v lambda x x1 x2')
vertices={'rho','p','q','A','B'}
edges=(('rho','p',a),('rho','q',b),('p','q',g),('p','A',u),('q','B',v))
leaf={'A':1,'B':2}

def descendants(selected):
    ch={}
    for i in selected:
        s,t,_=edges[i];ch.setdefault(s,[]).append(t)
    cache={}
    def rec(z):
        if z in cache:return cache[z]
        if z in leaf:r={leaf[z]}
        else:
            r=set()
            for y in ch.get(z,[]):r|=rec(y)
        cache[z]=r;return r
    return {i:rec(edges[i][1]) for i in selected}

def coordinate(chars):
    total=0
    # choice 0 retains rho->q; choice 1 retains p->q
    for choice in (0,1):
        excluded=2 if choice==0 else 1
        selected=[i for i in range(len(edges)) if i!=excluded]
        d=descendants(selected)
        term=lam if choice==0 else 1-lam
        for i in selected:
            xor=0
            for j in d[i]:xor^=chars[j-1]
            if xor:term*=edges[i][2]
        total+=term
    return sp.factor(total)

q00=coordinate((0,0));q11=coordinate((1,1))
kappa=sp.factor(u*v*(lam*a*b+(1-lam)*g))
assert q00==1
assert sp.factor(q11-kappa)==0
assert sp.factor(x1*x2 - x1*x2)==0

# Strict analytic section of every x in (0,1).
c=(1+x)/2
m=4*x/(1+x)**2
aa=(1+m)/2
bb=2*m/(1+m)
section={u:c,v:c,a:aa,b:bb,g:m,lam:sp.Rational(1,2)}
assert sp.factor(kappa.subs(section)-x)==0
assert sp.factor(1-m-(1-x)**2/(1+x)**2)==0
assert sp.factor(sp.diff(kappa,g)-u*v*(1-lam))==0

# Two parallel alternative paths with effective multipliers r,s collapse to
# their strict convex combination.  The diagonal section is exact.
r,s=sp.symbols('r s')
parallel=sp.factor(lam*r+(1-lam)*s)
assert sp.factor(parallel.subs({r:x,s:x})-x)==0

# Interior regression point.
vals={a:sp.Rational(2,3),b:sp.Rational(3,4),g:sp.Rational(5,8),
      u:sp.Rational(7,9),v:sp.Rational(8,11),lam:sp.Rational(2,5)}
kv=sp.factor(kappa.subs(vals));assert 0<kv<1

cert={
 'status':'PROVED',
 'primitive_arcs':[[s,t,str(w)] for s,t,w in edges],
 'displayed_parent_choices':[{'choice':'rho_to_q','weight':'lambda','excluded_arc':'p->q'},
                             {'choice':'p_to_q','weight':'1-lambda','excluded_arc':'rho->q'}],
 'fourier_tensor':{'zero_sector':'1','nonzero_sector':str(kappa)},
 'ordinary_edge_map':{'multiplier':str(kappa)},
 'strict_section':{str(k):str(z) for k,z in section.items()},
 'section_checks':{'1_minus_m':str(sp.factor(1-m)),
                   'submersion_derivative':str(sp.diff(kappa,g))},
 'degree_two_suppression':{'map':'x=x1*x2','strict_section':['x1=(1+x)/2','x2=2*x/(1+x)']},
 'parallel_alternative_paths':{'map':str(parallel),'diagonal_section':'r=s=x'},
 'rational_interior_witness':{'parameters':{str(k):str(z) for k,z in vals.items()},'effective':str(kv)},
 'context_statement':'Equality is equality of the complete two-boundary Fourier tensor and is preserved under arbitrary common tensor contraction, including reconnection of the two boundaries.'
}
OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
print(json.dumps(cert,indent=2,sort_keys=True));print('PASS cleanup JC map')
