import sys,itertools,json,time
sys.path.insert(0,str(__import__('pathlib').Path(__file__).parent))
from search_minors import product,graph

def facets_product(m,n):
 return [{i*n+j for i in range(m) for j in [k,(k+1)%n]} for k in range(n)]+[{i*n+j for i in [k,(k+1)%m] for j in range(n)} for k in range(m)]

def check(g,facets):
 n=len(g);fm=[sum(1<<i for i in f) for f in facets];nf={};counts={};allmasks=set()
 for root in range(n):
  def dfs(path,mask):
   u=path[-1]
   if len(path)>=3 and root in g[u] and path[1]<u:
    counts[len(path)]=counts.get(len(path),0)+1;allmasks.add(mask)
    if not any(mask&f==mask for f in fm):nf.setdefault(mask,path[:])
   if len(path)>=n-3:return
   for v in sorted(g[u]):
    if v>root and not (mask>>v&1):dfs(path+[v],mask|(1<<v))
  dfs([root],1<<root)
 full=(1<<n)-1;eligible=[None]*(1<<n)
 for m,p in nf.items():eligible[m]=m
 for i in range(n):
  for m in range(1<<n):
   if m>>i&1 and eligible[m] is None:eligible[m]=eligible[m^(1<<i)]
 pair=None
 for m,p in nf.items():
  k=eligible[full^m]
  if k is not None:pair=[p,nf[k]];break
 return {'n':n,'edges':len(sum([list(a) for a in g],[]))//2,'facets':[sorted(f) for f in facets], 'cycle_counts':counts,'distinct_cycle_vertex_masks':len(allmasks),'nonfacial_cycle_vertex_masks':len(nf),'uncovered_pair':pair,'all_disjoint_pairs_facially_covered':pair is None}
for m,n in [(3,3),(3,4),(3,5)]:
 st=time.time();r=check(product(m,n),facets_product(m,n));print(m,n,r,'secs',time.time()-st,flush=True)
 __import__('pathlib').Path(__file__).with_name('facial_'+str(m)+'_'+str(n)+'.json').write_text(json.dumps(r,indent=2)+'\n')
