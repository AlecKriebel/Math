#!/usr/bin/env python3
"""Independent per-vertex finite diagnostics. Not a formal/asymptotic proof."""
from collections import Counter
from itertools import product
import hashlib,json,pathlib,sys

def require(ok,msg):
    if not ok: raise ValueError(msg)

def enum_words(colors,n):
    if n==0: yield (); return
    for p in product(range(len(colors)),repeat=n):
        if all(colors[p[j]]!=colors[p[j+1]] for j in range(n-1)):yield p

def invword(w,inv):return tuple(inv[a] for a in w[::-1])

def case(colors,inv,ell):
    q,r=divmod(ell,3)
    lengths=(q,q,q) if r==0 else ((q,q,q+1) if r==1 else (q,q+1,q+1))
    types=set(lengths)
    verts={t:tuple(w for w in enum_words(colors,t) if invword(w,inv)!=w) for t in types}
    actual=Counter(); total=0; kept=0
    for rel in enum_words(colors,ell):
        if colors[rel[0]]==colors[rel[-1]]:continue
        total+=1
        a=rel[:lengths[0]];b=rel[lengths[0]:lengths[0]+lengths[1]];c=rel[lengths[0]+lengths[1]:]
        if any(invword(w,inv)==w for w in (a,b,c)):continue
        kept+=1
        for x,y in ((a,b),(b,c),(c,a)):
            ix=invword(x,inv)
            actual[ix,y]+=1;actual[y,ix]+=1
    coeff=Counter()
    for j in range(3):
        t,u=lengths[j],lengths[(j+1)%3]
        coeff[t,u]+=1;coeff[u,t]+=1
    expected=Counter();checked=0
    for t,u in product(types,repeat=2):
        if not coeff[t,u]:continue
        h=ell-t-u
        for x,y in product(verts[t],verts[u]):
            checked+=1
            if colors[x[0]]==colors[y[0]]:continue
            completions=sum(colors[x[-1]]!=colors[z[0]] and colors[z[-1]]!=colors[y[-1]] for z in verts[h])
            value=coeff[t,u]*completions
            if value:expected[x,y]=value
    require(actual==expected,"per-vertex expected kernel mismatch")
    require(sum(actual.values())==6*kept,"edge incidence total mismatch")
    return {"colors":colors,"inverse":inv,"ell":ell,"cyclic_words":total,"retained":kept,"vertex_pairs_checked":checked,"kernel":"PASS"}

def main():
    tests=[]
    for colors,inv,ells in [((0,1,2),(0,1,2),(6,7,8,9)),((0,1,2,2),(0,1,2,3),(6,7,8)),((0,1,2,2),(0,1,3,2),(6,7,8)),((0,0,1,1,2),(1,0,3,2,4),(6,7,8))]:
        require(all(inv[inv[i]]==i and colors[inv[i]]==colors[i] for i in range(len(colors))),"invalid alphabet")
        for ell in ells:tests.append(case(colors,inv,ell))
    print(json.dumps({"status":"PASS","kind":"independent per-vertex exact finite diagnostic; not proof certification","cases":tests},indent=2,sort_keys=True))
if __name__=="__main__":main()
