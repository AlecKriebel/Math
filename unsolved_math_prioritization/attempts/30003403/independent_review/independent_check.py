"""Independent rational/dyadic controls for the Countryman partial package.
No author checker is imported. Finite tests do not prove any uncountable assertion.
"""
from fractions import Fraction as F
from itertools import product,combinations,combinations_with_replacement
from collections import Counter
import json
C=Counter()
def check(v,k):
 assert v,k
 C[k]+=1
W=8
pad=lambda s:tuple(s)+(0,)*(W-len(s))
left,right=pad((-4,)),pad((4,))
def binary_coordinate(s):return sum((F(1,2**(j+1)) if v==2 else -F(1,2**(j+1))) for j,v in enumerate(s))
section=[(left,F(-1)),(right,F(1))]
for n in range(6):
 for word in product((-2,2),repeat=n):section.append((pad((0,)+word),binary_coordinate(word)))
section.sort();coords=[q for _,q in section]
check(len(coords)==len(set(coords)),'dyadic_nodes_distinct')
check(all(a<b for a,b in zip(coords,coords[1:])),'dyadic_tree_order_embedding')
# Work with numerical ancestor endpoints rather than author word-valued classifier.
def quotient_coordinate(x):
 if x[0]<0:return F(-1)
 if x[0]>0:return F(1)
 center=F(0);radius=F(1)
 for v in x[1:]:
  if v<-2:return center-radius
  if v>2:return center+radius
  if v not in (-2,2):return center
  radius/=2;center+=radius if v==2 else -radius
 raise AssertionError('No eventual zero in tested ambient sequence')
samples=sorted({left,right}|{pad(word) for n in range(1,5) for word in product((-4,-3,-2,-1,0,1,2,3,4),repeat=n) if left<=pad(word)<=right})
ys=[]
for x in samples:
 y=quotient_coordinate(x);ys.append(y)
 check(y in coords,'dyadic_output_in_section')
 for z,q in section:
  check((z>=x or q<=y) and (z<=x or q>=y),'independent_cut_brackets')
for x,q in section:check(quotient_coordinate(x)==q,'dyadic_section_fixed')
for a,b in zip(ys,ys[1:]):check(a<=b,'dyadic_global_monotonicity')
# Appending a signed digit refines between any two binary nodes in these samples.
for i,(x,q) in enumerate(section[1:-1],1):
 for y,r in section[i+1:-1]:
  if q>=r:continue
  middle=(q+r)/2
  # Every dyadic in (-1,1) has a finite signed search-tree representation.
  center=F(0);step=F(1,2);word=[]
  while center!=middle:
   sign=2 if middle>center else -2;word.append(sign);center+=step if sign==2 else -step;step/=2
  node=pad((0,)+tuple(word)) if len(word)<W else None
  check(q<middle<r,'dyadic_dense_insert_coordinate')
  if node is not None:check(x<node<y,'dyadic_dense_insert_lexicographic')
# All sections of all finite monotone surjections, rather than one floor map.
for n in range(1,8):
 for m in range(1,min(n,4)+1):
  for cuts in combinations(range(1,n),m-1):
   edges=(0,)+cuts+(n,);fibers=[list(range(edges[i],edges[i+1])) for i in range(m)]
   f={x:i for i,Fiber in enumerate(fibers) for x in Fiber}
   for representatives in product(*fibers):
    retract=[representatives[f[x]] for x in range(n)]
    check(all(a<=b for a,b in zip(retract,retract[1:])),'all_finite_sections_monotone')
    check(all(retract[b]==b for b in representatives),'all_finite_sections_fix_range')
    for x,y in enumerate(retract):
     lo=[b for b in representatives if b<x];hi=[b for b in representatives if b>x]
     check(x in representatives or (lo and y==max(lo)) or (hi and y==min(hi)),'all_finite_sections_cut_criterion')
# Missing-alphabet separators control cuts at every arbitrary earlier position.
for n in range(1,5):
 for x in product((-3,-1,0,2,4),repeat=n):
  if 4 not in x and -3 not in x:continue
  xm=pad(x+(-1,));x0=pad(x);xp=pad(x+(2,))
  check(xm<x0<xp,'late_bracket_order')
  for z in product((-1,0,2),repeat=n+1):
   zz=pad(z)
   check((zz<xm)==(zz<x0)==(zz<xp),'late_bracket_cut_unchanged')
# Independent finite forcing extensions on a nonuniform rational domain.
D=[F(-2),F(-1,2),F(0),F(1,3),F(2)]
for n in range(1,6):
 for domain in combinations(D,n):
  for vals in combinations_with_replacement([-2,0,3],n):
   pairs=list(zip(domain,vals))
   for z in [F(-3),F(3)]+[(a+b)/2 for a,b in zip(domain,domain[1:])]:
    lower=[v for x,v in pairs if x<z];upper=[v for x,v in pairs if x>z]
    y=lower[-1] if lower else upper[0]
    extended=sorted(pairs+[(z,y)])
    check(all(a[1]<=b[1] for a,b in zip(extended,extended[1:])),'forcing_new_domain_extension')
   for y in [-3,-1,1,4]:
    lower=[x for x,v in pairs if v<y];upper=[x for x,v in pairs if v>y]
    z=(lower[-1]+upper[0])/2 if lower and upper else (lower[-1]+1 if lower else upper[0]-1)
    extended=sorted(pairs+[(z,y)])
    check(z not in domain and all(a[1]<=b[1] for a,b in zip(extended,extended[1:])),'forcing_new_range_extension')
# The two tempting coordinate formulas genuinely reverse an ordered pair.
check((0,1)<(1,0) and 1>0,'second_projection_negative_control')
a=((0,-1),(1,0));b=((0,1),(-1,0));inter=lambda p:tuple(t for pair in zip(*p) for t in pair)
check(a<b and inter(a)>inter(b),'interleaving_negative_control')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'scope':'Independent finite dyadic, section, normality-separator and forcing-extension controls. No finite test proves PFA, properness, or strong surjectivity for uncountable targets.'},indent=2,sort_keys=True))
