"""Publish only owned source-gate/preparation records, preserving every foreign change."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess

P = Path(__file__).resolve().parent
R = P.parent
A = P / 'audits/pr311_30005303'
NAME = 'checkpoint_311_review_gate_027'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
load = lambda p: json.loads(p.read_bytes())
D = P / ('private_' + NAME)
D.mkdir(exist_ok=False)

def req(c, message):
    if not c:
        raise RuntimeError(message)

def git(*args):
    return subprocess.check_output(['/usr/bin/git', *args], cwd=R, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))

def window():
    req(not load(P / 'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'], 'Git window held')

window()
parent = git('rev-parse', 'HEAD').decode().strip()
req(parent == '48c4ff4d14a5bf8dece2bfe0a8cc70b865eba68a' and git('branch', '--show-current') == b'main\n', 'Wrong head/branch')
req(not git('diff', '--cached', '--raw', '-z') and git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == parent, 'Index/remote differs')
req(load(A / 'ROOT_PREPRINT01_SOURCE_GATE.json')['status'] == 'PASS_SOURCE_ONLY_GATE_NAMED_PACKAGE_RELEASE', 'Gate missing')
req(load(A / 'publication_preparation/TRACKER_READ_ONLY_PREFLIGHT.json')['tracker_append_performed'] is False, 'Unexpected tracker write')
req(load(P / 'private_shared_resume_pr66_integration_20261004/RESUME_RECEIPT.json')['status'].startswith('PASS'), 'Resume not checked')

files = [P / n for n in ['RESEARCH_LOG.md', 'SHARED_GIT_WINDOW_STATUS.json', 'checkpoint_311_preprint_026_receipt.json', 'root_pause_pr66_integration_20261004.py', 'root_resume_pr66_integration_20261004.py', Path(__file__).name]]
files += [A / n for n in ['RESEARCH_LOG.md', 'ROOT_PREPRINT01_SOURCE_GATE.json', 'root_release_preprint01.py', 'root_isolate_generated_gws_docs_03.py', 'ROOT_READ_SCOPE_AND_OPERATIONS_03.json']]
files += [A / 'preprint_review_01' / n for n in ['SOURCE_ONLY_CRITERIA.md', 'FIRST_INDEPENDENT_CONCLUSION.md', 'SOURCE_ONLY_FREEZE_MANIFEST.json']]
files += [A / 'publication_preparation' / n for n in ['preflight_tracker_read.py', 'TRACKER_READ_ONLY_PREFLIGHT.json']]
allow = P / (NAME + '_allowlist.json')
paths = {str(p.relative_to(R)) for p in files} | {str(allow.relative_to(R))}

def foreign():
    index, body = {}, {}
    for item in git('ls-files', '--stage', '-z').split(b'\0'):
        if item:
            meta, path = item.split(b'\t', 1)
            if path.decode() not in paths:
                index.setdefault(path, []).append(meta)
    for path in git('diff', '--name-only', '-z').split(b'\0'):
        if path and path.decode() not in paths:
            p = R / path.decode()
            body[path] = (p.exists(), p.read_bytes() if p.is_file() else None, stat.S_IMODE(p.stat().st_mode) if p.exists() else None)
    return index, body

before = foreign()
stamp = utc()
scope = dict(recorded_utc=stamp, status='ROOT_ADDITIONAL_READ_SCOPE_AND_OPERATIONAL_NOTES', mathematical_percent=100, bounded_priority_percent=100, workflow_percent=55, publication_ready=False,
    additional_actual_primary_reads={
        'GMS2006': 'Full appendix proof of Theorem3.1 through A.6, LemmaA.2 and its full proof, plus Theorem3.2 proof paragraphs, in extracted lines1210–1390. Complements ROOT_PRIORITY_READ_SCOPE_02; not the whole paper.',
        'KR2007': 'Full sections2.1–2.2 including normal-form figure/table and flow reparameterization, plus the first paragraph of2.3, extracted lines160–320. Complements earlier download-only scope; not the whole paper.',
        'LUZ2021': 'Publisher header with title, authors, volume49(2021), pages1436–1459.',
        'KS2024': 'Title/author header confirming Thomas Kahle and Seth Sullivant.'},
    read_time_limitation='These body reads occurred before manuscript freeze v01 in the preceding work segment; this is the actual later recording time, not an invented read-start timestamp.',
    additional_web_query_scope='Four targeted MTP2/Ising/closure queries saved in priority_sources_private/web_discovery_007.json; no new mathematical support or universal absence certificate claimed; the full returned response was not root-read.',
    gws_unexpected_generation=dict(command='gws generate-skills --help', effect='CLI generated96 previously untracked documentation files in root skills/ and docs/skills.md instead of showing help.', correction='All96 generated files moved byte/mode-preservingly into owned gws_generated_private_03; tracked files and existing documentation were preserved.', receipt_sha256=sha((A / 'gws_generated_private_03/ISOLATION_RECEIPT.json').read_bytes()), limitation='No reconstructed command start time; generated-file mtimes and native isolation capture retained.'),
    shared_resume=dict(receipt_sha256=sha((P / 'private_shared_resume_pr66_integration_20261004/RESUME_RECEIPT.json').read_bytes()), head=parent, scope='Exact three-commit chain, native remote/index, ownership and eight protected tracked bodies/modes checked; no review of another-status mathematics and no outbound other-chat message.'),
    source_gate=dict(receipt_sha256=sha((A / 'ROOT_PREPRINT01_SOURCE_GATE.json').read_bytes()), reviewer='/root/pr311_preprint_01', full_package_review_complete=False),
    tracker=dict(receipt_sha256=sha((A / 'publication_preparation/TRACKER_READ_ONLY_PREFLIGHT.json').read_bytes()), append_performed=False))
new = A / 'ROOT_READ_SCOPE_AND_OPERATIONS_03.json'
req(not new.exists(), 'Scope record already exists')
new.write_text(json.dumps(scope, indent=2) + '\n')
for p in [P / 'RESEARCH_LOG.md', A / 'RESEARCH_LOG.md']:
    with p.open('a') as f:
        f.write('\n' + stamp + ' — PR311 first preprint source-only gate: full original contribution independently read; complete criteria/first conclusion root-read and26 frozen inputs authenticated before named twelve-file package release at17:49:21.656356UTC. Full fresh review remains active, not cleared. Tracker read-only layout scan passed with zero target matches; no append. Additional primary-body read scopes and isolated CLI documentation-generation mistake recorded honestly. Ascending PR66 integration release independently verified before shared writes resumed. Math100%, boundedpriority100%, workflow55%; no merge/publication clearance.\n')
s = load(P / 'SHARED_GIT_WINDOW_STATUS.json')
s.update(utc=stamp, descending_git_checkpoint_preparing=True, descending_311_preprint_review_01_started=True, descending_311_preprint_review_01_agent='/root/pr311_preprint_01', descending_311_workflow_percent=55, descending_checkpoint_scope='Frozen first-review source-only criteria and named package gate, honest read/operation records and read-only tracker preparation; active reviewer output excluded.')
(P / 'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s, indent=2) + '\n')
req(all(p.is_file() and not p.is_symlink() for p in files), 'Missing/symlink selected file')
allow.write_text(json.dumps(dict(utc=utc(), paths=sorted(paths), pins={str(p.relative_to(R)): dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes()), mode=oct(stat.S_IMODE(p.stat().st_mode))) for p in files}, math_percent=100, bounded_priority_percent=100, workflow_percent=55, publication_ready=False), indent=2) + '\n')
for phase, args in [('stage', ['/usr/bin/git', 'add', '--', *sorted(paths)]), ('commit', ['/usr/bin/git', 'commit', '--only', '-m', 'Checkpoint PR311 source-first preprint review and publication preparation', '--', *sorted(paths)]), ('push', ['/usr/bin/git', 'push', 'origin', 'main'])]:
    window()
    req(foreign() == before, 'Foreign change before ' + phase)
    j = dict(argv=args, cwd=str(R), started_utc=utc(), operator_sha256=sha(Path(__file__).read_bytes()))
    (D / (phase + '_spec.json')).write_text(json.dumps(j, indent=2) + '\n')
    r = subprocess.run(args, cwd=R, capture_output=True)
    for k, b in [('stdout', r.stdout), ('stderr', r.stderr)]:
        (D / (phase + '.' + k)).write_bytes(b)
        j[k + '_bytes'] = len(b)
        j[k + '_sha256'] = sha(b)
    j.update(ended_utc=utc(), exit_code=r.returncode)
    (D / (phase + '_execution.json')).write_text(json.dumps(j, indent=2) + '\n')
    req(r.returncode == 0 and foreign() == before, 'Phase failed or foreign mutation ' + phase)
head = git('rev-parse', 'HEAD').decode().strip()
changed = set(git('diff-tree', '--no-commit-id', '--name-only', '-r', head).decode().splitlines())
req(changed <= paths and git('ls-remote', 'origin', 'refs/heads/main').decode().split()[0] == head, 'Scope/remote mismatch')
req(all(git('show', head + ':' + rel) == (R / rel).read_bytes() for rel in paths), 'Commit body mismatch')
req(not git('diff', '--cached', '--raw', '-z') and foreign() == before, 'Index/foreign mismatch')
j = dict(utc=utc(), status='PASS_PR311_FIRST_PREPRINT_GATE_CHECKPOINT_PUSHED', parent=parent, commit=head, changed_paths=len(changed), allowlist_paths=len(paths), entire_index_empty=True, remote_main_exact=True, foreign_index_body_modes_preserved=True, math_percent=100, bounded_priority_percent=100, workflow_percent=55, preprint_ready=False, immutable_publication_clearance=False, goal_complete=False, captures=str(D))
(P / (NAME + '_receipt.json')).write_text(json.dumps(j, indent=2) + '\n')
s = load(P / 'SHARED_GIT_WINDOW_STATUS.json')
s.update(utc=utc(), descending_git_checkpoint_preparing=False, last_owned_checkpoint=head, last_owned_checkpoint_pushed=True)
(P / 'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s, indent=2) + '\n')
print(json.dumps(j, indent=2))
