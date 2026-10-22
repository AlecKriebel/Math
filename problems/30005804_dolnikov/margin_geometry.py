"""Exact normalization and constructive margin theorem."""
from row_geometry import *
from itertools import product


def normalize(K):
    D = difference(K)
    delta,u,v = max((cross(u,v),u,v) for u,v in product(D,D))
    assert delta > 0
    def forward(p):
        return (cross(p,v)/delta, cross(u,p)/delta)
    def backward(p):
        return (p[0]*u[0]+p[1]*v[0],p[0]*u[1]+p[1]*v[1])
    N = hull(list(map(forward,K)))
    ND = difference(N)
    assert all(abs(x)<=1 and abs(y)<=1 for x,y in ND)
    assert all(inside(pt(p),ND) for p in [(1,0),(0,1),(-1,0),(0,-1)])
    return N,forward,backward,(u,v)


def rectangle(N,lam):
    L = hull([(-x,-y) for x,y in N])
    ell,cy,cx = longest_horizontal(L)
    swapped = hull([(y,x) for x,y in L])
    height,ix,iy = longest_horizontal(swapped)
    assert ell==height==1
    lower = (lam*cx+(1-lam)*ix, lam*cy+(1-lam)*iy)
    P = [(lower[0]+dx,lower[1]+dy) for dx,dy in
         [(0,0),(lam,0),(lam,1-lam),(0,1-lam)]]
    assert all(inside(p,L) for p in P)
    return lower,P


def margin_piercing(K,colors,lam):
    assert len(colors)==3 and 0<lam<=F(3,4)
    N,f,g,basis = normalize(K)
    transformed = [list(map(f,A)) for A in colors]
    ND = difference(N)
    assert all(inside((sub(a,b)[0]/lam,sub(a,b)[1]/lam),ND)
               for i in range(3) for j in range(i)
               for a in transformed[i] for b in transformed[j])
    candidates = [i for i,A in enumerate(transformed)
                  if row_span([x for x,y in A])<=lam
                  and row_span([y for x,y in A])<=lam]
    assert candidates
    i = candidates[0]; A = transformed[i]
    lower,P = rectangle(N,lam)
    x0=min(x for x,y in A); y0=min(y for x,y in A)
    Q = [g((x0-lower[0],y0+j*(1-lam)-lower[1])) for j in range(3)]
    return i,Q,basis
