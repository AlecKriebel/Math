from pathlib import Path
import json,hashlib,itertools
p=Path('/workspace/shared/math-30001014/research');src=p.parent/'source';n=0
for mf in ['SOURCE_GATE_MANIFEST.json','FINAL_AUTHOR_MANIFEST.json']+[f'TURN_{i}_MANIFEST.json' for i in range(1,6)]:
 for f in json.loads((p/mf).read_text())['files']:assert hashlib.sha256((p/f['path']).read_bytes()).hexdigest()==f['sha256'];n+=1
for f in json.loads((p/'SOURCE_MANIFEST.json').read_text())['sources']:assert hashlib.sha256((src/f['file']).read_bytes()).hexdigest()==f['sha256'];n+=1
def mul(a,b):
 out=list(a)
 for c in b:
  if out and out[-1]==c:out.pop()
  else:out.append(c)
 return tuple(out)
words=[()]
for length in range(1,9):words.extend(w for w in itertools.product(range(3),repeat=length) if all(w[i]!=w[i+1] for i in range(length-1)))
for w in words:
 neighbors=[mul((a,),w) for a in range(3)]
 if w:assert sorted(len(v)-len(w) for v in neighbors)==[-1,1,1]
 else:assert all(len(v)==1 for v in neighbors)
 n+=1
 for a in range(3):
  for b in range(3):assert mul((a,),mul(w,(b,)))==mul(mul((a,),w),(b,));n+=1
 for a in range(3):assert mul((a,),mul((),(a,)))==();n+=1
# Distinct ab-orbits of (ca)^j, finite controls of the reduced-word proof.
for j,k in itertools.product(range(1,20),range(-20,21)):
 g=(2,0)*j;h=(0,1)*k if k>=0 else (1,0)*(-k);v=mul(h,g)
 if k:assert v[0]!=2
 else:assert v==g
 n+=1
# Positive gap without rounding: 3>2sqrt(2) iff9>8.
assert 9>8;n+=1
print(json.dumps({'status':'PASS','independent_assertions':n,'reduced_words_checked':len(words),'scope':'integrity and exact group/tree controls; tensor norms and topology are audited in the written proof'},indent=2))
