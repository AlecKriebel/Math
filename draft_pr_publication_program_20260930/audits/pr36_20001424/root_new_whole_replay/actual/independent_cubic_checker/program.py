#!/usr/bin/env python3
"""Old-source consequence checks, using exact Q(i) arithmetic only.

No numerical orbit evidence is used. Controls deliberately break parity or
phase assumptions; they are tests of this proof and are not new candidates.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import comb
import json
from pathlib import Path

@dataclass(frozen=True)
class Qi:
    re: F = F(0)
    im: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))
    def __add__(self, other):
        o = qi(other); return Qi(self.re+o.re, self.im+o.im)
    __radd__ = __add__
    def __neg__(self): return Qi(-self.re, -self.im)
    def __sub__(self, other): return self + -qi(other)
    def __rsub__(self, other): return qi(other) + -self
    def __mul__(self, other):
        o = qi(other)
        return Qi(self.re*o.re-self.im*o.im, self.re*o.im+self.im*o.re)
    __rmul__ = __mul__
    def __truediv__(self, other):
        o = qi(other); n = o.re**2+o.im**2
        if not n: raise ZeroDivisionError
        return self * Qi(o.re/n, -o.im/n)
    def __pow__(self, n):
        if n < 0: return (ONE/self)**(-n)
        v=ONE
        for _ in range(n): v=v*self
        return v
    def conj(self): return Qi(self.re, -self.im)
    def label(self):
        if not self.im: return str(self.re)
        if not self.re: return f'{self.im}i'
        return f'({self.re}+{self.im}i)'

def qi(v): return v if isinstance(v, Qi) else Qi(v)
ZERO=Qi(); ONE=Qi(1); I=Qi(0,1)
def trim(p):
    p=list(map(qi,p))
    while len(p)>1 and p[-1]==ZERO: p.pop()
    return p
def add(p,q):
    return trim([(p[j] if j<len(p) else ZERO)+(q[j] if j<len(q) else ZERO)
                 for j in range(max(len(p),len(q)))])
def scale(p,a): return trim([x*a for x in p])
def mul(p,q):
    r=[ZERO]*(len(p)+len(q)-1)
    for j,a in enumerate(p):
        for k,b in enumerate(q): r[j+k]=r[j+k]+a*b
    return trim(r)
def power(p,n):
    r=[ONE]
    for _ in range(n): r=mul(r,p)
    return r
def deriv(p): return trim([j*p[j] for j in range(1,len(p))] or [ZERO])
def cross(a,b): return add(mul(a[0],b[1]),scale(mul(a[1],b[0]),-1))
def equal_maps(a,b): return cross(a,b)==[ZERO]
def phi_polys(d,c=I): return [scale(power([Qi(-1),ONE],d),c),power([ONE,ONE],d)]
def fg_polys(d,c=I): # F composed with g(z)=-1/z, homogeneous substitution
    return [scale(power([Qi(-1),Qi(-1)],d),c),power([Qi(-1),ONE],d)]
def g_after(pair): return [scale(pair[1],-1),pair[0]]
def bar(pair): return [[x.conj() for x in p] for p in pair]
def projective_equal(a,b): return a[0]*b[1]==b[0]*a[1]
def normalize(a):
    if a[1]==ZERO:
        assert a[0]!=ZERO; return (ONE,ZERO)
    return (a[0]/a[1],ONE)
def point_label(p): return 'infinity' if p[1]==ZERO else (p[0]/p[1]).label()
def phi_point(p,d,c=I):
    x,y=p
    return normalize((c*(x-y)**d,(x+y)**d))
def orbit(start,d,c=I,limit=16):
    values=[normalize(start)]
    for _ in range(limit):
        nxt=phi_point(values[-1],d,c)
        for j,old in enumerate(values):
            if projective_equal(nxt,old):
                return {'points':[point_label(p) for p in values],
                        'repeat_index':j,'repeat':point_label(nxt)}
        values.append(nxt)
    raise AssertionError('Orbit exceeded exact control bound')

def check(d,c=I):
    phi=phi_polys(d,c); fg=fg_polys(d,c)
    wronskian=add(mul(deriv(phi[0]),phi[1]),scale(mul(phi[0],deriv(phi[1])),-1))
    expected=scale(mul(power([Qi(-1),ONE],d-1),power([ONE,ONE],d-1)),2*d*c)
    assert wronskian==expected
    # Reverse coefficients are the local representative at infinity.
    p_rev=list(reversed(phi[0])); q_rev=list(reversed(phi[1]))
    infinity_local_derivative=(deriv(p_rev)[0]*q_rev[0]-p_rev[0]*deriv(q_rev)[0])/(q_rev[0]**2)
    assert infinity_local_derivative==-2*d*c
    conjugacy=equal_maps(g_after(fg),bar(phi))
    holomorphic_g=equal_maps(fg,g_after(phi))
    antipodal_J=equal_maps(fg,g_after(bar(phi)))
    return {
        'd':d, 'phase':c.label(), 'degree_ge_2':d>=2,
        'critical_wronskian_identity':True,
        'critical_multiplicities':{'1':d-1,'-1':d-1},
        'infinity_local_derivative':infinity_local_derivative.label(),
        'orbit_1':orbit((ONE,ONE),d,c),
        'orbit_minus1':orbit((Qi(-1),ONE),d,c),
        'g_conjugates_phi_to_coefficient_conjugate':conjugacy,
        'g_holomorphically_commutes':holomorphic_g,
        'J_antiholomorphically_commutes':antipodal_J,
        'holomorphic_g_residual_low_to_high':[x.label() for x in cross(fg,g_after(phi))]
    }

def main():
    main_cases=[check(d) for d in (3,5,7,9)]
    for r in main_cases:
        assert r['g_conjugates_phi_to_coefficient_conjugate']
        assert not r['g_holomorphically_commutes']
        assert r['J_antiholomorphically_commutes']
        assert r['orbit_1']['repeat_index']==0
        assert r['orbit_minus1']['repeat_index']==0
    r=main_cases[0]
    assert r['orbit_1']['points']==['1','0','-1i','-1','infinity','1i']
    assert r['orbit_minus1']['points']==['-1','infinity','1i','1','0','-1i']
    even=check(2)
    assert not even['g_conjugates_phi_to_coefficient_conjugate']
    assert even['g_holomorphically_commutes']
    assert not even['J_antiholomorphically_commutes']
    degree_one=check(1)
    assert not degree_one['degree_ge_2']
    assert degree_one['critical_multiplicities']=={'1':0,'-1':0}
    real_phase=check(3,ONE)
    assert real_phase['g_conjugates_phi_to_coefficient_conjugate']
    assert real_phase['g_holomorphically_commutes']
    assert real_phase['J_antiholomorphically_commutes']
    assert real_phase['orbit_1']['points']==['1','0','-1','infinity']
    wrong_orbit=['1','0','1i','-1','infinity','-1i']
    assert wrong_orbit!=r['orbit_1']['points']
    output={
        'status':'PASS', 'arithmetic':'Python Fraction Gaussian rationals; no float operations',
        'new_candidate_attempts':0,
        'main_old_source_cases':main_cases,
        'controls':{'even_degree':even,'degree_one':degree_one,'real_phase':real_phase,
                    'wrong_orbit_mutant_rejected':True},
        'proof_limit':'Finite tested degrees verify implementation; general odd-degree proof is in report.md.'
    }
    text=json.dumps(output,indent=2)+'\n'
    Path(__file__).with_name('exact_checks_output.json').write_text(text)
    print(text)
if __name__=='__main__': main()
