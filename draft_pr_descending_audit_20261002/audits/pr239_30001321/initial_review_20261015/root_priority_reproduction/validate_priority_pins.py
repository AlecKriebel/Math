from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess,shutil
D=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr239_30001321/initial_review_20261015')
families=[('priority_historical_01','AUTHORED_MANIFEST.json'),('priority_local_limit_01','PUBLIC_AUTHORED_MANIFEST.json'),('priority_recent_01','AUTHORED_MANIFEST.json'),('priority_bridge_01','PUBLIC_AUTHORED_MANIFEST.json')]
public=[];manifests=[];private=[]
def pin(path,e,kind):
 b=path.read_bytes();expected_bytes=e.get('bytes',e.get('size'));assert (expected_bytes is None or len(b)==expected_bytes) and hashlib.sha256(b).hexdigest()==e['sha256'],str(path)
 return {'path':str(path.relative_to(D)),'bytes':len(b),'sha256':e['sha256'],'type':kind}
for family,name in families:
 B=D/family;m=B/name;j=json.loads(m.read_text());count=0
 for e in j['files']:
  p=B/e['path'];assert p.resolve().is_relative_to(B.resolve()) and 'private_reading' not in p.parts
  public.append(pin(p,e,'public_authored'));count+=1
 manifests.append({'family':family,'path':str(m.relative_to(D)),'sha256':hashlib.sha256(m.read_bytes()).hexdigest(),'public_pins_verified':count})
B=D/'priority_historical_01'
for e in json.loads((B/'SOURCE_CATALOG.json').read_text())['objects']:
 if 'sha256' in e and 'local_path' in e:private.append(pin(B/'private_reading'/e['local_path'],e,'historical_primary'))
B=D/'priority_historical_01/adversary'
for e in json.loads((B/'source_manifest.json').read_text())['sources']:
 if 'sha256' in e:private.append(pin(B/e['private_path'],e,'historical_adversary_primary'))
B=D/'priority_local_limit_01'
for e in json.loads((B/'PRIMARY_RETRIEVAL.json').read_text()):
 if 'sha256' in e:private.append(pin(B/e['file'],e,'local_limit_primary'))
B=D/'priority_recent_01'
for e in json.loads((B/'SOURCE_INVENTORY.json').read_text())['private_inventory']:
 private.append(pin(B/e['path'],e,'recent_evidence'))
B=D/'priority_bridge_01'
for e in json.loads((B/'SOURCE_RETRIEVAL.json').read_text())['sources']:
 if e.get('status')=='retrieved':private.append(pin(B/'private_reading'/(e['name']+'.pdf'),e,'bridge_primary'))
W=D/'root_priority_reproduction/bridge';W.mkdir(exist_ok=False)
shutil.copy2(B/'finite_controls.py',W/'finite_controls.py')
r=subprocess.run(['python3','-I','-B','finite_controls.py'],cwd=W,capture_output=True,timeout=60)
(W/'stdout.json').write_bytes(r.stdout);(W/'stderr.txt').write_bytes(r.stderr);assert r.returncode==0 and not r.stderr
out=json.loads(r.stdout);expected=json.loads((B/'FINITE_CONTROLS.json').read_text());out.pop('utc');expected.pop('utc');assert out==expected
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','family_manifests':manifests,'public_authored_pins':public,'private_evidence_pins_verified':private,'counts':{'public_authored_pins':len(public),'private_evidence_pins':len(private)},'bridge_controls_actual_root_replay':True,'bridge_replay_ignored_keys':['utc'],'all_other_output_fields_identical':True,'other_actual_root_replays':'root_priority_reproduction/ROOT_REPLAYS.json','priority_verdict':'not assigned by integrity check; synthesis and archival source work pending','whole_third_party_objects_publishable':False}
(D/'ROOT_PRIORITY_PIN_VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
shutil.copy2('/tmp/pr239_priority_pins_20261015.py',D/'root_priority_reproduction/validate_priority_pins.py')
print(json.dumps({'status':'PASS','counts':receipt['counts'],'manifests':manifests,'bridge_replay':'all fields identical except actual UTC'},indent=2))
