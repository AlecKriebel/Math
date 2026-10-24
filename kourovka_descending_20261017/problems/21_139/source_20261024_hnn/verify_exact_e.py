#!/usr/bin/env python3
"""Direct covering-chain verification for E and a rank-two associated subgroup."""
from search_covers import fox_chain, rank, transitive, inv
from pathlib import Path
import json
from itertools import permutations

def exact_e(n):
    q=5;N=q*n;I=tuple(range(N));P=tuple(j*q+(i+1)%q for j in range(n) for i in range(q));T=[]
    for j in range(n):
        T.extend([5*j,5*j+1,5*((j+1)%n)+3,5*j+4,5*j+2])
    T=tuple(T); assert sorted(T)==list(I) and transitive([I,P,T])
    r=[-3,1,3,-2,-2,-2,-1,-2,-2,-1]
    d1,d2=fox_chain(r,[I,P,T]);r1=rank(d1);r2=rank(d2)
    witnesses=[]
    for j in range(n):
        x=[0]*N;x[5*j+1]=1;x[5*j+4]=-1
        assert all(sum(a*b for a,b in zip(row,x))==0 for row in d2);witnesses.append(x)
    assert N-r2==n and 3*N-r1-r2==6*n+1
    return {'copies':n,'degree':N,'b2':N-r2,'b1':3*N-r1-r2,'left_rep_b':P,'left_rep_t':T,'actual_right_cover_b':inv(P),'actual_right_cover_t':inv(T),'kernel_basis':witnesses}

def rank_two():
    I=(0,1);T=(1,0);gs=[I,I,I,T]
    rs=[[-4,1,4,-3,-2],[-4,2,4,-1,-3]]
    d1,d21=fox_chain(rs[0],gs);other,d22=fox_chain(rs[1],gs);assert d1==other
    d2=[a+b for a,b in zip(d21,d22)];b2=4-rank(d2)
    assert b2==1
    return {'presentation':'t^-1 a t=bc, t^-1 b t=ca','degree':2,'base_actions':'all identity','stable_action':T,'b2':b2,'d2':d2}

def auxiliary_e():
    I=tuple(range(5));P=tuple((i+1)%5 for i in range(5));hist={};first=None
    r=[-3,1,3,-2,-2,-2,-1,-2,-2,-1]
    for T in permutations(range(5)):
        d1,d2=fox_chain(r,[I,P,T]);b2=5-rank(d2);hist[b2]=hist.get(b2,0)+1
        if b2 and first is None:first={'degree':5,'left_rep_generators_a_b_t':[I,P,T],'actual_right_cover_generators_a_b_t':[I,inv(P),inv(T)],'b2':b2,'b1':15-rank(d1)-rank(d2),'d2':d2}
    return [{'degree':5,'hist':hist,'first':first}]

def solvable_e():
    I=tuple(range(5));P=tuple((i+1)%5 for i in range(5));T=tuple(2*i%5 for i in range(5));r=[-3,1,3,-2,-2,-2,-1,-2,-2,-1]
    d1,d2=fox_chain(r,[I,P,T]);assert 5-rank(d2)==1
    return {'degree':5,'b2':1,'b1':15-rank(d1)-rank(d2),'monodromy':'C5 semidirect C4, order 20','left_rep_b':P,'left_rep_t':T,'actual_right_cover_b':inv(P),'actual_right_cover_t':inv(T)}

if __name__=='__main__':
    result={'exact_e':[exact_e(n) for n in range(1,9)],'rank_two_boundary':rank_two(),'solvable_e':solvable_e()}
    Path(__file__).with_name('abelian_blind_results.json').write_text(json.dumps(auxiliary_e(),indent=2)+'\n')
    Path(__file__).with_name('exact_e_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'exact_e':[{k:v for k,v in x.items() if k in ('copies','degree','b1','b2')} for x in result['exact_e']],'rank_two_b2':result['rank_two_boundary']['b2']},indent=2))
