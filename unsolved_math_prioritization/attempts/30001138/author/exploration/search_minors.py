import itertools,random,json,pathlib,time
P=pathlib.Path(__file__).parent

def edges(g):return [(i,j) for i in range(len(g)) for j in g[i] if i<j]
def graph(n,es):
 g=[set() for _ in range(n)]
 for a,b in es:g[a].add(b);g[b].add(a)
 return g

def embedding(h,g,induced=False):
 if len(h)>len(g):return
 order=sorted(range(len(h)),key=lambda v:(-len(h[v]),v));mapping={};used=set()
 def go(i):
  if i==len(order):return dict(mapping)
  a=order[i]
  candidates=set(range(len(g)))-used
  for b in h[a]:
   if b in mapping:candidates &= g[mapping[b]]
  for x in sorted(candidates):
   if len(g[x])<len(h[a]):continue
   if induced and any((b in h[a])!=(mapping[b] in g[x]) for b in mapping):continue
   mapping[a]=x;used.add(x)
   r=go(i+1)
   if r is not None:return r
   del mapping[a];used.remove(x)
 return go(0)

def normalized(g):
 ks=sorted(g);mp={a:i for i,a in enumerate(ks)}
 return [set(mp[b] for b in g[a]) for a in ks]

def family():
 fs=[graph(6,itertools.combinations(range(6),2))];todo=list(fs)
 def add(g):
  if len(g)>10 or len(edges(g))!=15:return
  ds=sorted(map(len,g))
  if any(sorted(map(len,h))==ds and embedding(g,h,True) is not None for h in fs):return
  fs.append(g);todo.append(g)
 while todo:
  g=todo.pop()
  for tri in itertools.combinations(range(len(g)),3):
   if all(b in g[a] for a,b in itertools.combinations(tri,2)):
    h={i:set(g[i]) for i in range(len(g))};z=len(h);h[z]=set(tri)
    for a,b in itertools.combinations(tri,2):h[a].remove(b);h[b].remove(a)
    for a in tri:h[a].add(z)
    add(normalized(h))
  for v in range(len(g)):
   if len(g[v])!=3:continue
   ns=g[v];h={i:set(g[i])-{v} for i in range(len(g)) if i!=v}
   for a,b in itertools.combinations(ns,2):h[a].add(b);h[b].add(a)
   add(normalized(h))
 return sorted(fs,key=lambda g:(len(g),sorted(map(len,g))))

def product(m,n):return graph(m*n,[(i*n+j,((i+1)%m)*n+j) for i in range(m) for j in range(n)]+[(i*n+j,i*n+(j+1)%n) for i in range(m) for j in range(n)])
def truncated():
 labels=list(itertools.permutations(range(5),2));return graph(20,[(a,b) for a in range(20) for b in range(a+1,20) if labels[a][0]==labels[b][0] or labels[a]==labels[b][::-1]])

def search(g,fs,seed=666,tries=30000):
 rng=random.Random(seed);n=len(g)
 for trial in range(tries):
  cur={i:set(g[i]) for i in range(n)};sets={i:{i} for i in range(n)}
  while len(cur)>=6:
   ks=sorted(cur);q=normalized(cur)
   if len(cur)<=10:
    for idx,h in enumerate(fs):
     if len(h)!=len(cur) or len(edges(q))<15:continue
     mp=embedding(h,q)
     if mp is not None:return {'family_index':idx,'target_edges':edges(h),'branch_sets':[sorted(sets[ks[mp[a]]]) for a in range(len(h))],'trial':trial,'seed':seed}
   if len(cur)==6:break
   es=[(a,b) for a in cur for b in cur[a] if a<b]
   a,b=rng.choice(es)
   cur[a]=(cur[a]|cur[b])-{a,b};sets[a]|=sets[b]
   for c in cur[b]-{a}:cur[c].remove(b);cur[c].add(a)
   del cur[b];del sets[b]
 return {'not_found':True,'trials':tries,'seed':seed}
if __name__=='__main__':
 fs=family();print('family',[(len(g),sorted(map(len,g))) for g in fs],flush=True)
 (P/'family.json').write_text(json.dumps([{'n':len(g),'edges':edges(g)} for g in fs],indent=2)+'\n')
 results={}
 for name,g in [('Q4',product(4,4)),('truncated_simplex',truncated()),('triangle_hexagon',product(3,6)),('triangle_pentagon',product(3,5)),('triangle_square',product(3,4))]:
  st=time.time();r=search(g,fs,tries=50000);results[name]=r;print(name,r,'seconds',time.time()-st,flush=True)
  (P/'minor_search.json').write_text(json.dumps(results,indent=2)+'\n')
