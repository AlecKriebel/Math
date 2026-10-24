"""Exact bounded collision-cover lattice exploration; no all-n conclusion."""
from itertools import combinations,permutations
from pathlib import Path
from sympy import Matrix,zeros
from sympy.matrices.normalforms import hermite_normal_form
import json,time,datetime,argparse

def explore(n,limit_seconds):
 start=time.monotonic();rels=[]
 def canon(v):
  if next(x for x in v if x)!=1:v=tuple(-x for x in v)
  return tuple(v)
 def rel(a,b,c,d):
  v=[0]*n
  for i in (a,b):v[i]+=1
  for i in (c,d):v[i]-=1
  return canon(v)
 for a,b,c,d in combinations(range(n),4):
  for v in (rel(a,b,c,d),rel(a,c,b,d),rel(a,d,b,c)):
   if v not in rels:rels.append(v)
 ri={v:i for i,v in enumerate(rels)}
 cycles=[]
 for tail in permutations(range(1,n)):
  if tail[0]>tail[-1]:continue
  c=(0,)+tail;edges=[(c[i],c[(i+1)%n]) for i in range(n)];rr=set()
  for (a,b),(c,d) in combinations(edges,2):
   if len({a,b,c,d})==4:rr.add(ri[rel(a,b,c,d)])
  cycles.append(frozenset(rr))
 scaled_rel=[Matrix([2**(n-1)*x for x in v]) for v in rels]
 diffs=[]
 for i,j in combinations(range(n),2):
  v=[0]*n;v[i]=2**(n-1);v[j]=-2**(n-1);diffs.append(((i,j),Matrix(v)))
 seen=set();counts={'states':0,'collapsed_branches':0,'counterexample_modules':0,'cached_states':0,'maximum_rank':0}
 solutions=[]
 def key(H):return (H.cols,tuple(H))
 def visit(H,chosen):
  if time.monotonic()-start>limit_seconds:raise TimeoutError
  k=key(H)
  if k in seen:counts['cached_states']+=1;return
  seen.add(k);counts['states']+=1;counts['maximum_rank']=max(counts['maximum_rank'],H.cols)
  for pair,d in diffs:
   if hermite_normal_form(H.row_join(d))==H:
    counts['collapsed_branches']+=1;return
  closed={i for i,v in enumerate(scaled_rel) if hermite_normal_form(H.row_join(v))==H}
  uncovered=next((c for c in cycles if not c&closed),None)
  if uncovered is None:
   counts['counterexample_modules']+=1
   solutions.append({'chosen_relations':chosen,'hnf':[[int(H[i,j]) for j in range(H.cols)] for i in range(n)]})
   return
  for i in sorted(uncovered):visit(hermite_normal_form(H.row_join(Matrix(rels[i]))),chosen+[i])
 complete=True
 try:visit(zeros(n,0),[])
 except TimeoutError:complete=False
 return {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'n':n,'relation_count':len(rels),'hamiltonian_cycles':len(cycles),'complete':complete,'seconds':time.monotonic()-start,'counts':counts,'solutions':solutions,'interpretation':'Fixed-n exploratory exact lattice enumeration only; no originality or all-n claim.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,required=True);ap.add_argument('--seconds',type=float,default=30);args=ap.parse_args()
 result=explore(args.n,args.seconds);Path(__file__).with_name(f'result_n{args.n}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
