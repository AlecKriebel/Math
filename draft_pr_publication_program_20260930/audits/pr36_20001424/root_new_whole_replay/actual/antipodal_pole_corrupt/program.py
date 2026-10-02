#!/usr/bin/env python3
"""Exact Q(i) controls for Silverman's printed odd-degree map; standard library only.
The complete centralizer/classification proof is in PRIOR_APPLICATION.md.
No Python assert is used: checks stay active under python -O.
"""
import argparse, json, math
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path

@dataclass(frozen=True)
class G:
    a: Q = Q(0)
    b: Q = Q(0)
    def __add__(self,t): return G(self.a+t.a,self.b+t.b)
    def __neg__(self): return G(-self.a,-self.b)
    def __sub__(self,t): return self+-t
    def __mul__(self,t): return G(self.a*t.a-self.b*t.b,self.a*t.b+self.b*t.a)
    def inv(self):
        norm=self.a*self.a+self.b*self.b
        if not norm: raise ZeroDivisionError('zero Gaussian rational')
        return G(self.a/norm,-self.b/norm)
    def __truediv__(self,t): return self*t.inv()
    def __pow__(self,n):
        if n<0: return self.inv()**(-n)
        ans=G(Q(1))
        for _ in range(n): ans=ans*self
        return ans
    def conj(self): return G(self.a,-self.b)
    def label(self):
        for k,v in POINTS.items():
            if v==self: return k
        return str(self.a)+'+('+str(self.b)+')i'

ZERO=G(); ONE=G(Q(1)); I=G(Q(0),Q(1))
POINTS={'1':ONE,'0':ZERO,'-i':-I,'-1':-ONE,'inf':None,'i':I}
def check(cond,msg):
    if not cond: raise ValueError(msg)
def trim(p):
    while len(p)>1 and p[-1]==ZERO: p.pop()
    return p
def add(p,q):
    return trim([(p[j] if j<len(p) else ZERO)+(q[j] if j<len(q) else ZERO) for j in range(max(len(p),len(q)))])
def neg(p): return [-x for x in p]
def sub(p,q): return add(p,neg(q))
def mul(p,q):
    r=[ZERO]*(len(p)+len(q)-1)
    for j,x in enumerate(p):
        for k,y in enumerate(q): r[j+k]=r[j+k]+x*y
    return trim(r)
def scale(p,x):return trim([y*x for y in p])
def powp(p,n):
    r=[ONE]
    for _ in range(n):r=mul(r,p)
    return r
def deriv(p):return trim([G(Q(j))*p[j] for j in range(1,len(p))] or [ZERO])
def evaluate(p,z):
    ans=ZERO
    for x in reversed(p):ans=ans*z+x
    return ans
def eqrat(P,D,R,S):return sub(mul(P,S),mul(R,D))==[ZERO]
def image_point(p,q,z):
    if z is None:
        if len(p)==len(q):return p[-1]/q[-1]
        return None if len(p)>len(q) else ZERO
    den=evaluate(q,z)
    return None if den==ZERO else evaluate(p,z)/den

def run(spec):
    d=spec['degree']; check(d>=3 and d%2==1,'degree must be odd and >=3')
    factor=G(Q(spec['factor'][0]),Q(spec['factor'][1]));check(factor==I,'printed coefficient is exactly i')
    p=scale(powp([-ONE,ONE],d),factor);q=powp([-ONE,ONE],d)
    check(len(p)==d+1 and len(q)==d+1,'wrong degree')
    # Coprime because the only numerator root1 and denominator root-1 differ.
    W=sub(mul(deriv(p),q),mul(p,deriv(q)))
    expected=scale(mul(powp([-ONE,ONE],d-1),powp([ONE,ONE],d-1)),I*G(Q(2*d)))
    check(W==expected,'ramification polynomial disagrees')
    # In the infinity chart the derivative is -2*d*i, so infinity is unramified.
    infinity_chart_derivative=-I*G(Q(2*d));check(infinity_chart_derivative!=ZERO,'ramification at infinity')
    crit=['1','-1'];check(spec['critical_points']==crit,'mutated critical support')
    check(spec['critical_multiplicities']==[d-1,d-1],'mutated critical multiplicities')
    orbit={name:image_point(p,q,z).label() if image_point(p,q,z) is not None else 'inf' for name,z in POINTS.items()}
    check(orbit==spec['orbit'],'mutated orbit receipt')
    check(set(orbit.values())==set(POINTS),'six-point support is not invariant')
    # L phi L versus coefficient conjugate phi, with L=-1/z.
    pL=scale(powp([-ONE,-ONE],d),I);qL=powp([-ONE,ONE],d)
    LP=neg(qL);LD=pL
    barp=[x.conj() for x in p];barq=[x.conj() for x in q]
    check(eqrat(LP,LD,barp,barq),'antipodal/conjugation polynomial identity fails')
    # The only possible critical-swapping holomorphic symmetry is L=-1/z.
    L_of_phi0=-image_point(p,q,ZERO).inv();phi_L0=image_point(p,q,None)
    swap_commutes=(L_of_phi0==phi_L0)
    check(not swap_commutes,'unexpected critical-swapping symmetry')
    check(spec['swap_commutes']==swap_commutes,'mutated centralizer claim')
    cycles=[];remaining=set(POINTS)
    while remaining:
        start=next(k for k in POINTS if k in remaining);cycle=[];k=start
        while k not in cycle:cycle.append(k);remaining.discard(k);k=orbit[k]
        check(k==start,'support is not a permutation');cycles.append(cycle)
    return {'degree':d,'map':'i*((z-1)/(z+1))^'+str(d),'arithmetic':'exact Fraction pairs in Q(i)',
            'orbit':orbit,'cycles':cycles,'critical_points':crit,'critical_multiplicities':[d-1,d-1],
            'ramification_total':2*d-2,'infinity_unramified':True,'antipodal_identity':True,
            'swap_commutes':swap_commutes,'swap_mismatch_at0':[L_of_phi0.label(),phi_L0.label()],
            'algebraic_coefficient_field':'Q(i)','manual_proof_required':['exhaustion of holomorphic symmetries','uniqueness of antiholomorphic symmetry','no real model','absolute field of moduli Q']}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('spec');a=parser.parse_args()
    print(json.dumps(run(json.loads(Path(a.spec).read_text())),indent=2,sort_keys=True))
