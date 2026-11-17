"""Authenticate exact source/audit and record root semantic resolution only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[
 ('mink-riesz-k3-production-prepare-v2-sol-20261117','OWNED_MANIFEST.json','ddf44cba02ceefe26979d69abb39aa76674605b5fa629737d6b37cce2495afe7','bb1d3310715e55097986663b5500fd38a134c787e0e2ce507282a4c5b8f0dd02',12),
 ('mink-riesz-k3-production-static-v2-sol-20261117','MANIFEST.json','2229e5e8d338324468aba12847510149226162aad7ca36066db5a17bcc7aae9b','c532aa72c645b8913804e5ca013f6aa4e8a643b90340083b61d6efe93c3779d7',20)]
for n,mn,fh,mh,count in rows:
 b=P/'verification'/n
 assert sha((b/'FINAL.json').read_bytes())==fh
 assert sha((b/mn).read_bytes())==mh
 m=json.loads((b/mn).read_bytes());files={x.name:x for x in b.iterdir()}
 assert len(files)==count and all(x.is_file() and not x.is_symlink() for x in files.values())
 assert stat.S_IMODE(b.stat().st_mode)==0o755
 declared={r['path']:r for r in m['payload_files']}
 assert set(files)==set(declared)|{mn,'FINAL.json'}
 for name,f in files.items():
  assert stat.S_IMODE(f.stat().st_mode)==0o644
  if name in declared:
   r=declared[name];raw=f.read_bytes();assert len(raw)==r['bytes'] and sha(raw)==r['SHA256']
r={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ALL_STATIC_FINDINGS_RESOLVED_FOR_EXACT_ACTION',
 'helper_SHA256':'83c48bca3761c9fbd49d8b29c42a113e10eebfa58b9793bad84c25644b48b3f9',
 'PLAN_SHA256':'a039e52df5a04d5e8a6c4dec4709bebb1858f4757efd11c09c9e35c1a67aaf24',
 'audit_FINAL_SHA256':rows[1][2],'authenticated_files':32,'child_directories':0,
 'root_read_actual':['all1279savedhelperlines','wholePLAN/TARGETS/FINAL/SOURCEdiff','independentactualFINAL/REPORT/FINDINGS/CRITERIA/ADVERSARIAL_REVIEW'],
 'resolution':'Unconditional whole stdout retention precedes exit validation and all caller parsing; source differs only by root/PLAN-pin relocation otherwise.',
 'old_source_disposition':'Original06ce helper remains UNFIT and unexecuted; V2 does not retroactively pass it.',
 'mode_executions_at_adoption':0,'static_percent':100,'goal_active_incomplete':True,
 'future_action_requires_separate_exact_expiring_root_authority':True,'AA':None,'actual_UI':False}
with (P/'verification/root-mink-riesz-k3-v2-helper-adoption-20261117.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(json.dumps(r))
