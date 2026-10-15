#!/usr/bin/env python3
"""Independent finite audit derived from CANDIDATE coordinates, before old-code exposure.
No numerical map realization, no universal theorem/prose checker is claimed.
"""
import itertools,json,hashlib,datetime
from fractions import Fraction as Q
from pathlib import Path
OUT=Path(__file__).resolve().parent
EDGES=[(0,1),(1,2),(2,3),(3,0),(0,4),(1,5),(5,6),(2,7),(3,8),(8,9)]
COORDS=[(Q(1),Q(0)),(Q(0),Q(1)),(Q(-1),Q(0)),(Q(0),Q(-1)),(Q(1,2),Q(0)),(Q(0),Q(1,2)),(Q(0),Q(1,3)),(Q(-2),Q(0)),(Q(0),Q(-2)),(Q(0),Q(-3))]
BASE_ROT={0:[3,1,4],1:[0,2,5],2:[1,7,3],3:[2,8,0],4:[0],5:[1,6],6:[5],7:[2],8:[3,9],9:[8]}
def canonical_cycle(row):
 return min(tuple(row[i:]+row[:i]) for i in range(len(row)))
def faces(rot):
 unseen={(a,b) for a,b in EDGES}|{(b,a) for a,b in EDGES}; fs=[]
 while unseen:
  start=min(unseen); d=start; row=[]
  while d not in row:
   row.append(d); unseen.remove(d)
   a,b=d; nbrs=rot[b]; d=(b,nbrs[(nbrs.index(a)+1)%len(nbrs)])
  assert d==start
  fs.append(row)
 return fs
def enumeration(rot):
 adj={i:set() for i in range(10)}
 for a,b in EDGES: adj[a].add(b);adj[b].add(a)
 blocks=[tuple(i for i in range(10) if len(adj[i])==d) for d in (1,2,3)]
 autom=[]; tried=0
 edge_set={frozenset(e) for e in EDGES}
 for items in itertools.product(*(list(itertools.permutations(block)) for block in blocks)):
  perm=dict(zip(sum((list(b) for b in blocks),[]),sum((list(b) for b in items),[])))
  tried+=1
  if {frozenset((perm[a],perm[b])) for a,b in EDGES}!=edge_set: continue
  signs=[]
  for v in range(4):
   image=[perm[n] for n in rot[v]]; dest=rot[perm[v]]
   plus=canonical_cycle(image)==canonical_cycle(dest)
   minus=canonical_cycle(image)==canonical_cycle(list(reversed(dest)))
   assert plus!=minus
   signs.append(1 if plus else -1)
  fixedv=[v for v in range(10) if perm[v]==v]
  fixede=[i for i,(a,b) in enumerate(EDGES) if frozenset((perm[a],perm[b]))==frozenset((a,b))]
  fs=faces(rot); inv={tuple(sorted(f)):i for i,f in enumerate(fs)}
  face_image=None
  if len(set(signs))==1:
   face_image=[]
   for f in fs:
    mapped=[(perm[a],perm[b]) if signs[0]==1 else (perm[b],perm[a]) for a,b in f]
    face_image.append(inv[tuple(sorted(mapped))])
  autom.append({'permutation':[perm[i] for i in range(10)],'cycle':[perm[i] for i in range(4)],'local_signs':signs,'uniform_sign':signs[0] if len(set(signs))==1 else None,'fixed_vertices':fixedv,'fixed_edges':fixede,'face_action':face_image})
 return {'degree_compatible_permutations':tried,'abstract_automorphisms':autom,'preserving_count':sum(a['uniform_sign']==1 for a in autom),'reversing_count':sum(a['uniform_sign']==-1 for a in autom),'faces':faces(rot),'euler':10-10+len(faces(rot))}
def quarter_j(z):
 x,y=z;s=x*x+y*y
 return (-x/s,-y/s)
def sphere(z):
 x,y=z;s=x*x+y*y
 return (2*x/(s+1),2*y/(s+1),(s-1)/(s+1))
def derive_tangent_rotation():
 # Directions pointing away from each cycle vertex: previous/next tangent plus pendant.
 # Compare exact sign orientation of cyclic triples using their cross-products; data stored.
 pendants={0:4,1:5,2:7,3:8}; actual={}; tangent_rows={}
 def sort_ccw(row):
  from functools import cmp_to_key
  def half(z):x,y=z;return 0 if y>0 or y==0 and x>=0 else 1
  def cmp(a,b):
   u,v=a[1],b[1]
   if half(u)!=half(v):return -1 if half(u)<half(v) else 1
   cross=u[0]*v[1]-u[1]*v[0]
   return -1 if cross>0 else 1 if cross<0 else 0
  return [a[0] for a in sorted(row,key=cmp_to_key(cmp))]
 for j in range(4):
  x,y=COORDS[j]; px,py=COORDS[pendants[j]]
  row=[((j-1)%4,(y,-x)),((j+1)%4,(-y,x)),(pendants[j],(px-x,py-y))]
  tangent_rows[j]=[(v,[str(k) for k in vec]) for v,vec in row]
  actual[j]=sort_ccw(row)
  assert canonical_cycle(actual[j])==canonical_cycle(BASE_ROT[j])
 return {'exact_tangent_directions':tangent_rows,'counterclockwise_neighbor_orders':actual}
def radial_incidence(rot):
 fs=faces(rot);corner_edges=[]
 # One radial dart for each directed charge dart, ending at its left face.
 for k,f in enumerate(fs):
  for a,b in f:corner_edges.append((a,k,a,b))
 counts={v:sum(a==v for a,_,_,_ in corner_edges) for v in range(10)}
 assert counts=={v:len(rot[v]) for v in range(10)}
 return {'critical_vertices':10,'repelling_vertices':len(fs),'fixed_vertices':10+len(fs),'fixed_internal_ray_edges':len(corner_edges),'tischler_face_count':len(EDGES),'rays_per_critical_vertex':counts,'charge_face_boundary_lengths':[len(f) for f in fs],'note':'Formal radial incidence model; analytic existence/naturality require imported proof.'}
def main():
 original=enumeration(BASE_ROT)
 assert original['degree_compatible_permutations']==1152
 assert len(original['abstract_automorphisms'])==4
 assert (original['preserving_count'],original['reversing_count'])==(1,1)
 reverse=next(a for a in original['abstract_automorphisms'] if a['uniform_sign']==-1)
 assert reverse['cycle']==[2,3,0,1] and not reverse['fixed_vertices'] and not reverse['fixed_edges']
 assert reverse['face_action']==[1,0]
 j_image=[COORDS.index(quarter_j(z)) for z in COORDS]
 assert j_image==reverse['permutation']
 assert all(tuple(-a for a in sphere(z))==sphere(quarter_j(z)) for z in COORDS)
 tangent=derive_tangent_rotation()
 controls=[]
 for bits in itertools.product((0,1),repeat=4):
  rot={v:list(row) for v,row in BASE_ROT.items()}
  for j in range(4):
   prv,nxt=(j-1)%4,(j+1)%4;pnd=[v for v in rot[j] if v not in (prv,nxt)][0]
   rot[j]=[prv,pnd,nxt] if bits[j] else [prv,nxt,pnd]
  ans=enumeration(rot)
  controls.append({'inside_outside_bits':list(bits),'preserving_count':ans['preserving_count'],'reversing_count':ans['reversing_count'],'euler':ans['euler'],'face_lengths':[len(f) for f in ans['faces']]})
 all_inside=next(r for r in controls if r['inside_outside_bits']==[0,0,0,0])
 single_flip=next(r for r in controls if r['inside_outside_bits']==[0,0,1,0])
 assert (all_inside['preserving_count'],all_inside['reversing_count'])==(2,2)
 assert (single_flip['preserving_count'],single_flip['reversing_count'])==(1,1)
 single_rot={v:list(row) for v,row in BASE_ROT.items()};single_rot[3]=[2,0,8]
 single_reverse=next(a for a in enumeration(single_rot)['abstract_automorphisms'] if a['uniform_sign']==-1)
 assert single_reverse['fixed_vertices'] and single_reverse['fixed_edges']
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'claim':'Original graph finite geometry and symmetry audit; not standalone map realization proof.','edges':EDGES,'coordinates_rational':[[str(x),str(y)] for x,y in COORDS],'rotation':BASE_ROT,'original':original,'exact_geometric_rotation_derivation':tangent,'J_vertex_permutation':j_image,'J_is_antipodal_in_stereographic_sphere_exact':True,'radial_model':radial_incidence(BASE_ROT),'degree_and_PCF':{'degree':11,'critical_local_degrees':sorted(len(row)+1 for row in BASE_ROT.values()),'ramification_sum':sum(len(row) for row in BASE_ROT.values()),'postcritical_cardinality':10,'all_vertices_critical_fixed_by_realization':True,'totally_ramified_critical_count':0},'all_16_same_abstract_graph_embedding_controls':controls,'controls':{'all_inside_reflection_available':all_inside,'one_vertex_rotation_flip_has_reflection_not_antipode':{'embedding':single_flip,'reversing_action':single_reverse}}}
 (OUT/'independent_graph_results.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'permutations':1152,'automorphisms':4,'preserving':1,'reversing':1,'J_free_vertex_edge_action':True,'face_action':reverse['face_action'],'exact_geometry_pass':True,'16_embedding_controls_executed':True,'degree':11,'ramification':20},indent=2))
if __name__=='__main__':main()
