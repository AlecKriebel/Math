"""Independent exhaustive F2^2 noncommuting-action audit; imports no author code."""
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(q,k):
 assert q,k
 C[k]+=1
X=range(3);V=range(4);star=lambda x,y:(2*y-x)%3
# Bits represent (a,b); these three involutions generate GL(2,F2).
def act(x,v):
 a=v&1;b=v>>1
 if x==0:a,b=b,a
 elif x==1:a,b=a^b,b
 else:a,b=a,a^b
 return a+2*b
for x,y in product(X,repeat=2):
 for v in V:
  ck(act(star(x,y),v)==act(y,act(x,act(y,v))),'action_conjugation')
ck(any(act(0,act(1,v))!=act(1,act(0,v)) for v in V),'genuine_noncommutation')
pairs=[(x,y) for x,y in product(X,repeat=2) if x!=y]
def table(w):
 d={(x,x):0 for x in X};d.update(zip(pairs,w));return d
def df(f,x,y):return act(y,f[x]^act(x,f[y])^f[y])^f[star(x,y)]
cob={tuple(df(f,x,y) for x,y in pairs) for f in product(V,repeat=3)}
cocycles=[]
for w in product(V,repeat=6):
 p=table(w)
 valid=all(act(z,p[x,y])^p[star(x,y),z]==act(star(y,z),p[x,z]^act(star(x,z),p[y,z])^p[y,z])^p[star(x,z),star(y,z)] for x,y,z in product(X,repeat=3))
 if valid:cocycles.append(w)
ck(cob<=set(cocycles),'all_coboundaries_are_cocycles')
E=list(product(V,X));hist=Counter();lift_implications=0
for w in cocycles:
 p=table(w);kap=lambda x,y:act(star(x,y),p[x,y])
 def op(U,W):
  a,x=U;b,y=W
  return act(y,a^act(x,b)^b)^p[x,y],star(x,y)
 for U in E:ck(op(U,U)==U,'idempotent')
 for W in E:ck(len({op(U,W) for U in E})==len(E),'right_invertible')
 for U,W,Z in product(E,repeat=3):ck(op(op(U,W),Z)==op(op(U,Z),op(W,Z)),'extension_distributive')
 for x,y,z in product(X,repeat=3):
  L=act(z,kap(x,y))^kap(star(x,y),z)^act(star(star(x,y),z),kap(y,z))
  R=kap(y,z)^act(star(y,z),kap(x,z))^kap(star(x,z),star(y,z))
  ck(L==R,'independent_colored_RIII_weight_identity')
 for U,W in product(E,repeat=2):
  a,x=U;b,y=W;c,z=op(U,W);u=act(x,a);v=act(y,b)
  ck(act(z,c)==act(y,u)^v^act(z,v)^kap(x,y),'noncommuting_fiber_gauge')
 for f in product(V,repeat=3):
  pp={(x,y):p[x,y]^df(f,x,y) for x,y in product(X,repeat=2)}
  for U,W in product(E,repeat=2):
   a,x=U;b,y=W;c,z=op(U,W)
   new=act(y,(a^f[x])^act(x,b^f[y])^(b^f[y]))^pp[x,y]
   ck(new==c^f[z],'all_cochain_extension_gauges')
 # Closed two-braid sigma_1^3, represented by the actual extension switch.
 for x,y in product(X,repeat=2):
  colors=(x,y);weight=0
  for _ in range(3):
   u,v=colors;weight^=kap(u,v);colors=(v,star(u,v))
  if colors!=(x,y):continue
  direct=[];affine=[];kernel=[]
  for a,b in product(V,repeat=2):
   uv=((a,x),(b,y))
   for _ in range(3):uv=(uv[1],op(uv[0],uv[1]))
   if uv==((a,x),(b,y)):direct.append((a,b))
   # Build affine monodromy independently on coefficient pairs.
   cc=(x,y);aa=(a,b)
   for _ in range(3):
    u,v=cc;c,d=aa;aa=(d,act(v,c^act(u,d)^d)^p[u,v]);cc=(v,star(u,v))
   if aa==(a,b):affine.append((a,b))
   cc=(x,y);aa=(a,b)
   for _ in range(3):
    u,v=cc;c,d=aa;aa=(d,act(v,c^act(u,d)^d));cc=(v,star(u,v))
   if aa==(a,b):kernel.append((a,b))
  ck(direct==affine,'affine_fixedpoints_equal_lifts')
  ck(not direct or len(direct)==len(kernel),'fixedpoint_torsor_size')
  if direct:
   base=direct[0];ck({(base[0]^a,base[1]^b) for a,b in kernel}==set(direct),'fixedpoint_torsor_action')
   ck(weight==0,'published_one_way_lifting_control');lift_implications+=1
  hist[len(direct)]+=1
# Separate exhaustive scalar F3 action -1, containing non-coboundary cocycles.
scalar_cocycles=[];scalar_hist=Counter();zero_nonlift=0
for w in product(range(3),repeat=6):
 p=table(w)
 if all((2*p[x,y]+p[star(x,y),z]-2*p[x,z]-2*p[y,z]-p[star(x,z),star(y,z)])%3==0 for x,y,z in product(X,repeat=3)):scalar_cocycles.append(w)
for w in scalar_cocycles:
 p=table(w)
 for x,y in product(X,repeat=2):
  cc=(x,y);weight=0
  for _ in range(3):
   u,v=cc;weight=(weight+2*p[u,v])%3;cc=(v,star(u,v))
  if cc!=(x,y):continue
  sol=[]
  for a,b in product(range(3),repeat=2):
   cc=(x,y);aa=(a,b)
   for _ in range(3):
    u,v=cc;c,d=aa;aa=(d,(2*c+2*d+p[u,v])%3);cc=(v,star(u,v))
   if aa==(a,b):sol.append((a,b))
  ck(len(sol) in (0,9),'scalar_affine_fiber_size')
  if sol:ck(weight==0,'scalar_lift_implies_zero')
  elif weight==0:zero_nonlift+=1
  scalar_hist[len(sol)]+=1
ck(len(scalar_cocycles)==27,'exhaustive_scalar_cocycle_count')
print(json.dumps({'status':'PASS','model':'R3 with faithful noncommuting GL(2,F2) action on F2^2, plus exhaustive scalar F3 action -1','normalized_vector_cocycles':len(cocycles),'vector_coboundaries':len(cob),'noncoboundary_vector_cocycles':len(set(cocycles)-cob),'vector_trefoil_lift_histogram':dict(sorted(hist.items())),'scalar_normalized_cocycles':len(scalar_cocycles),'scalar_trefoil_lift_histogram':dict(sorted(scalar_hist.items())),'zero_scalar_nonliftable_cases_in_tested_family':zero_nonlift,'lift_implications_checked':lift_implications,'exact_assertions':sum(C.values()),'families':dict(C),'scope':'Independent finite algebra and colored RIII/affine diagnostics. General theorem, source coverage and arbitrary abelian coefficients are audited analytically.'},indent=2))
