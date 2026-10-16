"""Root read-only prepublication freeze/gates; does not accept or publish."""
import sys
if not sys.flags.isolated:
    raise RuntimeError('Use Python -I -B')
from pathlib import Path
import datetime, hashlib, json, types
ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_claimed_solved_900_1000_20261012'
A = P / 'audits/pr946_6000001'
D = A / 'preprint'
def fp(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def read(path):
    return json.loads(path.read_text())
def save(path, value):
    with path.open('x') as handle:
        json.dump(value, handle, indent=2)
        handle.write('\n')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
core = P / 'accept_pr946.py'
if fp(core)['sha256'] != '0ac1335d4703638002392802a37db43fa0307561a8052b54b98f47c955094591':
    raise RuntimeError('Externally checked candidate04 core differs')
old = read(D / 'reviewed_candidates/candidate03/FREEZE.json')
if read(D / 'FREEZE.json') != old:
    raise RuntimeError('Expected unchanged candidate03 before new freeze')
save(A / 'REVIEW03_REPAIR_RESOLUTIONS.json', {
    'utc': now, 'pr': 946, 'status': 'ROOT_REPAIRED_PENDING_NEW_ENTIRE_FULL_REVIEW04',
    'required_and_residual_issues': ['FP03-OPS-001', 'FP02-OPS-001'],
    'repair': 'Complete accepted-chain reauthentication after all completion/state/next-status reads immediately before completion writes, and before already-finalized return after reading state.',
    'all_other_dispatch_guards_preserved': True,
    'independent_old_defects_reproduced': 'ROOT_REVIEW03_OLD_DEFECT_REPRODUCTION.json',
    'actual_shared_guard_11_case_controls': 'REVIEW03_FINAL_COMPLETION_CONTROLS.json',
    'controls': ['valid complete accepted chain', 'valid completion', 'valid already-finalized recovery',
                 'pending/adverse new canonical rounds in both late read windows',
                 'payload/manifest drift in both late read windows'],
    'prior_actual_chain_regressions': {'receipt': 'ROOT_CANDIDATE04_POST_ACCEPTANCE_CONTROLS.json', 'cases': 17},
    'component_regressions': {'folder': 'repair_controls_v4', 'cases': [84, 68],
                              'shared_guard_fixture_stubs_disclosed': True},
    'paper_tex_pdf_inner_package_zip_and_outer_manifest_byte_identical': True,
    'all_old_candidate03_files_and7sources_preserved': True,
    'root_test_harness_correction': 'Initial added payload-drift fixture grew beyond sealed size; changed to same-length corruption to exercise fingerprint rejection. Both old/new full11-case suites then completed successfully.',
    'trusted_receipt_store_process_filesystem_assumed_no_atomic_OS_race_claim': True,
    'new_proof_responses': 0, 'actual_external_mutations': 0})
new_evidence = [
    'prepare_candidate04.py', 'freeze_candidate04.py',
    'ROOT_FULL_REVIEW_03_VERIFICATION.json', 'CANDIDATE03_PRESERVATION.json',
    'REVIEW03_REPAIR_RESOLUTIONS.json', 'REVIEW03_FINAL_COMPLETION_CONTROLS.py',
    'ROOT_REVIEW03_OLD_DEFECT_REPRODUCTION.json', 'REVIEW03_FINAL_COMPLETION_CONTROLS.json',
    'ROOT_CANDIDATE04_POST_ACCEPTANCE_CONTROLS.json',
    'repair_controls_v4/offline_controls_adapted.py', 'repair_controls_v4/review01_controls_adapted.py',
    'repair_controls_v4/ADAPTATION.md', 'repair_controls_v4/OFFLINE_CONTROLS.json',
    'repair_controls_v4/REVIEW01_COMPONENT_CONTROLS.json']
freeze = json.loads(json.dumps(old))
freeze.update(utc=now, revision_candidate=4,
              operations_inventory_sha256=fp(A / 'OPERATIONS_INVENTORY.json')['sha256'],
              readiness='FROZEN_CANDIDATE_ONLY; required NEW04 entire independent full-package review remains outstanding')
freeze['future_helpers']['accept_pr946.py'] = fp(core)
for relative in new_evidence:
    path = A / relative
    freeze['evidence_files'][path.relative_to(ROOT).as_posix()] = fp(path)
(D / 'FREEZE.json').write_text(json.dumps(freeze, indent=2) + '\n')
pin = fp(D / 'FREEZE.json')['sha256']
N = {'__name__': '_root_candidate04_readonly_', '__file__': str(core)}
exec(compile(core.read_bytes(), str(core), 'exec', dont_inherit=True, optimize=0), N)
context = N['capture_inventory'](freeze['operations_inventory_sha256'])
checked = N['freeze_check'](N['read_regular'](D / 'FREEZE.json'), pin, context)
N['disposition_check']()
pr, parent, source, originals = N['premerge_gate'](checked, require_draft=True)
archive = N['archive_check'](checked, originals)
for number in (1, 2, 3):
    base = D / 'reviewed_candidates' / ('candidate%02d' % number)
    raw = N['read_regular'](base / 'FREEZE.json')
    N['freeze_check'](raw, N['sha'](raw), context, base=base, historical=True)
kit_key = 'zenodo_deposit_tool/zenodo.py'
kit = {'__name__': '_root_captured_kit_check_', '__file__': str(ROOT / kit_key)}
exec(compile(context['captured'][kit_key], str(ROOT / kit_key), 'exec', dont_inherit=True, optimize=0), kit)
summary = kit['run'](types.SimpleNamespace(command='check', manifest=D / 'zenodo-deposit.json', sandbox=False))
save(A / 'ROOT_ZENODO_CANDIDATE04_LOCAL_CHECK.json', summary)
pr.pop('body', None)
save(A / 'ROOT_CANDIDATE04_PRE_REVIEW_GATE.json', {
    'utc': N['utc_now'](), 'result': 'PASS_READONLY_PREPARATION_GATES', 'candidate_revision': 4,
    'freeze_sha256': pin, 'operations_inventory_sha256': context['inventory_sha256'],
    'actual_live_PR': pr, 'fresh_main': parent, 'source_gate': source,
    'all33_actual_Git_disk_archive_verified': True,
    'archive': archive, 'captured_kit_local_check': 'PASS',
    'historical_candidate01_02_03_authentication': 'PASS',
    'FP03_and_residual_FP02_OPS_findings_repaired_pending_NEW_full_review04': True,
    'current_paper_and_archive_and_all223_files_byte_identical_to_candidate03': checked['files'] == old['files'],
    'actual_external_mutations': 0, 'acceptance_merge_publication_tracker_native_actions_executed': False})
print(json.dumps({'status': 'FROZEN4_AND_PRE_REVIEW_GATES_PASS', 'freeze_sha256': pin,
                  'operations_inventory_sha256': context['inventory_sha256'],
                  'frozen_files': len(freeze['files']), 'immutable_evidence': len(freeze['evidence_files']),
                  'fresh_main': parent, 'actual_external_mutations': 0}))
