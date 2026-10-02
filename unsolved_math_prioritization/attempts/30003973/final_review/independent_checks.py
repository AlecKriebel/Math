import itertools,json
from pathlib import Path
N=0
def ck(x):
 global N
 assert x;N+=1
def contain(cap,H):return len(cap)>=len(H) and all(a>=b for a,b in zip(sorted(cap,reverse=True),H))
def capacities(edges,colors,c):
 adj={}
 for (u,v),col in zip(edges,colors):
  if col!=c:continue
  adj.setdefault(u,set()).add(v);adj.setdefault(v,set()).add(u)
 seen=set();out=[]
 for v in adj:
  if v in seen:continue
  todo=[v];seen.add(v);comp=[]
  while todo:
   x=todo.pop();comp.append(x)
   for y in adj[x]:
    if y not in seen:seen.add(y);todo.append(y)
  out.append(max(len(adj[x]) for x in comp))
 return out
def host(ds,z):
 E=[];v=0
 for d in ds:E.extend((v,v+i) for i in range(1,d+1));v+=d+1
 for _ in range(z):E.extend([(v,v+1),(v,v+2),(v+1,v+2)]);v+=3
 return E
targets=[tuple(sorted(a,reverse=True)) for s in range(1,4) for a in itertools.combinations_with_replacement(range(1,4),s)]
hostcases=0
for m in range(0,4):
 for ds in itertools.combinations_with_replacement(range(1,5),m):
  for z in range(3):
   E=host(ds,z)
   if len(E)>8:continue
   profiles=[(capacities(E,C,0),capacities(E,C,1)) for C in itertools.product(range(2),repeat=len(E))]
   for H in targets:
    direct=all(contain(a,H) or contain(b,H) for a,b in profiles)
    tau=lambda t:sum(k>=t for k in H)
    formula=all(sum(d>=u+v-1 for d in ds)+z*(u<=2 and v<=2)>=tau(u)+tau(v)-1 for u in set(H) for v in set(H))
    ck(direct==formula);hostcases+=1
p=Path(__file__).parent/'TURN_5_CERTIFICATE.json';J=json.loads(p.read_text());E=J['edges'];H=J['target_H_star_sizes'];Hp=J['target_Hprime_star_sizes'];C=J['Hprime_avoiding_colors']
ck(not contain(capacities(E,C,0),Hp) and not contain(capacities(E,C,1),Hp))
for rec in J['H_edge_deletion_avoiding_colorings']:
 # inspect each explicit deleted-edge coloring independently from component metadata
 i=rec['deleted_edge_index'];EE=[e for j,e in enumerate(E) if j!=i];CC=rec['colors']
 if len(CC)==len(E):CC=[c for j,c in enumerate(CC) if j!=i]
 ck(not contain(capacities(EE,CC,0),H) and not contain(capacities(EE,CC,1),H))
# Independently expand the abstract pair from printed masks.
def down(fs):return {s for s in range(128) if any(s&f==s for f in fs)}
A=down([7,9,10,18,20,24,33,36,65,76,96]);B=down([3,14,17,20,34,36,40,66,69,72,80]);prod=lambda X,Y:{x|y for x in X for y in Y}
ck(prod(A,A)==prod(B,B));ck(prod(prod(A,A),A)==set(range(128)));ck(prod(prod(B,B),B)==set(range(127)))
print(json.dumps({'status':'PASS','independent_assertions':N,'direct_coloring_host_target_cases':hostcases,'edge_deletion_colorings':45},indent=2))
