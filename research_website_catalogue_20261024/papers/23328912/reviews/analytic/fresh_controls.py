#!/usr/bin/env python3
"""Fresh signed-corner and exact free-group controls from manuscript definitions."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter,defaultdict
from datetime import datetime,timezone
import json

def invword(w):return tuple(-x for x in reversed(w))
def red(w):
 st=[]
 for x in w:
  if st and st[-1]==-x:st.pop()
  else:st.append(x)
 return tuple(st)
def sub(w,m):return red(x for a in w for x in (m[a] if a>0 else invword(m[-a])))
def corners(word):return [frozenset((-word[i-1],word[i])) for i in range(len(word))]
checks=Counter()
def ck(ok,name):
 if not ok:raise ValueError(name)
 checks[name]+=1
# Base generators x=1,y=2,b=3. Corner occurrences retained until duplicate checks.
basefaces=[(1,2,-1,-2),(3,1,-3,-2)];basemulti=Counter(e for w in basefaces for e in corners(w));baseedges=set(basemulti)
ck(all(n==1 for n in basemulti.values()),'base_corner_multiplicities_simple')
ck(all(len(e)==2 for e in baseedges) and len(baseedges)==8,'base_link_eight_nondegenerate_edges')
lam={1:(2,),2:(1,),3:(-3,)}
for w in basefaces:
 image=sub(w,lam);maps=[]
 for sign in [1,-1]:
  for k in range(4):
   transported=tuple(w[(k+j)%4] if sign==1 else -w[(k-j-1)%4] for j in range(4))
   if transported==image:maps.append((k,sign))
 ck(len(maps)==1,'unique_square_dihedral_involution_map');k,sign=maps[0]
 ck(all((k+sign*(k+sign*j))%4==j for j in range(4)),'face_map_squares_to_identity')
# Q edge IDs p,q,r,s,d,e are1..6, labels in K are signed IDs.
edges={1:('B','A',1),2:('A','C',2),3:('D','C',1),4:('B','D',2),5:('A','B',3),6:('C','A',3)}
qfaces=[(1,2,-3,-4),(5,1,-6,-2)]
qverts=['A','B','C','D'];germs={v:set() for v in qverts};links={v:Counter() for v in qverts};qcorners=[]
def endpoints(h):
 a,b,l=edges[abs(h)];return (a,b) if h>0 else (b,a)
def label(h):return edges[abs(h)][2]*(1 if h>0 else -1)
for h,(a,b,l) in edges.items():germs[a].add(h);germs[b].add(-h)
for face in qfaces:
 for i,h in enumerate(face):
  vertex=endpoints(h)[0];ck(endpoints(face[i-1])[1]==vertex,'square_boundary_endpoints_match')
  edge=frozenset((-face[i-1],h));links[vertex][edge]+=1;qcorners.append((vertex,edge))
for v in qverts:
 ck(all(n==1 for n in links[v].values()),'Q_corner_multiplicities_simple')
 for endpoint in [0,1]:
  im=lambda h:label(h) if endpoint==0 else sub((label(h),),lam)[0]
  images={h:im(h) for h in germs[v]};ck(len(set(images.values()))==len(images),'endpoint_link_injective')
  imageedges={frozenset(im(h) for h in e) for e in links[v]};induced={e for e in baseedges if e<=set(images.values())}
  ck(imageedges==induced,'endpoint_link_full_induced')
ck([len(germs[v]) for v in qverts]==[4,3,3,2] and [len(links[v]) for v in qverts]==[3,2,2,1],'complete_Q_link_counts')
# Product-edge square attaching words rebuilt directly from endpoints and two maps.
z={v:4+i for i,v in enumerate(qverts)}
verticalfaces=[]
for h,(a,b,l) in edges.items():verticalfaces.append((l,z[b],-sub((l,),lam)[0],-z[a]))
Lmulti=Counter(e for f in basefaces+verticalfaces for e in corners(f));LE=set(Lmulti);LV=set().union(*LE)
ck(all(n==1 for n in Lmulti.values()),'Z_link_edges_have_no_hidden_multiplicities')
triangles=[]
for v,edge in qcorners:
 for endpoint in [0,1]:
  im=lambda h:label(h) if endpoint==0 else sub((label(h),),lam)[0]
  triangles.append(frozenset([z[v]*(1 if endpoint==0 else -1),*(im(h) for h in edge)]))
TM=Counter(triangles);LT=set(TM)
ck(all(len(t)==3 and n==1 for t,n in TM.items()),'Z_cube_corners_nondegenerate_distinct_triangles')
ck(all(frozenset(e) in LE for t in LT for e in combinations(t,2)),'triangle_faces_present')
cliques3={frozenset(c) for c in combinations(LV,3) if all(frozenset(e) in LE for e in combinations(c,2))}
cliques4=[c for c in combinations(LV,4) if all(frozenset(e) in LE for e in combinations(c,2))]
ck(cliques3==LT and not cliques4,'full_flag_condition_with_triangle_occurrences')
ck((len(LV),len(LE),len(LT))==(14,32,16),'Z_link_exact_f_vector')
ck((1,3+len(edges),2+len(edges),len(qfaces))!=(1,7,8,2),'wrong_vertical_edge_count_control')
ck((1,3+len(qverts),2+len(edges),len(qfaces))==(1,7,8,2),'Z_cells_and_Euler_zero')
# Omission of either repeated A corner is detected as a missing clique triangle.
Apositions=[i for i,(v,e) in enumerate(qcorners) if v=='A'];ck(len(Apositions)==3,'all_A_corner_occurrences_retained')
for i in Apositions[1:]:
 broken=triangles[:2*i]+triangles[2*i+2:];ck(set(broken)!=cliques3,'omitted_repeated_A_corner_detected')
# Original bx circle is not locally full at its intermediate vertex.
ck(frozenset((-3,1)) in baseedges,'raw_bx_circle_not_local_isometry')
# Exact free automorphism and semidirect normal form: a=1,b=2,c=3,t=4.
phi={1:(1,),2:(1,2),3:(2,3,2)};phiinv={1:(1,),2:(-1,2),3:(-2,1,3,-2,1)}
for g in range(1,4):ck(sub(sub((g,),phi),phiinv)==(g,) and sub(sub((g,),phiinv),phi)==(g,),'free_automorphism_two_sided_inverse')
def phipow(w,k):
 for _ in range(abs(k)):w=sub(w,phi if k>=0 else phiinv)
 return w
def normal(w):
 f=();k=0
 for h in w:
  if abs(h)==4:k+=1 if h>0 else -1
  else:f=red(f+phipow((h,),k))
 return f,k
# x,y,b,zA,zB,zC,zD to exact mapping torus.
old_to_new={1:(4,),2:(-1,4),3:(2,),4:(-3,-4)}
old_to_new[5]=sub((1,4,-2),old_to_new);old_to_new[6]=sub((-2,4,1),old_to_new);old_to_new[7]=sub((-2,1,4,-2,1),old_to_new)
for face in basefaces+verticalfaces:ck(normal(sub(face,old_to_new))==((),0),'all_eight_original_relators_in_exact_mapping_torus')
new_to_old={1:(1,-2),2:(3,),3:(-1,-4),4:(1,)}
for g in [1,2,3,4]:ck(sub(sub((g,),new_to_old),old_to_new)==(g,),'new_generator_substitutions_freely_inverse')
for g in [1,2,3,4]:ck(sub(sub((g,),old_to_new),new_to_old)==(g,),'core_old_generator_substitutions_freely_inverse')
ck(normal((4,3,-4,-2,-3,-2))==((),0),'positive_final_b_relation')
ck(normal((4,3,-4,2,-3,-2))!=((),0),'negative_final_b_variant_rejected')
# Spanning-tree collapse for Q retains two independent 2-cell relators.
collapsed=[red(x for x in f if abs(x) not in [1,2,4]) for f in qfaces]
ck(collapsed==[(-3,),(5,-6)],'Q_tree_collapse_kills_r_identifies_d_e')
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','guards':sum(checks.values()),'checks':dict(checks),'base_link_edges':[sorted(e) for e in sorted(baseedges,key=lambda e:sorted(e))],'Q_link_edges':{v:[sorted(e) for e in links[v]] for v in qverts},'product_square_words':verticalfaces,'Z_link':{'vertices':sorted(LV),'edges':[sorted(e) for e in sorted(LE,key=lambda e:sorted(e))],'triangles':[sorted(t) for t in sorted(LT,key=lambda e:sorted(e))],'four_cliques':cliques4},'scope':'Literal corner multiplicities, signed endpoint fullness, cube-corner triangles, exact free automorphism and mapping-torus controls. Reversible Tietze proof, global CAT(0), properness and auxiliary literature chain reviewed separately.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','guards':sum(checks.values())}))
