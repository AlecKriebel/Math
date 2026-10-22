#!/usr/bin/env python3
"""Fresh certificate checker: direct rational atanh powers, 64 bits / 24 terms.
Reads only JSON data. Does not import or execute either upstream or author code.
"""
from fractions import Fraction as Q
from pathlib import Path
from functools import lru_cache
from itertools import permutations,product
from math import isqrt
from hashlib import sha256
import json
BASE=1<<64; TERMS=24;counts={}
def check(t,g):
 if not t:raise AssertionError(g)
 counts[g]=counts.get(g,0)+1
def ceil(n,d):return -((-n)//d)
def direct_series(a,b):
 # Each power and denominator below is an exact integer; no rounded-power recurrence.
 assert 0<=3*a<=b
 lo=hi=0;ap=a;bp=b;aa=a*a;bb=b*b
 for j in range(TERMS):
  num=2*BASE*ap;den=(2*j+1)*bp
  lo+=num//den;hi+=ceil(num,den)
  ap*=aa;bp*=bb
 hi+=ceil(9*BASE,4*(2*TERMS+1)*3**(2*TERMS+1))
 return lo,hi
L2=direct_series(1,3)
@lru_cache(None)
def logs(x):
 check(x>0,'log positive domain')
 n,d=x.numerator,x.denominator;k=0
 while n<d:n*=2;k-=1
 while n>=2*d:d*=2;k+=1
 lo,hi=direct_series(n-d,n+d)
 if k>=0:return lo+k*L2[0],hi+k*L2[1]
 return lo+k*L2[1],hi+k*L2[0]
# Certified irrational star probabilities with a different precision from both prior checkers.
slo=Q(isqrt(3*BASE*BASE),BASE);shi=slo+Q(1,BASE)
check(slo*slo<3<shi*shi,'strict quadratic interval')
def aff(c,d):return (c+d*slo,c+d*shi) if d>=0 else (c+d*shi,c+d*slo)
star_coeff=[(Q(1,4),Q(0)),(Q(1,2),Q(-1,4)),(Q(1,2),Q(-1,4)),(Q(-3,4),Q(1,2)),(Q(1,2),Q(-1,4)),(Q(-3,4),Q(1,2)),(Q(-3,4),Q(1,2)),(Q(3,2),Q(-3,4))]
starlog=[]
for c,d in star_coeff:
 low,high=aff(c,d);check(low>0,'star probability positive');starlog.append((logs(low)[0],logs(high)[1]))
c_lower=-Q(3,4)*logs(2*shi-3)[1]
E=tuple(Q(int(i.bit_count()%2==0),4) for i in range(8));O=tuple(Q(1,4)-x for x in E)
def point(i):return tuple(Q(i==j) for j in range(8))
reps=[(0,7),(0,3,5),(0,1,2,7),(0,3,5,6),(0,1,2,4,7),(0,1,2,5,6,7)]
names=['two','three','four','parity','five','six']
def initial(support):
 if support in [reps[3],reps[4]]:
  parity=support if len(support)==4 else tuple(x for x in support if x)
  for order in permutations(parity):
   vs=tuple(tuple(Q(int(x in order[:j]),j) for x in range(8)) for j in range(1,5))
   yield vs if len(support)==4 else (point(0),)+vs
 else:yield tuple(point(i) for i in support)
# Independent support classification uses binary strings and coordinate deletion.
def erase(bits,i):return bits[:i]+bits[i+1:]
vertices=[tuple(map(int,format(x,'03b'))) for x in range(8)]
irr=set()
for mask in range(1,256):
 S={x for x in range(8) if mask&(1<<x)}
 reducible=False
 for i in range(3):
  slices=[{erase(vertices[x],i) for x in S if vertices[x][i]==b} for b in (0,1)]
  if slices[0]<=slices[1] or slices[1]<=slices[0]:reducible=True
 if not reducible:irr.add(tuple(sorted(S)))
orbits=[]
for rep in reps:
 orb=set()
 for perm in permutations(range(3)):
  for flips in product((0,1),repeat=3):
   transformed=[]
   for x in rep:
    bits=[vertices[x][perm[j]]^flips[j] for j in range(3)]
    transformed.append(4*bits[0]+2*bits[1]+bits[2])
   orb.add(tuple(sorted(transformed)))
 orbits.append(orb)
check(set().union(*orbits)==irr,'all support orbits covered')
check([len(o) for o in orbits]==[4,8,24,2,8,4],'orbit multiplicities')
check(sum(map(len,orbits))==len(irr)==50,'orbit disjointness')
@lru_cache(None)
def ent(v):return sum((p*logs(p)[1] for p in v if p),Q(0))
@lru_cache(None)
def mixed_log(den,ns):
 check(den>0 and len(ns)==7 and all(0<=x<=den for x in ns),'mixture closed parameter cube')
 lam,*v=[Q(x,den) for x in ns];q=[]
 for bits in vertices:
  terms=[]
  for weight,params in [(lam,v[:3]),(1-lam,v[3:])]:
   prod=weight
   for bit,t in zip(bits,params):prod*=t if bit else 1-t
   terms.append(prod)
  q.append(sum(terms))
 check(sum(q)==1 and min(q)>=0,'mixture probability normalization')
 return tuple(logs(x) if x else None for x in q)
def certificate(path,rep):
 obj=json.loads(path.read_text());check(obj['format']=='rbm31-convex-cover-v1','format')
 check(tuple(obj['support'])==rep,'support convention')
 tree={}
 for rec in obj['splits']:
  check(rec['path'] not in tree,'unique record address');tree[rec['path']]=('split',rec['edge'])
 for rec in obj['leaves']:
  check(rec['path'] not in tree,'unique record address');tree[rec['path']]=('leaf',rec['witness'])
 todo=[(str(j)+':',simplex,0) for j,simplex in enumerate(initial(rep))]
 reached=set();leafcount=incidences=eq=depth=0;minimum=None
 while todo:
  address,vs,d=todo.pop();depth=max(depth,d)
  check(address in tree and address not in reached,'complete acyclic tree');reached.add(address)
  kind,rec=tree[address]
  if kind=='split':
   i,j=rec;check(type(i)==int and type(j)==int and 0<=i<len(vs) and 0<=j<len(vs) and i!=j,'proper edge subdivision')
   mid=tuple((x+y)/2 for x,y in zip(vs[i],vs[j]))
   for digit,index in [('0',i),('1',j)]:
    child=list(vs);child[index]=mid;todo.append((address+digit,tuple(child),d+1))
  else:
   leafcount+=1
   if rec['kind']=='mixture':
    check(type(rec['denominator'])==int and all(type(n)==int for n in rec['numerators']),'integer witness data')
    qlogs=mixed_log(rec['denominator'],tuple(rec['numerators']));atom=None
   else:
    check(rec['kind']=='star' and type(rec['atom'])==int and 0<=rec['atom']<8,'star witness data');atom=rec['atom'];qlogs=tuple(starlog[x^atom] for x in range(8))
   for v in vs:
    incidences+=1;check(sum(v)==1 and min(v)>=0,'continuous simplex vertex validity')
    if v==E or v==O:
     check(atom is not None and atom.bit_count()%2==int(v==O),'exact analytic parity equality');eq+=1
    else:
     check(all(not p or qlogs[x] is not None for x,p in enumerate(v)),'finite KL witness')
     upper=ent(v)-sum((p*qlogs[x][0] for x,p in enumerate(v) if p),Q(0))
     margin=c_lower-upper;check(margin>0,'rigorous strict KL vertex bound')
     minimum=margin if minimum is None else min(minimum,margin)
 check(reached==set(tree),'all records reached')
 result={'file':path.name,'sha256':sha256(path.read_bytes()).hexdigest(),'roots':sum(1 for _ in initial(rep)),'leaves':leafcount,'vertex_incidences':incidences,'parity_incidences':eq,'max_depth':depth,'minimum_strict_margin_nats':str(minimum/BASE)}
 print(json.dumps(result),flush=True);return result
if __name__=='__main__':
 root=Path(__file__).resolve().parent
 results=[certificate(root/'certificates'/f'{name}.json',rep) for name,rep in zip(names,reps)]
 result={'verdict':'PASS','assertions':sum(counts.values()),'groups':counts,'scale_bits':64,'series_terms':24,'log_method':'Exact integer powers with separate direct quotient rounding; no rounded-power recurrence','certificates':results,'total_leaves':sum(x['leaves'] for x in results),'total_vertex_incidences':sum(x['vertex_incidences'] for x in results),'total_parity_incidences':sum(x['parity_incidences'] for x in results),'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'producer_code_executed':False,'author_code_imported':False}
 (root/'independent_cover_results.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',result['assertions'])
