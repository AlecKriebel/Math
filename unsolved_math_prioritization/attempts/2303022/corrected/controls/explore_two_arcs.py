#!/usr/bin/env python3
"""Exploratory finite differences. NOT a continuum proof or certified error bound."""
import json, math, argparse
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

def solve(n, m, mode='two_arcs'):
    # x=-log |z|, theta=2pi j/m; x in [0, 8 log2].
    # Outer lower semicircle r=1/2 -> i=n, inner upper r=1/4 -> i=2n.
    nx=8*n; dx=math.log(2)/n; dt=2*math.pi/m
    ax=1/dx**2; at=1/dt**2
    fixed={(0,j):1. for j in range(m)}
    if mode=='two_arcs':
        for j in range(m//2+1): fixed[(2*n,j)]=0.
        for j in range(m//2,m): fixed[(n,j)]=0.
        fixed[(n,0)]=0.
    elif mode=='full_circle':
        for j in range(m):fixed[(n,j)]=0.
    elif mode!='empty': raise ValueError(mode)
    free=[(i,j) for i in range(1,nx+1) for j in range(m) if (i,j) not in fixed]
    ids={ij:k for k,ij in enumerate(free)}
    a=lil_matrix((len(free),len(free))); rhs=np.zeros(len(free))
    for ij,k in ids.items():
        i,j=ij
        if i==nx:
            # Reflecting inner boundary, not the exact infinite-cylinder DtN map.
            a[k,k]=2*ax+2*at; neigh=[((i-1,j),2*ax),((i,(j-1)%m),at),((i,(j+1)%m),at)]
        else:
            a[k,k]=2*ax+2*at;neigh=[((i-1,j),ax),((i+1,j),ax),((i,(j-1)%m),at),((i,(j+1)%m),at)]
        for p,c in neigh:
            if p in fixed:rhs[k]+=c*fixed[p]
            else:a[k,ids[p]]-=c
    a=a.tocsr();u=spsolve(a,rhs)
    v=np.array([u[ids[(nx,j)]] for j in range(m)])
    return {'n':n,'m':m,'mode':mode,'unknowns':len(free),'q_fd':float(v.mean()),'inner_angle_spread':float(v.max()-v.min()),'relative_residual_inf':float(np.max(np.abs(a@u-rhs))/max(1,np.max(np.abs(rhs))))}

if __name__=='__main__':
    out={'limitation':'Floating-point finite-difference model with inner reflecting truncation; no continuum error bound; not a candidate solution.','results':[]}
    for n,m in [(8,64),(16,128),(32,256)]:out['results'].append(solve(n,m))
    out['results'].append(solve(8,64,'empty'));out['results'].append(solve(8,64,'full_circle'))
    assert abs(out['results'][-2]['q_fd']-1)<1e-9
    assert abs(out['results'][-1]['q_fd'])<1e-9
    assert all(0<=x['q_fd']<=1+1e-9 for x in out['results'])
    print(json.dumps(out,indent=2))
