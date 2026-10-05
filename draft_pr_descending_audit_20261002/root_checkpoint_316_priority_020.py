"""Publish completed priority audit; packet and remote correction still pending."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess
P = Path(__file__).resolve().parent
R = P.parent
A = P / 'audits/pr316_9900002'
NAME = 'checkpoint_316_priority_020'
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())
def require(c, m):
    if not c:
        raise RuntimeError(m)
def git(*args):
    return subprocess.check_output(['git', *args], cwd=R,
                                   env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
def window():
    require(not load(P / 'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],
            'Shared Git writes paused')
window()
require(not (P / (NAME + '_stage.json')).exists(), 'Checkpoint already started')
parent = git('rev-parse', 'HEAD').decode().strip()
require(parent == 'aadb7450c957679fc2dac486f1d3b0812fb5a6a2', 'Unexpected parent')
require(git('branch', '--show-current') == b'main\n', 'Not main')
require(git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == parent,
        'Remote differs')
require(not git('diff', '--cached', '--raw', '-z') and
        not git('diff', '--name-only', '--diff-filter=U'), 'Occupied/conflicted index')
accepted = load(A / 'ROOT_PRIORITY_ADJUDICATION.json')
require(accepted['status'] == 'PASS_PR316_CLASSICAL_COROLLARY_PRIORITY_ADJUDICATION'
        and accepted['adjudicated_operational_status'] == 'already_solved'
        and not accepted['paper_authorized'] and not accepted['merge_authorized'],
        'Unexpected adjudication')
stamp = utc()
inventory = load(P / 'inventory.json')
row = next(x for x in inventory['items'] if x['number'] == 316)
row.update(workflow_percent=55, audit_workflow_percent=55,
           mathematical_verification_percent=100, mathematical_acceptance=True,
           bounded_priority_audit_percent=100, priority_adjudication_accepted=True,
           adjudicated_status='already_solved',
           priority_acceptance=False, publication_ready=False,
           original_submitted_status='claimed_solved',
           actual_PR_status_correction_performed=False,
           disposition='classical_corollary_priority_correction_prepared_under_review',
           priority_qualification=accepted['exact_status_qualification'])
(P / 'inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
shared = load(P / 'SHARED_GIT_WINDOW_STATUS.json')
shared.update(utc=stamp, descending_active_pr=316, descending_316_workflow_percent=55,
              descending_316_mathematical_verification_percent=100,
              descending_316_bounded_priority_audit_percent=100,
              descending_git_checkpoint_preparing=True,
              descending_checkpoint_scope='Completed classical-corollary priority audit and fresh adversaries; prepared correction packet and current branch update pending. Operational already_solved; no paper or merge under claimed-only scope.')
(P / 'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared, indent=2) + '\n')
entry = (stamp + ' — PR316 bounded priority audit100%, submitted math100%, workflow55%. '
         'Root read complete independent priority/corollary and both fresh classical '
         'adversarial proofs, independently visually authenticated Erickson1970 '
         'pp265–266 and bound all132 closed priority artifacts/all24 initial pins. '
         'General negative answer is a verified classical consequence; operational '
         'already_solved with no authenticated prior explicit named-problem announcement '
         'and no firstness certificate. Specific lacunary law remains valid and outside '
         'regular variation; its first priority unestablished. Current six-file '
         'correction packet prepared, source-first fresh wrapper reviewer active; '
         'capacity errors retained as service limitations. No branch/status/PR '
         'correction yet, no paper/merge/Zenodo/DOI/tracker action; author1/5 unchanged. '
         'Goal active.\n')
for q in [P / 'RESEARCH_LOG.md', A / 'RESEARCH_LOG.md']:
    with q.open('a') as f:
        f.write('\n' + entry)
owned = [P / n for n in ['RESEARCH_LOG.md', 'SHARED_GIT_WINDOW_STATUS.json',
                         'inventory.json', 'checkpoint_316_math_019_receipt.json',
                         Path(__file__).name]]
owned.extend(A / n for n in [
    'RESEARCH_LOG.md', 'ROOT_CLASSICAL_PRIORITY_FINDING.md',
    'ROOT_PRIORITY_ADJUDICATION.json', 'root_accept_priority.py',
    'ROOT_CORRECTION_REVIEW_SOURCE_GATE.json',
    'root_prepare_priority_correction.py', 'PRIORITY_CORRECTION_PREPARATION.json'])
owned.extend(A / 'priority_correction_packet' / n for n in [
    'CURRENT_PRIORITY_NOTE.md', 'CURRENT_STATUS.json', 'PUBLICATION_MANIFEST.json',
    'README.md', 'PR_BODY.md', 'PR_TITLE.txt'])
owned.extend(A / 'priority_independent' / n for n in [
    'FINAL_PRIORITY_REPORT.md', 'SLOW_VARIATION_COROLLARY.md', 'FINAL_SHA256.json',
    'FREEZE_RECEIPT.json', 'FINAL_VERIFY_RESULT.json', 'FINAL_FREEZE_PROGRAM.py',
    'RESEARCH_LOG.md', 'slow_tail_adversary/report.md',
    'slow_tail_adversary/research_log.md', 'slow_tail_adversary/SHA256SUMS'])
owned.extend(A / 'classical_priority_adversary' / n for n in [
    '00_independent_assessment_frozen.md', 'report.md', 'decision.json',
    'RESEARCH_LOG.md', 'native_run.py', 'retrieve_original.py', 'retrieve_thorisson.py'])
owned.append(A / 'priority_correction_review/INDEPENDENT_SOURCE_CRITERIA.md')
for path, expected in accepted['bound_read_artifacts'].items():
    q = Path(path)
    require(sha(q.read_bytes()) == expected['sha256'] and
            oct(q.stat().st_mode & 0o7777) == expected['mode'], 'Held read artifact changed')
paths = {str(q.relative_to(R)) for q in owned}
allow = P / (NAME + '_allowlist.json')
paths.add(str(allow.relative_to(R)))
for rel in paths - {str(allow.relative_to(R))}:
    require((R / rel).is_file() and not (R / rel).is_symlink(), 'Invalid owned file')
def foreign():
    index, bodies = {}, {}
    for item in git('ls-files', '--stage', '-z').split(b'\0'):
        if item:
            meta, path = item.split(b'\t', 1)
            if path.decode() not in paths:
                index.setdefault(path, []).append(meta)
    for path in git('diff', '--name-only', '-z').split(b'\0'):
        if path and path.decode() not in paths:
            q = R / path.decode()
            bodies[path] = (q.exists(), q.read_bytes() if q.is_file() else None,
                            q.stat().st_mode & 0o7777 if q.exists() else None)
    return index, bodies
before = foreign()
allow.write_text(json.dumps(dict(utc=utc(), paths=sorted(paths),
    scope='Completed priority scientific reports, proof and manifests; primary copyrighted binaries/scans/OCR/raw browse datasets/private runs excluded. Prepared correction is not remotely published. Active correction review excluded except held source-only criteria.',
    current_file_pins={rel: dict(bytes=(R / rel).stat().st_size,
                               sha256=sha((R / rel).read_bytes()),
                               mode=oct((R / rel).stat().st_mode & 0o7777))
                       for rel in sorted(paths) if (R / rel).is_file()},
    mathematical_percent=100, bounded_priority_percent=100, workflow_percent=55),
    indent=2) + '\n')
for phase, argv in [
    ('stage', ['git', 'add', '--', *sorted(paths)]),
    ('commit', ['git', 'commit', '--only', '-m',
                'Adjudicate PR316 classical renewal priority and prepare qualified correction',
                '--', *sorted(paths)]),
    ('push', ['git', 'push', 'origin', 'main'])]:
    window()
    require(foreign() == before, 'Foreign tracked state changed before ' + phase)
    started = utc()
    (P / (NAME + '_' + phase + '_preexecution.json')).write_text(json.dumps(dict(
        utc=started, argv=argv, orchestrator_sha256=sha(Path(__file__).read_bytes())), indent=2) + '\n')
    run = subprocess.run(argv, cwd=R, capture_output=True)
    for stream, body in [('stdout', run.stdout), ('stderr', run.stderr)]:
        (P / (NAME + '_' + phase + '.' + stream)).write_bytes(body)
    (P / (NAME + '_' + phase + '.json')).write_text(json.dumps(dict(
        argv=argv, started_utc=started, ended_utc=utc(), exit_code=run.returncode,
        stdout_sha256=sha(run.stdout), stderr_sha256=sha(run.stderr)), indent=2) + '\n')
    require(run.returncode == 0, phase + ' failed: ' + run.stderr.decode(errors='replace'))
    require(foreign() == before, 'Foreign tracked state changed after ' + phase)
commit = git('rev-parse', 'HEAD').decode().strip()
changed = set(git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines())
require(changed <= paths and git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == commit,
        'Unexpected commit or remote state')
for rel in paths:
    q = R / rel
    require(git('show', commit + ':' + rel) == q.read_bytes(), 'Git byte mismatch')
    require(git('ls-tree', commit, '--', rel).decode().split()[0] ==
            ('100755' if q.stat().st_mode & 0o111 else '100644'), 'Git mode mismatch')
require(not git('diff', '--cached', '--raw', '-z') and foreign() == before,
        'Final index or foreign state differs')
out = dict(utc=utc(), status='PASS_PR316_CLASSICAL_PRIORITY_CHECKPOINT_PUSHED',
           parent=parent, commit=commit, changed_owned_paths=len(changed),
           allowlist_paths=len(paths), all_allowlisted_Git_disk_bytes_modes_equal=True,
           remote_main_exact=True, entire_index_empty=True,
           foreign_index_dirty_tracked_bodies_modes_preserved=True,
           mathematical_percent=100, bounded_priority_percent=100, workflow_percent=55,
           operational_outcome='already_solved_classical_corollary',
           actual_PR_correction_performed=False, paper=False, merge=False,
           zenodo_upload=False, tracker_append=False, persistent_goal_complete=False)
(P / (NAME + '_receipt.json')).write_text(json.dumps(out, indent=2) + '\n')
shared = load(P / 'SHARED_GIT_WINDOW_STATUS.json')
shared.update(utc=utc(), descending_git_checkpoint_preparing=False,
              last_owned_checkpoint=commit, last_owned_checkpoint_pushed=True)
(P / 'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared, indent=2) + '\n')
with (P / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n' + utc() + ' — Completed PR316 classical priority audit pushed ' + commit +
            '; exact scoped Git/disk and remote bindings pass, foreign tracked state '
            'preserved. Math100%, bounded priority100%, workflow55%; fresh prepared '
            'correction review and remote update pending. No paper/merge/publication.\n')
print(json.dumps(out, indent=2))
