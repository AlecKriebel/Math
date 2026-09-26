#!/usr/bin/env python3
"""Fresh reviewer checks; imports no manuscript verifier. SymPy 1.14.0.
Word products use binary X^x Z^z encoding, independent of the printed table.
Dense matrix checks independently use literal two-by-two matrices.
"""
from collections import defaultdict
from itertools import product
import json
import sympy as s
from datetime import datetime, timezone

I=s.I
rt=s.sqrt
alpha,beta=s.symbols('alpha beta',real=True)
bits={'I':(0,0),'X':(1,0),'Z':(0,1),'J':(1,1)}
inv={v:k for k,v in bits.items()}
def wordmul(a,b):
    out=[]; sign=1
    for ca,cb in zip(a,b):
        x,z=bits[ca]; y,w=bits[cb]
        sign*=(-1)**(z*y)
        out.append(inv[(x^y,z^w)])
    return ''.join(out),sign

def clean(a):
    return {k:v for k,x in a.items() if (v:=s.expand(x))!=0}
def mul(a,b):
    out=defaultdict(lambda:s.Integer(0))
    for wa,ca in a.items():
        for wb,cb in b.items():
            w,p=wordmul(wa,wb); out[w]+=p*ca*cb
    return clean(out)
def add(*args):
    out=defaultdict(lambda:s.Integer(0))
    for a in args:
        for w,c in a.items():out[w]+=c
    return clean(out)
def scale(c,a):return clean({w:c*v for w,v in a.items()})
def shift(a,l,r):return {'I'*l+w+'I'*r:c for w,c in a.items()}
def residual(a,m):
    l=shift(a,0,m); r=shift(a,m,0)
    return add(mul(mul(l,r),l),scale(-1,mul(mul(r,l),r)))
def frob(a):
    if not a:return s.Integer(0)
    return s.simplify(2**len(next(iter(a)))*sum(s.conjugate(c)*c for c in a.values()))

M={'ZIZZ':-s.Rational(1,2),'ZIJJ':-s.Rational(1,2),'JIZJ':-s.Rational(1,2),'JIJZ':s.Rational(1,2)}
E={'XIXX':s.Integer(1)}
Hf=add(scale(alpha,M),scale(beta,E))
l=shift(Hf,0,2);r=shift(Hf,2,0)
actual=add(residual(Hf,2),scale(-s.Rational(1,3),l),scale(s.Rational(1,3),r))
expected={}
rows=[(-alpha*(3*beta**2-1)/6,'IIJIJZ JIZJII ZIJJII ZIZZII'),(alpha*(3*beta**2-1)/6,'IIJIZJ IIZIJJ IIZIZZ JIJZII'),(-beta*(3*alpha**2-3*beta**2-1)/3,'IIXIXX'),(beta*(3*alpha**2-3*beta**2-1)/3,'XIXXII'),(alpha*(alpha**2-2*beta**2)/2,'JIJZXX JIZJXX XIJXZJ ZIZZXX'),(-alpha*(alpha**2-2*beta**2)/2,'XIJXJZ XIZXJJ XIZXZZ ZIJJXX')]
for c,words in rows:
    for w in words.split():expected[w]=c
assert actual==clean(expected),(actual,clean(expected))
assert len(actual)==18
print('PASS complete 18-word certificate as polynomial identity even before circle restriction',flush=True)
# Exact converse: radical ideal/groebner basis plus exceptional axis checks.
g=s.groebner(list(actual.values())+[alpha**2+beta**2-1],alpha,beta)
assert list(g)==[alpha**2-s.Rational(2,3),beta**2-s.Rational(1,3)]
print('PASS converse ideal Groebner basis:',list(g),flush=True)
assert all(s.simplify(v.subs({alpha:sa*rt(s.Rational(2,3)),beta:sb/rt(3)}))==0 for v in actual.values() for sa,sb in product([-1,1],repeat=2))
for aa,bb in [(1,0),(-1,0),(0,1),(0,-1)]:
    assert any(v.subs({alpha:aa,beta:bb})!=0 for v in actual.values())
print('PASS four signed solutions and four excluded axis endpoints',flush=True)
assert mul(M,M)=={'IIII':1} and mul(E,E)=={'IIII':1}
assert add(mul(M,E),mul(E,M))=={}
for a,b,c in product([0,1],repeat=3):
    x,y,z=[(-1)**k for k in [a,b,c]]
    assert s.Rational(-x-y-z+x*y*z,2)==-(-1)**(a*b+a*c+b*c)
print('PASS reflection and graph phase identities',flush=True)
H=add(scale(rt(s.Rational(2,3)),M),scale(-1/rt(3),E))
q=(1+I*rt(3))/2
R=add({'IIII':(q-1)/2},scale((q+1)/2,H))
assert residual(R,2)=={}
assert all(w[:2]!='II' and w[2:]!='II' for w in H)
print('PASS ordinary braid residual, both zero partial traces',flush=True)
KH={'ZZZ':-1/rt(6),'ZJJ':-1/rt(6),'JJZ':-1/rt(6),'JZJ':1/rt(6),'XXX':-1/rt(3)}
assert {w[1]+w[0]+w[3]+w[2]:c for w,c in H.items()}==shift(KH,1,0)
K=add({'III':(q-1)/2},scale((q+1)/2,KH))
assert frob(residual(K,1))==24
assert residual(K,2)=={}
for n in range(2,8):
    for k in range(1,n):
        old=shift(R,2*(k-1),2*(n-k-1))
        swapped={''.join(w[j+1]+w[j] for j in range(0,len(w),2)):c for w,c in old.items()}
        assert swapped==shift(K,1+2*(k-1),2*(n-k-1))
print('PASS generalized blocking, all generator placements n=2..7, norms (24,0)',flush=True)
# Dense checks with direct Kronecker products, independently of binary words.
pauli={'I':s.eye(2),'X':s.Matrix([[0,1],[1,0]]),'Z':s.diag(1,-1),'J':s.Matrix([[0,-1],[1,0]])}
def mat(w):return s.kronecker_product(*[pauli[c] for c in w])
def zmat(A):return A.applyfunc(s.simplify)==s.zeros(*A.shape)
A,B,C,D,F=[mat(w) for w in ['ZIZZ','ZIJJ','JIZJ','JIJZ','XIXX']]
assert all(T==T.T and T*T==s.eye(16) for T in [A,B,C,D,F])
assert A*B*C==D
assert all(T1*T2==T2*T1 for T1,T2 in product([A,B,C,D],repeat=2))
assert all(T*F==-F*T for T in [A,B,C,D])
Md=(-A-B-C+D)/2
Ad=-I*rt(2)*Md; Bd=I*F
Uk=(Ad+Ad*Bd)/2; Vk=(Ad-Ad*Bd)/2
assert Uk*Vk==Bd and Vk*Uk==-Bd
assert Uk*Uk==-s.eye(16) and Vk*Vk==-s.eye(16)
assert Uk.conjugate().T==-Uk and Vk.conjugate().T==-Vk
r=rt(2)
S=s.Matrix([[2+r,-I*r,I*r,2-r],[r,I*(2+r),I*(2-r),-r],[-(2-r),-I*r,I*r,-(2+r)],[-r,I*(2-r),I*(2+r),r]])/4
assert zmat(S.conjugate().T*S-s.eye(4))
U=I*mat('IZZI');V=I*mat('XIXX')
flip=s.zeros(16)
for a,b in product(range(4),repeat=2):flip[4*b+a,4*a+b]=1
S2=s.kronecker_product(S,S)
def conj(T):return (S2.conjugate().T*flip*T*flip*S2).applyfunc(s.expand)
assert zmat(conj(U)-Uk)
assert zmat(conj(V)-Vk)
assert zmat(conj(U*V)-Uk*Vk)
Hd=rt(s.Rational(2,3))*Md-F/rt(3)
Rd=(q-1)*s.eye(16)/2+(q+1)*Hd/2
zeta=(rt(3)+I)/2
Rgr=I*zeta*(s.eye(16)+U+V+U*V)/2
assert zmat(conj(Rgr)-Rd)
assert zmat(Rd.conjugate().T*Rd-s.eye(16))
assert zmat((Rd+s.eye(16))*(Rd-q*s.eye(16)))
assert s.trace(Hd)==0
assert not zmat(S2.conjugate().T*Rgr*S2-Rd)
print('PASS literal S unitarity, U/V/UV intertwining, full R equivalence, opposite required for this S',flush=True)
# Direct tensor contraction of both partial traces of P.
P=(s.eye(16)-Hd)/2
for first in [True,False]:
    out=s.zeros(4)
    for a,b,c in product(range(4),repeat=3):
        out[a,b]+=P[4*c+a,4*c+b] if first else P[4*a+c,4*b+c]
    assert out==2*s.eye(4)
print('PASS dense partial traces, unitary Hecke matrix, equal multiplicities',flush=True)
print('FINISHED',datetime.now(timezone.utc).isoformat(),flush=True)
