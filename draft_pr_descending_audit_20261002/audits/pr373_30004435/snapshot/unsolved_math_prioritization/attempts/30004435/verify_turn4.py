from fractions import Fraction as F
from itertools import product
import json
checks=0;inputs=0;decoded=0
def check(x):
 global checks
 assert x;checks+=1
# Truncate the zero-run at2, then query at offset1,2 or4.
words=list(product(range(2),repeat=5))
def code(w):
 L=0
 while L<2 and w[L]==0:L+=1
 return w[2**L],2**L
# Full table of decisive observed prefixes; unknown coordinates are enumerated.
decisive={}
for r in range(5):
 for prefix in product(range(2),repeat=r+1):
  vals={code(w)[0] for w in words if w[:r+1]==prefix}
  if len(vals)==1:decisive[r,prefix]=next(iter(vals))
for w in words:
 y,R=code(w)
 check((R,w[:R+1]) in decisive);check(decisive[R,w[:R+1]]==y)
 check(all((r,w[:r+1]) not in decisive for r in range(R)))
# Decode past output centers-8,...,-N using only input j<=0.
errors={N:0 for N in range(1,9)};union_events={N:0 for N in range(1,9)}
for bits in product(range(2),repeat=13):
 x=dict(zip(range(-8,5),bits));inputs+=1
 ys={};hats={};rads={}
 for k in range(-8,0):
  w=tuple(x[k+j] for j in range(5));ys[k],rads[k]=code(w)
  r=min(4,-k);hats[k]=decisive.get((r,w[:r+1]),0);decoded+=1
  if rads[k]<=-k:check(hats[k]==ys[k])
 for N in range(1,9):
  bad=any(ys[k]!=hats[k] for k in range(-8,-N+1));boundary=any(rads[k]>-k for k in range(-8,-N+1))
  check(not bad or boundary);errors[N]+=bad;union_events[N]+=boundary
law={1:F(1,2),2:F(1,4),4:F(1,4)}
for N in errors:
 ub=sum(sum(p for r,p in law.items() if r>j) for j in range(N,9))
 check(F(errors[N],inputs)<=F(union_events[N],inputs)<=ub)
# Exact expectation-tail identity for every bounded cutoff of the heavy-tail example.
for cap in range(1,13):
 # L geometric, R capped at2^cap.
 law={2**l:F(1,2**(l+1)) for l in range(cap)};law[2**cap]=F(1,2**cap)
 expectation=sum(r*p for r,p in law.items());tailsum=sum(sum(p for r,p in law.items() if r>j) for j in range(2**cap))
 check(expectation==tailsum==F(cap,2)+1)
# Summable geometric radius tails and their remote sums.
for N in range(1,31):
 partial=sum(F(1,2**j) for j in range(N,N+20));check(partial==F(1,2**(N-1))*(1-F(1,2**20)))
print(json.dumps(dict(assertions=checks,input_configurations=inputs,decoded_coordinates=decoded,past_decoder_error_counts=errors,boundary_union_counts=union_events,scope='Finite truth-table controls for the proved finite-mean coding transfer; no general coding representation is asserted.'),indent=2,sort_keys=True))
