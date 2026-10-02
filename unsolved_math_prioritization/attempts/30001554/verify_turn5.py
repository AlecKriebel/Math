from itertools import product
from math import comb
from pathlib import Path
import json
from word_tools import negative_periods,parameters
from finite_window_fast import search
root=Path(__file__).parent;checks=0

def check(x):
 global checks
 assert x;checks+=1
old=json.loads((root/'TURN_2_ENUMERATION.json').read_text())
# Cross-replay the genuinely different incremental-mask implementation.
for r in old:check(search(r['t'])==r)
r8=json.loads((root/'TURN_5_ENUMERATION_T8.json').read_text())
cpp=json.loads((root/'TURN_5_CPP_T8.json').read_text())
for k,v in cpp.items():check(r8[k]==v)
check(r8['leaf_sha256']==(root/'TURN_5_CPP_STREAM_SHA256.txt').read_text().split()[0])
# Test every incremental suffix-period mask against direct definitions.
mask_instances=0
for theta,N in [((1,0),10),((1,0,2),7),((1,0,3,2),6),((0,1),9)]:
 for w in product(range(len(theta)),repeat=N):
  masks=[]
  for m,a in enumerate(w):
   match=sum(1<<(m-j) for j,x in enumerate(w[:m]) if theta[x]==a)
   masks=[(old&match)|(1<<(m-i+1)) for i,old in enumerate(masks)]+[2]
   for i,mask in enumerate(masks):
    direct=sum(1<<p for p in negative_periods(w[i:m+1],theta))
    check(mask==direct);mask_instances+=1
# Combinatorial count of periodic canonical completions, without enumerating words.
A=[1];B=[1];F=[0]*9;N=[0]*9;S=[]
for m in range(8):
 A.append(sum(comb(m,k)*(1+2**k)*A[m-k] for k in range(m+1)))
 B.append(sum(comb(m,k)*B[m-k] for k in range(m+1)))
for p in range(1,9):
 F[p]=B[p]-sum(F[d] for d in range(1,p) if p%d==0)
 N[p]=A[p]-B[p]-sum(N[d] for d in range(1,p) if p%d==0 and (p//d)%2==1)
 S.append(sum(F[1:p+1])+sum(N[1:p+1]));check(S[-1]==(old+[r8])[p-1]['leaves'])
# Longest pre-saturation witnesses, independently direct-checked.
witnesses={4:'01001101',5:'0100011101',6:'01010010110101',7:'0101000101110101'}
z=[0]*7+[1]*6+[0]*7;witnesses[8]=''.join(str(x^(i%2)) for i,x in enumerate(z))
thresholds={4:9,5:11,6:15,7:17,8:21};proof_controls=[]
for t,L in thresholds.items():
 r=(old+[r8])[t-1];check(L>=2*t+1);check(r['nonperiodic_by_length'][L]==0)
 w=tuple(map(int,witnesses[t]));tau,p=parameters(w,(1,0));check((len(w),tau)==(L-1,t));check(p>t)
 proof_controls.append(dict(t=t,optimal_saturation_length=L,witness_word=witnesses[t],witness_tau=tau,witness_period=p))
for r in old[:3]:check(all(v==0 for v in r['nonperiodic_by_length']))
print(json.dumps(dict(assertions=checks,mask_instances=mask_instances,canonical_block_counts=A,ordinary_Bell_counts=B,fixed_primitive_counts=F,nonfixed_minimal_negative_counts=N,periodic_completion_counts=S,exact_thresholds=proof_controls,t8_stream_sha256=r8['leaf_sha256'],scope='Full t8 rerun remains a separate finite_window_fast.py --t8 command; C++ stream check is independent literal-border recursion.'),indent=2,sort_keys=True))
