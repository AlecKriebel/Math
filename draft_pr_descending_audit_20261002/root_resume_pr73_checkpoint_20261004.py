"""Verify the audit-only handoff before resuming owned shared writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess

P = Path(__file__).resolve().parent
R = P.parent
D = P / 'private_shared_resume_pr73_checkpoint_20261004'
D.mkdir(exist_ok=False)
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())

def git(*args):
    return subprocess.check_output(['/usr/bin/git', *args], cwd=R, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))

ack = load(P / 'private_shared_pause_pr73_checkpoint_20261004/PAUSE_ACKNOWLEDGEMENT.json')
receipt_path = R / 'draft_pr_publication_program_20260930/audits/pr73_2985/ROOT_mathematical_audit_checkpoint_20261004/RECEIPT.json'
receipt = load(receipt_path)
S = P / 'SHARED_GIT_WINDOW_STATUS.json'
s = load(S)
assert s['shared_git_writes_paused'] and s['paused_for'] == ack['paused_for'] == receipt['actual_ack_tag'] == 'PR73 mathematical-source checkpoint 20261004'
head = git('rev-parse', 'HEAD').decode().strip()
assert head == git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == receipt['audit_checkpoint_commit'] == '4f20301ee01f17de150192852d84c77a4ab51ee6'
assert git('branch', '--show-current') == b'main\n'
assert git('show', '-s', '--format=%P', head).decode().strip() == ack['local_main'] == receipt['parent']
changed = set(git('diff-tree', '--no-commit-id', '--name-only', '-r', head).decode().splitlines())
assert changed == set(receipt['committed_owned_paths']) and len(changed) == 83
assert all(n.startswith('draft_pr_publication_program_20260930/') for n in changed)
assert not git('diff', '--cached', '--raw', '-z')
assert not git('diff', '--name-only', ack['local_main'], head, '--', 'unsolved_math_prioritization')
allowed_live = {'draft_pr_publication_program_20260930/CURRENT_PROGRESS.json', 'draft_pr_publication_program_20260930/audits/pr66_10400033/RESEARCH_LOG.md'}
checks, live = {}, {}
for rel, pin in ack['held_dirty_tracked_bodies_modes'].items():
    p = R / rel
    assert p.is_file() and not p.is_symlink()
    actual = dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes()), mode=format(stat.S_IMODE(p.stat().st_mode), '04o'))
    if rel in allowed_live:
        live[rel] = actual
    else:
        assert actual == pin, 'Held foreign mutation: ' + rel
        checks[rel] = True
assert len(checks) == 9
assert {p.decode() for p in git('diff', '--name-only', '-z').split(b'\0') if p} <= set(ack['held_dirty_tracked_bodies_modes'])
stamp = utc()
result = dict(recorded_utc=stamp, status='PASS_ASCENDING_AUDIT_ONLY_CHECKPOINT_RELEASE_VERIFIED', paused_for=ack['paused_for'], parent=ack['local_main'], local_main=head, remote_main=head, exact_owned_checkpoint_paths=83, held_foreign_body_mode_checks=checks, allowed_ascending_live_current_pins=live, entire_index_empty=True, native_scientific_tree_unchanged=True, receipt_sha256=sha(receipt_path.read_bytes()), receipt_scope='Ownership/index/ref/native-tree verification only; no reading or adjudication of PR73 mathematical conclusions.', outbound_message_sent=False, descending_workflow_percent=55, persistent_goal_complete=False)
(D / 'RESUME_RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n')
s.update(utc=stamp, shared_git_writes_paused=False, resumed_because='Explicit audit-only release independently verified: exact83 ascending-owned paths, unchanged native tree, all9 protected tracked bodies/modes, empty index and matching main remote.', local_main_at_resume=head, remote_main_at_resume=head, dirty_tracked_bodies_modes_frozen_after_acknowledgement=False, native_resume_capture_directory=str(D))
S.write_text(json.dumps(s, indent=2) + '\n')
for p in [P / 'RESEARCH_LOG.md', P / 'audits/pr311_30005303/RESEARCH_LOG.md']:
    with p.open('a') as f:
        f.write('\n' + stamp + ' — PR73 audit-only shared Git window released and independently verified: exact83 ascending-owned paths, native scientific tree unchanged, all9 protected tracked bodies/modes preserved, index empty, local/remote4f20301ee01f17de150192852d84c77a4ab51ee6. Operational ownership review only, no other-status mathematical review and no outbound chat message. PR311 math100%, boundedpriority100%, workflow55%; first full preprint reviewer still finishing, package repairs and second fresh review pending.\n')
print(json.dumps(result, indent=2))
