#!/usr/bin/env python3
"""Blind canonical GHKK reconstruction. Python stdlib + SymPy 1.14.

Coordinates are chronological positions, one based in JSON. b[u][v]>0
means u -> v. Only the last occurrence of each letter is frozen.
KS2022 eq (3): X'_i = X_i(1+X_k^(-sign b_ik))^(-b_ik).
All exact computations are over Q; no numerical tolerances occur.
"""
import collections
import hashlib
import json
import pathlib
import sys
import sympy as s

BASE = pathlib.Path(__file__).resolve().parent
WORD = (1,2,3,2,4,2,1,2,3,2,4,2)
EDGES = {frozenset((1,2)),frozenset((2,3)),frozenset((2,4))}

def adjacent(a,b,edges=EDGES): return frozenset((a,b)) in edges

def seed(w,edges=EDGES):
    n=len(w)
    nxt=[next((j for j in range(k+1,n) if w[j]==w[k]),n) for k in range(n)]
    frozen={k for k in range(n) if nxt[k]==n}
    b=[[0]*n for _ in w]
    for k in range(n):
        for l in range(k+1,n):
            if k in frozen and l in frozen: continue
            v=1 if l==nxt[k] else (-1 if l<nxt[k]<nxt[l] and adjacent(w[k],w[l],edges) else 0)
            b[k][l]=v; b[l][k]=-v
    return b,frozen,nxt

def mutate(b,k,frozen):
    assert k not in frozen
    n=len(b)
    out=[[0]*n for _ in b]
    for i in range(n):
        for j in range(n):
            if i in frozen and j in frozen: continue
            out[i][j]=(-b[i][j] if k in (i,j) else
                b[i][j]+max(b[i][k],0)*max(b[k][j],0)-max(-b[i][k],0)*max(-b[k][j],0))
    return out

def moves(w,edges=EDGES):
    n=len(w)
    for t in range(n-1):
        if w[t]!=w[t+1] and not adjacent(w[t],w[t+1],edges):
            v=list(w); v[t],v[t+1]=v[t+1],v[t]
            yield tuple(v),('commute',t)
    for t in range(n-2):
        if w[t]==w[t+2] and adjacent(w[t],w[t+1],edges):
            v=list(w); v[t:t+3]=[w[t+1],w[t],w[t+1]]
            yield tuple(v),('braid',t)

def transport(w,v,m,edges=EDGES):
    b,f,_=seed(w,edges); c,g,_=seed(v,edges)
    kind,t=m; p=list(range(len(w)))
    if kind=='braid':
        b=mutate(b,t,f); p[t+1],p[t+2]=p[t+2],p[t+1]
    else: p[t],p[t+1]=p[t+1],p[t]
    assert [[b[p[i]][p[j]] for j in range(len(w))] for i in range(len(w))]==c,(w,v,m,'quiver')
    assert {i for i in range(len(w)) if p[i] in f}==g,(w,v,m,'frozen')
    return p

def route_graph(w,edges=EDGES):
    """0-1 BFS minimizes actual cluster mutations, with deterministic ties."""
    q=collections.deque([w]); distances={w:0}; parent={w:None}
    while q:
        u=q.popleft()
        for v,m in moves(u,edges):
            transport(u,v,m,edges)
            cost=int(m[0]=='braid'); d=distances[u]+cost
            if v not in distances or d<distances[v]:
                distances[v]=d; parent[v]=(u,m)
                (q.append if cost else q.appendleft)(v)
    routes={}
    for a in sorted(set(w)):
        target=min((u for u in distances if u[-1]==a),key=lambda u:(distances[u],u))
        rev=[]; v=target
        while parent[v] is not None:
            u,m=parent[v]; rev.append((u,v,m)); v=u
        routes[a]=list(reversed(rev))
    return routes,distances

def pullback(route,edges=EDGES):
    n=len(route[0][0]) if route else len(WORD)
    z=s.symbols('X1:'+str(n+1))
    out=1/z[-1]
    for w,v,m in reversed(route):
        p=transport(w,v,m,edges)
        b,f,_=seed(w,edges); kind,t=m
        repl=list(z)
        if kind=='braid':
            for i in range(n):
                v=b[i][t]
                repl[i]=(1/z[t] if i==t else
                    z[i]*(1+z[t]**(-s.sign(v)))**(-v))
        out=s.cancel(out.xreplace({z[i]:repl[p[i]] for i in range(n)}))
    return s.expand(out),z

def laurent_terms(expr,z):
    result=[]
    for term in s.Add.make_args(s.expand(expr)):
        powers=term.as_powers_dict()
        exp=tuple(int(powers.get(x,0)) for x in z)
        coefficient=s.cancel(term/s.prod(x**e for x,e in zip(z,exp)))
        assert coefficient.is_Integer and coefficient>0,(term,coefficient)
        result.append({'coefficient':int(coefficient),'exponents':list(exp)})
    return sorted(result,key=lambda t:t['exponents'])

def roots(w):
    C=s.Matrix([[2 if a==b else (-1 if adjacent(a,b) else 0) for b in range(1,5)] for a in range(1,5)])
    I=s.eye(4); refl=[]
    for a in range(4):
        S=I.copy()
        for j in range(4): S[a,j]-=C[a,j]
        refl.append(S)
    action=I; beta=[]
    for a in w:
        b=action[:,a-1]; assert all(e>=0 for e in b) and any(e>0 for e in b)
        beta.append(list(b)); action=action*refl[a-1]
    assert action==-I and len({tuple(b) for b in beta})==12
    return C,beta,action

def chamber(w,C):
    b,f,nxt=seed(w); n=len(w)
    M=s.zeros(n)
    for k in range(n):
        for l in range(k,n):
            if l in (k,nxt[k]): M[k,l]=-C[w[k]-1,w[l]-1]/2
            elif k<l<nxt[k]: M[k,l]=-C[w[k]-1,w[l]-1]
    assert M.det()==1 # 12 diagonal entries equal -1
    return M

def main():
    # Small source-normalization example. Chronological KS2022 seed.
    a2=(1,2,1); edges2={frozenset((1,2))}
    routes2,d2=route_graph(a2,edges2)
    p2,z2=pullback(routes2[2],edges2)
    assert s.cancel(p2-(1+1/z2[0])/z2[1])==0
    assert seed(a2,edges2)[0]==[[0,-1,1],[1,0,0],[-1,0,0]]
    C,beta,action=roots(WORD)
    routes,dist=route_graph(WORD)
    M=chamber(WORD,C)
    b,f,nxt=seed(WORD)
    answer={'schema':'blind-canonical-GHKK-v1','input':{'word':WORD,'edges':[[1,2],[2,3],[2,4]]},
      'coordinate_order':'X1,...,X12 = chronological reduced-word positions',
      'conventions':{'b_positive':'arrow from row to column','X_mutation':'Xprime_i=Xi*(1+Xk^(-sign(b_ik)))^(-b_ik); Xprime_k=1/Xk',
        'optimized':'all mutable arrows adjacent to frozen vertex enter it','frozen_normalization':'W_a=1/X_last_a in an optimized seed'},
      'seed':{'matrix':b,'frozen_positions':[k+1 for k in sorted(f)],'successors':[j+1 for j in nxt]},
      'root_validation':{'cartan':list(map(list,C.tolist())),'ordered_positive_roots':beta,'w0_matrix':action.tolist()},
      'braid_graph':{'vertices':len(dist),'directed_edges':sum(1 for u in dist for _ in moves(u)),
         'every_edge_quiver_and_frozen_transport_checked':True},
      'chamber_ansatz_exponent_matrix':M.tolist(),'summands':{},
      'blindness':{'input_seen':'Only root instruction naming G, Dynkin edges, word and source references; no candidate term count or result',
         'candidate_seen':False,'prior_reviews_seen':False,'parent_artifacts_seen':False}}
    for a,route in routes.items():
        if route:
            target=route[-1][1]
        else: target=WORD
        bt,ft,_=seed(target)
        assert len(target)-1 in ft
        assert all(bt[len(target)-1][j]<=0 for j in range(len(target)) if j not in ft)
        poly,z=pullback(route)
        terms=laurent_terms(poly,z)
        assert all(all(e<=0 for e in t['exponents']) for t in terms)
        pulled=[]
        for t in terms:
            pulled.append({'coefficient':t['coefficient'],'exponents':list((s.Matrix(1,12,t['exponents'])*M))})
        answer['summands'][str(a)]={'target_word':target,'mutation_count':sum(m[0]=='braid' for _,_,m in route),
          'route':[{'kind':m[0],'start_position':m[1]+1,'source_word':u,'target_word':v} for u,v,m in route],
          'canonical_X_support':terms,'chamber_pullback_support':sorted(pulled,key=lambda t:t['exponents'])}
    # Replays compare exact content, without altering the historical freeze.
    frozen=(BASE/'blind_frozen.json').read_bytes()
    reference=json.loads(frozen)
    assert json.loads(json.dumps(answer,default=int))==reference
    digest=hashlib.sha256(frozen).hexdigest()
    assert digest=='7881d1d0ef80ff7ca036f16a06d2d7f23cb666bab223500226d6cded3f66a30d'
    print(json.dumps({'frozen_sha256':digest,'comparison':'exact match; freeze untouched','graph_vertices':len(dist),'summands':{a:{'terms':len(v['canonical_X_support']),
         'coefficient_counts':dict(collections.Counter(t['coefficient'] for t in v['canonical_X_support'])),
         'mutation_count':v['mutation_count']} for a,v in answer['summands'].items()}},indent=2))

if __name__=='__main__': main()
