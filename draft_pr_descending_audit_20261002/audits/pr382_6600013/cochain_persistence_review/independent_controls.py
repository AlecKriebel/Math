"""Independent rational homology controls; no candidate library imports."""
from fractions import Fraction
from functools import lru_cache
from math import gcd,isqrt
from itertools import product
import json,hashlib,time
START=time.monotonic();checks={}
def ck(v,tag):
 assert v,tag
 checks[tag]=checks.get(tag,0)+1
# Integer sparse row-space algorithm: fraction-free insertion, primitive rows.
def rank(rows):
 piv={}
 for row in rows:
  r={j:int(v) for j,v in enumerate(row) if v}
  while r:
   j=min(r)
   if j not in piv:
    g=0
    for v in r.values():g=gcd(g,v)
    if g>1:r={k:v//g for k,v in r.items()}
    piv[j]=r;break
   a=piv[j];c=r[j];d=a[j];keys=r.keys()|a.keys()
   r={k:d*r.get(k,0)-c*a.get(k,0) for k in keys}
   r={k:v for k,v in r.items() if v}
   g=0
   for v in r.values():g=gcd(g,v)
   if g>1:r={k:v//g for k,v in r.items()}
 return len(piv)
def mm(a,b):
 cols=list(zip(*b))
 return [[sum(x*y for x,y in zip(r,c)) for c in cols] for r in a]
def transpose(a):return list(map(list,zip(*a)))
def zero(n,m):return [[0]*m for _ in range(n)]
def tm_word(n):return tuple(i.bit_count()%2 for i in range(n))
@lru_cache(None)
def tm(n):
 block=1
 while block<n-1:block*=2
 w=tm_word(8*block)
 return tuple(sorted({w[i:i+n] for i in range(len(w)-n+1)}))
# Certify floors a+b*sqrt(2) by exact integer comparisons, using a Pell sandwich.
def qsign(a,b):
 if not b:return (a>0)-(a<0)
 if a>=0 and b>0:return 1
 if a<=0 and b<0:return -1
 c=a*a-2*b*b
 return ((c>0)-(c<0))*(1 if a>0 else -1)
def qfloor(a,b):
 approx=Fraction(isqrt(2*10**24),10**12)
 v=(a+b*approx).__floor__()
 while qsign(a-v,b)<0:v-=1
 while qsign(a-v-1,b)>=0:v+=1
 return v
@lru_cache(None)
def st(n):
 # Cutting points {-k*alpha}, k=0..n. Lower/upper word closures have same language.
 pts=[]
 for k in range(n+1):
  a,b=Fraction(k),Fraction(-k);f=qfloor(a,b);pts.append((a-f,b))
 pts.append((Fraction(1),Fraction(0)))
 from functools import cmp_to_key
 pts.sort(key=cmp_to_key(lambda x,y:qsign(x[0]-y[0],x[1]-y[1])))
 ans=set()
 for x,y in zip(pts,pts[1:]):
  a=(x[0]+y[0])/2;b=(x[1]+y[1])/2
  ans.add(tuple(qfloor(a-k-1,b+k+1)-qfloor(a-k,b+k) for k in range(n)))
 return tuple(sorted(ans))
@lru_cache(None)
def patterns(n,m):
 return tuple(sorted(tuple(tuple((u[i+j],u[i+j+1],v[j]) for i in range(n)) for j in range(m)) for u,v in product(tm(n+m),st(m))))
def crop(p,k,n,m):return tuple(tuple(r[k:k+n]) for r in p[k:k+m])
@lru_cache(None)
def complex(n):
 groups=[patterns(n,n),patterns(n+1,n),patterns(n,n+1),patterns(n+1,n+1)]
 v,h,w,f=groups;ix=[{p:i for i,p in enumerate(g)} for g in groups]
 d1=zero(len(v),len(h)+len(w));d2=zero(len(h)+len(w),len(f))
 for typ,g in enumerate([h,w]):
  for j,p in enumerate(g):
   start=tuple(tuple(r[:n]) for r in p[:n])
   # Explicit shifts avoid boolean precedence ambiguities.
   end=tuple(tuple(r[(1 if typ==0 else 0):(n+1 if typ==0 else n)]) for r in p[(1 if typ==1 else 0):(n+1 if typ==1 else n)])
   col=j+(len(h) if typ else 0);d1[ix[0][start]][col]-=1;d1[ix[0][end]][col]+=1
 for j,p in enumerate(f):
  bottom=tuple(tuple(r) for r in p[:n]);top=tuple(tuple(r) for r in p[1:n+1]);left=tuple(tuple(r[:n]) for r in p);right=tuple(tuple(r[1:n+1]) for r in p)
  d2[ix[1][bottom]][j]+=1;d2[ix[1][top]][j]-=1;d2[len(h)+ix[2][right]][j]+=1;d2[len(h)+ix[2][left]][j]-=1
 return [v,h+w,f],d1,d2,len(h)
def mapchain(n,m):
 small,a,b,hs=complex(n);big,c,d,hl=complex(m);k=(m-n)//2;maps=[]
 for degree in range(3):
  ind={p:i for i,p in enumerate(small[degree])};out=zero(len(small[degree]),len(big[degree]))
  for j,p in enumerate(big[degree]):
   nx=n+int(degree==2 or degree==1 and j<hl);ny=n+int(degree==2 or degree==1 and j>=hl)
   out[ind[crop(p,k,nx,ny)]][j]=1
  maps.append(out)
 return maps
# Homology-image block rank uses target boundaries and source cycle constraints.
def hom_image(ds,bt,f):
 rows=[r+[0]*len(bt[0]) for r in ds]+[r+b for r,b in zip(f,bt)]
 return rank(rows)-rank(ds)-rank(bt)
records=[]
for n in range(1,10):
 ck(len(st(n))==n+1,'sturmian_count')
 ck(len(tm(n+1))-len(tm(n)) in [2,4],'thue_morse_increment')
for n in range(1,7):
 cells,d1,d2,hs=complex(n);nv,ne,nf=map(len,cells);r1,r2=rank(d1),rank(d2)
 ck(all(not v for r in mm(d1,d2) for v in r),'boundary_squared')
 betti=[nv-r1,ne-r1-r2,nf-r2]
 ck(betti[0]==1,'connectedness');ck(sum([nv,-ne,nf])==betti[0]-betti[1]+betti[2],'euler_betti')
 ck(nv==len(tm(2*n))*(n+1),'rectangle_complexity')
 records.append({'scale':n,'cells':[nv,ne,nf],'betti':betti})
images=[]
for n,m in [(1,3),(2,4),(2,6),(1,5),(3,5),(4,6)]:
 s,a,b,hs=complex(n);l,c,d,hl=complex(m);f0,f1,f2=mapchain(n,m)
 ck(mm(a,f1)==mm(f0,c),'chain_map_1');ck(mm(b,f2)==mm(f1,d),'chain_map_2')
 h1=hom_image(c,b,f1)
 h2=rank(d+f2)-rank(d)
 if (n,m) in [(1,3),(2,4),(2,6)]:ck([h1,h2]=={(1,3):[4,4],(2,4):[4,6],(2,6):[4,4]}[(n,m)],'published_image')
 images.append({'from':n,'to':m,'H1':h1,'H2':h2})
for n,m,j in [(1,3,5),(2,4,6)]:
 f=mapchain(n,m);g=mapchain(m,j);h=mapchain(n,j)
 for degree in range(3):ck(mm(f[degree],g[degree])==h[degree],'cropping_composite')
# Build stationary collar matrix from complete substituted strings, not the asserted formula.
v=tuple(sorted(tm(2)));e=tuple(sorted(tm(3)));d=zero(len(v),len(e));M=zero(len(e),len(e));N=zero(len(v),len(v))
for j,p in enumerate(e):
 d[v.index(p[1:])][j]+=1;d[v.index(p[:2])][j]-=1
 expanded=tuple(c for a in p for c in ((0,1) if a==0 else (1,0)))
 for off in (1,2):M[e.index(expanded[off:off+3])][j]+=1
for j,p in enumerate(v):N[v.index((1-p[0],p[1]))][j]=1
ck(mm(d,M)==mm(N,d),'stationary_chain')
# Independent cycle-space image calculation at powers rather than asserted cycle basis.
q=M
survival=[]
for power in range(1,6):
 h=hom_image(d,zero(6,0),q);ck(h==2,'stationary_H1_rank');survival.append(h);q=mm(M,q)
# Linear algebra stress controls, including non-square maps and adversarial zero maps.
ck(rank([[1,2],[2,4]])==1,'rank_control');ck(rank([[0,0],[0,0]])==0,'rank_control');ck(rank([[1,2,3],[0,1,2]])==2,'rank_control')
result={'checks':sum(checks.values()),'categories':checks,'pattern_betti':records,'homology_image_ranks':images,'stationary_H1_image_ranks':survival,'method':'independently assembled integer chains; primitive sparse integer row elimination computes exact rational ranks; homology block-rank images avoid candidate cochain cocycle-basis routine','elapsed_seconds':time.monotonic()-START}
print(json.dumps(result,indent=2,sort_keys=True))
