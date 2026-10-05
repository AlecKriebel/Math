"""Publish only owned completed tracker and provisional research intake artifacts."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess

P = Path(__file__).resolve().parent
R = P.parent
A = P / 'audits/pr356_30001552'
B = P / 'audits/pr364_30004048'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
assert json.loads((B / 'PUBLICATION_RESULT.json').read_bytes())['status'] == 'MERGED_PUBLISHED_AND_TRACKER_VERIFIED'
assert json.loads((A / 'ROOT_FROZEN_GIT_VERIFICATION.json').read_bytes())['status'] == 'PASS_LITERAL_GIT_ALL17_PREVIOUSLY_API_FROZEN_FILES'
assert json.loads((A / 'ROOT_CANDIDATE_REPLAY_RECEIPT.json').read_bytes())['all_program_outputs_compared_byte_for_byte']
paths = set()
def add(p):
    assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
    paths.add(str(p.relative_to(R)))
for p in A.iterdir():
    if p.is_file() and (p.suffix in {'.md', '.json', '.py'} or p.name == '.gitignore'):
        add(p)
for p in (A / 'snapshot').rglob('*'):
    if p.is_file():
        assert p.suffix in {'.md', '.json', '.py'}
        add(p)
for name in ['finalize_tracker.py', 'PUBLICATION_RESULT.json', 'acceptance_criteria.json', 'README.md', 'RESEARCH_LOG.md', 'ACCEPTANCE_DECISION.md']:
    add(B / name)
for name in ['append_tracker.py', 'TRACKER_COMPLETE.json', 'tracker_row_request.json', 'tracker_append_response_execution.json', 'tracker_readback_execution.json', 'README.md']:
    add(B / 'publication' / name)
for name in ['RESEARCH_LOG.md', 'inventory.json', 'STATUS_FILTER_LEDGER.json', 'root_filter_next_claimed.py',
             'SHARED_GIT_WINDOW_STATUS.json', 'checkpoint_359_zenodo_publication_receipt.json', Path(__file__).name]:
    add(P / name)
allow = P / 'checkpoint_364_tracker_356_intake_allowlist.json'
paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc': utc(), 'explicit_owned_paths': sorted(paths),
    'pr364_workflow_percent': 100, 'pr356_mathematical_audit_percent': 75, 'pr356_workflow_percent': 20,
    'scope': 'Completed PR364 first tracker append and provisional exact claimed_solved PR356 intake/reproductions. No excluded-status processing, PR356 promotion, private/copyrighted source publication or concurrent agent namespace writes.'}, indent=2) + '\n')
git = lambda *a: subprocess.check_output(['git', *a], cwd=R)
def window():
    assert not json.loads((P / 'SHARED_GIT_WINDOW_STATUS.json').read_bytes())['shared_git_writes_paused']
assert git('branch', '--show-current') == b'main\n'
assert not git('diff', '--name-only', '--diff-filter=U')
assert subprocess.run(['git', 'rev-parse', '-q', '--verify', 'MERGE_HEAD'], cwd=R, capture_output=True).returncode != 0
def foreign():
    out = {}
    for item in git('ls-files', '--stage', '-z').split(b'\0'):
        if item:
            meta, name = item.split(b'\t', 1)
            if name.decode() not in paths:
                out.setdefault(name, []).append(meta)
    return out
before = foreign()
parent = git('rev-parse', 'HEAD').decode().strip()
assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == parent
for label, args in [('stage', ['git', 'add', '-f', '--', *sorted(paths)]),
                    ('commit', ['git', 'commit', '--only', '-m', 'Complete biconstrained DOI tracker and record antimorphic proof audit intake', '--', *sorted(paths)]),
                    ('push', ['git', 'push', 'origin', 'main'])]:
    window()
    start = utc()
    r = subprocess.run(args, cwd=R, capture_output=True)
    for name, b in [('stdout', r.stdout), ('stderr', r.stderr)]:
        (P / ('checkpoint_364_tracker_356_intake_' + label + '.' + name)).write_bytes(b)
    rec = {'argv': args, 'cwd': str(R), 'started_utc': start, 'completed_utc': utc(), 'exit_code': r.returncode,
           'stdout_bytes': len(r.stdout), 'stdout_sha256': sha(r.stdout), 'stderr_bytes': len(r.stderr), 'stderr_sha256': sha(r.stderr)}
    (P / ('checkpoint_364_tracker_356_intake_' + label + '.json')).write_text(json.dumps(rec, indent=2) + '\n')
    assert r.returncode == 0, (label, r.stderr.decode(errors='replace'))
    assert foreign() == before
commit = git('rev-parse', 'HEAD').decode().strip()
changed = set(git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines())
assert changed <= paths
assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == commit
for path in paths:
    assert git('show', commit + ':' + path) == (R / path).read_bytes(), path
rec = {'utc': utc(), 'status': 'PASS_OWNED_TRACKER_AND_PROVISIONAL_INTAKE_CHECKPOINT_PUSHED_FULL_READBACK',
       'commit': commit, 'parent': parent, 'changed_owned_paths': len(changed), 'allowlist_paths': len(paths),
       'all_allowlisted_git_disk_bytes_equal': True, 'remote_main_exact': True,
       'foreign_staged_entries_preserved': True, 'pr364_workflow_percent': 100,
       'pr356_mathematical_audit_percent': 75, 'pr356_workflow_percent': 20,
       'pr356_priority_and_closed_reviews_pending': True, 'pr356_promoted': False}
(P / 'checkpoint_364_tracker_356_intake_receipt.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps(rec, indent=2))
