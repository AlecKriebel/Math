"""Independent exact algebra audit. Requires SymPy; no concordance test."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import gcd
import hashlib,json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form

root=Path(__file__).resolve().parent
EXPECTED='99bcb8b993af2ac3fafadadbf6fae854718cb57c6227d1ef19824d9e3b5632d3'
assert hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest()==EXPECTED
counts={}
def ck(v,name):
    assert bool(v),name
    counts[name]=counts.get(name,0)+1
V1=s.Matrix([[3,2],[1,3]]);V2=s.Matrix([[1,2],[1,9]])
W=s.diag(V1,-V2)
u=s.Matrix([0,-3,6,-1]);v=s.Matrix([2,-1,0,1]);w=(u+v)/2
C=s.Matrix.hstack(w,v);C0=s.Matrix.hstack(u,v)
ck(C.T*W*C==s.zeros(2),'exact_matrix')
ck(C0.T*W*C0==s.zeros(2),'exact_matrix')
E=s.Matrix.hstack(w,v,s.eye(4)[:,1],s.eye(4)[:,2])
ck(abs(E.det())==1,'unimodular_completion')
ck(C*s.Matrix([[2,0],[-1,1]])==C0,'index_two_change')
ck(abs(s.Matrix([[2,0],[-1,1]]).det())==2,'index_two_change')
for den in range(2,9):
    for aa,bb in product(range(den),repeat=2):
        z=C*s.Matrix([s.Rational(aa,den),s.Rational(bb,den)])
        ck(all(t.q==1 for t in z)==(aa==bb==0),'saturation_residue_control')
for aa,bb in product(range(-10,11),repeat=2):
    z=C*s.Matrix([aa,bb]);coeff=s.Matrix([s.Rational(aa,2),bb+s.Rational(aa,2)])
    ck(C0*coeff==z,'printed_lattice_membership')
    ck(all(t.q==1 for t in coeff)==(int(z[0])%2==0),'printed_lattice_membership')

A=C[:2,:];B=C[2:,:];Q=B*A.inv()
ck(A.det()==B.det()==3,'projection_index')
ck(Q==s.Matrix([[-1,-2],[s.Rational(2,3),s.Rational(1,3)]]),'rational_isometry')
ck(Q.T*V2*Q==V1 and Q.det()==1,'rational_isometry')
for x,y in product(range(3),repeat=2):
    z=Q*s.Matrix([x,y])
    ck(all(t.q==1 for t in z)==((2*x+y)%3==0),'graph_domain_mod_three')
    if all(t.q==1 for t in z):ck(int(z[0])%3==0,'graph_image_mod_three')

a,b,c,d,t,z=s.symbols('a b c d t z')
P=s.Matrix([[a,b],[c,d]]);J=s.Matrix([[0,1],[-1,0]])
ck(s.simplify(P.T*J*P-P.det()*J)==s.zeros(2),'determinant_identity')
S1=V1+V1.T;S2=V2+V2.T
ck(S1.applyfunc(lambda a:a%3)==s.zeros(2),'local_rank_obstruction')
ck(S2.applyfunc(lambda a:a%3)==s.diag(2,0),'local_rank_obstruction')
for entries in product(range(3),repeat=4):
    Pm=s.Matrix(2,2,entries)
    if int(Pm.det())%3:
        R=(Pm.T*S2*Pm).applyfunc(lambda a:a%3)
        ck(R!=s.zeros(2),'finite_local_control')
for V in [V1,V2]:
    ck(s.expand((V-t*V.T).det())==7*t*t-13*t+7,'alexander_polynomial')
    ck((V-V.T).det()==1,'seifert_form')
ck(smith_normal_form(S1,domain=s.ZZ).applyfunc(abs)==s.diag(3,9),'smith_form')
ck(smith_normal_form(S2,domain=s.ZZ).applyfunc(abs)==s.diag(1,27),'smith_form')
Hr1=(1-z)*V1+(1-s.conjugate(z))*V1.T
Hr2=(1-z)*V2+(1-s.conjugate(z))*V2.T
ck(s.simplify(Q.T*Hr2*Q-Hr1)==s.zeros(2),'all_parameter_hermitian_identity')

# Symmetrized elementary S-enlargement adds a unimodular pair.
S=s.Matrix([[a,b],[b,c]]);q=s.Matrix([d,t])
enlarged=S.row_join(q).row_join(s.zeros(2,1))
enlarged=enlarged.col_join(s.Matrix([[d,t,2*z,1],[0,0,1,0]]))
T=s.eye(4);T[3,0]=-d;T[3,1]=-t
ck(s.simplify(T.T*enlarged*T-s.diag(S,s.Matrix([[2*z,1],[1,0]])))==s.zeros(4),
   's_equivalence_cokernel_preservation')
ck(T.det()==1 and s.Matrix([[2*z,1],[1,0]]).det()==-1,
   's_equivalence_cokernel_preservation')

# Prior-source control: different groups can have a metabolic difference pairing.
# Livingston v1 Theorem 10.7, not a new geometric assertion.
G=list(product(range(9),range(3),range(27)))
def pairing(x,y):return (15*x[0]*y[0]+18*x[1]*y[1]-2*x[2]*y[2])%27
for sign in [-1,1]:
    gens=[(0,sign%3,3),(3,0,0)]
    M={((3*j)%9,(sign*i)%3,(3*i)%27) for i,j in product(range(9),range(3))}
    ck(len(M)==27,'prior_linking_metabolizer')
    for x in G:
        ck(all(pairing(x,y)==0 for y in gens)==(x in M),'prior_linking_annihilator')
    for x in M:
        ck(all(pairing(x,y)==0 for y in M),'prior_linking_isotropy')

result={'all_pass':True,'assertions':sum(counts.values()),'counts':counts,
        'artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),
        'scope':'Exact saturation, rational isometry, local rank, S-equivalence cokernel and prior linking-form controls. No geometric concordance theorem.'}
(root/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
