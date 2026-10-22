#!/usr/bin/env python3
"""Round2 independent spine elimination and fresh real-corruption controls."""
from collections import deque
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
from random import Random
import copy,hashlib,json,subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent;PUB=HERE.parent.parent/'publication'
def require(c,m):
 if not c:raise ValueError(m)
def sha(d):return hashlib.sha256(d).hexdigest()
SPINE=('a','b','c','d','e');GROUPS={'a':('a1','a2'),'b':('b1',),'d':('d1',),'e':('e1','e2')}
V=SPINE+tuple(v for g in GROUPS.values() for v in g)
E=tuple(zip(SPINE,SPINE[1:]))+tuple((p,v) for p,g in GROUPS.items() for v in g)
A=(1,2,3,4,5);B=(1,3,4,5,6)
def spine_count(lists):
 count=0;viable=0
 for vals in product(*(lists[v] for v in SPINE)):
  if any(abs(vals[i]-vals[i+1])<2 for i in range(4)) or any(vals[i]==vals[i+2] for i in range(3)):continue
  f=dict(zip(SPINE,vals));ways=1
  for p,leaves in GROUPS.items():
   i=SPINE.index(p);near={vals[j] for j in (i-1,i+1) if 0<=j<5}
   allowed=[[x for x in lists[w] if abs(x-f[p])>=2 and x not in near] for w in leaves]
   ways*=sum(len(set(xs))==len(xs) for xs in product(*allowed))
  count+=ways;viable+=ways>0
 return {'solutions':count,'spines_with_extensions':viable}
def distance(vertices,edges):
 adj={v:set() for v in vertices}
 for u,v in edges:adj[u].add(v);adj[v].add(u)
 ds={}
 for v in vertices:
  d={v:0};q=deque([v])
  while q:
   u=q.popleft()
   for w in adj[u]:
    if w not in d:d[w]=d[u]+1;q.append(w)
  ds[v]=d
 return adj,ds
def valid(vertices,edges,lists,f):
 if set(f)!=set(vertices) or any(f[v] not in lists[v] for v in vertices):return False
 _,d=distance(vertices,edges)
 return all(abs(f[u]-f[v])>=(2 if dist==1 else 1) for u in vertices for v,dist in d[u].items() if dist in (1,2))
def brute_count(vertices,edges,lists):
 return sum(valid(vertices,edges,lists,dict(zip(vertices,xs))) for xs in product(*(lists[v] for v in vertices)))
def recurrence_checks():
 rng=Random(202610171211);checked=0;invalid_leaves=0
 for trial in range(45):
  n=rng.randrange(1,6);vertices=tuple(range(n));edges=tuple((i,rng.randrange(i)) for i in range(1,n))
  lists={v:tuple(sorted(rng.sample(range(1,7),rng.randrange(1,4)))) for v in vertices}
  parent={0:None};children={v:[] for v in vertices};desc={}
  for v,p in edges:parent[v]=p;children[p].append(v)
  for v in reversed(vertices):desc[v]=(v,)+tuple(w for c in children[v] for w in desc[c])
  @lru_cache(None)
  def state(v,p,q):
   if q not in lists[v]:return False
   if v!=0 and (p not in lists[parent[v]] or abs(p-q)<2):return False
   if v==0 and p is not None:return False
   sets=[tuple(r for r in lists[w] if r!=p and state(w,q,r)) for w in children[v]]
   return any(len(set(rs))==len(rs) for rs in product(*sets))
  for v in vertices:
   for p,q in product((None,) if v==0 else tuple(range(1,8)),range(1,8)):
    verts=desc[v];es=tuple((u,w) for u,w in edges if u in verts and w in verts)
    local=q in lists[v] and (v==0 or (p in lists[parent[v]] and abs(p-q)>=2));expected=False
    if local:
     remaining=tuple(w for w in verts if w!=v)
     for xs in product(*(lists[w] for w in remaining)):
      f={v:q,**dict(zip(remaining,xs))}
      if valid(verts,es,lists,f) and all(f[w]!=p for w in children[v]):expected=True;break
    actual=state(v,p,q);require(actual==expected,('recurrence',trial,v,p,q,actual,expected));checked+=1
    if not children[v] and not local:invalid_leaves+=1;require(not actual,'invalid leaf admitted')
 return {'seeded_trees':45,'all_local_states_vs_cartesian':checked,'invalid_leaf_states_rejected':invalid_leaves}
def rank_checks():
 palette=(1,3,4,7);choices=tuple(combinations(palette,2));checked=0;edgeset=((0,1),(0,2),(1,2));vertices=(0,1,2)
 for mask in range(8):
  edges=tuple(e for i,e in enumerate(edgeset) if mask>>i&1)
  for sets in product(choices,repeat=3):
   lists=dict(zip(vertices,sets));union=sorted(set().union(*map(set,sets)));rank={x:i+1 for i,x in enumerate(union)}
   compressed={v:tuple(rank[x] for x in lists[v]) for v in vertices}
   for vals in product(*(compressed[v] for v in vertices)):
    f=dict(zip(vertices,vals))
    if valid(vertices,edges,compressed,f):require(valid(vertices,edges,lists,{v:union[f[v]-1] for v in vertices}),'rank lifting failed')
   checked+=1
 require(brute_count((0,1),((0,1),),{0:(1,),1:(3,)})==1,'rank control original')
 require(brute_count((0,1),((0,1),),{0:(1,),1:(2,)})==0,'rank control compressed')
 return {'three_vertex_graph_list_assignments':checked,'forward_feasibility_counterexample':'edge lists {1},{3} become {1},{2}'}
def extension_checks():
 base=json.loads((HERE/'clean_extract/specimen.json').read_text())['ordinary_five_witness'];checked=0
 for lengths in product(range(3),repeat=6):
  vertices=list(V);edges=list(E);f=dict(base)
  for leaf,length in zip(('a1','a2','b1','d1','e1','e2'),lengths):
   parent=next(u if v==leaf else v for u,v in E if leaf in (u,v));last=leaf;grand=parent
   for j in range(length):
    w=leaf+'_'+str(j);available=[x for x in A if abs(x-f[last])>=2 and x!=f[grand]]
    require(bool(available),'five palette extension');f[w]=available[0];vertices.append(w);edges.append((last,w));grand,last=last,w
  require(valid(vertices,edges,{v:A for v in vertices},f),'extended all-pair validity');checked+=1
 return {'all_independent_lengths_0_to_2':checked,'leaves':6}
def archive_controls():
 mutant=HERE/'mutant_extract'
 with zipfile.ZipFile(PUB/'Tree_Five_List_Verification_v1.0.zip') as z:z.extractall(mutant)
 records=[]
 def execute(args):return subprocess.run([sys.executable,'-B',*args],cwd=mutant,capture_output=True,text=True,timeout=60)
 def fail(name,args,substring):
  p=execute(args);require(p.returncode!=0 and substring in p.stderr,(name,p.returncode,p.stderr));records.append({'name':name,'mode':args,'exit_code':p.returncode,'detected_by':substring})
 specimen=mutant/'specimen.json';original=specimen.read_bytes();data=json.loads(original)
 for name,change,error in [('edge_endpoint_changed',lambda d:d['edges'][0].__setitem__(1,'e'),'paper edge binding'),('five_list_changed',lambda d:d['lists'].__setitem__('b1',[1,2,3,4,6]),'paper list binding'),('ordinary_witness_edge_corruption',lambda d:d['ordinary_five_witness'].__setitem__('a',5),'provided common-palette witness'),('expected_count_changed',lambda d:d['expected_counts'].__setitem__('common_5',9),'claimed count metadata')]:
  changed=copy.deepcopy(data);change(changed);specimen.write_text(json.dumps(changed))
  try:fail(name,['-O','verify.py'],error)
  finally:specimen.write_bytes(original)
 verifier=mutant/'verify.py';raw=verifier.read_bytes();verifier.write_bytes(raw.replace(b'Root exact global-CSP',b'root exact global-CSP',1))
 try:fail('same_size_code_tamper',['replay.py'],'member digest verify.py')
 finally:verifier.write_bytes(raw)
 exp=mutant/'expected_results.json';e_raw=exp.read_bytes();manifest=mutant/'MANIFEST.json';m_raw=manifest.read_bytes()
 changed=json.loads(e_raw);changed['enumerations']['common_5']['solutions']=9;exp.write_text(json.dumps(changed));m=json.loads(m_raw)
 for e in m['files']:
  if e['path']=='expected_results.json':e['bytes']=exp.stat().st_size;e['sha256']=sha(exp.read_bytes())
 manifest.write_text(json.dumps(m))
 try:fail('authenticated_stale_expected_results',['replay.py'],'fresh result differs from expected')
 finally:exp.write_bytes(e_raw);manifest.write_bytes(m_raw)
 p=execute(['replay.py']);require(p.returncode==0,'restored pristine replay');records.append({'name':'restored_pristine_replay','exit_code':p.returncode,'stdout':p.stdout.strip()})
 return records
def main():
 counts={str(k):spine_count({v:tuple(range(1,k+1)) for v in V}) for k in range(1,7)};bad=spine_count({v:B if v in ('a1','a2','e1','e2') else A for v in V})
 require([counts[str(k)]['solutions'] for k in range(1,7)]==[0,0,0,0,8,6336],'independent exact counts');require(bad['solutions']==0,'independent obstruction')
 result={'python':sys.version,'mechanism':'spine Cartesian enumeration and exact leaf-star elimination; candidate programs not imported','counts':counts,'bad_lists':bad,'recurrence':recurrence_checks(),'rank_compression':rank_checks(),'six_path_extensions':extension_checks(),'real_corruption_controls':archive_controls()}
 (HERE/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
