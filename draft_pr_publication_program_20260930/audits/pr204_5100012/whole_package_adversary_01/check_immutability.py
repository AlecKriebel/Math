import json,hashlib,os
from pathlib import Path
from datetime import datetime,timezone
O=Path(__file__).resolve().parent
doc=json.loads((O/'IMMUTABLE_INPUTS_BEFORE.json').read_text())
B=Path(doc['base'])
after=[];differences=[]
for old in doc['files']:
 p=Path(old['path']) if old['path'].startswith('/') else B/old['path']
 if p.is_symlink(): row={'path':old['path'],'symlink':os.readlink(p)}
 elif p.is_file(): row={'path':old['path'],'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 else: row={'path':old['path'],'missing':True}
 after.append(row)
 if row!=old:differences.append({'before':old,'after':row})
known={r['path'] for r in doc['files'] if not r['path'].startswith('/')}
actual=set()
for root,dirs,files in os.walk(B):
 dirs[:]=[d for d in dirs if Path(root,d)!=O]
 for name in files: actual.add(str(Path(root,name).relative_to(B)))
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if not differences else 'FAIL','expected_immutable_records':len(after),'content_differences':differences,'new_nonreview_paths_since_freeze':sorted(actual-known),'missing_nonreview_paths':sorted(known-actual),'before_manifest_sha256':hashlib.sha256((O/'IMMUTABLE_INPUTS_BEFORE.json').read_bytes()).hexdigest(),'all_frozen_input_bytes_identical':not differences,'note':'New Root operational files, if any, are reported separately from changes to frozen review inputs.'}
(O/'IMMUTABLE_INPUTS_AFTER.json').write_text(json.dumps({'files':after,'verification':report},indent=2)+'\n')
print(json.dumps(report,indent=2))
if differences:raise SystemExit(1)

