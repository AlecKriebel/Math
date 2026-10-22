"""Exact controls for the fixed-delta limit identification and mesh reductions."""
import sympy as s,json
from collections import Counter
C=Counter()
def ck(x,k):assert x,k;C[k]+=1
# Arbitrary rational orthogonal projections, including proper subspaces.
for n in range(2,8):
 U=s.eye(n)
 for i in range(n):
  for j in range(i+1,n):U[i,j]=s.Rational(i+j+1,n+2)
 A=U.T*U+s.eye(n)
 for rank in range(n+1):
  B=U[:,:rank]
  P=B*(B.T*B).inv()*B.T if rank else s.zeros(n)
  ck(P.T==P and P*P==P,'orthogonal_projection_identity')
  for d in [s.Rational(1,5),s.Integer(1),s.Integer(7)]:
   K=A+d*P
   ck(K.det()>0,'positive_projected_reaction_matrix')
   e=s.Matrix([(-1)**i*s.Rational(i+1,n) for i in range(n)])
   ck((e.T*K*e)[0]==(e.T*A*e)[0]+d*(P*e).dot(P*e),'projected_reaction_energy_identity')
   ck((e.T*K*e)[0]>0,'no_nonzero_limit_error')
   u=s.Matrix(range(1,n+1));w=u+e;q=P*w
   div=f=A*u
   # limit equations: div(sigma_inf)=f-d*P(w-u), sigma_inf=-grad(w)
   residual=A*w-(f-d*P*(w-u))
   ck(residual==K*e,'limit_equation_sign')
# Marked primary cell volume and edge allocations. The loss of each marked
# edge is at least half its full contribution and therefore at least half the
# total contribution allocated to its marked adjacent cells.
for marked_sides in [0,1,2]:
 allocation=s.Rational(marked_sides,2)
 loss=s.Rational(1,2) if marked_sides else 0
 ck(loss>=allocation/2,'edge_half_allocation_reduction')
ck(1-s.Rational(1,4)>=s.Rational(1,2),'marked_cell_volume_reduction')
for theta in [s.Rational(1,10),s.Rational(1,3),s.Rational(2,3),s.Rational(9,10)]:
 zeta=theta/8;q=(1+zeta)*(1-theta/2)
 ck(0<q<1,'primary_and_fine_recursion_contraction')
# Independent exact fixed-delta moving-input stability in Euclidean models.
for n in range(2,7):
 B=s.Matrix([[1 if j==i else s.Rational(1,3) if j==n-1 else 0 for j in range(n)] for i in range(n-1)])
 M=s.eye(n);f=s.Matrix(range(1,n));u=s.Matrix([s.Rational(i+1,7) for i in range(n-1)])
 for d in [s.Rational(1,4),s.Integer(1),s.Integer(3)]:
  H=B.T*B+d*M;z=H.inv()*B.T*(f+d*u)
  perturb=s.Matrix([s.Rational((-1)**i,5) for i in range(n-1)])
  v=H.inv()*B.T*(f+d*(u+perturb));e=v-z
  ck((e.T*H*e)[0]<=d*d*perturb.dot(perturb),'moving_input_Bdelta_stability')
  recovered=u+perturb+(f-B*v)/d
  ck(v-B.T*recovered==s.zeros(n,1),'recovered_first_mixed_equation')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Finite exact positivity, projection/sign, mesh-weight and moving-input identities. The infinite-dimensional fixed-parameter convergence theorem rests on TURN_4.md.'},indent=2,sort_keys=True))
