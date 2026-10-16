"""Authenticate sealed review03 and preserve candidate03 before the focused repair.

Root preparation only: no acceptance, remote mutation, or proof-search response.
"""
import sys
if not sys.flags.isolated:
    raise RuntimeError('Use Python -I -B')
from pathlib import Path
import datetime, hashlib, json, shutil, stat

ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_claimed_solved_900_1000_20261012'
A = P / 'audits/pr946_6000001'
D = A / 'preprint'
R = A / 'reviews/full_package_03'
SEAL = '28f08795caf265a412463b3b30880f29bcbc615eb84baf4b92010d1720326370'
FP = 'fdff50b3a1c77523b1b1b7c3da42b2dfdbb1bc17ada7b19abfcbfbbd40d4c505'

def need(test, reason):
    if not test:
        raise RuntimeError(reason)

def read(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'nonregular input: ' + str(path))
    return path.read_bytes()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def obj(path):
    return json.loads(read(path))

def checked(path, want):
    raw = read(path)
    need(len(raw) == want['bytes'] and sha(raw) == want['sha256'], str(path))
    return raw

def save_new(path, value):
    with path.open('x') as handle:
        json.dump(value, handle, indent=2)
        handle.write('\n')

manifest_raw = read(R / 'MANIFEST.json')
need(sha(manifest_raw) == SEAL, 'external review03 seal')
manifest = json.loads(manifest_raw)
need(set(manifest['files']) == set(manifest['explicit_public_allowlist']), 'closed allowlist')
need(set(p.name for p in R.iterdir() if p.name != 'private') ==
     set(manifest['files']) | {'MANIFEST.json'}, 'unexpected public review object')
for name, want in manifest['files'].items():
    need(Path(name).name == name and name not in ('.', '..'), 'unsafe public name')
    checked(R / name, want)
need(len(manifest['files']) == 35, 'review payload count')
result = obj(R / 'RESULT.json')
start = obj(R / 'AUTHENTICATION_START.json')
end = obj(R / 'AUTHENTICATION_END.json')
cold = obj(R / 'COLD_REPLAY.json')
freeze_raw = read(D / 'FREEZE.json')
need(sha(freeze_raw) == FP, 'current candidate03 freeze')
freeze = json.loads(freeze_raw)
need(result['candidate_revision'] == 3 and result['candidate_pins']['freeze'] == FP,
     'corresponding candidate')
need(result['clean_context'] is True and result['full_reproducer_completed'] is True,
     'entire clean-context review')
times = [result['started_utc'], start['utc'], cold['utc'], end['utc'], result['completed_utc']]
need(sorted(datetime.datetime.fromisoformat(t) for t in times) ==
     [datetime.datetime.fromisoformat(t) for t in times], 'review chronology')
for auth in (start, end):
    need(auth['status'] == 'PASS' and auth['freeze_sha256'] == FP, 'authentication status')
    need(auth['candidate_files'] == freeze['files'], 'complete candidate correspondence')
    need(auth['future_helpers'] == freeze['future_helpers'], 'operation correspondence')
    need(auth['operations_inventory_sha256'] == freeze['operations_inventory_sha256'], 'inventory')
    need(auth['live_pr']['headRefOid'] == freeze['original_pr_head'] and
         auth['live_pr']['state'] == 'OPEN' and auth['live_pr']['isDraft'] is True and
         auth['live_pr']['baseRefName'] == 'main', 'live exact-head scope')
    need('| claimed_solved | 4/5 |' in auth['immutable_queue_row'], 'eligible immutable row')
    need(auth['source_gate']['holds'] == [] and auth['source_gate']['related_target_membership'] == {},
         'source holds or related target')
    need(len(auth['originals']) == 33 and auth['disk_and_archive_match'] is True and
         auth['archive_members'] == 220 and auth['evidence_files_verified'] == 34, 'complete evidence')
need(cold['normalized_fields_ignored'] == [] and cold['canonical_receipts_compared_without_deletion'] is True,
     'unedited canonical receipts')
for mode, expected, row in zip(('normal', 'O', 'OO', 'env2'), (0, 1, 2, 2), cold['modes']):
    need(row['mode'] == mode and row['observed_outer_optimization'] == expected and
         row['returncode'] == 0, 'actual four cold modes')
    need(row['receipt'] == obj(D / ('PACKAGE_REPLAY_' + mode + '.json')), 'whole canonical receipt')
    need(row['receipt']['worker_optimization'] == 0, 'diagnostic worker actually normal')
need(len(cold['modes']) == 4, 'exact four modes')
pins = obj(R / 'PRESERVATION_AND_SOURCE_PINS.json')
for relative, want in pins['primary_source_fingerprints'].items():
    checked(A / relative, want)
for name, family in pins['families'].items():
    raw = read(A / 'reviews' / name / 'MANIFEST.json')
    need(sha(raw) == family['manifest_sha256'], 'old family seal')
    mapping = json.loads(raw)
    entries = next(mapping[k] for k in ('files', 'curated_files', 'public_files', 'payloads') if k in mapping)
    entries = entries if isinstance(entries, dict) else {row['path']: row for row in entries}
    for relative, want in entries.items():
        checked(A / 'reviews' / name / relative, want)
    need(len(entries) == family['payloads_authenticated'], 'old family count')
need(result['mathematical_remaining_gap_for_stated_theorem'] is None and
     result['clean_for_preprint'] is False and result['optional_issues'] == [] and
     [v['id'] for v in result['required_issues']] == ['FP03-OPS-001'], 'actual nonclean disposition')
need(len(result['prior_issue_resolution']) == 25 and
     [k for k,v in result['prior_issue_resolution'].items() if v['verified'] is not True] == ['FP02-OPS-001'],
     'honest residual older issue')
for relative, want in freeze['files'].items():
    checked(D / relative, want)
for relative, want in freeze['evidence_files'].items():
    checked(ROOT / relative, want)
inventory_raw = read(A / 'OPERATIONS_INVENTORY.json')
need(sha(inventory_raw) == freeze['operations_inventory_sha256'], 'captured inventory')
inventory = json.loads(inventory_raw)
for relative, want in inventory['files'].items():
    checked(ROOT / relative, want)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
save_new(A / 'ROOT_FULL_REVIEW_03_VERIFICATION.json', {
    'utc': now, 'status': 'AUTHENTICATED_NONCLEAN_REVIEW', 'pr': 946,
    'manifest_sha256': SEAL, 'payloads': 35, 'primary_objects_authenticated': 16,
    'all8_earlier_family_seals_and_payloads_unchanged': True,
    'actual_cold_modes': [0,1,2,2], 'canonical_cold_receipts_exact': True,
    'authentication_start_utc': start['utc'], 'authentication_end_utc': end['utc'],
    'review_completed_utc': result['completed_utc'],
    'required_issues': ['FP03-OPS-001'], 'optional_issues': [], 'mathematical_gap': None,
    'older_FP02_OPS_001_partially_resolved': True, 'all_findings_accepted_for_repair': True,
    'root_read_full_report_result_derivation_primary_review_and_actual31case_control_program': True,
    'root_independent_old_completion_and_already_finalized_defects_reproduced_in_private7case_suite': True,
    'new_proof_responses': 0, 'external_actions': 0})

history = D / 'reviewed_candidates/candidate03'
need(not history.exists(), 'preservation must be new')
history.mkdir()
for relative in freeze['files']:
    src = D / relative
    dest = history / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    dest.chmod(stat.S_IMODE(src.stat().st_mode))
    checked(dest, freeze['files'][relative])
shutil.copyfile(D / 'FREEZE.json', history / 'FREEZE.json')
shutil.copyfile(A / 'OPERATIONS_INVENTORY.json', history / 'OPERATIONS_INVENTORY.json')
for relative, want in inventory['files'].items():
    dest = history / 'operations' / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / relative, dest)
    dest.chmod(stat.S_IMODE((ROOT / relative).stat().st_mode))
    checked(dest, want)
save_new(A / 'CANDIDATE03_PRESERVATION.json', {
    'utc': now, 'status': 'PASS', 'files': len(freeze['files']), 'operation_sources': 7,
    'freeze_sha256': FP, 'history_path': str(history.relative_to(ROOT)),
    'all_historical_bytes_and_modes_preserved': True})
print(json.dumps({'status': 'AUTHENTICATED_AND_PRESERVED', 'review_payloads': 35,
                  'candidate_files': 223, 'operation_sources': 7, 'external_actions': 0}))
