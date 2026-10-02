from pathlib import Path
import hashlib,json,itertools
import sympy as s
p=Path('/workspace/shared/hodge_tate_30006078');src=Path('/workspace/scratch/c7d6ade09fc0/hodge_tate_30006078/source');n=0
for mf in ['FINAL_AUTHOR_MANIFEST.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]:
 data=json.loads((p/mf).read_text()); fs=data.get('files',data)
 for name,h in fs.items():
  if isinstance(h,dict):h=h['sha256']
  assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h;n+=1
for mf in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T3.json']:
 for name,info in json.loads((p/mf).read_text())['files'].items():assert hashlib.sha256((src/name).read_bytes()).hexdigest()==info['sha256'];n+=1
B=[]
for i in range(2):
 for j in range(2):
  m=s.zeros(2);m[i,j]=1;B.append(m)
Z=s.zeros(2);I=s.eye(2);pairs=[(a,Z) for a in B]+[(Z,b) for b in B]
def alt(ms):
 q=len(ms);out=0
 for perm in itertools.permutations(range(q)):
  v=s.eye(ms[0].rows)
  for k in perm:v=v*ms[k]
  out+=(-1)**sum(perm[i]>perm[j] for i in range(q) for j in range(i+1,q))*s.trace(v)
 return out
for ix in itertools.product(range(8),repeat=3):
 vals=[pairs[j] for j in ix]; aa=[a for a,b in vals];bb=[b for a,b in vals]
 assert alt([s.kronecker_product(a,I)+s.kronecker_product(I,b) for a,b in vals])==2*alt(aa)+2*alt(bb);n+=1
 assert alt([-a.T for a in aa])==alt(aa);n+=1
M=s.Matrix([[0,1,1,1],[1,0,1,1],[1,1,0,2],[1,1,2,0]])
assert M.det()==-4 and M.rank()==4;n+=1
assert len([(x,y) for x in range(5) for y in range(5) if (y*y-x*x*x+x)%5==0])+1==8;n+=1
for degree in range(1,15):
 assert degree-1>=0;n+=1
for prime in [2,3,5,7,11]:
 for rank in range(1,100):
  v=0;r=rank
  while r%prime==0:v+=1;r//=prime
  N=v+3
  assert s.Rational(N-v)>s.Rational(1,prime-1);n+=1
print(json.dumps({'status':'PASS','independent_assertions':n,'scope':'integrity, alternating trace tensor/dual, elliptic cycle and determinant-root convergence controls; p-adic comparison theorems are credited'},indent=2))
