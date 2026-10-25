#!/usr/bin/env python3
"""Independent exact mechanism controls; no submitted helper or data imported.
Finite models test interfaces, not Baire category or infinite Borel hyperfiniteness.
"""
from pathlib import Path
from itertools import product
from collections import deque,defaultdict
from math import factorial
from datetime import datetime,timezone
import json
O=Path(__file__).resolve().parent

def rotate(v,k):
 n=len(v);return tuple(v[(i-k)%n] for i in range(n))
def add(v,i,d,q):
 w=list(v);w[i%len(v)]=(w[i%len(v)]+d)%q;return tuple(w)
def t(x,k):return rotate(x[0],k),(x[1]+k)%H
def lamp(x,i,d=1):return add(x[0],i,d,Q),x[1]
def coord(x,m):
 r=x[1]%m;return t(x,-r),r
def graph(states,m,uncut=False):
 E={x:set() for x in states}
 for x in states:
  for y in [lamp(x,0)]+([t(x,1)] if uncut or x[1]%m<m-1 else []):
   if y!=x:E[x].add(y);E[y].add(x)
 return E
def distances(E,x,R=None):
 d={x:0};todo=deque([x])
 while todo:
  z=todo.popleft()
  if R is not None and d[z]>=R:continue
  for y in E[z]:
   if y not in d:d[y]=d[z]+1;todo.append(y)
 return d
def components(E):
 left=set(E);out=[]
 while left:
  comp=set(distances(E,next(iter(left))));left-=comp;out.append(comp)
 return out

def threshold_colored(E,color,R):
 out={x:set() for x in E}
 for x in E:
  for y in distances(E,x,R):
   if x!=y and color(x)==color(y):out[x].add(y)
 return out

model_results=[];wrong_sign_witness=None;wrap_witness=None;endpoint_witness=None
for L,Q,H in [(3,2,6),(4,2,12),(2,4,6),(5,1,6)]:
 states=list(product(product(range(Q),repeat=L),range(H)));states=[(tuple(v),h) for v,h in states]
 widths=[m for m in range(1,H+1) if H%m==0]
 edges={m:graph(states,m) for m in widths};rows=[]
 for m in widths:
  B=[x for x in states if x[1]%m==0]
  assert len(B)*m==len(states)
  assert len({coord(x,m) for x in states})==len(states)
  for x in states:
   z,r=coord(x,m);assert t(z,r)==x
   z2,r2=coord(lamp(x,0),m)
   assert r2==r and z2==lamp(z,-r)
   if wrong_sign_witness is None and z2!=lamp(z,r):
    wrong_sign_witness={'model':[L,Q,H],'width':m,'point':x,'correct_base':z2,'wrong_base':lamp(z,r)}
   if r<m-1:assert coord(t(x,1),m)==(z,r+1)
   elif m<H and wrap_witness is None:
    z2,r2=coord(t(x,1),m)
    assert z2!=z
    wrap_witness={'model':[L,Q,H],'width':m,'point':x,'uncut_wrap_changes_base_from':z,'to':z2}
  assert max(map(len,edges[m].values()))<=4
  base={z:set() for z in B}
  for z in B:
   for i in range(m):
    for sg in [-1,1]:
     zz=lamp(z,-i,sg)
     if zz!=z:base[z].add(zz)
  color=lambda z:(z[0][0]%2,(z[1]//m)%2)
  rb=[]
  for R in [1,2,3]:
   base_thr=threshold_colored(base,color,R);Cs=components(base_thr);C=max(map(len,Cs))
   lifted=threshold_colored(edges[m],lambda x:color(coord(x,m)[0]),R)
   lifted_comps=components(lifted)
   base_id={z:i for i,c in enumerate(Cs) for z in c}
   for comp in lifted_comps:
    assert len(comp)<=m*C
    projected={coord(x,m)[0] for x in comp}
    assert len({base_id[z] for z in projected})==1
    # A simple path in the endpoint threshold graph has <= |component|-1 steps.
    for x in comp:
     actual=distances(edges[m],x)
     assert max(actual[y] for y in comp)<=R*(len(comp)-1)
   rb.append({'R':R,'base_component_bound':C,'lifted_max_size':max(map(len,lifted_comps)),'bound':m*C})
  rows.append({'width':m,'base_points':len(B),'slab_components':len(components(edges[m])),'radius_controls':rb})
 for m in widths:
  for M in widths:
   if M%m==0:assert all(edges[m][x]<=edges[M][x] for x in states)
 # Endpoint-only color criterion matters: a two-step path can cross other colors.
 if (L,Q,H)==(2,4,6):
  m=2;x=((0,0),0);y=((2,0),0)
  col=lambda v:coord(v,m)[0][0][0]%2
  assert col(x)==col(y)==0 and distances(edges[m],x)[y]==2
  mono={v:{w for w in edges[m][v] if col(w)==col(v)} for v in states}
  assert y not in distances(mono,x)
  endpoint_witness={'model':[L,Q,H],'width':m,'x':x,'y':y,'ordinary_distance':2,'connected_in_same_color_unit_graph':False,'connected_in_same_color_radius2_graph':True}
 model_results.append({'L':L,'lamp_modulus':Q,'height_modulus':H,'states':len(states),'nonfree_action':True,'widths':rows})
assert wrong_sign_witness and wrap_witness and endpoint_witness

# Exact dense-subset model of atomwise Cantor homeomorphism. Integers encode
# binary sequences including negative eventually-one sequences; unary prefix codes
# partition Cantor tails into q nonempty clopen copies. No finite-action approximation.
def decode_tail(z,copies):
 if copies==1:return 0,z
 j=0
 while j<copies-1 and ((z>>j)&1):j+=1
 length=j+1 if j<copies-1 else copies-1
 return j,z>>length
def encode_tail(j,u,copies):
 if copies==1:return u
 length=j+1 if j<copies-1 else copies-1
 return (u<<length)|((1<<j)-1)
def factor_maps(s,copies,depth):
 m=2**s;n=m*copies;mask=2**depth-1
 def h(x):
  atom=x&mask;j,u=decode_tail(x>>depth,copies)
  return (u<<depth)|atom,(x%m)+m*j
 def hi(u,label):
  assert label%m==u%m
  j=(label-(u%m))//m
  assert 0<=j<copies
  tail=encode_tail(j,u>>depth,copies)
  return (tail<<depth)|(u&mask)
 def beta(x,k):
  u,label=h(x);return hi(u+k,(label+k)%n)
 return m,n,h,hi,beta
lifting=[]
for s,copies,depth in [(0,3,4),(1,3,5),(2,5,6),(2,1,4)]:
 m,n,h,hi,beta=factor_maps(s,copies,depth);cases=0
 for x in range(-180,181):
  u,label=h(x);assert hi(u,label)==x and label%m==x%m
  for k in [-9,-2,-1,0,1,2,11]:
   y=beta(x,k)
   assert h(y)==(u+k,(label+k)%n)
   assert y%(2**depth)==(x+k)%(2**depth)
   assert beta(y,-k)==x
   assert beta(beta(x,k),3)==beta(x,k+3)
   cases+=1
 witness=next((x for x in range(-20,21) if beta(x,n)!=x),None)
 assert witness is not None
 lifting.append({'old_modulus':m,'new_modulus':n,'preserved_prefix_bits':depth,'signed_orbit_checks':cases,'factor_period_does_not_imply_action_period':{'x':witness,'beta_to_new_modulus':beta(witness,n)}})

# Exceptional normalized model with integer heights: N acts on a finite base;
# the symbolically unbounded height coordinate is tested through growing bands.
L,Q=3,2;B=[(v,tag) for v in product(range(Q),repeat=L) for tag in range(2)]
J=4;states=[(b,k) for b in B for k in range(-J,J+1)]
def Fj_key(b,j):v,tag=b;return tag,tuple(v[min(j,L):])
def Hj_key(x,j):
 b,k=x
 return ('band',Fj_key(b,j)) if abs(k)<=j else ('singleton',x)
previous=None;exceptional=[]
for j in range(J+1):
 classes=defaultdict(list)
 for x in states:classes[Hj_key(x,j)].append(x)
 assert all(len(v)<=(2*j+1)*2**min(j,L) for v in classes.values())
 if previous:
  for old in previous:assert len({Hj_key(x,j) for x in old})==1
 previous=list(classes.values())
 exceptional.append({'stage':j,'classes':len(classes),'max_class_size':max(map(len,classes.values())),'symbolic_band_bound':(2*j+1)*2**min(j,L)})
for x in states:
 for y in states:assert (Hj_key(x,J)==Hj_key(y,J))==(x[0][1]==y[0][1])
# Without the band, even pulling back identity yields the whole integer height fibre.
unbanded=[{'window':j,'preimage_of_single_base_point_size':2*j+1} for j in [1,2,4,8,16]]

# Factorial cuts: exact nesting, persistent integer -1, and no finite-stage certificate.
cut=[]
for h in range(-40,41):
 allowed=[h%factorial(n)<factorial(n)-1 for n in range(1,7)]
 assert all(not allowed[i] or allowed[i+1] for i in range(len(allowed)-1))
 assert any(allowed)==(h!=-1)
 if h in [-25,-7,-1,0,5]:cut.append({'integer_height':h,'allowed_at_widths_1_2_6_24_120_720':allowed})
finite_prefix=[]
for N in range(2,7):
 h=-1+factorial(N)
 assert all(h%factorial(n)==factorial(n)-1 for n in range(1,N+1))
 assert h%factorial(N+1)!=factorial(N+1)-1
 finite_prefix.append({'checked_stages':N,'height_indistinguishable_from_minus1_at_those_stages':h,'admitted_next_stage':True})
r={'utc':datetime.now(timezone.utc).isoformat(),'submitted_helpers_read_or_imported':False,'finite_quotient_models':model_results,'reversed_conjugation_countercontrol':wrong_sign_witness,'uncut_wrap_countercontrol':wrap_witness,'endpoint_color_countercontrol':endpoint_witness,'cantor_prefix_lifting_controls':lifting,'exceptional_band_controls':exceptional,'unbanded_pullback_growth':unbanded,'factorial_cut_controls':cut,'finite_prefix_insufficiency':finite_prefix,'limits':['Finite quotient models satisfy finite residue equations only and cannot possess a full profinite equivariant height.','Cantor prefix tests support the explicit atomwise construction; the infinite homeomorphism/Baire proof is checked analytically, not inferred from samples.','Finite graphs or cardinality bounds alone do not prove Borel hyperfiniteness. The exact CJMST theorem supplies that step.']}
(O/'fresh-controls.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'utc':r['utc'],'quotient_models':len(model_results),'prefix_lift_families':len(lifting),'signed_prefix_orbit_checks':sum(x['signed_orbit_checks'] for x in lifting),'exceptional_stages':len(exceptional),'negative_mechanisms':['wrong conjugation sign','uncut wrap','monochromatic-path substitution','unbanded pullback','finite-factor mistaken for finite-order action','finite-prefix proof mistaken for profinite conclusion']},indent=2))
print('PASS independent finite and exact prefix controls; universal conclusions require the analytic proof audit.')
