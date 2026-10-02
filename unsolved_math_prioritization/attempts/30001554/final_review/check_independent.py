from pathlib import Path
import json,hashlib,itertools
p=Path('/workspace/shared/research_involution_30001554/checkpoint');src=p.parent/'sources';checks=0
for mf in ['FINAL_FROZEN_MANIFEST.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]:
 data=json.loads((p/mf).read_text());fs=data.get('files',data)
 if isinstance(fs,list):fs={f['path']:f['sha256'] for f in fs}
 for name,h in fs.items():
  if isinstance(h,dict):h=h['sha256']
  assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h;checks+=1
for name,f in json.loads((p/'SOURCE_MANIFEST.json').read_text())['files'].items():assert hashlib.sha256((src/name).read_bytes()).hexdigest()==f['sha256'];checks+=1
def params(w,theta):
 n=len(w)
 def bordered(v):return any(tuple(theta[c] for c in v[:k])==v[-k:] for k in range(1,len(v)))
 t=max(j-i for i in range(n) for j in range(i+1,n+1) if not bordered(w[i:j]))
 period=min(q for q in range(1,n+1) if all(w[i+q]==theta[w[i]] for i in range(n-q)))
 return t,period
for theta,N in [((1,0),10),((1,0,2),7),((0,1),9)]:
 for n in range(1,N+1):
  for w in itertools.product(range(len(theta)),repeat=n):
   t,q=params(w,theta);assert t<=q;checks+=1
   if n>=2*q-1:assert t==q;checks+=1
   if n>=3*t:assert t==q;checks+=1
for L in range(2,15,2):
 for a in range(1,10):
  for c in range(1,10):
   z=(0,)*a+(1,)*L+(0,)*c;w=tuple(v^(i%2) for i,v in enumerate(z));M=max(a,c)
   expected=(L,L) if M<=L else ((L+2,2*L+1) if M==L+1 else (M+L+1-M%2,)*2)
   assert params(w,(1,0))==expected;checks+=1
for t,word,q in [(4,'01001101',5),(5,'0100011101',7),(6,'01010010110101',9),(7,'0101000101110101',11)]:
 assert params(tuple(map(int,word)),(1,0))==(t,q);checks+=1
print(json.dumps({'status':'PASS','independent_assertions':checks,'scope':'integrity, literal factor/period checks, three-run classification and sharp lower witnesses; full Python/C++ canonical streams separately replayed'},indent=2))
