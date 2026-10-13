from pathlib import Path
from itertools import product
from math import gcd
import hashlib,json
p=Path('/workspace/shared/math-30001552');n=0
for mf in ['FINAL_AUTHOR_MANIFEST.json','SOURCE_HASHES.json']:
 for name,h in json.loads((p/mf).read_text()).items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h;n+=1
for flip in [0,1]:
 def theta(w):return tuple(x^flip for x in reversed(w))
 def alternating(w,k):
  block=w[:k]+theta(w[:k]);return all(w[i]==block[i%(2*k)] for i in range(len(w)))
 for L in range(1,13):
  for w in product(range(2),repeat=L):
   periods=[k for k in range(1,L+1) if alternating(w,k)]
   W=theta(w)+w
   for k in periods:
    assert all(W[i]==W[i+2*k] for i in range(2*L-2*k));n+=1
   for a in periods:
    for b in periods:
     g=gcd(a,b)
     if L>=a+b-g:assert alternating(w,g);n+=1
# Reversal sharpness, independently of final loop's flip.
w=(0,1,1)
def rev_alt(k):
 z=w[:k]+tuple(reversed(w[:k]));return all(w[i]==z[i%(2*k)] for i in range(len(w)))
assert rev_alt(2) and rev_alt(3) and not rev_alt(1);n+=1
print(json.dumps({'status':'PASS','independent_assertions':n,'binary_lengths':'1 through 12','involutions':'reversal and reversal-complement','scope':'supplemental finite checks, proof is the universal reflection reduction'},indent=2))
