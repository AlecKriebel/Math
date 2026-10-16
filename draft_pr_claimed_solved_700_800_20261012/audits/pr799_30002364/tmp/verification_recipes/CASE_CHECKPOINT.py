from pathlib import Path
import contextlib, datetime, hashlib, io, json, sys
R = Path('/Users/alec/Documents/Math')
D = R / 'draft_pr_claimed_solved_700_800_20261012'
T = D / 'audits/pr799_30002364/tmp'
M = T / 'root-receipts'
sys.path.insert(0, str(D))
from graphql_scoped_commit import Remote, head_oid, commit_updates
plan = json.loads((T / 'CHECKPOINT_PLAN.json').read_text())
phase = plan['phase']
assert phase.replace('_', '').isalnum()
receiptpath = M / (phase + '_CHECKPOINT_RECEIPT.json')
assert not receiptpath.exists(), 'Reconcile a confirmed checkpoint instead of duplicating it'
updates = {}
for name in ['intake', 'root-receipts', 'verification_recipes']:
    for p in (T / name).rglob('*'):
        if p.is_file():
            assert not p.is_symlink() and p.stat().st_nlink == 1
            updates[p.relative_to(R).as_posix()] = p.read_bytes()
for entry in plan.get('sealed_packets', []):
    folder = T / entry['folder']
    manifest = entry.get('manifest', 'MANIFEST.json')
    assert hashlib.sha256((folder / manifest).read_bytes()).hexdigest() == entry['manifest_sha256']
    assert hashlib.sha256((folder / entry['checker']).read_bytes()).hexdigest() == entry['checker_sha256']
    document = json.loads((folder / manifest).read_text())
    rows = document.get('authored_files', document.get('files'))
    if isinstance(rows, dict):
        rows = [dict(path=n, **({'sha256':v} if isinstance(v,str) else v)) for n,v in rows.items()]
    paths = {x.get('path', x.get('name')) for x in rows} | {manifest, entry['checker']} | set(entry.get('extra_files', []))
    assert len(paths) == entry['files']
    for name in paths:
        assert not Path(name).is_absolute() and all(x not in ('', '.', '..') for x in name.split('/')) and '\\' not in name
        p = folder / name
        assert not p.is_symlink() and p.is_file() and p.stat().st_nlink == 1
        updates[p.relative_to(R).as_posix()] = p.read_bytes()
for name in plan.get('other_safe_files', []) + ['CHECKPOINT_PLAN.json']:
    p = T / name
    assert p.resolve().is_relative_to(T) and not p.is_symlink() and p.is_file() and p.stat().st_nlink == 1
    updates[p.relative_to(R).as_posix()] = p.read_bytes()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
entry = '\n## ' + now + ' — ' + plan['heading'] + '\n\n' + plan['notes'] + '\n\nCase ' + str(plan['case_percent']) + '%; shard ' + str(plan['shard_percent']) + '%.\n'
for attempt in range(3):
    remote = Remote(head_oid())
    u = dict(updates)
    for name in ['RESEARCH_LOG.md', 'audits/pr799_30002364/RESEARCH_LOG.md']:
        path = D.name + '/' + name
        u[path] = remote.read(path) + entry
    state = json.loads(remote.read(D.name + '/STATE.json'))
    assert len(state['processed']) == 11 and state['current_pr'] == 799
    state.update(updated_at=now, current_stage=plan['heading'], overall_completion_estimate_percent=plan['shard_percent'])
    u[D.name + '/STATE.json'] = json.dumps(state, indent=2) + '\n'
    log = remote.read(D.name + '/checkpoint_receipts.jsonl')
    for name in plan.get('previous_receipts', []):
        previous = json.loads((M / name).read_text())
        if not any(json.loads(line).get('commit') == previous['commit'] for line in log.splitlines() if line):
            log += json.dumps(previous) + '\n'
    u[D.name + '/checkpoint_receipts.jsonl'] = log
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        receipt = commit_updates(remote, u, plan['message'])
    (M / (phase + '_CHECKPOINT_RAW.txt')).write_text(out.getvalue())
    if receipt:
        break
else:
    raise RuntimeError('Three main races; checkpoint unconfirmed')
receiptpath.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'commit': receipt['commit'], 'phase': phase, 'case_percent': plan['case_percent'], 'shard_percent': plan['shard_percent']}))
