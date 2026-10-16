"""Independent rational counterexample/geometry/tail diagnostics, not a PDE certificate."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def need(v,m):
 if not v:raise RuntimeError(m)
def zero(n):return [[F(0) for _ in range(n)] for _ in range(n)]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def tr(a):return list(map(list,zip(*a)))
def mul(a,b):return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def sub(a,b):return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def diag(v):return [[v[i] if i==j else F(0) for j in range(len(v))] for i in range(len(v))]
def rotation(n,i,j,c,s):
 a=eye(n);a[i][i]=a[j][j]=c;a[i][j]=-s;a[j][i]=s;return a
def projection(n,k):return diag([F(i<k) for i in range(n)])
def norm2sq_frob(a):return sum(x*x for row in a for x in row)
def main():
 rows=[];n=5;c=F(20,29);s=F(21,29);u=rotation(n,0,1,c,s);need(mul(tr(u),u)==eye(n),'unitary')
 p=projection(n,1);q=mul(mul(u,p),tr(u));diff=sub(p,q)
 need(mul(diff,diff)==diag([s*s,s*s,F(0),F(0),F(0)]),'exact branch norm')
 cluster=projection(n,2);need(mul(mul(u,cluster),tr(u))==cluster,'whole cluster')
 for t in [F(1,8),F(1,32),F(1,128)]:
  r0=diag([F(1,2),F(1,2),F(1,5),F(1,6),F(1,7)])
  rt=mul(mul(u,diag([F(1,2)-t,F(1,2)+t,F(1,5),F(1,6),F(1,7)])),tr(u))
  need(mul(sub(rt,r0),sub(rt,r0))==diag([t*t,t*t,F(0),F(0),F(0)]),'normrt')
  need(mul(rt,cluster)==mul(cluster,rt),'cluster commute');rows.append({'t':str(t),'operator_distance':str(t),'branch_projection_distance':str(s),'whole_cluster_distance':'0'})
 nested=[]
 for t in [F(1,16),F(1,64),F(1,256)]:
  cc=(1-t*t)/(1+t*t);ss=2*t/(1+t*t);v=rotation(n,1,4,cc,ss)
  p2=mul(mul(v,projection(n,2)),tr(v));p3=mul(mul(v,projection(n,3)),tr(v));r=mul(mul(v,diag([F(1,2),F(2,3),F(3,4),F(4,5),F(5,6)])),tr(v))
  for k,pj in [(2,p2),(3,p3)]:
   need(tr(pj)==pj and mul(pj,pj)==pj and sum(pj[i][i] for i in range(n))==k,'rank projection');need(mul(pj,r)==mul(r,pj),'commute')
  need(mul(p2,p3)==p2,'nested');need(norm2sq_frob(sub(p2,projection(n,2)))==2*ss*ss,'distance')
  nested.append({'t':str(t),'ranks':[2,3],'norm_distance':str(ss)})
 geometry=[];delta=F(1,7);old=F(3,2);new=F(11,4);coordinates=[-2*delta,-delta,-delta/2,F(0),delta/2,delta,2*delta]
 for d in [2,3,5]:
  count=0
  for x in product(coordinates,repeat=d):
   inold=(-2*old<x[0]<0 and all(abs(a)<old for a in x[1:]));innew=(0<x[0]<2*new and all(abs(a)<new for a in x[1:]));inconn=all(abs(a)<delta for a in x)
   added=inconn and not(inold or innew);face=x[0]==0 and all(abs(a)<delta for a in x[1:]);need(added==face,'face identity');count+=1
  geometry.append({'d':d,'rational_grid_points':count})
 S={4,7,10,13};forbidden=set()
 for m in product(range(1,11),repeat=4):
  norm=sum(k*k for k in m)
  for lam in S:
   a2=F(norm,lam)
   if 4<a2<9:forbidden.add(a2)
 a=F(17,7);need(2<a<3 and a*a not in forbidden,'nonresonant')
 for lam in S:need((lam*a*a).denominator!=1,'integer sum obstruction')
 tails=[]
 for j in range(1,151):
  partial=sum((F(1,2**(k+2)) for k in range(j,j+200)),F(0));remainder=F(1,2**(j+201));need(partial+remainder==F(1,2**(j+1)),'tail');need(F(1,2**j)+F(1,2**(j+1))==F(3,2**(j+1)),'birthtail');tails.append(j)
 derivative_energy=36*(F(1,3)-F(1,2)+F(1,5));need(derivative_energy==F(6,5),'profile integral')
 result={'status':'PASS_FINITE_DIAGNOSTICS_ONLY','different_rational_branch_controls':rows,'nested_cluster_controls':nested,'geometry':geometry,'nonresonance':{'d':4,'protected_units_pi2_over4':sorted(S),'forbidden_squared_widths':len(forbidden),'chosen_width':str(a),'integer_bound':10},'exact_tail_identities':len(tails),'C1_cutoff_profile_auxiliary_energy':str(derivative_energy),'limits':'C1 polynomial is only an auxiliary integration check; the analytic proof uses a smooth flat-endpoint theta. Finite matrices/grids/tails do not prove capacity, PDE convergence, aperture sizes or infinite completeness.'}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
