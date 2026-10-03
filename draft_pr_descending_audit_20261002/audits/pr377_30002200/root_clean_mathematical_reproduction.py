#!/usr/bin/env python3
"""Root reproduction of the fresh credited-result mathematical gate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,shutil,subprocess
A=Path(__file__).resolve().parent
D=A/'clean_corrected_final_adversary'
PY=A.parents[0]/'pr378_30004322/sources_effective_review/private_runtime/bin/python'
W=A/'tmp/root_clean_math'
assert not W.exists();W.mkdir(parents=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def check_entries(root,entries,key='path'):
 for e in entries:
  b=(root/e[key]).read_bytes()
  assert sha(b)==e['sha256'] and len(b)==e.get('bytes',len(b)),e[key]
 return len(entries)
public=json.loads((D/'public_evidence_manifest.json').read_text())
public_count=check_entries(D,public['files']);assert public_count==54
seals=[]
for f in ['independent_pre_candidate_seal.json','mathematical_verdict_seal.json']:
 m=json.loads((D/f).read_text());seals.append({'manifest':f,'sha256':sha((D/f).read_bytes()),'entries':check_entries(D,m['files'])})
private=json.loads((D/'private_source_evidence_manifest.json').read_text())
private_count=check_entries(D,private['files'],'private_path');assert private_count==42
prep=json.loads((A/'scope_repair_preparation_receipt.json').read_text())
packet=Path(prep['private_packet']);check_entries(packet,prep['files'])
CURRENT=W/'current';shutil.copytree(packet,CURRENT)
OLD=W/'original';shutil.copytree(A/'snapshot/unsolved_math_prioritization/attempts/30002200',OLD)
records=[]
jobs=[('new_mechanism',D/'independent_mechanism_checks.py',D/'independent.stdout',D),
      ('new_falsification',D/'correction_falsification.py',D/'correction_falsification.stdout',D)]
for script,stream in [('verify_source_cases.py','verify_source_cases.stdout'),
                       ('review/independent_check.py','review_independent_check.stdout'),
                       ('verify_corrected_source_cases.py','verify_corrected_source_cases.stdout'),
                       ('review/independent_check_corrected.py','review_independent_check_corrected.stdout'),
                       ('verify_publication.py','verify_publication.stdout')]:
 jobs.append((script.replace('/','_').removesuffix('.py'),CURRENT/script,D/stream,CURRENT))
jobs.append(('old_publication',OLD/'verify_publication.py',D/'original_verify_publication.stdout',OLD))
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for label,script,expected,cwd in jobs:
 p=subprocess.run([str(PY),'-B',str(script)],cwd=cwd,env=env,capture_output=True)
 (A/f'root_clean_{label}.stdout').write_bytes(p.stdout);(A/f'root_clean_{label}.stderr').write_bytes(p.stderr)
 assert p.returncode==0 and not p.stderr,(label,p.stderr.decode())
 assert p.stdout==expected.read_bytes(),label
 records.append({'label':label,'script_sha256':sha(script.read_bytes()),'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'full_stream_byte_exact':True})
 print(label+': PASS',flush=True)
mutants=[]
for i,f in enumerate(['CURRENT_SCOPE_CORRECTION.md','review/independent_check_corrected.py',
                       'CREDITED_PROOF_GUIDE.md','review/CORRECTED_INDEPENDENT_CHECKS.json']):
 root=W/f'mutation_{i}';shutil.copytree(packet,root)
 with (root/f).open('ab') as out:out.write(b'\nROOT DELIBERATE BINDING MUTATION\n')
 p=subprocess.run([str(PY),'-B',str(root/'verify_publication.py')],cwd=root,env=env,capture_output=True)
 (A/f'root_clean_mutation_{i}.stdout').write_bytes(p.stdout);(A/f'root_clean_mutation_{i}.stderr').write_bytes(p.stderr)
 assert p.returncode==1 and not p.stdout and b'AssertionError' in p.stderr
 mutants.append({'path':f,'exit_code':p.returncode,'stderr_sha256':sha(p.stderr),'rejected':True})
check_entries(CURRENT,prep['files'])
# Initial families were already root-reexecuted independently. Compare the
# fresh investigator's complete streams to those root/family results explicitly.
family=[]
for own,other in [('family_geometry_morse_review_independent_local_controls.stdout','geometry_morse_review/independent_local_controls.stdout.txt'),
                  ('family_koszul_depth_review_independent_koszul_controls.stdout','koszul_depth_review/independent_koszul_controls.stdout.txt'),
                  ('family_koszul_depth_review_frozen_comparison_controls.stdout','koszul_depth_review/frozen_comparison_controls.stdout.txt'),
                  ('family_priority_sources_review_independent_source_controls.stdout','priority_sources_review/source_controls_full.stdout')]:
 a,b=(D/own).read_bytes(),(A/other).read_bytes()
 if 'priority' in own:
  aa=[json.loads(v) for v in a.splitlines()];bb=[json.loads(v) for v in b.splitlines()]
  for rows in [aa,bb]:rows[0].pop('started_utc');rows[-1].pop('completed_utc')
  assert aa==bb;comparison='Every JSON field equal except only two explicit UTC values'
 else:assert a==b;comparison='Full bytes equal'
 family.append({'stream':own,'bytes':len(a),'comparison':comparison})
backup=json.loads((D/'source_priority_supplement.json').read_text())
for e in backup['all11_author_bytes_match']:
 b=subprocess.check_output(['git','show',backup['author_backup']+':unsolved_math_prioritization/attempts/30002200/'+e['path']])
 assert sha(b)==e['sha256']
check_entries(D,public['files'])
receipt={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'workflow_percent':90,
         'original_status':'already_solved','original_turns':'0/5','novel_original_discovery':False,
         'public_bindings':public_count,'private_source_bindings':private_count,'seals':seals,
         'corrected_packet_paths':25,'preserved_historical_files':16,'runs':records,
         'four_mutations_rejected':mutants,'family_full_stream_checks':family,
         'author_backup11_objects_verified':True,'current_corrected_inputs_unchanged':True,
         'historical_pinned_search_reproduced':False,'own_review_erratum_authoritative':True,
         'source_grade_version_difference':'2b-2; zero at exported b1',
         'remaining_gate':'Actual corrected Git/head/queue after378 acceptance and final public manifest',
         'paper':False,'doi':False}
(A/'root_clean_mathematical_reproduction_receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','public_bindings':public_count,'private_source_bindings':private_count,'streams':len(records),'mutations':len(mutants),'sealed_entries':sum(s['entries'] for s in seals)},sort_keys=True))
