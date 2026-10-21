"""Exact source-derived permutation controls; this is not a GAP execution."""
import json, pathlib
def orbits(p):
 todo=set(p); result=[]
 while todo:
  x=min(todo); cyc=[]; y=x
  while y not in cyc: cyc.append(y); todo.remove(y); y=p[y]
  result.append(cyc)
 return result
def facts(rho,iota,marks):
 f={x:rho[iota[x]] for x in rho}; inv={rho[x]:x for x in rho}
 faces=orbits(f)
 return {'rho_orbits':orbits(rho),'faces':faces,'marked_counts':[sum(inv[x] in marks for x in F) for F in faces],'genus':(2-len(orbits(rho))+len(rho)//2-len(faces))//2}
def build(n,paths,repair):
 rho={x:x for x in range(1,2*n+1)}; iota={x:x+1 if x%2 else x-1 for x in rho}; marks=[]; used=set(); collisions=[]
 for P in paths:
  slots=[]
  if repair:
   for v in P:
    x=2*v-1 if 2*v-1 not in used else 2*v
    assert x not in used; used.add(x); slots.append(x)
   # Right-action source transpositions produce this cyclic occurrence order.
   for a,b in zip(slots,slots[1:]+slots[:1]):rho[a]=b
   marks.append(slots[-1])
  else:
   start=2*P[0]-1 if rho[2*P[0]-1]==2*P[0]-1 else 2*P[0]
   for v in P[1:]:
    target=2*v-1 if rho[2*v-1]==2*v-1 else 2*v
    if start==target:collisions.append({'start':start,'target':target,'path':P})
    # Right-action rho*(start,target), allowing equal-point cycle as identity only for diagnosis.
    for x in rho:
     if rho[x]==start:rho[x]=target
     elif rho[x]==target:rho[x]=start
   inverse={rho[x]:x for x in rho};marks.append(inverse[start])
 for x in rho:
  if rho[x]==x:marks.append(x)
 return {'repair':repair,'marks':marks,'collisions':collisions,**facts(rho,iota,marks)}
results=[]
for name,n,paths in [('field',1,[]),('one_arrow',2,[[1,2]]),('two_arrow_chain',3,[[1,2,3]]),('square_zero_loop',1,[[1,1]]),('full_relation_triangle',3,[[1,2],[2,3],[3,1]])]:
 for fix in [False,True]:results.append({'name':name,**build(n,paths,fix)})
sq=[r for r in results if r['name']=='square_zero_loop'];assert len(sq[0]['faces'])==1 and len(sq[1]['faces'])==2
assert sq[0]['collisions'] and not sq[1]['collisions']
assert sq[0]['marked_counts']==[2] and sorted(sq[1]['marked_counts'])==[0,1]
assert all(r['genus']==0 for r in results)
for name in ['field','one_arrow','two_arrow_chain','full_relation_triangle']:
 a,b=[r for r in results if r['name']==name]
 assert all(a[k]==b[k] for k in ['rho_orbits','faces','marks','marked_counts','genus'])
root=pathlib.Path(__file__).resolve().parent
(root/'QPA_OCCURRENCE_RESULTS.json').write_text(json.dumps({'scope':'source-derived exact permutation translation, no GAP runtime','results':results},indent=2)+'\n')
print(json.dumps(results))
