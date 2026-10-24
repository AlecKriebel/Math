#!/usr/bin/env python3
"""Exact finite-permutation covering H2 for two free-factor cyclic HNN controls.
Only standard library. The rank computation uses exact fractions.
Permutation convention P(p)e_i=e_{p(i)} for a LEFT representation.
The actual cellular cover uses RIGHT generator actions p^{-1}; its boundary
blocks equal Fox D_x^T, checked by direct edge walks on every computed action.
"""
from itertools import permutations, product
from fractions import Fraction
import json

def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
    r=[0]*len(p)
    for i,j in enumerate(p): r[j]=i
    return tuple(r)
def eval_word(word,gens):
    p=tuple(range(len(gens[0])))
    for s in word: p=compose(p,gens[s-1] if s>0 else inv(gens[-s-1]))
    return p

def rank(mat):
    a=[[Fraction(x) for x in row] for row in mat]
    m,n=len(a),len(a[0]); k=0
    for j in range(n):
        i=next((i for i in range(k,m) if a[i][j]),None)
        if i is None: continue
        a[k],a[i]=a[i],a[k]
        x=a[k][j]; a[k]=[y/x for y in a[k]]
        for i in range(m):
            if i!=k and a[i][j]:
                x=a[i][j];a[i]=[y-x*z for y,z in zip(a[i],a[k])]
        k+=1
        if k==min(m,n): break
    return k

def direct_cover_chain(word,right_gens):
    n=len(right_gens[0]);rank_f=len(right_gens)
    d1=[[0]*(rank_f*n) for _ in range(n)]
    d2=[[0]*n for _ in range(rank_f*n)]
    for x,g in enumerate(right_gens):
        for i,j in enumerate(g):
            d1[j][x*n+i]+=1;d1[i][x*n+i]-=1
    inverses=[inv(g) for g in right_gens]
    for face in range(n):
        sheet=face
        for letter in word:
            x=abs(letter)-1
            if letter>0:
                d2[x*n+sheet][face]+=1;sheet=right_gens[x][sheet]
            else:
                sheet=inverses[x][sheet];d2[x*n+sheet][face]-=1
        assert sheet==face
    return d1,d2

def fox_chain(word,gens):
    n=len(gens[0]); ident=tuple(range(n)); pref=ident
    ds=[[[0]*n for _ in range(n)] for _ in gens]
    for s in word:
        g=gens[abs(s)-1]
        if s>0:
            for j in range(n): ds[s-1][pref[j]][j]+=1
            pref=compose(pref,g)
        else:
            pref=compose(pref,inv(g))
            for j in range(n): ds[-s-1][pref[j]][j]-=1
    assert pref==ident
    d2=[[ds[x][j][i] for j in range(n)] for x in range(len(gens)) for i in range(n)]
    d1=[[int(gens[x][i]==j)-int(i==j) for x in range(len(gens)) for j in range(n)] for i in range(n)]
    assert all(sum(d1[i][k]*d2[k][j] for k in range(n*len(gens)))==0 for i in range(n) for j in range(n))
    assert (d1,d2)==direct_cover_chain(word,[inv(g) for g in gens])
    return d1,d2

def transitive(gens):
    orbit={0}
    while True:
        nxt=orbit|{g[i] for g in gens for i in orbit}
        if nxt==orbit:return len(orbit)==len(gens[0])
        orbit=nxt

def search(word,limit=4):
    levels=[]
    for n in range(1,limit+1):
        ps=list(permutations(range(n)));total=0;hist={};first=None
        for gs in product(ps,repeat=3):
            if eval_word(word,gs)!=tuple(range(n)) or not transitive(gs):continue
            total+=1
            d1,d2=fox_chain(word,gs);b2=n-rank(d2);hist[b2]=hist.get(b2,0)+1
            if b2 and first is None:
                first={"degree":n,"left_rep_generators_a_b_t":gs,"actual_right_cover_generators_a_b_t":[inv(g) for g in gs],"b2":b2,"b1":3*n-rank(d1)-rank(d2),"d1":d1,"d2":d2}
        levels.append({"degree":n,"transitive_labeled_actions":total,"b2_histogram":hist,"first_positive":first})
        print(json.dumps(levels[-1]),flush=True)
    return levels

if __name__=='__main__':
    # G=<a,b,t | t^-1 a t = a b a b^2>.
    relator=[-3,1,3,-2,-2,-1,-2,-1]
    result=search(relator,4)
    with open(__file__.replace('search_covers.py','cover_results.json'),'w') as f:json.dump(result,f,indent=2)
