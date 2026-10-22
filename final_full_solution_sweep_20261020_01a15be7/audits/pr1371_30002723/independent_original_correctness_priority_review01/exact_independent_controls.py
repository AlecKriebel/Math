"""Independent finite diagnostics. No author imports; not an AHT implementation."""
from fractions import Fraction as Q
from itertools import combinations,product
import random,json,hashlib,sys
from pathlib import Path
DIRS=((0,0),(1,0),(0,1),(-1,0),(0,-1),(1,-1),(-1,1),(1,1),(-1,-1),(2,-1),(1,-2),(-2,1),(-1,2))
def check(t,m):
 if not t: raise RuntimeError(m)
def rank(rows):
 piv={}
 for row in rows:
  r={i:Q(x) for i,x in enumerate(row) if x}
  while r:
   k=min(r)
   if k not in piv:
    a=r[k];piv[k]={i:x/a for i,x in r.items()};break
   a=r[k]
   for i,b in piv[k].items():
    r[i]=r.get(i,Q(0))-a*b
    if not r[i]: del r[i]
 return len(piv)
def vec(N,terms):
 a=[0]*(3*N)
 for k,v in terms:a[k]+=v
 return a
def add(*terms):return [sum(a) for a in zip(*terms)]
def neg(a):return [-x for x in a]
def val(N,k,d):
 k%=N
 return vec(N,[(2*N+k,1)]) if not d else vec(N,[(k,1)]) if d>0 else vec(N,[(N+(k-1)%N,1)])
def slope(N,k):k%=N;return vec(N,[(N+k,1),(k,-1)])
def jump(N,k):k%=N;return vec(N,[(k,1),(N+(k-1)%N,-1)])
def spike(N,k):k%=N;return vec(N,[(2*N+k,2),(k,-1),(N+(k-1)%N,-1)])
def inside(bounds,v,d):
 for (a,b),x,t in zip(bounds,(v[0],v[1],v[0]+v[1]),(d[0],d[1],d[0]+d[1])):
  if a==b:
   if x!=a or t: return False
  elif not(a<=x<=b) or (x==a and t<=0) or (x==b and t>=0): return False
 return True
def vertices(bounds):
 lines=[(1,0,t) for t in bounds[0]]+[(0,1,t) for t in bounds[1]]+[(1,1,t) for t in bounds[2]]
 vs=set()
 for (a,b,c),(d,e,f) in combinations(lines,2):
  det=a*e-b*d
  if det:
   x=Q(c*e-b*f,det);y=Q(a*f-c*d,det)
   if all(l<=z<=u for (l,u),z in zip(bounds,(x,y,x+y))):vs.add((x,y))
 vs=tuple(sorted(vs))
 if not vs:return ()
 cen=(sum(v[0] for v in vs)/len(vs),sum(v[1] for v in vs)/len(vs))
 if not inside(bounds,cen,(0,0)):return ()
 return vs
def dim(vs):
 if len(vs)==1:return 0
 a,b=vs[:2]
 return 2 if any((b[0]-a[0])*(c[1]-a[1])!=(b[1]-a[1])*(c[0]-a[0]) for c in vs[2:]) else 1
def linear(v,c):return c[0]*v[0]+c[1]*v[1]+c[2]
def residual(N,bounds,vs,c,drop_rays=False):
 out=[]
 for x,y in vs:
  if linear((x,y),c):continue
  for dx,dy in DIRS:
   if drop_rays and (not dx or not dy or not dx+dy):continue
   if inside(bounds,(x,y),(dx,dy)):
    out.append(add(val(N,int(x),dx),val(N,int(y),dy),neg(val(N,int(x+y),dx+dy))))
 return out
def dense(N,bounds,c):
 rows=[]
 for x,y in product(range(N+1),repeat=2):
  if linear((x,y),c):continue
  for dx,dy in DIRS:
   if inside(bounds,(x,y),(dx,dy)):
    rows.append(add(val(N,x,dx),val(N,y,dy),neg(val(N,x+y,dx+dy))))
 return rows
def local(N,bounds,vs,c,mut=''):
 out=residual(N,bounds,vs,c,mut=='omit_rays')
 d=dim(vs);zeros=[v for v in vs if not linear(v,c)]
 if not zeros:return out
 def projections(v):return [(int(min(f(t) for t in v)),int(max(f(t) for t in v))) for f in (lambda t:t[0],lambda t:t[1],lambda t:t[0]+t[1])]
 def force(ranges):
  for a,b in ranges:
   for k in range(a+1,b):out.extend((jump(N,k),spike(N,k)))
 def pair(edge,forced=False):
  pr=projections(edge)
  fixed=next(i for i,(a,b) in enumerate(pr) if a==b)
  inds=[i for i in range(3) if i!=fixed];a,b=inds;t=pr[fixed][0]
  for k in range(*pr[a]):
   j=t-k-(0 if mut=='reflection_cell' else 1) if fixed==2 else k+t
   out.append(add(slope(N,k),neg(slope(N,j))))
  if forced:force([pr[a],pr[b]])
  else:
   for k in range(pr[a][0]+1,pr[a][1]):
    j=t-k if fixed==2 else k+t
    # Independent derivation: reflected jumps match; reflected point spikes oppose.
    s=-1 if mut=='reflected_jump' and fixed==2 else 1
    out.append(add(jump(N,k),[-s*z for z in jump(N,j)]))
    out.append(add(spike(N,k),[z*(1 if fixed==2 else -1) for z in spike(N,j)]))
 if d==2 and len(zeros)==len(vs):
  pr=projections(vs);cells=[k for a,b in pr for k in range(a,b)]
  for k in cells[1:]:out.append(add(slope(N,cells[0]),neg(slope(N,k))))
  force(pr)
 elif d==1 and len(zeros)==len(vs):pair(vs)
 elif d==2 and len(zeros)>1:pair(zeros,True)
 return out

def local_checks():
 cases=[];mutations={k:None for k in ('omit_rays','reflection_cell','reflected_jump')}
 # N=8 and 12 are 4q; sparse original grids include asymmetric/wrapped projections.
 for N,B in [(8,[0,4,8]),(12,[0,4,8,12]),(12,[0,4,12])]:
  fs=[(b,b) for b in B]+list(zip(B,B[1:]));ks=[(b,b) for b in sorted(set(B+[b+N for b in B]))]+list(zip(sorted(set(B+[b+N for b in B])),sorted(set(B+[b+N for b in B]))[1:]))
  found=[]
  for bounds in product(fs,fs,ks):
   vs=vertices(bounds)
   if not vs:continue
   coeffs={(0,0,0)}
   for (a,b),ab in zip(bounds,((1,0),(0,1),(1,1))):
    coeffs.update(((ab[0],ab[1],-a),(-ab[0],-ab[1],b)))
   for u,v in combinations(tuple(coeffs),2):coeffs.add(tuple(x+y for x,y in zip(u,v)))
   for c in sorted(coeffs):
    z=[linear(v,c) for v in vs]
    if min(z)<0 or min(z)>0:continue
    found.append((bounds,vs,c))
  # Deterministic coverage sample, retaining every geometry/type plus random support choices.
  rr=random.Random(1371+N+len(B));rr.shuffle(found)
  seen=set();selected=[]
  for bounds,vs,c in found:
   sig=(bounds,dim(vs),sum(not linear(v,c) for v in vs))
   if sig not in seen:seen.add(sig);selected.append((bounds,vs,c))
  for bounds,vs,c in selected:
   a=dense(N,bounds,c);b=local(N,bounds,vs,c)
   ra,rb,rab=rank(a),rank(b),rank(a+b)
   check(ra==rb==rab,('local rowspace',N,bounds,c,ra,rb,rab))
   cases.append({'N':N,'bounds':bounds,'zero_affine':c,'dimension':dim(vs),'zero_vertices':sum(not linear(v,c) for v in vs),'dense_rows':len(a),'sparse_rows':len(b),'rank':ra})
   for mut in mutations:
    if mutations[mut] is None:
     m=local(N,bounds,vs,c,mut)
     if rank(m)!=ra or rank(m+a)!=ra:mutations[mut]={'N':N,'bounds':bounds,'zero_affine':c,'reference_rank':ra,'mutant_rank':rank(m),'joint_rank':rank(m+a)}
 check(all(mutations.values()),('undetected local mutation',mutations))
 return cases,mutations
class DSU:
 def __init__(s,n):s.p=list(range(n))
 def find(s,x):
  while s.p[x]!=x:s.p[x]=s.p[s.p[x]];x=s.p[x]
  return x
 def join(s,a,b):s.p[s.find(a)]=s.find(b)
 def count(s):return len({s.find(i) for i in range(len(s.p))})
def orbit_info(N,edges,zeros):
 u=DSU(N);l=DSU(2*N)
 for a,b,sgn in edges:
  u.join(a,b)
  for e in range(2):l.join(a+e*N,b+(e^(sgn<0))*N)
 for z in zeros:l.join(z,z+N)
 return u,l,l.count()-u.count()
def graph_checks():
 rr=random.Random(30002723);stats={'cases':0,'free_components':0,'cutoff_examples':0,'balanced':0,'unbalanced':0,'forced':0,'negative_prefixes':0}
 hashout=hashlib.sha256()
 for N in range(2,18):
  for trial in range(24):
   edges=[]
   for _ in range(rr.randrange(0,7)):
    length=rr.randrange(1,N+1);a=rr.randrange(N-length+1);b=rr.randrange(N-length+1);rev=rr.randrange(2);sgn=rr.choice((-1,1))
    edges.extend((a+i,b+length-i-1 if rev else b+i,sgn) for i in range(length))
   zeros={i for i in range(N) if rr.randrange(11)==0}
   u,l,D=orbit_info(N,edges,zeros)
   rows=[vec(N,[(a,1),(b,-sgn)])[:N] for a,b,sgn in edges]+[vec(N,[(z,1)])[:N] for z in zeros]
   check(N-rank(rows)==D,('signed dimension',N,trial))
   reps=[];killed=set(zeros)
   while orbit_info(N,edges,killed)[2]:
    old=orbit_info(N,edges,killed)[2];lo,hi=0,N-1
    while lo<hi:
     mid=(lo+hi)//2
     if orbit_info(N,edges,killed|set(range(mid+1)))[2]<old:hi=mid
     else:lo=mid+1
    check(orbit_info(N,edges,killed|{lo})[2]==old-1,'prefix singleton')
    reps.append(lo);killed.add(lo)
   check(len(reps)==D,'reps')
   basis=[]
   for r in reps:
    root=l.find(r);check(root!=l.find(r+N),'balanced marked')
    v=[int(l.find(i)==root)-int(l.find(i+N)==root) for i in range(N)]
    check(v[r]==1 and all(v[a]==sgn*v[b] for a,b,sgn in edges) and all(not v[z] for z in zeros),'basis')
    # Nonnegative separate-sheet indicator weights, then subtraction.
    for t in range(N+1):
     plus=sum(l.find(i)==root for i in range(t));minus=sum(l.find(i+N)==root for i in range(t))
     check(plus-minus==sum(v[:t]),'weighted prefix')
     stats['negative_prefixes']+=plus<minus
    basis.append(v)
   check(rank(basis)==D,'basis independence')
   check(all(sum(row[i]*v[i] for i in range(N))==0 for row in rows for v in basis),'basis kernel')
   stats['cases']+=1;stats['free_components']+=D;stats['cutoff_examples']+=D>2
   stats['forced']+=bool(zeros);stats['unbalanced']+=any(l.find(i)==l.find(i+N) for i in range(N));stats['balanced']+=D>0
   hashout.update(json.dumps([N,edges,sorted(zeros),D,reps,basis],separators=(',',':')).encode())
 check(stats['negative_prefixes']>0 and stats['cutoff_examples']>0,'edge coverage')
 stats['trace_sha256']=hashout.hexdigest();return stats

def global_checks():
 out=[]
 models=[('continuous_GMI',8,[0,4,8],[Q(0),Q(1)],[Q(0),Q(1)],[Q(1),Q(0)]),
 ('two_sided_point_spikes',8,[0,4,8],[Q(0),Q(1)],[Q(1,2),Q(1,2)],[Q(1,2),Q(1,2)]),
 ('two_sided_with_nonzero_slopes',8,[0,4,8],[Q(0),Q(1)],[Q(1,8),Q(7,8)],[Q(7,8),Q(1,8)]),
 ('same_grid_shortcut_counterexample',20,[0,4,8,16,20],[Q(0),Q(1),Q(1,3),Q(2,3)],[Q(0),Q(1),Q(1,3),Q(2,3)],[Q(1),Q(1,3),Q(2,3),Q(0)])]
 for name,N,B,P,L,R in models:
  def affine(interval):
   a,b=interval;offset=(a//N)*N if a==b else (Q(a+b,2)//N)*N
   if a==b:return Q(0),P[B.index(a%N)]
   i=B.index(a-offset);m=(R[i]-L[i])/(b-a);return m,L[i]-m*a
  def pi(k,d):
   k%=N
   if not d and k in B:return P[B.index(k)]
   if d<0 and k in B:
    kk=k or N;i=B.index(kk)-1
   else:kk=k;i=next(i for i,(a,b) in enumerate(zip(B,B[1:])) if a<=kk<b)
   return L[i]+(R[i]-L[i])*Q(kk-B[i],B[i+1]-B[i])
  for k in range(N):
   for d in (-1,0,1):
    check(Q(0)<=pi(k,d)<=Q(1),('minimality/bounds',name,k,d))
    check(pi(k,d)+pi(B[1]-k,-d)==1,('minimality/symmetry',name,k,d))
  fs=[(b,b) for b in B]+list(zip(B,B[1:]));B2=sorted(set(B+[b+N for b in B]));ks=[(b,b) for b in B2]+list(zip(B2,B2[1:]))
  da=[val(N,0,0),val(N,B[1],0)];sp=da[:];faces=0;tight=0
  for bounds in product(fs,fs,ks):
   vs=vertices(bounds)
   if not vs:continue
   (mi,bi),(mj,bj),(mk,bk)=map(affine,bounds);c=(mi-mk,mj-mk,bi+bj-bk)
   check(min(linear(v,c) for v in vs)>=0,('minimality/subadditivity',name,bounds))
   if not any(not linear(v,c) for v in vs):continue
   a=dense(N,bounds,c);b=local(N,bounds,vs,c);da.extend(a);sp.extend(b);faces+=1;tight+=len(a)
  rd,rs,rj=rank(da),rank(sp),rank(da+sp)
  check(rd==rs==rj,('global rowspace',name,rd,rs,rj))
  check((3*N-rd==0)==(name=='continuous_GMI'),('expected extremality',name,rd))
  out.append({'model':name,'N':N,'point_variables':N,'independent_interval_endpoint_variables':2*N,'active_coarse_incidents':faces,'complete_tight_rows':tight,'rank':rd,'kernel_dimension':3*N-rd,'two_sided_at_origin':L[0]!=0 and R[-1]!=0})
 return out

def main():
 cases,mutations=local_checks();graphs=graph_checks();global_models=global_checks()
 result={'status':'PASS','arithmetic':'exact Python Fraction/int; explicit exceptions remain active under optimization','boundary':'finite diagnostics only; no complexity inference and no author code executed','local_case_count':len(cases),'local_cases_by_dimension':{str(d):sum(t['dimension']==d for t in cases) for d in range(3)},'local_cases_sha256':hashlib.sha256(json.dumps(cases,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'detected_local_mutants':mutations,'graphs':graphs,'global_models':global_models,'local_cases':cases}
 print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
