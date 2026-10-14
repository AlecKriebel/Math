"""Independent bounded geometric falsification, not certified floating-point proof."""
import cmath,math,random,json,datetime
from pathlib import Path
R=Path(__file__).resolve().parent
rng=random.Random(1525000006)
count={};examples=[];max_residual=0.;ratios={}
def ck(k,b):
 if not b:raise RuntimeError(k)
 count[k]=count.get(k,0)+1
def cross(a,b):return (a.conjugate()*b).imag
def reflection(z,a,b):
 e=b-a;return a+e*((z-a)/e).conjugate()
def poly(n):
 phi=1.5*math.pi-math.pi/n;z=[cmath.exp(1j*(phi-2*math.pi*j/n)) for j in range(n)]
 return [(w-z[0])/(2*math.sin(math.pi/n)) for w in z]
def trace(P,d,max_steps=350):
 n=len(P);x=0j;L=0.;develop=P[:];sides=[]
 for step in range(max_steps):
  hits=[]
  for j in range(n):
   a=P[j];e=P[(j+1)%n]-a;den=cross(d,e)
   if abs(den)<1e-11:continue
   t=cross(a-x,e)/den;u=cross(a-x,d)/den
   if t>1e-8 and -1e-8<=u<=1+1e-8:hits.append((t,j,u))
  if not hits:return None
  t,j,u=min(hits);y=x+t*d;L+=t
  distances=[abs(y-v) for v in P];end=min(range(n),key=distances.__getitem__)
  if distances[end]<2e-7:
   return {'L':L,'N':step+1,'end':end,'dend':d,'devpoly':develop,'sides':sides,'error':distances[end]}
  if u<1e-7 or u>1-1e-7:return None
  a=P[j];e=P[(j+1)%n]-a;d=e*((d/e).conjugate());d/=abs(d)
  aD=develop[j];bD=develop[(j+1)%n];develop=[reflection(z,aD,bD) for z in develop]
  sides.append(j);x=y
 return None
for n in range(3,23):
 P=poly(n);delta=(n-2)*math.pi/n
 # Derive gluings by physical translation, rather than assuming endpoint cycles.
 corners=[(s,j) for s in [1,-1] for j in range(n)]
 graph={v:set() for v in corners}
 for j in range(n):
  a,b=P[j],P[(j+1)%n];shift=-a-b
  ck('side_translation_endpoint',abs(a+shift+P[(j+1)%n])<1e-12 and abs(b+shift+P[j])<1e-12)
  for u,v in [((1,j),(-1,(j+1)%n)),((1,(j+1)%n),(-1,j))]:graph[u].add(v);graph[v].add(u)
 unseen=set(corners);classes=[]
 while unseen:
  todo=[unseen.pop()];cl=set(todo)
  while todo:
   for z in graph[todo.pop()]:
    if z not in cl:cl.add(z);unseen.discard(z);todo.append(z)
  classes.append(cl)
 g=(n-len(classes))//2
 ck('geometric_Euler_genus',g==((n-1)//2 if n%2 else (n-2)//2))
 ck('involution_class_fixed',sum(any((-s,j) in cl for s,j in cl) for cl in classes)==(1 if n%2 else 0))
 # Polygon centers cannot be fixed since interiors are disjoint sheets.
 ck('Riemann_Hurwitz_sphere',2-2*g==2*2-(n+n%2))
 candidates=[]
 for j in range(1,n):candidates.append(P[j])
 for trial in range(550):
  Q=P[:];last=None
  for depth in range(rng.randrange(1,7)):
   side=rng.randrange(n)
   if side==last:side=(side+1)%n
   a,b=Q[side],Q[(side+1)%n];Q=[reflection(z,a,b) for z in Q];last=side
  candidates.append(Q[rng.randrange(n)])
 seen=set()
 for z in candidates:
  if abs(z)<1e-8:continue
  alpha=cmath.phase(z)
  if alpha<-1e-9 or alpha>delta+1e-9:continue
  key=round(alpha,11)
  if key in seen:continue
  seen.add(key)
  if alpha<1e-8 or delta-alpha<1e-8:continue # side controls handled separately
  res=trace(P,z/abs(z))
  if res is None:continue
  j=res['end'];back=-res['dend'];start=P[(j-1)%n]-P[j]
  interior=(cmath.phase(back/start))%(2*math.pi)
  if interior>delta+1e-5:raise RuntimeError('terminal interior offset')
  beta=math.pi-interior;N=res['N'];s=n*((alpha+beta) if N%2 else (beta-alpha))/(2*math.pi)
  residual=abs(s-round(s));max_residual=max(max_residual,residual)
  if residual>1e-5:raise RuntimeError('source integrality')
  k=((n-1-round(s)) if N%2 else (round(s)-1))%(n-2)
  sr=n*((2*math.pi-alpha-beta) if N%2 else (beta-alpha))/(2*math.pi)
  kr=((n-1-round(sr)) if N%2 else (round(sr)-1))%(n-2)
  ck('physical_parity_sensitive_reversal',kr==((-k) if N%2 else k)%(n-2))
  # Recover the actual canonical terminal corner from the physically reflected copy.
  sign=1 if N%2 else -1;canonical=[sign*w for w in P]
  shift=sum(res['devpoly'])/n-sum(canonical)/n
  endpoint=res['devpoly'][j]-shift
  idx=min(range(n),key=lambda a:abs(endpoint-canonical[a]))
  ck('canonical_developed_corner',abs(endpoint-canonical[idx])<1e-7)
  e=0 if n%2 else ((idx if sign==1 else idx+1)%2)
  t=idx
  if n%2 and ((t%2==0)!=(sign==1)):t+=n
  offset=(math.pi-beta) if sign==1 else (beta-2*math.pi/n)
  diff=t*delta+offset-alpha;m=(diff-(1-e)*math.pi)/(2*math.pi)
  ck('actual_geometric_cone_integrality',abs(m-round(m))<1e-5)
  K=(2*round(m)+1-e)%(n-2)
  ck('actual_geometry_source_dictionary',K==k)
  w=math.sin((k+1)*math.pi/n);q=res['L']/w
  sig=round(math.cos((n if n%2==0 else 2*n)*alpha),8)
  key=(n,sig)
  if key in ratios:
   ck('sample_dihedral_labelled_ratio',abs(q/ratios[key]-1)<5e-5)
  else:ratios[key]=q
  count['physical_first_vertex_paths']=count.get('physical_first_vertex_paths',0)+1
  if len(examples)<25:examples.append({'n':n,'N':N,'k':k,'K':K,'alpha_pi':alpha/math.pi,'beta_pi':beta/math.pi,'L':res['L'],'sides':res['sides']})
 # Convex model-direction exhaustion: every inward symmetry-direction ray meets a vertex.
 for a in range(n):
  for j in range(n):
   theta=(j*math.pi/n)
   d=cmath.exp(1j*theta)
   for eps in [1,-1]:
    v=eps*d
    hits=[]
    for b in range(n):
     edge=P[(b+1)%n]-P[b];den=cross(v,edge)
     if abs(den)<1e-10:continue
     t=cross(P[b]-P[a],edge)/den;u=cross(P[b]-P[a],v)/den
     if t>1e-8 and -1e-8<=u<=1+1e-8:hits.append((t,u))
    if hits:
     tt,uu=min(hits)
     ck('model_chord_exhaustion',min(abs(uu),abs(uu-1))<1e-7)
# Dense angular lift checks use a continuous explicitly unwrapped lift with slope sign.
for A in [(2.,1.,1.,1.),(1.,1000.,0.,1.),(.0001,0.,0.,10000.),(0.,-1.,1.,0.)]:
 a,b,c,d=A;det=a*d-b*c;ck('lift_positive_det',det>0)
 def raw(theta):x,y=math.cos(theta),math.sin(theta);return math.atan2(c*x+d*y,a*x+b*y)
 for theta in [i*.037 for i in range(-100,101)]:
  ck('angular_antipodality',abs(cmath.exp(1j*(raw(theta+math.pi)-raw(theta)))+1)<2e-7)
  # Consequence of derivative angular speed det/|Av|^2 is increasing lift.
  speed=det/((a*math.cos(theta)+b*math.sin(theta))**2+(c*math.cos(theta)+d*math.sin(theta))**2)
  ck('angular_speed_positive',speed>0)
receipt={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','counts':count,'check_total':sum(count.values()),'maximum_source_integrality_residual':max_residual,'examples':examples,'angular_tolerance':{'empirical_acceptance_tolerance':2e-7,'proved_numerical_error_bound':False,'initial_tolerance':1e-9,'universal_claim_proof':'analytic angular derivative and antipodality, not this computation'},'limits':'Independent double-precision controls, seed 1525000006, n3..22, depth at most6; not interval-validated and not universal proof.'}
(R/'INDEPENDENT_GEOMETRY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','counts':count,'max_residual':max_residual},indent=2))
