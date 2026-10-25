from pathlib import Path
import json,gzip,hashlib
E=Path(__file__).absolute().parent;P=E.parents[3];S=P/'papers/23124601/sources/published-source/verification'
ours=[json.loads(x) for x in (E/'own-20-full-records.jsonl').read_text().splitlines()]
original=[json.loads(x) for x in gzip.decompress((S/'certificates/20_full_actions.jsonl.gz').read_bytes()).splitlines()]
a={(r['start'],tuple(r['word'])):(r['full_four_images'],r['matches_target']) for r in ours};b={(r['center'],tuple(r['word'])):(r['images'],r['survives']) for r in original};assert a==b and len(a)==810
# Own free-group implementation, independently check the full-twist decomposition and shift.
def inverse(w):return tuple(-v for v in reversed(w))
def substitute(w,tab):
 out=[]
 for x in w:
  for y in (tab[x-1] if x>0 else inverse(tab[-x-1])):
   if out and out[-1]==-y:out.pop()
   else:out.append(y)
 return tuple(out)
T=[];Ti=[]
for i in range(1,6):
 t=[(j,) for j in range(1,7)];t[i-1]=(i,i+1,-i);t[i]=(i,);T.append(t)
 t=[(j,) for j in range(1,7)];t[i-1]=(i+1,);t[i]=(-(i+1),i,i+1);Ti.append(t)
def act(w):
 out=tuple((j,) for j in range(1,7))
 for x in w:out=tuple(substitute(v,T[x-1] if x>0 else Ti[-x-1]) for v in out)
 return out
c=(1,2,3,4)*5;h=(5,4,3,2,1,1,2,3,4,5);z=(1,2,3,4,5)*6;d=(1,2,3,4,5)
assert act(c+h)==act(h+c)==act(z)
assert all(act(d+(i,)+inverse(d))==act((i+1,)) for i in range(1,5))
assert all(act(z+(i,))==act((i,)+z) for i in range(1,6))
r={'own810_full_actions_equal_actual_original810_records_not_hash_only':True,'faithful_F6_full_twist_decomposition_ch_hc_z':True,'all4_shift_conjugation_identities':True,'z_commutes_with_all5_generators':True,'interpretation':'Exact signed-word equalities; B6 equality uses the authenticated classical faithful Artin theorem, not a claimed faithful F4 quotient action.'}
(E/'additional-own-results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
