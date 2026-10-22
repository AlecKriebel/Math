#!/usr/bin/env python3
"""Independent exact audit; never imports the author's implementation.

Uses exhaustive labelled spanning supports, BFS connectivity, column-major
Kronecker-product endomorphism equations, and the trace pairing on the faithful
representation (rather than the author's regular representation).
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import time
import sympy as sp
from sympy.polys.matrices import DomainMatrix


def positions(d, arrows):
    return [(a, r, c) for a,(u,v) in enumerate(arrows) for c in range(d[u]) for r in range(d[v])]


def connected(d, arrows, edges):
    offsets=[sum(d[:i]) for i in range(len(d))]
    adj=[[] for _ in range(sum(d))]
    for a,r,c in edges:
        u,v=arrows[a]; x,y=offsets[u]+c,offsets[v]+r
        adj[x].append(y);adj[y].append(x)
    seen={0};todo=[0]
    while todo:
        for v in adj[todo.pop()]:
            if v not in seen:seen.add(v);todo.append(v)
    return len(seen)==sum(d)


def matrices(d, arrows, edges):
    out=[sp.zeros(d[v],d[u]) for u,v in arrows]
    for a,r,c in edges:out[a][r,c]=1
    return out


def null_basis(m):
    # DomainMatrix uses exact rational arithmetic; rows of the returned matrix
    # span the nullspace. Unlike the author's Matrix.nullspace algorithm, no
    # normalization of free coordinates is needed for the trace test.
    return DomainMatrix.from_Matrix(m).to_field().nullspace().to_Matrix().T


def analyze(d, arrows, mats):
    sizes=[n*n for n in d]; starts=[sum(sizes[:i]) for i in range(len(d))]
    nv=sum(sizes)
    eq=sp.zeros(sum(d[u]*d[v] for u,v in arrows), nv)
    k=0
    for (u,v),A in zip(arrows,mats):
        n=d[u]*d[v]
        eq[k:k+n,starts[v]:starts[v]+sizes[v]]=sp.kronecker_product(A.T,sp.eye(d[v]))
        eq[k:k+n,starts[u]:starts[u]+sizes[u]]-=sp.kronecker_product(sp.eye(d[u]),A)
        k+=n
    B=null_basis(eq)
    # In column-vectorization, trace(XY)=vec(X)^T vec(Y^T).
    flip=[]
    for n,start in zip(d,starts):
        flip.extend(start+c+n*r for c in range(n) for r in range(n))
    T=B.T*B[flip,:]
    r=DomainMatrix.from_Matrix(T).rank()
    return B.cols,r,B


def enumerate_case(d, arrows):
    counts=Counter(); num=0; indecomp_edges=[]
    for edges in combinations(positions(d,arrows),sum(d)-1):
        if not connected(d,arrows,edges):continue
        num+=1
        h,r,B=analyze(d,arrows,matrices(d,arrows,edges))
        counts[f'{h},{r}']+=1
        if r==1:indecomp_edges.append(edges)
    return {'dimensions':d,'arrows':arrows,'tree_supports':num,
            'endomorphism_dimension_faithful_trace_rank_histogram':dict(sorted(counts.items())),
            'indecomposable_supports':len(indecomp_edges),
            'decomposable_supports':num-len(indecomp_edges)},indecomp_edges


def explicit_affine():
    d=[3,2,2,1,1];arrows=[(1,0),(2,0),(3,0),(4,0)]
    A=[sp.Matrix([[1,0],[1,0],[0,1]]),sp.Matrix([[1,0],[0,0],[0,1]]),sp.Matrix([0,1,1]),sp.Matrix([0,1,0])]
    h,r,B=analyze(d,arrows,A)
    # Construct the expected nonzero nilpotent at every vertex independently.
    N=[sp.zeros(3),sp.zeros(2),sp.zeros(2),sp.zeros(1),sp.zeros(1)]
    N[0][2,0]=1;N[1][1,0]=1;N[2][1,0]=1
    assert all(N[v]*a==a*N[u] for (u,v),a in zip(arrows,A))
    assert all(n*n==sp.zeros(n.rows) for n in N)
    expected=sp.Matrix.hstack(sp.Matrix([x for n in d for x in sp.eye(n)]),sp.Matrix([x for n in N for x in n.T]))
    assert expected.rank()==h==2
    # Reflection sequence uses leaf numbering 1,2, then center 0, then 1..4.
    seq=[d[:]]; current=d[:]
    for v in [1,2,0,1,2,3,4]:
        current=current[:]
        current[v]=(sum(current[1:]) if v==0 else current[0])-current[v]
        seq.append(current)
    assert current==[1,0,0,0,0]
    return {'endomorphism_dimension':h,'faithful_trace_rank':r,
            'N_vertex_blocks':[list(m) for m in N], 'N_squared_zero':True,
            'root_reflection_sequence':seq,
            'quadratic_form':sum(x*x for x in d)-d[0]*sum(d[1:])}


def independent_pencil(d,arrows,edges):
    A,B=matrices(d,arrows,edges)
    detpoly=sp.Poly((A+sp.Symbol('t')*B).det(),sp.Symbol('t'))
    assert not detpoly.is_zero
    invertible=next(A+t*B for t in (0,1,2) if (A+t*B).det()!=0)
    C=invertible.inv()*B
    scalar=C==C[0,0]*sp.eye(2)
    return not scalar and sp.trace(C)**2==4*C.det()


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--skip-affine',action='store_true');args=p.parse_args()
    results={'implementation':'BFS and column-major Kronecker equations; faithful trace form; every labelled support tested, no orbit quotient','sympy_version':sp.__version__,'cases':{},'explicit_affine_D4':explicit_affine()}
    cases=[('K2_2_2',[2,2],[(0,1),(0,1)]),('D4_2_1_1_1',[2,1,1,1],[(1,0),(2,0),(3,0)]),('A2_2_1_nonroot',[2,1],[(0,1)])]
    if not args.skip_affine:cases.append(('affine_D4_3_2_2_1_1',[3,2,2,1,1],[(1,0),(2,0),(3,0),(4,0)]))
    for name,d,arrows in cases:
        t=time.monotonic();result,edges=enumerate_case(d,arrows);results['cases'][name]=result
        print(name,result, 'seconds',round(time.monotonic()-t,2),flush=True)
        if name=='K2_2_2':
            independent=Counter(independent_pencil(d,arrows,es) for es in combinations(positions(d,arrows),3) if connected(d,arrows,es))
            assert independent=={True:8,False:24}
            results['kronecker_pencil']={str(k):v for k,v in independent.items()}
        args.output.write_text(json.dumps(results,indent=2,default=int)+'\n')
    # Simple, matrix, local and nonlocal algebras; source-author code not used.
    controls={}
    for name,d,arr,mat in [
        ('one_vertex_simple',[1],[],[]),('one_vertex_double',[2],[],[]),
        ('connected_decomposable',[2,2],[(0,1),(0,1)],[sp.Matrix([[1,1],[1,0]]),sp.zeros(2)]),
        ('degeneration_nonzero',[2,2],[(0,1),(0,1)],[sp.eye(2),sp.Matrix([[0,2],[0,0]])]),
        ('degeneration_zero',[2,2],[(0,1),(0,1)],[sp.eye(2),sp.zeros(2)])]:
        h,r,_=analyze(d,arr,mat);controls[name]={'endomorphism_dimension':h,'faithful_trace_rank':r,'indecomposable':r==1}
    results['controls']=controls
    args.output.write_text(json.dumps(results,indent=2,default=int)+'\n')

if __name__=='__main__':main()
