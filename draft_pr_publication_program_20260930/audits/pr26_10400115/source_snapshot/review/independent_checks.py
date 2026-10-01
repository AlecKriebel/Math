#!/usr/bin/env python3
"""Exact diagnostics only; not a faithfulness search for higher braid groups."""
from pathlib import Path
import hashlib,json
import sympy as s
I=s.eye(2);U=s.Matrix([[1,1],[0,1]]);V=s.Matrix([[1,0],[-1,1]])
checks={}
def check(name,value):
    assert bool(value),name
    checks[name]='PASS'
check('scaled_braid_relation',(2*U)*(2*V)*(2*U)==(2*V)*(2*U)*(2*V))
check('image_nonabelian',U*V!=V*U)
check('modular_order_two',(U*V*U)**2==-I)
check('modular_order_three',(U*V)**3==-I)
check('twisted_center',((2*U)*(2*V))**3==-64*I)
for k in range(-4,5):
    z=(-64)**k if k>=0 else s.Rational(1,(-64)**(-k))
    check('central_power_'+str(k),(z*I==I)==(k==0))
# Three nonscalar Jordan/rational-canonical types; solve the commutation equations.
entries=s.symbols('a:d');X=s.Matrix(2,2,entries)
for n,C in enumerate((s.Matrix([[0,2],[1,0]]),s.Matrix([[1,1],[0,1]]),s.diag(2,3))):
    equations=list(X*C-C*X)
    A,_=s.linear_eq_to_matrix(equations,entries)
    check('centralizer_dimension_'+str(n),len(A.nullspace())==2)
    check('centralizer_basis_'+str(n),s.Matrix.hstack(s.Matrix(list(I)),s.Matrix(list(C))).rank()==2)
# The regular representation of Q(sqrt(2)) on basis (1,sqrt(2)).
def reg(a,b):return s.Matrix([[a,2*b],[b,a]])
R=reg(0,1)
check('regular_square',R*R==2*I)
A=s.BlockMatrix([[R,I],[I,I]]).as_explicit()
# Algebraic determinant sqrt(2)-1 has norm -1.
check('restriction_of_scalars_determinant',A.det()==-1)
check('restriction_of_scalars_inverse',A*A.inv()==s.eye(4))
# Build a kernel word from each integer annihilating polynomial, including
# nonmonic and negative-coefficient examples. Check modulo its ideal exactly.
t=s.symbols('t');D=s.diag(t,1)
for n,p in enumerate((2*t-3,t*t-2,t*t+1,t**3-t-1)):
    W=I
    for (k,),c in s.Poly(p,t).terms():
        W=W*D**k*U**int(c)*D**(-k)
    W=s.simplify(W)
    check('polynomial_word_'+str(n),W==s.Matrix([[1,p],[0,1]]))
    check('word_nontrivial_'+str(n),W!=I)
    check('word_killed_mod_polynomial_'+str(n),all(s.rem(z,p,t)==0 for z in W-I))
receipt={'status':'PASS','assertions':len(checks),'sympy_version':s.__version__,'checks':checks,'scope':'Exact matrix identities; the general arguments and limits are in REVIEW.md.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
