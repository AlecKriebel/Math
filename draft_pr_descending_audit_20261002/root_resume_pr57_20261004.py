#!/usr/bin/env python3
"""One-shot native verification of the released PR57 ordered publication integration window."""
from pathlib import Path
import datetime, hashlib, json, stat, subprocess
ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_descending_audit_20261002'
OUT = P / 'private_shared_resume_20261004T0525_pr57'
EXPECTED = '5884f4fd1237f66ba6759d59b245f8cdbf0c8afa'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b = p.read_bytes()
    return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b), 'mode': stat.S_IMODE(p.stat().st_mode)}
if OUT.exists(): raise RuntimeError('One-shot capture exists')
OUT.mkdir()
def run(label, argv):
    start = now()
    pre = {'utc': start, 'argv': argv, 'cwd': str(ROOT), 'program': pin(Path(__file__))}
    (OUT / (label + '.preexecution.json')).write_text(json.dumps(pre, indent=2) + '\n')
    proc = subprocess.run(argv, cwd=ROOT, capture_output=True)
    (OUT / (label + '.stdout')).write_bytes(proc.stdout)
    (OUT / (label + '.stderr')).write_bytes(proc.stderr)
    rec = dict(pre, started_utc=start, completed_utc=now(), exit_status=proc.returncode,
               stdout=pin(OUT / (label + '.stdout')), stderr=pin(OUT / (label + '.stderr')))
    (OUT / (label + '.json')).write_text(json.dumps(rec, indent=2) + '\n')
    if proc.returncode: raise RuntimeError(label + ' failed')
    return proc.stdout
branch = run('branch', ['git', 'branch', '--show-current']).decode().strip()
head = run('head', ['git', 'rev-parse', 'HEAD']).decode().strip()
remote = run('remote', ['git', 'ls-remote', 'origin', 'refs/heads/main']).decode().split()[0]
staged = run('staged', ['git', 'diff', '--cached', '--raw', '-z'])
index = run('index', ['git', 'ls-files', '--stage', '-z'])
assert branch == 'main' and head == remote == EXPECTED and not staged
old = json.loads((P / 'private_shared_pause_20261004T0508_pr57/PAUSE_ACKNOWLEDGEMENT.json').read_text())
foreign = {rel: value for rel, value in old['dirty_tracked_body_mode_pins_before_status_acknowledgement'].items()
           if not rel.startswith('draft_pr_descending_audit_20261002/')}
checks = {rel: pin(ROOT / rel) == expected for rel, expected in foreign.items()}
assert len(checks) == 6 and all(checks.values()), checks
rec = {'utc': now(), 'status': 'PR57_ORDERED_PUBLICATION_INTEGRATION_RELEASE_VERIFIED',
       'local_main': head, 'remote_main': remote, 'branch': branch, 'index_empty': True,
       'whole_index_sha256': hashlib.sha256(index).hexdigest(),
       'previous_dirty_foreign_body_mode_checks': checks, 'outbound_message_sent': False,
       'program': pin(Path(__file__))}
(OUT / 'RESUME_RECEIPT.json').write_text(json.dumps(rec, indent=2) + '\n')
path = P / 'SHARED_GIT_WINDOW_STATUS.json'
status = json.loads(path.read_text())
status.update({'utc': now(), 'shared_git_writes_paused': False,
               'resumed_because': 'Explicit ascending PR57 ordered publication integration checkpoint release followed by independently verified exact main/remote, empty whole index and all six preserved prior dirty foreign bodies/modes.',
               'local_main_at_resume': head, 'remote_main_at_resume': remote,
               'all_staged_path_count': 0, 'owned_staged_paths': [],
               'native_resume_capture_directory': str(OUT),
               'dirty_tracked_bodies_modes_frozen_after_acknowledgement': False,
               'ascending_pr57_integration_completed': True,
               'descending_git_checkpoint_preparing': False})
path.write_text(json.dumps(status, indent=2) + '\n')
with (P / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n### ' + now() + ' — PR57 ordered publication integration window released and independently verified\n\n'
            'Native main and remote both ' + head + '; entire index empty; all six prior dirty foreign tracked bodies/modes preserved. Shared owned writes resumed. PR344 mathematics100%, publication workflow30%, and deep priority review remains open. No outbound chat message sent.\n')
print(json.dumps(rec, indent=2))
