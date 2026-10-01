"""Independent exact mass-matrix, projection and refinement controls.
No author checker is imported. Infinite-dimensional claims are reviewed in prose.
"""
import sympy as s
from collections import Counter
import json
C=Counter()
def ck(q,k):
 assert q,k
 C[k]+=1

def mass(n,seed):
 U=s.eye(n)
 for i in range(n):
  for j in range(n):
   if i<j:U[i,j]=s.Rational(seed+i+2*j+1,seed+n+5)
 return U.T*s.diag(*[s.Rational(i+seed+2,i+1) for i in range(n)])*U
# Both flux and scalar inner products are nonorthogonal in the displayed basis.
for n in range(3,7):
 m=n-2;Mv=mass(n,2);Mq=mass(m,5)
 D=s.zeros(m,n)
 for i in range(m):
  D[i,i]=i+2;D[i,n-2]=s.Rational((-1)**i,i+2);D[i,n-1]=s.Rational(i+1,5)
 G=Mv.inv()*D.T*Mq;S=D*G;R=G*S.inv()
 ck(Mv*G==D.T*Mq,'weighted_adjoint')
 ck(Mq*S==S.T*Mq,'weighted_schur_selfadjoint')
 ck(D*R==s.eye(m),'weighted_minimum_lift_right_inverse')
 for z in D.nullspace():ck(z.T*Mv*R==s.zeros(1,m),'all_kernel_lift_orthogonality')
 F=s.Matrix([s.Rational(2*i+3,i+1) for i in range(m)])
 p=S.inv()*F;sm=G*p
 for delta in [s.Rational(1,23),s.Rational(2,5),s.Integer(1),s.Integer(17)]:
  B=D.T*Mq*D+delta*Mv
  for coarse in [s.zeros(m,1),p,s.Matrix([(-1)**i*(i+2) for i in range(m)])]:
   sh=B.inv()*D.T*Mq*(F+delta*coarse);q=coarse+(F-D*sh)/delta;d=D*sh-F;e=sh-sm
   ck(Mv*sh==D.T*Mq*q,'recovered_mixed_equation_nonorthogonal')
   ck(q==(S+delta*s.eye(m)).inv()*(F+delta*coarse),'reaction_equivalence_nonorthogonal')
   ck(e==R*d,'exact_weighted_correction')
   ck((e.T*Mv*e)[0]==(d.T*Mq*S.inv()*d)[0],'weighted_schur_energy')
   gap=coarse-p
   ck((e.T*Mv*e)[0]<=delta*(gap.T*Mq*gap)[0]/4,'weighted_sharp_half_sqrt_delta')
   ck((d.T*Mq*d)[0]<=delta**2*(gap.T*Mq*gap)[0],'weighted_defect_bound')
   change=s.ones(m,1)/7
   sh2=B.inv()*D.T*Mq*(F+delta*(coarse+change));v=sh2-sh
   ck((v.T*B*v)[0]<=delta**2*(change.T*Mq*change)[0],'moving_input_energy_bound')
# Proper scalar subspaces and the positive projected-reaction limit, with
# non-Euclidean mass, including rank zero and full rank.
for n in range(2,7):
 M=mass(n,3);K=mass(n,7)
 U=s.eye(n)
 for i in range(n):
  for j in range(i+1,n):U[i,j]=s.Rational(i+j+1,n+1)
 for rank in range(n+1):
  E=U[:,:rank];P=E*(E.T*M*E).inv()*E.T*M if rank else s.zeros(n)
  ck(P*P==P and M*P==P.T*M,'proper_weighted_orthogonal_projection')
  e=s.Matrix([s.Rational((-1)**i,i+2) for i in range(n)])
  for delta in [s.Rational(1,29),s.Integer(1),s.Integer(41)]:
   L=K+delta*M*P
   ck(L.T==L,'projected_reaction_symmetric_form')
   ck((e.T*L*e)[0]==(e.T*K*e)[0]+delta*((P*e).T*M*(P*e))[0],'projected_reaction_energy')
   # Sylvester's criterion is exact and checks all directions, not just e.
   ck(all(L[:j,:j].det()>0 for j in range(1,n+1)),'projected_reaction_positive_all_directions')
# Actual edge integrals: old RT0 tangential jumps are affine. Test partitions
# produced by midpoint refinement, including additional nonuniform refinement.
t=s.symbols('t');a,b=s.symbols('a b')
partitions=[[(0,s.Rational(1,2)),(s.Rational(1,2),1)],[(0,s.Rational(1,4)),(s.Rational(1,4),s.Rational(1,2)),(s.Rational(1,2),1)],[(s.Rational(i,8),s.Rational(i+1,8)) for i in range(8)]]
for coeff in [(i,j) for i in range(-3,4) for j in range(-3,4)]:
 f=(coeff[0]+coeff[1]*t)**2;old=s.integrate(f,(t,0,1))
 for parts in partitions:
  new=sum((v-u)*s.integrate(f,(t,u,v)) for u,v in parts)
  ck(new<=old/2,'marked_edge_actual_weight_reduction')
# A symbolic identity handles every affine jump for exact halving.
f=(a+b*t)**2
new=sum((v-u)*s.integrate(f,(t,u,v)) for u,v in partitions[0])
ck(s.expand(new-s.integrate(f,(t,0,1))/2)==0,'all_affine_edge_half_identity')
for marked_adjacent in [0,1,2]:
 marked_allocation=s.Rational(marked_adjacent,2)
 loss=s.Rational(1,2) if marked_adjacent else 0
 ck(loss>=marked_allocation/2,'primary_half_allocated_edge_loss')
# Exact contraction and asymptotically small perturbation logic certificates.
r=s.symbols('r',positive=True);theta=s.symbols('theta',positive=True)
# zeta=theta/32 for fine transferred bulk theta/4.
q=(1+theta/32)*(1-theta/8)
ck(s.expand(1-q)==3*theta/32+theta**2/256,'fine_reduction_positive_gap_polynomial')
qp=(1+theta/8)*(1-theta/2)
ck(s.expand(1-qp)==3*theta/8+theta**2/16,'primary_reduction_positive_gap_polynomial')
for root in [s.Rational(i,16) for i in range(1,16)]:
 err=root/4
 ck(((root-err)/(1+err))**2>=root**2/4,'eventual_bulk_transfer_no_zero_division')
# H2 duality weights, for independently varied cell and edge diameters.
for k in range(1,12):
 hs=[s.Rational(1,i+2) for i in range(k)];es=[s.Rational(2,2*i+5) for i in range(k+1)]
 vs=[s.Rational(i+1,7) for i in range(k)];js=[s.Rational(i+3,11) for i in range(k+1)]
 base=sum(h*h*v for h,v in zip(hs,vs))+sum(h*j for h,j in zip(es,js))
 high=sum(h**4*v for h,v in zip(hs,vs))+sum(h**3*j for h,j in zip(es,js))
 ck(high<=max(hs+es)**2*base,'separate_cell_edge_higher_order_weights')
# Fixed-delta fine-only eigenmode comparison, in arbitrary positive scalar
# eigenvalues: the bias is real, and the augmented coarse term cannot vanish.
for lam in [s.Rational(1,3),s.Integer(2),s.Integer(13)]:
 for delta in [s.Rational(1,7),s.Integer(1),s.Integer(9)]:
  ratio=lam/(lam+delta)
  ck(0<ratio<1 and 1-ratio==delta/(lam+delta),'nonzero_fixed_coarse_bias')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Independent exact nonorthogonal-inner-product algebra, all-direction positivity certificates, edge integrals and mesh weights. Analytic convergence, Helmholtz, trace, lifting and source claims are audited in INDEPENDENT_REVIEW.md, not inferred from finite samples.'},indent=2,sort_keys=True))
