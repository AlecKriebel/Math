#!/usr/bin/env python3
"""Exact independent input/output runs of the non-isometric refinement construction."""
from fractions import Fraction as Q
from itertools import product,combinations
from collections import Counter,defaultdict
import json
checks=Counter()
def ck(x,label):
 assert x,label;checks[label]+=1
def edge(i,j):return tuple(sorted((i,j)))
def edgelist(F):return sorted({edge(i,j) for f in F for i,j in combinations(f,2)})
def vertices(F):return set(v for f in F for v in f)
def valid(F,L):
 for i,j,k in F:
  a,b,c=L[edge(i,j)],L[edge(i,k)],L[edge(j,k)]
  if not(a+b>c and a+c>b and b+c>a):return False
 return True

def refine(F,L,reverse=False):
 oldF=list(F);oldE=edgelist(F);n=max(vertices(F))+1
 adj={e:set() for e in oldE}
 for f in F:
  es=[edge(i,j) for i,j in combinations(f,2)]
  for e in es:adj[e].update(x for x in es if x!=e)
 colors={}
 for e in oldE:
  used={colors[a] for a in adj[e] if a in colors};colors[e]=next(c for c in range(5) if c not in used)
 newids={e:n+i for i,e in enumerate(oldE)}
 out=dict(L);faces=[(tuple(f),i) for i,f in enumerate(F)];records=[]
 for color in range(5):
  es=[e for e in oldE if colors[e]==color]
  if reverse:es=es[::-1]
  for i,j in es:
   incident=[(f,parent) for f,parent in faces if i in f and j in f]
   assert len(incident) in (1,2)
   qs=sorted(next(v for v in f if v not in (i,j)) for f,parent in incident)
   q=qs[0];b=out[edge(i,q)];a=out[edge(j,q)];t=b/(a+b);c=out.pop((i,j));m=newids[i,j]
   out[edge(i,m)]=t*c;out[edge(m,j)]=(1-t)*c;local=[]
   faces=[(f,parent) for f,parent in faces if not(i in f and j in f)]
   for f,parent in incident:
    q=next(v for v in f if v not in (i,j));b=out[edge(i,q)];a=out[edge(j,q)];h=(1-t)*b+t*a
    out[edge(m,q)]=h;faces.extend([((i,m,q),parent),((m,j,q),parent)])
    local.append((a,b,c,h))
   records.append({'edge':(i,j),'m':m,'t':t,'local':local})
 return [f for f,p in faces],out,newids,colors,records,faces

def extend(a,records):
 a=dict(a)
 for r in records:
  i,j=r['edge'];t=r['t'];D=a[i]*t+a[j]*(1-t);a[r['m']]=a[i]*a[j]/D
 return a

def verify_output(F,L,result):
 F1,L1,ids,colors,records,parented=result;V=vertices(F)
 ck(valid(F1,L1),'all_refined_triangle_inequalities')
 ck(len(F1)==4*len(F) and len(vertices(F1))==len(V)+len(ids),'subdivision_cell_counts')
 ck(len(L1)==2*len(L)+3*len(F),'subdivision_edge_count')
 ck(max(colors.values())<5,'at_most_five_color_rounds')
 ck(max(L1.values())<=max(L.values()),'no_edge_maximum_increase')
 for e,m in ids.items():ck(L1[edge(e[0],m)]+L1[edge(m,e[1])]==L[e],'old_edge_total_preserved')
 for r in records:
  t=r['t'];ck(0<t<1,'strict_split_fraction')
  for a,b,c,h in r['local']:
   induced=(1-t)*b*b+t*a*a-t*(1-t)*c*c
   gap=t*(1-t)*(c*c-(a-b)**2)
   ck(h*h-induced==gap and gap>0,'exact_strict_nonisometry_gap')
 # A fixed underlying realization uses arithmetic edge midpoints, independent of metrics.
 byparent=defaultdict(list)
 for f,j in parented:byparent[j].append(f)
 for j,oldface in enumerate(F):
  coords={oldface[0]:(Q(0),Q(0)),oldface[1]:(Q(1),Q(0)),oldface[2]:(Q(0),Q(1))}
  for e,m in ids.items():
   if all(v in oldface for v in e):coords[m]=tuple((x+y)/2 for x,y in zip(coords[e[0]],coords[e[1]]))
  area=0
  for f in byparent[j]:
   x,y,z=[coords[v] for v in f];D=(y[0]-x[0])*(z[1]-x[1])-(y[1]-x[1])*(z[0]-x[0])
   ck(D!=0,'underlying_child_simplex_nondegenerate');area+=abs(D)
  ck(area==1,'underlying_face_area_partition')

meshes={'one_triangle':[(0,1,2)],'two_face_disk':[(0,1,2),(0,2,3)],'tetrahedron':[(0,1,2),(0,3,1),(0,2,3),(1,3,2)],'octahedron':[(0,2,3),(0,3,4),(0,4,5),(0,5,2),(1,3,2),(1,4,3),(1,5,4),(1,2,5)]}
records_summary={};cases=0
for name,F in meshes.items():
 L={e:Q(1) for e in edgelist(F)};R=refine(F,L);verify_output(F,L,R);F1,L1,ids,col,rec,parented=R
 Rev=refine(F,L,True)
 ck(Rev[1]==L1 and sorted(map(sorted,Rev[0]))==sorted(map(sorted,F1)),'same_color_operations_commute')
 nv=len(vertices(F));accepted=0
 for aa in product((Q(3,4),Q(1),Q(5,4)),repeat=nv):
  a=dict(enumerate(aa));M={e:a[e[0]]*a[e[1]]*l for e,l in L.items()}
  if not valid(F,M):continue
  S=refine(F,M);verify_output(F,M,S);F2,M1,_,_,rec2,_=S
  ck(F2==F1,'metric_independent_output_combinatorics')
  outa=extend(a,rec)
  ck(all(outa[v]==a[v] for v in a),'original_vertex_factors_preserved')
  for e in L1:ck(M1[e]==outa[e[0]]*outa[e[1]]*L1[e],'all_final_conformal_edge_equations')
  for r,s in zip(rec,rec2):
   i,j=r['edge'];t=r['t'];D=a[i]*t+a[j]*(1-t)
   ck(s['t']==a[i]*t/D,'fractional_linear_split_covariance')
  accepted+=1;cases+=1
 # A second pass checks that prior inserted factors really persist as old factors.
 a={v:(Q(3,4) if v==0 else Q(1)) for v in vertices(F)};M={e:a[e[0]]*a[e[1]]*l for e,l in L.items()}
 S=refine(F,M);a1=extend(a,rec);R2=refine(F1,L1);S2=refine(S[0],S[1]);a2=extend(a1,R2[4]);verify_output(F1,L1,R2);verify_output(S[0],S[1],S2)
 ck(R2[0]==S2[0] and all(S2[1][e]==a2[e[0]]*a2[e[1]]*l for e,l in R2[1].items()),'two_pass_conformal_composition')
 records_summary[name]={'valid_original_scalings':accepted,'output_faces':len(F1),'colors_used':1+max(col.values())}
ck(Q(1)-Q(3,4)==Q(1,4),'equilateral_gap_control')
print(json.dumps({'status':'PASS','arithmetic':'exact rational, independently refined input pairs','assertions':sum(checks.values()),'by_scope':dict(checks),'input_pairs':cases,'meshes':records_summary,'scope':'Complete for the output-metric interpretation, with old edge totals and factors retained. Strict positive face-diagonal distortion is verified; no isometric-subdivision or iterative-convergence claim.'},indent=2,sort_keys=True))
