#!/usr/bin/env python3
"""Independent exact-rational diagnostics; no deposited program or dependency used."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import datetime, json

E = Path(__file__).resolve().parent

def clean(p): return {m:F(v) for m,v in p.items() if v}
def con(v,d=2): return {(0,)*d:F(v)} if v else {}
def var(i,d=2): return {tuple(int(j==i) for j in range(d)):F(1)}
def add(*ps):
 r={}
 for p in ps:
  for m,v in p.items():r[m]=r.get(m,F(0))+v
 return clean(r)
def scale(p,s): return clean({m:v*s for m,v in p.items()})
def mul(p,q):
 r={}
 for a,v in p.items():
  for b,w in q.items():
   m=tuple(x+y for x,y in zip(a,b));r[m]=r.get(m,F(0))+v*w
 return clean(r)
def powp(p,n):
 r=con(1,len(next(iter(p), (0,0))))
 for _ in range(n):r=mul(r,p)
 return r
def diff(p,i):
 r={}
 for m,v in p.items():
  if m[i]:
   mm=list(m);mm[i]-=1;r[tuple(mm)]=v*m[i]
 return clean(r)
def d0(p,*ix):
 for i in ix:p=diff(p,i)
 return p.get((0,)*len(next(iter(p),(0,0))),F(0))
def eq(p,q):return not add(p,scale(q,-1))

def coordinate_checks():
 y=[var(0),var(1)];G=[[F(2),F(1,3)],[F(1,3),F(3)]]
 dg=[[[F(2+i+j+2*k,7) for k in range(2)] for j in range(2)] for i in range(2)]
 cv=[F(2,5),F(-3,7),F(4,9),F(-1,2)]
 C=lambda i,j,k:cv[i+j+k]
 Q=lambda i,j,k:(dg[j][k][i]+dg[i][k][j]+dg[i][j][k]-C(i,j,k))/2
 Gamma=lambda i,j,k:(dg[j][k][i]+dg[i][k][j]-dg[i][j][k]-C(i,j,k))/2
 checks=[]
 for a,b,c in [(F(1,2),F(2,3),F(-1,4)),(F(-2),F(5,7),F(3,2)),(F(0),F(1),F(0))]:
  x=[add(y[0],scale(powp(y[0],2),a),mul(y[0],y[1]),scale(powp(y[1],3),F(5,6))),add(y[1],scale(powp(y[0],2),b),scale(powp(y[1],2),c))]
  q={}
  for i,j in product(range(2),repeat=2):q=add(q,scale(mul(x[i],x[j]),G[i][j]/2))
  for i,j,k in product(range(2),repeat=3):q=add(q,scale(mul(mul(x[i],x[j]),x[k]),Q(i,j,k)/6))
  gp={}
  for i,j in product(range(2),repeat=2):
   z={}
   for r,s in product(range(2),repeat=2):
    old=add(con(G[r][s]),*[scale(x[k],dg[r][s][k]) for k in range(2)])
    z=add(z,mul(mul(diff(x[r],i),diff(x[s],j)),old))
   gp[i,j]=z
  tensor_wrong_detected=False
  for i,j,k in product(range(2),repeat=3):
   qp=d0(q,i,j,k)
   connection=Gamma(i,j,k)+sum(d0(x[r],i,j)*G[r][k] for r in range(2))
   target=d0(gp[i,j],k)+connection
   direct=Q(i,j,k)+sum(G[r][k]*d0(x[r],i,j)+G[r][j]*d0(x[r],i,k)+G[r][i]*d0(x[r],j,k) for r in range(2))
   assert qp==target==direct
   tensor_wrong_detected|=qp!=Q(i,j,k)
  assert tensor_wrong_detected
  checks.append({'coordinate_second_jet':[str(a),str(b),str(c)],'eight_ordered_third_components_match':True,'incorrect_tensor_rule_rejected':True})
 return checks

def scalar_lift_checks():
 t=var(0,1);one=con(1,1)
 g=add(one,powp(t,2));C=add(powp(t,3),scale(powp(t,2),2),one)
 Q=add(scale(diff(g,0),F(3,2)),scale(C,F(-1,2)))
 a=[add(scale(mul(g,powp(t,2)),F(1,2)),scale(mul(Q,powp(t,3)),F(-1,6))),add(scale(mul(g,t),-1),scale(mul(Q,powp(t,2)),F(1,2))),add(scale(g,F(1,2)),scale(mul(Q,t),F(-1,2))),scale(Q,F(1,6))]
 f=[one,t,powp(t,2),powp(t,3)]
 def pair(xs,ys):return add(*[mul(x,y) for x,y in zip(xs,ys)])
 df=[diff(x,0) for x in f];ddf=[diff(x,0) for x in df];dddf=[diff(x,0) for x in ddf]
 assert eq(pair(a,f),{}) and eq(pair(a,df),{}) and eq(pair(a,ddf),g) and eq(pair(a,dddf),Q)
 dphi=[scale(diff(x,0),-1) for x in a]
 Gamma=add(scale(diff(g,0),F(1,2)),scale(C,F(-1,2)))
 assert eq(pair(df,dphi),g) and eq(pair(ddf,dphi),Gamma)
 assert not eq(pair(df,[diff(x,0) for x in a]),g)
 return {'base_domain':'all real t','metric':'1+t^2>0','cubic':'t^3+2t^2+1','jet_identity_polynomials':4,'metric_and_ordered_connection_polynomials':2,'wrong_phi_sign_rejected':True,'coefficients_can_grow':True}

def transpose(A):return [list(x) for x in zip(*A)]
def mm(A,B):return [[sum(a*b for a,b in zip(r,c)) for c in zip(*B)] for r in A]
def inv(A):
 n=len(A);R=[[F(v) for v in A[i]]+[F(i==j) for j in range(n)] for i in range(n)]
 for i in range(n):
  k=next(k for k in range(i,n) if R[k][i]);R[i],R[k]=R[k],R[i];z=R[i][i];R[i]=[v/z for v in R[i]]
  for j in range(n):
   if j!=i:z=R[j][i];R[j]=[v-z*w for v,w in zip(R[j],R[i])]
 return [r[n:] for r in R]
def det(A):
 if not A:return F(1)
 R=[list(r) for r in A];ans=F(1);n=len(R)
 for i in range(n):
  k=next((k for k in range(i,n) if R[k][i]),None)
  if k is None:return F(0)
  if k!=i:R[i],R[k]=R[k],R[i];ans=-ans
  p=R[i][i];ans*=p
  for j in range(i+1,n):
   z=R[j][i]/p
   for k in range(i+1,n):R[j][k]-=z*R[i][k]
 return ans
def positive(A):return all(det([r[:k] for r in A[:k]])>0 for k in range(1,len(A)+1))
def psd(A):return all(det([[A[i][j] for j in ids] for i in ids])>=0 for k in range(1,len(A)+1) for ids in combinations(range(len(A)),k))

def schur_checks():
 count=0
 for n,m,k in product(range(1,4),range(1,4),[-12,0,12]):
  S=[[F(1) if i==j else F(i+j+1,7) if j>i else F(0) for j in range(n)] for i in range(n)]
  D=[[F(10)**(k*(i+1)) if i==j else F(0) for j in range(n)] for i in range(n)]
  A=mm(mm(transpose(S),D),S);Ai=inv(A);assert positive(A)
  for factor in [F(0),F(10)**12]:
   B=[[factor*F((-1)**(i+j)*(i+2*j+1),3) for j in range(m)] for i in range(n)]
   norm=sum(v*v for r in B for v in r);t=sum(Ai[i][i] for i in range(n))*norm;lam=1+t;M=mm(mm(transpose(B),Ai),B)
   assert psd([[t*F(i==j)-M[i][j] for j in range(m)] for i in range(m)])
   H=[A[i]+B[i] for i in range(n)]+[transpose(B)[j]+[2*lam*F(i==j) for i in range(m)] for j in range(m)]
   assert positive(H);count+=1
 assert det([[F(1),F(3)],[F(3),F(2)]])<0
 return {'exact_positive_block_cases':count,'smallest_diagonal_input':'10^-36','largest_B_factor':'10^12','zero_B_included':True,'all_principal_minors_of_tI_minus_BT_Ainv_B_nonnegative':True,'fixed_lambda_1_negative_control_detected':True}

def torsion_check():
 # Constant metric I: Gamma*_i,k^j = -Gamma_i,j^k.
 G={(0,1,0):F(1)}
 Gs={(i,k,j):-v for (i,j,k),v in G.items()}
 tors=lambda A,i,j,k:A.get((i,j,k),0)-A.get((j,i,k),0)
 assert tors(G,0,1,0)==1
 assert all(tors(Gs,i,j,k)==0 for i,j,k in product(range(2),repeat=3))
 assert all(G.get((i,j,k),0)+Gs.get((i,k,j),0)==0 for i,j,k in product(range(2),repeat=3))
 return {'positive_metric_I_dual_pair':True,'one_connection_torsion_nonzero':True,'other_connection_torsion_zero':True,'necessity_of_both_torsion_conditions_demonstrated':True}

if __name__=='__main__':
 out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arithmetic':'Python Fraction; no floating output or external package','coordinate_law':coordinate_checks(),'noncompact_scalar_lift':scalar_lift_checks(),'Schur':schur_checks(),'torsion_boundary':torsion_check(),'all_pass':True,'scope':'Exact finite diagnostics support identified identities and controls; written argument, not finite tests, handles all dimensions/noncompact manifolds.'}
 (E/'independent-exact-checks.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
