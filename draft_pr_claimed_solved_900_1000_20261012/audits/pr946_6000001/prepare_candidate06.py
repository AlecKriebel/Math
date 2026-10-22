"""Authenticate complete sealed review05 and preserve candidate05 without approval."""
import sys
if not sys.flags.isolated or sys.flags.optimize:
    raise RuntimeError('Use Python -I -B at optimization zero')
from pathlib import Path
import argparse, datetime, hashlib, json, shutil, stat

ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_claimed_solved_900_1000_20261012'
A = P / 'audits/pr946_6000001'
D = A / 'preprint'
R = A / 'reviews/full_package_05'
FP = 'adf39584e2645b7b530447523f690ca7e2bf68587c647f7bd5b218b758fa8068'
CORE = '62fa159687104c889195863303fa5642d877e52257bc9e4fb2bc97e89ea2b919'
ap = argparse.ArgumentParser()
ap.add_argument('--review-sha256', required=True)
args = ap.parse_args()

def need(test, why):
    if not test:
        raise RuntimeError(why)

def read(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'Nonregular: ' + str(path))
    return path.read_bytes()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def obj(path):
    return json.loads(read(path))

def checked(path, pin):
    raw = read(path)
    need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], str(path))
    return raw

def save_new(path, value):
    with path.open('x') as handle:
        json.dump(value, handle, indent=2)
        handle.write('\n')

core = P / 'accept_pr946.py'
need(sha(read(core)) == CORE, 'Current candidate05 core changed')
N = {'__name__': '_root_review05_readonly_', '__file__': str(core)}
exec(compile(read(core), str(core), 'exec', dont_inherit=True, optimize=0), N)
need(N['re'].fullmatch('[0-9a-f]{64}', args.review_sha256) is not None,
     'External review pin required')
raw = read(R / 'MANIFEST.json')
need(sha(raw) == args.review_sha256, 'External review05 seal')
manifest = json.loads(raw)
need(set(manifest['files']) == set(manifest['explicit_public_allowlist']), 'Curated closure')
unlisted = set(p.name for p in R.iterdir() if p.name != 'private') - (
    set(manifest['files']) | {'MANIFEST.json'})
need(unlisted == {'REPLAY_' + mode + '.stderr' for mode in ('normal','O','OO','env2')}
     and all(read(R / name) == b'' for name in unlisted),
     'Only explicitly excluded empty replay stderr files may be unlisted')
for name, pin in manifest['files'].items():
    need(Path(name).name == name and name not in ('.', '..'), 'Unsafe review path')
    checked(R / name, pin)
result = obj(R / 'RESULT.json')
start, end = (obj(R / name) for name in ('AUTHENTICATION_START.json', 'AUTHENTICATION_END.json'))
cold = obj(R / 'COLD_REPLAY.json')
N['result_schema'](result)
N['cold_schema'](cold)
freeze_raw = read(D / 'FREEZE.json')
need(sha(freeze_raw) == FP, 'Current freeze05 changed')
freeze = json.loads(freeze_raw)
need(result['candidate_revision'] == 5 and result['candidate_pins']['freeze'] == FP
     and result['clean_context'] is True and result['full_reproducer_completed'] is True,
     'Corresponding complete independent review')
need(result['mathematical_remaining_gap_for_stated_theorem'] is None
     and result['clean_for_preprint'] is False and result['optional_issues'] == []
     and [v['id'] for v in result['required_issues']] == ['FP05-OPS-001', 'FP05-OPS-002'],
     'Actual nonclean disposition')
need(len(result['prior_issue_resolution']) == 28 and
     [k for k,v in result['prior_issue_resolution'].items() if v['verified'] is not True] ==
     ['FP02-OPS-001'], 'Honest residual older contract')
times = [result['started_utc'], start['utc'], cold['utc'], end['utc'], result['completed_utc']]
need([N['utc'](t) for t in times] == sorted(N['utc'](t) for t in times), 'Chronology')
for auth in (start, end):
    N['authentication_schema'](auth)
    need(auth['status'] == 'PASS' and auth['freeze_sha256'] == FP
         and N['exact'](auth['candidate_files'], freeze['files'])
         and N['exact'](auth['future_helpers'], freeze['future_helpers'])
         and type(auth['external_evidence_files']) is int
         and auth['external_evidence_files'] == len(freeze['evidence_files']) == 65
         and auth['operations_inventory_sha256'] == freeze['operations_inventory_sha256'],
         'Complete START/END inventories')
    live = auth['actual_live_pr']
    N['main_destination'](live)
    need(live['isDraft'] is True and N['sha'](live['body'].encode()) == freeze['pr_description_sha256'],
         'Live draft/body custody')
    N['claimed_row'](auth['immutable_queue_row'].encode())
need(cold['normalized_fields_ignored'] == [] and len(cold['modes']) == 4, 'Unedited cold receipts')
for label, opt, row in zip(('normal','O','OO','env2'), (0,1,2,2), cold['modes']):
    need(row['mode'] == label and type(row['observed_outer_optimization']) is int
         and row['observed_outer_optimization'] == opt and row['returncode'] == 0
         and N['exact'](row['receipt'], obj(D / ('PACKAGE_REPLAY_' + label + '.json')))
         and row['receipt']['worker_optimization'] == 0, 'Whole canonical cold receipt')
primary = obj(R / 'PRIMARY_SOURCE_FINGERPRINTS.json')['sources']
for pin in primary:
    checked(A / pin['private_path'], pin)
families = obj(A / 'reviews/full_package_03/PRESERVATION_AND_SOURCE_PINS.json')['families']
for name, family in families.items():
    mb = read(A / 'reviews' / name / 'MANIFEST.json')
    need(sha(mb) == family['manifest_sha256'], 'Old family seal')
    mapping = json.loads(mb)
    records = next(mapping[k] for k in ('files','curated_files','public_files','payloads') if k in mapping)
    records = records if isinstance(records, dict) else {row['path']:row for row in records}
    for relative, pin in records.items():
        checked(A / 'reviews' / name / relative, pin)
    need(len(records) == family['payloads_authenticated'], 'Family count')
context = N['capture_inventory'](freeze['operations_inventory_sha256'])
N['freeze_check'](freeze_raw, FP, context)
N['disposition_check']()
pr, parent, source, originals = N['premerge_gate'](freeze, require_draft=True)
archive = N['archive_check'](freeze, originals)
for auth in (start, end):
    need(set(auth['originals']) == set(originals) and auth['archive_members'] == 220,
         'Entire original and archive inventories')
    for path, want in originals.items():
        got = auth['originals'][path]
        need(all(N['exact'](got.get(k), value) for k,value in want.items())
             and got['archive_mode'] == '100644' and got['disk_and_archive_match'] is True,
             'Actual original Git/disk/ZIP custody')
for number in range(1,5):
    base = D / 'reviewed_candidates' / ('candidate%02d' % number)
    rb = read(base / 'FREEZE.json')
    N['freeze_check'](rb, sha(rb), context, base=base, historical=True)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
save_new(A / 'ROOT_FULL_REVIEW_05_VERIFICATION.json', {
    'utc': now, 'status': 'AUTHENTICATED_COMPLETE_NONCLEAN_REVIEW', 'pr':946,
    'manifest_sha256': args.review_sha256, 'payloads':len(manifest['files']),
    'primary_objects_authenticated':len(primary), 'all8_family_seals_and_payloads_unchanged':True,
    'actual_cold_modes':[0,1,2,2], 'entire_canonical_receipts_exact':True,
    'authentication_start_utc':start['utc'], 'authentication_end_utc':end['utc'],
    'review_completed_utc':result['completed_utc'],
    'required_issues':['FP05-OPS-001','FP05-OPS-002'], 'optional_issues':[], 'mathematical_gap':None,
    'older_FP02_OPS_001_partially_resolved':True, 'FP03_and_FP04_exact_repairs_verified':True,
    'root_read_entire_verdict_derivation_primary_report_and_current79case_service_and_decisive3case_programs':True,
    'root_behavioral_reproduction':'Separate root rebuild required before applying repair',
    'unlisted_empty_replay_stderr_excluded_from_publication':sorted(unlisted),
    'fresh_live_source_main_originals_gate':{'main':parent,'source':source,'status':'PASS'},
    'new_proof_responses':0, 'external_actions':0})
history = D / 'reviewed_candidates/candidate05'
need(not history.exists(), 'Preservation must be new')
history.mkdir()
for relative, pin in freeze['files'].items():
    src, dest = D / relative, history / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    immutable = D / 'reviewed_candidates/candidate04' / relative
    if read(immutable) == read(src):
        dest.hardlink_to(immutable)
    else:
        shutil.copyfile(src, dest)
        dest.chmod(stat.S_IMODE(src.stat().st_mode))
    checked(dest, pin)
for name, src in [('FREEZE.json',D/'FREEZE.json'), ('OPERATIONS_INVENTORY.json',A/'OPERATIONS_INVENTORY.json')]:
    shutil.copyfile(src, history / name)
for relative, pin in context['inventory']['files'].items():
    src, dest = ROOT / relative, history / 'operations' / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    dest.chmod(stat.S_IMODE(src.stat().st_mode))
    checked(dest, pin)
save_new(A / 'CANDIDATE05_PRESERVATION.json', {
    'utc':now,'status':'PASS','files':223,'operation_sources':7,'freeze_sha256':FP,
    'history_path':str(history.relative_to(ROOT)), 'all_historical_bytes_and_modes_preserved':True,
    'unchanged_payloads_linked_only_between_immutable_historical_snapshots':True})
print(json.dumps({'status':'AUTHENTICATED_REVIEW05_AND_PRESERVED5',
                  'review_payloads':len(manifest['files']),'primary_objects':len(primary),
                  'candidate_files':223,'operation_sources':7,'external_actions':0}))
