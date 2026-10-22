"""Reviewer-owned independent finite controls; does not import author code."""
from itertools import combinations
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
ROOT=Path(__file__).resolve().parent.parent

def vertices(H): return set().union(*H) if H else set()
def tau(H):
    V=sorted(vertices(H))
    for k in range(len(V)+1):
        for C in combinations(V,k):
            if all(set(C)&e for e in H): return k
    raise ValueError('empty edge')
def degree(H):
    return {v:sum(v in e for e in H) for v in vertices(H)}
def delta(H): return max(degree(H).values(),default=0)
def packing(H,s):
    for k in range(len(H),-1,-1):
        good=[I for I in combinations(range(len(H)),k) if delta([H[i] for i in I])<=s]
        if good:return k,good
def pq(H,p,q):
    return all(any(len(set.intersection(*(set(H[i]) for i in J)))>0 for J in combinations(I,q)) for I in combinations(range(len(H)),p))
def pad(H,r):
    V=vertices(H); fresh=max(V,default=-1)+1; result=[]
    for e in H:
        d=r-len(e);result.append(e|set(range(fresh,fresh+d)));fresh+=d
    return result

def witness(H,t):
    assert tau(H)>t
    E=H[0]
    if t==0:return [E]
    W=[E]
    for x in E:
        W+=witness([e for e in H if x not in e],t-1)
    return list(dict.fromkeys(map(frozenset,W)))

counts={'rank3_families':0,'padding_tau_and_packings':0,'growth':0,'pq_equivalence':0,'finite_witnesses':0,'maximal_cover_certificates':0}
E=[frozenset(x) for k in range(1,4) for x in combinations(range(3),k)]
for mask in range(1<<len(E)):
    H=[e for i,e in enumerate(E) if mask>>i&1];m=len(H);counts['rank3_families']+=1
    P=pad(H,3)
    assert len(P)==len(set(map(frozenset,P)))
    assert tau(P)==tau(H)
    ns={s:packing(H,s)[0] for s in range(1,m+2)}
    for s in range(1,m+2):
        assert packing(P,s)[0]==ns[s];counts['padding_tau_and_packings']+=1
    for s in range(1,m+1):
        assert ns[s+1]>=min(m,ns[s]+1);counts['growth']+=1
    for p in range(2,m+1):
        for q in range(2,p+1):
            assert pq(H,p,q)==(ns[q-1]<=p-1)
            assert pq(H,p,q)==pq(P,p,q);counts['pq_equivalence']+=1
    for t in range(tau(H)):
        W=witness(H,t);assert tau(W)>t and len(W)<=sum(3**i for i in range(t+1));counts['finite_witnesses']+=1
    # Every inclusion-maximal rank-3 packing, including empty H.
    for sm in range(1<<m):
        M=[e for i,e in enumerate(H) if sm>>i&1]
        if delta(M)>3:continue
        if any(delta(M+[e])<=3 for i,e in enumerate(H) if not sm>>i&1):continue
        S={v for v,d in degree(M).items() if d==3}
        N=[e for e in M if e&S];M0=[e for e in M if not e&S]
        D=len(N)-len(S)
        assert D>=0 and tau(H)<=len(S)+tau(M0)<=len(M)
        counts['maximal_cover_certificates']+=1

fano=list(map(frozenset,({0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5})))
H=fano+[frozenset({0,1,7})]
def structural(H,r):
    k,packings=packing(H,r);detail=[]
    for I in packings:
        M=[H[i] for i in I];S={v for v,d in degree(M).items() if d==r};N=[e for e in M if e&S];M0=[e for e in M if not e&S]
        detail.append({'mask':sum(1<<i for i in I),'saturated':sorted(S),'surplus':len(N)-len(S),'residual_edges':len(M0),'certificate_saving':len(N)-len(S)+len(M0)-tau(M0)})
    return {'r':r,'vertices':len(vertices(H)),'edges':len(H),'tau':tau(H),'nu_r':k,'maximum_packings':sorted(detail,key=lambda d:d['mask'])}
actual={'extended_fano':structural(H,3),'simplex':structural([frozenset(set(range(4))-{i}) for i in range(4)],3)}
expected=json.loads((ROOT/'turn2_structural_results.json').read_text())
assert all(actual[k]==expected[k] for k in actual)
assert {sum(bool(e&set(pair)) for e in fano) for pair in combinations(range(7),2)}=={5}
assert {sum(bool(e&{v,7}) for e in fano) for v in range(7)}=={3}
assert all(tau([e for j,e in enumerate([frozenset(set(range(4))-{i}) for i in range(4)]) if j!=k])==1 for k in range(4))

# Known controls distinguish maximum from merely maximal; demonstrate why Delta>r matters.
k4=[frozenset(e) for e in combinations(range(4),2)];triangle=[e for e in k4 if 3 not in e]
assert delta(triangle)==2 and all(delta(triangle+[e])>2 for e in k4 if e not in triangle)
assert tau(k4)==3 and packing(k4,2)[0]==4 and tau(k4)>len(triangle)-1
matching=[frozenset({0,1}),frozenset({2,3})]
assert delta(matching)<=2 and tau(matching)>packing(matching,2)[0]-1
# Equality families: all finite r,t in this small declared control grid.
cyclic=[]
for r in range(2,5):
 for t in range(2,5):
    n=r+t-1;C=[frozenset((i+j)%n for j in range(r)) for i in range(n)]
    assert len(C)==len(set(C))==n and set(degree(C).values())=={r}
    # Complete family has t-cover threshold from complements, no packing optimization needed.
    assert n-r+1==t
    cyclic.append({'r':r,'tau':t,'n':n,'cyclic_edges':n,'degrees_all_r':True})
result={'all_pass':True,'counts':counts,'structural_results_match':True,'structural_results':actual,'known_negative_controls':['K4 maximal triangle cannot substitute for maximum packing','two disjoint graph edges refute inequality if Delta>r guard is removed'],'cyclic_packing_controls':cyclic}
(OUT/'reviewer_reduction_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('structural_results','cyclic_packing_controls')},indent=2))
