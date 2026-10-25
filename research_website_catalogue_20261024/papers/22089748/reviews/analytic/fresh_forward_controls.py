#!/usr/bin/env python3
"""Independent exact death–Birth subset-chain controls, manuscript equations only.
Does not import any supplied mathematical helper or certificate.
"""
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations
import json,hashlib,time
import sympy as s
R=s.Rational
checks=[];details={};start=time.time()
def check(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def J(n):return s.Matrix(n,n,lambda i,j:0 if i==j else R(1,n-1))
def chain(P,r=R(2)):
 n=P.rows; full=(1<<n)-1; states=list(range(1,full));T=s.zeros(full+1)
 for S in range(full+1):
  for v in range(n):
   x=sum(P[v,u] for u in range(n) if S>>u&1);f=r*x/(1+(r-1)*x)
   T[S,S|(1<<v)]+=f/n;T[S,S&~(1<<v)]+=(1-f)/n
 return T

def fixation(P,r=R(2)):
 n=P.rows;F=(1<<n)-1;T=chain(P,r);h=(s.eye(F-1)-T[1:F,1:F]).inv(method='DM')*T[1:F,F];return sum(h[(1<<i)-1] for i in range(n))/n,h,T

def expansion(n,delta):
 F=(1<<n)-1;P=J(n);Cs=[s.zeros(F+1) for _ in range(3)]
 for S in range(F+1):
  for v in range(n):
   x=sum(P[v,u] for u in range(n) if S>>u&1);z=sum(delta[v,u] for u in range(n) if S>>u&1)
   fs=[2*x/(1+x),2*z/(1+x)**2,-2*z*z/(1+x)**3]
   for k,f in enumerate(fs):
    Cs[k][S,S|(1<<v)]+=f/n;Cs[k][S,S&~(1<<v)]+=((1 if k==0 else 0)-f)/n
 Q=[c[1:F,1:F] for c in Cs];bs=[c[1:F,F] for c in Cs];inv=(s.eye(F-1)-Q[0]).inv(method='DM')
 h0=inv*bs[0];h1=inv*(Q[1]*h0+bs[1]);h2=inv*(Q[1]*h1+Q[2]*h0+bs[2]);rho=[sum(h[(1<<i)-1] for i in range(n))/n for h in [h0,h1,h2]]
 check(rho[1]==0,f'forward first variation n{n}')
 return -rho[2]/(n*rho[0]**2),rho

def standard(n):
 xi=[1,-1]+[0]*(n-2)
 return s.Matrix(n,n,lambda i,j:0 if i==j else R(xi[i]+(n-1)*xi[j],n*(n-2)))
def anti(n):
 D=s.zeros(n)
 for a,b in [(0,1),(1,2),(2,0)]:D[a,b]=1;D[b,a]=-1
 return D
def sym(n):
 D=s.zeros(n)
 for a,b,v in [(0,1,1),(1,2,-1),(2,3,1),(3,0,-1)]:D[a,b]=D[b,a]=v
 return D
expected={3:[R(1,11),None,R(1,9)],4:[R(87,640),R(3,208),R(57,640)],5:[R(8585,57314),R(359,26660),R(143,2100)]}
for n in (3,4,5):
 es=[]
 for name,D,want in zip(['standard','symmetric','antisymmetric'],[standard(n),sym(n) if n>=4 else None,anti(n)],expected[n]):
  if D is None:continue
  check(D*s.ones(n,1)==s.zeros(n,1),'row-zero '+name+str(n));val,rho=expansion(n,D);norm=sum(x*x for x in D)
  check(val/norm==want,'published sector table '+name+str(n));es.append((name,str(val/norm)))
  check(rho[0]==R(n-1,n)*R(1,2)/(1-R(1,2)**(n-1)),'baseline '+str(n))
 A=standard(n);B=anti(n)
 if n>=4:B+=sym(n)
 ra,_=expansion(n,A);rb,_=expansion(n,B);rm,_=expansion(n,A+B)
 check(rm==ra+rb,'sector cross-orthogonality '+str(n));details['sector_'+str(n)]=es
 print('forward Hessian',n,es,flush=True)
# Full tangent curvature at n=4: polarization in the natural row-zero basis.
n=4;basis=[]
for v in range(n):
 cols=[u for u in range(n) if u!=v];anchor=cols[-1]
 for u in cols[:-1]:
  D=s.zeros(n);D[v,u]=1;D[v,anchor]=-1;basis.append(D)
vals=[expansion(n,D)[0] for D in basis];H=s.diag(*vals)
for i,j in combinations(range(len(basis)),2):H[i,j]=H[j,i]=(expansion(n,basis[i]+basis[j])[0]-vals[i]-vals[j])/2
mins=[H[:k,:k].det(method='domain-ge') for k in range(1,len(basis)+1)]
check(all(x>0 for x in mins),'all8 principal minors positive for full directed n4 tangent');details['n4_full_tangent_principal_minors']=list(map(str,mins))
# Strong-selection Taylor coefficient from the full forward chain, using epsilon=1/r.
def strong(P):
 n=P.rows;F=(1<<n)-1;T0=s.zeros(F+1);T1=s.zeros(F+1)
 for S in range(F+1):
  for v in range(n):
   x=sum(P[v,u] for u in range(n) if S>>u&1)
   f0=0 if x==0 else 1;f1=0 if x==0 else -(1-x)/x
   for T,k,f in [(T0,0,f0),(T1,1,f1)]:
    T[S,S|1<<v]+=R(1,n)*f;T[S,S&~(1<<v)]+=R(1,n)*((1 if k==0 else 0)-f)
 inv=(s.eye(F-1)-T0[1:F,1:F]).inv(method='DM');h0=inv*T0[1:F,F];h1=inv*(T1[1:F,1:F]*h0+T1[1:F,F]);return [sum(h[(1<<i)-1] for i in range(n))/n for h in (h0,h1)]
for n in (3,4,5):
 W=s.Matrix(n,n,lambda v,u:0 if v==u else (v+2)*(u+3)+(v-u)**2);P=s.Matrix(n,n,lambda v,u:W[v,u]/sum(W[v,j] for j in range(n)))
 a0,a1=strong(P);E=sum((P[v,u]-P[v,z])**2/(P[v,u]*P[v,z]) for v in range(n) for u,z in combinations([j for j in range(n) if j!=v],2))
 check(a0==R(n-1,n),'strong leading '+str(n));check(-R(n-1,n)-a1==E/(n*n*(n-2)),'strong defect coefficient '+str(n));details['strong_'+str(n)]=[str(a0),str(a1),str(E)]
 print('strong selection',n,flush=True)
# Triangle global rational identity against exact 6-state absorption and determinant.
for a,b,c,r in [(1,2,3,R(2)),(2,5,7,R(7,3)),(4,4,4,R(9,5)),(5,2,1,R(1,3))]:
 W=s.Matrix([[0,a,b],[a,0,c],[b,c,0]]);P=s.Matrix(3,3,lambda v,u:W[v,u]/sum(W[v,j] for j in range(3)));rho,h,T=fixation(P,r)
 ss1=a+b+c;ss2=a*b+a*c+b*c;ss3=a*b*c
 aa=3*ss3*(ss1*ss2-9*ss3);dd=12*ss1**3*ss3-45*ss1*ss2*ss3+4*ss2**3-27*ss3**2;ee=4*ss2*(3*ss1**2*ss2-3*ss1*ss3-8*ss2**2);Hr=aa*(r-1)**4+dd*r*(r-1)**2+ee*r*r
 # Paper's matrix after multiplying single state first-step equations by n.
 M=3*(s.eye(6)-T[1:7,1:7]);L=s.prod(r*p+q for i,p in enumerate((a,b,c)) for j,q in enumerate((a,b,c)) if i!=j);Pr=L*M.det(method='domain-ge')/3
 check(s.factor(rho-2*r/(3*(r+1))+r*(r-1)*Hr/(3*(r+1)*Pr))==0,'triangle identity '+str((a,b,c,r)))
results={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':len(checks),'labels':checks,'details':details,'seconds':time.time()-start,'scope':'Fresh original forward subset-chain, Taylor expansion at J, full n4 tangent, n3-5 sector table/strong asymptotics, rational triangle controls; no submitted code imported.','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('fresh_forward_results.json').write_text(json.dumps(results,indent=2)+'\n');print({'status':'PASS','checks':len(checks),'seconds':time.time()-start})
