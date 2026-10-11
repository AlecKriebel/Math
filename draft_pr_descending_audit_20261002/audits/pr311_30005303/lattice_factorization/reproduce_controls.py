#!/usr/bin/env python3
"""Capture complete checker streams and exact input/output/argv bindings.

No reviewer material is opened. All writes remain in this family's folder.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,datetime,stat,shutil

B=Path(__file__).resolve().parent
A=B.parent/'snapshot'/'unsolved_math_prioritization'/'attempts'/'30005303'
R=B/'reproduction'; R.mkdir(exist_ok=True)
I=R/'independent'; I.mkdir(exist_ok=True)
sha=lambda data:hashlib.sha256(data).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
packet=json.loads((A/'FINAL_PACKET_MANIFEST.json').read_text())
author_names=['FINAL_PACKET_MANIFEST.json']+[item['path'] for item in packet['files']]
assert len(author_names)==19
assert all(not name.startswith('review/') for name in author_names)
read_names=author_names+['PUBLICATION_MANIFEST.json','PUBLICATION_SUMMARY.md']
inputs=[]
for name in read_names:
 p=A/name; data=p.read_bytes()
 inputs.append({'path':str(p),'relative_path':name,'bytes':len(data),'sha256':sha(data),'mode':f'{stat.S_IMODE(p.stat().st_mode):04o}',
  'role':'released author packet' if name in author_names else 'released publication binding only' if name=='PUBLICATION_MANIFEST.json' else 'extra read disclosed; inherited summary claims excluded from evidence'})
for item in packet['files']:
 p=A/item['path']; data=p.read_bytes()
 assert len(data)==item['bytes'] and sha(data)==item['sha256']
publication=json.loads((A/'PUBLICATION_MANIFEST.json').read_text())
lookup={item['path']:item for item in publication['files']}
for name in author_names:
 data=(A/name).read_bytes(); expected=lookup[name]
 assert len(data)==expected['bytes'] and sha(data)==expected['sha256']
(B/'AUTHOR_INPUT_BINDINGS.json').write_text(json.dumps({'utc':utc(),'files':inputs,'author_packet_count':19,
 'publication_entries_checked':'author packet only; no review files opened'},indent=2)+'\n')
(B/'AUTHOR_INPUT_BINDINGS.json').chmod(0o444)

runs=[]
def run(label,path,expected=None):
 argv=[sys.executable,str(path)]
 started=utc()
 p=subprocess.run(argv,cwd=str(B),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
 ended=utc(); stdout=R/(label+'.stdout.json'); stderr=R/(label+'.stderr.txt')
 stdout.write_bytes(p.stdout); stderr.write_bytes(p.stderr)
 record={'label':label,'argv':argv,'cwd':str(B),'utc_started':started,'utc_finished':ended,
 'exit_code':p.returncode,'python_version':sys.version,'code_sha256':sha(path.read_bytes()),
 'stdout_path':str(stdout),'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),
 'stderr_path':str(stderr),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr)}
 assert p.returncode==0,record
 if expected is not None:
  data=expected.read_bytes();record['expected_output_path']=str(expected)
  record['expected_output_sha256']=sha(data);record['stdout_matches_expected_bytes']=p.stdout==data
  assert p.stdout==data,record
 else:
  result=path.with_name('source_control_result.json' if label=='independent_source' else 'prose_controls_result.json')
  original=B/result.name
  record['result_path']=str(result);record['result_sha256']=sha(result.read_bytes())
  record['result_matches_frozen_bytes']=result.read_bytes()==original.read_bytes()
  assert record['result_matches_frozen_bytes'],record
 runs.append(record)
 print(json.dumps(record,indent=2))

# Exact copies only: original independent scripts/results remain frozen.
for label,name in [('independent_source','source_control_exact.py'),('independent_prose','prose_controls_exact.py')]:
 copied=I/name; data=(B/name).read_bytes(); copied.write_bytes(data)
 assert sha(copied.read_bytes())==sha(data)
 run(label,copied)
for label,script,receipt in [
 ('author_c4','checks/verify_turn1.py','checks/turn1_c4_output.json'),
 ('author_c6','checks/verify_c6.py','checks/turn1_c6_output.json'),
 ('author_turn2','checks/verify_turn2.py','checks/turn2_output.json')]:
 run(label,A/script,A/receipt)

for item in inputs:
 data=Path(item['path']).read_bytes()
 assert len(data)==item['bytes'] and sha(data)==item['sha256']
 assert f'{stat.S_IMODE(Path(item["path"]).stat().st_mode):04o}'==item['mode']
summary={'utc':utc(),'all_runs_passed':True,'author_inputs_bytes_and_modes_unchanged':True,
 'author_assertions':sum(json.loads((R/(label+'.stdout.json')).read_text())['assertions'] for label in ('author_c4','author_c6','author_turn2')),
 'runs':runs,'no_review_file_read':True}
(R/'RUN_RECEIPTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='runs'},indent=2))
