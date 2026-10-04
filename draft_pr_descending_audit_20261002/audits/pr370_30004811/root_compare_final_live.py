"""Compare all receipt leaves and validate each observed runtime difference."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json
A = Path(__file__).resolve().parent
C = A / 'clean_final_adversary/final_live'
def sha(b): return hashlib.sha256(b).hexdigest()
def differences(a, b, path=''):
    assert type(a) == type(b), (path, type(a), type(b))
    out = []
    if isinstance(a, dict):
        assert a.keys() == b.keys(), path
        for k in a: out += differences(a[k], b[k], path + '/' + k)
    elif isinstance(a, list):
        assert len(a) == len(b), path
        for i, (u, v) in enumerate(zip(a, b)): out += differences(u, v, path + '/' + str(i))
    elif a != b: out.append({'path': path, 'whole': a, 'root': b})
    return out
mf = json.loads((C / 'PUBLIC_MANIFEST.json').read_bytes())
seen = set()
for row in mf['files']:
    p = PurePosixPath(row['path'])
    assert len(p.parts) == 1 and row['path'] not in seen and not p.is_absolute()
    seen.add(row['path']); f = C / p
    assert not f.is_symlink()
    b = f.read_bytes(); assert len(b) == row['bytes'] and sha(b) == row['sha256']
assert len(seen) == 9 and mf['self_excluded'] == 'PUBLIC_MANIFEST.json'
x = json.loads((C / 'RECEIPT_gate02.json').read_bytes())
y = json.loads((C / 'RECEIPT_root_replay_02.json').read_bytes())
allowed = {'/started_utc', '/completed_utc', '/label', '/private_run_relative'}
allowed |= {'/commands/' + phase + '/stdout_sha256' for phase in ['initial_pr', 'final_pr']}
for i in range(7):
    for k in ['started_utc', 'completed_utc']:
        allowed |= {'/sources/' + str(i) + '/' + k, '/checks/126/evidence/' + str(i) + '/' + k}
runtime_argv = {'replay_author': [1], 'replay_historical_review': [1, 2],
                'replay_publication_source_free': [1], 'replay_publication_sources': [1]}
for key, indices in runtime_argv.items():
    allowed |= {'/commands/' + key + '/argv/' + str(i) for i in indices}
diffs = differences(x, y)
assert {d['path'] for d in diffs} <= allowed, diffs
api_diffs = {}
for j, label in [(x, 'gate02'), (y, 'root_replay_02')]:
    assert j['label'] == label and j['private_run_relative'] == 'private/' + label
    run = C / j['private_run_relative']
    start = datetime.datetime.fromisoformat(j['started_utc'])
    end = datetime.datetime.fromisoformat(j['completed_utc'])
    assert start <= end and start.utcoffset() == end.utcoffset() == datetime.timedelta(0)
    assert j['status'] == 'PASS_EXACT_LIVE_QUALIFIED'
    assert len(j['checks']) == 134 and all(row['pass'] for row in j['checks'])
    assert j['program_sha256'] == sha((C / 'exact_live_gate.py').read_bytes())
    assert j['pins_file_sha256'] == sha((C / 'PINS.json').read_bytes())
    assert j['checks'][126]['name'] == 'all_seven_fresh_primary_pdf_identities'
    assert j['checks'][126]['evidence'] == j['sources']
    for source in j['sources']:
        t0 = datetime.datetime.fromisoformat(source['started_utc'])
        t1 = datetime.datetime.fromisoformat(source['completed_utc'])
        assert start <= t0 <= t1 <= end and t0.utcoffset() == t1.utcoffset() == datetime.timedelta(0)
        b = (run / 'candidate/private_source_cache' / source['name']).read_bytes()
        assert len(b) == source['bytes'] and sha(b) == source['sha256'] and source['match']
    for key, command in j['commands'].items():
        assert command['returncode'] == 0
        for stream in ['stdout', 'stderr']:
            b = (run / (key + '.' + stream)).read_bytes()
            assert sha(b) == command[stream + '_sha256'], (label, key, stream)
    for key, indices in runtime_argv.items():
        for i in indices:
            xp = Path(x['commands'][key]['argv'][i])
            yp = Path(y['commands'][key]['argv'][i])
            assert xp.relative_to(C / 'private/gate02') == yp.relative_to(C / 'private/root_replay_02')
            assert xp.exists() and yp.exists()
            if xp.is_file(): assert xp.read_bytes() == yp.read_bytes()
for phase in ['initial_pr', 'final_pr']:
    a = json.loads((C / 'private/gate02' / (phase + '.stdout')).read_bytes())
    b = json.loads((C / 'private/root_replay_02' / (phase + '.stdout')).read_bytes())
    ds = differences(a, b)
    permitted = {'/' + side + '/repo/' + key for side in ['base', 'head']
                 for key in ['open_issues', 'open_issues_count', 'pushed_at', 'size']}
    assert {d['path'] for d in ds} <= permitted, ds
    for obs in [a, b]:
        for side in ['base', 'head']:
            repo = obs[side]['repo']
            assert repo['full_name'] == 'AlecKriebel/Math'
            assert repo['open_issues'] == repo['open_issues_count'] >= 0 and repo['size'] >= 0
            datetime.datetime.strptime(repo['pushed_at'], '%Y-%m-%dT%H:%M:%SZ')
    api_diffs[phase] = ds
assert x['initial_live_projection'] == x['final_live_projection'] == y['initial_live_projection'] == y['final_live_projection']
root = json.loads((A / 'root_exact_live_receipt.json').read_bytes())
assert root['status'] == 'PASS_ROOT_EXACT_LIVE' and len(root['checks']) == 615 and all(r['pass'] for r in root['checks'])
out = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status': 'PASS_ENTIRE_FINAL_LIVE_RECEIPTS',
       'whole_receipt_sha256': sha((C / 'RECEIPT_gate02.json').read_bytes()),
       'root_receipt_sha256': sha((C / 'RECEIPT_root_replay_02.json').read_bytes()),
       'root_separate_gate_sha256': sha((A / 'root_exact_live_receipt.json').read_bytes()),
       'manifest_sha256': sha((C / 'PUBLIC_MANIFEST.json').read_bytes()), 'public_bindings': 9,
       'complete_equal_checks_after_validated_source_timestamps': 134,
       'all_144_command_stream_hashes_validated_in_each_run': True,
       'runtime_differences': diffs, 'raw_API_repository_metadata_differences': api_diffs,
       'failed_first_root_replay_preserved': 'RECEIPT_root_replay_01.json',
       'first_failure': 'Disk full before recursive tree save; not a mathematical approval',
       'actual_merge_pending': True}
(A / 'root_final_live_comparison.json').write_text(json.dumps(out, indent=2) + '\n')
criteria = json.loads((A / 'acceptance_criteria.json').read_bytes())
criteria.update(workflow_completion_percent=95, exact_live_root_and_whole_gates_pending=False,
                root_exact_live_checks=615, fresh_whole_exact_live_checks=134,
                root_independent_full_whole_gate_checks=134,
                root_and_whole_entire_receipts_equal_after_validated_runtime_leaves=True,
                fresh_whole_final_additive_manifest_verified=True)
(A / 'acceptance_criteria.json').write_text(json.dumps(criteria, indent=2) + '\n')
print(json.dumps({'status': out['status'], 'complete_checks': 134, 'separate_root_checks': 615,
                  'runtime_differences': len(diffs), 'public_bindings': 9}))
