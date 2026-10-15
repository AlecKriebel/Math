from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parent.parent;R=Path(__file__).resolve().parent
corpus=[W/'source_alignment/private_reading',W/'priority_cross/private_reading',W/'nearest_primary_recovery/private_reading',W/'priority_broad/private_reading',W/'priority_source_adversary/private_reading']
found={}
for root in corpus:
 for p in root.rglob('*'):
  if p.is_file():
   b=p.read_bytes(); k=(len(b),hashlib.sha256(b).hexdigest());found.setdefault(k,[]).append(str(p.relative_to(W)))
records=json.loads((W/'preprint_package_v03/SOURCE_PROVENANCE.json').read_bytes())['source_records'];out=[]
for r in records:
 b=r.get('source_artifact_binding'); matches=None if b is None else found.get((b['bytes'],b['sha256']),[])
 out.append({'id':r.get('id',r.get('work',r.get('title'))),'family':r['audit_family'],'binding':b,'matched_local_files':matches})
result={'records':len(out),'records_with_binding':sum(x['binding'] is not None for x in out),'bound_records_locally_matched':sum(bool(x['matched_local_files']) for x in out),'records_without_local_match':[x for x in out if x['binding'] is not None and not x['matched_local_files']],'source_records':out,'scope':'Binding existence/byte check only. Independent primary semantic extents separately recorded. Unmatched archived metadata bindings are not treated as theorem bodies or as new body-access defects.'}
(R/'SOURCE_BINDING_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='source_records'},indent=2))
