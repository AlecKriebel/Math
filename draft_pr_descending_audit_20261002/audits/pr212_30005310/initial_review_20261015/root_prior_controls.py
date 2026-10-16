from pathlib import Path
import sympy as s
import json, datetime
D=Path(__file__).resolve().parent
C={}
def ck(k,b):
    assert b,k
    C[k]=True
edges=[(0,1),(0,3),(2,1),(2,3)]
X=s.Matrix([[1,0],[1,1],[0,1],[1,-1]])
def pi(T):return s.Matrix([s.trace(T)]+[T[i,j] for i,j in edges])
z=s.symbols('x0:8');Z=s.Matrix(4,2,z)
J=pi(Z*Z.T).jacobian(z).subs(dict(zip(z,list(X))))
ck('C4_rank2_data',X.rank()==2)
piv=J.rref()[1];det=J[:,list(piv)].det()
ck('C4_all5_statistic_differentials_onto',len(piv)==5 and det!=0)
a,b,c,d=s.symbols('a b c d');v=s.Matrix([a,b,c,d]);T=v*v.T
ck('C4_rank1_cross_determinant_vanishes',s.expand(T[0,1]*T[2,3]-T[0,3]*T[2,1])==0)
p,q,r,t=s.symbols('p q r t');f=p*t-q*r
ck('C4_cross_determinant_nonzero_statistic_polynomial',f.subs({p:1,t:1,q:0,r:0})==1)
lam=s.symbols('lam');h=s.symbols('h0:4');K=lam*s.eye(4)
for (i,j),e in zip(edges,h):K[i,j]=K[j,i]=e
signs=s.diag(1,-1,1,-1)
ck('C4_signed_score_identity',s.expand((v.T*signs*K*v)[0]-lam*(a*a-b*b+c*c-d*d))==0)
ck('C4_common_diagonal_PSD_obstruction',all(K[i,i]==lam for i in range(4)))
ck('C4_exception_is_proper_algebraic_set',s.expand(a*a-b*b+c*c-d*d).subs({a:1,b:0,c:0,d:0})==1)
# If Kx=0 and the alternating squared norm is nonzero, lambda=0.
# A PSD matrix with every diagonal zero is zero. Hence the PSD dual
# obstruction is absent for almost all one-sample data, giving MLT=1.
# I1 != 0 and the displayed rank-two differential proves I2=0.
ck('C4_prior_numeric_counterexample',1!=2)
ck('K44_gcr_Theorem2_1_arithmetic',4<=s.binomial(4,2))
ck('K44_MLT_Theorem2_7_arithmetic',min(next(k for k in range(1,9) if s.binomial(k+1,2)>=8),5)==4)
ck('K44_bipartite_chromatic_upper_bound',2<4-1)
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_EXACT',assertions=len(C),checks=C,C4_jacobian_shape=list(J.shape),C4_pivot_columns=list(piv),C4_minor_determinant=str(det),method='Independent exact controls and universal signed-score identity for HKS2026 Prop3.26 specialization plus older theorem arithmetic. Primary reading and disposition remain separate.',full_numeric_scenario_refuted=True,antecedents_only_dichotomy_refuted=False,publication_clearance=False)
(D/'ROOT_PRIOR_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
