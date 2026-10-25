#!/usr/bin/env python3
"""Fresh exact checks; no imports from supplied or historical verifiers.
The analytic all-actions argument remains separately checked in REVIEW.md.
"""
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import json,hashlib,datetime,time
start=time.monotonic();counts=Counter();results={}
def check(x,k):
 counts[k]+=1
 if not x:raise AssertionError(k)
def mul(x,y,p=29):
 return tuple(sum(x[2*i+k]*y[2*k+j] for k in range(2))%p for i in range(2) for j in range(2))
def act(x,v,p=29):return ((x[0]*v[0]+x[1]*v[1])%p,(x[2]*v[0]+x[3]*v[1])%p)
def inv(x,p=29):return (x[3],-x[1]%p,-x[2]%p,x[0])
I=(1,0,0,1);A=(0,28,1,0);B=(2,7,12,28);Z=(28,0,0,28)
def close(gens,e,op):
 # Layered frontier, rather than supplied positive-word queue.
 S={e};front={e}
 while front:
  nxt={op(g,x) for x in front for g in gens}-S
  S.update(nxt);front=nxt
 return frozenset(S)
H=sorted(close([A,B],I,mul));ix={h:i for i,h in enumerate(H)};eid=ix[I];zi=ix[Z]
check(len(H)==120,'complement_order')
T=[[ix[mul(a,b)] for b in H] for a in H]
check(all((a*d-b*c)%29==1 for a,b,c,d in H),'determinant_one')
check([h for h in H if h!=I and mul(h,h)==I]==[Z],'unique_involution')
for h in H:
 if h!=I:check(((h[0]-1)*(h[3]-1)-h[1]*h[2])%29!=0,'fixed_point_free_nonidentity')
def hc(gs):return close(gs,eid,lambda a,b:T[a][b])
# All two-generator candidates, then verify closure under adjoining ANY element.
# That completeness check is independent of the candidate-generation heuristic.
subs={hc([])}|{hc([a]) for a in range(120)}|{hc([a,b]) for a,b in combinations(range(120),2)}
check(len(subs)==76,'two_generator_candidate_count')
for S in subs:
 for x in range(120):
  if x not in S:check(hc(list(S)+[x]) in subs,'complete_adjoining_closure')
subs=sorted(subs,key=lambda h:(len(h),sorted(h)))
odd=[s for s in subs if len(s)%2]
for s in odd:check(len(s) in (1,3,5),'odd_subgroups_prime_or_trivial')
for s in subs:
 if len(s)%2==0:check(zi in s,'even_subgroups_contain_center')
# Check every matrix conjugation for normal subgroups, with no generator shortcut.
normals=[]
for s in subs:
 n=all(ix[mul(mul(g,H[h]),inv(g))] in s for g in H for h in s)
 if n:normals.append(len(s))
check(sorted(normals)==[1,2,120],'normal_subgroups_of_complement')
R=[A,(12,24,0,17),(25,3,4,4)]
check(R[1]==mul(mul(B,A),mul(B,B)),'printed_R2_word')
check(R[2]==mul(mul(A,R[1]),mul(mul(A,B),mul(A,B))),'printed_R3_word')
orders=[]
for i,j in [(1,2),(0,2),(0,1)]:
 h=mul(R[i],R[j]);orders.append(len(close([h],I,mul)))
check(orders==[4,3,10],'printed_pair_product_orders')
oms=[hc([ix[R[j]] for j in range(3) if i!=j]) for i in range(3)]
check(list(map(len,oms))==[8,12,20],'pair_subgroup_orders')
check(set.intersection(*map(set,oms))=={eid,zi},'complement_normal_bottom')
check(hc([ix[r] for r in R])==frozenset(range(120)),'triple_generation')
# All possible images of the restriction lemma: scalar line groups C29:C2,C4.
scalar_results=[]
for m,lam in [(1,1),(2,28),(4,12)]:
 elts=list(product(range(29),range(m)));ii={g:i for i,g in enumerate(elts)}
 st=[[ii[((a+pow(lam,i,29)*b)%29,(i+j)%m)] for b,j in elts] for a,i in elts]
 ident=ii[(0,0)];sclose=lambda gs:close(gs,ident,lambda x,y:st[x][y])
 ss={sclose([])}|{sclose([x]) for x in range(len(elts))}|{sclose([x,y]) for x,y in combinations(range(len(elts)),2)}
 for s in list(ss):
  for x in range(len(elts)):
   if x not in s:check(sclose(list(s)+[x]) in ss,'scalar_complete_adjoining_closure')
 proper=[s for s in ss if len(s)<len(elts)];bad=0
 for a,b,c in combinations(proper,3):
  meet=a&b&c
  bad+=int((a&b)!=meet and (a&c)!=meet and (b&c)!=meet)
 check(bad==0,'scalar_no_irredundant_triple')
 scalar_results.append({'order':29*m,'subgroups':len(ss),'proper_triples_tested':len(proper)*(len(proper)-1)*(len(proper)-2)//6,'irredundant_triples':bad})
# Enumerate every subgroup whose translation intersection is a line, including
# all affine lifts, not only zero-translation split examples.
def am(x,y,p=29):
 v,h=x;w,k=y;hw=act(h,w,p)
 return (((v[0]+hw[0])%p,(v[1]+hw[1])%p),mul(h,k,p))
e=((0,0),I)
line_counts=Counter();line_group_hash=hashlib.sha256();seen_line=set()
lines=[(1,a) for a in range(29)]+[(0,1)]
for w in lines:
 st=[h for h in H if (act(h,w)[0]*w[1]-act(h,w)[1]*w[0])%29==0]
 check(len(st)==4,'all_line_stabilizers_order_four')
 h=next(h for h in st if mul(h,h)==Z);outside=(0,1) if w[0] else (1,0)
 W=frozenset((((j*w[0])%29,(j*w[1])%29),I) for j in range(29))
 for d,hh in [(1,I),(2,Z),(4,h)]:
  for t in (range(1) if d==1 else range(29)):
   v=((t*outside[0])%29,(t*outside[1])%29)
   K=close([(w,I),(v,hh)],e,am)
   check(len(K)==29*d,'all_affine_lift_orders')
   check(frozenset(x for x in K if x[1]==I)==W,'all_affine_lift_translation_intersections')
   check(K not in seen_line,'all_affine_lifts_distinct');seen_line.add(K)
   line_counts[29*d]+=1
   line_group_hash.update(json.dumps(sorted(K),separators=(',',':')).encode())
check(len(seen_line)==1770,'complete_line_intersection_family_count')
# Deform the explicit base witness through all 841 involution offsets.
def line_dihedral(w,v,p=29):
 z=(p-1,0,0,p-1)
 return frozenset([(((j*w[0])%p,(j*w[1])%p),I) for j in range(p)]+[(((v[0]+j*w[0])%p,(v[1]+j*w[1])%p),z) for j in range(p)])
l1=line_dihedral((1,0),(0,0));l2=line_dihedral((0,1),(0,0));good=bad=0
for v in product(range(29),repeat=2):
 l3=line_dihedral((1,1),v);total=l1&l2&l3
 check(len(l1&l3)==len(l2&l3)==2,'deformed_base_pair_meets')
 if len(total)==1:good+=1
 else:bad+=1
 check((len(total)==2)==(v[0]==v[1]),'deformed_base_exact_degeneracy')
check((good,bad)==(812,29),'deformed_base_counts')
l3=line_dihedral((1,1),(2,0))
check(l1&l2=={e,((0,0),Z)},'printed_base_meet_12')
check(l1&l3=={e,((2,0),Z)},'printed_base_meet_13')
check(l2&l3=={e,((0,27),Z)},'printed_base_meet_23')
check(l1&l2&l3=={e},'printed_faithful_base')
check(am(am(((1,0),I),((0,0),Z)),((28,0),I))==((2,0),Z),'printed_nonnormality')
# Printed characteristic-11 C, not the supplied checker's first-found C.
A11=(0,10,1,0);B11=(0,2,5,1);C=(6,10,0,2);Z11=(10,0,0,10)
H11=close([A11,B11],I,lambda x,y:mul(x,y,11))
check(len(H11)==120 and C in H11,'printed_characteristic11_complement')
check(len(close([C],I,lambda x,y:mul(x,y,11)))==10,'printed_characteristic11_C_order')
c2=mul(C,C,11);c5=I
for _ in range(5):c5=mul(c5,C,11)
f11=[close([((1,0),I),((0,0),C)],e,lambda x,y:am(x,y,11)),close([((1,4),I),((0,0),C)],e,lambda x,y:am(x,y,11)),close([((1,0),I),((0,1),I),((0,0),c5)],e,lambda x,y:am(x,y,11)),close([((1,0),I),((0,1),I),((0,0),c2)],e,lambda x,y:am(x,y,11))]
check([len(k) for k in f11]==[110,110,242,605],'printed_characteristic11_family_sizes')
check(set.intersection(*map(set,f11))=={e},'printed_characteristic11_faithfulness')
del11=[len(set.intersection(*(set(f11[j]) for j in range(4) if j!=i))) for i in range(4)]
check(del11==[11,11,5,2],'printed_characteristic11_minimality')
# Compare fresh small-group sets only after their construction and completeness proof.
cert=json.loads((Path(__file__).parent/'replay/python/finite_certificate.json').read_text())
old={frozenset(tuple(cert['matrices'][j]) for j in k['elements']) for k in cert['subgroups']}
ours={frozenset(H[j] for j in k) for k in subs}
check(old==ours,'fresh_subgroup_sets_match_replay')
results={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions':sum(counts.values()),'families':dict(counts),'complement_subgroup_order_histogram':dict(Counter(map(len,subs))),'scalar_models':scalar_results,'all_line_intersection_subgroups':{'count':len(seen_line),'orders':dict(line_counts),'canonical_digest':line_group_hash.hexdigest()},'base_offset_deformation':{'valid':good,'degenerate':bad},'printed_characteristic11_deletion_orders':del11,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':round(time.monotonic()-start,3),'limits':'Exact finite controls; all-actions bound checked separately by structural proof. No use of historical reviewer code or opinions as evidence; no novelty or human-review certification.'}
p=Path(__file__).with_name('independent_controls_result.json');p.write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
