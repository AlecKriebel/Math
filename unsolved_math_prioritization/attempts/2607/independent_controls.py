#!/usr/bin/env python3
"""Independent audit controls. No import from the candidate's control script."""
from itertools import permutations, product
from pathlib import Path
import json
from sympy import Matrix, eye

matrix_count=power_checks=rigidity_checks=0
for d in range(1,5):
    for p in permutations(range(d)):
        for signs in product((-1,1),repeat=d):
            M=Matrix(d,d,lambda i,j: signs[j] if i==p[j] else 0)
            D=M-eye(d)
            r=D.rank()
            matrix_count+=1
            for exponent in range(1,6):
                assert (D**exponent).rank()==r
                power_checks+=1
                if M.det()==1 and (D**exponent).rank()<=1:
                    assert M==eye(d)
                    rigidity_checks+=1

# Represent H(Z) x H(Z) as two independently multiplied 3x3 matrices.
def matrices(t):
    return Matrix([[1,t[0],t[4]],[0,1,t[1]],[0,0,1]]), Matrix([[1,t[2],t[5]],[0,1,t[3]],[0,0,1]])
def coordinates(pair):
    A,B=pair
    return (int(A[0,1]),int(A[1,2]),int(B[0,1]),int(B[1,2]),int(A[0,2]),int(B[0,2]))
def pairmul(P,Q):return tuple(A*B for A,B in zip(P,Q))
def pairinv(P):return tuple(A.inv() for A in P)
def comm(P,Q):return pairmul(pairmul(pairmul(pairinv(P),pairinv(Q)),P),Q)
X=set()
for pos in range(4):
    for horizontal,c,d in product(range(-2,3),range(-1,2),range(-1,2)):
        t=[0]*6;t[pos]=horizontal;t[4]=c;t[5]=d;X.add(tuple(t))
# Independent exact matrix formula verified once symbolically, then evaluated.
from sympy import symbols, simplify
u=symbols('a b c d e f');v=symbols('A B C D E F')
U=matrices(u);V=matrices(v)
# coordinates() deliberately casts integers; retain symbols here.
C=tuple(A.applyfunc(simplify) for A in comm(U,V))
assert C[0]==Matrix([[1,0,u[0]*v[1]-v[0]*u[1]],[0,1,0],[0,0,1]])
assert C[1]==Matrix([[1,0,u[2]*v[3]-v[2]*u[3]],[0,1,0],[0,0,1]])
# Use lambdify of symbolic matrix commutator, avoiding the release multiplication formula.
from sympy import lambdify
central=lambdify(u+v,(C[0][0,2],C[1][0,2]),'math')
heisenberg_pairs=0
for x,y in product(X,repeat=2):
    z=central(*(x+y))
    assert z==(x[0]*y[1]-y[0]*x[1],x[2]*y[3]-y[2]*x[3])
    assert z[0]==0 or z[1]==0
    heisenberg_pairs+=1
# Symbolic normality and inverse closure for arbitrary inputs: abelianization unchanged/negated.
Ui=pairinv(U)
assert (Ui[0][0,1],Ui[0][1,2],Ui[1][0,1],Ui[1][1,2])==tuple(-t for t in u[:4])
conjugate=pairmul(pairmul(pairinv(V),U),V)
assert tuple(simplify(z) for z in (conjugate[0][0,1],conjugate[0][1,2],conjugate[1][0,1],conjugate[1][1,2]))==u[:4]
# Exact actual group-matrix basis commutators give independent central generators.
e=[tuple(int(i==j) for i in range(6)) for j in range(6)]
assert coordinates(comm(matrices(e[0]),matrices(e[1])))==e[4]
assert coordinates(comm(matrices(e[2]),matrices(e[3])))==e[5]
# Distinct affine directions, direct determinant criterion.
points=[Matrix([1,n]) for n in range(-100,101)]
assert all(Matrix.hstack(P,Q).det()!=0 for i,P in enumerate(points) for Q in points[i+1:])
result={
 'implementation':'independent SymPy exact matrices and symbolic unitriangular matrices',
 'signed_permutation_matrices':matrix_count,
 'signed_permutation_power_rank_checks':power_checks,
 'determinant_one_rank_at_most_one_checks':rigidity_checks,
 'heisenberg_X_samples':len(X),
 'heisenberg_commutator_pair_checks':heisenberg_pairs,
 'heisenberg_symbolic_formula_verified':True,
 'heisenberg_symbolic_conjugation_and_inverse_verified':True,
 'heisenberg_basis_commutators_rank':2,
 'distinct_affine_directions':len(points),
 'candidate_code_imported':False,
 'scope':'Finite controls and exact symbolic identities only; not evidence of universal quantification.'}
assert power_checks==2210 and rigidity_checks==20 and heisenberg_pairs==23409
path=Path(__file__).with_name('independent_control_results.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
