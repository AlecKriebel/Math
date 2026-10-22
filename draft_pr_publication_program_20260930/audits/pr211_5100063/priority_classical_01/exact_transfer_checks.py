#!/usr/bin/env python3
"""Fresh finite transfer checks; standard library only; no historical helpers.

Arithmetic is exact in Q(sqrt(5),sqrt(21)). These two triangle phases are
checks of proposed reductions, not evidence for an all-period theorem.
"""
from fractions import Fraction as F
from pathlib import Path
import json


class K:
    def __init__(self, a=0):
        self.v = tuple(map(F, a)) if isinstance(a, (tuple, list)) else (F(a), F(0), F(0), F(0))
    def __add__(self, o):
        o = cv(o)
        return K(tuple(a+b for a,b in zip(self.v,o.v)))
    __radd__ = __add__
    def __neg__(self): return K(tuple(-a for a in self.v))
    def __sub__(self,o): return self+-cv(o)
    def __rsub__(self,o): return cv(o)+-self
    def __mul__(self,o):
        o=cv(o); z=[F(0)]*4
        for i,a in enumerate(self.v):
            for j,b in enumerate(o.v):
                common=i&j
                z[i^j]+=a*b*(5 if common&1 else 1)*(21 if common&2 else 1)
        return K(z)
    __rmul__=__mul__
    def conj(self,bits):
        return K(tuple((-a if (i&bits).bit_count()%2 else a) for i,a in enumerate(self.v)))
    def inv(self):
        y=self.conj(1)*self.conj(2)*self.conj(3)
        norm=self*y
        assert norm.v[1:]==(F(0),F(0),F(0)) and norm.v[0]
        return K(tuple(a/norm.v[0] for a in y.v))
    def __truediv__(self,o): return self*cv(o).inv()
    def __rtruediv__(self,o): return cv(o)*self.inv()
    def __eq__(self,o): return self.v==cv(o).v
    def out(self): return [str(a) for a in self.v]


def cv(x): return x if isinstance(x,K) else K(x)
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def area(p): return sum(det(x,y) for x,y in zip(p,p[1:]+p[:1]))/2
def focal_inverse(p, f):
    z=sub(p,f); den=dot(z,z)
    return tuple(x+y/den for x,y in zip(f,z))
def tangent_outer(p,a2,b2):
    out=[]
    for x,y in zip(p,p[1:]+p[:1]):
        n=(x[0]/a2,x[1]/b2); m=(y[0]/a2,y[1]/b2)
        den=det(n,m)
        out.append(((m[1]-n[1])/den,(n[0]-m[0])/den))
    return out


def main():
    r5=K((0,1,0,0)); r21=K((0,0,1,0))
    a2,b2=K(21),K(16); alpha2,beta2=K(F(189,25)),K(F(64,25))
    assert a2-b2==alpha2-beta2==5
    phases=[[(K(0),K(4)),(K(F(-21,5)),K(F(-8,5))),(K(F(21,5)),K(F(-8,5)))],
            [(-r21,K(0)),(3*r21/5,K(F(-16,5))),(3*r21/5,K(F(16,5)))]]
    records=[]
    for p in phases:
        assert all(x*x/a2+y*y/b2==1 for x,y in p)
        for x,y in zip(p,p[1:]+p[:1]):
            edge=sub(y,x); n=(edge[1],-edge[0]); h=dot(n,x)
            assert n[0]*n[0]*alpha2+n[1]*n[1]*beta2==h*h
        q=tangent_outer(p,a2,b2)
        assert all(x*x/K(F(175,3))+y*y/100==1 for x,y in q)
        bp,bm=[area([focal_inverse(x,f) for x in q]) for f in [(r5,K(0)),(-r5,K(0))]]
        pp,pm=[area([focal_inverse(x,f) for x in p]) for f in [(r5,K(0)),(-r5,K(0))]]
        records.append(dict(P=[list(map(lambda z:z.out(),x)) for x in p],
                            Q=[list(map(lambda z:z.out(),x)) for x in q],
                            area_P=area(p).out(),area_Q=area(q).out(),
                            area_ratio=(area(q)/area(p)).out(),
                            untransformed_product=(area(p)*area(q)).out(),
                            inverse_outer_plus=bp.out(),inverse_outer_minus=bm.out(),
                            inverse_outer_product=(bp*bm).out(),
                            inverse_original_plus=pp.out(),inverse_original_minus=pm.out(),
                            outer_to_original_inverse_ratio_plus=(bp/pp).out(),
                            outer_to_original_inverse_ratio_minus=(bm/pm).out(),
                            inverse_original_product=(pp*pm).out()))
        assert area(q)/area(p)==F(25,6)
        assert bp*bm==F(1,3600)
        assert pp*pm==F(1,324)
    assert records[0]['untransformed_product']!=records[1]['untransformed_product']
    # An affine map sending P to Q does not intertwine ordinary inversions.
    # Evaluate z=(0,4), S=diag(5/3,5/2), f=(sqrt5,0).
    z=(K(0),K(4)); f=(r5,K(0)); spre=(3*r5/5,K(0))
    sz=(5*z[0]/3,5*z[1]/2)
    lhs=sub(focal_inverse(sz,f),f)
    iz=sub(focal_inverse(z,spre),spre)
    rhs=(5*iz[0]/3,5*iz[1]/2)
    assert lhs!=rhs
    result=dict(schema='pr211-fresh-classical-transfer-finite-check-v1',
                exact_field_basis=['1','sqrt(5)','sqrt(21)','sqrt(105)'],
                method='Fraction arithmetic in a biquadratic number field; ellipse/tangency/tangent-intersection checks',
                triangle_least_period=3,
                repeated_odd_orbit_does_not_acquire_antipodal_pairing=True,
                ordinary_affine_inversion_intertwining_false=True,
                two_phases=records,
                scope='Two exact phases falsify parity-doubling and naive affine-inversion transfers. No universal novelty or theorem check.')
    Path(__file__).with_name('EXACT_TRANSFER_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
