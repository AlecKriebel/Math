"""Preserve executed own controls; author separate exact metadata/test refinements."""
from pathlib import Path
import hashlib,json,os
D=Path(__file__).resolve().parent
changes={
 'independent_controls.py':[
  ("('reversed_clock','finished_utc',before[:-6])","('reversed_clock','finished_utc',(now-dt.timedelta(seconds=3)).isoformat())"),
  ("PRIVATE_PATH_FIXTURES'","PRIVATE_PATH_FIXTURES_V2'"),
  ("PRIVATE_MODE_FIXTURES'","PRIVATE_MODE_FIXTURES_V2'"),
  ("INDEPENDENT_CONTROL_RESULT.json'","INDEPENDENT_CONTROL_RESULT_V2.json'")],
 'supplemental_controls.py':[
  ('used={}','attrs_by_source={}'),('used[name]=sorted(attrs)','attrs_by_source[name]=sorted(attrs)'),
  ("'AST_all_guard_exports_checked':used","'AST_all_guard_exports_checked':attrs_by_source"),
  ("PRIVATE_PUBLICATION_FIXTURES'","PRIVATE_PUBLICATION_FIXTURES_V2'"),
  ("SUPPLEMENTAL_CONTROL_RESULT.json'","SUPPLEMENTAL_CONTROL_RESULT_V2.json'")]
}
result={'actual_pid':os.getpid(),'own_executed_controls_preserved':True,'candidate_production_changed':False,'changes':[]}
for name,deltas in changes.items():
    old=(D/name).read_bytes();new=old
    for before,after in deltas:
        assert new.count(before.encode())==1
        new=new.replace(before.encode(),after.encode(),1)
    dest=D/name.replace('.py','_v2.py')
    with dest.open('xb') as stream:stream.write(new)
    result['changes'].append({'before':name,'after':dest.name,'old_sha256':hashlib.sha256(old).hexdigest(),'new_sha256':hashlib.sha256(new).hexdigest(),'exact_replacements':deltas})
(D/'OWN_CONTROL_REFINEMENT_RECORD.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
