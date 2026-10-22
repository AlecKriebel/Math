#!/usr/bin/env python3
"""Independent exact calibration checks; no submitted source is read or run.

These elementary two-variable examples check the certificate machinery. They
are not an audit or acceptance of any PR212 model or submitted conclusion.
Only Python's standard library is used.
"""
from fractions import Fraction
import json

class P:
    def __init__(self, terms=None, n=6):
        self.n=n
        self.t={k:Fraction(v) for k,v in (terms or {}).items() if v}
    @classmethod
    def var(cls, i, n=6):
        e=[0]*n; e[i]=1
        return cls({tuple(e):1},n)
    def lift(self,v):
        return v if isinstance(v,P) else P({(0,)*self.n:v},self.n)
    def __add__(self,v):
        v=self.lift(v); r=dict(self.t)
        for e,c in v.t.items(): r[e]=r.get(e,Fraction(0))+c
        return P(r,self.n)
    __radd__=__add__
    def __neg__(self): return P({e:-c for e,c in self.t.items()},self.n)
    def __sub__(self,v): return self+-self.lift(v)
    def __rsub__(self,v): return self.lift(v)+-self
    def __mul__(self,v):
        v=self.lift(v); r={}
        for e,c in self.t.items():
            for f,d in v.t.items():
                k=tuple(a+b for a,b in zip(e,f))
                r[k]=r.get(k,Fraction(0))+c*d
        return P(r,self.n)
    __rmul__=__mul__
    def __pow__(self,k):
        assert k>=0
        r=self.lift(1)
        for _ in range(k): r=r*self
        return r
    def zero(self): return not self.t

def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))

# Complete Sym_2 model, n=1: exact ideal-membership and Gram identities.
t1,t2,t3,s11,s22,s12=[P.var(i) for i in range(6)]
f=t1*t2-t3**2
minor=s11*s22-s12**2
membership=minor+(t1-s11)*t2+s11*(t2-s22)-(t3-s12)*(t3+s12)
assert (f-membership).zero()
x,y=P.var(0),P.var(1)
q1,q2,q3=x*x,y*y,x*y
assert (q1*q2-q3*q3).zero()
k11,k12,k22=y*y,-x*y,x*x
assert (k11*x+k12*y).zero()
assert (k12*x+k22*y).zero()
assert (k11*k22-k12*k12).zero()
# PSD holds identically since K=(y,-x)(y,-x)^T; trace=x^2+y^2.
assert (k11-y*y).zero() and (k22-(-x)*(-x)).zero()
assert (k12-y*(-x)).zero()

# Diagonal Sym_2 model, n=1: Jacobian determinant and good completion.
assert ((2*x)*(2*y)-4*x*y).zero()
X0=(Fraction(1),Fraction(1))
Sigma0=((Fraction(1),Fraction(0)),(Fraction(0),Fraction(1)))
assert (X0[0]**2,X0[1]**2)==(Sigma0[0][0],Sigma0[1][1])
assert Sigma0[0][0]>0
assert Sigma0[0][0]*Sigma0[1][1]-Sigma0[0][1]**2>0

# Complete Sym_2 model, n=2: a full-row-rank Jacobian at X=I_2.
# Chosen variable columns: x11, x12, x22.
Jminor=[[2,0,0],[0,0,2],[0,1,0]]
assert det3(Jminor)==-4

# Adjoint factor 1/2 for a one-edge statistic A(S)=(s11,s22,s12).
a,b,c=Fraction(2,3),Fraction(-5,7),Fraction(11,13)
u,v,w=Fraction(17,19),Fraction(23,29),Fraction(31,37)
trKS=a*u+b*v+2*(c/2)*w
assert trKS==a*u+b*v+c*w

print(json.dumps({
 'status':'PASS',
 'scope':'Independent elementary calibration examples only; no submitted artifacts used',
 'arithmetic':'Exact integer polynomial coefficients and rational matrix checks',
 'checks':[
  'Exact nonzero elimination relation membership identity for complete Sym_2 at n=1',
  'Identically zero relation after one-column real Gram substitution',
  'Identically annihilating PSD dyad and determinant-zero stress',
  'Diagonal-model Jacobian minor and rational PD-completion witness at n=1',
  'Complete-model nonzero Jacobian minor at n=2',
  'Adjoint edge-coordinate factor 1/2'
 ]},indent=2))
