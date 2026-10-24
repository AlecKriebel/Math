#!/usr/bin/env python3
"""Reproduce telescoping finite-cover certificates using exact rational ranks."""
from search_covers import fox_chain, rank, transitive, inv
import json
from pathlib import Path

def build(p,k,eps,n):
    q=k*p+eps; assert q>=3 and p>=1 and k>=1 and eps in (-1,1)
    identity=tuple(range(n*q))
    P=tuple(v*q+(i+1)%q for v in range(n) for i in range(q))
    T=[None]*(n*q)
    free_sources=[];free_targets=[]
    for v in range(n):
        T[v*q]=v*q
        T[v*q+(-k)%q]=v*q+(-p*k)%q
        free_sources.append([v*q+i for i in range(q) if i not in (0,(-k)%q)])
        free_targets.append([v*q+i for i in range(q) if i not in (0,(-p*k)%q)])
    for v in range(n):
        T[free_sources[v][0]]=free_targets[(v+1)%n][0]
        for s,t in zip(free_sources[v][1:],free_targets[v][1:]):T[s]=t
    assert sorted(T)==list(range(n*q))
    word_B=([1]+[2]*k)*p+([2] if eps==1 else [-2])
    relator=[-3,1,3]+[-s for s in reversed(word_B)]
    gens=[identity,P,tuple(T)]
    assert transitive(gens)
    d1,d2=fox_chain(relator,gens)
    witnesses=[]
    for v in range(n):
        x=[0]*(n*q);x[v*q]=1;x[v*q+(-k)%q]=-1
        assert all(sum(a*b for a,b in zip(row,x))==0 for row in d2)
        witnesses.append(x)
    return {'p':p,'k':k,'epsilon':eps,'q':q,'copies':n,'degree':n*q,'left_rep_a':identity,'left_rep_b':P,'left_rep_t':T,'actual_right_cover_a':identity,'actual_right_cover_b':inv(P),'actual_right_cover_t':inv(T),'certified_independent_h2_classes':n,'exact_b2':n*q-rank(d2),'exact_b1':3*n*q-rank(d1)-rank(d2),'witnesses':witnesses}

if __name__=='__main__':
    cases=[(p,k,eps,n) for p,k,eps in [(2,2,1),(2,1,1),(3,1,1),(2,2,-1),(3,2,-1),(1,3,1)] for n in (1,2,3,4)]
    results=[build(*case) for case in cases]
    for r in results:print(json.dumps({k:v for k,v in r.items() if k not in ('left_rep_a','left_rep_b','left_rep_t','actual_right_cover_a','actual_right_cover_b','actual_right_cover_t','witnesses')}))
    Path(__file__).with_name('telescoping_results.json').write_text(json.dumps(results,indent=2)+'\n')
