from pathlib import Path
import itertools,json
p=Path('/workspace/shared/math-30004033-final');d=json.loads((p/'turn4/prism_certificates.json').read_text());E=[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3),(1,4),(2,5)];es=set(E);count=0
perms=[x for x in itertools.permutations(range(6)) if {tuple(sorted((x[a],x[b]))) for a,b in E}==es];assert len(perms)==12
covered=set()
for c in d['certificates']:
 m=c['mask'];colors=[set(t) for t in c['triples']]
 assert all(len(t)==3 and t<=set(range(1,9)) for t in colors);count+=1
 for x in perms:
  m2=sum(1<<E.index(tuple(sorted((x[a],x[b])))) for i,(a,b) in enumerate(E) if m>>i&1)
  cs=[None]*6
  for i in range(6):cs[x[i]]=colors[i]
  for i,(a,b) in enumerate(E):
   q=len(cs[a]&cs[b]);assert (q==0 if m2>>i&1 else q in (1,2));count+=1
  covered.add(m2)
valid=set()
for m in range(512):
 H={E[i] for i in range(9) if m>>i&1}
 if not any(all(tuple(sorted(e)) in H for e in itertools.combinations(T,2)) for T in itertools.combinations(range(6),3)):valid.add(m)
assert covered==valid and len(valid)==392;count+=1
# Independent disjointness graph walks, endpoint intersection classifications.
triples=[frozenset(t) for t in itertools.combinations(range(8),3)];a=triples[0];reach={a}
for L in range(1,16):
 reach={c for b in reach for c in triples if not b&c}
 for c in triples:
  q=len(a&c);expected=(q==0 if L==1 else q>=1 if L==2 else q<=2 if L==3 else True)
  assert (c in reach)==expected;count+=1
# Every five-palette prescribed I/D pair and valid child type has a middle two-set.
two=[set(x) for x in itertools.combinations(range(5),2)]
for A in two:
 for C in two:
  q=len(A&C)
  if q not in (0,1):continue
  for left,right in itertools.product((0,1),repeat=2):
   if q==0 and left==right==0:continue
   assert any(len(A&B)==left and len(B&C)==right for B in two);count+=1
print(json.dumps({'status':'PASS','assertions':count,'prism_masks':len(covered),'automorphisms':len(perms)},sort_keys=True))
