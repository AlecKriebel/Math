#!/usr/bin/env python3
"""Independent reconstruction; deliberately imports no discovery-side module."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
import sympy as sp

@dataclass(frozen=True)
class Reaction:
    label:str; y:tuple[int,...]; yp:tuple[int,...]

def reaction_list(m:int)->list[Reaction]:
    if m<3: raise ValueError
    n=m+1
    def vec(items=None):
        v=[0]*n
        for k,x in (items or {}).items():v[k]=x
        return tuple(v)
    r=[Reaction('feed',vec(),vec({0:1}))]
    for i in range(2,m-1):r.append(Reaction(f'chain{i}',vec({0:1,i-1:1}),vec({0:1,i:1})))
    r.extend([
      Reaction('terminal',vec({0:1,m-2:1}),vec({m-1:2})),
      Reaction('return',vec({m-1:2}),vec({1:1})),
      Reaction('plus',vec({m:2}),vec({0:1,m-1:1})),
      Reaction('minus',vec({0:1,m-1:1}),vec({m:2}))])
    assert len(r)==m+2
    return r

def matrices(m:int):
    rs=reaction_list(m)
    Y=sp.Matrix.hstack(*(sp.Matrix(r.y) for r in rs));Yp=sp.Matrix.hstack(*(sp.Matrix(r.yp) for r in rs))
    return Yp-Y,Y

def Avec(m:int,a=sp.Integer(1),b=sp.Integer(1)):
    G,Y=matrices(m);v=sp.Matrix([a]*m+[b,b]);return sp.simplify(G*sp.diag(*list(v))*Y.T)

def cvec(m:int):return sp.Matrix([0]+[4]*(m-2)+[2,1])

def B(m:int,u:sp.Matrix,v:sp.Matrix):
    G,Y=matrices(m);ans=sp.zeros(m+1,1)
    for r in range(Y.cols):
        q=0
        for i in range(m+1):
            yi=int(Y[i,r]);q+=yi*(yi-1)*u[i]*v[i]
            for j in range(i+1,m+1):
                yj=int(Y[j,r]);q+=yi*yj*(u[i]*v[j]+u[j]*v[i])
        ans += q*G[:,r]
    return sp.simplify(ans)

def K(m,i):return 91*m-181-i

def selected(m:int):
    r=sp.Matrix([1]+[-sp.Rational(K(m,i),63*(m-2)) for i in range(2,m)]+[-sp.Rational(2,9),sp.Rational(5,14)])
    d=[sp.Rational(23,63)]+[sp.Rational(1,K(m,i)) for i in range(2,m)]+[sp.Rational(1,7),sp.Rational(16,45)]
    ell=sp.Matrix([-sp.Rational(266,815)]+[sp.Rational(78260*(m-2),163*K(m,i-1)) for i in range(2,m)]+[sp.Rational(18368,7335),1])
    return r,d,ell

def Hsum(m:int):return sp.Add(*(sp.Rational(1,K(m,j)) for j in range(1,m-1)),evaluate=True)
def Q3(m):return 589180301*m**3-3500015940*m**2+6930529579*m-4574434500

def w0(m:int):
    s=sp.Rational(1,126*(m-2));w2=sp.Rational(1008*m*m-20459*m+37138,31752*(m-2)*(8*m-17))
    return sp.Matrix([sp.Rational(182448*m-373417,31752*(8*m-17)),w2,*[w2-(i-2)*s for i in range(3,m)],-sp.Rational(1,81),sp.Rational(16861*m-34044,7938*(8*m-17))])
def T(m,i):
    num=sp.prod(sp.Integer(K(m,j)) if isinstance(K(m,j),int) else K(m,j) for j in range(i-3,i+1))
    den=sp.prod(sp.Integer(K(m,j)) if isinstance(K(m,j),int) else K(m,j) for j in range(-1,3))
    return sp.factor(num/den)
def w2(m:int):
    q=Q3(m);sig=sp.Rational(1,126*(m-2))
    a=sp.Rational(11*(8832129632*m**3-52772027580*m**2+105099636403*m-69768261675),2457*q)
    b=sp.Rational((91*m-183)*(27306456137*m**3-163220086095*m**2+325200697288*m-215972758800),6804*(m-2)*q)
    c=-sp.Rational(3123724821523*m**3-18723524680620*m**2+37405968085217*m-24907679699400,176904*q)
    z=-sp.Rational(25*(82375210916*m**3-488921724540*m**2+967289665339*m-637893501255),68796*q)
    return sp.Matrix([a,b,*[sp.factor(T(m,i)*(b+sig*K(m,2)/3)-sig*K(m,i)/3) for i in range(3,m)],c,z])
def ellr_formula(m,H):return sp.factor(-(-7043400*H+7043400*m-13600927)/sp.Integer(924210))
def ellDr_formula(m,H):return sp.factor(-2*(1760850*H+16559)/sp.Integer(462105))
def N_formula(m,H):
    q=Q3(m)
    R=(68605040480814208768*m**4-550882186169626030957*m**3+1658612632937449670852*m**2-2219226476204103501323*m+1113379274975809565700)/(sp.Integer(286118780220)*(8*m-17)*q)
    C=-sp.Integer(215)*(652054120726848*m**4-5151971981328467*m**3+15265080924982572*m**2-20102347725659113*m+9927281930180400)/(sp.Integer(11645046)*(8*m-17)*q)
    return sp.factor(R+C*H)
def signed_omissions(m,a=sp.Integer(1),b=sp.Integer(1)):
    A=Avec(m,a,b);out=[]
    for omit in range(m+1):
      I=[i for i in range(m+1) if i!=omit];out.append(sp.factor((-1)**m*A.extract(I,I).det()))
    return out

# Compatibility aliases used by simulation and figure code.
def d_seed(m:int): return selected(m)[1]
def r_seed(m:int): return selected(m)[0]
def ell_seed(m:int): return selected(m)[2]
def ell_r_formula(m,H): return ellr_formula(m,H)
def ell_Dr_formula(m,H): return ellDr_formula(m,H)
def cubic_num_formula(m,H): return N_formula(m,H)
