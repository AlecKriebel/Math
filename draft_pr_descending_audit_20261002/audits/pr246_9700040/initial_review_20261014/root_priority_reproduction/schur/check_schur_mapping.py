#!/usr/bin/env python3
"""Independent finite controls for the priority mapping; standard library only.
No candidate implementation is imported. Output is an authored finite check.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations, combinations_with_replacement
from math import factorial
from pathlib import Path
import json, hashlib, datetime

OUT = Path(__file__).resolve().parent

def contained(mu, la):
    return len(mu) <= len(la) and all(a <= b for a,b in zip(mu,la))

@lru_cache(None)
def skew(la,mu=()):
    if not contained(mu,la): return 0
    if la == mu: return 1
    out=0
    for i,a in enumerate(la):
        if i+1 == len(la) or a > la[i+1]:
            ne=list(la); ne[i]-=1
            if ne[-1] == 0: ne.pop()
            ne=tuple(ne)
            if contained(mu,ne): out+=skew(ne,mu)
    return out

def determinant(M):
    M=[[F(x) for x in r] for r in M]
    ans=F(1)
    for i in range(len(M)):
        p=next((p for p in range(i,len(M)) if M[p][i]),None)
        if p is None:return F(0)
        if p!=i: M[p],M[i]=M[i],M[p];ans=-ans
        pivot=M[i][i];ans*=pivot
        for j in range(i+1,len(M)):
            c=M[j][i]/pivot
            for k in range(i+1,len(M)): M[j][k]-=c*M[i][k]
    return ans

@lru_cache(None)
def D(la,mu,t):
    if not contained(mu,la):return F(0)
    L=max(len(la),len(mu));a=la+(0,)*(L-len(la));b=mu+(0,)*(L-len(mu))
    def h(k):return t**k/factorial(k) if k>=0 else F(0)
    return determinant([[h(a[i]-b[j]-i+j) for j in range(L)] for i in range(L)])

def rsk_shapes(p):
    rows=[];sh=[()]
    for v in p:
        y=v
        for row in rows:
            j=next((j for j,a in enumerate(row) if a>y),None)
            if j is None:row.append(y);break
            row[j],y=y,row[j]
        else:rows.append([y])
        sh.append(tuple(map(len,rows)))
    return sh

cases=0; permutations_checked=0; chain_checks=0; determinant_checks=0
raw_results={}
for n in range(8):
    counts={cuts:{} for cuts in combinations_with_replacement(range(n+1),2)}
    for p in permutations(range(1,n+1)):
        permutations_checked+=1
        sh=rsk_shapes(p)
        for (a,b), dic in counts.items():
            chain=(sh[a],sh[b],sh[n]);dic[chain]=dic.get(chain,0)+1
    raw_c=F(0);raw_brute=F(0)
    for (a,b), dic in counts.items():
        d=(a,b-a,n-b)
        for chain,count in dic.items():
            cases+=1;last=();prod=1
            for la in chain:prod*=skew(la,last);last=la
            pred=skew(chain[-1])*prod
            assert count==pred, (n,(a,b),chain,count,pred)
            chain_checks+=1
            cand=D(chain[-1],(),F(1));last=()
            nica=D(chain[-1],(),F(2));markov=F(1);oldn=0;olddim=1
            for la,delta in zip(chain,map(F,(1,2,1))):
                dim=skew(la);newn=sum(la);dd=newn-oldn
                f=skew(la,last)
                det=D(la,last,delta)
                assert det == delta**dd*f/factorial(dd)
                determinant_checks+=1
                cand*=det;nica*=D(la,last,delta/2)
                markov*=delta**dd/factorial(dd)*F(f*dim*factorial(oldn),olddim*factorial(newn))
                last=la;oldn=newn;olddim=dim
            assert cand==nica==markov
            # Nonmonotone row bounds b=(2,1,3).
            if all((la[0] if la else 0)<=bound for la,bound in zip(chain,(2,1,3))):
                raw_c+=cand
                raw_brute+=F(count,factorial(n))*F(1)**d[0]/factorial(d[0])*F(2)**d[1]/factorial(d[1])*F(1)**d[2]/factorial(d[2])
        # Shape probabilities conditional on these cut sizes sum to 1.
        assert sum(dic.values())==factorial(n)
    assert raw_c==raw_brute
    raw_results[str(n)]={'raw_constrained_mass':str(raw_c),'checked_permutation_counts':True}
result={
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'purpose':'Exact parameter/orientation controls for Schur/Plancherel/Nica priority identification; not exhaustive historical proof',
 'terminal_sizes':list(range(8)), 'permutations_checked':permutations_checked,
 'shape_chain_count_equalities':chain_checks,'skew_determinant_equalities':determinant_checks,
 'time_increment_controls':[1,2,1], 'Nica_square_side':2,
 'identities':'candidate raw chain weight = square rescaled Nica raw weight = Poissonized Plancherel raw Markov weight',
 'nonmonotone_bounds':[2,1,3], 'raw_constrained_mass_by_terminal_size':raw_results,
 'all_passed':True,
}
(OUT/'EXACT_MAPPING_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='raw_constrained_mass_by_terminal_size'},indent=2))
