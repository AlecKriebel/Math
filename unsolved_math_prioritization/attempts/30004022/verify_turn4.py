#!/usr/bin/env python3
"""Exact deterministic controls for the specialized commutator linearization."""
import sympy as s
import json
from collections import Counter
C=Counter()
def ck(g,v):
    if not v:raise AssertionError(g)
    C[g]+=1
I=s.I;eps=s.symbols('eps',real=True);a,b=s.symbols('a b',commutative=False)
Q=s.Matrix([[0,-I],[I,0]])
ck('lower_corner_involution',Q*Q==s.eye(2))
ck('regularized_lower_inverse',s.simplify((I*eps*s.eye(2)-Q)*(-I*eps*s.eye(2)-Q)/(1+eps**2))==s.eye(2))
v=s.Matrix([[a,b]]);vt=s.Matrix([a,b]);c=I*(a*b-b*a)
ck('formal_commutator_sign',s.expand((v*Q*vt)[0]+c)==0)
ck('formal_regularized_schur',s.expand((v*(-I*eps*s.eye(2)-Q)*vt)[0]-(c-I*eps*(a*a+b*b)))==0)

pairs=[
    (s.Matrix([[1,0],[0,0]]),s.Matrix([[0,1],[1,0]])),
    (s.Matrix([[2,1],[1,-1]]),s.Matrix([[0,2],[2,3]])),
    (s.Matrix([[s.Rational(1,2),1],[1,s.Rational(-2,3)]]),s.Matrix([[1,0],[0,-2]])),
    (s.zeros(2),s.Matrix([[2,1],[1,3]])),
    (s.eye(2)*3,s.Matrix([[1,2],[2,-1]])),
]
cases=0
for A,B in pairs:
    Cc=I*(A*B-B*A);D2=A*A+B*B;d=2;E=s.eye(d);O=s.zeros(d)
    La=s.BlockMatrix([[O,A,B],[A,O,-I*E],[B,I*E,O]]).as_explicit()
    ck('matrix_selfadjoint_pencil',La.H==La)
    ck('matrix_selfadjoint_commutator',Cc.H==Cc)
    abound=max(sum(abs(A[i,j]) for j in range(d)) for i in range(d))
    bbound=max(sum(abs(B[i,j]) for j in range(d)) for i in range(d))
    for z in [I,s.Rational(1,2)+2*I,-2+s.Rational(1,3)*I]:
        eta=s.im(z);R0=(z*E-Cc).inv()
        Lambda0=s.diag(z*E,O,O)
        ck('unregularized_block_identity',s.simplify((Lambda0-La).inv()[:d,:d]-R0)==O)
        for ee in [s.Rational(1,8),s.Rational(1,2),s.Rational(2,3)]:
            cases+=1
            Lambda=s.diag(z*E,I*ee*E,I*ee*E)
            block=(Lambda-La).inv()[:d,:d]
            schur=z*E-Cc/(1+ee*ee)+I*ee*D2/(1+ee*ee)
            RR=schur.inv()
            ck('regularized_block_identity',s.simplify(block-RR)==O)
            ck('imaginary_coercivity_identity',s.simplify((schur-schur.H)/(2*I)-eta*E-ee*D2/(1+ee*ee))==O)
            Delta=s.simplify(RR-R0)
            bound=(2*ee*ee*abound*bbound+ee*(abound**2+bbound**2))/((1+ee*ee)*eta*eta)
            H=s.simplify(bound*bound*E-Delta.H*Delta)
            ck('exact_norm_bound_diagonal',all(s.simplify(H[j,j])>=0 for j in range(d)))
            ck('exact_norm_bound_determinant',s.simplify(H.det())>=0)
            ck('exact_resolvent_identity',s.simplify(Delta-RR*(-ee*ee*Cc-I*ee*D2)/(1+ee*ee)*R0)==O)
print(json.dumps({'problem_id':30004022,'turn':4,'status':'PASS','counts':dict(sorted(C.items())),
    'exact_assertions':sum(C.values()),'regularized_matrix_cases':cases,'arithmetic':'exact symbolic noncommutative expressions and rational complex matrices',
    'scope':'Deterministic Schur identities and norm-bound controls. The operator-valued subordination theorem is credited primary literature; no finite matrix is assumed free and no floating-point fixed-point convergence is claimed.'},indent=2,sort_keys=True))
