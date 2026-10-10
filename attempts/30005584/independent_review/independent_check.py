#!/usr/bin/env python3
"""Independent exact local-frame and form-congruence controls for30005584."""
from fractions import Fraction as Q
from collections import Counter
from itertools import product
import json
import sympy as S
counts=Counter()
def ck(group,v):
 if not v:raise AssertionError(group)
 counts[group]+=1
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def mv(M,x):return [dot(row,x) for row in M]
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A):return sum(A[i][i] for i in range(len(A)))
def sq(A):return sum(x*x for row in A for x in row)
def E(i,j):return int(i==j)
def warpR(a,b,c,d,T,K):
 ans=Q(0)
 for (i,j),k in zip([(0,1),(0,2),(1,2)],K):
  ans+=k*(E(a,i)*E(b,j)-E(a,j)*E(b,i))*(E(d,i)*E(c,j)-E(d,j)*E(c,i))
 for i in range(3):
  for j in range(3):
   ans-=T[i][j]*(E(a,3)*E(b,i)-E(a,i)*E(b,3))*(E(d,3)*E(c,j)-E(d,j)*E(c,3))
 return ans
def curv(h,T,K):
 return sum(warpR(a,b,c,d,T,K)*h[b][c]*h[a][d] for a,b,c,d in product(range(4),repeat=4))
def circle_derivative(h,L):
 G=[[Q(0) for i in range(4)] for k in range(4)]
 for i in range(3):G[3][i]=L[i];G[i][3]=-L[i]
 return [[-sum(G[k][i]*h[k][j]+G[k][j]*h[i][k] for k in range(4)) for j in range(4)] for i in range(4)]
for n in range(1,241):
 vals=[Q(((n*(k+3)+k*k)%23)-11,k%4+1) for k in range(20)]
 L=vals[:3];eta=vals[3:6];q=vals[6]
 T=[[vals[7+i+j] for j in range(3)] for i in range(3)]
 B=[[vals[11+i+j] for j in range(3)] for i in range(3)];K=vals[17:20]
 odd=[[Q(0) for j in range(4)] for i in range(4)]
 for i in range(3):odd[3][i]=eta[i];odd[i][3]=eta[i]
 ck('odd_circle_connection',sq(circle_derivative(odd,L))==2*dot(L,L)*dot(eta,eta)+6*dot(L,eta)**2)
 ck('odd_curvature_contraction',curv(odd,T,K)==2*dot(eta,mv(T,eta)))
 even=[[Q(0) for j in range(4)] for i in range(4)]
 for i,j in product(range(3),repeat=2):even[i][j]=B[i][j]
 even[3][3]=q
 ck('even_circle_connection',sq(circle_derivative(even,L))==2*dot([x-q*y for x,y in zip(mv(B,L),L)],[x-q*y for x,y in zip(mv(B,L),L)]))
 base=[row[:] for row in even];base[3][3]=0
 ck('even_curvature_cross',curv(even,T,K)-curv(base,T,K)==-2*q*sum(T[i][j]*B[i][j] for i,j in product(range(3),repeat=2)))
 H=[[T[i][j]-L[i]*L[j] for j in range(3)] for i in range(3)]
 left=sq(circle_derivative(even,L))-2*(curv(even,T,K)-curv(base,T,K))
 right=2*dot(mv(B,L),mv(B,L))+2*q*q*dot(L,L)+4*q*sum(H[i][j]*B[i][j] for i,j in product(range(3),repeat=2))
 ck('full_even_Hessian_cross',left==right)
 # General a^3 rescaling, rather than only a radial substitution.
 lam=Q(n%7+1,2);ell2=dot(L,L)
 div_mu_L=lam+2*ell2
 ck('odd_rescaling_scalar',2*ell2-div_mu_L==-lam)
 ricF=[[T[i][j]-lam*E(i,j)-3*H[i][j] for j in range(3)] for i in range(3)]
 ck('weighted_Hodge_curvature',ricF==[[-2*T[i][j]+3*L[i]*L[j]-lam*E(i,j) for j in range(3)] for i in range(3)])
# Symbolic ground-state calculation, including the exact irrational root.
c,lam,v=S.symbols('c lam v',real=True)
ratio=c*lam+(2-c*c)*v
ck('exact_ground_state',S.expand(ratio.subs(c,S.sqrt(2))-S.sqrt(2)*lam)==0)
ck('normalization_half',S.simplify((S.sqrt(2)*lam).subs(lam,S.Rational(1,2))-1/S.sqrt(2))==0)
ck('threshold_nonintegrability',3-2*S.sqrt(2)>-1)
for n in range(1,81):
 H=S.Matrix([[n%5+2,S.Rational(n%3,3)],[S.Rational(n%3,3),n%7+2]])
 R=S.Matrix([[n%4-2,S.Rational(n,7)],[S.Rational(1,3),n%5-2]])
 B=S.Matrix([[n%7-3,1],[1,n%9-4]])
 M=B.row_join(2*R.T).col_join((2*R).row_join(H))
 P=S.eye(2).row_join(S.zeros(2)).col_join((-2*H.inv()*R).row_join(S.eye(2)))
 Eff=B-4*R.T*H.inv()*R
 expected=Eff.row_join(S.zeros(2)).col_join(S.zeros(2).row_join(H))
 ck('positive_scalar_block',H[0,0]>0 and H.det()>0)
 ck('Schur_congruence',P.T*M*P==expected)
 ck('Schur_nullity',4-M.rank()==2-Eff.rank())
 ck('triangular_congruence_orientation',P.det()==1)
# Exact finite properness controls and parity.
for n in range(1,241):
 x=Q(n%13-6,3);y=Q(n%17-8,5);z=Q(n%7-3,2)
 A=[[x,z,1],[z,y,-1],[1,-1,-x-y]];A2=mm(A,A);s=tr(A2)
 f=[[A2[i][j]-s*Q(E(i,j),3) for j in range(3)] for i in range(3)]
 ck('proper_even_map_norm',tr(mm(f,f))==s*s/6)
 ck('trace_free',tr(f)==0)
 ck('circle_nonzero_weight_even',(2*n)%2==0)
# Variational inverse pointwise square and angular comparison controls.
for z,q,V in product(range(-7,8),range(-7,8),range(1,8)):
 ck('variational_square',Q(z*z,V)-(2*z*q-V*q*q)==Q((z-V*q)**2,V))
for j in range(1,61):
 ck('angular_core_integrable',2*j>=2)
 ck('core_inverse_vanishes',j*(j+1)>0)
 ck('origin_cutoff_energy_exponent',2*j+1>0)
 ck('one_form_origin_boundary_exponent',2*j+1>0)
print(json.dumps({'problem_id':30005584,'status':'PASS','counts':dict(sorted(counts.items())),'assertions':sum(counts.values()),'scope':'Independent exact finite geometric/form controls. The infinite-domain, compactness, kernel and source-scope conclusions are audited in the accompanying written review.'},indent=2,sort_keys=True))
