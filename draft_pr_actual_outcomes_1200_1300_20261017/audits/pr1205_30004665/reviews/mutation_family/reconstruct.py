#!/usr/bin/env python3
"""Independent, exact GHKK reconstruction from reduced-word seeds.

No candidate input/code is imported. Python 3 + sympy 1.14.0.
The matrix B[i][j] is arrows i->j minus arrows j->i.
X'_i=X_i(1+X_k**(-sign B[i][k]))**(-B[i][k]).
Sources: KS2022 Def5, Eq3, Def7; GKS arXiv1711.07176 4.2.2.
"""
from collections import deque
from pathlib import Path
import json, hashlib, itertools, sys
import sympy as s

HERE=Path(__file__).resolve().parent
WORD=(1,2,3,2,4,2,1,2,3,2,4,2)
EDGES={frozenset((1,2)),frozenset((2,3)),frozenset((2,4))}

def adjacent(a,b): return frozenset((a,b)) in EDGES

def seed(word):
    n=len(word)
    nxt=[next((j for j in range(i+1,n) if word[j]==word[i]),n) for i in range(n)]
    frozen={i for i in range(n) if nxt[i]==n}
    B=[[0]*n for _ in word]
    for i in range(n):
        for j in range(i+1,n):
            if i in frozen and j in frozen: continue
            if j==nxt[i]: B[i][j]=1; B[j][i]=-1
            elif j<nxt[i]<nxt[j] and adjacent(word[i],word[j]):
                B[j][i]=1; B[i][j]=-1
    return B,frozen

def mutate_B(B,k,frozen):
    n=len(B)
    C=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i in frozen and j in frozen: continue
            C[i][j]=(-B[i][j] if k in (i,j) else B[i][j]
                       +max(B[i][k],0)*max(B[k][j],0)
                       -max(-B[i][k],0)*max(-B[k][j],0))
    return C

def mutate_X(X,B,k,wrong_sign=False):
    out=list(X)
    for i in range(len(X)):
        if i==k: out[i]=1/X[k]
        elif B[i][k]:
            b=B[i][k]*(-1 if wrong_sign else 1)
            out[i]=s.cancel(X[i]*(1+X[k]**(-s.sign(b)))**(-b))
    return out

def swap(B,X,frozen,p,q):
    n=len(B); perm=list(range(n)); perm[p],perm[q]=q,p
    return [[B[perm[i]][perm[j]] for j in range(n)] for i in range(n)], [X[perm[i]] for i in range(n)], {perm[i] for i in frozen}

def neighbors(w,reverse=False):
    moves=[]
    for p in range(len(w)-1):
        a,b=w[p:p+2]
        if a!=b and not adjacent(a,b):
            v=list(w);v[p:p+2]=b,a; moves.append((tuple(v),('commute',p)))
    for p in range(len(w)-2):
        a,b,c=w[p:p+3]
        if a==c and adjacent(a,b):
            v=list(w);v[p:p+3]=b,a,b; moves.append((tuple(v),('braid',p)))
    return reversed(moves) if reverse else moves

def routes(start,reverse=False):
    parent={start:None}; queue=deque([start]); found={}
    while queue and len(found)<4:
        w=queue.popleft()
        if w[-1] not in found:
            path=[]; cur=w
            while parent[cur] is not None:
                prev,move=parent[cur];path.append(move);cur=prev
            found[w[-1]]=list(reversed(path))
        for v,move in neighbors(w,reverse):
            if v not in parent: parent[v]=(w,move);queue.append(v)
    assert len(found)==4
    return found,len(parent)

def execute(word,path,wrong_sign=False):
    n=len(word);B,frozen=seed(word);X=list(s.symbols('X1:'+str(n+1)));w=list(word)
    recorded=[]
    for typ,p in path:
        if typ=='braid':
            assert p not in frozen
            X=mutate_X(X,B,p,wrong_sign)
            B=mutate_B(B,p,frozen)
            B,X,frozen=swap(B,X,frozen,p+1,p+2)
            a,b,c=w[p:p+3];w[p:p+3]=b,a,b
        else:
            B,X,frozen=swap(B,X,frozen,p,p+1)
            w[p],w[p+1]=w[p+1],w[p]
        # Independent reconstruction of target seed checks every mutation and
        # vertex relabelling, including frozen-vertex identity transport.
        assert (B,frozen)==seed(tuple(w)),(typ,p,w)
        recorded.append({'type':typ,'position_1based':p+1,'word':w.copy()})
    assert n-1 in frozen
    assert all(B[n-1][j]<=0 for j in range(n) if j not in frozen)
    return s.cancel(1/X[-1]),recorded

def laurent(expr,n):
    expr=s.cancel(expr); xs=s.symbols('X1:'+str(n+1))
    num,den=s.fraction(expr)
    pd=s.Poly(den,*xs)
    assert len(pd.terms())==1,('non-Laurent denominator',den)
    de,dc=pd.terms()[0]
    assert dc==1
    out=[]
    for e,c in s.Poly(num,*xs).terms():
        assert c>0 and c.is_Integer
        out.append({'coefficient':int(c),'exponents':[int(a-b) for a,b in zip(e,de)]})
    return sorted(out,key=lambda t:t['exponents'])

def reduced_check(word):
    C=s.Matrix([[2,-1,0,0],[-1,2,-1,-1],[0,-1,2,0],[0,-1,0,2]])
    Id=s.eye(4); mats=[]
    for i in range(4):
        M=Id.copy()
        for j in range(4): M[i,j]-=C[i,j]
        mats.append(M)
    g=Id.copy();roots=[]
    for a in word:
        beta=g*Id[:,a-1]
        assert all(x>=0 for x in beta) and any(x>0 for x in beta)
        roots.append(list(map(int,beta)));g=g*mats[a-1]
    assert g==-Id and len(set(map(tuple,roots)))==12
    return roots

def controls():
    # Rank-two control is published GKS Example5.3 after removing -I:
    # W2=X2^-1+X1^-1 X2^-1 for reduced word 121.
    B,F=seed((1,2,1));X=list(s.symbols('X1:4'))
    out=mutate_X(X,B,0)
    assert s.cancel(1/out[1]-(1+1/X[0])/X[1])==0
    bad=mutate_X(X,B,0,True)
    assert s.cancel(1/bad[1]-(1+1/X[0])/X[1])!=0
    # Full X-mutation involution, with changed matrix.
    T=mutate_X(out,mutate_B(B,0,F),0)
    assert all(s.cancel(a-b)==0 for a,b in zip(X,T))
    return {'A2_published_example':'passed','transposed_sign_rejected':'passed','X_mutation_involution':'passed'}

def main():
    roots=reduced_check(WORD);control=controls(); results={};checks=[]
    for reverse in (False,True):
        rs,seen=routes(WORD,reverse)
        for a,path in sorted(rs.items()):
            print('route',reverse,a,len(path),'moves',sum(t=='braid' for t,p in path),'mutations',flush=True)
            f,recorded=execute(WORD,path)
            support=laurent(f,len(WORD))
            if a in results: assert support==results[a]['support']
            else: results[a]={'expression':str(f),'support':support,'route':recorded}
            checks.append({'reverse_search':reverse,'letter':a,'moves':len(path),'mutations':sum(t=='braid' for t,p in path),'states_seen':seen})
    B,F=seed(WORD)
    report={'word':WORD,'root_sequence':roots,'matrix':B,'frozen_1based':sorted(i+1 for i in F),'controls':control,'route_checks':checks,'summands':results}
    allterms=[t for r in results.values() for t in r['support']]
    report['total_support_size']=len(allterms)
    report['max_abs_exponent']=max(abs(e) for t in allterms for e in t['exponents'])
    report['coefficient_set']=sorted({t['coefficient'] for t in allterms})
    path=HERE/'independent_output.json';path.write_text(json.dumps(report,indent=2)+'\n')
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    (HERE/'OUTPUT_DIGEST.txt').write_text('Current replay output SHA256 independent_output.json '+digest+'\nThis replay does not recreate historical review chronology.\n')
    print({k:report[k] for k in ('total_support_size','max_abs_exponent','coefficient_set')})
    print('summand sizes',{k:len(v['support']) for k,v in results.items()})
    print('output sha256',digest)

if __name__=='__main__':main()
