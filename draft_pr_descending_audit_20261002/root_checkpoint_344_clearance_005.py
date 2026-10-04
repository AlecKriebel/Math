"""Checkpoint completed clean third PR344 review and root clearance before exact integration."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess
P = Path(__file__).resolve().parent
R = P.parent
A = P / 'audits/pr344_30005649'
PREFIX = 'checkpoint_344_clearance_005'
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def window(): assert not load(P / 'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
assert not (P / (PREFIX + '_receipt.json')).exists()
assert not (P / (PREFIX + '_stage.json')).exists()
progress = load(A / 'ROOT_PRIORITY_ACCEPTANCE.json')
assert progress['math_percent'] == progress['priority_percent'] == 100
assert progress['status'].startswith('PRIORITY_ACCEPTED')
paths = set()
def add(p):
    assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(P)
    assert not any(part.startswith('private_') or part.endswith('_private') or part == '__pycache__' for part in p.relative_to(R).parts)
    paths.add(str(p.relative_to(R)))
for name in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','inventory.json',
             'checkpoint_344_preparation_004_receipt.json',Path(__file__).name]:add(P/name)
for name in ['RESEARCH_LOG.md','CURRENT_PREPRINT_STATUS.json','acceptance_criteria.json',
             'PUBLISHING_CLEARANCE.json','ROOT_PREPRINT_REVIEW03_SEAL.json',
             'ROOT_PREPRINT_REVIEW03_VERIFICATION.json','ROOT_PREPRINT_REVIEW03_NATIVE_COMPARISON.json',
             'ROOT_FINAL_CLOSED_EVIDENCE.json','root_verify_preprint_review03.py',
             'root_clear_submission.py','finalize_publication.py','accepted_pr_body.txt','merge_body.txt']:add(A/name)
for name in ['FULL_PREPRINT_REVIEW.md','READING_LEDGER.md','VERDICT.json','RESEARCH_LOG.md',
             'FINAL_NAMESPACE_MANIFEST.json','SOURCE_ONLY_FREEZE.md','SOURCE_ONLY_FREEZE.pin.json',
             'FIRST_MATHEMATICAL_ASSESSMENT.md','FIRST_MATHEMATICAL_ASSESSMENT.pin.json',
             'candidate_inputs.json','primary_inputs.json','supporting_inputs.json','public_members.json',
             'independent_controls.py','mutation_suite.py','audit_relations.py','verify_review.py']:add(A/'preprint_review_03'/name)
import sys
sys.path.insert(0,str(A))
from root_submission_gate import current_clearance
current_clearance()
assert not (A/'queue_repair_receipt.json').exists()
assert not (A/'ACTUAL_MERGE_ATTEMPT.json').exists()
allow = P / (PREFIX + '_allowlist.json')
paths.add(str(allow.relative_to(R)))
allow.write_text(json.dumps({'utc': utc(), 'paths': sorted(paths), 'math_percent': 100,
                            'priority_percent_estimate': 100, 'workflow_percent': 75,
                            'scope': 'Completed clean third NEW full preprint review selected report/ledger/verdict/code/input/source/member pins and final265-file local namespace manifest; external root14 native replays/complete document and all component stream comparisons, final eight-namespace evidence pins, clearance and current progress. Raw primary/source/render/candidate/receipt bodies remain local; this selected public audit subset is not advertised as a full standalone private audit checkout. The public33-member Zenodo verification ZIP remains self-contained. All eight v04 author inputs unchanged. No author-branch refresh/PR edit/merge/deposit/tracker yet.'}, indent=2) + '\n')
def git(*args):
    return subprocess.check_output(['git', *args], cwd=R, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
assert git('branch', '--show-current') == b'main\n'
assert not git('diff', '--name-only', '--diff-filter=U')
assert not git('diff', '--cached', '--raw', '-z')
assert subprocess.run(['git', 'rev-parse', '-q', '--verify', 'MERGE_HEAD'], cwd=R, capture_output=True).returncode != 0
def foreign():
    entries = {}
    bodies = {}
    for item in git('ls-files', '--stage', '-z').split(b'\0'):
        if item:
            meta, name = item.split(b'\t', 1)
            if name.decode() not in paths: entries.setdefault(name, []).append(meta)
    for name in git('diff', '--name-only', '-z').split(b'\0'):
        if name and name.decode() not in paths:
            f = R / name.decode()
            bodies[name] = {'exists': f.exists(), 'bytes': f.read_bytes() if f.is_file() else None,
                            'mode': f.stat().st_mode & 0o7777 if f.exists() else None}
    return entries, bodies
window()
before = foreign()
parent = git('rev-parse', 'HEAD').decode().strip()
assert parent == '12c8ecfe519fbf1d6f3cb7b35547c39055307341'
assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == parent
for label, argv in [('stage', ['git', 'add', '-f', '--', *sorted(paths)]),
                    ('commit', ['git', 'commit', '--only', '-m', 'Clear repaired PR344 preprint after clean third independent adversary', '--', *sorted(paths)]),
                    ('push', ['git', 'push', 'origin', 'main'])]:
    window()
    start = utc()
    (P / (PREFIX + '_' + label + '_preexecution.json')).write_text(json.dumps({'utc': start, 'argv': argv, 'orchestrator_sha256': sha(Path(__file__).read_bytes())}, indent=2) + '\n')
    proc = subprocess.run(argv, cwd=R, capture_output=True)
    for name, value in [('stdout', proc.stdout), ('stderr', proc.stderr)]:
        (P / (PREFIX + '_' + label + '.' + name)).write_bytes(value)
    (P / (PREFIX + '_' + label + '.json')).write_text(json.dumps({'argv': argv, 'started_utc': start, 'finished_utc': utc(), 'exit_status': proc.returncode, 'stdout_sha256': sha(proc.stdout), 'stderr_sha256': sha(proc.stderr)}, indent=2) + '\n')
    assert proc.returncode == 0, (label, proc.stderr.decode(errors='replace'))
    assert foreign() == before
commit = git('rev-parse', 'HEAD').decode().strip()
changed = set(git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines())
assert changed <= paths
assert git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == commit
for relative in paths:
    f = R / relative
    assert git('show', commit + ':' + relative) == f.read_bytes(), relative
    mode = git('ls-tree', commit, '--', relative).decode().split()[0]
    assert mode == ('100755' if f.stat().st_mode & 0o111 else '100644'), relative
assert not git('diff', '--cached', '--raw', '-z')
rec = {'utc': utc(), 'status': 'PASS_PR344_CLEAN_REVIEW_CLEARANCE_CHECKPOINT_PUSHED',
       'commit': commit, 'parent': parent, 'changed_owned_paths': len(changed), 'allowlist_paths': len(paths),
       'all_allowlisted_git_disk_bytes_modes_equal': True, 'remote_main_exact': True,
       'foreign_index_and_dirty_file_bytes_modes_preserved': True,
       'math_percent': 100, 'priority_percent_estimate': 100, 'workflow_percent': 75,
       'priority_accepted': True, 'pr344_merged_or_published': False, 'persistent_goal_complete': False}
(P / (PREFIX + '_receipt.json')).write_text(json.dumps(rec, indent=2) + '\n')
shared_path = P / 'SHARED_GIT_WINDOW_STATUS.json'
shared = load(shared_path)
shared.update({'utc': utc(), 'last_owned_checkpoint': commit, 'last_owned_checkpoint_pushed': True,
               'descending_git_checkpoint_preparing': False})
shared_path.write_text(json.dumps(shared, indent=2) + '\n')
with (P / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n### ' + utc() + ' — PR344 clean third review and root clearance checkpoint pushed\n\n'
            'Owned commit ' + commit + ' pushed after exact scoped Git/disk body/mode and remote verification. All foreign index and dirty tracked bodies/modes preserved. Mathematics100%, bounded priority review100%, workflow75%; historical first/second reviews remain adverse, B1 and F01/root B2 repaired; third NEW full review and external root closure clean. Every new native component stream reproduced; all v04 author inputs unchanged. Exact integration and production publication remain pending. Historical first priority uncertified. No PR344 merge or publication.\n')
print(json.dumps(rec, indent=2))
