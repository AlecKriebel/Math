from nerve_operations import *
import json
checks=0;cats={};rows=[]
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
C=cycle(5);IC,labels=inflate(C,{i:2 for i in range(5)});RP,_=surface_models();BRP,_=barycentric(RP);IRP,rlabels=inflate(BRP,{0:2})
for name,K,J,ls in [('doubled_pentagon',C,IC,labels),('one_fiber_projective',BRP,IRP,rlabels)]:
 vs,_=graph(K);fib={v:{i for i,x in enumerate(ls) if x[0]==v} for v in vs};seen=set()
 for sigma in [()]+sorted(J,key=lambda f:(len(f),f)):
  A=tuple(sorted(v for v in vs if fib[v]<=set(sigma)));ck(not A or A in K,'deleted_full_fibers_form_simplex');seen.add(A)
  JP=puncture(J,sigma);KP=puncture(K,A);projection={tuple(sorted(set(ls[v][0] for v in f))) for f in JP};ck(projection==KP,'puncture_projection_exact')
  reps={v:min(fib[v]-set(sigma)) for v in vs-set(A)}
  for f in KP:ck(tuple(sorted(reps[v] for v in f)) in JP,'simplicial_section')
  for f in JP:
   join=tuple(sorted(set(f)|{reps[ls[v][0]] for v in f}));ck(join in JP,'contiguity_union_face')
 ck(seen=={()}|K,'all_old_punctures_realized');ck(cliques(J)==J,'inflation_flag');ck((square(J) is None)==(square(K) is None),'inflation_square_equivalence')
 rows.append({'model':name,'vertices_before':len(vs),'vertices_after':len(ls),'new_punctures':1+len(J)})
for p in [0,2,3]:ck(profile(IC,p)==profile(C,p)==2,'inflated_cohomological_profile')
CC,apex=cone(C)
for p in [0,2,3]:ck(profile(CC,p)==profile(C,p),'cone_profile')
ck(square(CC) is None,'cone_no_square')
# Two cycles intersect exactly in one vertex, or in one edge.
C6v=closure([(0,5),(5,6),(6,7),(7,8),(8,9),(9,0)])
C6e=closure([(0,1),(1,5),(5,6),(6,7),(7,8),(8,0)])
for B in [C6v,C6e]:
 J=C|B;ck(cliques(J)==J,'clique_sum_flag');ck(square(J) is None,'clique_sum_no_square')
 for p in [0,2,3]:ck(profile(J,p)==max(1,profile(C,p),profile(B,p))==2,'clique_sum_profile')
# Join of pentagons: explicit cross-factor induced square.
B=cycle(5,5);J=closure([a+b for a in C for b in B]);ck(square(J) is not None,'join_square_obstruction')
for q1 in range(1,10):
 for d1 in range(q1,15):
  for q2 in range(1,10):
   for d2 in range(q2,15):
    if 3*q1>=2*d1 and 3*q2>=2*d2:
     ck(3*(q1+q2)>=2*(d1+d2),'product_ratio_inequality')
     ck(3*max(1,q1,q2)>=2*max(1,d1,d2),'clique_sum_ratio_inequality')
print(json.dumps({'assertions':checks,'categories':cats,'models':rows,'scope':'Exact puncture projection, simplicial section and contiguity controls; no singular hyperbolic counterexample produced.'},sort_keys=True,indent=2))
