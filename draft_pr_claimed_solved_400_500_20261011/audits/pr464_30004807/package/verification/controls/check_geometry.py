#!/usr/bin/env python3
"""Independent bounded exact geometry controls; no frozen checker imports.

Python standard library only. Assertions are intentionally not used. The report
contains the all-parameter deductions; this finite rational replay is corroboration.
"""
from fractions import Fraction as F
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class Jet:
    v: F
    d: F = F(0)
    dd: F = F(0)
    def __add__(self, b):
        b = b if isinstance(b, Jet) else Jet(F(b))
        return Jet(self.v+b.v, self.d+b.d, self.dd+b.dd)
    __radd__ = __add__
    def __neg__(self): return Jet(-self.v, -self.d, -self.dd)
    def __sub__(self, b): return self + (-b if isinstance(b, Jet) else -F(b))
    def __rsub__(self, b): return -self + b
    def __mul__(self, b):
        b = b if isinstance(b, Jet) else Jet(F(b))
        return Jet(self.v*b.v, self.d*b.v+self.v*b.d,
                   self.dd*b.v+2*self.d*b.d+self.v*b.dd)
    __rmul__ = __mul__
    def inv(self):
        return Jet(1/self.v, -self.d/self.v**2,
                   2*self.d**2/self.v**3-self.dd/self.v**2)
    def __truediv__(self, b):
        b = b if isinstance(b, Jet) else Jet(F(b))
        return self*b.inv()
    def __rtruediv__(self, b): return Jet(F(b))*self.inv()
    def __pow__(self, n):
        if n < 0: return self.inv()**(-n)
        r = Jet(F(1))
        for _ in range(n): r=r*self
        return r

count = 0
cases = 0
families = {}
def check(name, left, right=True):
    global count
    if left != right:
        raise ValueError(f'{name}: {left!r} != {right!r}')
    count += 1
    families[name] = families.get(name, 0)+1

for a in map(F, [F(1,2), 1, 3]):
    for offset in map(F, [F(1,100), F(1,7), F(1,2), 1, 2, 11]):
        x = Jet(a+offset,F(1))
        p = 1-a/x
        nv = (x+a)/(x-a)
        r = x*p**2
        rr = -2*p.dd/p.v+4*p.d**2/p.v**2
        rt = -2*p.d/(x.v*p.v)-2*p.d**2/p.v**2
        mr = rr/p.v**4
        mt = rt/p.v**4
        check('radial_Ricci_eigenvalue', mr,4*a/(x.v**3*p.v**6))
        check('angular_Ricci_eigenvalue', mt,-2*a/(x.v**3*p.v**6))
        check('scalar_flat',mr+2*mt,F(0))
        hv_r = nv.dd-2*p.d*nv.d/p.v
        hv_t = (1/x.v+2*p.d/p.v)*nv.d
        check('vacuum_Hessian_radial',hv_r,nv.v*rr)
        check('vacuum_Hessian_angular',hv_t,nv.v*rt)
        check('vacuum_Laplacian',hv_r+2*hv_t,F(0))
        check('area_radius_derivative',r.d,(x.v**2-a*a)/x.v**2)
        check('spatial_Schwarzschild_radial',r.d**2/(1+4*a/r.v),p.v**4)
        n = p**(-1)
        check('half_vacuum_lapse',n.v,(1+nv.v)/2)
        check('counterexample_radial_G',mr/(2*n.v),2*a/(x.v**3*p.v**5))
        gr = mr/(2*n.v)
        gt = mt/(2*n.v)
        check('connection_cancellation',2*p.d/p.v*(gr+2*gt),F(0))
        check('nonzero_density_radial',n.v*p.v**6*gr*x.v**2,2*a/x.v)
        check('angular_density_contribution',n.v*p.v**6*2*gt*x.v,-2*a/x.v**2)
        check('angular_NEC_failure',gt<0)
        dr = 2*a/x**3
        dt = -a/x**3
        check('density_Euclidean_divergence',dr.d+2*(dr.v-dt.v)/x.v,F(0))
        check('regular_factor_positive',p.v>0)
        check('null_affine_density_positive',p.v>0)
        for q in [F(-3,4),F(0),F(1,2),F(99,100)]:
            check('uniformly_spacelike_tilt',1-q*q>0)
        check('near_null_spacelike_radial',p.v**6>0)
        cases += 1
print(json.dumps({'verdict':'PASS','exact_check_count':count,
                  'rational_parameter_case_count':cases,'check_families':families,
                  'finite_controls_only':True,
                  'uses_frozen_checkers':False},indent=2,sort_keys=True))
