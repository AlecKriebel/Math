#!/usr/bin/env python3
"""Independent reconstruction for the nonlinear-frontier verifier.

This module intentionally imports no discovery-side code.
"""
from __future__ import annotations
from dataclasses import dataclass
import sympy as sp

@dataclass(frozen=True)
class R:
    name:str; source:tuple[int,...]; target:tuple[int,...]

def reactions(m:int)->list[R]:
    if m<3: raise ValueError
    n=m+1
    def vv(d=None):
        out=[0]*n
        for i,a in (d or {}).items():out[i]=a
        return tuple(out)
    rr=[R('feed',vv(),vv({0:1}))]
    for i in range(2,m-1):
        rr.append(R(f'chain_{i}',vv({0:1,i-1:1}),vv({0:1,i:1})))
    rr += [
      R('terminal',vv({0:1,m-2:1}),vv({m-1:2})),
      R('return',vv({m-1:2}),vv({1:1})),
      R('plus',vv({m:2}),vv({0:1,m-1:1})),
      R('minus',vv({0:1,m-1:1}),vv({m:2})),
    ]
    assert len(rr)==m+2
    return rr

def gamma_y(m:int):
    rr=reactions(m)
    Y=sp.Matrix.hstack(*(sp.Matrix(q.source) for q in rr))
    Yp=sp.Matrix.hstack(*(sp.Matrix(q.target) for q in rr))
    return Yp-Y,Y

def A(m:int,a=sp.Integer(1),b=sp.Integer(1)):
    G,Y=gamma_y(m)
    flux=sp.Matrix([a]*m+[b,b])
    return sp.simplify(G*sp.diag(*list(flux))*Y.T)

def cvec(m:int): return sp.Matrix([0]+[4]*(m-2)+[2,1])
def rhovec(m:int): return sp.Matrix([2]+[-2]*(m-2)+[0,1])

def Hessian(m:int,u:sp.Matrix,v:sp.Matrix):
    G,Y=gamma_y(m); ans=sp.zeros(m+1,1)
    for k in range(Y.cols):
        q=0
        for i in range(m+1):
            yi=int(Y[i,k]); q += yi*(yi-1)*u[i]*v[i]
            for j in range(i+1,m+1):
                yj=int(Y[j,k]); q += yi*yj*(u[i]*v[j]+u[j]*v[i])
        ans += q*G[:,k]
    return sp.simplify(ans)

def K(m,i): return 91*m-181-i

def rcrit(m):
    return sp.Matrix([1]+[-sp.Rational(K(m,i),63*(m-2)) for i in range(2,m)]+[-sp.Rational(2,9),sp.Rational(5,14)])

def Deff(m):
    return [sp.Rational(23,63)]+[sp.Rational(1,K(m,i)) for i in range(2,m)]+[sp.Rational(1,7),sp.Rational(16,45)]

def ellref(m):
    return sp.Matrix([-sp.Rational(266,815)]+[sp.Rational(78260*(m-2),163*K(m,i-1)) for i in range(2,m)]+[sp.Rational(18368,7335),1])

def Hsum(m): return sp.Add(*(sp.Rational(1,K(m,j)) for j in range(1,m-1)),evaluate=True)
def endpoint_kappa(m):
    """Dimension-dependent constant in the certified lower endpoint.

    The exceptional case m=3 is handled by a direct cubic Routh--Hurwitz
    calculation.  Starting at m=4, the homogeneous half-plane certificate
    requires (m-2)*L**2 >= 5/4.
    """
    if m < 3:
        raise ValueError
    return 1/sp.sqrt(3) if m == 3 else sp.sqrt(5)/2

def L0(m): return sp.factor(endpoint_kappa(m)/sp.sqrt(m-2))
def L1(m):
    r=m-2; return sp.Rational(90*r,90*r+1)
def Hlist(m,L): return [1]+[sp.factor(K(m,i)/(L*K(m,i-1))) for i in range(2,m)]+[1,1]
def Dphys(m,L): return [sp.factor(a*b) for a,b in zip(Hlist(m,L),Deff(m))]

def Q3(m):return 589180301*m**3-3500015940*m**2+6930529579*m-4574434500

def w0ref(m):
    sig=sp.Rational(1,126*(m-2)); b=sp.Rational(1008*m*m-20459*m+37138,31752*(m-2)*(8*m-17))
    return sp.Matrix([sp.Rational(182448*m-373417,31752*(8*m-17)),b,*[b-(i-2)*sig for i in range(3,m)],-sp.Rational(1,81),sp.Rational(16861*m-34044,7938*(8*m-17))])

def Tfac(m,i):
    num=sp.prod(sp.Integer(K(m,j)) for j in range(i-3,i+1))
    den=sp.prod(sp.Integer(K(m,j)) for j in range(-1,3))
    return sp.factor(num/den)
def w2ref(m):
    q=Q3(m);sig=sp.Rational(1,126*(m-2))
    a=sp.Rational(11*(8832129632*m**3-52772027580*m**2+105099636403*m-69768261675),2457*q)
    b=sp.Rational((91*m-183)*(27306456137*m**3-163220086095*m**2+325200697288*m-215972758800),6804*(m-2)*q)
    cm=-sp.Rational(3123724821523*m**3-18723524680620*m**2+37405968085217*m-24907679699400,176904*q)
    z=-sp.Rational(25*(82375210916*m**3-488921724540*m**2+967289665339*m-637893501255),68796*q)
    return sp.Matrix([a,b,*[sp.factor(Tfac(m,i)*(b+sig*K(m,2)/3)-sig*K(m,i)/3) for i in range(3,m)],cm,z])

def N0(m,H):
    q=Q3(m)
    R=(68605040480814208768*m**4-550882186169626030957*m**3+1658612632937449670852*m**2-2219226476204103501323*m+1113379274975809565700)/(sp.Integer(286118780220)*(8*m-17)*q)
    C=-sp.Integer(215)*(652054120726848*m**4-5151971981328467*m**3+15265080924982572*m**2-20102347725659113*m+9927281930180400)/(sp.Integer(11645046)*(8*m-17)*q)
    return sp.factor(R+C*H)

def Sterm(m,H): return sp.factor(-4*(1760850*H-10253)/sp.Integer(462105))
def tau_formula(m,H,L):
    r=m-2
    top=1494249120*H*L*r**2-69786990*H*L*r+108738630*L*r**2+1214388*L*r-8521*L-125249670*r**2+1031940*r
    bot=15876*(8*r-1)*(32760*H*L*r+32760*L*r**2+4*L-4095*r)
    return sp.factor(-top/bot)
def den_formula(m,L): return sp.factor(-sp.Rational(485873,924210)-sp.Rational(11180,1467)*L*(m-2))
def eta_num(m,H): return sp.factor(-2*(1760850*H+16559)/sp.Integer(462105))
