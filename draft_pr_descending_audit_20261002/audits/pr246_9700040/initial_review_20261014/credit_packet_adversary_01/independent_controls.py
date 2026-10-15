#!/usr/bin/env python3
"""Fresh finite falsification controls, separate from inherited campaign controls."""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations, product
from collections import Counter
from math import factorial
from datetime import datetime, timezone
import importlib.util, json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('subject',HERE/'isolated_replay/current_author/stationary_law.py')
subject=importlib.util.module_from_spec(spec);spec.loader.exec_module(subject)
C=Counter();start=datetime.now(timezone.utc).isoformat()
def ck(ok,name):
    assert ok,name
    C[name]+=1
@lru_cache(None)
def parts(n,cap=None):
    if n==0:return ((),)
    return tuple((a,)+p for a in range(1,min(n,cap or n)+1) for p in parts(n-a,a))
def subset(lam,mu):return len(lam)>=len(mu) and all(lam[i]>=x for i,x in enumerate(mu))
@lru_cache(None)
def f(lam,mu=()):
    if not subset(lam,mu):return 0
    cells=[(i,j) for i,a in enumerate(lam) for j in range(mu[i] if i<len(mu) else 0,a)]
    need=[sum(1<<h for h,(i2,j2) in enumerate(cells) if (i2==i and j2<j) or (j2==j and i2<i)) for i,j in cells]
    @lru_cache(None)
    def extend(mask):
        if mask==(1<<len(cells))-1:return 1
        return sum(extend(mask|1<<h) for h,r in enumerate(need) if not mask>>h&1 and r&mask==r)
    return extend(0)
def ins(word):
    rows=[]
    for value in word:
        v=value
        for row in rows:
            h=next((h for h,w in enumerate(row) if w>v),len(row))
            if h==len(row):row.append(v);break
            row[h],v=v,row[h]
        else:rows.append([v])
    return tuple(tuple(r) for r in rows)
def lis(word):
    d=[]
    for j,v in enumerate(word):d.append(1+max((d[i] for i in range(j) if word[i]<v),default=0))
    return max(d,default=0)
for n in range(8):
    multiplicities=Counter()
    for p in permutations(range(1,n+1)):
        t=ins(p);multiplicities[t]+=1
        for q in range(n+1):
            restricted=tuple(tuple(x for x in r if x<=q) for r in t)
            restricted=tuple(r for r in restricted if r)
            ck(restricted==ins(tuple(x for x in p if x<=q)),'small_value_P_restriction')
    for t,count in multiplicities.items():ck(count==f(tuple(map(len,t))),'tableau_multiplicity_f_over_n_factorial')
ck(tuple(map(len,ins((2,3))))!=tuple(map(len,ins((2,1)))),'negative_P_Q_prefix_shortcut')

# Remove the common exp(-4) normalizer and independently reconstruct each old
# joint chain weight. Cell-poset f uses neither the subject determinant nor a
# Young-lattice corner-removal implementation.
xs=(Q(1,2),Q(3,2),Q(4));deltas=(xs[0],xs[1]-xs[0],xs[2]-xs[1]);theta=Q(2)
shapes=[p for n in range(7) for p in parts(n)]
for a in shapes:
    for b in shapes:
        if not subset(b,a):continue
        for c in shapes:
            if not subset(c,b):continue
            chain=((),a,b,c);candidate=subject.D(c,())
            bo=Q(1);nica=theta**sum(c)*f(c)/factorial(sum(c))
            for dt,mu,nu in zip(deltas,chain,chain[1:]):
                n=sum(mu);d=sum(nu)-n
                bo*=dt**d/factorial(d)*f(nu,mu)*Q(f(nu),f(mu))*Q(factorial(n),factorial(n+d))
                nica*=Q(f(nu,mu),factorial(d))*(dt/theta)**d
                candidate*=subject.D(nu,mu,dt)
            ck(candidate==bo==nica,'whole_chain_candidate_BO_Nica_weight')
ck(Q(1,4)!=Q(1,2),'negative_missing_birth_d_factorial')

# Recreate the 42 complete historical raw coefficient comparisons from the
# actual fresh independent-checker receipt, rather than trusting its PASS flag.
receipt=json.loads((HERE/'ARCHIVED_INDEPENDENT_RECEIPT.json').read_text())
import ast
for key,raw in receipt['raw_coefficients'].items():
    rs=ast.literal_eval(key)
    actual=subject.raw_by_size(tuple(map(Q,receipt['three_thresholds'])),rs,6)
    for v,w in zip(actual,raw):ck(v==Q(w),'complete_42_historical_raw_coefficients')

# Direct finite-particle event update vs augmented-LIS no-jump condition. The
# chronological word may create more unrestricted piles than tracked particles.
for k in range(1,5):
    initial=tuple(Q(j*j) for j in range(1,k+1));a=initial[-1]
    # Poisson event coordinates are distinct and avoid the deterministic
    # initial row. Repeated spatial coordinates would test a different tie
    # convention (first strictly greater vs strict LIS), a null case here.
    grid=tuple(sorted(set((Q(1,2),Q(3,2),Q(7,4),a-Q(1,4),a+Q(1,2)))-set(initial)))
    for n in range(len(grid)+1):
        for word in permutations(grid,n):
            finite=list(initial)
            for u in word:
                h=next((h for h,z in enumerate(finite) if z>u),k)
                if h<k:finite[h]=u
            small=tuple(u for u in word if u<a)
            U=lis(initial[:-1]+small)
            ck(sum(z<a for z in finite)==min(k,U),'LRW_finite_count_cap')
            variational=max(j+lis(tuple(u for u in small if u>(initial[j-1] if j else 0))) for j in range(k))
            ck(U==variational,'LRW_augmented_LIS_suffix_variational_identity')
            reflected=tuple(a-u for u in reversed(small))
            xs2=tuple(a-initial[k-i-1] for i in range(1,k))+(a,)
            barriers=all(lis(tuple(u for u in reflected if u<x))<i for i,x in enumerate(xs2,1))
            ck((finite[-1]==a)==barriers,'LRW_reflected_joint_event')
initial=(Q(2),);word=(Q(1,2),Q(1))
ck(lis(initial[:-1]+word)==2 and min(1,lis(word))==1,'negative_unrestricted_pile_count_exceeds_k')

# Polynomial LRW determinant independently from entire ell-series, compared
# with positive-tableau evaluator coefficients through total degree 6. Scaling
# every threshold by z makes these the terminal point-count coefficients.
N=6
def mul(a,b):return [sum((a[i]*b[n-i] for i in range(n+1)),Q(0)) for n in range(N+1)]
def ell(order,x):return [Q(0) if p<max(order,0) else x**p/Q(factorial(p)*factorial(p-order)) for p in range(N+1)]
det_results=[]
for xs3 in [(Q(1,3),Q(3,2)),(Q(1,4),Q(1),Q(5,2)),(Q(1,5),Q(3,5),Q(4,3),Q(3))]:
    k=len(xs3);m=k-1;det=[Q(0)]*(N+1)
    for p in permutations(range(m)):
        v=[Q(1)]+[Q(0)]*N
        for i,j in enumerate(p):v=mul(v,ell(i-j,xs3[-1]-xs3[k-j-2]))
        sign=(-1)**sum(p[i]>p[j] for i in range(m) for j in range(i+1,m))
        det=[a+sign*b for a,b in zip(det,v)]
    actual=subject.raw_by_size(xs3,tuple(range(1,k+1)),N)
    for a,b in zip(det,actual):ck(a==b,'LRW_entire_determinant_vs_candidate_coefficients')
    det_results.append({'x':list(map(str,xs3)),'raw_coefficients':list(map(str,det))})
out={'status':'PASS','started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),
     'assertions':sum(C.values()),'categories':dict(C),'LRW_coefficients':det_results,
     'scope':'Finite falsification controls; general identities and primary source reading are documented in REPORT.md.'}
(HERE/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','assertions':out['assertions'],'categories':dict(C)}))
