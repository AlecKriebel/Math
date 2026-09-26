#!/usr/bin/env python3
"""Independent transcription from visually checked GHR preprint Eq.(5.2), p26.
Compare literally printed scalar assignment with common-prefactor correction.
No production verification modules are imported.
"""
import sympy as s
from itertools import product
from datetime import datetime,timezone
I=s.I;r=s.sqrt
q=(1+I*r(3))/2
z=(1+I)/r(2);zi=s.conjugate(z)
A=s.Matrix([[zi,0,-zi,0],[0,z,0,z],[z,0,z,0],[0,-zi,0,zi]])
B=s.Matrix([[z,0,z,0],[0,zi,0,-zi],[-zi,0,zi,0],[0,z,0,z]])
scalar=-s.conjugate(q)/r(2)
printed=s.diag(scalar*A,B/r(2)).applyfunc(s.expand)
corrected=(scalar*s.diag(A,B)).applyfunc(s.expand)
def tidy(A):return A.applyfunc(s.expand)
def residual(L,m):
    a=s.kronecker_product(L,s.eye(2**m));b=s.kronecker_product(s.eye(2**m),L)
    return tidy(tidy(tidy(a*b)*a)-tidy(tidy(b*a)*b))
def norm2(A):return s.simplify(sum(s.expand(s.conjugate(v)*v) for v in A))
for name,L,expected_norms,expected_hecke in [('literal_preprint',printed,(30,60),18),('common_prefactor',corrected,(0,48),0)]:
    print(name,'trace',s.simplify(s.trace(L)),flush=True)
    print(name,'charpoly',s.factor((s.symbols('t')*s.eye(8)-L).det(),extension=[I,r(3)]),flush=True)
    for m in [1,2]:
        R=residual(L,m)
        assert norm2(R)==expected_norms[m-1]
        print(name,'m',m,'residual_norm2',norm2(R),flush=True)
        nonzero=[(i,j,s.simplify(R[i,j])) for i,j in product(range(R.rows),repeat=2) if R[i,j]!=0]
        print(name,'m',m,'first_nonzero',nonzero[:1],flush=True)
    hn=norm2(tidy((L+s.eye(8))*(L-q*s.eye(8))))
    assert hn==expected_hecke
    print(name,'Hecke residual norm2',hn,flush=True)
# A short, explicit definition of the corrected representative is possible.
paulis={'I':s.eye(2),'X':s.Matrix([[0,1],[1,0]]),'Z':s.diag(1,-1),'J':s.Matrix([[0,-1],[1,0]])}
Q=tidy(2*corrected/(-s.conjugate(q)))
expansion={}
for letters in product(paulis,repeat=3):
    word=''.join(letters);T=s.kronecker_product(*(paulis[c] for c in word))
    c=s.simplify(s.trace(T.conjugate().T*Q)/8)
    if c:expansion[word]=str(c)
print('common_prefactor equals -qbar/2 times',expansion,flush=True)
left=s.kronecker_product(corrected,s.eye(4));right=s.kronecker_product(s.eye(4),corrected)
print('common_prefactor far commutator norm2',norm2(tidy(left*right-right*left)),flush=True)

assert s.simplify(s.trace(printed)-(1+I*r(3)))==0
assert s.simplify(s.trace(corrected)-4*(q-1))==0
assert norm2(tidy(left*right-right*left))==0
assert expansion=={'III':'1','IXI':'I','ZZZ':'-I','ZJZ':'1'}
print('FINISHED',datetime.now(timezone.utc).isoformat(),flush=True)
