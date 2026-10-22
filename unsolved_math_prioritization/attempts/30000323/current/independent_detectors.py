#!/usr/bin/env python3
"""Independent exact finite detector audit; never evaluates MSTOP cohomology."""
from collections import defaultdict
from fractions import Fraction
from itertools import product, combinations_with_replacement
from math import gcd, lcm
import json, os, sys

def check(ok, message):
    if not ok:
        raise RuntimeError(message)

def points(ns):
    return tuple(product(*(range(n) for n in ns)))

def phase(ns, w, g):
    return sum((Fraction(a*b,n) for a,b,n in zip(w,g,ns)), Fraction()) % 1

def avoid(ns, ws):
    return tuple(g for g in points(ns) if all(phase(ns,w,g) for w in ws))

def ring(ns, ws):
    # Independent distributive expansion indexed by subsets, not convolution.
    out=defaultdict(int)
    for selection in product((0,1), repeat=len(ws)):
        key=tuple(sum(flag*w[i] for flag,w in zip(selection,ws))%n for i,n in enumerate(ns))
        out[key]+=(-1)**sum(selection)
    return {key:value for key,value in out.items() if value}

def polynomial(ws, p=None, ns=None):
    # Explicit monomial selections; optional coefficient reduction.
    rank=len(ws[0]) if ws else len(ns)
    out=defaultdict(int)
    for choices in product(range(rank),repeat=len(ws)):
        coefficient=1; exponents=[0]*rank
        for w,i in zip(ws,choices):
            coefficient*=w[i]; exponents[i]+=1
        out[tuple(exponents)]+=coefficient
    if p is not None:
        return {k:v%p for k,v in out.items() if v%p}
    if ns is not None:
        reduced={}
        for k,v in out.items():
            divisor=0
            for a,n in zip(k,ns):
                if a: divisor=gcd(divisor,n)
            v=v%divisor if divisor else v
            if v: reduced[k]=v
        return reduced
    return {k:v for k,v in out.items() if v}

def order(ns,w):
    return lcm(*(n//gcd(n,a) for n,a in zip(ns,w)))

def generated(ns, gens):
    if not gens: return frozenset([(0,)*len(ns)])
    return frozenset(tuple(sum(a*g[i] for a,g in zip(coeffs,gens))%n for i,n in enumerate(ns))
                     for coeffs in product(*(range(order(ns,g)) for g in gens)))

def subgroups(ns):
    zero=(0,)*len(ns); found={frozenset([zero]):()}; queue=[frozenset([zero])]
    while queue:
        h=queue.pop()
        for g in points(ns):
            if g in h: continue
            gens=found[h]+(g,); larger=generated(ns,gens)
            if larger not in found:
                found[larger]=gens;queue.append(larger)
    return tuple(found)

def run():
    cases=[]
    for p in (3,5,7,11,13):
        ns=(p*p,p); ws=((p,0),)+tuple((a*p,1) for a in range(p))
        check(not avoid(ns,ws),'W kernel cover')
        check(not ring(ns,ws),'W representation-ring vanishing')
        check(not polynomial(ws,p=p),'W mod-p vanishing')
        # pu*v=0 already occurs in the Chern-generated tensor subring.
        check(not polynomial(ws,ns=ns),'W integral Chern polynomial vanishing')
        kernels={frozenset(g for g in points(ns) if not phase(ns,w,g)) for w in ws}
        check(len(kernels)==p+1 and all(len(h)==p*p for h in kernels),'W distinct maximal kernels')
        proper_count=None
        if p in (3,5,7):
            all_h=subgroups(ns); proper=[h for h in all_h if len(h)<p**3]
            check(all(any(all(not phase(ns,w,g) for g in h) for w in ws) for h in proper),'W all proper subgroup fixed lines')
            proper_count=len(proper)
        deletion_counts=[]
        for i in range(len(ws)):
            smaller=ws[:i]+ws[i+1:]
            available=avoid(ns,smaller)
            check(len(available)==p*(p-1),'deletion uncovered count')
            check(bool(ring(ns,smaller)),'deletion ring detector')
            deletion_counts.append(len(available))
        ews=((1,0),)+tuple((a,1) for a in range(p))
        check(not ring((p,p),ews) and bool(polynomial(ews,p=p)),'elementary complementary detectors')
        check(not polynomial(((p,),(p,)),p=p) and bool(ring((p*p,),((p,),(p,)))),'cyclic complementary detectors')
        check(not ring(ns,ws+((0,0),)),'trivial-line zero')
        primitive=((1,0),)+ws[1:]
        check(bool(polynomial(primitive,p=p)),'primitive replacement ordinary detector')
        check(not polynomial(ws,p=p) and bool(polynomial(ews,p=p)),'inflation does not preserve ordinary nonvanishing')
        check({(a*p,0):1 for a in range(p)}!={(0,0):p},'transfer is not scalar index')
        cases.append({'p':p,'group_orders':ns,'W_K_ring_zero':True,'W_mod_p_zero':True,
                      'W_integral_Chern_polynomial_zero':True,'maximal_kernels':len(kernels),
                      'all_proper_subgroups_enumerated':proper_count,'deletion_counts':deletion_counts})
    exhausted=0; numerical_cases=0; primitive_cases=0; covered_cases=0
    group_list=((3,),(9,),(27,),(3,3),(9,3),(3,3,3))
    for ns in group_list:
        weights=[g for g in points(ns) if any(g)]
        maxd=4 if ns==(3,3) else 3
        for d in range(0,maxd+1):
            for ws in combinations_with_replacement(weights,d):
                avoidance=bool(avoid(ns,ws)); kr=bool(ring(ns,ws))
                check(avoidance==kr,'exact character-ring/avoidance equivalence')
                ordinary=bool(polynomial(ws,p=3,ns=ns))
                primitive=all(any(a%3 for a in w) for w in ws)
                check(ordinary==primitive,'mod-p iff no p-divisible weight')
                check(d>3 or avoidance,'dimension <= p')
                sum_orders=sum((Fraction(1,order(ns,w)) for w in ws),Fraction())
                if sum_orders<=1:
                    check(avoidance,'reciprocal-order sufficient criterion');numerical_cases+=1
                for w in ws:
                    restricted=any(phase(ns,w,g) for g in points(ns) if all((3*a)%n==0 for a,n in zip(g,ns)))
                    check(restricted==any(a%3 for a in w),'primitive iff nontrivial on G[p]')
                exhausted+=1; primitive_cases+=primitive; covered_cases+=not avoidance
    # Disallow accidental use of Python assert as an optimization-sensitive guard.
    caught=False
    try: check(False,'forced guard failure')
    except RuntimeError: caught=True
    check(caught,'explicit guard contract')
    return {'status':'passed','python_optimize':sys.flags.optimize,'uid':os.getuid(),'euid':os.geteuid(),
            'exhaustive_multisets':exhausted,'reciprocal_order_cases':numerical_cases,
            'mod_p_detected_multisets':primitive_cases,'kernel_cover_multisets':covered_cases,
            'cases':cases,'scope':'Finite character algebra only; no MSTOP cohomology, novelty, or full resolution claim.'}
if __name__=='__main__': print(json.dumps(run(),indent=2))
