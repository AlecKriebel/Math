#!/usr/bin/env python3
"""Independent exact cone-cycle, source-angle and lattice controls.

These do not prove the Veech or hyperelliptic theorems; see REVIEW.md.
"""
from fractions import Fraction as F
from math import gcd
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json

C=Counter()
def ck(name,v):
 assert v,name
 C[name]+=1

def labels(n,a,b,parity=None):
 # a,b are alpha,beta in units pi/(2n). Transcription of the four printed branches.
 out=set();h=n//2
 for k in range(n-1):
  lower=2*n-4*(k+1);upper=4*(n-k-2)
  small1=k<=h-1 if n%2==0 else k<=h+1
  small2=k<=h-1
  large=k>=h-1 if n%2==0 else k>=h
  clauses=[('even',small1 and a<=lower and b-a==4*(k+1)),
           ('odd',small2 and a>=lower and b+a==4*(n-k-1)),
           ('even',large and a>=upper and b-a==4*(k+3-n)),
           ('odd',large and a<=upper and b+a==4*(n-k-1))]
  if any(ok and (parity is None or p==parity) for p,ok in clauses):out.add(k%(n-2))
 return out

# Construct the actual cyclic corner order by traversing paired polygon edges.
for n in range(3,25):
 unvisited={(s,j) for s in (0,1) for j in range(n)};cycles=[];lookup={}
 for start in ((0,0),(1,0)):
  if start not in unvisited:continue
  cyc=[];v=start
  while v not in cyc:
   ck('corner_not_previously_identified',v in unvisited)
   lookup[v]=(len(cycles),len(cyc));cyc.append(v);unvisited.remove(v)
   v=(1-v[0],(v[1]+1)%n)
  ck('closed_corner_cycle',v==start);cycles.append(cyc)
 ck('all_corners_covered',not unvisited)
 ck('vertex_count',len(cycles)==(1 if n%2 else 2))
 genus=F(n-len(cycles),2)
 ck('genus',(genus==F(n-1,2) if n%2 else genus==F(n-2,2)))
 ck('hyperelliptic_fixed_count',n+n%2==2*genus+2)
 for corner,(cid,t) in lookup.items():
  s,j=corner;base=0 if cid==0 else n
  ck('actual_corner_boundary_direction',(base+t*(n-2)-(s*n-2*j))%(2*n)==0)
  image=lookup[(1-s,j)]
  ck('iota_vertex_action',(image[0]==cid)==(n%2==1))

 r=n-2 if n%2 else (n-2)//2
 for (s,j),(cid,t) in lookup.items():
  e=int(cid!=0)
  # Move the terminal germ by iota precisely when it is at the other cone point.
  ct=lookup[(1-s,j)][1] if e else t
  parity='odd' if s==0 else 'even'
  for a in range(0,2*(n-2)+1):
   for b in range(4,2*n+1):
    off=2*n-b if s==0 else b-4
    diff=ct*2*(n-2)+off-a-(1-e)*2*n
    if diff%(4*n):continue
    m=diff//(4*n)
    intrinsic=(2*m+1-e)%(n-2)
    ck('geometric_to_printed_type',labels(n,a,b,parity)=={intrinsic})
    # Reflection of the physical corner offsets, preserving segment parity.
    ar=2*(n-2)-a;br=2*n+4-b
    ck('source_reflection_weight',labels(n,ar,br,parity)=={(-intrinsic)%(n-2)})
    mr=(-m-1 if e==0 else -m)%r
    ck('intrinsic_reverse',((2*mr+1-e)%(n-2))==(-intrinsic)%(n-2))

 # Check the exact chord label via the full printed definition, including both sides.
 for j in range(1,n):
  a=2*(n-1-j);b=2*(n+1-j)
  ks=labels(n,a,b,'odd');ck('direct_chord_label',ks=={(j-1)%(n-2)})
  k=next(iter(ks));ck('direct_chord_weight',j in (k+1,n-(k+1)))
 for k in range(n-2):
  neg=(-k)%(n-2)
  ck('canonical_weight_reversal',neg+1==k+1 or neg+1==n-(k+1))

# A diagnostic showing why the preceding source parity convention is essential.
ck('source_overlap_without_parity',labels(5,4,8)=={0,1})
ck('source_overlap_resolved_by_odd_parity',labels(5,4,8,'odd')=={1})

# Nonlinear increasing antipodal angular maps, in units of pi, with arbitrary sheets.
def H(x):
 z=x.numerator//x.denominator;y=x-z
 return z+(y/2 if y<=F(1,2) else F(1,4)+F(3,2)*(y-F(1,2)))
for r in range(1,17):
 for sheet in (-5,0,7):
  for a in (F(-7,3),F(0),F(2,7),F(5,4)):
   for m in range(r):
    ck('same_cone_antipodal_lift',H(a+1+2*m)+2*sheet-(H(a)+2*sheet)==1+2*m)
    ck('opposite_cone_iota_lift',H(a+2*m)+2*sheet-(H(a)+2*sheet)==2*m)

# Direct first-marked-vertex search, then all twelve lattice dihedral transforms.
def rotate(v):p,q=v;return p-q,p
def reflect(v):p,q=v;return q,p
def norm(v):p,q=v;return p*p-p*q+q*q
def hex_data(v):
 for scale in range(1,5):
  p,q=(scale*x for x in v)
  if (p+q)%3!=2:break
 ck('hex_first_marked_vertex',scale<=2)
 ck('hex_no_intermediate_mark',all((t*sum(v))%3==2 for t in range(1,scale)))
 if (p%3,q%3)==(1,2):k=1
 elif p%2==q%2==0:k=2
 elif (p%3,q%3)==(2,1):k=3
 else:k=0
 w2={0:F(1,4),1:F(3,4),2:F(1),3:F(3,4)}[k]
 return F(norm((p,q)))/w2

directions=0
for p in range(-13,14):
 for q in range(-13,14):
  if gcd(p,q)!=1:continue
  directions+=1;v=(p,q);base=hex_data(v)
  vv=v
  for turn in range(6):
   for z in (vv,reflect(vv)):
    ck('hex_dihedral_norm',norm(z)==norm(v))
    ck('hex_dihedral_primitive',gcd(*z)==1)
    ck('hex_dihedral_ratio',hex_data(z)==base)
   vv=rotate(vv)
  ck('hex_rotation_order',vv==v)
  ck('square_type_parity',(p%2==q%2==1)==((-q)%2==p%2==1))

root=Path(__file__).resolve().parent
receipt={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(sorted(C.items())),'primitive_lattice_directions':directions,'artifact_sha256':sha256((root/'author_replay/CANDIDATE.md').read_bytes()).hexdigest(),'scope':'Exact cone-cycle/source-label, reflected-weight and finite lattice diagnostics; no computational proof of Veech cusp reduction or hyperelliptic uniqueness.'}
(root/'independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
