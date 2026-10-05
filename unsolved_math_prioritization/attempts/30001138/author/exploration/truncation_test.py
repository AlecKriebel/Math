import pathlib,sys,itertools,json,time
sys.path.insert(0,str(pathlib.Path(__file__).parent));from search_minors import graph,family,search
from facial_test import check

def truncated_k(k):
 labels=[(i,j) for i in range(k) for j in range(5) if i!=j]+[(i,i) for i in range(k,5)]
 es=[]
 for a,(i,j) in enumerate(labels):
  for b,(u,v) in enumerate(labels):
   if a>=b:continue
   if (i==u and i<k) or (i!=u and ((i>=k or j==u) and (u>=k or v==i))):es.append((a,b))
 # x_i >= 0 old facets; x_i <=2 new
 coords=[]
 for i,j in labels:
  x=[0]*5;x[i]=3 if i==j else 2
  if i!=j:x[j]=1
  coords.append(x)
 fs=[{a for a,x in enumerate(coords) if x[i]==0} for i in range(5)]+[{a for a,x in enumerate(coords) if x[i]==2} for i in range(k)]
 return labels,coords,graph(len(labels),es),fs
fs=family();out={}
for k in range(6):
 labs,coords,g,f=truncated_k(k);t=time.time()
 r={'labels':labs,'coordinates_barycentric':coords,'edges':[(a,b) for a in range(len(g)) for b in g[a] if a<b],'facets':[sorted(x) for x in f]}
 if k<=3:r['facial_cover']=check(g,f)
 if k>=2:r['minor']=search(g,fs,tries=5000)
 out[str(k)]=r;print(k,r.get('minor'),r.get('facial_cover',{}).get('all_disjoint_pairs_facially_covered'),'seconds',time.time()-t,flush=True)
 pathlib.Path(__file__).with_name('truncation_results.json').write_text(json.dumps(out,indent=2)+'\n')
