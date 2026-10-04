#!/usr/bin/env python3
"""Read-only independent PR369 post-merge audit with literal pins and unique runs.

All writes are confined to this post_merge folder. Remote calls are GET only.
Run with the existing audit Python runtime and a fresh --label on every run.
"""
from pathlib import Path, PurePosixPath
import argparse, base64, concurrent.futures, datetime, gzip, hashlib
import json, os, re, subprocess, traceback

OWN = Path(__file__).resolve().parent
AUDIT = OWN.parent.parent
REPO = Path('/Users/alec/Documents/Math')
PYTHON = REPO / 'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
MERGE = 'feec7623f289284c33d685f101342fc74502c819'
MERGED_AT = '2026-10-03T13:22:24Z'
ORIGINAL_MF_SHA = '3abb7304a0875e6d796d97c9bc2b495e181e3ad743e10f797b0ebeceeb9bc698'
LIVE_MF_SHA = 'bf5b94282945a80b06a0a866121929624d984397870946d1ac6e805f5e11af1a'
HEAD = 'f8c075b4018afb91b048e378e884382e8ba3f108'
BASE = '209581a4627b01745974837fe7adab62ab8c0af7'
TREE = '92251767fc944636adb5e7ef0c3d04c677fc870b'
PARENT1 = 'b6de823369765d321a1781032f7e08a557b21fea'
FROZEN = 'd9e4600d05b8272fe913a22ae7dcc0fbe0a26344'
ORIGINAL_BASE = 'efd29c05204703acca9a0860812f54b94fae54b1'
BODY_SHA = '0b63fb68e7155aa9f3ac1168a7ce40d36664b4c978151743da09c65ecfab6ad5'
BASE_QUEUE_SHA = '6318eab1bf5cec094466ca4e4b6a734ed3a705f0f05798fe2eab0520c3f7d7d5'
BRANCH = 'math/2302055-reviewed-liouville-criteria'
PREFIX = 'unsolved_math_prioritization/attempts/2302055/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
CHECKPOINTS = ['6a6164860d7f46a1073babeab9665b3546e2f55d',
               '68c823a4613c38b4af556f9dffbc3d4320aff0b8',
               'd8dab0657462712e7719c3aca697a6c117638586',
               '6e620ae93e637be90f6ea7fd63e4f9cc9346fc46',
               '81b9b389012ec79645c73e8d1196aa6b955fb531']
FAMILIES = ['clean_final_adversary', 'function_theory_review', 'geometric_hypotheses_review']

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--label', required=True, help='Unique run label; existing labels are rejected.')
args = parser.parse_args()
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', args.label):
    parser.error('label must be a safe unique filename component')
RUN = OWN / 'runs' / args.label
PRIVATE = OWN / 'private' / args.label
if RUN.exists() or PRIVATE.exists():
    parser.error('label exists; use a fresh unique label')
RUN.mkdir(parents=True)
PRIVATE.mkdir(parents=True)
checks = []
receipt = {'label': args.label, 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'status': 'RUNNING', 'expected_pins': {'head': HEAD, 'base': BASE, 'tree': TREE,
           'head_ordered_parents': [PARENT1, BASE], 'merge_commit': MERGE,
           'merge_ordered_parents': [BASE, HEAD], 'merged_at': MERGED_AT, 'body_sha256': BODY_SHA,
           'base_queue_sha256': BASE_QUEUE_SHA}, 'checks': checks}

receipt['initial_program_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def blob_sha(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def ck(value, name):
    checks.append({'name': name, 'pass': bool(value)})
    if not value:
        raise AssertionError(name)

def git(*parts):
    return subprocess.check_output(['git', *parts], cwd=REPO)

def get(commit, path):
    return git('show', commit + ':' + path)

def archive(name, raw):
    path = PRIVATE / (name + '.gz')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(raw, mtime=0))
    return {'private_stream': str(path.relative_to(OWN)), 'bytes': len(raw),
            'sha256': sha(raw), 'gzip_bytes': path.stat().st_size}

def api(endpoint, label):
    result = subprocess.run(['gh', 'api', '--method', 'GET', endpoint], cwd=REPO,
                            capture_output=True, timeout=90)
    streams = {'stdout': archive('api/' + label + '.stdout', result.stdout),
               'stderr': archive('api/' + label + '.stderr', result.stderr),
               'returncode': result.returncode, 'endpoint': endpoint}
    if result.returncode or result.stderr:
        raise RuntimeError(json.dumps(streams))
    return json.loads(result.stdout), streams

def local_tree(commit, root):
    result = {}
    for row in git('ls-tree', '-rz', commit, '--', root).split(b'\0'):
        if row:
            meta, path = row.split(b'\t', 1)
            result[path.decode()] = meta.decode().split()
    return result

def local_refs():
    raw = git('for-each-ref', '--format=%(refname) %(objectname)',
              'refs/heads/main', 'refs/remotes/origin/main',
              'refs/heads/' + BRANCH, 'refs/remotes/origin/' + BRANCH)
    return dict(line.split(' ', 1) for line in raw.decode().splitlines())

def preserved_main(commit, phase, kind):
    result = subprocess.run(['git', 'merge-base', '--is-ancestor', MERGE, commit], cwd=REPO, capture_output=True)
    ck(result.returncode == 0 and not result.stderr, phase + ' ' + kind + ' verified descendant of literal merge')
    targets = local_tree(commit, PREFIX)
    ck(targets == local_tree(MERGE, PREFIX), phase + ' ' + kind + ' complete target inventory modes and blobs preserved')
    raw = get(commit, QUEUE)
    rows = [(i + 1, line) for i, line in enumerate(raw.splitlines(keepends=True))
            if len(line.split(b'|')) > 9 and line.split(b'|')[2].strip().split(b' / ')[0] == b'2302055']
    merged_rows = [line for line in get(MERGE, QUEUE).splitlines(keepends=True)
                  if len(line.split(b'|')) > 9 and line.split(b'|')[2].strip().split(b' / ')[0] == b'2302055']
    ck(len(rows) == 1 and len(merged_rows) == 1 and rows[0][1] == merged_rows[0],
       phase + ' ' + kind + ' complete own queue row unchanged from exact merge')
    ck(local_tree(commit, QUEUE)[QUEUE][0:2] == ['100644', 'blob'], phase + ' ' + kind + ' queue mode preserved')
    # Current main can contain independent later work, but it cannot rewrite these published audit records.
    evidence = []
    for family in FAMILIES + ['function_theory_review/provenance_appendix']:
        root = AUDIT / family
        mf = root / 'PUBLIC_MANIFEST.json'
        paths = ['PUBLIC_MANIFEST.json'] + [entry['path'] for entry in json.loads(mf.read_bytes())['files']]
        for rel in paths:
            repo_path = (root / rel).relative_to(REPO).as_posix()
            ck(get(commit, repo_path) == get(BASE, repo_path), phase + ' ' + kind + ' published evidence preserved ' + family + '/' + rel)
            evidence.append(repo_path)
    root_records = ['ROOT_PROVENANCE_CLARIFICATION_RECEIPT.json', 'ROOT_SOURCE_FIRST_SEAL.json', 'ROOT_MATHEMATICAL_SEAL.json']
    for name in ['ROOT_SOURCE_FIRST_SEAL.json', 'ROOT_MATHEMATICAL_SEAL.json']:
        root_records.append(json.loads((AUDIT / name).read_bytes())['file'])
    for rel in root_records:
        repo_path = (AUDIT / rel).relative_to(REPO).as_posix()
        ck(get(commit, repo_path) == get(BASE, repo_path), phase + ' ' + kind + ' root published seal/proof preserved ' + rel)
        evidence.append(repo_path)
    return {'kind': kind, 'commit': commit, 'tree': git('rev-parse', commit + '^{tree}').decode().strip(),
            'merge_ancestry_verified': True, 'target_entries': targets, 'full_queue_sha256': sha(raw),
            'own_queue_physical_row': rows[0][0], 'own_queue_row': rows[0][1].decode().rstrip('\n'),
            'complete_current_queue': archive('current_queue/' + phase + '_' + kind, raw),
            'published_review_paths_preserved': evidence,
            'later_other_problem_queue_changes_permitted': True}

def snapshot(phase):
    pr, pr_stream = api('repos/AlecKriebel/Math/pulls/369', phase + '_pr')
    main, main_stream = api('repos/AlecKriebel/Math/git/ref/heads/main', phase + '_main_ref')
    # Pull-request head is pinned by the closed PR, independent of later branch deletion.
    refs = local_refs()
    merge = subprocess.run(['git', 'rev-parse', '--verify', '--quiet', 'MERGE_HEAD'], cwd=REPO, capture_output=True)
    state = {'utc': now(), 'local_refs': refs, 'symbolic_branch': git('symbolic-ref', '--short', 'HEAD').decode().strip(),
             'remote_main': main['object']['sha'],
             'pr': {k: pr.get(k) for k in ['state', 'draft', 'merged', 'mergeable', 'mergeable_state',
                    'title', 'changed_files', 'additions', 'deletions', 'commits', 'updated_at', 'merge_commit_sha', 'merged_at']},
             'pr_head': pr['head']['sha'], 'pr_base': pr['base']['sha'],
             'pr_head_ref': pr['head']['ref'], 'pr_base_ref': pr['base']['ref'],
             'body_sha256': sha(pr['body'].encode()), 'body_bytes': len(pr['body'].encode()),
             'raw_streams': [pr_stream, main_stream],
             'merge_head': merge.stdout.decode().strip() if merge.returncode == 0 else None}
    receipt[phase] = state
    ck(state['symbolic_branch'] == 'main', phase + ' local branch main')
    ck(state['merge_head'] is None, phase + ' no active foreign or owned merge state')
    ck(state['pr_head'] == HEAD and state['pr_base'] == BASE and
       state['pr_head_ref'] == BRANCH and state['pr_base_ref'] == 'main', phase + ' exact merged PR head base branch names')
    ck(pr['state'] == 'closed' and not pr['draft'] and pr['merged'] is True and
       pr['merge_commit_sha'] == MERGE and pr['merged_at'] == MERGED_AT, phase + ' exact closed ready merged state commit and UTC')
    ck(state['body_sha256'] == BODY_SHA, phase + ' full exact PR body hash')
    ck(pr['changed_files'] == 50, phase + ' fifty changed files')
    state['verified_current_main'] = []
    for kind, commit in [('local_main', refs.get('refs/heads/main')), ('tracking_main', refs.get('refs/remotes/origin/main')),
                         ('remote_main', state['remote_main'])]:
        ck(bool(commit), phase + ' present ' + kind)
        state['verified_current_main'].append(preserved_main(commit, phase, kind))
    remote_commit, stream = api('repos/AlecKriebel/Math/git/commits/' + state['remote_main'], phase + '_current_main_commit')
    ck(remote_commit['sha'] == state['remote_main'] and remote_commit['tree']['sha'] == state['verified_current_main'][-1]['tree'],
       phase + ' actual remote main commit/tree agrees with independently checked local object')
    state['remote_main_commit_stream'] = stream
    return state


def validate_manifest(raw, root_path, commit, label):
    obj = json.loads(raw)
    listed = set()
    rows = []
    for entry in obj['files']:
        rel = PurePosixPath(entry['path'])
        ck(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in listed,
           label + ' safe unique relative path ' + str(rel))
        listed.add(str(rel))
        path = root_path / str(rel)
        data = path.read_bytes()
        repo_path = path.relative_to(REPO).as_posix()
        expected = get(commit, repo_path)
        ck(data == expected and len(data) == entry['bytes'] and sha(data) == entry['sha256'],
           label + ' disk/published Git/size/hash ' + str(rel))
        rows.append({'path': str(rel), 'bytes': len(data), 'sha256': sha(data),
                     'git_blob_sha': blob_sha(data), 'matches': True})
    ck('PUBLIC_MANIFEST.json' not in listed, label + ' self-excluded public manifest')
    return {'label': label, 'manifest_sha256': sha(raw), 'files': rows, 'bound_count': len(rows)}

def check_seal(family, name, packet):
    path = AUDIT / family / name
    obj = json.loads(path.read_bytes())
    ck(path.read_bytes() == get(BASE, path.relative_to(REPO).as_posix()),
       family + ' unchanged published ' + name)
    bindings = []
    if isinstance(obj.get('sha256'), dict):
        bindings.extend(obj['sha256'].items())
    elif obj.get('file') and obj.get('sha256'):
        bindings.append((obj['file'], obj['sha256']))
    for key in ['files', 'own_files']:
        if isinstance(obj.get(key), dict):
            bindings.extend(obj[key].items())
    if obj.get('verdict_file'):
        bindings.append((obj['verdict_file'], obj['verdict_sha256']))
    rows = []
    for rel, digest in bindings:
        raw = (path.parent / rel).read_bytes()
        ck(sha(raw) == digest, family + ' ' + name + ' own sealed binding ' + rel)
        rows.append({'path': rel, 'sha256': digest})
    math = obj.get('turn_math_sha256', obj.get('candidate_math', {}))
    for rel, digest in math.items():
        ck(sha((packet / rel).read_bytes()) == digest,
           family + ' ' + name + ' candidate mathematics binding ' + rel)
    return {'family': family, 'seal': name, 'sha256': sha(path.read_bytes()),
            'sealed_utc': obj.get('sealed_utc'), 'own_bindings': rows,
            'candidate_math_bindings': math}

def replay(label, command, expected_bytes):
    result = subprocess.run(command, cwd=PRIVATE, capture_output=True, timeout=120,
                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    out = archive('replay/' + label + '.stdout', result.stdout)
    err = archive('replay/' + label + '.stderr', result.stderr)
    ck(result.returncode == 0 and not result.stderr, 'replay clean exit ' + label)
    ck(result.stdout == expected_bytes, 'complete byte-exact stdout ' + label)
    return {'label': label, 'exit': result.returncode, 'stdout': out, 'stderr': err,
            'complete_json_output': json.loads(result.stdout)}

try:
    print('Checking exact merged state and independently preserved current-main ancestry.', flush=True)
    receipt['start'] = snapshot('start')
    ck(git('rev-parse', HEAD + '^{tree}').decode().strip() == TREE, 'local exact head tree')
    ck(git('show', '-s', '--format=%P', HEAD).decode().strip().split() == [PARENT1, BASE],
       'local ordered head parents')
    commit, stream = api('repos/AlecKriebel/Math/git/commits/' + HEAD, 'head_commit')
    ck(commit['sha'] == HEAD and commit['tree']['sha'] == TREE and
       [p['sha'] for p in commit['parents']] == [PARENT1, BASE], 'remote ordered parents and exact tree')
    receipt['head_commit'] = {'sha': commit['sha'], 'tree': commit['tree']['sha'],
                              'parents': [p['sha'] for p in commit['parents']], 'stream': stream}
    ck(git('rev-parse', MERGE + '^{tree}').decode().strip() == TREE, 'literal merge exact tree identical audited head')
    ck(git('show', '-s', '--format=%P', MERGE).decode().strip().split() == [BASE, HEAD], 'literal merge exact ordered parents')
    merged, merged_stream = api('repos/AlecKriebel/Math/git/commits/' + MERGE, 'merged_commit')
    ck(merged['sha'] == MERGE and merged['tree']['sha'] == TREE and [p['sha'] for p in merged['parents']] == [BASE, HEAD],
       'actual remote merge commit exact tree and ordered parents')
    receipt['merge_commit'] = {'sha': MERGE, 'tree': TREE, 'ordered_parents': [BASE, HEAD], 'merged_at': MERGED_AT, 'stream': merged_stream}
    paths = git('diff', '--name-only', BASE, MERGE).decode().splitlines()
    trees = local_tree(MERGE, PREFIX)
    frozen_tree = local_tree(FROZEN, PREFIX)
    target_paths = set(trees)
    ck(len(paths) == 50 and set(paths) == target_paths | {QUEUE} and len(target_paths) == 49,
       'entire repository diff exactly forty-nine target files and queue')
    ck(trees == frozen_tree, 'all forty-nine target path mode type and blob entries unchanged')
    receipt['literal_git_scope'] = {'changed_paths': paths, 'target_entries': trees,
                                   'raw_diff': archive('git/full_raw_diff', git('diff', '--raw', '--no-abbrev', BASE, MERGE))}
    packet = PRIVATE / 'packet'
    packet.mkdir()
    for path in sorted(target_paths):
        rel = path.removeprefix(PREFIX)
        out = packet / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        raw = get(MERGE, path)
        ck(raw == get(FROZEN, path) == (AUDIT / 'snapshot' / path).read_bytes(),
           'complete live/frozen/published snapshot bytes ' + rel)
        out.write_bytes(raw)
    # Obtain API modes by traversing nonrecursive trees, preserving complete raw streams as gzip.
    remote_modes = {}
    root, stream = api('repos/AlecKriebel/Math/git/trees/' + TREE, 'root_tree')
    ck(not root.get('truncated', False) and root['sha'] == TREE, 'complete remote root tree')
    queue_meta = None
    node = next(x for x in root['tree'] if x['path'] == 'unsolved_math_prioritization')
    prioritization, _ = api('repos/AlecKriebel/Math/git/trees/' + node['sha'], 'prioritization_tree')
    ck(not prioritization.get('truncated', False), 'complete remote prioritization tree')
    queue_meta = next(x for x in prioritization['tree'] if x['path'] == 'QUEUE.md')
    remote_modes[QUEUE] = queue_meta
    node = next(x for x in prioritization['tree'] if x['path'] == 'attempts')
    attempts, _ = api('repos/AlecKriebel/Math/git/trees/' + node['sha'], 'attempts_tree')
    ck(not attempts.get('truncated', False), 'complete remote attempts tree')
    node = next(x for x in attempts['tree'] if x['path'] == '2302055')
    target, _ = api('repos/AlecKriebel/Math/git/trees/' + node['sha'], 'target_tree')
    ck(not target.get('truncated', False), 'complete remote target tree')
    for entry in target['tree']:
        if entry['type'] == 'blob':
            remote_modes[PREFIX + entry['path']] = entry
        else:
            ck(entry['path'] == 'review' and entry['type'] == 'tree', 'only expected target child tree')
            sub, _ = api('repos/AlecKriebel/Math/git/trees/' + entry['sha'], 'review_tree')
            ck(not sub.get('truncated', False), 'complete remote review tree')
            for leaf in sub['tree']:
                remote_modes[PREFIX + 'review/' + leaf['path']] = leaf
    ck(set(remote_modes) == set(paths), 'complete API tree path inventory exactly fifty')
    files, file_stream = api('repos/AlecKriebel/Math/pulls/369/files?per_page=100', 'all_pr_files')
    ck(len(files) == 50 and {f['filename'] for f in files} == set(paths), 'complete API file diff exactly fifty')
    statuses = {line.split('\t')[1]: line.split('\t')[0]
                for line in git('diff', '--name-status', BASE, MERGE).decode().splitlines()}
    def actual_file(entry):
        name = entry['filename']
        obj, streams = api('repos/AlecKriebel/Math/git/blobs/' + entry['sha'],
                           'blobs/' + name.replace('/', '__'))
        raw = base64.b64decode(obj['content'])
        local = get(MERGE, name)
        mode = remote_modes[name]
        patch = git('diff', '--no-ext-diff', '--no-textconv', '--unified=3', BASE, MERGE, '--', name).decode()
        patch = patch[patch.index('@@'):].rstrip('\n')
        adds = sum(x.startswith('+') and not x.startswith('+++') for x in patch.splitlines())
        dels = sum(x.startswith('-') and not x.startswith('---') for x in patch.splitlines())
        valid = (obj['encoding'] == 'base64' and obj['sha'] == entry['sha'] == blob_sha(raw) == mode['sha']
                 and raw == local and obj['size'] == len(raw) and mode['mode'] == '100644'
                 and mode['type'] == 'blob' and entry['patch'] == patch and entry['additions'] == adds
                 and entry['deletions'] == dels and entry['changes'] == adds + dels
                 and entry['status'] == {'A': 'added', 'M': 'modified'}[statuses[name]])
        return {'path': name, 'bytes': len(raw), 'sha256': sha(raw), 'blob_sha': blob_sha(raw),
                'mode': mode['mode'], 'type': mode['type'], 'status': entry['status'],
                'additions': adds, 'deletions': dels, 'changes': adds + dels,
                'complete_patch_sha256': sha(patch.encode()), 'full_record_fields': sorted(entry),
                'all_actual_blob_patch_mode_fields_match': valid, 'streams': streams}
    rows = list(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(actual_file, files))
    for row in rows:
        ck(row['all_actual_blob_patch_mode_fields_match'], 'complete actual API/Git blob mode patch ' + row['path'])
    receipt['api_files'] = rows
    receipt['api_files_stream'] = file_stream
    # The entire base queue hash and physical row replacement are literal acceptance conditions.
    queue_base = get(BASE, QUEUE)
    ck(sha(queue_base) == BASE_QUEUE_SHA, 'entire exact published base queue hash')
    lines = queue_base.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if len(line.split(b'|')) > 9 and
               line.split(b'|')[2].strip().split(b' / ')[0] == b'2302055']
    ck(matches == [403], 'unique exact physical queue row 404')
    old = lines[403]
    cells = old.split(b'|')
    ck([cells[i].strip() for i in [8, 9]] == [b'queued', b'0/5'], 'exact old own queue cells')
    cells[8:10] = [b' unsolved ', b' 5/5 ']
    lines[403] = b'|'.join(cells)
    repaired = b''.join(lines)
    ck(repaired == get(MERGE, QUEUE), 'entire live queue equals base with only own cells 8 and 9 replaced')
    receipt['queue'] = {'physical_row': 404, 'columns': [8, 9], 'base_sha256': sha(queue_base),
                        'merged_sha256': sha(repaired), 'old_row': old.decode().rstrip('\n'),
                        'new_row': lines[403].decode().rstrip('\n'), 'status': 'unsolved', 'turns': '5/5'}
    # All historical nested bindings and actual checkpoint bytes remain frozen.
    names = ['SOURCE_GATE_MANIFEST.json', *[f'TURN_{i}_MANIFEST.json' for i in range(1, 6)],
             'FINAL_AUTHOR_MANIFEST.json', 'review/REVIEW_MANIFEST.json', 'PUBLICATION_MANIFEST.json']
    manifests = []
    binding_count = 0
    for name in names:
        mf = packet / name
        obj = json.loads(mf.read_bytes())
        seen = set()
        rows = []
        for entry in obj['files']:
            rel = PurePosixPath(entry['path'])
            ck(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in seen,
               'safe unique candidate nested path ' + name + ' ' + str(rel))
            seen.add(str(rel))
            raw = (mf.parent / str(rel)).read_bytes()
            ck(len(raw) == entry['bytes'] and sha(raw) == entry['sha256'],
               'complete nested candidate binding ' + name + ' ' + str(rel))
            rows.append({'path': str(rel), 'bytes': len(raw), 'sha256': sha(raw)})
        binding_count += len(rows)
        manifests.append({'name': name, 'sha256': sha(mf.read_bytes()), 'complete_files': rows})
    ck(binding_count == 211 and len(manifests) == 9, 'nine manifests and all 211 nested binding instances')
    receipt['candidate_manifests'] = manifests
    history = []
    for i, checkpoint in enumerate(CHECKPOINTS, 1):
        parents = git('show', '-s', '--format=%P', checkpoint).decode().strip().split()
        ck(parents == [ORIGINAL_BASE if i == 1 else CHECKPOINTS[i - 2]], 'actual author checkpoint parent ' + str(i))
        mf = f'TURN_{i}_MANIFEST.json'
        obj = json.loads((packet / mf).read_bytes())
        listed = [e['path'] for e in obj['files']] + [mf]
        for rel in listed:
            ck(get(checkpoint, PREFIX + rel) == (packet / rel).read_bytes(),
               'actual historical author checkpoint ' + str(i) + ' ' + rel)
        history.append({'turn': i, 'commit': checkpoint, 'parents': parents,
                        'utc': git('show', '-s', '--format=%cI', checkpoint).decode().strip(),
                        'complete_bound_paths_plus_manifest': listed})
    receipt['actual_author_checkpoints'] = history
    author = json.loads((packet / 'FINAL_AUTHOR_MANIFEST.json').read_bytes())
    for rel in [e['path'] for e in author['files']] + ['FINAL_AUTHOR_MANIFEST.json']:
        ck(get(CHECKPOINTS[-1], PREFIX + rel) == (packet / rel).read_bytes(), 'final forty-file author anchor ' + rel)
    review = json.loads((packet / 'review/REVIEW_MANIFEST.json').read_bytes())
    disposition = json.loads((packet / 'DISPOSITION.json').read_bytes())
    ck(review['author_manifest_sha256'] == sha((packet / 'FINAL_AUTHOR_MANIFEST.json').read_bytes()),
       'historical review exact author-manifest anchor')
    ck(disposition['review_manifest'] == sha((packet / 'review/REVIEW_MANIFEST.json').read_bytes()),
       'historical review exact disposition anchor')
    receipt['historical_review_anchor'] = {'author_manifest_sha256': review['author_manifest_sha256'],
        'review_manifest_sha256': disposition['review_manifest'], 'first_parent_review_donor_claimed': False,
        'qualification': 'Six review files are exact hash-bound frozen records; no earlier independent Git donor review tree is present.'}
    print('Validating published independent families, seals, and honest source chronology.', flush=True)
    family_rows = []
    seal_rows = []
    for family in FAMILIES:
        root = AUDIT / family
        raw = (root / 'PUBLIC_MANIFEST.json').read_bytes()
        ck(raw == get(BASE, (root / 'PUBLIC_MANIFEST.json').relative_to(REPO).as_posix()),
           family + ' original public manifest unchanged from published base')
        family_rows.append(validate_manifest(raw, root, BASE, family))
        for name in ['SOURCE_FIRST_SEAL.json', 'MATHEMATICAL_SEAL.json']:
            seal_rows.append(check_seal(family, name, packet))
    ck(sum(r['bound_count'] for r in family_rows) == 53, 'all original three family manifests and fifty-three files')
    receipt['original_family_manifests'] = family_rows
    receipt['original_family_seals'] = seal_rows
    appendix = AUDIT / 'function_theory_review/provenance_appendix'
    raw = (appendix / 'PUBLIC_MANIFEST.json').read_bytes()
    ck(raw == get(BASE, (appendix / 'PUBLIC_MANIFEST.json').relative_to(REPO).as_posix()),
       'published additive provenance appendix manifest unchanged')
    receipt['provenance_appendix'] = validate_manifest(raw, appendix, BASE, 'additive provenance appendix')
    ck(receipt['provenance_appendix']['bound_count'] == 5, 'all five provenance appendix bindings')
    clarification = json.loads((AUDIT / 'ROOT_PROVENANCE_CLARIFICATION_RECEIPT.json').read_bytes())
    ck(clarification['appendix_manifest_sha256'] == sha(raw) and
       clarification['supplemental_full_source_read_before_math_seal'] is False and
       clarification['supplemental_classical_proof_sealed_before_full_source_read'] is True and
       clarification['candidate_partial_deductions_affected'] is False,
       'honest post-seal full Picard primary chronology preserved without retroactive certification')
    ck((AUDIT / 'ROOT_PROVENANCE_CLARIFICATION_RECEIPT.json').read_bytes() ==
       get(BASE, (AUDIT / 'ROOT_PROVENANCE_CLARIFICATION_RECEIPT.json').relative_to(REPO).as_posix()),
       'root chronology clarification exactly published')
    receipt['root_provenance_clarification'] = clarification
    for name in ['ROOT_SOURCE_FIRST_SEAL.json', 'ROOT_MATHEMATICAL_SEAL.json']:
        obj = json.loads((AUDIT / name).read_bytes())
        ck(sha((AUDIT / obj['file']).read_bytes()) == obj['sha256'] and
           (AUDIT / name).read_bytes() == get(BASE, (AUDIT / name).relative_to(REPO).as_posix()),
           'unchanged root sealed mathematical/source artifact ' + name)
    proof_seal = json.loads((AUDIT / 'ROOT_MATHEMATICAL_SEAL.json').read_bytes())
    ck(proof_seal['prior_source_seal_sha256'] == sha((AUDIT / 'ROOT_SOURCE_FIRST_SEAL.json').read_bytes()),
       'root mathematics seal exact source seal anchor')
    prior = OWN.parent / 'final_live'
    original_raw = (OWN.parent / 'PUBLIC_MANIFEST.json').read_bytes()
    live_raw = (prior / 'PUBLIC_MANIFEST.json').read_bytes()
    ck(sha(original_raw) == ORIGINAL_MF_SHA and len(json.loads(original_raw)['files']) == 19, 'original nineteen manifest literal identity unchanged')
    ck(sha(live_raw) == LIVE_MF_SHA and len(json.loads(live_raw)['files']) == 18, 'prior final_live eighteen manifest literal identity unchanged')
    def local_bound_manifest(root, manifest_name, label):
        raw = (root / manifest_name).read_bytes()
        obj = json.loads(raw)
        rows = []
        seen = set()
        for entry in obj['files']:
            rel = PurePosixPath(entry['path'])
            ck(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in seen and str(rel) != manifest_name,
               label + ' safe unique self-excluded binding ' + str(rel))
            seen.add(str(rel))
            data = (root / str(rel)).read_bytes()
            ck(len(data) == entry['bytes'] and sha(data) == entry['sha256'], label + ' preserved entire binding ' + str(rel))
            rows.append({'path': str(rel), 'bytes': len(data), 'sha256': sha(data)})
        return {'manifest_sha256': sha(raw), 'complete_files': rows}
    receipt['immutable_prior_final_live'] = local_bound_manifest(prior, 'PUBLIC_MANIFEST.json', 'prior final_live18')
    receipt['immutable_prior_live_runs'] = []
    for label in ['agent_20261003_exact_live_01', 'agent_20261003_exact_live_02', 'root_20261003_exact_live_01']:
        oldrun = prior / 'runs' / label
        bindings = local_bound_manifest(oldrun, 'PUBLIC_MANIFEST.json', 'prior uniquely labelled live run ' + label)
        seal = json.loads((oldrun / 'SEAL.json').read_bytes())
        gate = json.loads((oldrun / 'FULL_GATE.json').read_bytes())
        ck(seal['full_gate_sha256'] == sha((oldrun / 'FULL_GATE.json').read_bytes()) and seal['status'] == gate['status'],
           'prior exact-live seal full receipt anchor ' + label)
        expected_status = 'REJECTED' if label == 'agent_20261003_exact_live_01' else 'PASS_EXACT_LIVE'
        ck(gate['status'] == expected_status and (expected_status == 'REJECTED' or gate['check_count'] == 929),
           'retained earlier live acceptance or drift rejection ' + label)
        receipt['immutable_prior_live_runs'].append({'label': label, 'status': gate['status'], 'check_count': gate['check_count'], **bindings})
    chronology = json.loads((appendix / 'SOURCE_ACCESS_CHRONOLOGY.json').read_bytes())
    math_utc = json.loads((AUDIT / 'function_theory_review/MATHEMATICAL_SEAL.json').read_bytes())['sealed_utc']
    events = chronology['events']
    ck(events[1]['utc'] == math_utc and events[2]['before_mathematical_seal'] is False and
       datetime.datetime.fromisoformat(events[3]['utc']) > datetime.datetime.fromisoformat(math_utc) and
       events[0]['independent_local_full_source_receipt_exists'] is False,
       'complete appendix explicit source access chronology agrees with immutable family math seal')
    receipt['complete_source_access_chronology'] = chronology

    # Freshly download all five original primary PDFs; metadata-only public receipt, assets private.
    source_entries = json.loads((packet / 'SOURCE_MANIFEST.json').read_bytes())['sources']
    source_entries += [json.loads((packet / 'SOURCE_ADDITION_T4.json').read_bytes())['source']]
    sources = PRIVATE / 'primary'
    sources.mkdir()
    def fresh_source(entry):
        start = now()
        path = sources / entry['file']
        result = subprocess.run(['curl', '--fail', '--location', '--max-time', '60', '--silent',
                                 '--show-error', entry['url'], '-o', str(path)], capture_output=True)
        stream = archive('sources/' + entry['file'] + '.stderr', result.stderr)
        raw = path.read_bytes() if path.exists() else b''
        return {'file': entry['file'], 'url': entry['url'], 'started_utc': start, 'finished_utc': now(),
                'returncode': result.returncode, 'bytes': len(raw), 'sha256': sha(raw),
                'stderr': stream, 'matches': result.returncode == 0 and not result.stderr and
                len(raw) == entry['bytes'] and sha(raw) == entry['sha256'] and raw.startswith(b'%PDF')}
    source_rows = list(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(fresh_source, source_entries))
    for row in source_rows:
        ck(row['matches'], 'fresh original primary PDF size/hash ' + row['file'])
    receipt['fresh_primary_sources'] = source_rows
    code_paths = [*[f'verify_turn{i}.py' for i in range(1, 6)], 'review/independent_check.py', 'review/replay_author.py']
    code_rows = []
    for rel in code_paths:
        raw = (packet / rel).read_bytes()
        compile(raw, rel, 'exec')
        ck(raw == get(MERGE, PREFIX + rel), 'complete pre-replay audited program exact merged bytes ' + rel)
        code_rows.append({'path': rel, 'bytes': len(raw), 'sha256': sha(raw), 'syntax_valid': True})
    receipt['pre_replay_code_bindings'] = {'utc': now(), 'complete_programs': code_rows,
        'original_all_code_read_before_replay_seal_sha256': sha((OWN.parent / 'CODE_PRE_REPLAY_SEAL.json').read_bytes())}
    runtime = subprocess.run([str(PYTHON), '-B', '-c', 'import json,platform,sympy; print(json.dumps({"python":platform.python_version(),"sympy":sympy.__version__}))'], capture_output=True,
                             env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    ck(runtime.returncode == 0 and not runtime.stderr, 'existing mathematical runtime clean probe')
    receipt['runtime'] = {'path': str(PYTHON), 'versions': json.loads(runtime.stdout),
                          'stdout': archive('runtime/stdout', runtime.stdout), 'stderr': archive('runtime/stderr', runtime.stderr)}
    print('Reproducing all complete outputs in portable no-source and source-present packages.', flush=True)
    replays = []
    for mode in ['no_raw_sources', 'raw_sources_present']:
        if mode == 'raw_sources_present':
            (packet / 'raw_primary').mkdir()
            for entry in source_entries:
                os.link(sources / entry['file'], packet / 'raw_primary' / entry['file'])
        for i in range(1, 6):
            replays.append(replay(mode + '_author' + str(i), [str(PYTHON), '-B', str(packet / f'verify_turn{i}.py')],
                                  (packet / f'TURN_{i}_CHECKS.json').read_bytes()))
        replays.append(replay(mode + '_historical_review', [str(PYTHON), '-B', str(packet / 'review/independent_check.py')],
                              (packet / 'review/INDEPENDENT_CHECKS.json').read_bytes()))
        replays.append(replay(mode + '_author_replay', [str(PYTHON), '-B', str(packet / 'review/replay_author.py'), str(packet)],
                              (packet / 'review/AUTHOR_REPLAY.json').read_bytes()))
    receipt['portable_replays'] = replays
    totals = [sum(r['complete_json_output']['exact_assertions'] for r in replays[j:j + 5]) for j in [0, 7]]
    ck(totals == [38066, 38066] and replays[5]['complete_json_output']['independent_assertions'] == 1420 and
       replays[12]['complete_json_output']['independent_assertions'] == 1420, 'both portable complete stored-output totals')
    control = OWN.parent / 'ADVERSARIAL_CONTROLS.py'
    receipt['own_control_replay'] = replay('own327', [str(PYTHON), '-B', str(control)],
                                          (OWN.parent / 'ADVERSARIAL_CONTROLS_RESULT.json').read_bytes())
    ck(receipt['own_control_replay']['complete_json_output']['assertions'] == 327, 'all original 327 adversarial controls')
    expected_appendix = json.dumps(clarification['verification'], indent=2).encode() + b'\n'
    receipt['appendix_replay'] = replay('appendix_manifest', [str(PYTHON), '-B', str(appendix / 'verify_appendix_manifest.py')], expected_appendix)
    # Fresh end state permits a later main only after independent ancestry and preservation checks.
    receipt['end'] = snapshot('end')
    progression = []
    for kind in ['local_main', 'tracking_main', 'remote_main']:
        start = next(x['commit'] for x in receipt['start']['verified_current_main'] if x['kind'] == kind)
        end = receipt['end']['remote_main'] if kind == 'remote_main' else receipt['end']['local_refs']['refs/heads/main' if kind == 'local_main' else 'refs/remotes/origin/main']
        result = subprocess.run(['git', 'merge-base', '--is-ancestor', start, end], cwd=REPO, capture_output=True)
        ck(result.returncode == 0 and not result.stderr, kind + ' start to end unchanged or verified forward ancestry')
        progression.append({'kind': kind, 'start': start, 'end': end, 'advanced': start != end, 'forward_ancestry_verified': True})
    receipt['main_progression'] = progression
    ck(receipt['start']['body_sha256'] == receipt['end']['body_sha256'], 'exact merged PR body preserved start/end')
    ck(get(BASE, QUEUE) == queue_base and get(MERGE, QUEUE) == repaired, 'complete original merged queue immutable at end')
    ck(sha(Path(__file__).read_bytes()) == receipt['initial_program_sha256'], 'executed post-merge audit program unchanged start/end')
    ck(sha((OWN.parent / 'PUBLIC_MANIFEST.json').read_bytes()) == ORIGINAL_MF_SHA and
       sha((OWN.parent / 'final_live/PUBLIC_MANIFEST.json').read_bytes()) == LIVE_MF_SHA, 'both original manifests immutable at end')
    receipt['status'] = 'PASS_POST_MERGE'

except Exception as exc:
    receipt['status'] = 'REJECTED'
    receipt['error'] = str(exc)
    receipt['exception_type'] = type(exc).__name__
    receipt['traceback'] = traceback.format_exc()
finally:
    receipt['finished_utc'] = now()
    receipt['check_count'] = len(checks)
    receipt['program_sha256'] = sha(Path(__file__).read_bytes())
    streams = []
    for path in sorted(PRIVATE.rglob('*.gz')):
        raw = gzip.decompress(path.read_bytes())
        row = {'private_stream': path.relative_to(OWN).as_posix(), 'bytes': len(raw),
               'sha256': sha(raw), 'gzip_bytes': path.stat().st_size}
        if path.relative_to(PRIVATE).parts[0] == 'api' and '.stdout.gz' in path.name and raw:
            obj = json.loads(raw)
            row['complete_JSON_canonical_sha256'] = sha(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode())
            row['complete_top_level_fields'] = sorted(obj) if isinstance(obj, dict) else None
            row['complete_top_level_items'] = len(obj) if isinstance(obj, list) else None
        streams.append(row)
    receipt['complete_private_stream_inventory'] = streams

    receipt['limits'] = {'original_problem_resolved': False, 'original_problem_resolution_percent': 0,
        'full_Rubel_Squires_Taylor_original_proof_reproduced': False,
        'historical_all_ref_search_reproduced': False, 'novelty_or_current_open_certified': False,
        'general_double_exponential_Liouville_proved': False, 'raw_sources_redistributed': False,
        'new_author_research_turn': False, 'actual_merge_authorized_or_performed_by_gate': False,
        'paper_release_or_DOI_created': False, 'supplemental_full_Picard_source_before_family_math_seal': False}
    (RUN / 'FULL_GATE.json').write_text(json.dumps(receipt, indent=2) + '\n')
    status = receipt['status']
    (RUN / 'REPORT.md').write_text('# PR369 independent post-merge audit\n\n**' + status + '** at ' + receipt['finished_utc'] + '.\n\n' +
        'Literal merged commit ' + MERGE + ', original head ' + HEAD + ', base ' + BASE + ', exact tree ' + TREE +
        ', merge ordered parents [' + BASE + ', ' + HEAD + '], merged at ' + MERGED_AT + ', full body SHA-256 ' + BODY_SHA + '.\n\n' +
        ('Complete actual API/Git bytes, modes and patches for all fifty paths; forty-nine target artifacts unchanged; '
         'entire queue reconstructed from pinned base by changing only physical row 404 cells 8/9 to unsolved 5/5; '
         'all nine candidate manifests/211 bindings and five actual author checkpoints; all 53 original family files '
         'and five additive provenance files/seals against published base; fresh original five primary PDF identities; '
         'fourteen complete portable source/no-source replays plus 327 original controls and appendix verification; '
         'exact merged state/body at start/end; each current main independently checked for merge ancestry and complete result preservation.\n\n' if status == 'PASS_POST_MERGE' else
         'Acceptance rejected: ' + receipt.get('error', 'unknown failure') + '. A fresh unique labelled audit is required after repair.\n\n') +
        'The full original problem remains unresolved. Finite controls are auxiliary. Original full irreducibility proof and '
        'historical exhaustive reference search are not reconstructed; novelty/current-open/human-review certification is absent. '
        'The supplemental Picard primary PDF was fully inspected after its family mathematics seal; the additive chronology '
        'corrects that provenance claim without changing the sealed classical deduction. No original seal/MF, candidate, '
        'Git ref/index/branch, remote service, paper or DOI was changed by this gate. Raw streams/assets remain private and gzip-compressed where applicable.\n')
    (RUN / 'RESEARCH_LOG.md').write_text('# Additive post-merge research log\n\n- ' + receipt['started_utc'] +
        ' — 0% of additive post-merge audit; original frozen/live audits 100%. Began independently after actual merge; original discovery 0%.\n\n- ' +
        receipt['finished_utc'] + ' — ' + ('100% post-merge audit assignment; original discovery 0%.' if status == 'PASS_POST_MERGE' else
        'Post-merge audit rejected; completion estimate80%, acceptance0%. Failed checks retained in FULL_GATE.json.') + '\n')
    seal = {'sealed_utc': now(), 'label': args.label, 'status': status, 'program_sha256': receipt['program_sha256'],
            'full_gate_sha256': sha((RUN / 'FULL_GATE.json').read_bytes()), 'expected_pins': receipt['expected_pins'],
            'original_frozen_manifest_sha256': sha((OWN.parent / 'PUBLIC_MANIFEST.json').read_bytes()),
            'prior_final_live_manifest_sha256': sha((OWN.parent / 'final_live/PUBLIC_MANIFEST.json').read_bytes()),
            'check_count': len(checks)}
    (RUN / 'SEAL.json').write_text(json.dumps(seal, indent=2) + '\n')
    manifest = {'generated_utc': now(), 'own_root': str(RUN), 'self_excluded': 'PUBLIC_MANIFEST.json',
                'excluded': ['PUBLIC_MANIFEST.json'], 'raw_streams_public': False, 'files': []}
    for file in sorted(RUN.iterdir()):
        if file.is_file() and file.name != 'PUBLIC_MANIFEST.json':
            raw = file.read_bytes()
            manifest['files'].append({'path': file.name, 'bytes': len(raw), 'sha256': sha(raw)})
    (RUN / 'PUBLIC_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'label': args.label, 'status': status, 'checks': len(checks),
                      'full_json': str(RUN / 'FULL_GATE.json'), 'seal': str(RUN / 'SEAL.json')}, indent=2))
if receipt['status'] != 'PASS_POST_MERGE':
    raise SystemExit(1)
