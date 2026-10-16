import random,json
from collections import Counter
from gaussian_matrix import matrix,matmul,scale,conj,Z
checks=0;gauges=0;rng=random.Random(780001201)
def check(x):
 global checks
 assert x;checks+=1
def data(L,u,v,mod):
 F={(x,y):(u[x,y]+v[(x+1)%L,y]-u[x,(y+1)%L]-v[x,y])%mod for x in range(L) for y in range(L)}
 return F,sum(u[x,0] for x in range(L))%mod,sum(v[0,y] for y in range(L))%mod
for L in [4,6,8,10]:
 for mod in [4,5,7,12]:
  for case in range(12):
   u={(x,y):rng.randrange(mod) for x in range(L) for y in range(L)};v={(x,y):rng.randrange(mod) for x in range(L) for y in range(L)}
   F,H,V=data(L,u,v,mod);check(sum(F.values())%mod==0)
   g={(0,0):0}
   for y in range(1,L):g[0,y]=(g[0,y-1]-v[0,y-1])%mod
   for y in range(L):
    for x in range(1,L):g[x,y]=(g[x-1,y]-u[x-1,y])%mod
   U={(x,y):(u[x,y]+g[(x+1)%L,y]-g[x,y])%mod for x,y in u};W={(x,y):(v[x,y]+g[x,(y+1)%L]-g[x,y])%mod for x,y in v}
   check(data(L,U,W,mod)==(F,H,V));h=H
   for y in range(L):
    w=V if y==L-1 else 0
    for x in range(L):
     check(U[x,y]==(h if x==L-1 else 0));check(W[x,y]==w);w=(w+F[x,y])%mod
    h=(h-sum(F[x,y] for x in range(L)))%mod
   check(h==H);gauges+=1
moments={}
for kind in ['quarter_flux','zero_flux','one_twist','two_twists']:
 L=4;u={(x,y):(2 if x==3 and kind in ['one_twist','two_twists'] else 0) for x in range(4) for y in range(4)}
 v={(x,y):(x if kind=='quarter_flux' else (2 if y==3 and kind=='two_twists' else 0)) for x in range(4) for y in range(4)}
 F,H,V=data(4,u,v,4);check(set(F.values())==({1} if kind=='quarter_flux' else {0}))
 T=matrix(L,u,v);T2=matmul(T,T);T3=matmul(T2,T);T4=matmul(T2,T2)
 for i in range(16):
  for j in range(16):
   check(T[i][j]==conj(T[j][i]))
   if kind in ['quarter_flux','two_twists']:check(T3[i][j]==scale(T[i][j],8))
 check(sum(T2[i][i][0] for i in range(16))==64);check(all(T2[i][i][1]==0 for i in range(16)))
 moments[kind]=sum(T4[i][i][0] for i in range(16))
check(moments=={'quarter_flux':512,'zero_flux':640,'one_twist':576,'two_twists':512})
# Exact walk-count obstruction; all four directed length3 displacements are unique.
for L in [8,10,12]:
 counts=Counter({(0,0):1})
 for t in range(3):
  nxt=Counter()
  for (x,y),n in counts.items():
   for a,b in [(1,0),(-1,0),(0,1),(0,-1)]:nxt[(x+a)%L,(y+b)%L]+=n
  counts=nxt
 for p in [(3,0),(L-3,0),(0,3),(0,L-3)]:check(counts[p]==1);check(p not in [(1,0),(L-1,0),(0,1),(0,L-1)])
print(json.dumps(dict(assertions=checks,gauge_reconstruction_cases=gauges,fourth_moments=moments,scope='Exact gauge and4x4 polynomial certificates; large-volume quarter-filling optimum unresolved.'),indent=2,sort_keys=True))
