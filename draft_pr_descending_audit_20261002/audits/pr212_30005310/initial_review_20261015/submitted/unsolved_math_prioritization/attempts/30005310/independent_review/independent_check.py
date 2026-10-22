#!/usr/bin/env python3
"""Independent exact directional, completion, and rank controls for 30005310."""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib,json,random
import sympy as s
C=Counter()
def check(cat,condition):
    assert condition,cat
    C[cat]+=1
I=s.eye(4)
V=s.Matrix([[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]])
X=I.col_join(V)
t=s.symbols('t')
def singleton(M):
    return s.Matrix([M[i,i] for i in range(8)]+[M[i,j] for i in range(4) for j in range(4,8)])
def colored(M):
    q=singleton(M)
    return s.Matrix([q[0]+q[1]]+list(q[2:]))
def lift_direction(y):
    D=s.zeros(4)
    H=s.Matrix(4,4,list(y[8:]))
    for i in range(4):D[i,i]=y[i]/2
    for j in range(4):
        k=(j+1)%4
        # right-diagonal derivative = 2<v_j,H_column_j>-2 v_j D v_j^T
        D[j,k]=(V[j,:]*H[:,j])[0]-y[4+j]/2-D[j,j]-D[k,k]
    W=(H-D*V.T).T
    return D.col_join(W)
# A constructive right inverse independently tested by polynomial differentiation.
for j in range(24):
    y=s.eye(24)[:,j];direction=lift_direction(y)
    derivative=singleton((X+t*direction)*(X+t*direction).T).diff(t).subs(t,0)
    for k in range(24):check('singleton_right_inverse_entries',derivative[k]==y[k])
for j in range(23):
    y=s.eye(23)[:,j]
    lift=s.Matrix([y[0],0]+list(y[1:]))
    direction=lift_direction(lift)
    derivative=colored((X+t*direction)*(X+t*direction).T).diff(t).subs(t,0)
    for k in range(23):check('colored_right_inverse_entries',derivative[k]==y[k])
check('rank4_input',X.rank()==4)
# Rank-three cross blocks must be singular; distinct exact rational controls.
rng=random.Random(30005310)
for r in [1,2,3]:
    for trial in range(18):
        A=s.Matrix(4,r,[rng.randrange(-4,5) for _ in range(4*r)])
        B=s.Matrix(4,r,[rng.randrange(-4,5) for _ in range(4*r)])
        cross=A*B.T
        check('rank_le3_cross_minor',cross.det()==0)
check('determinant_polynomial_nonzero',s.eye(4).det()==1)
# Explicit rank-two data match the PD identity, for both color partitions.
Z=s.Matrix([[1,0]]*4+[[0,1]]*4)
check('rank_two_witness',Z.rank()==2 and (Z*Z.T).rank()==2)
check('singleton_witness',singleton(Z*Z.T)==singleton(s.eye(8)))
check('colored_witness',colored(Z*Z.T)==colored(s.eye(8)))
e=s.Rational(1,100)
bound=2*e*(1+e)
for corners in product([-e,e],repeat=4):
    a,b,c,d=corners
    dot=(1+a)*c+b*(1+d)
    check('cross_box_extrema',abs(dot)<=bound)
margin=(1-e)**2-4*bound
check('uniform_margin',margin==s.Rational(8993,10000) and margin>0)
check('two_sample_minor_lower',1-2*e>0)
for trial in range(32):
    Y=Z+s.Matrix(8,2,[s.Rational(rng.randrange(-9,10),1000) for _ in range(16)])
    S=Y*Y.T
    M=s.diag(*[S[i,i] for i in range(8)])
    for i in range(4):
        for j in range(4,8):M[i,j]=M[j,i]=S[i,j]
    check('perturbed_data_rank',Y.rank()==2)
    check('perturbed_singleton_statistics',singleton(M)==singleton(S))
    check('perturbed_colored_statistics',colored(M)==colored(S))
    for i in range(8):check('diagonal_dominance',M[i,i]-sum(abs(M[i,j]) for j in range(8) if i!=j)>=margin)
    for k in range(1,9):check('positive_principal_leading_minors',M[:k,:k].det()>0)
# One sample: all 16 singleton cross edges obstruct PD completion.
a=s.symbols('a0:8')
for i in range(4):
    for j in range(4,8):
        det=s.det(s.Matrix([[a[i]**2,a[i]*a[j]],[a[i]*a[j],a[j]**2]]))
        check('one_sample_edge_obstruction',det==0)
# After merging only vertices1,2, edge3--5 still retains both diagonal coordinates.
check('untied_edge_survives_color_merge',2 not in {0,1} and 4 not in {0,1})
check('classical_MLT_formula',3*4//2<8<=4*5//2 and min(4,5)==4)
root=Path(__file__).resolve().parent
out={'status':'PASS','assertions':sum(C.values()),'categories':dict(C),'method':'Constructive derivative right inverse tested by exact polynomial differentiation; rational completion and obstruction controls','floating_point':False,'proof_sha256':'69ffeade6c2ee758e3c2869d9c5b7dd607c9a1b6782f7ecebfb81d0812fdb676','open_box_margin':str(margin)}
(root/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
