#!/usr/bin/env python3
"""Fresh certificate consumer/arithmetical witness check; no published module imports.

Coefficients are reconstructed in a unital polynomial array. The committed rows
contain transcript commitments; full deterministic transcripts are independently
regenerated and consumed, then checked against each commitment.
"""
from pathlib import Path
from hashlib import sha256
from itertools import product
import json,copy
BASE=Path(__file__).resolve().parent
FIN=BASE/'tmp/extracted/audit/reviews/finite_01'
V=[v for v in range(32) if v.bit_count()%2==0]
BV=[17,18,20,24]
Z=(0,0,0);X=(1,0,0);A=(125,0,0);B=(0,0,1)
BASIS=[(5**j,0,0) for j in range(4)]+[(0,v,0) for v in BV]+[B]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def coeff(n):return [0]+[n//5**j%5 for j in range(4)]
def encode(c):return sum(c[j]%5*5**(j-1) for j in range(1,5))
def plusp(a,b):return [(x+y)%5 for x,y in zip(a,b)]
def mulp(a,b):return [sum(a[j]*b[k-j] for j in range(k+1))%5 for k in range(5)]
def scale(a,n):return encode([n*x%5 for x in coeff(a[0])]),a[1] if n%2 else 0,a[2] if n%2 else 0
def plus(a,b):return encode(plusp(coeff(a[0]),coeff(b[0]))),a[1]^b[1],a[2]^b[2]
def minus(a,b):return plus(a,scale(b,-1))
def bet(a,b):return sum((a>>j&1)*(b>>j&1) for j in range(5))%2
def rot(v,s):
 bits=[v>>j&1 for j in range(5)]
 return sum(bits[(j-s)%5]<<j for j in range(5))
def eta(r):
 _,a,b,c,d=coeff(r)
 return (d-a*c-3*b*b+a*a*b-4*a**4)%5
def circ(a,b,mutation=None):
 r,v,z=a;u,w,t=b
 p,q=coeff(r),coeff(u)
 e=(z+(v.bit_count()//2)%2)%2
 if mutation=='drop_Q':e=z
 if mutation=='drop_sigma':e=0
 q=[value*((-1)**j if e else 1)%5 for j,value in enumerate(q)]
 s=eta(r) if mutation!='raw_eta' else p[4]
 if mutation=='drop_M':s=0
 w=rot(w,s)
 return encode(plusp(plusp(p,q),mulp(p,q))),v^w,z^t^bet(v,w)
def star(a,b):return minus(minus(circ(a,b),a),b)
def logpoly(r):
 p=coeff(r);out=[0]*5;power=[1,0,0,0,0]
 for j in range(1,5):
  power=mulp(power,p)
  c=(-1)**(j+1)*pow(j,-1,5)
  out=plusp(out,[c*v%5 for v in power])
 return encode(out)
def make(seed):
 nodes=[seed];records=[['seed',list(seed)]]
 def emit(kind,i,actor,out):
  records.append([kind,[i],actor,list(out)]);nodes.append(out);return len(nodes)-1
 def sc(i,n):return emit('integer_multiple',i,n,scale(nodes[i],n))
 def ld(i,g):return emit('lambda_difference',i,list(g),star(g,nodes[i]))
 def st(i,g):return emit('star',i,list(g),star(nodes[i],g))
 def from5(i):
  c=coeff(nodes[i][0]);j=next(j for j in range(1,5) if c[j])
  q=i if j==4 else ld(i,(5**(3-j),0,0))
  need(nodes[q]==(125*c[j],0,0),'Top extraction')
  return sc(q,pow(c[j],-1,5))
 def from2(i):
  if nodes[i][1]:i=ld(i,(0,next(w for w in V if bet(w,nodes[i][1])),0))
  need(nodes[i]==B,'Binary extraction');return i
 if seed[0]:ia=from5(sc(0,2));ib=None;route='nonzero_ring_projection'
 else:ib=from2(0);ia=from5(st(ib,X));route='nonzero_binary_projection'
 need(nodes[ia]==A,'Need x4')
 inv={rot(w,1)^w:w for w in V}
 vn=[st(ia,(0,inv[v],0)) for v in BV]
 if ib is None:ib=from2(vn[0])
 ix=sc(st(ib,X),2);ring=[ix]
 for j in range(3):ring.append(ld(ring[-1],X))
 need([nodes[i] for i in ring+vn+[ib]]==BASIS,'Need all basis')
 return records,route
def consume(seed,records):
 need(seed!=Z and records[0]==['seed',list(seed)],'seed')
 known=[seed]
 for row in records[1:]:
  kind,refs,actor,out=row
  need(len(refs)==1 and type(refs[0])==int and 0<=refs[0]<len(known),'prior ref')
  p=known[refs[0]]
  if kind=='integer_multiple':
   need(type(actor)==int and actor>=0,'scalar')
   q=Z
   for j in range(actor):q=plus(q,p)
  elif kind=='lambda_difference':q=star(tuple(actor),p)
  elif kind=='star':q=star(p,tuple(actor))
  else:raise ValueError('unknown operation')
  need(q==tuple(out),'wrong arithmetic')
  known.append(q)
 need(set(BASIS)<=set(known),'incomplete generator endpoint')
 return len(records)-1

def main():
 for r in range(625):need(coeff(logpoly(r))[4]==eta(r),'eta independently expanded')
 rows=[json.loads(line) for line in (FIN/'ideal_seed_derivations.jsonl').read_text().splitlines()]
 seeds=[(r,v,z) for r in range(625) for v in V for z in range(2) if (r,v,z)!=Z]
 need(len(rows)==19999,'row count');need([tuple(r['seed']) for r in rows]==seeds,'complete ordered inventory')
 steps=0;routes={};samples={}
 for row in rows:
  seed=tuple(row['seed']);rec,route=make(seed)
  need(sha256(json.dumps(rec,separators=(',',':')).encode()).hexdigest()==row['trace_sha256'],'commitment mismatch')
  need(row['steps']==len(rec)-1 and row['route']==route,'row metadata')
  steps+=consume(seed,rec);routes[route]=routes.get(route,0)+1
  if seed in [(0,0,1),(0,3,0),(1,0,0),(1,3,1),(125,0,0)]:samples[seed]=rec
 given=json.loads((FIN/'sample_ideal_traces.json').read_text())
 for s in given:
  seed=tuple(s['seed']);need(s['records']==samples[seed],'sample differs from commitment')
  consume(seed,s['records'])
 controls=[];seed=(1,0,0);good,_=make(seed)
 def reject(label,rec):
  try:consume(seed,rec)
  except ValueError as e:controls.append({'label':label,'rejected':str(e)});return
  raise RuntimeError('corruption accepted '+label)
 bad=copy.deepcopy(good);bad[1][3][0]=(bad[1][3][0]+1)%625;reject('altered arithmetic output',bad)
 bad=copy.deepcopy(good);bad[1][1]=[len(bad)];reject('future reference',bad)
 bad=copy.deepcopy(good);bad=bad[:-2];reject('missing x3 basis generator',bad)
 bad=copy.deepcopy(good);bad[0][1]=[2,0,0];reject('different seed',bad)
 witnesses={}
 for mode,triple in {'raw_eta':(X,(25,0,0),(0,3,0)),'drop_Q':((0,3,0),(0,5,0),X)}.items():
  a,b,c=triple;l=circ(circ(a,b,mode),c,mode);r=circ(a,circ(b,c,mode),mode)
  need(l!=r,'mutation associativity');witnesses[mode]={'a':a,'b':b,'c':c,'left':l,'right':r}
 need(star(star(X,X),X)==(25,0,0),'triple witness')
 # Compute the central witness with a direct polynomial inverse, without log coordinates.
 central=(encode([0,0,1,0,3]),0,0)
 need(all(circ(central,g)==circ(g,central) for g in seeds+[Z]),'central all 20000')
 result={'status':'PASS','seed_count':len(rows),'independent_consumed_inferences':steps,'routes':routes,'matching_samples':len(given),'corruption_controls':controls,'nonassociativity_controls':witnesses,'triple_star':star(star(X,X),X),'central_witness':central,'central_pairs':20000,'source_modules_imported':False}
 (BASE/'SEED_CHECK.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
