if not __debug__:
    raise RuntimeError("Verification requires assertions; rerun without -O or PYTHONOPTIMIZE.")

import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent
z=json.loads((ROOT/'example_tiling.json').read_text());N=z['side'];T=z['tiles'];n=len(T)
assert all(s>0 and 0<=x and 0<=y and x+s<=N and y+s<=N for x,y,s in T)
A=[set() for _ in T]
for i,(x,y,s) in enumerate(T):
 for j,(a,b,t) in enumerate(T[:i]):
  dx=min(x+s,a+t)-max(x,a);dy=min(y+s,b+t)-max(y,b)
  assert not(dx>0 and dy>0)
  if dx>=0 and dy>=0:A[i].add(j);A[j].add(i)
assert sum(s*s for x,y,s in T)==N*N
vertices=set((x+dx*s,y+dy*s)for x,y,s in T for dx in [0,1] for dy in [0,1])
max_meet=max(sum(x<=a<=x+s and y<=b<=y+s for x,y,s in T) for a,b in vertices)
assert max_meet<=3
masks={}
for k in ['left','right','bottom','top']:masks[k]=sum(1<<i for i,(x,y,s) in enumerate(T) if {'left':x==0,'right':x+s==N,'bottom':y==0,'top':y+s==N}[k])
allmask=(1<<n)-1
adj=[sum(1<<j for j in x) for x in A]
def cross(mask,src,dst):
 seen=mask&masks[src];front=seen
 while front:
  new=0
  while front:
   b=front&-front;front-=b;new|=adj[b.bit_length()-1]
  front=(new&mask)&~seen;seen|=front
 return bool(seen&masks[dst])
H=[];V=[];piv=[0]*n
for mask in range(1<<n):
 h=cross(mask,'left','right');v=cross(mask,'bottom','top')
 assert h != cross(allmask^mask,'bottom','top')
 formula=bool((mask & (1<<3)) and (mask & ((1<<0)|(1<<2)|(1<<5))) and (mask & ((1<<1)|(1<<4)|(1<<6))) or not(mask & (1<<3)) and (mask & (1<<0)) and (mask & (1<<1)))
 assert h == formula
 H.append(int(h));V.append(int(v))
for i in range(n):
 piv[i]=sum(H[m]!=H[m^(1<<i)] for m in range(1<<n))
result={'tile_count':n,'configurations':1<<n,'max_tiles_at_vertex':max_meet,'black_horizontal':str(Fraction(sum(H),1<<n)),'black_vertical':str(Fraction(sum(V),1<<n)),'duality_all_configurations':True,'influences':[str(Fraction(p,1<<n)) for p in piv],'H_by_black_count':[sum(H[m] for m in range(1<<n) if m.bit_count()==k)for k in range(n+1)],'V_by_black_count':[sum(V[m] for m in range(1<<n) if m.bit_count()==k)for k in range(n+1)]}
print(json.dumps(result,indent=2));(ROOT/'exact_crossings_results.json').write_text(json.dumps(result,indent=2)+'\n')
