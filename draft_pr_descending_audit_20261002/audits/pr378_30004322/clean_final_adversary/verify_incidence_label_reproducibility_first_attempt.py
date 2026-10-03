"""Read full existing records; reconcile only the three unordered vertex labels.

Never edits or reruns the original sealed control code or incidence records.
"""
from pathlib import Path
from itertools import permutations
import json,hashlib,datetime
D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
results=[]
for q in (1,2,4):
    original_path=D/'streams'/f'new_q{q}_all_line_incidence.json'
    root_path=D.parent/f'root_clean_q{q}_all_line_incidence.json'
    ob=original_path.read_bytes();rb=root_path.read_bytes()
    o=json.loads(ob);r=json.loads(rb)
    assert o['n']==r['n']==5*q and o['point_kinds']==r['point_kinds']
    start=13*q*q
    assert o['point_kinds'][start:]==['vertex']*3
    assert all(k!='vertex' for k in o['point_kinds'][:start])
    def index_records(records):
        result={}
        for e in records:
            I=tuple(e['support']);pair=e['representative_pair']
            assert I==tuple(sorted(set(I))) and len(I)>=2
            assert len(pair)==2 and pair[0]!=pair[1] and set(pair).issubset(I)
            assert I not in result
            result[I]=(e['class'],e['dual_load'])
        return result
    oi=index_records(o['records']);ri=index_records(r['records'])
    valid=[]
    for perm in permutations(range(start,start+3)):
        def relabel(i):return i if i<start else perm[i-start]
        transformed={tuple(sorted(relabel(i) for i in I)):value for I,value in oi.items()}
        if transformed==ri:valid.append(list(perm))
    assert len(valid)==1,(q,valid)
    assert len(oi)=={1:51,2:921,4:17775}[q]
    results.append({'q':q,'records':len(oi),'original_bytes':len(ob),'root_bytes':len(rb),
      'original_sha256':sha(ob),'root_sha256':sha(rb),'raw_byte_equal':ob==rb,
      'valid_vertex_permutations':valid,'all_support_class_dual_load_records_match_after_relabeling':True,
      'every_original_and_root_representative_pair_checked_distinct_and_in_support':True})
receipt=(D.parent/'root_clean_mathematical_reproduction_receipt.json').read_bytes()
root=json.loads(receipt)
for x,y in zip(results,root['full_incidence_reconciliation']):
    assert x['q']==y['q'] and x['original_sha256']==y['original_sha256'] and x['root_sha256']==y['root_sha256']
    assert x['valid_vertex_permutations']==y['valid_vertex_permutations']
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
 'qualification':'Summary stdout is byte reproducible; full incidence JSON is geometrically/combinatorially reproducible up to the unique permutation of the three coordinate vertices introduced by unordered set iteration. Representative pairs are valid line witnesses, not guaranteed byte-identical choices across labelings. No old code/data rewritten.',
 'root_receipt_sha256':sha(receipt),'full_record_checks':results},sort_keys=True,indent=2))
