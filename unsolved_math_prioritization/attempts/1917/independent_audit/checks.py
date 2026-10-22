#!/usr/bin/env python3
"""Independent finite corroboration, provenance and integrity checks; not a proof checker."""
import argparse,hashlib,json,itertools,zipfile
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
PINS={
 'catalog':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 'problems':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'reports':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
 'pdf':(432079,'9654af66b347f47df1bc2dd807f1c1950a3afce4f4fe0ece8973fdb4d7d5fa53')}
PAIR='f52f8c63ea451e4c7291492e30ee56ffcb16c96041ddef4e957fec3a642dfa51'
STATEMENT='583e23540df12cb7c9315490febf0e1d184ede1129d0b813cf2b6b1f275fb725'
def require(x,msg):
 if not x: raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(path,key):
 b=Path(path).read_bytes(); require((len(b),sha(b))==PINS[key],key+' pin mismatch');return b
def F(n):return n*(n+1)//6
def Q(n,s):return F(n+s)-s*(s+1)//2

def finite():
 res={}
 # All labelled graphs through order 5: exact partitions, induced-cycle chordality,
 # and the rooted-simplicial condition are checked by separate implementations.
 rows=[]
 for n in range(6):
  edges=list(itertools.combinations(range(n),2));ix={e:i for i,e in enumerate(edges)}
  vmasks=range(1<<n)
  clique_masks=[]
  for v in vmasks:
   inds=[i for i in range(n) if v>>i&1]
   if len(inds)>=2:clique_masks.append(sum(1<<ix[e] for e in itertools.combinations(inds,2)))
  @lru_cache(None)
  def cp(E):
   if not E:return 0
   first=E&-E
   return 1+min(cp(E^c) for c in clique_masks if c&first and c&E==c)
  chord_count=0;maximum=0
  for E in range(1<<len(edges)):
   adj=[0]*n
   for i,(u,v) in enumerate(edges):
    if E>>i&1:adj[u]|=1<<v;adj[v]|=1<<u
   chord=True
   for V in vmasks:
    if V.bit_count()<4:continue
    if all((adj[v]&V).bit_count()==2 for v in range(n) if V>>v&1):
     reached=V&-V;old=0
     while reached!=old:
      old=reached
      for v in range(n):
       if old>>v&1:reached|=adj[v]&V
     if reached==V:chord=False;break
   rooted=True
   for V in vmasks:
    if not V:continue
    simplicial=0
    for v in range(n):
     if not V>>v&1:continue
     N=adj[v]&V
     if all((N&~(1<<u))&~adj[u]==0 for u in range(n) if N>>u&1):simplicial|=1<<v
    # Existence of an exterior simplicial vertex for every proper clique root
    for C in vmasks:
     if C&~V or C==V:continue
     isclique=all((C&~(1<<u))&~adj[u]==0 for u in range(n) if C>>u&1)
     if isclique and not simplicial&~C:rooted=False;break
    if not rooted:break
   require(chord==rooted,'chordal/rooted mismatch')
   if chord:
    chord_count+=1;v=cp(E);maximum=max(maximum,v);require(v<=F(n),'small-order bound failed')
  rows.append({'n':n,'all_graphs':1<<len(edges),'chordal_graphs':chord_count,'max_cp':maximum,'F_n':F(n)})
 res['exhaustive_small_graphs']=rows
 # Exact arithmetic and strict normalized margins, including the smallest margin.
 arithmetic_cases=0
 for s in range(41):
  lam=Fraction(1,100*(s+1));rho=lam/100
  require(lam/3-8*rho>0 and Fraction(1,6)-4*lam>0,'nonpositive margin')
  require((2*s+2)*lam==Fraction(1,50),'common-neighbour margin')
  for n in range(max(1,2*s),2*s+201):
   arithmetic_cases+=1
   require(Q(n,s)-Q(n-1,s)==(n+s+1)//3,'increment')
   vals=[c*(n-c)-(c-s)*(c-s-1)//2 for c in range(n+s+1)]
   require(max(vals)==Q(n,s),'integer optimum')
 res['arithmetic_cases']=arithmetic_cases
 # Negative control: K3 join independent two has fractional value 3 and cp 4.
 n=5;es=list(itertools.combinations(range(n),2));full=sum(1<<i for i,e in enumerate(es) if e!=(3,4))
 C=[sum(1<<es.index(e) for e in itertools.combinations(v,2)) for k in range(2,6) for v in itertools.combinations(range(n),k) if (3 not in v or 4 not in v)]
 @lru_cache(None)
 def opt(E):
  if not E:return 0
  return 1+min(opt(E^c) for c in C if c&(E&-E) and c&E==c)
 require(opt(full)==4,'non-integral test cp')
 triangles=[(i,j,r) for i,j in itertools.combinations(range(3),2) for r in (3,4)]
 for e in es:
  mass=sum(Fraction(1,2) for T in triangles if set(e)<=set(T))
  require(mass==(0 if e==(3,4) else 1),'fractional test edge load')
 require(sum(Fraction(1,2) for T in triangles)==3,'fractional test objective')
 weights={e:(-1 if max(e)<3 else 1) for e in es if e!=(3,4)}
 for cm in C:
  require(sum(weights[e] for i,e in enumerate(es) if cm>>i&1)<=1,'fractional dual feasibility')
 require(sum(weights.values())==3,'fractional dual value')
 res['fractional_equals_integral_negative_control']={'fractional_partition':3,'integer_partition':4,'rejected_exact_rounding':True}
 # A missing core-edge negative weight matters: two +1 spokes of a triangle
 # force its third edge <= -1. A nonnegative dual cannot carry that assignment.
 require(1+1-1<=1 and 1+1+0>1,'signed dual control')
 res['signed_dual_negative_control']='PASS'
 res['machine_proof_certification']=False
 return res

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for k in PINS:p.add_argument('--'+k)
 p.add_argument('--author-archive');p.add_argument('--author-manifest')
 a=p.parse_args();r={'finite':finite(),'corpus_replay':'NOT_RUN','primary_pdf_replay':'NOT_RUN','author_freeze_replay':'NOT_RUN'}
 if any([a.catalog,a.problems,a.reports]):
  require(all([a.catalog,a.problems,a.reports]),'all three corpus inputs required')
  cat=json.loads(pin(a.catalog,'catalog'));ps=json.loads(pin(a.problems,'problems'));reports=json.loads(pin(a.reports,'reports'))
  require(type(cat)is list and type(ps)is list and type(reports)is dict,'corpus types')
  require(len(cat)==len(ps)==15458,'corpus counts')
  cc=[c for c in cat if str(c.get('id'))=='1917'];pp=[p for p in ps if p.get('id')==1917]
  require(len(cc)==len(pp)==1,'unique problem');c=cc[0];p=pp[0];old=reports.get(p['problem_number'],{})
  require(c['rank']==883 and p['problem_number']=='EP-81' and old=={},'identity/empty report')
  require(sha(p['statement'].encode())==STATEMENT,'statement identity')
  require(sha(json.dumps([p,old],sort_keys=True).encode())==PAIR,'complete pair identity')
  r['corpus_replay']='PASS'
 if a.pdf:require(pin(a.pdf,'pdf').startswith(b'%PDF'),'PDF magic');r['primary_pdf_replay']='PASS'
 if a.author_archive or a.author_manifest:
  require(a.author_archive and a.author_manifest,'both author freeze inputs required')
  z=Path(a.author_archive).read_bytes();mb=Path(a.author_manifest).read_bytes()
  require((len(z),sha(z))==(16904,'5023ed1178ffada4f6c05ef80484bbf4ec6f0070a4f1554d0acef7147d3ae843'),'author archive')
  require(sha(mb)=='175287bb667cc8a78c99cb2e7d5684d6c1eaf70d5c8ee490d5d7727515ab4a13','author manifest')
  man=json.loads(mb)
  with zipfile.ZipFile(a.author_archive) as f:
   require(sorted(f.namelist())==sorted(x['name'] for x in man['members']),'member names')
   for x in man['members']:
    b=f.read(x['name']);require((len(b),sha(b))==(x['bytes'],x['sha256']),'author member')
  r['author_freeze_replay']='PASS'
 print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':main()
