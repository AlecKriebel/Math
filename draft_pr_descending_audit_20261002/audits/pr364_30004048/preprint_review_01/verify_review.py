#!/usr/bin/env python3
"""Read-only review closure/integrity check; no writes or subprocesses."""
from pathlib import Path
import hashlib,json,stat,zipfile

A=Path(__file__).resolve().parent
P=A.parent/'preprint'
sha=lambda b:hashlib.sha256(b).hexdigest()
closure_names={'MANIFEST.json','FINAL_SEAL.json','private/closure_001/stdout',
 'private/closure_001/stderr','private/closure_001/receipt.json'}
m=json.loads((A/'MANIFEST.json').read_bytes())
assert set(m['excluded_files'])==closure_names
assert not any(p.is_symlink() for p in A.rglob('*'))
actual={p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file()}
assert actual-closure_names==set(m['files'])
assert {p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_dir()}==set(m['directories'])
for name,e in m['files'].items():
 p=A/name
 assert stat.S_ISREG(p.lstat().st_mode)
 b=p.read_bytes()
 assert len(b)==e['bytes'] and sha(b)==e['sha256'],name
assert m['scope']=='Exact preprint_review_01 namespace; no mathematical or priority proof by hashes.'

seal=json.loads((A/'ANALYTIC_SEAL.json').read_bytes())
b=(A/seal['file']).read_bytes()
assert len(b)==seal['bytes'] and sha(b)==seal['sha256']
assert seal['candidate_programs_executed'] is False
assert seal['supplied_analytic_verdicts_read'] is False
assert seal['initial_pin_manifest_pass_summaries_exposed'] is True

pins=json.loads((P/'INITIAL_REVIEW_PACKAGE.json').read_bytes())
initial=json.loads((A/'INITIAL_BINDING.json').read_bytes())
assert initial==pins['submission_files']
assert set(initial)=={'biconstrained_asymmetry.tex','biconstrained_asymmetry.pdf',
 'biconstrained-asymmetry-verification.zip','zenodo-deposit.json'}
for name,e in initial.items():
 b=(P/name).read_bytes()
 assert len(b)==e['bytes'] and sha(b)==e['sha256'],name

R=A/'private/zip_scratch_002/biconstrained-asymmetry-verification'
zb=json.loads((A/'ZIP_BINDING.json').read_bytes())
archive=P/'biconstrained-asymmetry-verification.zip'
assert zb['zip_sha256']==sha(archive.read_bytes())
with zipfile.ZipFile(archive) as z:
 entries=[i for i in z.infolist() if not i.is_dir()]
 assert len(entries)==87
 assert len({i.filename for i in entries})==87
 assert {i.filename for i in entries}=={e['path'] for e in zb['members']}
 zi={e['path']:e for e in zb['members']}
 for i in entries:
  parts=Path(i.filename).parts
  assert parts[0]=='biconstrained-asymmetry-verification' and '..' not in parts
  name=Path(*parts[1:])
  b=z.read(i)
  assert b==(P/'verification'/name).read_bytes()==(R/name).read_bytes()
  assert len(b)==zi[i.filename]['bytes'] and sha(b)==zi[i.filename]['sha256']
pm=json.loads((R/'MANIFEST.json').read_bytes())
assert {p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}==set(pm['files'])|{'MANIFEST.json'}
for name,e in pm['files'].items():
 b=(R/name).read_bytes()
 assert len(b)==e['bytes'] and sha(b)==e['sha256']
assert sum(p.is_file() for p in (R/'reference').rglob('*'))==41
reads=json.loads((A/'ALL_FILE_READ_RECEIPT.json').read_bytes())
assert len(reads['files'])==87 and len(reads['validated_manifest_instances'])==253
assert reads['unavailable_manifest_members']==[]
assert reads['all_prose_and_executable_code_read'] is True
for e in reads['files']:
 b=(R/e['path']).read_bytes()
 assert len(b)==e['bytes'] and sha(b)==e['sha256']

specs=[('reference/verify_turn1.py','reference/TURN_1_CHECKS.json',29175),
 ('reference/verify_turn2.py','reference/TURN_2_CHECKS.json',12749),
 ('reference/verify_turn3.py','reference/TURN_3_CHECKS.json',1831),
 ('reference/review/check_independent.py','reference/review/INDEPENDENT_CHECKS.json',2552),
 ('controls/graph_boundary_controls.py','controls/graph_boundary_expected.json',122568),
 ('controls/polytope_controls.py','controls/polytope_expected.json',357),
 ('verify_package.py',None,None)]
replays=json.loads((A/'REPLAY_RECEIPT.json').read_bytes())
assert replays['package_unchanged'] is True
assert len(replays['entries'])==len(specs)
for index,(program,expected,count) in enumerate(specs):
 e=replays['entries'][index]
 assert e['program']==program and e['expected_file']==expected
 assert len(e['argv'])==3 and e['argv'][1]=='-B' and e['argv'][2]==str(R/program)
 cwd=R/'reference' if program.startswith('reference/') else (R/program).parent
 assert e['cwd']==str(cwd) and e['start_utc']<=e['end_utc']
 assert e['program_sha256']==sha((R/program).read_bytes())
 C=A/'private/replays_001'
 assert json.loads((C/(e['capture_stem']+'.receipt.json')).read_bytes())==e
 out=(C/(e['capture_stem']+'.stdout')).read_bytes()
 err=(C/(e['capture_stem']+'.stderr')).read_bytes()
 assert e['exit_code']==0 and err==b'' and e['stderr_bytes']==0
 assert len(out)==e['stdout_bytes'] and sha(out)==e['stdout_sha256']
 assert sha(err)==e['stderr_sha256']
 assert sha(b'STDOUT\0'+out+b'STDERR\0'+err)==e['logical_stream_sha256']
 obj=json.loads(out)
 assert obj['status']=='PASS'
 if expected:
  assert out==(R/expected).read_bytes() and e['exact_expected_stdout'] is True
  assert obj.get('assertions',obj.get('exact_assertions'))==count
 else:
  assert obj==pins['portable_whole_replay']
  assert e['exact_expected_stdout'] is None

sources=json.loads((A/'SOURCE_RECEIPTS.json').read_bytes())
expected_sources=json.loads((R/'reference/SOURCE_MANIFEST.json').read_bytes())['sources']
assert len(sources)==len(expected_sources)==3
for s,e in zip(sources,expected_sources):
 assert s['file']==e['file'] and s['url']==e['url']
 b=(A/'private/primary'/s['file']).read_bytes()
 assert len(b)==s['bytes']==e['bytes'] and sha(b)==s['sha256']==e['sha256']
 assert sha((A/'private/primary'/Path(s['file']).with_suffix('.txt')).read_bytes())==s['text_sha256']

C=A/'private/controls_capture_001'
e=json.loads((C/'receipt.json').read_bytes())
out=(C/'stdout').read_bytes();err=(C/'stderr').read_bytes()
assert out==(A/'CONTROLS.json').read_bytes()
assert e['exit_code']==0 and err==b'' and e['stderr_bytes']==0
assert len(out)==e['stdout_bytes'] and sha(out)==e['stdout_sha256'] and sha(err)==e['stderr_sha256']
assert e['argv'][1:]==['-B',str(A/'independent_controls.py')] and e['cwd']==str(A)
assert e['start_utc']<=e['end_utc']
control=json.loads(out)
assert control['status']=='PASS' and control['assertions']==188472
assert control['census_pairs']==53919649 and control['ordinary_patterns']==7343
assert control['full_cases']+control['nonfull_cases']==control['census_pairs']
assert control['nonfull_cases']==13716 and control['repeated_C_nonfull']==11988 and control['extra_A_nonfull']==11880

fs=A/'FINAL_SEAL.json'
if fs.exists():
 final=json.loads(fs.read_bytes())
 assert final['workflow_completion_percent']==100 and final['mandatory_corrections']==0
 for e in final['bindings']:
  b=(A/e['path']).read_bytes()
  assert len(b)==e['bytes'] and sha(b)==e['sha256']
 assert final['verifier_exit_code']==0 and final['verifier_stderr_bytes']==0
 assert json.loads((A/'private/closure_001/stdout').read_bytes())['status']=='PASS_EXACT_REVIEW_NAMESPACE'

print(json.dumps(dict(status='PASS_EXACT_REVIEW_NAMESPACE',submission_files=4,zip_members=87,
 original_reference_files=41,distributed_manifest_instances=253,whole_replays=7,
 primary_PDF_pins=3,fresh_control_assertions=188472,
 scope='Read-only byte, namespace and stored whole-stream/semantic validation. Universal proof is reviewed analytically; no historical priority, exact minima/values/sign or execution-event provenance is proved by hashes.'),indent=2,sort_keys=True))
