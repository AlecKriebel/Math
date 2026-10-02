from pathlib import Path
import hashlib,json,itertools
import sympy as s
p=Path('/workspace/shared/math-30001563-final');src=Path('/workspace/shared/math-30001563/sources');n=0
man=json.loads((p/'FINAL_SOURCE_MANIFEST.json').read_text());fs=man.get('files',man)
if isinstance(fs,list):fs={f.get('path',f.get('name')):f['sha256'] for f in fs}
for name,h in fs.items():
 if isinstance(h,dict):h=h['sha256']
 assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h;n+=1
for f in json.loads((p/'SOURCE_MANIFEST.json').read_text())['files']:assert hashlib.sha256((src/f['name']).read_bytes()).hexdigest()==f['sha256'];n+=1
z=s.symbols('z');M=s.Matrix([[1,0,0,1],[0,0,1,1],[1,1,0,0],[0,1,0,0]]);poly=z**4-z**3-2*z*z+2*z-1
assert M.charpoly(z).as_expr()==poly;n+=1
R=s.Matrix([1,z*(z-1),(1+z*(z-1))/z,z-1]);L=s.Matrix([[1,z*(z-1),z-1,(1+z*(z-1))/z]])
for v in list(M*R-z*R)+list(L*M-z*L):assert s.rem(s.together(v*z).expand(),poly,z)==0;n+=1
U=set(tuple(map(int,line.split(','))) for line in (p/'U_CERTIFIED.csv').read_text().splitlines())
alpha=(0,1,3,4);index={x:i for i,x in enumerate(alpha)};morph={0:(0,3),1:(4,3),3:(1,),4:(0,1)}
def unit(c):return tuple(int(c==a) for a in alpha)
def vecadd(*v):return tuple(map(sum,zip(*v)))
def neg(v,k=1):return tuple(-k*x for x in v)
def mv(v):return (v[0]+v[3],v[2]+v[3],v[0]+v[1],v[1])
zero=(0,)*4
edges={a:[(b,zero if j==0 else unit(morph[a][0])) for j,b in enumerate(morph[a])] for a in alpha}
w=(0,)
for _ in range(5):w=tuple(b for a in w for b in morph[a])
prefix=[zero]
for c in w:prefix.append(vecadd(prefix[-1],unit(c)))
seen=set()
for l,r in [(0,1),(3,4),(5,6)]:
 for ends in [(l,l,l,r),(l,l,r,r),(l,r,r,r)]:
  a,b,c,d=ends;u=vecadd(prefix[c],neg(prefix[b],2),prefix[a]);v=vecadd(prefix[d],neg(prefix[c],2),prefix[b]);seen.add((tuple(w[i] for i in ends),u,v))
queue=list(seen);checked=0
# Direct vector transitions, no packed-index or cached-next-vector machinery.
for chars,u,v in queue:
 assert not(sum(u)==0 and sum(a*b for a,b in zip(alpha,u))==0 and sum(v)==0 and sum(a*b for a,b in zip(alpha,v))==0);n+=1
 mu=mv(u);mvv=mv(v)
 for branches in itertools.product(*(edges[a] for a in chars)):
  letters,ls=zip(*branches);uu=vecadd(mu,ls[2],neg(ls[1],2),ls[0]);vv=vecadd(mvv,ls[3],neg(ls[2],2),ls[1]);checked+=1
  if uu not in U or vv not in U:continue
  state=(letters,uu,vv)
  if state not in seen:seen.add(state);queue.append(state)
assert len(seen)==135572 and checked==1129490;n+=1
rows=sorted((sum(index[a]*4**i for i,a in enumerate(chars)),u,v) for chars,u,v in seen)
stream='\n'.join(','.join(map(str,(c,)+u+v)) for c,u,v in rows)+'\n'
digest=hashlib.sha256(stream.encode()).hexdigest()
expected=json.loads((p/'CERTIFIED_LARGER_GRAPH_REPLAY.json').read_text())['reachable_stream_sha256']
assert digest==expected;n+=1
print(json.dumps({'status':'PASS','independent_assertions':n,'direct_vector_states':len(seen),'outgoing_edges':checked,'reachable_stream_sha256':digest,'scope':'independent direct-vector closure and eigenvector identities; author directed-interval certificate separately replayed'},indent=2))
