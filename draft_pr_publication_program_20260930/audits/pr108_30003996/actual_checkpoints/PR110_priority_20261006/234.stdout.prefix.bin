from fractions import Fraction as F
from pathlib import Path
import hashlib,json,os,datetime
D=Path(__file__).resolve().parent
checks=0

def ck(v):
 global checks
 checks+=1
 if not v:raise AssertionError(checks)

def dot(u,v):return sum(x*y for x,y in zip(u,v))
def sub(u,v):return tuple(x-y for x,y in zip(u,v))
def J(u):return (-u[1],u[0])
def serial(x):return str(x) if isinstance(x,F) else x

a,b,c=F(5),F(3),F(4); lam=F(225,34)
P=[(a,F(0)),(F(0),b),(-a,F(0)),(F(0),-b)]
ck(a*a-b*b==c*c);ck(0<lam<b*b)
rows=[]
for i,A in enumerate(P):
 B=P[(i+1)%4];n=(B[1]-A[1],A[0]-B[0]);k=dot(n,A)
 ck(A[0]**2/a**2+A[1]**2/b**2==1)
 ck(dot(n,B)==k);ck(k*k==(a*a-lam)*n[0]**2+(b*b-lam)*n[1]**2)
 ck(A[0]*B[1]-A[1]*B[0]>0)
 qs=[]
 for sig in [1,-1]:
  f=(sig*c,F(0));u=sub(A,f);v=sub(B,f);r=dot(u,u);s=dot(v,v);det=u[0]*v[1]-u[1]*v[0]
  ck(k-dot(n,f)!=0);ck(det!=0)
  q=((r*v[1]-s*u[1])/det,(u[0]*s-v[0]*r)/det)
  ck(dot(q,u)==r);ck(dot(q,v)==s);ck(dot(q,q)>0)
  Q=(q[0]+f[0],q[1]+f[1])
  tA=dot(sub(Q,A),J(u))/r;tB=dot(sub(Q,B),J(v))/s
  ck(sub(Q,A)==tuple(tA*x for x in J(u)));ck(sub(Q,B)==tuple(tB*x for x in J(v)))
  qs.append(dot(q,q))
  if i==0 and sig==1:
   ck(tA==F(29,3));ck(tB==F(-5,3))
   ray_control={'closed_4_orbit':True,'ellipse_axes':['5','3'],'focus':['4','0'],'lambda':'225/34','A':['5','0'],'B':['0','3'],'Q':['5','29/3'],'ray_parameters_along_same_90_degree_rotation':['29/3','-5/3'],'one_fixed_oriented_half_ray_at_each_endpoint_cannot_contain_intersection':True}
 ck(qs[0]==qs[1]);rows.append({'edge':i,'focal_antipedal_squared_norms':[str(x) for x in qs]})
ck(len(rows)==4);ck(sum(P[(i+1)%4][1]-P[i][1] for i in range(4))==0)
ck(sum((P*2)[(i+1)%8][1]-(P*2)[i][1] for i in range(8))==0)
rec={'schema':'pr110-independent-source-scope-exact-controls/v1','actual_operator_PID':os.getpid(),'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'ray_terminology_negative_control':ray_control,'rows':rows,'purpose':'Exact boundary and interpretation controls, not a proof or novelty certificate.','new_central_search_turns':0}
(D/('EXACT_SCOPE_CONTROLS_OPTIMIZED.json' if not __debug__ else 'EXACT_SCOPE_CONTROLS.json')).write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps({'checks':checks,'actual_operator_PID':os.getpid(),'optimized':not __debug__,'all_passed':True}))
