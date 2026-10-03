#!/usr/bin/env python3
"""Exact structural controls written without candidate exposure; stdlib only."""
from fractions import Fraction
from collections import defaultdict
from math import log, exp
import json

def families(a, cap=None):
    out=defaultdict(list)
    for m in range(1 << len(a)):
        b=frozenset(a[i] for i in range(len(a)) if (m>>i)&1)
        if cap is None or len(b)<=cap:
            out[sum(b)].append(b)
    return out

def peak(a, cap=None, exact=None):
    f=families(tuple(sorted(a)),cap)
    return max((sum(exact is None or len(b)==exact for b in v) for v in f.values()),default=0)

def main():
    checks=0
    core_examples=[]
    # Complete enumeration of A subset [10], all cap h=1,2,3.
    for mask in range(1<<10):
        a=frozenset(i+1 for i in range(10) if (mask>>i)&1)
        f=families(tuple(sorted(a)))
        for cut in range(11):
            lo={x for x in a if x<=cut}; hi=a-lo
            assert peak(hi)<=peak(a)<=2**len(lo)*peak(hi)
            checks+=1
        for h in (1,2,3):
            c=set()
            ff=families(tuple(sorted(a)),h)
            for vv in ff.values():
                for u in vv:
                    for v in vv:
                        if u!=v:
                            c.update(u-v);c.update(v-u)
            assert peak(a,h)==peak(c,h)
            bound=max(peak(c,exact=j) for j in range(h+1))
            assert peak(a,exact=h)<=bound
            checks+=2
            if len(core_examples)<8 and c and len(c)<len(a):
                core_examples.append({'a':sorted(a),'h':h,'core':sorted(c),'cap_peak':peak(a,h),'exact_peak':peak(a,exact=h),'exact_bound':bound})
    # Independent coefficient multiplication for all disjoint adjacent blocks.
    tensors=[]
    for n in range(1,9):
        for cut in range(n+1):
            a=tuple(range(1,cut+1)); b=tuple(range(cut+1,n+1))
            ma=peak(a);mb=peak(b);mc=peak(a+b)
            assert mc>=ma*mb
            tensors.append({'n':n,'cut':cut,'left':ma,'right':mb,'union':mc})
            checks+=1
    # Exact ordered-composition weights and identity/bound, no floating arithmetic.
    comp={(1,s):Fraction(1,s) for s in range(1,61)}
    comp_checks=[]
    for t in range(2,6):
        for s in range(1,61):
            w=sum((comp.get((t-1,s-a),0)/a for a in range(1,s)),Fraction())
            comp[t,s]=w
            identity=Fraction(t,s)*sum((comp.get((t-1,u),0) for u in range(1,s)),Fraction())
            harm=sum((Fraction(1,a) for a in range(1,s)),Fraction())
            assert w==identity
            assert w<=Fraction(t,s)*harm**(t-1)
            checks+=2
        comp_checks.append({'t':t,'s':60,'weight':str(comp[t,60])})
    # Monotone staircase: t=loglogD, logM=2T_j on [T_j,T_{j+1}), T_j=2^j.
    staircase=[]
    for j in range(3,15):
        t=2**j
        staircase.append({'j':j,'at_jump_ratio':2,'before_next_jump_ratio':2*t/(2*t-1)})
    # Probability-to-one cannot itself imply eventual success: independent failure
    # probabilities 1/n tend to zero but their sum diverges, so BC II applies.
    result={'all_passed':True,'assertions':checks,'universe_subsets':1024,
            'core_examples':core_examples,'tensor_cases':tensors,
            'composition_cases':comp_checks,'staircase':staircase,
            'probability_mode_counterexample':{'independent_failure_probability':'1/n','failure_probability_limit':0,'failure_probability_sum':'infinity','infinitely_many_failures':'almost surely (Borel-Cantelli II)'},
            'limits':'Finite controls verify identities, not the FGK threshold theorem or an asymptotic sharp exponent.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
