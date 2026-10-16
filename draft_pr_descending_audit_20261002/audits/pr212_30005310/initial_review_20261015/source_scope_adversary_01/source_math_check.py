#!/usr/bin/env python3
"""Authored source audit checks; writes only beside this script; exact arithmetic."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import sympy as sp

root = Path(__file__).resolve().parent
checks = []
def check(label, assertion):
    assert assertion, label
    checks.append(label)

# Audit the adjoint differential rather than reusing the submitted Jacobian code.
# A stress K has diagonal blocks diag(a),diag(b) and cross block C.
# K*[I;V]=0 forces C=-V.T*diag(b), diag(a)=V.T*diag(b)*V.
a = sp.symbols('a0:4')
b = sp.symbols('b0:4')
V = sp.Matrix([[1,1,0,0], [0,1,1,0], [0,0,1,1], [1,0,0,1]])
R = V.T*sp.diag(*b)*V
off = sp.Matrix([R[0,1], R[1,2], R[2,3], R[0,3]])
check('off_diagonal_stress_equations_are_b_coordinates', off == sp.Matrix(b))
check('stress_constraints_force_all_b_zero', off.jacobian(b).det() == 1)
check('zero_b_forces_zero_a_and_cross', R.subs(dict(zip(b,[0]*4))) == sp.zeros(4))
check('rank_four_gram_witness', sp.eye(4).col_join(V).rank() == 4)

# The right-side 4-by-4 cross determinant is nonzero as a statistic polynomial.
z = sp.symbols('z0:16')
B = sp.Matrix(4,4,z)
check('cross_determinant_nonzero', B.det().subs(dict(zip(z,list(sp.eye(4))))) == 1)

# Use a two-column Gram witness and check both statistic projections.
Y = sp.Matrix([[1,0]]*4 + [[0,1]]*4)
T = Y*Y.T
P = sp.eye(8)
def projection(M, merged):
    d = [M[i,i] for i in range(8)]
    if merged:
        d = [d[0]+d[1]]+d[2:]
    return d+[M[i,j] for i in range(4) for j in range(4,8)]
check('rank_two_sample_witness', T.rank() == 2)
check('singleton_statistics_match_identity', projection(T,False)==projection(P,False))
check('tied_statistics_match_identity', projection(T,True)==projection(P,True))
Y3 = sp.Matrix([[1,0,0]]*4 + [[0,1,0]]*2 + [[0,0,1]]*2)
T3 = Y3*Y3.T
check('exact_rank_three_intersection_witness', T3.rank()==3)
check('rank_three_singleton_statistics_match_identity', projection(T3,False)==projection(P,False))
check('rank_three_tied_statistics_match_identity', projection(T3,True)==projection(P,True))
e=Fraction(1,100)
check('uniform_PD_margin_positive', (1-e)**2-8*e*(1+e)==Fraction(8993,10000)>0)
check('open_box_rank_two_minor_positive', (1-e)**2-e**2==Fraction(98,100)>0)

# An independent direct likelihood obstruction for one observation in both models.
x3,x5,t=sp.symbols('x3 x5 t',real=True)
v=sp.Matrix([x5,-x3])
x=sp.Matrix([x3,x5])
check('one_sample_stress_annihilates_data', (v.T*x)[0]==0)
check('one_sample_likelihood_ray_determinant', sp.expand((sp.eye(2)+t*v*v.T).det()-1-t*(x3*x3+x5*x5))==0)

# Credited theorem arithmetic, separate from the self-contained negative answer.
k=next(k for k in range(1,9) if k*(k+1)//2 >= 8)
check('Blekherman_Sinn_Theorem_2_7_arithmetic', min(k,5)==4)

out={
    'status':'PASS_EXACT',
    'checks':checks,
    'count':len(checks),
    'method':'adjoint differential, exact matrices and rational inequalities',
    'scope':'Supports literal Proposition 3 numerical counterexample; does not falsify bare A-or-B exhaustiveness',
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
}
(root/'SOURCE_MATH_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
