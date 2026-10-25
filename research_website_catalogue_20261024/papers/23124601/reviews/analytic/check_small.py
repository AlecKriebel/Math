"""Independent analytic small certificates, from manuscript definitions only."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import json,math,datetime
E=Path(__file__).resolve().parent

def need(v,s):
 if not v:raise RuntimeError(s)
def reduce(w):
 out=[]
 for x in w:
  if out and out[-1]==-x:out.pop()
  else:out.append(x)
 return tuple(out)
def inv(w):return tuple(-x for x in w[::-1])
def sub(w,A):
 out=[]
 for x in w:
  t=A[x-1] if x>0 else inv(A[-x-1])
  for y in t:
   if out and out[-1]==-y:out.pop()
   else:out.append(y)
 return tuple(out)
I=((1,),(2,),(3,),(4,))
A=[((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),((1,),(2,),(3,),(3,-2,1,4))]
AI=[((1,),(-1,2),(-1,3),(-1,4)),((2,),(2,-1,2),(3,),(4,)),((1,),(3,),(3,-2,3),(4,)),((1,),(2,),(4,),(4,-3,4)),((1,),(2,),(3,),(-1,2,-3,4))]
def compose(B,C):return tuple(sub(w,C) for w in B)
def act(word,table=A):
 out=I
 for i in word:out=compose(out,table[i-1])
 return out
relations=[]
for i in range(5):
 need(compose(A[i],AI[i])==I and compose(AI[i],A[i])==I,'two_sided_inverse');relations.append('inverse_both:'+str(i+1))
for i in range(1,5):need(act([i,i+1,i])==act([i+1,i,i+1]),'adjacent_braid');relations.append('braid:'+str(i))
for i,j in combinations(range(1,6),2):
 if j-i>1:need(act([i,j])==act([j,i]),'distant_commute');relations.append('commute:'+str((i,j)))
c=[1,2,3,4]*5;h=[5,4,3,2,1,1,2,3,4,5];z=[1,2,3,4,5]*6
need(act(c)==act(h),'relator_descends_to_quotient');need(act(c+c)==act(z)==act(h+h),'F4_model_products');relations.append('c_equals_h')
# A malformed table must be caught by the exact inverse/relator checks.
bad=list(A);bad[4]=bad[4][:3]+(bad[4][3]+(1,),);need(compose(bad[4],AI[4])!=I,'table_mutation_rejected')
# Rigorous integer boxes, derived by summing inequalities excluding/including one label.
pairs=list(combinations(range(6),2));patterns=[]
for m in [0,10,20,30,40]:
 T=m//10-4;beta={(i,j):2 if j<5 else 0 for i,j in pairs};bounds={e:(beta[e]+T)//2 for e in pairs};ranges=[]
 for i in range(6):
  D=sum(v for e,v in bounds.items() if i in e);C=sum(v for e,v in bounds.items() if i not in e)
  lo=T-(C//4);hi=(D-T)//4;ranges.append(range(lo,hi+1))
 solutions=[]
 for t in product(*ranges):
  if sum(t)!=T or any(t[i]+t[j]>bounds[i,j] for i,j in pairs):continue
  vec=[beta[i,j]+T-2*(t[i]+t[j]) for i,j in pairs];need(all(x>=0 for x in vec),'nonnegative_linking');solutions.append({'t':t,'linking':vec})
 expected=0 if m<20 else 6 if m in [20,40] else 1;need(len(solutions)==expected,'integer_solution_count');patterns.append({'length':m,'T':T,'rigorous_coordinate_bounds':[[r.start,r.stop-1] for r in ranges],'solutions':solutions})
# Full unpruned20-step walks with exact labelled-crossing and F4 image records.
target=act(c+c);records=[];starts=[];survivors=[]
for start in range(6):
 here=[]
 def walk(pos,counts,word):
  if len(word)==20:
   if pos!=start:return
   need(all(v==4 for v in counts),'edge_caps_saturate');order=list(range(6));cross=Counter()
   for a in word:
    i=a-1;cross[tuple(sorted((order[i],order[i+1])))]+=1;order[i],order[i+1]=order[i+1],order[i]
   need(order==list(range(6)) and all(cross[e]==(4 if start in e else 0) for e in pairs),'literal_star_purity_and_counts');images=act(word);passing=images==target;row={'start':start+1,'word':word,'images':images,'matches_target':passing};records.append(row);here.append(row)
   if passing:survivors.append(tuple(word))
   return
  for nxt in [pos-1,pos+1]:
   if 0<=nxt<6:
    edge=min(pos,nxt)
    if counts[edge]<4:
     cc=list(counts);cc[edge]+=1;walk(nxt,cc,word+[edge+1])
 walk(start,[0]*5,[]);starts.append({'start':start+1,'all_candidates':len(here),'passing':sum(x['matches_target'] for x in here)})
rotations={tuple((h+h)[k:]+(h+h)[:k]) for k in range(20)};need(len(records)==810 and len(rotations)==10 and set(survivors)==rotations and len(survivors)==10,'exact_complete_survivor_set')
# LiteralS6 subgroup images for the two length40 generator universes.
def mult(p,i):q=list(p);q[i],q[i+1]=q[i+1],q[i];return tuple(q)
def subgroup(gs):
 seen={tuple(range(6))};queue=list(seen)
 for p in queue:
  for i in gs:
   q=mult(p,i)
   if q not in seen:seen.add(q);queue.append(q)
 return seen
H=subgroup(range(4));K=subgroup(range(1,5));need(len(H)==len(K)==120 and H!=K and all(x[5]==5 for x in H) and all(x[0]==0 for x in K),'distinct_generated_S5_subgroups')
(E/'cache/walk20-full-independent.json').write_text(json.dumps(records,separators=(',',':'))+'\n')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','source_program_or_record_import':False,'all_relations_literal_reduced_words':relations,'malformed_A5_table_inverse_control_rejected':True,'integer_linking_patterns':patterns,'walk20_starts':starts,'complete_candidates':len(records),'literal_survivors':[list(x) for x in sorted(survivors)],'F4_target_images':target,'permutation_subgroups':{'sizes':[len(H),len(K)],'distinct':True,'fixed_labels':[6,1]},'faithfulness_of_F4_assumed':False,'full810images_retained_in_ignored_cache':True};(E/'SMALL_CERTIFICATES.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','relations':len(relations),'candidates':len(records),'starts':starts,'integer_solution_counts':[(x['length'],len(x['solutions'])) for x in patterns],'survivors':len(survivors),'record_bytes':(E/'cache/walk20-full-independent.json').stat().st_size},indent=2))
