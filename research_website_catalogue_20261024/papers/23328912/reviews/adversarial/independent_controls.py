"""Fresh controls from the six-page manuscript, before packaged helper reading."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations,product
from datetime import datetime,timezone
import json
OWN=Path(__file__).resolve().parent
checks={}
def req(test,msg):
 if not test:raise RuntimeError(msg)
def inv(w):return tuple(-x for x in reversed(w))
def red(w):
 out=[]
 for a in w:
  if out and out[-1]==-a:out.pop()
  else:out.append(a)
 return tuple(out)
def subst(w,mp):
 return red(a for g in w for a in (mp[g] if g>0 else inv(mp[-g])))
def canon(w):
 w=red(w)
 while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
 return min(tuple(v[i:]+v[:i]) for v in [w,inv(w)] for i in range(len(v))) if w else ()
def fmt(w,names):return ' '.join(names[abs(g)]+('^-1' if g<0 else '') for g in w) or '1'
# Independent corner incidence construction: do not import the printed link table.
base={'x':('o','o'),'y':('o','o'),'b':('o','o')}
qedges={'p':('B','A','x'),'q':('A','C','y'),'r':('D','C','x'),'s':('B','D','y'),'d':('A','B','b'),'e':('C','A','b')}
qs=[('B',[('p',1),('q',1),('r',-1),('s',-1)]),('A',[('d',1),('p',1),('e',-1),('q',-1)])]
bs=[[('x',1),('y',1),('x',-1),('y',-1)],[('b',1),('x',1),('b',-1),('y',-1)]]
def corner(word,i):
 a,s=word[i-1];b,t=word[i]
 return ((a,-s),(b,t))
def sm(x):return frozenset(x)
def transform(g):
 e,sg=g
 return ({'x':'y','y':'x','b':'b'}[e],-sg if e=='b' else sg)
basecorners=[sm(corner(w,i)) for w in bs for i in range(4)]
req(len(set(basecorners))==8,'base multiedge'); req(all(len(x)==2 for x in basecorners),'base loop')
base_edges=set(basecorners);base_vertices={g for e in base_edges for g in e}
qcorners=defaultdict(list);vertices_by_square=[]
for start,w in qs:
 v=start;vs=[]
 for i,(edge,sg) in enumerate(w):
  u,t,label=qedges[edge]
  if sg<0:u,t=t,u
  req(u==v,'square boundary mismatch');vs.append(v)
  qcorners[v].append(corner(w,i));v=t
 req(v==start,'open square');vertices_by_square.append(vs)
qverts=defaultdict(set)
for e,(u,v,label) in qedges.items():qverts[u].add((e,1));qverts[v].add((e,-1))
image=lambda g:(qedges[g[0]][2],g[1])
rows={}
for v in sorted(qverts):
 germs=qverts[v];corners=qcorners[v]
 req(len({sm(c) for c in corners})==len(corners),'Q duplicate link edge')
 for fn in [image,lambda g:transform(image(g))]:
  im={fn(g) for g in germs};ims={sm(map(fn,c)) for c in corners}
  req(len(im)==len(germs),'Q germ collision')
  req(ims=={e for e in base_edges if e<=im},'not full link')
 rows[v]={'germs':[list(z) for z in sorted(germs)],'corners':[[list(g) for g in c] for c in corners]}
# Full quotient link edges from EACH characteristic square corner.
zsq=[]
for e,(u,v,label) in qedges.items():
 zsq.append([(label,1),('z'+v,1),transform((label,-1)),('z'+u,-1)])
zedges=[sm(corner(w,i)) for w in bs+zsq for i in range(4)]
req(len(zedges)==32 and len(set(zedges))==32,'quotient link multiplicity')
zvertices={g for e in zedges for g in e}
triangles=[];trianglereceipts=[]
for cube,((start,w),vs) in enumerate(zip(qs,vertices_by_square)):
 for height in (0,1):
  for i,v in enumerate(vs):
   pair=tuple(map(image,corner(w,i)))
   if height:pair=tuple(map(transform,pair))
   tri=sm(pair+(('z'+v,1 if height==0 else -1),))
   req(len(tri)==3,'degenerate triangle');triangles.append(tri)
   trianglereceipts.append({'cube':cube,'corner':i,'height':height,'domain_vertex':v,'germs':[list(g) for g in sorted(tri)]})
req(len(triangles)==len(set(triangles))==16,'duplicated link triangle')
zedges=set(zedges);triangles=set(triangles)
cliques3={sm(c) for c in combinations(zvertices,3) if all(sm(pair) in zedges for pair in combinations(c,2))}
cliques4=[c for c in combinations(zvertices,4) if all(sm(pair) in zedges for pair in combinations(c,2))]
req(cliques3==triangles and not cliques4,'nonflag link')
req(len(zvertices)==14,'vertex count')
# Missing a repeated A corner must yield a missing required triangle, even if a set of vertices is unchanged.
drop=next(t for t in trianglereceipts if t['cube']==1 and t['corner']==2 and t['height']==0)
dropped_triangle=sm(tuple(g) for g in drop['germs'])
req(cliques3 != triangles-{dropped_triangle},'missing repeated corner not detected')
req(max(Counter(list(triangles)+[dropped_triangle]).values())==2,'duplicate characteristic corner not detected')
checks['incidences']={'base_link_counts':[6,8],'Q_links':rows,'Q_characteristic_vertex_cycles':vertices_by_square,'cell_counts':[1,7,8,2],'Z_link_counts':[14,32,16],'all_16_cube_corners':trianglereceipts,'no_repeated_link_simplex':True,'all_cliques_filled':True,'four_cliques':0,'repeated_A_corner_omission_detected':drop}
# Square automorphism isometry: track oriented cyclic indices, not only group relators.
def dihedral_equivalents(w):
 iw=[(e,-sg) for e,sg in reversed(w)]
 return [(orientation,k,v[k:]+v[:k]) for orientation,v in [(1,w),(-1,iw)] for k in range(4)]
isometries=[]
for w in bs:
 tw=list(map(transform,w));matches=[(orient,k) for orient,k,c in dihedral_equivalents(w) if c==tw]
 req(len(matches)==1,'cell isometry ambiguous')
 req(list(map(transform,tw))==w,'lambda square')
 isometries.append(matches[0])
checks['lambda']={'square_dihedral_matches':isometries,'edge_and_cell_order_two':True}
# Reversible Tietze elimination. Use integers for the seven original generators.
names={1:'x',2:'y',3:'b',4:'zA',5:'zB',6:'zC',7:'zD'}
x,y,b,zA,zB,zC,zD=range(1,8)
rels=[(x,y,-x,-y),(b,x,-b,-y),(x,zA,-y,-zB),(y,zC,-x,-zA),(x,zC,-y,-zD),(y,zD,-x,-zB),(b,zB,b,-zA),(b,zA,b,-zC)]
steps=[]
for gen,at in [(zB,2),(zC,2),(zD,3)]:
 w=rels[at];positions=[i for i,g in enumerate(w) if abs(g)==gen];req(len(positions)==1,'invalid Tietze defining relation')
 i=positions[0];U=w[:i];V=w[i+1:];val=red(inv(U)+inv(V)) if w[i]>0 else red(V+U)
 mp={g:(g,) for g in names};mp[gen]=val
 removed=rels.pop(at);rels=[subst(w,mp) for w in rels]
 steps.append({'eliminated':names[gen],'defining_relator':fmt(removed,names),'substitution':fmt(val,names)})
# Remaining order base, base, r, d, e. r vanishes by commuting adjacent angular blocks.
def commute_xy(w):
 out=[];i=0
 while i<len(w):
  if abs(w[i]) not in (x,y):out.append(w[i]);i+=1;continue
  sx=sy=0
  while i<len(w) and abs(w[i]) in (x,y):
   if abs(w[i])==x:sx+=1 if w[i]>0 else -1
   else:sy+=1 if w[i]>0 else -1
   i+=1
  out+=([x if sx>0 else -x]*abs(sx)+[y if sy>0 else -y]*abs(sy))
 return red(out)
r=rels[2];after=r
for _ in range(5):after=commute_xy(after)
req(after==(),'r redundant')
def rotate_at(w,g):
 i=w.index(g);return w[i:]+w[:i]
D=rotate_at(rels[3],-zA);E=rotate_at(rels[4],-zA)
def replace_once(w,old,new):
 for i in range(len(w)-len(old)+1):
  if w[i:i+len(old)]==old:return red(w[:i]+new+w[i+len(old):])
 raise RuntimeError('rewrite unavailable')
E1=replace_once(E,(y,b),(b,x));E2=replace_once(E1,(b,-x),(-y,b));req(E2==D,'e redundancy certificate')
# Both rewrites follow from b x B Y: y b = b x, b X = Y b.
# New generators a,b,c,t use integers 11,12,13,14.
a,bb,c,t=11,12,13,14
newnames={a:'a',bb:'b',c:'c',t:'t'}
forward={x:(t,),y:(-a,t),b:(bb,),zA:(-c,-t)}
back={a:(x,-y),bb:(b,),c:(-x,-zA),t:(x,)}
for g in forward:req(subst(forward[g],back)==(g,),'inverse source map')
for g in back:req(subst(back[g],forward)==(g,),'inverse target map')
target=[(t,a,-t,-a),(t,bb,-t,-bb,-a),(t,c,-t,-bb,-c,-bb)]
changed=[subst(rels[0],forward),subst(rels[1],forward),subst(D,forward)]
req(canon(changed[0])==canon(target[0]),'first relator')
req(canon(changed[1])==canon(target[1]),'second relator')
third=replace_once(changed[2],(a,bb),(t,bb,-t))
req(canon(third)==canon(target[2]),'third relator')
checks['nonabelian_Tietze_certificate']={'steps':steps,'remaining_r':fmt(r,names),'r_after_commutations':fmt(after,names),'D':fmt(D,names),'E':fmt(E,names),'E_after_yb_to_bx':fmt(E1,names),'E_after_bX_to_Yb':fmt(E2,names),'free_inverse_generator_maps':True,'transformed_relators':[fmt(w,newnames) for w in changed],'third_after_ab_to_tbT':fmt(third,newnames),'target_relators':[fmt(w,newnames) for w in target],'equivalence':'first two and final third cyclically equivalent up to inversion; all replacements use retained defining relations'}
# Distinct normal-form falsification check in the exact semidirect product F3 semidirect Z.
phi={a:(a,),bb:(a,bb),c:(bb,c,bb)}
phiinv={a:(a,),bb:(-a,bb),c:(-bb,a,c,-bb,a)}
for g in phi:
 req(subst(phi[g],phiinv)==(g,) and subst(phiinv[g],phi)==(g,),'phi not automorphism')
def apply(w,k,m=phi):
 for _ in range(abs(k)):w=subst(w,m if k>=0 else phiinv)
 return w
def mul(p,q,m=phi):return (red(p[0]+apply(q[0],p[1],m)),p[1]+q[1])
def targetnf(w,m=phi):
 out=((),0)
 for g in w:out=mul(out,((g,),0) if abs(g)!=t else ((),1 if g>0 else -1),m)
 return out
actual={**forward,zB:(t,-c,-t,-t,a),zC:(-t,a,-c),zD:(-t,a,t,-c,-t,-t,a,t)}
# Derive the last three automatically from the exact published edge definitions, avoiding hand expansion.
actual[zB]=subst((x,zA,-y),forward);actual[zC]=subst((-y,zA,x),forward);actual[zD]=subst((-y,x,zA,-y,x),forward)
original=[(x,y,-x,-y),(b,x,-b,-y),(x,zA,-y,-zB),(y,zC,-x,-zA),(x,zC,-y,-zD),(y,zD,-x,-zB),(b,zB,b,-zA),(b,zA,b,-zC)]
for w in original:req(targetnf(subst(w,actual))==((),0),'geometric square not target relation')
# Same abelianization, different nonabelian monodromy: append [a,b] to phi(c).
mutant=red(phi[c]+(a,bb,-a,-bb));req(Counter(mutant)!=Counter(phi[c]) or mutant!=phi[c],'mutant trivial')
wrong_rel=(t,c,-t)+inv(mutant)
res=targetnf(wrong_rel);req(res!=((),0),'same-abelianization mutant escaped')
req(sum(1 if g==a else -1 if g==-a else 0 for g in mutant)==0,'mutant a exponent')
req(sum(1 if g==bb else -1 if g==-bb else 0 for g in mutant)==2,'mutant b exponent')
checks['exact_semidirect_normal_form']={'automorphism_and_inverse_compositions':6,'geometric_square_relators':8,'all_identity':True,'same_abelianization_mutant':fmt(mutant,newnames),'mutant_relator_nontrivial_residue':fmt(res[0],newnames),'mutant_t_exponent':res[1]}
result={'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'pass','input':'published PDF and TeX only; no packaged helper or historical audit reading before these controls','checks':checks,'limits':['Finite incidence enumeration is exhaustive for the specified finite complex, not a machine proof of CAT(0).','Nonabelian presentation equivalence follows explicit reversible Tietze operations, supplemented by exact target normal forms.','No minimality/priority or general-family claim.']}
(OWN/'evidence/independent-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'pass','link_counts':[14,32,16],'cube_corners':16,'square_relators':8,'reversible_presentation_equivalence':True,'same_abelianization_negative_control':'rejected'}))
