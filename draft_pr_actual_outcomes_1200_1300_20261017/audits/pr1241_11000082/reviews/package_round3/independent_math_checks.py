from pathlib import Path
import itertools,json,hashlib,sys
sys.set_int_max_str_digits(0)
R=Path(__file__).resolve().parent

def need(c,m):
 if not c:raise RuntimeError(m)
def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def inv(a):return (a[3],-a[1],-a[2],a[0])
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
def power(a,n):
 if n<0:return power(inv(a),-n)
 z=(1,0,0,1)
 while n:
  if n%2:z=mul(z,a)
  a=mul(a,a);n//=2
 return z
def invert(w):return tuple(-x for x in reversed(w))
def red(w):
 a=[]
 for x in w:
  if a and a[-1]==-x:a.pop()
  else:a.append(x)
 return tuple(a)
def cyc(w):
 w=red(w)
 while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
 return w
def minimum_rotation(s):
 if not s:return s
 ss=s+s;i=0;j=1;k=0;n=len(s)
 while i<n and j<n and k<n:
  a=ss[i+k];b=ss[j+k]
  if a==b:k+=1;continue
  if a>b:i=i+k+1;i+=(i==j)
  else:j=j+k+1;j+=(i==j)
  k=0
 p=min(i,j);return ss[p:p+n]
def normal(w):return minimum_rotation(cyc(w))
def word(signs):
 u=(1,)
 for j,e in enumerate(signs,1):
  a=u if e==1 else invert(u);b=invert(a)
  u=b+(2,)*(2*j)+a+(2,)*(2*j-1)+b+(2,)*(2*j)+a
 return u
def evaluate(w,a,b):
 mats={1:a,-1:inv(a),2:b,-2:inv(b)};z=(1,0,0,1)
 for x in w:z=mul(z,mats[x])
 return z
mat=[]
for mu in (2,4,6,8,14):
 u=(1,mu,0,1);v=(1,0,-mu,1);c=u
 for r in range(2,8):
  c=comm(v,c);need(c[1]==-mu**(2**r-1),'q recurrence');need(c[0]+c[3]==2+mu**(2**r),'trace recurrence');need(c[0]*c[3]-c[1]*c[2]==1,'det');mat.append([mu,r])
need(sum(mul((1,2,0,1),(1,0,-2,1))[i] for i in (0,3))==-2,'n=2 cusp boundary')
need(abs(sum(mul((1,4,0,1),(1,0,-4,1))[i] for i in (0,3)))>2,'n=4 hyperbolic boundary')
reps=[((1,1,0,1),(1,0,1,1)),((2,1,1,1),(1,2,0,1)),((-2,-1,-1,-1),(1,0,-4,1)),((1,8,0,1),(1,0,-8,1))]
levels=[]
for m in range(1,6):
 words=[word(s) for s in itertools.product((-1,1),repeat=m)];classes={normal(w) for w in words};need(len(classes)==2**m,'cyclic classes');need(all(red(w)==w and w for w in words),'nontrivial reduced')
 traces=[]
 for a,b in reps:
  values=[sum(evaluate(w,a,b)[i] for i in (0,3)) for w in words];need(len(set(values))==1,'trace identity finite');traces.append({'digits':len(str(abs(values[0]))),'sha256':hashlib.sha256(str(values[0]).encode()).hexdigest()})
 altered=(words[0][0]*-1,)+words[0][1:];need(any(sum(evaluate(altered,a,b)[i] for i in (0,3))!=sum(evaluate(words[0],a,b)[i] for i in (0,3)) for a,b in reps),'altered-word negative control')
 levels.append({'m':m,'classes':len(classes),'word_length':len(words[0]),'traces':traces})
# A two-vertex covering core for <b, a b a^-1> has two b loops.
# For every tested exponent each start has one closed lift of b^q, and these
# loops are distinct intrinsic classes despite conjugacy in the ambient rose.
trans={(0,1):1,(1,-1):0,(0,2):0,(0,-2):0,(1,2):1,(1,-2):1}
fiber=[]
for q in (1,2,3,7,30,101):
 closed=[]
 for start in (0,1):
  at=start
  for x in (2,)*q:at=trans[(at,x)]
  if at==start:closed.append(start)
 need(closed==[0,1],'power core bound');fiber.append({'power':q,'closed_lifts':len(closed),'same_fixed_bound':2})
report={'status':'PASS','commutator_cases':mat,'trace_levels':levels,'proper_power_core_controls':fiber,'limits':'Finite supplementary algebra only. General outer centrality, Schottky compactness, full-stabilizer uniqueness and uniform ambient fusion checked analytically; no geometric realization asserted for arbitrary matrix parameters.'}
(R/'INDEPENDENT_MATH_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','matrix_cases':len(mat),'maximum_m':5,'representations':len(reps)}))
