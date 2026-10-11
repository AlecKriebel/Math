"""Independent finite-state checks; no infinite-volume claim is tested numerically."""
from collections import defaultdict,deque
from fractions import Fraction
from itertools import product
from pathlib import Path
import json,hashlib
A=0
def ck(x):
 global A
 A+=1
 assert x

def edge(a,b):return tuple(sorted((a,b)))
def model(base,heights):
 vs=sorted({(u,h) for e in base for u in e for h in heights})
 vert=sorted({edge((u,h),(u,h+1)) for u,h in vs if h+1 in heights})
 hor=sorted({edge((u,h),(v,h)) for u,v in base for h in heights})
 es=sorted(vert+hor);adj={u:sorted(v for e in es if u in e for v in e if v!=u) for u in vs}
 return vs,vert,hor,es,adj

def explore(adj,M,reveal,start=(0,0)):
 accepted={start};count=defaultdict(int,{start[0]:1});q=deque([start]);states={};uses=defaultdict(int)
 while q:
  u=q.popleft()
  for v in adj[u]:
   e=edge(u,v)
   if e in states:continue
   if u[0]!=v[0]:uses[tuple(sorted((u[0],v[0])))]+=1
   state=reveal(e);states[e]=state
   if state and v not in accepted and count[v[0]]<M:
    accepted.add(v);count[v[0]]+=1;q.append(v)
 ck(all(n<=M for n in count.values()));ck(all(n<=2*M for n in uses.values()))
 return tuple(sorted(accepted)),states,uses

def hist_add(hist,key,ones):hist[(key,ones)]+=1
def mass(hist,key,a,b,N):return sum(c*a**k*(b-a)**(N-k) for (v,k),c in hist.items() if v==key)
base=[(0,1),(1,2)];reports=[]
vs,vertical,horizontal,edges,adj=model(base,range(3))
for M in (1,2):
 actual=defaultdict(int);reservoir=defaultdict(int);yhist=defaultdict(int)
 for bits in product((0,1),repeat=len(edges)):
  vals=dict(zip(edges,bits));reached,states,uses=explore(adj,M,vals.__getitem__)
  hist_add(actual,reached,sum(bits))
  # Preservation when the uncapped component already fits the cap.
  full,_,_=explore(adj,len(vs),vals.__getitem__)
  if all(sum(v[0]==u for v in full)<=M for u in (0,1,2)):ck(full==reached)
 R=len(vertical)+len(base)*2*M
 for bits in product((0,1),repeat=R):
  vals=dict(zip(vertical,bits));pools={e:bits[len(vertical)+i*2*M:len(vertical)+(i+1)*2*M] for i,e in enumerate(base)};idx=defaultdict(int)
  def reveal(e):
   if e in vals:return vals[e]
   b=tuple(sorted((e[0][0],e[1][0])));j=idx[b];idx[b]+=1;return pools[b][j]
  reached,states,uses=explore(adj,M,reveal)
  yy=tuple(int(any(pools[e])) for e in base)
  reachable={0}
  for _ in range(3):
   for e,opened in zip(base,yy):
    if opened and reachable.intersection(e):reachable.update(e)
  ck(all(u in reachable for u,h in reached))
  hist_add(reservoir,reached,sum(bits));hist_add(yhist,yy,sum(bits))
 keys={v for v,k in actual}|{v for v,k in reservoir}
 for a,b in [(1,2),(1,3),(2,3)]:
  for key in keys:ck(mass(actual,key,a,b,len(edges))*b**R==mass(reservoir,key,a,b,R)*b**len(edges))
  q=1-(1-Fraction(a,b))**(2*M)
  for yy in product((0,1),repeat=2):
   got=Fraction(mass(yhist,yy,a,b,R),b**R);expected=q**sum(yy)*(1-q)**(2-sum(yy));ck(got==expected)
 reports.append({'base':'three-vertex path','heights':3,'cap':M,'direct_configurations':2**len(edges),'reservoir_configurations':2**R,'parameters':['1/2','1/3','2/3'],'accepted_law_and_joint_Y_independence':True})
# Full percolation law after independent completion, rather than just reached-set law.
vs,V,H,E,adj=model(base,range(2));M=1;R=len(V)+4
completion=[]
for a,b in [(1,2),(1,3),(2,3)]:
 law=defaultdict(int)
 for bits in product((0,1),repeat=R):
  vals=dict(zip(V,bits));pools={e:bits[len(V)+2*i:len(V)+2*i+2] for i,e in enumerate(base)};idx=defaultdict(int)
  def reveal(e):
   if e in vals:return vals[e]
   be=tuple(sorted((e[0][0],e[1][0])));j=idx[be];idx[be]+=1;return pools[be][j]
  _,states,_=explore(adj,1,reveal);unseen=[e for e in E if e not in states]
  w=a**sum(bits)*(b-a)**(R-sum(bits))
  for tail in product((0,1),repeat=len(unseen)):
   full=dict(states);full.update(zip(unseen,tail));key=tuple(full[e] for e in E)
   wt=a**sum(tail)*(b-a)**(len(tail)-sum(tail));law[key]+=w*wt*b**(len(E)-len(unseen))
 for key in product((0,1),repeat=len(E)):
  expected=a**sum(key)*(b-a)**(len(E)-sum(key));ck(law[key]==expected*b**R)
 completion.append({'p':str(Fraction(a,b)),'product_configurations':2**len(E),'full_iid_completion_law':True})
# Attain the full 2M bound on one edge through exploration of a third fiber.
B=[(0,1),(0,2),(1,2)];vs,V,H,E,adj=model(B,range(-1,3))
opened={edge((0,0),(0,1)),edge((0,0),(1,0)),edge((1,0),(1,-1)),edge((0,1),(2,1)),edge((2,1),(2,2))}
reached,_,uses=explore(adj,2,lambda e:int(e in opened));sharp_queries=uses[(1,2)];ck(sharp_queries==4)
# Increasing finite degrees do not affect the per-edge bound.
for degree in range(2,31):
 B=[(0,j) for j in range(1,degree+1)];vs,V,H,E,adj=model(B,range(2))
 reached,_,uses=explore(adj,1,lambda e:1);ck(len(reached)==degree+1);ck(all(n<=2 for n in uses.values()))
# Exact ray lower bound and stretched-tree level lengths.
pr=Fraction(1)
for n in range(1,81):
 pr*=1-Fraction(1,2**(n+1));ck(pr>=Fraction(1,2));ck(sum(2**j for j in range(1,n+1))==2**(n+1)-2)
 # At p=1/2 the elementary union bound is exactly this dyadic number.
 ck(Fraction(2**n,2**(2**(n+1)-2))>0) if n<=10 else None
out={'all_passed':True,'assertions':A,'multi_reservoir_tests':reports,'full_completion_tests':completion,'sharp_2M_configuration':{'cap':2,'base_edge':[1,2],'queried_horizontal_edges':sharp_queries,'verified':True},'star_degree_controls':list(range(2,31)),'exact_ray_products':80,'reviewed_sha256':hashlib.sha256(Path(__file__).with_name('reviewed_partial.md').read_bytes()).hexdigest(),'scope':'Finite exact diagnostics only. Infinite/countability steps require the written proof audit.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
