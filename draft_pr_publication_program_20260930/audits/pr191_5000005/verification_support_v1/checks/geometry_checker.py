from collections import Counter
from fractions import Fraction
from pathlib import Path
import datetime,json,math
counts=Counter()
def require(ok,message):
 if not ok:raise AssertionError(message)
def vertical_length(vertices,x):
 ys=[]
 for (u,v) in zip(vertices,vertices[1:]+vertices[:1]):
  if abs(v[0]-u[0])<1e-14:continue
  t=(x-u[0])/(v[0]-u[0])
  if -1e-11<=t<=1+1e-11:ys.append(u[1]+t*(v[1]-u[1]))
 require(len(ys)>=2,('intersection',x,ys))
 return max(ys)-min(ys)
def corner(n,copy,j):
 if n%2:
  t=j
  if t%2!=copy:t+=n
  return 0,t
 return (j+copy)%2,j
for n in range(3,129):
 N=n-2;rho=math.pi/n
 parent=list(range(2*n))
 def find(a):
  while parent[a]!=a:a=parent[a]
  return a
 def union(a,b):parent[find(a)]=find(b)
 for j in range(n):
  union(j,n+(j+1)%n);union((j+1)%n,n+j)
 classes=Counter(find(j) for j in range(2*n))
 require(sorted(classes.values())==([2*n] if n%2 else [n,n]),('cones',n,classes))
 for copy in range(2):
  for j in range(n):
   c,t=corner(n,copy,j)
   physical=((t*N+c*n)%(2*n))
   require(physical==(copy*n-2*j)%(2*n),('angle alignment',n,copy,j,c,t))
   counts['corner_physical_alignments']+=1
   for q in range(1,n):
    jp=(j+q)%n;cp,tp=corner(n,copy,jp)
    h=copy*n-2*j+n-1-q
    a=Fraction(t*N+n-1-q-h,n)
    b=Fraction(tp*N+q-1-h,n)
    require(a.denominator==b.denominator==1,('germ_integrality',n,copy,j,q,a,b))
    require((a+b+h)%N==0,('canonical_matching',n,copy,j,q,h,a,b))
    counts['exact_canonical_chords']+=1
 vertices=[(math.cos(2*j*rho),math.sin(2*j*rho)) for j in range(n)]
 lam=2/math.tan(rho)
 for j in range(1,n//2+1):
  a=math.cos(2*j*rho);b=math.cos(2*(j-1)*rho);S=a+b
  H=b-a;L=2*(math.sin(2*j*rho)+math.sin(2*(j-1)*rho))
  require(H>0 and L>0,('positive_cylinder',n,j,H,L))
  require(math.isclose(L/H,lam,rel_tol=2e-11,abs_tol=1e-11),('modulus',n,j,L/H,lam))
  for r in [0.13,0.5,0.87]:
   x=a+r*H;xq=x-S
   lp=vertical_length(vertices,x)
   # Q is -P; its vertical chord at xq has P's length at -xq.
   lq=vertical_length(vertices,-xq)
   require(math.isclose(lp+lq,L,rel_tol=2e-10,abs_tol=2e-11),('constant_circumference',n,j,r,lp,lq,L))
   require(-b<xq<-a,('strip_pair',n,j,r,xq,-b,-a))
   counts['numeric_cylinder_cross_sections']+=1
  counts['cylinder_moduli']+=1
 for r in [0.01,0.1,0.25,0.5,0.75,0.9,0.99]:
  theta=r*rho/(2 if n%2 else 1)
  x=math.cos(theta);y=math.sin(theta)
  x1=x-lam*y
  require(x1*x1+y*y<x*x+y*y,('descent',n,r))
  counts['strict_descent_samples']+=1
 if not n%2:
  x=math.cos(rho);y=math.sin(rho)
  require(math.isclose((x-lam*y)**2+y*y,x*x+y*y,abs_tol=1e-12),('second_cusp_boundary',n))
  counts['even_boundary_equalities']+=1
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'n_min':3,'n_max':128,'counts':dict(counts),'status':'PASS','proof_scope':'Finite corroboration only; universal cylinder/descent proof is analytic. Numeric cylinder comparisons use explicit tolerances and are not interval arithmetic.'}
Path('GEOMETRY_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))
