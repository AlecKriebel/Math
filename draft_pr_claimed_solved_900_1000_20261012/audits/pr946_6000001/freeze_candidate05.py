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
    if path.name == 'REVIEW04_REPAIR_RESOLUTIONS.json' and path.exists():
        previous = read(path)
        if {k:v for k,v in previous.items() if k != 'utc'} != {k:v for k,v in value.items() if k != 'utc'}:
            raise RuntimeError('Existing partial-preparation repair record differs')
        return
    with path.open('x') as handle:
        json.dump(value, handle, indent=2)
        handle.write('\n')
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
core = P / 'accept_pr946.py'
if fp(core)['sha256'] != '62fa159687104c889195863303fa5642d877e52257bc9e4fb2bc97e89ea2b919':
    raise RuntimeError('Externally checked candidate05 core differs')
old = read(D / 'reviewed_candidates/candidate04/FREEZE.json')
if read(D / 'FREEZE.json') != old:
    raise RuntimeError('Expected unchanged candidate04 before new freeze')
save(A / 'REVIEW04_REPAIR_RESOLUTIONS.json', {
    'utc': now, 'pr': 946, 'status': 'ROOT_REPAIRED_PENDING_NEW_ENTIRE_FULL_REVIEW05',
    'required_and_residual_issues': ['FP04-OPS-001', 'FP04-OPS-002', 'FP02-OPS-001'],
    'repair': 'Central accepted_state_check at shared-history guard entry and after all original/Git/full-review reads: reread/compare entire canonical acceptance, recapture pinned seven dependencies, authenticate current external freeze/all223+48 source files, recheck disposition; final canonical-directory scan repeated. Every existing dispatch/completion guard preserved.',
    'independent_old_defects_reproduced': {'receipt': 'ROOT_REVIEW04_OLD_DEFECT_REPRODUCTION.json', 'cases': 46, 'defects': 9},
    'actual_full_capture_and_shared_guard_controls': {'receipt': 'REVIEW04_CANONICAL_STATE_CONTROLS.json', 'cases': 59,
        'additional_root_cases': '12 acceptance/freeze/TeX/helper/inventory drift injections during original-source or full-history reads, plus restored positive full-chain check',
        'transport_fixture': 'Immutable candidate04 with its actual captured seven-file inventory, actual real01/02/03 sealed reports/historical snapshots, and explicitly synthetic terminal04; subject core tested separately by external62fa pin. Production candidate05 context independently reauthenticated below.'},
    'legacy_component_regressions': {'folder': 'repair_controls_v5', 'cases': [84,68,17,11],
        'fresh_state_or_shared_guard_fixture_stubs_explicitly_disclosed_not_evidence_for_new_state_check': True},
    'all_old_candidate04_files_and7sources_preserved': True,
    'paper_tex_pdf_inner_package_zip_outer_manifest_all223_payloads_byte_identical': True,
    'no_OS_atomic_hostile_filesystem_guarantee': True, 'new_proof_responses': 0, 'external_mutations': 0})
new_evidence = [
    'prepare_candidate05.py', 'freeze_candidate05.py', 'ROOT_FULL_REVIEW_04_VERIFICATION.json',
    'CANDIDATE04_PRESERVATION.json', 'REVIEW04_REPAIR_RESOLUTIONS.json',
    'REVIEW04_CANONICAL_STATE_CONTROLS.py', 'ROOT_REVIEW04_OLD_DEFECT_REPRODUCTION.json',
    'REVIEW04_CANONICAL_STATE_CONTROLS.json',
    'repair_controls_v5/offline_controls_adapted.py', 'repair_controls_v5/review01_controls_adapted.py',
    'repair_controls_v5/review02_history_controls_adapted.py', 'repair_controls_v5/review03_completion_controls_adapted.py',
    'repair_controls_v5/ADAPTATION.md', 'repair_controls_v5/OFFLINE_CONTROLS.json',
    'repair_controls_v5/REVIEW01_COMPONENT_CONTROLS.json', 'repair_controls_v5/REVIEW02_HISTORY_CONTROLS.json',
    'repair_controls_v5/REVIEW03_COMPLETION_CONTROLS.json']

freeze = json.loads(json.dumps(old))
freeze.update(utc=now, revision_candidate=5,
              operations_inventory_sha256=fp(A / 'OPERATIONS_INVENTORY.json')['sha256'],
              readiness='FROZEN_CANDIDATE_ONLY; required NEW05 entire independent full-package review remains outstanding')
freeze['future_helpers']['accept_pr946.py'] = fp(core)
for relative in new_evidence:
    path = A / relative
    freeze['evidence_files'][path.relative_to(ROOT).as_posix()] = fp(path)
(D / 'FREEZE.json').write_text(json.dumps(freeze, indent=2) + '\n')
pin = fp(D / 'FREEZE.json')['sha256']
N = {'__name__': '_root_candidate05_readonly_', '__file__': str(core)}
exec(compile(core.read_bytes(), str(core), 'exec', dont_inherit=True, optimize=0), N)
context = N['capture_inventory'](freeze['operations_inventory_sha256'])
checked = N['freeze_check'](N['read_regular'](D / 'FREEZE.json'), pin, context)
N['disposition_check']()
pr, parent, source, originals = N['premerge_gate'](checked, require_draft=True)
archive = N['archive_check'](checked, originals)
for number in (1, 2, 3, 4):
    base = D / 'reviewed_candidates' / ('candidate%02d' % number)
    raw = N['read_regular'](base / 'FREEZE.json')
    N['freeze_check'](raw, N['sha'](raw), context, base=base, historical=True)
kit_key = 'zenodo_deposit_tool/zenodo.py'
kit = {'__name__': '_root_captured_kit_check_', '__file__': str(ROOT / kit_key)}
exec(compile(context['captured'][kit_key], str(ROOT / kit_key), 'exec', dont_inherit=True, optimize=0), kit)
summary = kit['run'](types.SimpleNamespace(command='check', manifest=D / 'zenodo-deposit.json', sandbox=False))
save(A / 'ROOT_ZENODO_CANDIDATE05_LOCAL_CHECK.json', summary)
pr.pop('body', None)
save(A / 'ROOT_CANDIDATE05_PRE_REVIEW_GATE.json', {
    'utc': N['utc_now'](), 'result': 'PASS_READONLY_PREPARATION_GATES', 'candidate_revision': 5,
    'freeze_sha256': pin, 'operations_inventory_sha256': context['inventory_sha256'],
    'actual_live_PR': pr, 'fresh_main': parent, 'source_gate': source,
    'all33_actual_Git_disk_archive_verified': True,
    'archive': archive, 'captured_kit_local_check': 'PASS',
    'historical_candidate01_02_03_04_authentication': 'PASS',
    'FP04_and_residual_FP02_OPS_findings_repaired_pending_NEW_full_review05': True,
    'current_paper_and_archive_and_all223_files_byte_identical_to_candidate04': checked['files'] == old['files'],
    'actual_external_mutations': 0, 'acceptance_merge_publication_tracker_native_actions_executed': False})
print(json.dumps({'status': 'FROZEN5_AND_PRE_REVIEW_GATES_PASS', 'freeze_sha256': pin,
                  'operations_inventory_sha256': context['inventory_sha256'],
                  'frozen_files': len(freeze['files']), 'immutable_evidence': len(freeze['evidence_files']),
                  'fresh_main': parent, 'actual_external_mutations': 0}))
