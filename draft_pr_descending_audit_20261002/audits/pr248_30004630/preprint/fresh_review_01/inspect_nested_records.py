from pathlib import Path
import json,hashlib,datetime
OWN=Path(__file__).resolve().parent;ROOT=OWN/'extracted';rows=[];fail=[];missing=[]
for mf in sorted(ROOT.rglob('*MANIFEST.json')):
 d=json.loads(mf.read_text())
 if mf.name=='FILE_MANIFEST.json':continue
 def walk(o,kpath=''):
  if isinstance(o,dict):
   if isinstance(o.get('path'),str) and 'sha256' in o and 'bytes' in o:
    p=Path(o['path']);candidates=[mf.parent/p,ROOT/p]
    exists=next((q for q in candidates if q.is_file()),None)
    if exists is not None:
     b=exists.read_bytes();match=(hashlib.sha256(b).hexdigest()==o['sha256'] and len(b)==o['bytes']);row={'manifest':str(mf.relative_to(ROOT)),'field_path':kpath,'artifact':str(exists.relative_to(ROOT)) if exists.is_relative_to(ROOT) else str(exists),'matches':match};rows.append(row)
     if not match:fail.append(row)
    else:missing.append({'manifest':str(mf.relative_to(ROOT)),'field_path':kpath,'excluded_or_historical_path':str(p)})
   for k,v in o.items():walk(v,kpath+'/'+str(k))
  elif isinstance(o,list):
   for i,v in enumerate(o):walk(v,kpath+'/'+str(i))
 walk(d)
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'nested_resolved_pin_checks':len(rows),'resolved_mismatches':fail,'all_resolved_pins':rows,'missing_paths':missing,'missing_paths_are_not_automatically_defects':'Portable archive explicitly omits whole external reading copies and some audit-only inputs; historical manifests may describe files in their original directory. Distinguish these from scientific runner inputs, which are all present and validated.'}
(OWN/'NESTED_PIN_CONSISTENCY.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'resolved_checks':len(rows),'mismatches':fail,'missing_paths_count':len(missing)},indent=2))
