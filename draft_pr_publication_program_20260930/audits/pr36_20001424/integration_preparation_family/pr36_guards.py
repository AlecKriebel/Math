"""PR36 future root-owned acceptance guards; import has no write or remote call.

Prepared independently from read-only PR34/35 administrative patterns. All
phase entry points require explicit finalized gate pins. No old gate transfers.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, importlib.util, json, os, re, subprocess, traceback
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
A = HERE.parent
R = A.parents[2]
B = R / 'draft_pr_publication_program_20260930'
C = A / 'reviewed_candidate'
K = R / 'unsolved_math_prioritization/attempts/20001424'
Q = R / 'unsolved_math_prioritization/QUEUE.md'
BASE = B / 'infrastructure/accepted_state_sync'
ID, CODE, PR = '20001424', 'AIM-DYNAMICAL_SYSTEMS-0082', 36
HEAD = '35be7fe58a2832c4d7012cf69c973810fb4c42f8'
ORIGINAL_BASE = '01358d66fc67d1c462bddf31c0d4ee5b120e6737'
CURRENT_SHA = '75d103fcfe2bce2322ff091fea73d0f03c7875b00c7c7af8f6e20ff741a2975c'
DEPENDENCIES_SHA = 'f6b0af0f11ee8aae60678cc37e7cb24373d99484918f893e1a94e9e703d43261'
SNAPSHOT_SHA = 'b1b3fb41892b20e45abfcd5df70cfbfbbaa354da3e5cdb342511282354a47ebc'
LEDGER_SHA = 'b4f2c3a0e24c49c0ead5206efdb5e97f7f3c2099194b6f4c4545fc1bef35cffd'
MIRROR_SHA = 'ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
WRITER_SHA = 'b72afa148d034818cc90fd25b6b084fd94e42604d433a64e09a4ee01ae6e5271'
PREVIOUS = B / 'audits/pr35_2744/state_mirror_bindings.json'
PREVIOUS_SHA = '7e0490b03d35e055a73a5a8f0b4258123004b06886f6db13642db82474ac1769'
ADMIN = {'README.md', 'pr_body.md', 'readiness.json', 'status.json', 'CURRENT_AUDIT_SCOPE.md', 'RESEARCH_LOG.md'}
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def load(path):
    return json.loads(Path(path).read_bytes())

def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n').encode()

def write(path, data, exclusive=False):
    """Durable replacement; an existing staging temporary is never overwritten."""
    path = Path(path)
    require(path.parent.is_dir() and not path.is_symlink(), 'Unsafe output: ' + str(path))
    if exclusive:
        require(not path.exists(), 'Inspect existing receipt before retry: ' + str(path))
    temp = path.with_name(path.name + '.pr36-tmp')
    with temp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def dump(path, value, exclusive=False):
    write(path, encode(value), exclusive)

def git_bytes(*args):
    return subprocess.check_output(['git', *args], cwd=R, timeout=30)

def git(*args):
    return git_bytes(*args).decode().strip()

def remote():
    # Read only. Root performs draft-ready/body/merge/push operations separately.
    value = json.loads(subprocess.check_output(['gh', 'pr', 'view', '36', '--repo', 'AlecKriebel/Math', '--json', 'number,url,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,body'], cwd=R, timeout=30))
    require(value['number'] == PR and value['url'] == 'https://github.com/AlecKriebel/Math/pull/36', 'Wrong remote PR')
    require(value['headRefOid'] == HEAD and value['headRefName'] == 'dot/math-' + ID and value['baseRefName'] == 'main', 'Remote exact-head/base mismatch')
    return value

def relative(name):
    path = PurePosixPath(name)
    require(bool(name) and not path.is_absolute() and '..' not in path.parts, 'Unsafe member: ' + name)
    require(not ({'__pycache__', 'tmp', 'private_tmp', 'private_sources', 'foreign_sources', 'foreign_downloads'} & set(path.parts)), 'Excluded scratch/foreign member: ' + name)
    require(path.suffix not in {'.pyc', '.tmp'}, 'Excluded temporary member')
    return path

def manifest(base, path, expected=None, count=None, exact=True):
    base, path = Path(base), Path(path)
    raw = path.read_bytes()
    if expected:
        require(sha(raw) == expected, 'Pinned manifest changed: ' + str(path))
    obj = json.loads(raw)
    rows = obj['files']
    if isinstance(rows, dict):
        rows = [{'path': k, **v} for k, v in rows.items()]
    require(isinstance(rows, list), 'Unknown manifest schema')
    names = [z['path'] for z in rows]
    require(len(names) == len(set(names)), 'Duplicate manifest members')
    if count is not None:
        require(len(rows) == count, 'Wrong manifest count')
    if 'files_count' in obj:
        require(obj['files_count'] == len(rows), 'Declared manifest count differs')
    for row in rows:
        relative(row['path'])
        child = base / row['path']
        require(child.resolve().is_relative_to(base.resolve()) and child.is_file() and not child.is_symlink(), 'Unsafe/nonregular member: ' + str(child))
        raw = child.read_bytes()
        require(len(raw) == row.get('bytes', row.get('size')) and sha(raw) == row['sha256'], 'Member binding changed: ' + str(child))
        if child.suffix == '.json':
            json.loads(raw)
        elif child.suffix == '.jsonl':
            for line in raw.splitlines():
                json.loads(line)
    if exact:
        actual = {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
        require(not any(p.is_symlink() for p in base.rglob('*')), 'Symlink in frozen package')
        require(path.resolve().is_relative_to(base.resolve()), 'Manifest outside bound package')
        require(set(names) == actual - {str(path.relative_to(base))}, 'Manifest not exact/self-excluding')
    return rows

def add_gate_args(parser):
    parser.add_argument('--execute', action='store_true', help='Root-only explicit execution after finalized gate review')
    parser.add_argument('--whole-manifest', required=True, help='Repository-relative FINAL new whole family self-excluding manifest')
    parser.add_argument('--whole-manifest-sha256', required=True)
    parser.add_argument('--root-final-receipt', required=True, help='Repository-relative FINAL actual root whole reproduction receipt')
    parser.add_argument('--root-final-receipt-sha256', required=True)

def gates(args):
    require(args.execute, 'Prepared only; explicit root --execute required')
    require(git('branch', '--show-current') == 'main', 'Stay on main')
    frozen = manifest(C, C / 'MANIFEST.json', CURRENT_SHA, 60)
    deps = C / 'CURRENT_PROOF_DEPENDENCIES.json'
    require(sha(deps.read_bytes()) == DEPENDENCIES_SHA, 'Frozen dependencies changed')
    d = load(deps)
    require(d['dependency_anchor_repository_relative'] == str(A.relative_to(R)), 'Wrong canonical dependency anchor')
    require(len(d['files']) == 480, 'Require all480 frozen dependencies')
    for z in d['files']:
        p = A / relative(z['path'])
        raw = p.read_bytes()
        require(p.is_file() and not p.is_symlink() and len(raw) == z['bytes'] and sha(raw) == z['sha256'], 'Dependency changed: ' + str(p))
    for pin in [args.whole_manifest_sha256, args.root_final_receipt_sha256]:
        require(re.fullmatch(r'[0-9a-f]{64}', pin) is not None, 'Final review pin must be explicit lowercase SHA256')
    whole = R / relative(args.whole_manifest)
    receipt = R / relative(args.root_final_receipt)
    require(whole.resolve().is_relative_to(A.resolve()) and receipt.resolve().is_relative_to(A.resolve()), 'Final gates must belong to PR36 audit')
    require(whole.parent != C and 'whole' in whole.parent.name.lower(), 'Cannot reuse candidate or old individual-family verdict')
    manifest(whole.parent, whole, args.whole_manifest_sha256)
    require(sha(receipt.read_bytes()) == args.root_final_receipt_sha256, 'Explicit root final receipt pin changed')
    root = load(receipt)
    required = {'status': 'PASS', 'pr': PR, 'problem_id': int(ID), 'original_head': HEAD,
                'reviewed_candidate_manifest_sha256': CURRENT_SHA, 'current_proof_dependencies_sha256': DEPENDENCIES_SHA,
                'whole_manifest_sha256': args.whole_manifest_sha256, 'queue_status': 'already_solved',
                'priority_classification': 'PRIOR_APPLICATION', 'mandatory_corrections': [],
                'entire_current_packet_checked': True, 'root_actual_reproduction': True,
                'original_substantive_attempts': 1, 'new_substantive_attempts': 0, 'verification_attempts_added': 0,
                'paper_or_new_doi_or_tracker': False}
    require(all(root.get(k) == v for k, v in required.items()), 'Final actual root receipt lacks exact complete-gate scope; inspect schema, never fabricate a pass')
    require(sha((A / 'snapshot_manifest.json').read_bytes()) == SNAPSHOT_SHA, 'Original snapshot changed')
    sm = load(A / 'snapshot_manifest.json')
    require(sm['head'] == HEAD and sm['base'] == ORIGINAL_BASE and len(sm['files']) == 16, 'Wrong original scope')
    for z in sm['files']:
        raw = (C / 'original_archive' / relative(z['path'])).read_bytes()
        require(len(raw) == z['size'] and sha(raw) == z['sha256'], 'Original archive altered')
        require(raw == git_bytes('show', HEAD + ':unsolved_math_prioritization/attempts/' + ID + '/' + z['path']), 'Original actual Git bytes differ')
    require(sha((C / 'turns.jsonl').read_bytes()) == LEDGER_SHA, 'Whole original ledger altered')
    records = [json.loads(x) for x in (C / 'turns.jsonl').read_bytes().splitlines()]
    require(len(records) == 1 and records[0]['turn'] == 1 and records[0]['outcome'] == 'candidate' and records[0]['artifact'] == 'CANDIDATE.md', 'Original candidate scope changed')
    require(load(C / 'source_record.json')['problem'] == load(C / 'problem.json'), 'Nested/raw source mismatch')
    require(load(C / 'source_record.json')['upstream_prior_report'] == load(C / 'prior_report.json'), 'Complete prior report changed')
    return frozen, {'reviewed_candidate_manifest_sha256': CURRENT_SHA, 'current_proof_dependencies_sha256': DEPENDENCIES_SHA,
                    'whole_manifest': args.whole_manifest, 'whole_manifest_sha256': args.whole_manifest_sha256,
                    'root_final_receipt': args.root_final_receipt, 'root_final_receipt_sha256': args.root_final_receipt_sha256}

def selected_row(data):
    lines = data.decode().splitlines(keepends=True)
    headers = [x for x in lines if x.startswith('| Rank | ID / code |')]
    require(len(headers) == 1 and [x.strip() for x in headers[0].split('|')[1:-1]] == HEADER, 'Require exact12-column queue')
    rows = [x for x in lines if len(x.split('|')) == 14 and x.split('|')[2].strip() == ID + ' / ' + CODE]
    require(len(rows) == 1, 'Selected numeric/code row absent or ambiguous')
    return rows[0]

def binding(path):
    return {'path': str(Path(path).relative_to(R)), 'sha256': sha(Path(path).read_bytes())}

def merged_overlay_tree(merge, check, queue_bytes):
    """Verify the actual published merge's complete canonical overlay, not just worktree."""
    prefix = 'unsolved_math_prioritization/attempts/' + ID + '/'
    rows = check['canonical_overlay_files']
    names = [z['path'] for z in rows]
    require(len(names) == len(set(names)), 'Duplicate canonical overlay tree binding')
    actual = git_bytes('ls-tree', '-r', '--name-only', merge, '--', prefix).decode().splitlines()
    require(set(actual) == {prefix + x for x in names}, 'Actual merge canonical membership differs from reviewed overlay')
    for z in rows:
        relative(z['path'])
        raw = git_bytes('show', merge + ':' + prefix + z['path'])
        require(len(raw) == z['bytes'] and sha(raw) == z['sha256'], 'Actual merged canonical bytes differ: ' + z['path'])
        mode = git_bytes('ls-tree', merge, '--', prefix + z['path']).decode().split()[0]
        require(mode in {'100644', '100755'}, 'Merged canonical member is not a regular blob')
    require(git_bytes('show', merge + ':unsolved_math_prioritization/QUEUE.md') == queue_bytes, 'Actual published merge queue differs from reviewed named-row overlay')

def load_mirror():
    # Import only occurs during explicitly root-executed mirror/postvalidation.
    path = BASE / 'revision2/accepted_state_sync_v2.py'
    require(sha(path.read_bytes()) == MIRROR_SHA, 'Reviewed mirror implementation changed')
    require(sha((BASE / 'root_apply/guarded_import_v2.py').read_bytes()) == WRITER_SHA, 'Root writer implementation changed')
    spec = importlib.util.spec_from_file_location('pr36_bound_mirror', path)
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    native = mirror.ledger_budget
    def ledger(data, kind, used, limit):
        if kind == 'json_zero_source_triage':
            obj = json.loads(data)
            mirror.require(str(obj.get('problem_id')) == '30002145' and used == obj.get('used') == 0 and limit == obj.get('limit') == 5 and obj.get('substantive_proof_attempts') == [] and isinstance(obj.get('reason'), str) and obj['reason'], 'Invalid preserved PR23 string-ID zero-triage ledger')
        elif kind == 'json_substantive_responses':
            obj = json.loads(data)
            mirror.require(obj.get('problem_id') == 2744 and obj.get('problem_number') == 'KP-1.85' and type(obj.get('substantive_turns_used')) is int and used == obj['substantive_turns_used'] == 1 and limit == obj.get('turn_limit') == 5 and obj.get('outcome') == 'unsolved' and isinstance(obj.get('responses'), list) and [z.get('turn') for z in obj['responses']] == [1] and obj['responses'][0].get('outcome') == 'unsolved' and obj['responses'][0].get('artifact') == 'OBSTRUCTION.md', 'Invalid preserved PR35 original response ledger')
        else:
            native(data, kind, used, limit)
    mirror.ledger_budget = ledger
    return mirror

def run(main):
    try:
        main()
    except Exception:
        # Retain failures inside dedicated helper folder; no silent retry cleanup.
        path = HERE / ('FAILURE_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ') + '.json')
        dump(path, {'utc': stamp(), 'status': 'FAIL', 'traceback': traceback.format_exc(), 'instruction': 'Inspect any intent/staging/output before retry; retain this failure.'}, exclusive=True)
        raise
