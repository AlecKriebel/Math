"""Exact GF(2) odd-cover relaxation; certificate is not a positive tiling."""
from pathlib import Path
import sys,json,hashlib
from collections import Counter
from tile_model import D4
W=int(sys.argv[1]);H=int(sys.argv[2]);size=W*H;target=((1<<size)-1)|(1<<size)
placements=[];columns=[]
for ori,q in enumerate(D4):
 for y in range(H-max(b for a,b in q)):
  for x in range(W-max(a for a,b in q)):
   bits=sum(1<<(x+a+W*(y+b)) for a,b in q)|(1<<size)
   placements.append({'x':x,'y':y,'orientation':ori});columns.append(bits)
basis={}
for j,col in enumerate(columns):
 v=col;comb=1<<j
 while v:
  k=v.bit_length()-1
  if k in basis:v^=basis[k][0];comb^=basis[k][1]
  else:basis[k]=(v,comb);break
v=target;comb=0
while v:
 k=v.bit_length()-1
 if k not in basis:break
 v^=basis[k][0];comb^=basis[k][1]
out={'width':W,'height':H,'number_legal_placements':len(placements),'rank':len(basis),'augmented_dimension':size+1,'odd_cover_exists_mod2':not v}
if not v:
 ids=[j for j in range(len(columns)) if comb>>j&1];counts=Counter();xor=0
 for j in ids:
  xor^=columns[j];p=placements[j]
  for a,b in D4[p['orientation']]:counts[p['x']+a,p['y']+b]+=1
 assert xor==target and len(ids)%2==1 and len(counts)==size and all(n%2 for n in counts.values())
 out.update(selected_placements=[placements[j] for j in ids],selected_count=len(ids),coverage_histogram=dict(sorted(Counter(counts.values()).items())),is_positive_exact_cover=all(n==1 for n in counts.values()))
else:
 free=v.bit_length()-1;dual=0
 for i in range(size+1):
  z=1<<i
  for k in sorted(basis,reverse=True):
   if z>>k&1:z^=basis[k][0]
  if z>>free&1:dual|=1<<i
 assert all((col&dual).bit_count()%2==0 for col in columns) and (target&dual).bit_count()%2==1
 out.update(dual_color_bitmask=str(dual))
path=Path(__file__).with_name(f'parity_{W}x{H}.json');path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='selected_placements'},indent=2))
