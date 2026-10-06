#!/usr/bin/env python3
import datetime
import hashlib
import json
import os
from pathlib import Path

root = Path(__file__).resolve().parent
a = root.parent
original = a / 'original_head_authentication_20261006' / 'original_attempt'
def pin(path):
    body = path.read_bytes()
    return {'path':str(path),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}

initial = json.loads((root/'INITIAL_INPUT_PINS.json').read_text())
for expected in initial['pins']:
    if pin(Path(expected['path'])) != expected:
        raise RuntimeError('Original independent input changed')
names = ['source_record.json','CANDIDATE.md','verify.py','verification.json',
         'review/independent_checks.py','review/independent_results.json',
         'review/REVIEW.md','review/review_summary.json','review/source_verification.json']
original_pins = [pin(original/name) for name in names]
effective_paths = [a/'ROOT_EFFECTIVE_GUARD_VALIDATION_20261006.json',
                   a/'repaired_diagnostics_v1/REPAIR.json',
                   a/'repaired_diagnostics_v1/verify.py',
                   a/'repaired_diagnostics_v1/independent_checks.py']
effective_pins = [pin(path) for path in effective_paths]
old_author = (original/'verify.py').read_bytes()
old_review = (original/'review/independent_checks.py').read_bytes()
if old_author.replace(b' assert b\n',b' if not b:raise ValueError("Exact verification guard failed")\n') != effective_paths[2].read_bytes():
    raise RuntimeError('Effective author diff is not limited to the reported guard repair')
if old_review.replace(b'    assert b,name\n',b'    if not b:raise ValueError(name)\n') != effective_paths[3].read_bytes():
    raise RuntimeError('Effective independent diff is not limited to the reported guard repair')
inputs = {'immutable_head':initial['immutable_original_head'],
          'original_inputs':original_pins,'late_effective_guard_inputs':effective_pins,
          'proof_unchanged':True,'independent_code_comparison_verified':True,
          'original_review_read_only_after_initial_independent_reasoning':True}
(root/'FINAL_INPUT_PINS.json').write_text(json.dumps(inputs,indent=2)+'\n')

retrieved = json.loads((root/'PRIMARY_SOURCE_RETRIEVAL_PINS.json').read_text())
for p in retrieved:
    actual = pin(root/'private_sources'/p['filename'])
    if actual['bytes'] != p['bytes'] or actual['sha256'] != p['sha256']:
        raise RuntimeError('Private primary PDF body changed')
images = ['owr-37.png','owr-38.png','owr-39.png','shibuta_takagi-06.png','shibuta_takagi-08.png']
source_auth = {'full_pdf_pins':retrieved,'visually_inspected_private_images':[pin(root/'private_sources'/name) for name in images],
               'printed_pages':['OWR 1137','OWR 1138','OWR 1139','Shibuta–Takagi v3 6','Shibuta–Takagi v3 8'],
               'complete_relevant_source_text_extracted_and_read':'Shibuta–Takagi v3 printed pp.6–8',
               'ring':'polynomial k[x1,...,xn] over characteristic-zero field',
               'laurent_or_unit_inversion_required':False,
               'regular_sequence_or_space_curve_required_in_question':False,
               'private_pdf_text_render_bodies_excluded':True}
(root/'SOURCE_VISUAL_AUTHENTICATION.json').write_text(json.dumps(source_auth,indent=2)+'\n')
controls = json.loads((root/'INDEPENDENT_CONTROLS_NORMAL.json').read_text())
optimized = json.loads((root/'INDEPENDENT_CONTROLS_OPTIMIZED.json').read_text())
if controls['checks_total'] != 59747 or optimized['checks_total'] != 59747:
    raise RuntimeError('Independent guard count changed unexpectedly')
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
result = {'schema':'pr117-ideal-hypotheses-adversarial-audit/v1','utc':utc,
          'actual_sealer_PID':os.getpid(),'verdict':'PASS_IDEAL_AND_HYPOTHESES',
          'candidate_sha256':hashlib.sha256((original/'CANDIDATE.md').read_bytes()).hexdigest(),
          'mandatory_mathematical_corrections':[],
          'family_audit_completion_percent':100,
          'global_and_homogeneous_local_minimality':True,
          'polynomial_and_homogeneous_local_monomial_absence':True,
          'optional_all_degree_prime_kernel_proof':True,
          'independent_controls_normal_and_optimized':True,
          'controls_per_mode':59747,'new_central_proof_search_turns':0,
          'original_attempts':'1/5','priority_clearance':False,
          'publication_readiness':False,'human_peer_review':False,
          'effective_root_guard_repair_body_diff_verified':True,
          'full_lp_gate_adjudication':'outside this family',
          'private_sources_excluded':True}
(root/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
with (root/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n'+utc+' — Final family checkpoint, 100% complete. PASS_IDEAL_AND_HYPOTHESES with no mandatory mathematical correction. All-degree proofs, exact independent controls, source/body pins, inspected root guard-only repair, and public-safe output manifest sealed. No full-LP, priority, publication, native-assessment, or PR-service clearance. Original inputs unchanged.\n')
public_names = ['.gitignore','RESEARCH_LOG.md','INITIAL_INPUT_PINS.json','FINAL_INPUT_PINS.json',
                'INDEPENDENT_REASONING_BEFORE_COMPARISON.md','independent_ideal_controls.py',
                'INDEPENDENT_CONTROLS_NORMAL.json','INDEPENDENT_CONTROLS_OPTIMIZED.json',
                'run_and_authenticate_controls.py','EXECUTION_RECEIPT.json',
                'retrieve_primary_sources.py','PRIMARY_SOURCE_RETRIEVAL_PINS.json',
                'SOURCE_VISUAL_AUTHENTICATION.json','REPORT.md','RESULT.json','seal_final_outputs.py']
members = []
for name in public_names:
    path = root/name
    if path.is_symlink() or not path.is_file():
        raise RuntimeError('Public member is not a regular file: '+name)
    p = pin(path)
    members.append({'path':name,'bytes':p['bytes'],'sha256':p['sha256']})
manifest = {'schema':'public-safe-adversarial-output-manifest/v1','utc':utc,
            'members':members,'copyright_bodies_excluded':['private_sources/'],
            'manifest_self_hash_not_included':True}
(root/'OUTPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
for member in members:
    actual = pin(root/member['path'])
    if actual['bytes'] != member['bytes'] or actual['sha256'] != member['sha256']:
        raise RuntimeError('Final public readback changed: '+member['path'])
print(json.dumps({'result':result,'manifest':pin(root/'OUTPUT_MANIFEST.json'),
                  'report':pin(root/'REPORT.md'),'public_members':len(members)},indent=2))
