#!/usr/bin/env python3
"""Independent certificate check in Q(sqrt(5)), via Gaussian elimination.
Does not import producers or use their wedge canonicalization.
Rank-three completeness is proved by exact independent-triple counting.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
from math import comb
from pathlib import Path
import json, hashlib, argparse, time
O=(F(0),F(0));U=(F(1),F(0))
def plus(x,y):return(x[0]+y[0],x[1]+y[1])
def minus(x,y):return(x[0]-y[0],x[1]-y[1])
def times(x,y):return(x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def over(x,y):
 n=y[0]*y[0]-5*y[1]*y[1]
 if n==0:raise ZeroDivisionError
 return times(x,(y[0]/n,-y[1]/n))
def dot(x,y):
 out=O
 for a,b in zip(x,y):out=plus(out,times(a,b))
 return out

def parsevec(v):return tuple((F(a)+F(b)/2,F(b)/2) for a,b in v)
def normal(v):
 z=next(x for x in v if x!=O)
 return tuple(over(x,z) for x in v)

def rref(rows):
 out=[list(v) for v in rows];h=0;piv=[];n=len(rows[0])
 for j in range(n):
  k=next((k for k in range(h,len(out)) if out[k][j]!=O),None)
  if k is None:continue
  out[k],out[h]=out[h],out[k];x=out[h][j];out[h]=[over(y,x) for y in out[h]]
  for k in range(len(out)):
   if k==h or out[k][j]==O:continue
   x=out[k][j];out[k]=[minus(a,times(x,b)) for a,b in zip(out[k],out[h])]
  piv.append(j);h+=1
  if h==len(out):break
 return tuple(tuple(v) for v in out[:h]),piv

def annihilator(rows):
 rr,piv=rref(rows);n=len(rows[0]);out=[]
 for j in range(n):
  if j in piv:continue
  v=[O]*n;v[j]=U
  for i,k in enumerate(piv):v[k]=minus(O,rr[i][j])
  out.append(tuple(v))
 return rr,out

def check_flats(r,flats,rank):
 keys=set();membersets=[]
 for f in flats:
  s=f['members'];assert s==sorted(set(s)) and len(s)>=rank
  rr,ann=annihilator([r[i] for i in s]);assert len(rr)==rank
  assert rr not in keys;keys.add(rr)
  members={i for i,v in enumerate(r) if all(dot(v,a)==O for a in ann)}
  assert members==set(s)
  membersets.append(members)
 return membersets

def check_reflection_model(d,r):
 model=d['reflection_model'];bs=[parsevec(v) for v in model['simple_roots']];assert len(rref(bs)[0])==4
 rr=set(r);seen={normal(v) for v in bs};todo=list(seen)
 while todo:
  v=todo.pop()
  for s in bs:
   c=over(times((F(2),F(0)),dot(v,s)),dot(s,s))
   w=normal(tuple(minus(a,times(c,b)) for a,b in zip(v,s)))
   assert w in rr
   if w not in seen:seen.add(w);todo.append(w)
 assert rr==seen
 expected=[(F(1,4),F(0)),(F(1,2),F(0)),(F(1,4),F(0))] if d['type']=='F4' else [(F(3,8),F(1,8)),(F(1,4),F(0)),(F(1,4),F(0))]
 for i,j in combinations(range(4),2):
  z=dot(bs[i],bs[j])
  if j-i>1:assert z==O
  else:
   assert over(times(z,z),times(dot(bs[i],bs[i]),dot(bs[j],bs[j])))==expected[i]
   # Exact negativity in the positive square-root embedding.
   a,b=z
   assert (a<0 and b<=0) or (a>=0 and b<0 and a*a<5*b*b) or (a<0 and b>0 and a*a>5*b*b)
 return len(seen)

def check_ambient(d):
 r=[parsevec(v) for v in d['hyperplanes']];assert len(set(normal(v) for v in r))==len(r)
 check_reflection_model(d,r)
 f2=check_flats(r,d['rank2_flats'],2)
 pairs=Counter(pair for s in f2 for pair in combinations(sorted(s),2));assert len(pairs)==comb(len(r),2) and set(pairs.values())=={1}
 f3=check_flats(r,d['rank3_flats'],3)
 # Complete, distinct closed rank-three spans cannot share an independent triple.
 independent=comb(len(r),3)-sum(comb(len(s),3) for s in f2)
 covered=sum(comb(len(s),3)-sum(comb(len(t),3) for t in f2 if t<=s) for s in f3)
 assert independent==covered
 profiles=Counter()
 for s,f in zip(f3,d['rank3_flats']):
  loc=Counter(len(t) for t in f2 if t<=s);assert {str(k):v for k,v in loc.items()}==f['rank2_profile']
  profiles[str((len(s),tuple(sorted(loc.items()))))]+=1
 assert dict(profiles)==d['rank3_profiles']
 counts=Counter(len(s) for s in f2);assert {str(k):v for k,v in counts.items()}==d['rank2_multiplicity_counts']
 b2=sum(len(s)-1 for s in f2)
 b3=sum(1-len(s)+sum(len(t)-1 for t in f2 if t<=s) for s in f3)
 b4=-1+len(r)-b2+b3
 central=[1,len(r),b2,b3,b4];projective=[1,len(r)-1,b2-len(r)+1,b4]
 return {'type':d['type'],'hyperplanes':len(r),'rank2_flats':len(f2),'rank3_flats':len(f3),'independent_triples':independent,'covered_independent_triples':covered,'central_betti':central,'projective_betti':projective,'projective_euler':sum((-1)**i*b for i,b in enumerate(projective)),'rank2_counts':dict(counts),'rank3_profiles':dict(profiles)}

def check_restriction(d,ambient):
 r=[parsevec(v) for v in d['hyperplanes']];ar=[parsevec(v) for v in ambient['hyperplanes']];h=parsevec(d['selected_mirror_normal']);bs=[parsevec(v) for v in d['mirror_basis']]
 assert len(rref(bs)[0])==3 and all(dot(v,h)==O for v in bs)
 expected=set()
 for a in ar:
  v=tuple(dot(a,b) for b in bs)
  if any(x!=O for x in v):expected.add(normal(v))
 assert expected==set(r)
 f2=check_flats(r,d['rank2_flats'],2);pairs=Counter(pair for s in f2 for pair in combinations(sorted(s),2));assert len(pairs)==comb(len(r),2) and set(pairs.values())=={1}
 counts=Counter(len(s) for s in f2);b2=sum(len(s)-1 for s in f2);b3=1-len(r)+b2
 assert d['central_betti']==[1,len(r),b2,b3]
 assert d['projective_betti']==[1,len(r)-1,b3]
 return {'type':d['ambient_type'],'hyperplanes':len(r),'rank2_counts':dict(counts),'central_betti':d['central_betti'],'projective_euler':2-len(r)+b3}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--directory',default=str(Path(__file__).resolve().parent));p.add_argument('--output',required=True);args=p.parse_args();base=Path(args.directory);start=time.monotonic()
 a=json.loads((base/'arrangement_certificate.json').read_text())['types'];restr=json.loads((base/'restriction_certificate.json').read_text())
 out={'status':'PASS','independent_method':'Q(sqrt5) Gaussian elimination, reflection orbit closure and independent-triple counting', 'ambient':[check_ambient(x) for x in a],'restrictions':[check_restriction(x,y) for x,y in zip(restr,a)],'elapsed_seconds':time.monotonic()-start,'input_sha256':{n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in ('arrangement_certificate.json','restriction_certificate.json')}}
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
