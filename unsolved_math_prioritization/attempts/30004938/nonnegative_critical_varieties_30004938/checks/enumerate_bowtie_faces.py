from pathlib import Path
BASE = Path(__file__).resolve().parent
# Exploratory finite-window tubing check, not an all-affine certificate.
exec(open(BASE / 'enumerate_bowtie_tubes.py').read().split('out=[]')[0])
raw=json.load(open(BASE / 'bowtie_tubes.json'))['tubes']
tubes=list(map(frozenset,raw));N=len(tubes)
def compatibles(A,B):
 for t in range(-4,5):
  C={x+5*t for x in B}
  if A&C and not (A<=C or C<=A):return False
 return True
compat={(i,j):compatibles(tubes[i],tubes[j]) for i in range(N) for j in range(i+1,N)}

def acyclic(ids):
 verts=[frozenset(x+5*t for x in tubes[i]) for i in ids for t in range(-2,3)]
 adj=[set() for v in verts];indeg=[0 for v in verts]
 for i,A in enumerate(verts):
  for j,B in enumerate(verts):
   if i!=j and not A&B and any(related(a,b) for a in A for b in B):adj[i].add(j);indeg[j]+=1
 stack=[i for i in range(len(verts)) if indeg[i]==0];removed=0
 while stack:
  i=stack.pop();removed+=1
  for j in adj[i]:
   indeg[j]-=1
   if indeg[j]==0:stack.append(j)
 return removed==len(verts)

def face_of_factor(ids,R):
 # R is a cyclic ordered triple of residue representatives, e.g. 1,2,3.
 # Determine pairwise leading scales by the smallest tubing tube containing
 # lifts of all 3 residues. At root, residues may collide via translated tubes.
 allts=[frozenset(x+5*t for x in tubes[i]) for i in ids for t in range(-3,4)]
 candidates=[]
 for T in allts:
  vals=[next((x for x in T if (x-r)%5==0),None) for r in R]
  if all(x is not None for x in vals):candidates.append((len(T),T,vals))
 if candidates:
  _,container,vals=min(candidates,key=lambda z:(z[0],min(z[1])))
  # A finite line triple in increasing lifted order; the cyclic closing gap is longest.
  order=sorted(range(3),key=lambda i:vals[i])
  # Pair collision at a lower scale yields vertex, indexed by vanishing chord.
  for i,j in itertools.combinations(range(3),2):
   if any(U<container and vals[i] in U and vals[j] in U for U in allts):
    return ('v',tuple(sorted((R[i],R[j]))))
  return ('e',tuple(sorted((R[order[0]],R[order[-1]]))))
 else:
  for i,j in itertools.combinations(range(3),2):
   if any(any((x-R[i])%5==0 for x in U) and any((x-R[j])%5==0 for x in U) for U in allts):
    return ('v',tuple(sorted((R[i],R[j]))))
  return ('int',)
levels={0:[()]}
for size in range(1,5):
 cur=[]
 for old in levels[size-1]:
  for j in range(old[-1]+1 if old else 0,N):
   if all(compat[i,j] for i in old):
    ids=old+(j,)
    if acyclic(ids):cur.append(ids)
 levels[size]=cur
 print('codim',size,'count',len(cur),flush=True)
images=collections.defaultdict(list)
for size,level in levels.items():
 for ids in level:
  key=str((face_of_factor(ids,(1,2,3)),face_of_factor(ids,(2,4,5))))
  images[key].append(ids)
print('predicted images',len(images),flush=True)
print('Euler',sum((-1)**(4-s)*len(v) for s,v in levels.items()))
open(BASE / 'bowtie_faces_exploratory.json','w').write(json.dumps({'warning':'Finite-window acyclicity and predicted image types; no certification of surjectivity of face images.','codim_counts':{s:len(v) for s,v in levels.items()},'image_count':len(images),'images':images},indent=2))
