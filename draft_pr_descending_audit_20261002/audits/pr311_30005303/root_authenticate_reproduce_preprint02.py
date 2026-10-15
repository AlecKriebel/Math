"""Independently authenticate the final seal and reproduce reviewer02's finite checks."""
from root_submission_gate import *
import shutil

D = A/'preprint_review_02'
known = {'FINAL_REVIEW_REPORT.md':(26730,'ffb4c0ffe9fdbe9870e37c53e1cecc271695be2eaa7914d44fb503a38854acab'),
         'FINAL_SEAL_MANIFEST.json':(103144,'15a25f31d96f838f1c46e8879572b108a0ad4c610e253e940d57422446a75c8d'),
         'FINAL_SEAL_VERIFICATION.json':(112964,'0914802ba647ce1a79c69bf1fa2e54478dab4028c860a5b4c393337e4ceb2abb'),
         'FINAL_CLOSURE_RECORD.json':(2989,'984099dc58bea6f22e0d87da2b1ca4fbcaa25c11f3dc17c0029a7c23b684c16a')}
for n,(size,h) in known.items():
    assert pin(D/n) == {'bytes':size,'sha256':h,'mode':'0444'}
m = load(D/'FINAL_SEAL_MANIFEST.json')
v = load(D/'FINAL_SEAL_VERIFICATION.json')
c = load(D/'FINAL_CLOSURE_RECORD.json')
assert m['substantive_full_review_complete'] and m['blocking_findings'] == 0
assert len(m['files']) == m['manifested_file_count'] == 457
assert v['status'] == 'PASS_INDEPENDENT_COMPLETE_NAMESPACE_AND_INPUT_VERIFICATION' and v['verified_files'] == m['files']
assert c['status'] == 'PASS_FINAL_READONLY_FILE_CLOSURE' and c['final_file_count_including_this_record'] == 466
excluded = set(m['administrative_non_self_hashing_exclusions'])
assert len(excluded) == 9
def verify(entry,root=D,absolute=False):
    p = Path(entry['path']) if absolute else root/entry['relative_path']
    assert pin(p) == {k:entry[k] for k in ['bytes','sha256','mode']}, p
for entry in m['files']:
    rel = Path(entry['relative_path'])
    assert not rel.is_absolute() and '..' not in rel.parts
    verify(entry)
assert {str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()} == {e['relative_path'] for e in m['files']} | excluded
assert {str(p.relative_to(D)):format(stat.S_IMODE(p.stat().st_mode),'04o') for p in D.rglob('*') if p.is_dir()} == {e['relative_path']:e['mode'] for e in m['directories']}
assert not any(p.is_symlink() for p in D.rglob('*'))
assert {e['relative_path'] for e in c['administrative_records_measured']} == excluded-{'FINAL_CLOSURE_RECORD.json'}
for entry in c['administrative_records_measured']:
    verify(entry)
g = load(A/'ROOT_PREPRINT02_SOURCE_GATE.json')
released = g['named_package_files']+g['named_formal_submission_files']+g['named_historical_build_evidence_files']
assert len(released) == 31
assert {e['path']:e for e in released} == {e['path']:e for e in v['verified_named_originals']}
for entry in released+g['source_gate_pins']:
    verify(entry,absolute=True)
early = load(D/'SOURCE_ONLY_FREEZE_MANIFEST.json')
assert early['reports']+early['private_evidence'] == v['verified_original_source_only_entries']
for entry in early['reports']+early['private_evidence']:
    verify(entry,absolute=True)
native = []
for p in (D/'private').glob('*.command.json'):
    rec = load(p)
    for stream in ['stdout','stderr']:
        entry = rec[stream]
        assert pin(Path(entry['path']))['sha256'] == entry['sha256'] and pin(Path(entry['path']))['bytes'] == entry['bytes']
    native.append({'path':str(p.relative_to(D)), 'argv':rec['argv'],'start_utc':rec['start_utc'],
                   'end_utc':rec['end_utc'],'exit_code':rec['exit_code']})
for case in load(D/'NEGATIVE_CONTROL_RESULTS.json')['native_cases']:
    rec = load(Path(case['execution_record']))
    assert rec['exit_code'] == case['exit_code'] == 1 and case['passed']
    for stream in ['stdout','stderr']:
        entry = rec[stream]
        assert pin(Path(entry['path']))['sha256'] == entry['sha256'] and pin(Path(entry['path']))['bytes'] == entry['bytes']
before = {str(p.relative_to(D)):pin(p) for p in D.rglob('*') if p.is_file()}
cap = Capture('root_preprint02_reproduction')
X = cap.directory/'fresh_reviewer_copy'
priv = X/'private'
package = priv/'different_location/portable_package'
package.mkdir(parents=True)
with zipfile.ZipFile(O/'mtp2-edge-closure-verification.zip') as z:
    assert len(z.namelist()) == 13 and set(z.namelist()) == {str(p.relative_to(Q)) for p in Q.rglob('*') if p.is_file()}
    for i in z.infolist():
        rel = Path(i.filename)
        assert not rel.is_absolute() and '..' not in rel.parts
        p = package/rel
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(z.read(i))
        p.chmod(0o644)
        assert p.read_bytes() == (Q/rel).read_bytes()
for n in ['INDEPENDENT_CHECKS.py','NEGATIVE_CONTROLS.py']:
    shutil.copyfile(D/n,X/n)
    assert (X/n).read_bytes() == (D/n).read_bytes()
run = cap.run('new_independent_exact',['/opt/homebrew/bin/python3','-B',X/'INDEPENDENT_CHECKS.py',
    '--expected',package/'expected','--output',X/'INDEPENDENT_CHECK_RESULTS.json'],cwd=X)
assert not run.stderr and (X/'INDEPENDENT_CHECK_RESULTS.json').read_bytes() == (D/'INDEPENDENT_CHECK_RESULTS.json').read_bytes()
portable = cap.run('new_portable_reproduction',['/opt/homebrew/bin/python3','-B',package/'REPRODUCE.py',
    '--out-dir',priv/'different_location/fresh_results'],cwd=priv/'different_location')
assert not portable.stderr
results = priv/'different_location/fresh_results'
assert load(results/'boundary.stdout') == load(Q/'expected/boundary.json')
assert (results/'priority_laws.json').read_bytes() == (Q/'expected/priority_laws.json').read_bytes()
negative = cap.run('new_negative_cases',['/opt/homebrew/bin/python3','-B',X/'NEGATIVE_CONTROLS.py',
    '--private-dir',priv],cwd=X)
assert not negative.stderr
now,old = load(X/'NEGATIVE_CONTROL_RESULTS.json'),load(D/'NEGATIVE_CONTROL_RESULTS.json')
assert now['status'] == old['status'] and now['malformed_pin_independently_rejected']
assert [{k:x[k] for k in ['name','exit_code','passed']} for x in now['native_cases']] == [{k:x[k] for k in ['name','exit_code','passed']} for x in old['native_cases']]
assert {str(p.relative_to(D)):pin(p) for p in D.rglob('*') if p.is_file()} == before
for entry in released+g['source_gate_pins']:
    verify(entry,absolute=True)
out = {'recorded_utc':utc(),'status':'PASS_ROOT_AUTHENTICATION_AND_FRESH_PREPRINT02_REPRODUCTION',
    'final_pins':{n:h for n,(_,h) in known.items()},'sealed_body_files':457,'terminal_files_authenticated':9,
    'all466_review_files_0444_unchanged':True,'source_gate_27_entries_and_four_pins_unchanged':True,
    'all31_named_released_inputs_unchanged':True,'native_review_captures_authenticated':native,
    'root_native_capture_directory':str(cap.directory),'root_native_jobs':cap.entries,
    'entire_independent_result_bytes_equal':True,'portable_boundary_semantics_and_priority_bytes_equal':True,
    'all_nine_native_negative_outcomes_and_malformed_pin_control_equal':True,
    'root_read_scope_recorded_separately':True,'publication_clearance_created':False,'workflow_percent':70}
with (A/'ROOT_PREPRINT02_ARTIFACT_AUTHENTICATION.json').open('x') as h:
    h.write(json.dumps(out,indent=2)+'\n')
for label,res in [('independent',run),('portable',portable),('negative',negative)]:
    print(label+' FULL STDOUT')
    print(res.stdout.decode())
print(json.dumps({'status':out['status'],'body_files':457,'terminal_files':9,
                  'actual_utc':out['recorded_utc'],'root_capture_directory':str(cap.directory)},indent=2))
