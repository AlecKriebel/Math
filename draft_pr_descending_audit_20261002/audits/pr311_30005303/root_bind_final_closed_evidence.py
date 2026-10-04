"""Bind historical seals and final clean review after ROOT's actual adjudication."""
from root_submission_gate import *

f = load(A/'ROOT_PREPRINT02_ADJUDICATION.json')
assert f['status'] == 'PASS_ROOT_CLOSED_CLEAN_FULL_PREPRINT_REVIEW' and f['unresolved_findings'] == 0
assert f['complete_report_read'] and f['independent_reproduction_verified']
assert f['sealed_review_authenticated'] and f['source_gate_unchanged'] and f['all_released_inputs_unchanged']
assert not (A/'ROOT_FINAL_CLOSED_EVIDENCE.json').exists()
expected = {
    'lattice_factorization/FINAL_AUDIT_MANIFEST.json':'eae6746baa8d258b254978d90b5f9f82350cfb19865d903e72719d39ade2400a',
    'markov_closure/FINAL_AUDIT_MANIFEST.json':'f7179349eac3082de85e1730ca9ede60dfd9551672555fbe718254cedeac8336',
    'priority_factorization/FINAL_INPUT_OUTPUT_SHA_MANIFEST.json':'f4719a1af2d90c98bc14db57d475809aeae72721a8dad8669aa647d8a941d579',
    'priority_closure/INPUT_OUTPUT_SHA_MANIFEST.json':'4855a0c002716e42a3416c12b58328ac6752ad6caabb9a29a53c97fcaf60d20f',
    'closure_priority_adversary/public/SEALED_MANIFEST.json':'816aea4b853ecf63fc34920423ee24032b787519d5cac10f3494418c4db95420',
    'preprint_review_01/FINAL_SEAL_MANIFEST.json':'41f47c6204cf050e1275cf678a28c5a648285fe3d2a831097c54c226129655b8',
    'lattice_factorization/FINAL_WHOLE_PROOF_REPORT.md':'69c516eead3f4b4582a6bcd9985791ba2b9756ac54cafe9ffab8c6a0103ae184',
    'markov_closure/FINAL_WHOLE_PROOF_REPORT.md':'965f48523340ea9d753cf3d9ce9ab6bffa35834c91af086816b0f51fcb87119f',
    'priority_factorization/FINAL_PRIORITY_REPORT.md':'0f328de205ba243eb2ada09a07f0bf4488e9a40e8dc36b7643c5716e25da8dff',
    'priority_closure/FINAL_PRIORITY_REPORT.md':'205e8114aed491f04b54f8f7dda67d09c741d5ac78663f1fc8e936796bb783f2',
    'closure_priority_adversary/public/FINAL_PRIORITY_REPORT.md':'2253f36227468bfdc59b85d4d9c2f14563b2b1d8427bc5a384c9a643509dd71f',
    'preprint_review_01/FINAL_REVIEW.md':'d9eb02de0a037159b6a618b7da391876f4606ba83582281831d0f79cb7f9eb9c'}
for n,h in expected.items():
    assert pin(A/n)['sha256'] == h and pin(A/n)['mode'] == '0444', n
for n,h in f['final_pins'].items():
    assert pin(A/'preprint_review_02'/n)['sha256'] == h and pin(A/'preprint_review_02'/n)['mode'] == '0444', n

verified_rows = {}
def verify_row(p,e):
    assert p.is_relative_to(A)
    actual = pin(p)
    assert actual['mode'] == '0444'
    assert actual['sha256'] == e['sha256']
    assert actual['bytes'] == e.get('bytes',e.get('size_bytes'))
    rel = str(p.relative_to(A))
    if rel in verified_rows:
        assert verified_rows[rel] == actual
    verified_rows[rel] = actual

L = A/'lattice_factorization'
lm = load(L/'FINAL_AUDIT_MANIFEST.json')
assert len(lm['files']) == 31
for r in lm['files']:
    assert r['new_mode'] == '0444'
    verify_row(Path(r['path']),r)
M = A/'markov_closure'
mm = load(M/'FINAL_AUDIT_MANIFEST.json')
assert len(mm['artifacts']) == 24
for r in mm['artifacts']:
    assert r['observed_final_mode'] == '0o444'
    verify_row(Path(r['path']),r)
F = A/'priority_factorization'
fm = load(F/'FINAL_INPUT_OUTPUT_SHA_MANIFEST.json')
assert len(fm['audit_files']) == 115
for r in fm['audit_files']:
    e = r['final_actual_measurement']
    assert e['mode'] == '0o444'
    verify_row(F/r['relative_path'],e)
C = A/'priority_closure'
cm = load(C/'INPUT_OUTPUT_SHA_MANIFEST.json')
for r in cm['public_outputs_before_seal']+cm['private_preservation_inventory']:
    assert r['planned_final_mode'] == '0o444'
    verify_row(C/r['path'],r)
cs = load(C/'FINAL_SEAL.json')
assert len(cs['files']) == 92 and cs['all_bytes_unchanged']
for r in cs['files']:
    assert r['sha256_before'] == r['sha256_after'] and r['measured_final_mode'] == '0o444'
    verify_row(C/r['path'],{'bytes':r['bytes'],'sha256':r['sha256_after']})
V = A/'closure_priority_adversary'
vm = load(V/'public/SEALED_MANIFEST.json')
assert len(vm['files']) == 110
for r in vm['files']:
    assert r['mode'] == '0o444'
    verify_row(V/r['path'],r)
R1 = A/'preprint_review_01'
r1 = load(R1/'FINAL_SEAL_MANIFEST.json')
assert len(r1['files']) == 376
for r in r1['files']:
    verify_row(Path(r['path']),r)
# The new complete review's own original seal has already been authenticated
# during ROOT adjudication. Pin every readonly body and terminal receipt now.
folders = {'lattice_factorization':33,'markov_closure':27,'priority_factorization':117,
           'priority_closure':94,'closure_priority_adversary':112,'preprint_review_01':385,
           'preprint_review_02':f['sealed_body_files']+f['terminal_files_authenticated']}
closed = {}
namespace_counts = {}
for n,count in folders.items():
    found = {str(p.relative_to(A)):pin(p) for p in (A/n).rglob('*')
             if p.is_file() and stat.S_IMODE(p.stat().st_mode) == 0o444}
    assert len(found) == count, (n,len(found),count)
    namespace_counts[n] = count
    closed.update(found)
assert set(verified_rows) <= set(closed)
for n,e in verified_rows.items():
    assert closed[n] == e
source_gate = load(A/'ROOT_PREPRINT02_SOURCE_GATE.json')
historical_build = {}
for e in source_gate['named_historical_build_evidence_files']:
    p = Path(e['path'])
    assert pin(p) == {k:e[k] for k in ['bytes','sha256','mode']}
    historical_build[str(p.relative_to(A))] = pin(p)
out = {'recorded_utc':utc(),'status':'ALL_CURRENT_SCIENTIFIC_AND_REVIEW_FROZEN_FILES_BOUND',
       'closed_scientific_files':closed,'namespace_file_counts':namespace_counts,
       'historical_original_seal_payload_rows_rechecked':len(verified_rows),
       'historical_build_evidence_files':historical_build,
       'excluded_files_policy':'Only non-readonly historical auxiliary logs/source copies are outside this frozen-file binding. All original seal payload rows, readonly scientific/review bodies and terminal receipts are covered. No claim all private source bodies were read or published.',
       'final_review_adjudication':pin(A/'ROOT_PREPRINT02_ADJUDICATION.json'),
       'root_content_read_scope':'Complete scientific/review reports, proof artifacts and verification programs were read in their recorded review stages. This operation mechanically reauthenticates pins and adds no literature or mathematical proof claim.',
       'math_percent':100,'bounded_priority_percent':100,'workflow_percent':75,
       'publication_clearance_created_here':False}
with (A/'ROOT_FINAL_CLOSED_EVIDENCE.json').open('x') as h:
    h.write(json.dumps(out,indent=2)+'\n')
print(json.dumps({'recorded_utc':out['recorded_utc'],'status':out['status'],
                  'frozen_files':len(closed),'namespace_counts':namespace_counts,
                  'original_seal_rows':len(verified_rows),'historical_build_files':len(historical_build)},indent=2))
