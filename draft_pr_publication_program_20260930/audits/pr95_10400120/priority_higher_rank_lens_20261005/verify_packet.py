from pathlib import Path
import hashlib,json,datetime,os
D=Path.cwd(); checks=[]
def check(label,condition):
 checks.append({'check':label,'pass':bool(condition)})
 if not condition: raise RuntimeError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=sorted((D/'processes').glob('*.json'))+sorted((D/'independent_old_example_adversary/processes').glob('*.json'))
for p in records:
 j=json.loads(p.read_text())
 if 'argv' not in j or 'stdout_sha256' not in j:continue
 for name in ['stdout','stderr']:
  f=p.with_suffix('.'+name)
  check(str(f.relative_to(D))+' hash',f.exists() and sha(f)==j[name+'_sha256'])
  check(str(f.relative_to(D))+' bytes',f.stat().st_size==j[name+'_bytes'])
 for item in j.get('inputs',[]):
  f=Path(item['path'])
  if not (f.exists() and f.stat().st_size==item['bytes'] and sha(f)==item['sha256']):
   preserved=p.parent/(p.stem+'.source_bytes')/f.name
   check(str(p.relative_to(D))+' preserved historical input '+f.name,preserved.exists() and preserved.stat().st_size==item['bytes'] and sha(preserved)==item['sha256'])
  else:check(str(p.relative_to(D))+' input '+f.name,True)
 check(str(p.relative_to(D))+' actual PID/argv/UTC',bool(j.get('operator_PID')) and bool(j.get('child_PID')) and bool(j.get('argv')) and bool(j.get('UTC_started')) and bool(j.get('UTC_finished')))
 expected_exit=1 if p==D/'processes/verify_packet.json' else 0
 check(str(p.relative_to(D))+' recorded expected exit '+str(expected_exit),j.get('exit')==expected_exit)
check('HT authenticated hash',sha(D/'private_sources/hansen_takata_0209403v2.pdf')=='a00c189a481c1c7f5ccb14968e4d3b29abe7e560d3bb416f13ba56ae795e609e')
check('accepted gate unchanged',sha(D/'ACCEPTED_PARENT_MATHEMATICAL_GATE.json')==sha(D.parent/'ROOT_MATHEMATICAL_GATE_20261005.json'))
for row in json.loads((D/'INCOMING_SOURCE_MANIFEST.json').read_text()):
 check('incoming '+Path(row['copy']).name,sha(Path(row['copy']))==row['sha256'] and sha(Path(row['source']))==row['sha256'])
for source in json.loads((D/'SOURCE_LEDGER.json').read_text())['sources']:
 for row in source['files']:
  f=D/row['path'];check(source['id']+' '+row['path'],sha(f)==row['sha256'] and f.stat().st_size==row['bytes'])
for name,expected in [('AUDIT_REPORT.txt','1e0a21cf723fb326877d1bd71296ab78f47cdd161e5a766bc464d515e84710e9'),('AUDIT_ARTIFACT_MANIFEST.json','4e4d8658c4f5da8f2593554e6f2c567eba46e69a55965547ec000d68b98d5d90'),('SOURCE_MANIFEST.json','e706c5a1f2113cb98ae89885c32729edc63540637bb280d836c193734d7807be')]:
 check('adversary '+name,sha(D/'independent_old_example_adversary'/name)==expected)
for name in ['ht_old_example','modular_old_example_exact']:
 j=json.loads((D/'processes'/f'{name}.stdout').read_text())
 check(name+' exact result stdout JSON',bool(j))
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'checks':checks,'all_pass':True,'note':'Integrity validation only; no new proof search or recomputation.'}
(D/'INTEGRITY_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'UTC':result['UTC'],'actual_PID':os.getpid(),'all_pass':True,'check_count':len(checks),'INTEGRITY_CHECK_sha256':sha(D/'INTEGRITY_CHECK.json')},indent=2))
