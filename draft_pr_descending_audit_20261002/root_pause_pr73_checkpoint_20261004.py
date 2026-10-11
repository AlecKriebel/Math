"""Freeze shared writes for the exact incoming audit-checkpoint request."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess

P = Path(__file__).resolve().parent
R = P.parent
D = P / 'private_shared_pause_pr73_checkpoint_20261004'
D.mkdir(exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()

def git(*args):
    return subprocess.check_output(['/usr/bin/git', *args], cwd=R, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))

S = P / 'SHARED_GIT_WINDOW_STATUS.json'
s = json.loads(S.read_bytes())
assert s['shared_git_writes_paused'] is False
head = git('rev-parse', 'HEAD').decode().strip()
remote = git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
assert head == remote == 'a3032109d314f335a2563086c06d9608896a8570'
assert git('branch', '--show-current') == b'main\n'
staged = git('diff', '--cached', '--name-only', '-z').split(b'\0')
staged = [p.decode() for p in staged if p]
assert not staged and not git('diff', '--cached', '--raw', '-z')
before = git('ls-files', '--stage', '-z')
ack = utc()
s.update(utc=ack, shared_git_writes_paused=True,
    paused_for='PR73 mathematical-source checkpoint 20261004',
    reason='Incoming ascending request for an audit-only checkpoint; no PR merge or native QUEUE/state/history write authorized by this window.',
    resume_on='Explicit incoming release followed by independent head/remote/index and held tracked-body/mode verification.',
    outbound_message_sent=False, coordination_channel='Owned shared status acknowledgment; no outbound chat message.',
    descending_mathematical_readonly_review_continues=True,
    all_staged_path_count=len(staged), owned_staged_paths=[],
    local_main_at_pause=head, remote_main_at_pause=remote,
    entire_index_sha256_at_pause=sha(before),
    dirty_tracked_bodies_modes_frozen_after_acknowledgement=True,
    native_pause_capture_directory=str(D))
S.write_text(json.dumps(s, indent=2) + '\n')
held = {}
for n in git('diff', '--name-only', '-z').split(b'\0'):
    if n:
        p = R / n.decode()
        assert p.is_file() and not p.is_symlink()
        held[n.decode()] = dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes()), mode=format(stat.S_IMODE(p.stat().st_mode), '04o'))
assert git('ls-files', '--stage', '-z') == before
assert git('rev-parse', 'HEAD').decode().strip() == head
result = dict(recorded_utc=utc(), status='PASS_SHARED_WRITES_PAUSED_FOR_ASCENDING_AUDIT_CHECKPOINT', acknowledged_utc=ack,
    paused_for=s['paused_for'], local_main=head, remote_main=remote,
    all_staged_path_count=len(staged), entire_index_sha256=sha(before),
    held_dirty_tracked_bodies_modes=held,
    native_scientific_mutation_allowed=False, outbound_message_sent=False,
    descending_workflow_percent=55, persistent_goal_paused=False)
(D / 'PAUSE_ACKNOWLEDGEMENT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
