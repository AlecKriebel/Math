"""Exact nontrivial projection models for the Helmholtz/scalar comparison.
Finite controls supplement the functional analytic proof in TURN_5.md.
"""
import sympy as s,json
from collections import Counter
C=Counter()
def ck(p,k):assert p,k;C[k]+=1
for m in range(2,6):
 n=m+2
 D=s.zeros(m,n)
 for i in range(m):D[i,i]=i+1;D[i,n-2]=s.Rational(i+1,3);D[i,n-1]=s.Rational((-1)**i,4)
 G=D.T;S=D*G
 E=s.zeros(n,m-1)
 for i in range(m-1):E[i,i]=1;E[n-1,i]=s.Rational(i+1,5)
 B=D*E;M=E.T*E;P=B*(B.T*B).inv()*B.T
 R=E*(B.T*B).inv()*B.T
 CR2=s.trace(R.T*R)
 f=s.Matrix(range(1,m+1));u=S.inv()*f;true=G*u
 for coarse in [s.zeros(m,1),u,s.Matrix([(-1)**i*(i+2) for i in range(m)])]:
  for delta in [s.Rational(1,7),s.Integer(1),s.Integer(11)]:
   coeff=(B.T*B+delta*M).inv()*B.T*(f+delta*coarse)
   flux=E*coeff;w=S.inv()*D*flux;xi=flux-G*w
   q=P*coarse+(P*f-D*flux)/delta;eps=q-P*w;e=w-u
   ck(D*xi==s.zeros(m,1),'actual_divergence_free_Helmholtz_part')
   ck(G.T*xi==s.zeros(m,1),'orthogonal_Helmholtz_part')
   ck(P*eps==eps,'recovered_scalar_error_in_projected_space')
   ck(B.T*eps==E.T*xi,'exact_recovered_scalar_comparison')
   ck(eps.dot(eps)<=CR2*xi.dot(xi),'uniform_lift_scalar_bound')
   ck(S*e+delta*P*e==(P*f-f)+delta*P*(coarse-u)-delta*eps,'projected_reaction_error_signs')
   ck((true-flux).dot(true-flux)==(e.T*S*e)[0]+xi.dot(xi),'exact_flux_error_orthogonal_sum')
   residual=P*f-f;dual2=(residual.T*S.inv()*residual)[0]
   energy=(e.T*S*e)[0]+delta*(P*e).dot(P*e)
   ck(energy<=3*(dual2+delta*(coarse-u).dot(coarse-u)+delta*eps.dot(eps)),'squared_energy_majorant')
# Coarse mesh-power comparison, retaining distinct cell/edge sizes.
for N in range(1,9):
 H=[s.Rational(1,i+1) for i in range(N)];J=[s.Rational(i+1,3) for i in range(N)]
 volume=[s.Rational(2*i+1,5) for i in range(N)]
 rho=sum(h*h*v+h*j for h,v,j in zip(H,volume,J))
 rho2=sum(h**4*v+h**3*j for h,v,j in zip(H,volume,J))
 ck(rho2<=max(H)**2*rho,'higher_order_primary_mesh_factor')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Exact projection/Hodge models and mesh-power bookkeeping. No PDE reliability, elliptic regularity, or adaptive convergence theorem is inferred from finite models.'},indent=2,sort_keys=True))
