"""Independent tuple-based audit of all finite-search positive certificates.
Checks coverage for exhaustive domains and makes no coverage claim for samples.
"""
from pathlib import Path
from itertools import combinations
from math import prod
import json,hashlib,datetime
from root_certificate_audit import require,decode
P=Path(__file__).resolve().parents[1]
def audit():
 reports=[];unique=set();total=0
 for folder in ['exhaustive_order15','exhaustive_sizes7','larger_samples']:
  for path in sorted((P/'finite_search'/folder).glob('*.jsonl')):
   seen=set();count=0
   with path.open() as stream:
    h=json.loads(next(stream));mods=tuple(h['moduli']);q=prod(mods)
    require(q==h['order'] and q%2==1,'group header')
    for line in stream:
     row=json.loads(line);mask=row['mask'];c=row['cycle'];n=len(c)
     require(type(mask)is int and 0<=mask<2**q and mask&1,'bad mask')
     require(mask not in seen,'duplicate subset in file');seen.add(mask)
     want={x for x in range(q) if mask>>x&1}
     require(n==len(want)>2 and set(c)==want and len(set(c))==n,'bad permutation')
     require(c[0]==0 and all(type(v)is int for v in c),'bad cycle coordinates')
     cc=[decode(v,mods) for v in c]
     ss={tuple((a+b)%m for a,b,m in zip(cc[i],cc[(i+1)%n],mods)) for i in range(n)}
     require(len(ss)==n,'repeated sum')
     unique.add((mods,mask));count+=1
   if folder=='exhaustive_order15':
    expected={m for m in range(1,2**q,2) if m.bit_count()>2}
    require(seen==expected,'order15 coverage')
   elif folder=='exhaustive_sizes7':
    require(mods in [(3,3,3),(5,5)] and h['sizes']==[3,4,5,6,7],'size domain')
    expected={1+sum(1<<x for x in cc) for n in range(3,8) for cc in combinations(range(1,q),n-1)}
    require(seen==expected,'size7 coverage')
   else:
    require(h.get('domain')=='listed_samples','sample domain')
    if 'covered_subsets' in h:require(count==h['covered_subsets'],'header covered count')
   reports.append({'file':str(path.relative_to(P)),'rows':count,'moduli':mods,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'coverage':folder})
   total+=count
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'total_positive_witness_rows':total,'distinct_group_subset_pairs':len(unique),'files':reports,'meaning':'Each stored cycle verified independently. Exhaustive coverage only for the exact two stated domains; larger samples do not certify general existence.'}
 require(total==530233 and len(unique)==530155,'unexpected final totals')
 return result
if __name__=='__main__':
 r=audit();Path(__file__).with_name('root_large_certificate_audit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='files'}))
