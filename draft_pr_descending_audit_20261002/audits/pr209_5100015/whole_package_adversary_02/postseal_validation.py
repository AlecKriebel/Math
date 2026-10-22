"""Additive preservation of an own path-lookup error and final read-only QA.

The report, assessment, freeze and every originally sealed payload stay unchanged.
The initial seal is retained byte-exact; the final manifest adds this provenance.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

O=Path(__file__).resolve().parent;B=O.parent/'preprint'
old=(O/'AUTHORED_MANIFEST.json').read_bytes();m=json.loads(old)
assert not (O/'AUTHORED_MANIFEST_INITIAL.json').exists()
(O/'AUTHORED_MANIFEST_INITIAL.json').write_bytes(old)
failed_code="""from pathlib import Path
import hashlib,json
O=Path('.');m=json.loads((O/'AUTHORED_MANIFEST.json').read_text());a=json.loads((O/'ASSESSMENT.json').read_text())
for r in m['files']:
 raw=(O/r['path']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
for r in a['evidence'].values():
 raw=(O/r['path']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
for n,r in a['frozen_bindings'].items():
 raw=(O.parent/'preprint'/n).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
assert a['mandatory_findings']==a['optional_findings']==[]
text=(O/'REPORT.md').read_text();assert all(x not in text for x in ['COMPLETED_UTC','FROZEN_UTC','CORE_TABLE'])
print(json.dumps(dict(status='PASS',review_completed_utc=a['completed_utc'],sealed_rows=len(m['files']),review_files_valid=True,all_seven_current_core_bindings_valid=True,mandatory=0,optional=0),indent=2))
"""
error="""Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
  File "/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/lib/python3.12/pathlib.py", line 1019, in read_bytes
    with self.open(mode='rb') as f:
         ^^^^^^^^^^^^^^^^^^^^
  File "/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/lib/python3.12/pathlib.py", line 1013, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'preprint/PACKAGE_MANIFEST.json'
"""
failure=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),program=failed_code,stdout='',stderr=error,exit_code=1,scope='Own additional read-only postseal QA, after every original manifest row and assessment evidence pin had passed',cause="Path('.').parent is '.' rather than the resolved working-directory parent; wrong relative candidate lookup",resolution='Use absolute resolved owned directory. No candidate defect or scientific failure; all original assertions/timestamps and payload bytes preserved.')
(O/'FAILED_FINAL_CHECK_01.json').write_text(json.dumps(failure,indent=2)+'\n')
for r in m['files']:
    raw=(O/r['path']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
a=json.loads((O/'ASSESSMENT.json').read_text())
for r in a['evidence'].values():
    raw=(O/r['path']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
for n,r in a['frozen_bindings'].items():
    raw=(B/n).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
assert a['mandatory_findings']==a['optional_findings']==[]
assert all(x not in (O/'REPORT.md').read_text() for x in ['COMPLETED_UTC','FROZEN_UTC','CORE_TABLE'])
qa=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',originally_sealed_payloads_unchanged=len(m['files']),all_assessment_evidence_pins_valid=True,all_seven_current_core_bindings_valid=True,review_completed_utc_preserved=a['completed_utc'],report_and_assessment_unchanged=True,own_readonly_path_probe_corrected=True)
(O/'FINAL_SEAL_QA.json').write_text(json.dumps(qa,indent=2)+'\n')
def pin(p):
    raw=p.read_bytes();return dict(path=p.relative_to(O).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
rows=[]
prefixes=[r['prefix'] for r in m['excluded_copied_input_trees']]
for p in sorted(O.rglob('*')):
    if not p.is_file() or p==O/'AUTHORED_MANIFEST.json':continue
    rel=p.relative_to(O).as_posix()
    if any(rel.startswith(prefix) for prefix in prefixes):continue
    row=pin(p);row['role']='candidate fixture or copied science execution evidence' if '/inputs/' in rel or (rel.startswith('real_eight_suite_replay/') and p.suffix=='.py') or (rel.startswith('own_real_failure_controls/') and p.suffix=='.py') else 'authored review evidence';rows.append(row)
new=dict(m);new.update(sealed_utc=datetime.now(timezone.utc).isoformat(),initial_sealed_utc=m['sealed_utc'],initial_seal=pin(O/'AUTHORED_MANIFEST_INITIAL.json'),additive_postseal_record='Read-only own relative-path QA error retained and corrected. All636 original payloads and completed review assertions unchanged; only additive provenance and final QA are added.',files=rows)
(O/'AUTHORED_MANIFEST.json').write_text(json.dumps(new,indent=2)+'\n')
for r in rows:
    raw=(O/r['path']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
print(json.dumps(dict(status='PASS',verdict=a['verdict'],mandatory=0,optional=0,report=pin(O/'REPORT.md'),assessment=pin(O/'ASSESSMENT.json'),final_authored_manifest=pin(O/'AUTHORED_MANIFEST.json'),sealed_rows=len(rows),initial636_payloads_unchanged=True),indent=2))
