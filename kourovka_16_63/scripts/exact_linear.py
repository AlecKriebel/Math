#!/usr/bin/env python3
"""Deterministic sparse linear algebra over a prime field."""
from __future__ import annotations
from collections.abc import Iterable
from itertools import combinations
import json, time
from pathlib import Path
import numpy as np
from lie31 import D,MODS,NAMES,bracket_table,adapted_basis,bracket

def rank_sparse(rows:Iterable[dict[int,int]],p:int,return_basis=False):
    pivots={}; source_rows=[]; pivot_columns=[]
    max_support=0
    for row_index,row in enumerate(rows):
        row={int(j):int(a)%p for j,a in row.items() if int(a)%p}
        while row:
            j=min(row)
            if j not in pivots:
                inverse=pow(row[j],-1,p)
                row={k:a*inverse%p for k,a in row.items()}
                pivots[j]=row; source_rows.append(row_index); pivot_columns.append(j)
                max_support=max(max_support,len(row)); break
            scalar=row[j]
            for k,a in pivots[j].items():
                b=(row.get(k,0)-scalar*a)%p
                if b: row[k]=b
                else: row.pop(k,None)
    result={'rank':len(pivots),'source_rows':source_rows,'pivot_columns':pivot_columns,'maximum_pivot_support':max_support}
    if return_basis: result['basis']=pivots
    return result

def delta_rows(C):
    for i,j in combinations(range(D),2):
        for k in range(D):
            row={}
            def add(col,v):
                a=row.get(col,0)+int(v)
                if a: row[col]=a
                else: row.pop(col,None)
            for a in np.flatnonzero(C[i,j]): add(k*D+a,C[i,j,a])
            for a in np.flatnonzero(C[:,j,k]): add(a*D+i,-C[a,j,k])
            for a in np.flatnonzero(C[i,:,k]): add(a*D+j,-C[i,a,k])
            yield row

def row_vectors(A):
    for row in A:
        yield {int(j):int(row[j]) for j in np.flatnonzero(row)}

def Lie_generated(C,gens,p):
    """Iterative exact span closure with explicit bracket-generation witnesses."""
    basis={}; generators=[]; witnesses=[]
    def add(v,witness):
        v=np.array(v,dtype=np.int64)%p
        for j,b in sorted(basis.items()):
            if v[j]: v=(v-int(v[j])*b)%p
        nz=np.flatnonzero(v)
        if not len(nz): return False
        j=int(nz[0]); v=(v*pow(int(v[j]),-1,p))%p
        basis[j]=v; generators.append(v); witnesses.append(witness); return True
    for i,v in enumerate(gens): add(v,['input',i])
    cursor=0
    while cursor<len(generators):
        for j in range(cursor):
            add(bracket(C,generators[j],generators[cursor])%p,['bracket',j,cursor])
        cursor+=1
    return len(basis),generators,witnesses

def main():
    root=Path(__file__).resolve().parents[1]; C=bracket_table(); p=1009
    assert all(p%d for d in range(2,32))
    t=time.perf_counter()
    Mrows=list(delta_rows(C)); delta=rank_sparse(Mrows,p)
    perfect=rank_sparse(row_vectors(C.reshape(D*D,D)),p)
    # Columns represent x, rows encode [x,b_j]_k.
    centre=rank_sparse(({i:int(C[i,j,k]) for i in range(D) if C[i,j,k]}
                        for j in range(D) for k in range(D)),p)
    P,Pinv,weights,names=adapted_basis()
    generated,genvectors,witnesses=Lie_generated(C,[P[:,0],P[:,1]],p)
    # Derivations are inner once rank(delta)=31^2-30 and centre dimension=1.
    assert delta['rank']==931 and centre['rank']==30
    assert perfect['rank']==31 and generated==31
    # Infinitesimal flag stabilizer: [u,F2] in F2, [u,F3] in F3.
    constraints=[]
    for a,cut in [(0,2),(1,2),(2,3)]:
        matrix=np.column_stack([Pinv@bracket(C,np.eye(D,dtype=np.int64)[:,i],P[:,a]) for i in range(D)])
        constraints.extend(row_vectors(matrix[cut:]))
    stab=rank_sparse(constraints,p)
    assert stab['rank']==30 # only the central u remains; ad(u)=0.
    # Tangent dimension of Aut(A) modulo p^2 B: [u,F2] in F3.
    constraints2=[]
    for a in (0,1):
        matrix=np.column_stack([Pinv@bracket(C,np.eye(D,dtype=np.int64)[:,i],P[:,a]) for i in range(D)])
        constraints2.extend(row_vectors(matrix[3:]))
    stab2=rank_sparse(constraints2,p)
    k0=30-stab2['rank']
    # Extract and save a square nonzero minor for independent dense checking.
    rr=delta['source_rows']; cc=delta['pivot_columns']
    minor=np.array([[Mrows[i].get(j,0)%p for j in cc] for i in rr],dtype=np.int64)
    np.savetxt(root/'data/delta_rank_minor.txt',minor,fmt='%d',header=f'{len(rr)} {p}',comments='')
    (root/'data/delta_rank_certificate.json').write_text(json.dumps(delta,indent=2)+'\n')
    (root/'data/generator_closure_certificate.json').write_text(json.dumps({'prime':p,'basis':NAMES,'vectors':[v.tolist() for v in genvectors],'witnesses':witnesses},indent=2)+'\n')
    results={'prime':p,'dimension':D,'derived_dimension':perfect['rank'],'centre_dimension':D-centre['rank'],
        'derivation_matrix_shape':[D*D*(D-1)//2,D*D], 'derivation_matrix_rank':delta['rank'],
        'derivation_dimension':D*D-delta['rank'],'inner_derivation_dimension':centre['rank'],
        'Lie_subalgebra_generated_by_x_y_dimension':generated,
        'infinitesimal_flag_stabilizer_dimension':30-stab['rank'],
        'first_congruence_stabilizer_dimension':k0,
        'elapsed_seconds':time.perf_counter()-t,'algorithm':'deterministic sparse modular Gaussian elimination'}
    (root/'logs/lie31_linear.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
if __name__=='__main__': main()
