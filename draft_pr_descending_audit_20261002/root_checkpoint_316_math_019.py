"""Checkpoint completed PR316 mathematics; priority adjudication remains pending."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess

P = Path(__file__).resolve().parent
R = P.parent
A = P / 'audits/pr316_9900002'
NAME = 'checkpoint_316_math_019'
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda q: json.loads(q.read_bytes())

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def git(*args):
    return subprocess.check_output(['git', *args], cwd=R,
                                   env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))

def window():
    require(not load(P / 'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'],
            'Shared Git writes are paused')

window()
require(not (P / (NAME + '_receipt.json')).exists(), 'Checkpoint already completed')
require(not (P / (NAME + '_stage.json')).exists(), 'Checkpoint already started')
parent = git('rev-parse', 'HEAD').decode().strip()
require(parent == '6a640c407f329e8582791829a8eefbc6bc0b72af', 'Unexpected parent')
require(git('branch', '--show-current') == b'main\n', 'Not main')
require(git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == parent,
        'Remote main differs')
require(not git('diff', '--cached', '--raw', '-z'), 'Index is occupied')
require(not git('diff', '--name-only', '--diff-filter=U'), 'Unmerged paths')
accepted = load(A / 'ROOT_MATHEMATICAL_ACCEPTANCE.json')
require(accepted['mathematical_acceptance'] and not accepted['priority_acceptance'],
        'Unexpected acceptance state')
stamp = utc()
inventory = load(P / 'inventory.json')
row = next(x for x in inventory['items'] if x['number'] == 316)
row.update(workflow_percent=35, audit_workflow_percent=35,
           mathematical_verification_percent=100, mathematical_acceptance=True,
           priority_acceptance=False, publication_ready=False,
           current_priority_obstruction='Classical alpha-zero renewal theorem implies broader no-scale corollary; historical adjudication active',
           fresh_probability_checks=263, fresh_normalization_checks=1773)
(P / 'inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
shared = load(P / 'SHARED_GIT_WINDOW_STATUS.json')
shared.update(utc=stamp, descending_active_pr=316,
              descending_316_workflow_percent=35,
              descending_316_mathematical_verification_percent=100,
              descending_git_checkpoint_preparing=True,
              descending_checkpoint_scope='Completed independently reproduced PR316 mathematical audit; classical priority obstruction provisional, fresh adversaries active. No preprint, merge or publication acceptance.')
(P / 'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared, indent=2) + '\n')
(A / 'README.md').write_text(
    '# Descending adversarial audit: PR316 / 9900002\n\n'
    'Submitted head c96a3b2019ed3d6aabe0612b31491161dcb275e8, '
    'claimed_solved, author1/5. All19 changed objects and18 target files were '
    'authenticated against API/Git/disk and imported full raw source records. '
    'Root reproduced the two author controls and its independent geometric proof. '
    'Two fresh source-first mathematical families passed: independent renewal '
    'concentration and every-scale proper-limit exclusion, with263 and1773 exact '
    'controls reproduced again by root. ROOT_MATHEMATICAL_ACCEPTANCE.json binds '
    'all held reports, programs and actual execution streams. Mathematics100%.\n\n'
    'Current priority audit found an exact broader no-scale consequence of the '
    'alpha-zero classical renewal theorem in Erickson1970. Root visually checked '
    'the relevant original article pages; fresh adversaries are testing the '
    'corollary and historical implications. An old premise and a prior explicit '
    'answer to Thorisson2011 are distinct evidence categories. See '
    'ROOT_CLASSICAL_PRIORITY_FINDING.md for the complete provisional derivation '
    'and access/read qualifications. No priority, preprint, merge, Zenodo or '
    'tracker acceptance for316. Workflow35%; goal active. Full original Thorisson '
    'PDF binary access remains pending; relevant indexed primary text checked. '
    'No outside individual contacted.\n')
entry = (stamp + ' — PR316 meaningful mathematical checkpoint: both fresh '
         'source-first families completed and root independently replayed all263/1773 '
         'controls, read full proofs/code/actual streams and bound every final '
         'artifact. Submitted18 files unchanged, author1/5. Mathematics100%, '
         'workflow35%. Classical Erickson1970 alpha0 theorem, original pp265–266 '
         'visually checked by root, yields a broader no-scale corollary; explicit '
         'historical answer and particular-construction priority remain distinct '
         'unresolved questions. Provisional derivation recorded; fresh adversaries '
         'active. No paper/merge/publication/tracker acceptance. Goal active.\n')
for q in [P / 'RESEARCH_LOG.md', A / 'RESEARCH_LOG.md']:
    with q.open('a') as f:
        f.write('\n' + entry)
owned = [P / n for n in ['RESEARCH_LOG.md', 'SHARED_GIT_WINDOW_STATUS.json',
                         'inventory.json', 'checkpoint_316_initial_018_receipt.json',
                         Path(__file__).name]]
owned.extend(A / n for n in ['README.md', 'RESEARCH_LOG.md',
                             'ROOT_MATHEMATICAL_ACCEPTANCE.json', 'root_accept_math.py',
                             'ROOT_PRIORITY_SOURCE_GATE.json', 'root_priority_fetch.py',
                             'root_lamperti_ocr.py', 'ROOT_CLASSICAL_PRIORITY_FINDING.md'])
for family, pins in accepted['family_pins'].items():
    for name, pin in pins.items():
        q = A / family / name
        require(len(q.read_bytes()) == pin['bytes'] and sha(q.read_bytes()) == pin['sha256']
                and oct(q.stat().st_mode & 0o7777) == pin['mode'],
                'Final mathematical artifact changed: ' + str(q))
        owned.append(q)
# Historical probability source-gate modes were0644; final freeze is0444.
# Compare the early priority assessment's bytes; record current mode independently.
for name, pin in load(A / 'ROOT_PRIORITY_SOURCE_GATE.json')['held_files'].items():
    q = A / 'priority_independent' / name
    require(len(q.read_bytes()) == pin['bytes'] and sha(q.read_bytes()) == pin['sha256'],
            'Early priority freeze bytes changed: ' + name)
    owned.append(q)
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
allow.write_text(json.dumps(dict(
    utc=utc(), paths=sorted(paths), mathematical_percent=100, workflow_percent=35,
    current_file_pins={rel: dict(bytes=(R / rel).stat().st_size,
                               sha256=sha((R / rel).read_bytes()),
                               mode=oct((R / rel).stat().st_mode & 0o7777))
                       for rel in sorted(paths) if (R / rel).is_file()},
    scope='Completed mathematical families and provisional root priority deduction. Active priority/adversary work, primary copyrighted PDFs/scans/text, raw datasets/API objects and private runs excluded. No paper/merge/publication acceptance.'), indent=2) + '\n')
for phase, argv in [
    ('stage', ['git', 'add', '--', *sorted(paths)]),
    ('commit', ['git', 'commit', '--only', '-m',
                'Validate PR316 renewal scaling proof and flag classical priority obstruction',
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
require(changed <= paths, 'Commit escaped allowlist')
require(git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == commit,
        'Remote does not equal checkpoint')
for rel in paths:
    q = R / rel
    require(git('show', commit + ':' + rel) == q.read_bytes(), 'Git byte mismatch')
    mode = '100755' if q.stat().st_mode & 0o111 else '100644'
    require(git('ls-tree', commit, '--', rel).decode().split()[0] == mode, 'Git mode mismatch')
require(not git('diff', '--cached', '--raw', '-z') and foreign() == before,
        'Final index or foreign state changed')
receipt = dict(utc=utc(), status='PASS_PR316_COMPLETED_MATHEMATICAL_CHECKPOINT_PUSHED',
               parent=parent, commit=commit, changed_owned_paths=len(changed),
               allowlist_paths=len(paths), all_allowlisted_Git_disk_bytes_modes_equal=True,
               remote_main_exact=True, entire_index_empty=True,
               foreign_index_dirty_tracked_bodies_modes_preserved=True,
               mathematical_verification_percent=100, workflow_percent=35,
               mathematical_acceptance=True, priority_acceptance=False,
               publication_ready=False, active_priority_and_adversaries_excluded=True,
               persistent_goal_complete=False)
(P / (NAME + '_receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
shared = load(P / 'SHARED_GIT_WINDOW_STATUS.json')
shared.update(utc=utc(), descending_git_checkpoint_preparing=False,
              last_owned_checkpoint=commit, last_owned_checkpoint_pushed=True)
(P / 'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared, indent=2) + '\n')
with (P / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n' + utc() + ' — PR316 mathematical checkpoint pushed ' + commit +
            '; scoped Git/disk bytes/modes and remote exact; foreign tracked index '
            'and dirty bodies/modes preserved. Math100%, workflow35%; priority '
            'adjudication active, no paper/merge/publication acceptance. Goal active.\n')
print(json.dumps(receipt, indent=2))
