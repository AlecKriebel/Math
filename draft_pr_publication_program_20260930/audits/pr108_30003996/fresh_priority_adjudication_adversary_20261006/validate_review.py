import json,hashlib,os
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
W=Path(__file__).resolve().parent
checks=[]
def check(label,ok):checks.append({'check':label,'pass':bool(ok)})
def match(p,n,h,prefix=False):
 b=Path(p).read_bytes();b=b[:n] if prefix else b
 return len(b)==n and hashlib.sha256(b).hexdigest()==h
v=json.loads((W/'VERDICT.json').read_text())
check('candidate immutable',match(**{'p':v['candidate_proof']['path'],'n':v['candidate_proof']['bytes'],'h':v['candidate_proof']['sha256']}))
check('criteria frozen immutable',hashlib.sha256((W/'CRITERIA_FROZEN.md').read_bytes()).hexdigest()=='8714cd68a1e383963d4cad32477eef40f23fc48b295c0db2f235b82e0c051f8c')
for p in W.glob('*.json'):
 json.loads(p.read_text());check('JSON parses '+p.name,True)
fm=json.loads((W/'FAMILY_MANIFEST_VERIFICATION.json').read_text())
for n,c in enumerate(fm['checks']):check('family prior pin '+str(n),match(c['path'],c['expected_bytes'],c['expected_sha256'],c['status']=='PASS_PREFIX'))
for n in ['FAMILY_INPUT_BINDINGS_V1.json','FAMILY_INPUT_BINDINGS_CORRECTED_V2.json']:
 d=json.loads((W/n).read_text());ps=d['files'] if 'files' in d else [p for f in d['families'] for p in f['public_root_file_pins']]
 for p in ps:check('input snapshot '+p['path'],match(p['path'],p['bytes'],p['sha256']))
d=json.loads((W/'CORRECTED_V2_VERIFICATION.json').read_text())
for c in d['ordinary_byte_sha_checks']+d['V1_snapshot_rechecks']:
 p=c['expected'];check('corrected packet pin '+p['path'],match(p['path'],p['bytes'],p['sha256']))
for r in json.loads((W/'WEB_RECEIPTS.json').read_text()):check('own exact web raw '+r['call_id'],match(W/r['raw_private_file'],r['raw_bytes'],r['raw_sha256']))
for line in (W/'EXECUTION_RECEIPTS.jsonl').read_text().splitlines():
 r=json.loads(line)
 for stream in ['stdout','stderr']:
  stream_file=r.get(stream+'_file','private/'+r['label']+'_reproduction.'+stream)
  check('execution stream '+r['label']+' '+stream,match(W/stream_file,r[stream+'_bytes'],r[stream+'_sha256']))
 source_path=r.get('source_path',r.get('source_script_path'))
 if source_path:
  source_bytes=r.get('source_bytes',r.get('source_script_bytes'));source_sha=r.get('source_sha256',r.get('source_script_sha256'))
  for h in json.loads((W/'EXECUTION_SOURCE_HISTORY.json').read_text())['historical_sources']:
   if source_sha==h['sha256']:source_path=str(W/h['archived_copy'])
  check('execution source '+r['label'],match(source_path,source_bytes,source_sha))
 if r.get('executed_copy_sha256'):check('executed diagnostic copy '+r['label'],match(r['argv'][-1],r['executed_copy_bytes'],r['executed_copy_sha256']))
check('all three diagnostics exit0',len(json.loads((W/'DIAGNOSTIC_REPRODUCTIONS.json').read_text()))==3 and all(x['exit_code']==0 for x in json.loads((W/'DIAGNOSTIC_REPRODUCTIONS.json').read_text())))
check('F01 closed',json.loads((W/'CORRECTION_DISPOSITION.json').read_text())['status']=='CLOSED')
check('18 matrix rows',len(json.loads((W/'NOVELTY_DISPOSITION_MATRIX.json').read_text())['rows'])==18)
check('no unseen package certified',v['publication_package_certified'] is False and v['publication_authorized_by_this_audit'] is False)
failed=[x for x in checks if not x['pass']]
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'operator_pid':os.getpid(),'checks':len(checks),'failed':failed,'status':'PASS' if not failed else 'FAIL','meaning':'Integrity and evidence custody recheck, not an absolute priority or publication certificate.'},indent=2))
raise SystemExit(bool(failed))
