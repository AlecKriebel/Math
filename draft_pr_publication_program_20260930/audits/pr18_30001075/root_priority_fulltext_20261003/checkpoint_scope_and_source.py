"""Checkpoint only the dated revised scope and ROOT PR18 source observations."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path('/Users/alec/Documents/Math')
program = repo / 'draft_pr_publication_program_20260930'
scope = program / 'claimed_solved_scope_20261003'
own = program / 'audits/pr18_30001075/root_priority_fulltext_20261003'
audit = own.parent
capture = program / 'audits/pr45_9900007'

def git(*args):
    p = subprocess.run(['git', *args], cwd=repo, capture_output=True, check=True)
    return p.stdout

if git('branch', '--show-current').strip() != b'main':
    raise SystemExit('checkpoint requires main')
base = git('rev-parse', 'HEAD').decode().strip()
ready = json.loads((scope / 'READY.json').read_text())
expected = {Path(x['path']).resolve(): x for x in ready['all_current_payload_files']}
observed = {p.resolve() for p in scope.rglob('*') if p.is_file()}
if observed != set(expected) | {(scope / 'READY.json').resolve()}:
    raise SystemExit('scope payload census changed')
for p, pin in expected.items():
    if not p.is_relative_to(scope) or p.is_symlink():
        raise SystemExit('invalid scope payload path')
    raw = p.read_bytes()
    if len(raw) != pin['bytes'] or hashlib.sha256(raw).hexdigest() != pin['sha256'] or p.stat().st_mode & 0o7777 != pin['full_mode']:
        raise SystemExit('scope payload changed: ' + str(p))
paths = [p.relative_to(repo).as_posix() for p in sorted(observed)]
paths += [p.relative_to(repo).as_posix() for p in sorted(own.iterdir()) if p.is_file()]
paths += [(audit / 'ROOT_RENEWED_MATHEMATICAL_READING_20261003.json').relative_to(repo).as_posix(), (audit / 'RESEARCH_LOG.md').relative_to(repo).as_posix()]
for name in ['root_pr18_supplied_priority_article_extraction_actual_capture', 'root_pr18_supplied_priority_article_render_actual_capture']:
    paths += [p.relative_to(repo).as_posix() for p in sorted((capture / name).iterdir()) if p.is_file()]
paths = sorted(set(paths))
if any(not (repo / p).is_file() or (repo / p).is_symlink() for p in paths):
    raise SystemExit('checkpoint selects only ordinary regular files')
selected = {p.encode() for p in paths}

def foreign_entries():
    entries = []
    for entry in git('ls-files', '--stage', '-z').split(b'\0'):
        if entry and entry.split(b'\t', 1)[1] not in selected:
            entries.append(entry)
    return b'\0'.join(entries)

before = foreign_entries()
work_pins = {p: hashlib.sha256((repo / p).read_bytes()).hexdigest() for p in paths}
if git('rev-parse', 'HEAD').decode().strip() != base:
    raise SystemExit('HEAD changed before staging')
git('add', '--', *paths)
if git('rev-parse', 'HEAD').decode().strip() != base or foreign_entries() != before:
    raise SystemExit('foreign Git state changed before commit; stop')
message = 'Checkpoint claimed-solved scope and complete PR18 priority-source reading'
git('commit', '--only', '-m', message, '--', *paths)
commit = git('rev-parse', 'HEAD').decode().strip()
if git('rev-parse', commit + '^').decode().strip() != base or foreign_entries() != before:
    raise SystemExit('unexpected commit parent or foreign index drift; stop before push')
changed = set(git('diff-tree', '--no-commit-id', '--name-only', '-r', '-z', commit).split(b'\0')) - {b''}
if not changed <= selected:
    raise SystemExit('commit contains unselected paths; stop before push')
if any(hashlib.sha256((repo / p).read_bytes()).hexdigest() != digest for p, digest in work_pins.items()):
    raise SystemExit('selected working file changed; stop before push')
git('push', 'origin', 'main')
remote = git('ls-remote', '--heads', 'origin', 'main').decode().split()[0]
if remote != commit or foreign_entries() != before:
    raise SystemExit('post-push readback or foreign index changed')
print(json.dumps({
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pid': os.getpid(),
    'status': 'PASS_SCOPED_CHECKPOINT', 'base': base, 'commit': commit,
    'remote_main': remote, 'selected_files': len(paths), 'changed_files': len(changed),
    'scope_payload_files_checked': len(observed), 'scope_bytes_checked': sum(p.stat().st_size for p in observed),
    'foreign_index_entries_identical': True, 'foreign_index_sha256': hashlib.sha256(before).hexdigest(),
    'no_native_acceptance_or_publication': True,
    'scope_inventory_percent': 100, 'PR18_publication_workflow_estimate_percent': 60,
    'new_discovery_percent': 0
}, indent=2))
