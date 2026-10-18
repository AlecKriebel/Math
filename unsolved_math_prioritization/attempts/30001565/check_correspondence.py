"""Exact controls for the credited source-to-split-algebra correspondence.

This does not reimplement the Ivanyos–Rónyai–Schicho algorithm. It constructs
an actual Schurian coherent configuration (the regular S3 action), checks its
central block, a known rank-one-in-the-block element, the left-ideal action,
and its trace-Gram *-normalization. No downloaded package is run.
"""
from itertools import permutations
from collections import Counter
import json
import sympy as s
counts=Counter()
def ck(x,n):
    assert x,n
    counts[n]+=1
P=list(permutations(range(3)));idx={p:i for i,p in enumerate(P)}
def mul(a,b):return tuple(a[b[i]] for i in range(3))
def inverse(a):return tuple(a.index(i) for i in range(3))
def regular(g):
    A=s.zeros(6)
    for j,h in enumerate(P):A[idx[mul(g,h)],j]=1
    return A
A=[regular(g) for g in P];eye=s.eye(6);J=s.ones(6)
ck(sum(A,s.zeros(6))==J,'coherent_disjoint_cover')
ck(eye in A,'coherent_identity')
for i,g in enumerate(P):
    ck(A[i].T==A[idx[inverse(g)]],'coherent_transpose')
    for j,h in enumerate(P):ck(A[i]*A[j]==A[idx[mul(g,h)]],'coherent_structure_constants')
chi={g:sum(g[i]==i for i in range(3))-1 for g in P}
e=sum((s.Rational(1,3)*chi[inverse(g)]*A[i] for i,g in enumerate(P)),s.zeros(6))
ck(e*e==e and e.T==e,'character_projection_self_adjoint_idempotent')
ck(e.rank()==4,'physical_isotypic_rank')
B=[e*a for a in A]
def flat(M):return s.Matrix(list(M))
ck(s.Matrix.hstack(*[flat(b) for b in B]).rank()==4,'component_dimension_m_squared')
t=(1,0,2);u=(0,2,1)
x=e*(eye+regular(t))/2
ck(x*x==x and x.T==x,'chosen_block_idempotent')
ck(x.rank()==2,'reduced_rank_one_is_not_physical_rank_one')
Ivec=s.Matrix.hstack(*[flat(b*x) for b in B]).columnspace()
ck(len(Ivec)==2,'minimal_left_ideal_dimension')
U=[s.Matrix(6,6,v) for v in Ivec];basis=s.Matrix.hstack(*Ivec)
R=[]
for a in A:
    columns=[]
    for v in U:
        sol,params=basis.gauss_jordan_solve(flat(a*v));ck(params.rows==0,'unique_left_action_coordinates');columns.append(sol)
    R.append(s.Matrix.hstack(*columns))
ck(s.Matrix.hstack(*[flat(r) for r in R]).rank()==4,'absolutely_irreducible_full_image')
H=s.Matrix([[(u.T*v).trace() for v in U] for u in U])
ck(H[0,0]>0 and H.det()>0,'positive_trace_Gram')
C=H.cholesky().T
ck(s.simplify(C.T*C-H)==s.zeros(2),'exact_Gram_factor')
Phi=[s.simplify(C*r*C.inv()) for r in R]
for i,g in enumerate(P):
    astar=idx[inverse(g)]
    ck(R[i].T*H==H*R[astar],'adjoint_relative_to_trace_Gram')
    ck(s.simplify(Phi[i].T-Phi[astar])==s.zeros(2),'standard_star_after_normalization')
    for j,h in enumerate(P):
        k=idx[mul(g,h)]
        ck(R[i]*R[j]==R[k],'left_action_multiplicative')
        ck(s.simplify(Phi[i]*Phi[j]-Phi[k])==s.zeros(2),'normalized_action_multiplicative')
# A real self-adjoint algebra element whose reduced polynomial does not split over Q.
X=e*(regular(t)+2*regular(u));RX=R[idx[t]]+2*R[idx[u]];T=s.symbols('t')
ck(X.T==X and e*X==X,'nonsplit_example_is_self_adjoint_component_element')
ck(RX.charpoly(T).as_expr()==T*T-3,'nonsplit_reduced_polynomial')
ck(s.Poly(T*T-3,T,domain=s.QQ).is_irreducible,'nonsplit_over_given_splitting_field_Q')
ck(s.factor(X.charpoly(T).as_expr())==T*T*(T*T-3)**2,'ambient_characteristic_multiplicities')
# The field needed for standard orthonormality is a distinct question.
R0=s.Matrix([[0,-1],[1,-1]]);T0=s.Matrix([[0,1],[1,0]]);H0=s.Matrix([[2,-1],[-1,2]])
ck(R0**3==s.eye(2) and T0**2==s.eye(2) and T0*R0*T0==R0.inv(),'standard_S3_relations')
ck(R0.T*H0*R0==H0 and T0.T*H0*T0==H0,'standard_S3_invariant_form')
a,b,c=s.symbols('a b c');Z=s.Matrix([[a,b],[b,c]])
sol=s.linsolve(list(R0.T*Z*R0-Z)+list(T0.T*Z*T0-Z),(a,b,c))
ck(sol==s.FiniteSet((c,-c/2,c)),'unique_rational_invariant_form_line')
ck(H0.det()==3,'rational_orthonormality_square_class_obstruction')
# Repeated embeddings of full matrix algebras: left-ideal dimension, not ambient rank.
for m in range(1,5):
    units=[]
    for i in range(m):
        for j in range(m):
            E=s.zeros(m);E[i,j]=1;units.append(E)
    E11=units[0]
    for r in range(1,5):
        xx=s.kronecker_product(s.eye(r),E11)
        bs=[s.kronecker_product(s.eye(r),E) for E in units]
        ck(xx.rank()==r,'amplified_physical_rank')
        ck(s.Matrix.hstack(*[flat(bb*xx) for bb in bs]).rank()==m,'amplified_minimal_left_ideal_dimension')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'categories':dict(sorted(counts.items())),'S3_trace_Gram':[[str(z) for z in row] for row in H.tolist()],'S3_normalization':[[str(z) for z in row] for row in C.tolist()],'scope':'Exact correspondence and normalization controls, not a reimplementation or complexity benchmark of the published split-algebra algorithm.','substantive_author_research_turns':0,'credit':'Ivanyos–Ronyai–Schicho2012 for the general algorithm; classical centralizer decomposition, minimal-left-ideal representation and trace-Gram unitarization.'},indent=2,sort_keys=True))
