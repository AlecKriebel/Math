"""Exact finite consistency checks for PR1261. Not an infinite-theorem certificate."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import datetime,hashlib,json

def need(c,m):
 if not c:raise RuntimeError(m)
def trim(p):
 p=list(p)
 while len(p)>1 and not p[-1]:p.pop()
 return p
def add(a,b):return trim([(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0)) for i in range(max(len(a),len(b)))])
def scale(a,s):return trim([s*x for x in a])
def mul(a,b):
 c=[F(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def power(a,n):
 p=[F(1)]
 for _ in range(n):p=mul(p,a)
 return p
def compose(a,b):
 p=[F(0)]
 for x in reversed(a):p=add(mul(p,b),[x])
 return p
def value(p,t):
 x=F(0)
 for c in reversed(p):x=x*t+c
 return x
def integral(p,shift=0):return sum((c/F(i+shift+1) for i,c in enumerate(p)),F(0))
def kernel(m):
 t0=[F(1)];t1=[F(1),F(-2)];polys=[t0,t1]
 for j in range(1,m):polys.append(add(scale(mul(t1,polys[-1]),2),scale(polys[-2],-1)))
 a=[F(1)]
 for p in polys[1:m+1]:a=add(a,scale(p,2))
 return scale(a,F(1,2*m+1))
def binomial_kernel(m):
 n=2*m+1;a=[F(0)]
 for j in range(m+1):a=add(a,scale(mul([F(0)]*j+[F(1)],power([F(1),F(-1)],m-j)),F((-1)**j*comb(n,2*j+1),n)))
 return a

def moment(a,b,c):return F(0) if a%2 or b%2 else F(4,(a+1)*(b+1)*(a+b+c+3))
def ldl_positive(a):
 a=[list(row) for row in a];pivots=[]
 for k in range(len(a)):
  pivot=a[k][k];need(pivot>0,'Nonpositive exact moment pivot');pivots.append(pivot)
  for i in range(k+1,len(a)):
   for j in range(k+1,len(a)):a[i][j]-=a[i][k]*a[k][j]/pivot
 return pivots

def run():
 identities=0;grid=0;core=0;moments=[];composed=[]
 for m in range(1,9):
  a=kernel(m);need(a==binomial_kernel(m),'Kernel sine/binomial identity');need(len(a)-1==m and value(a,F(0))==1 and value(a,F(1))==F((-1)**m,2*m+1),'Kernel degree/endpoints');identities+=1
  n=2*m+1;h=F(1,n*n)
  for den in [17,31,53]:
   for j in range(den+1):
    t=F(j,den);v=value(a,t);need(v*v<=1,'Triangle bound')
    if t:need(v*v<=F(1,n*n)/t,'Endpoint tail bound')
    grid+=1
  for j in range(33):need(value(a,h*F(j,32))>=F(7,11),'Positive core rational weaker control');core+=1
 for n in range(1,7):
  L=n+2;bound=F(11,7)**(2*L)*(1+2**(n+2))
  for m in range(1,5):
   q=power(kernel(m),2*L);z=integral(q,n-1);num=integral(q,n);need(z>0 and num>0,'Beta full mass positive');ratio=num/z;h=F(1,(2*m+1)**2);need(ratio<=bound*h,'Exact beta ratio bound');moments.append({'dimension':n,'m':m,'ratio':str(ratio),'ratio_over_h':str(ratio/h),'degree':len(q)-1,'direct_affine_order':m*L})
 for name,u,obj,G in [('boundary_affine',[F(0),F(1,2),F(1,2)],[F(0),F(1)],F(2)),('boundary_concave',[F(0),F(4,9),F(5,9)],[F(0),F(1),F(-1,4)],F(9,4)),('interior_nonconvex',[F(0),F(0),F(1)],[F(0),F(0),F(1),F(0),F(-2,5)],F(12,5))]:
  for m in range(1,5):
   q=power(compose(kernel(m),u),6);z=integral(q);e=integral(mul(q,obj))/z;eu=integral(mul(q,u))/z;need(z>0 and 0<=e<=G*eu,'Proxy moment domination');need(len(q)-1<=12*m,'Global square degree');need(eu<=F(11,7)**6*9/F((2*m+1)**2),'Composed proxy full mass bound');composed.append({'case':name,'m':m,'error':str(e),'proxy_moment':str(eu),'normalization':str(z),'degree':len(q)-1,'order':6*m})
 pyramid=[]
 for r in range(0,4):
  basis=[(i,j,k) for i in range(r+1) for j in range(r+1-i) for k in range(r+1-i-j)]
  H=[[moment(a[0]+b[0],a[1]+b[1],a[2]+b[2]) for b in basis] for a in basis];Z=[[moment(a[0]+b[0],a[1]+b[1],a[2]+b[2]+1) for b in basis] for a in basis]
  hp=ldl_positive(H);zp=ldl_positive(Z);pyramid.append({'r':r,'dimension':len(basis),'positive_H_pivots':len(hp),'positive_Z_pivots':len(zp),'last_H_pivot':str(hp[-1]),'last_Z_pivot':str(zp[-1])})
 need(moment(0,0,0)==F(4,3) and moment(1,2,3)==0,'Pyramid parity/volume')
 degree_cases=0
 for n in range(1,9):
  L=n+2
  for r in range(1,2001):
   if r>=2*L:
    m=r//(2*L);need(m>=1 and 4*m*L<=2*r and 2*m+1>=F(r,2*L),'All-order degree/floor');degree_cases+=1
   else:need(F(4*L*L,r*r)>1,'Small-order constant');degree_cases+=1
 rejected=[]
 def rejects(name,fn):
  try:fn()
  except RuntimeError:rejected.append(name)
  else:raise RuntimeError('Negative control accepted '+name)
 wrong=kernel(3);wrong[1]+=F(1)
 rejects('altered_kernel_identity',lambda:need(wrong==binomial_kernel(3),'altered'))
 rejects('incorrect_quadratic_composition_degree',lambda:need(len(power(compose(kernel(2),[F(0),F(0),F(1)]),6))-1<=2*(2*3),'degree'))
 rejects('critical_exponent_geometric_divergence',lambda:need(3>2+1,'L must exceed n+1'))
 rejects('reversed_sublevel_ratio',lambda:need(F(2,10)**3<=F(1,10)**3,'growth direction'))
 need(len(rejected)==4,'Missing controls')
 return {'status':'PASS','kernel_identities':identities,'rational_grid_cases':grid,'rational_core_cases':core,'core_check_limit':'Tests weaker 7/11 lower bound; exact2/pi bound proved analytically, not inferred from finite grid.','beta_moment_cases':moments,'composed_proxy_cases':composed,'pyramid_exact_LDL':pyramid,'all_integer_degree_floor_cases':degree_cases,'rejected_negative_controls':rejected,'limits':'Finite exact consistency only. No infinite proof certificate, new general-measure claim, efficient minimizer algorithm, original omitted-code replay or numerical SDP certificate.'}
if __name__=='__main__':
 result=run();p=Path(__file__).resolve();report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'program_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'result':result};print(json.dumps(report,indent=2,sort_keys=True))
