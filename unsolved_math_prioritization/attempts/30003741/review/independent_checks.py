#!/usr/bin/env python3
"""Independent receptor linear-algebra elimination and exact Sturm controls."""
from pathlib import Path
from itertools import product
import hashlib,json
import sympy as s
counts={}
def ck(name,ok):
    assert bool(ok),name
    counts[name]=counts.get(name,0)+1
u,v,t=s.symbols('u v t')
# The negative of the original receptor coefficient matrix with phi=1.
# Binding contributes the inhomogeneous source v*sigma in its first row.
def receptor_matrix(N,u,v):
    B=s.zeros(N+1)
    B[0,0]=1+v
    for j in range(1,N):B[j,j]=1+u
    B[N,N]=u
    for j in range(N):B[j,j+1]=-(u-v)
    for j in range(1,N+1):B[j,j-1]=-1
    return B

P=[s.S.One,u];D=[s.S.One,1+u]
for m in range(2,13):
    P.append(s.expand(u*P[-1]+v*D[-2]));D.append(s.expand(D[-1]+P[-1]))
for N in range(1,8):
    B=receptor_matrix(N,u,v)
    ck('original_matrix_determinant',s.expand(B.det(method='domain-ge')-v*D[N])==0)
    ck('original_C1_cofactor',s.expand(B.cofactor(0,1)-P[N-1])==0)
    ck('matrix_column_balance',all(s.expand(sum(B[i,j] for i in range(N+1))-v)==0 for j in range(N+1)))
for m in range(2,13):
    ck('equivalent_second_order_recurrence',s.expand(P[m]-(1+u)*P[m-1]+(u-v)*P[m-2])==0)

# Direct rational linear solves are independent of the submitted tail-recurrence
# evaluator and test all original receptor equations at the reconstruction.
parameter_sets=[(s.Rational(1,5000),s.Rational(1,10000)),(s.Rational(5,3),s.Rational(1,7)),(s.Rational(11,8),s.Rational(2,3))]
linear_solves=0
for N in range(1,11):
    for dd,vv in parameter_sets:
        for tt in (s.Rational(1,10),s.Rational(2,3),s.Rational(5)):
            sigma=s.Rational(3,7);hh=s.Rational(11);AA=s.Rational(5,4)
            freeL=s.Rational(4,5);freeR=s.Rational(6,5);L=sigma+freeL;R=sigma+freeR
            kap=vv*sigma/(freeL*freeR)
            B=receptor_matrix(N,dd+tt,vv);rhs=s.zeros(N+1,1);rhs[0]=vv*sigma
            C=B.inv()*rhs;linear_solves+=1
            denominator=D[N].subs({u:dd+tt,v:vv})
            expected=s.Matrix([sigma*P[N-j].subs({u:dd+tt,v:vv})/denominator for j in range(N+1)])
            ck('direct_reconstruction',C==expected)
            ck('fixed_total_class',sum(C)==sigma and L-sum(C)==freeL and R-sum(C)==freeR)
            ck('physical_concentrations',all(x>0 for x in C) and 0<tt<hh and dd>vv>0)
            ck('binding_balance',kap*(L-sum(C))*(R-sum(C))-vv*sum(C)==0)
            ck('original_receptor_residuals',B*C==rhs)
            F=tt*denominator-AA*(hh-tt)*P[N-1].subs({u:dd+tt,v:vv})
            # beta=gamma=phi=1 and alpha=A/sigma.
            ck('phosphatase_residual',s.simplify(AA/sigma*C[1]*(hh-tt)-tt+F/denominator)==0)

# Exhaust every possible zero/nonzero coefficient-sign pattern consistent with
# the analytic leading/constant restrictions for low N; the unrestricted proof
# is the parity/sign-change argument in REVIEW.md.
for N in range(1,10):
    bound=N if N%2 else N-1
    for middle in product((-1,0,1),repeat=N-1):
        seq=[-1]+list(middle)+[1,1]
        seq=[x for x in seq if x]
        changes=sum(x!=y for x,y in zip(seq,seq[1:]))
        ck('parity_sign_bound',changes%2==1 and changes<=bound)

# Recover the N=4 polynomial directly from the original receptor matrix and
# Cramer's rule, without using P or D to construct it.
vv=s.Rational(1,10000);dd=s.Rational(1,5000);sigma=s.Rational(1,2)
B=receptor_matrix(4,t+dd,vv)
detB=s.expand(B.det(method='domain-ge'));cofactor=s.expand(B.cofactor(0,1))
scale=s.Integer(625000000000000)
Q=s.Poly(s.expand(scale/vv*(t*detB-(20-t)*vv*sigma*cofactor)),t)
expected=[625000000000000,938000000000000,-5624249850000000,621812687520000,624093093765001,-625250050000]
ck('independent_integer_polynomial',Q.all_coeffs()==expected)
points=[s.S.Zero,s.Rational(1,100),s.S.One,s.Integer(3)]
values=[-625250050000,s.Rational(567224734905201,100),-2815969318764999,83466222268925003]
for x,y in zip(points,values):ck('exact_witness_signs',Q.eval(x)==y)
ck('Sturm_total_positive',Q.count_roots(0,s.oo)==3)
ck('Sturm_physical',Q.count_roots(0,20)==3)
ck('Sturm_no_unphysical_positive',Q.count_roots(20,s.oo)==0)
for l,r in zip(points,points[1:]):ck('Sturm_brackets',Q.count_roots(l,r)==1)
ck('simple_scalar_roots',s.gcd(Q,Q.diff()).degree()==0)
ck('binding_root',s.Rational(1,5000)*(1-sigma)**2-vv*sigma==0)
# Entire reconstruction in the quotient by Q: receptor residuals vanish
# identically, and the cleared phosphatase numerator is exactly a multiple of Q.
C=s.Matrix([s.cancel(vv*sigma*B.cofactor(0,j)/detB) for j in range(5)])
rhs=s.Matrix([vv*sigma,0,0,0,0])
for z in B*C-rhs:ck('witness_symbolic_receptor',s.cancel(z)==0)
ck('witness_symbolic_total',s.cancel(sum(C)-sigma)==0)
ck('witness_scalar_ideal',s.cancel((C[1]*(20-t)-t)*detB+vv*Q.as_expr()/scale)==0)
for x in points[1:]:
    evaluated=[z.subs(t,x) for z in C]
    ck('witness_positive_bracket_data',all(z>0 for z in evaluated) and sum(evaluated)==sigma and 20-x>0)

root=Path(__file__).parent
out={'problem_id':30003741,'status':'PASS_INDEPENDENT_LINEAR_ALGEBRA_AND_STURM_CHECKS','assertions':sum(counts.values()),'groups':counts,
     'direct_rational_linear_solves':linear_solves,'positive_roots_by_Sturm':3,'physical_roots_by_Sturm':3,
     'artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL.md').read_bytes()).hexdigest(),
     'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'scope':'Exact agonist-only equilibrium reduction, all-parameter written parity bound and sharp N=4 witness. No higher-N three-root ceiling, stability, clinical relevance or two-ligand theorem is established.'}
print(json.dumps(out,indent=2,sort_keys=True))
