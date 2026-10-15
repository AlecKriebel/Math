#!/usr/bin/env python3
"""Prepare the reviewed PR681 publication using immutable captures and small trees.

Default execution only reads remote state and creates local Git objects/receipts.
Only --push updates the existing PR branch, by an ordinary non-force push. The
shared checkout, selected main branch and index are never written. The exact
23-file attempt is preserved; new material goes in publications/30003703 because
the original verifier deliberately rejects any addition to the attempt itself.
"""
import argparse
import contextlib
import datetime
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
A = Path(__file__).absolute().parent
REPO = A.parents[2]
PR = 681
PROBLEM = '30003703'
BRANCH = 'research/30003703-andreadakis-counterexamples'
ORIGINAL = 'e92320ea5979c812089780a982fbd88136a26522'
PREFIX = 'unsolved_math_prioritization/attempts/30003703/'
PUB_PREFIX = 'unsolved_math_prioritization/publications/30003703/'
QPATH = 'unsolved_math_prioritization/QUEUE.md'
KEY = '30003703 / OWR-15987-013'
TITLE = "Counterexamples to Satoh's SL(2) representation-filtration conjecture"
SNAPSHOT_SHA = '38d15790e96924232a1980c83e3b3881f2af4d83bc39988dd1763f453cc72ff7'
PUB_NAMES = (
    'satoh_filtration_counterexamples.pdf', 'satoh_filtration_counterexamples.tex',
    'satoh_filtration_verification.zip', 'zenodo-deposit.json', 'PACKAGE_README.md',
    'CURRENT_PRIORITY_AND_STATUS.md', 'CLAIM_SCOPE.json', 'requirements.txt',
    'verify_package.py', 'build_package.py',
)
UPLOAD_NAMES = ('satoh_filtration_counterexamples.pdf', 'satoh_filtration_verification.zip')
FALSE_FLAGS = (
    'degree5_rank3_claim', 'every_degree_failure_claim', 'SLm_m_gt2_claim',
    'character_algebra_claim', 'ordinary_IA_LCS_conjecture_claim',
    'new_PI_identity_claim', 'new_general_PI_method_claim',
    'historical_firstness_claim', 'exhaustive_novelty_clearance',
    'current_literature_openness_certified', 'formal_proof_certificate',
    'AI_reviews_are_human_peer_review',
)
EXPECTED_SCOPE = {
    'problem_id': PROBLEM, 'original_pr': PR, 'original_head': ORIGINAL,
    'claim': 'explicit_counterexamples_to_2018_component_filtration_equality',
    'degree5_rank_min': 4, 'degree6_rank_min': 3,
    'component_algebra': 'rational_SL2_matrix_entry_functions',
    'A_uses_integral_free_group_LCS': True, 'D_acts_on_whole_J_quotient': True,
    'classical_identity_explicitly_credited': True,
    **{flag: False for flag in FALSE_FLAGS},
    'AI_tools_used_extensively': True, 'unrefereed': True,
}
HELPER_NAMES = ('prepare_integration.py', 'record_tracker.py')
GATE_NAMES = ('MATH_SOURCE_GATE_ACCEPTANCE.json', 'PRIORITY_GATE_ACCEPTANCE.json')
GIT_ENV = None
ACCEPTANCE = A / 'ACCEPTED_PUBLICATION_INPUTS.json'
PUSH_INTENT = A / 'INTEGRATION_PUSH_INTENT.json'
PUSHED_RECEIPT = A / 'INTEGRATION_PUSHED_RECEIPT.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def parse_json(data):
    return json.loads(data, object_pairs_hook=unique_pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def valid_doi(doi):
    require(type(doi) is str and re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*', doi), 'invalid Zenodo DOI')
    return doi


def safe_name(name):
    require(type(name) is str, 'path must be a string')
    path = PurePosixPath(name)
    require(bool(name) and not path.is_absolute() and '..' not in path.parts
            and path.as_posix() == name and name != '.' and '\\' not in name and ':' not in name
            and all(ord(c) >= 32 and ord(c) != 127 for c in name), 'unsafe file path: ' + name)
    return name


def regular_bytes(path):
    """Open every path component without following links, then capture once."""
    path = Path(path).absolute()
    require(path.is_absolute(), 'input must be absolute')
    directory = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for name in path.parts[1:-1]:
            next_fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | getattr(os, 'O_NOFOLLOW', 0), dir_fd=directory)
            os.close(directory); directory = next_fd
        fd = os.open(path.name, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0), dir_fd=directory)
        with os.fdopen(fd, 'rb') as stream:
            before = os.fstat(stream.fileno())
            require(stat.S_ISREG(before.st_mode), 'input is not a regular file: ' + str(path))
            data = stream.read()
            after = os.fstat(stream.fileno())
            require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
                    == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns)
                    and len(data) == before.st_size, 'input changed during capture: ' + str(path))
            return data
    finally:
        os.close(directory)


# Bind the source actually captured by the tracker loader; never import pyc.
EXECUTED_SOURCE_SHA256 = globals().get('_CAPTURED_SOURCE_SHA256') or sha(regular_bytes(Path(__file__).absolute()))


def timestamp(value, label):
    require(type(value) is str, label + ' timestamp must be text')
    try:
        parsed = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        raise ValueError(label + ' timestamp malformed')
    require(parsed.tzinfo is not None and parsed.utcoffset() == datetime.timedelta(0), label + ' timestamp must be UTC')
    return parsed


def file_pin(data):
    return {'bytes': len(data), 'sha256': sha(data)}


def valid_pin(record):
    return (type(record) is dict and set(record) == {'bytes', 'sha256'}
            and type(record['bytes']) is int and record['bytes'] >= 0
            and type(record['sha256']) is str and re.fullmatch('[0-9a-f]{64}', record['sha256']) is not None)


def helper_pins():
    pins = {name: sha(regular_bytes(A / name)) for name in HELPER_NAMES}
    require(pins['prepare_integration.py'] == EXECUTED_SOURCE_SHA256,
            'executed integration source differs from current reviewed source')
    return pins


def write_json(path, value):
    """Atomic, durable receipt; no silently reused temporary path or symlink."""
    path = Path(path)
    require(not path.is_symlink() and path.parent.is_dir() and not path.parent.is_symlink(), 'unsafe receipt path')
    temporary = path.with_name(path.name + '.tmp')
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(json_bytes(value)); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        if temporary.exists() and not temporary.is_symlink():
            temporary.unlink()
        raise


@contextlib.contextmanager
def action_lock(name):
    """Serialize this PR's local operator processes without touching Git's index."""
    path = A / name
    fd = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    try:
        require(stat.S_ISREG(os.fstat(fd).st_mode), 'operation lock is not a regular file')
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        os.close(fd)


def git(*args, input=None):
    """Git writes are confined to an isolated object database; never use an index."""
    require(args and args[0] in {'symbolic-ref', 'rev-parse', 'remote', 'ls-remote', 'fetch', 'show',
            'ls-tree', 'diff', 'mktree', 'hash-object', 'commit-tree', 'push'}, 'unsupported Git operation')
    if args[0] in {'fetch', 'mktree', 'hash-object', 'commit-tree', 'push'}:
        require(GIT_ENV is not None, 'Git object writes require isolated object storage')
    environment = dict(os.environ)
    for name in list(environment):
        if name in {'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY',
                    'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_COMMON_DIR', 'GIT_NAMESPACE',
                    'GIT_QUARANTINE_PATH', 'GIT_CONFIG_PARAMETERS'} or name.startswith('GIT_CONFIG_'):
            environment.pop(name, None)
    environment['GIT_OPTIONAL_LOCKS'] = '0'
    if GIT_ENV is not None:
        environment.update(GIT_ENV)
    return subprocess.check_output(['git', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false',
        '-c', 'core.hooksPath=/dev/null', '-c', 'fetch.writeCommitGraph=false',
        '-c', 'fetch.prune=false', '-c', 'fetch.pruneTags=false', '-c', 'submodule.recurse=false',
        '-c', 'push.recurseSubmodules=no', '-c', 'commit.gpgsign=false', '-c', 'push.gpgsign=false', *args],
                                   cwd=REPO, input=input, stderr=subprocess.PIPE, env=environment, timeout=180)


@contextlib.contextmanager
def isolated_objects(directory):
    global GIT_ENV
    require(GIT_ENV is None, 'nested Git object contexts are forbidden')
    require(git('rev-parse', '--is-shallow-repository').decode().strip() == 'false',
            'shallow repositories are unsupported: never update shared shallow metadata')
    original_objects = Path(git('rev-parse', '--git-path', 'objects').decode().strip())
    if not original_objects.is_absolute(): original_objects = REPO / original_objects
    require(original_objects.is_dir() and not original_objects.is_symlink(), 'repository object store invalid')
    objects = Path(directory) / 'objects'; objects.mkdir()
    require(not objects.is_symlink(), 'temporary object store linked')
    GIT_ENV = {'GIT_OBJECT_DIRECTORY': str(objects.absolute()),
               'GIT_ALTERNATE_OBJECT_DIRECTORIES': str(original_objects.absolute())}
    try:
        yield str(objects.absolute())
    finally:
        GIT_ENV = None


def origin_url(push=False):
    arguments = ('remote', 'get-url', '--push', '--all', 'origin') if push else ('remote', 'get-url', '--all', 'origin')
    urls = git(*arguments).decode().splitlines()
    allowed = {'https://github.com/AlecKriebel/Math.git', 'https://github.com/AlecKriebel/Math',
               'git@github.com:AlecKriebel/Math.git', 'git@github.com:AlecKriebel/Math'}
    require(len(urls) == 1 and urls[0] in allowed, 'origin must have one exact selected GitHub repository URL')
    return urls[0]


def remote_oid(ref):
    require(ref in {'refs/heads/main', 'refs/heads/' + BRANCH}, 'unexpected remote reference')
    lines = git('ls-remote', '--exit-code', origin_url(), ref).decode().splitlines()
    require(len(lines) == 1, 'remote reference must identify exactly one object')
    fields = lines[0].split()
    require(len(fields) == 2 and fields[1] == ref and re.fullmatch('[0-9a-f]{40}', fields[0]), 'remote object malformed')
    return fields[0]


def fetch_main():
    """Fetch exact advertised objects without updating FETCH_HEAD or any ref."""
    base = remote_oid('refs/heads/main')
    require(remote_oid('refs/heads/' + BRANCH) == ORIGINAL, 'remote PR branch changed before fetch')
    for oid in dict.fromkeys((base, ORIGINAL)):
        git('fetch', '--no-write-fetch-head', '--no-tags', '--no-recurse-submodules', '--refmap=', origin_url(), oid)
        require(git('rev-parse', oid + '^{commit}').decode().strip() == oid, 'fetched commit identity differs')
    require(remote_oid('refs/heads/main') == base, 'remote main advanced during isolated fetch; prepare again')
    require(remote_oid('refs/heads/' + BRANCH) == ORIGINAL, 'remote PR branch advanced during isolated fetch')
    return base, {'exact_advertised_objects_fetched': True, 'FETCH_HEAD_and_all_shared_refs_untouched': True,
                  'isolated_object_store_only': True, 'no_shared_git_cleanup_or_automatic_fetch_retry': True}


def pr_metadata():
    return parse_json(subprocess.check_output(
        ['gh', 'pr', 'view', str(PR), '--json',
         'number,state,isDraft,baseRefName,headRefOid,headRefName,headRepositoryOwner,isCrossRepository'], cwd=REPO, timeout=120))


def check_known_head(meta):
    """Run before reading any live candidate, frozen attempt or paper contents."""
    require(meta.get('number') == PR and meta.get('state') == 'OPEN' and meta.get('isDraft') is True,
            'selected PR must remain the open draft PR681')
    require(meta.get('baseRefName') == 'main' and meta.get('headRefName') == BRANCH,
            'selected PR branch/base differs')
    require(meta.get('isCrossRepository') is False
            and meta.get('headRepositoryOwner', {}).get('login') == 'AlecKriebel', 'unexpected head repository')
    require(meta.get('headRefOid') == ORIGINAL, 'unreviewed PR head; abort before reading or overwriting files')
    return ORIGINAL


def queue_row(data):
    require(type(data) is bytes, 'queue must be captured bytes')
    rows = data.splitlines(keepends=True)
    matches = []
    for i, line in enumerate(rows):
        cells = line.rstrip(b'\r\n').split(b'|')
        if len(cells) > 2 and cells[2].strip() == KEY.encode():
            matches.append((i, line, cells))
    require(len(matches) == 1, 'queue must contain exactly one selected problem row')
    i, line, cells = matches[0]
    require(len(cells) == 14 and cells[1].strip() == b'710', 'unexpected selected row shape/rank')
    return rows, i, line, cells


def patch_queue(data, doi, original_row):
    valid_doi(doi)
    rows, i, before, cells = queue_row(data)
    _, _, _, original_cells = queue_row(original_row.encode() + b'\n')
    require(original_cells[8].strip() == b'claimed_solved' and original_cells[9].strip() == b'1/5',
            'historical target is not the reviewed claimed_solved 1/5 row')
    require(cells[8].strip() == b'queued' and cells[9].strip() == b'0/5' and not cells[11].strip(),
            'remote main target is no longer the unattempted queued row; reconcile without overwrite')
    require(all(cells[j] == original_cells[j] for j in range(14) if j not in (8, 9, 11)),
            'remote main identity/source/other fields differ from reviewed row')
    cells[8], cells[9] = original_cells[8], original_cells[9]
    cells[11] = (
        ' Accepted explicit counterexamples to Satoh\'s 2018 component-filtration equality: '
        'D_n(5) != A_n(5) for every n >= 4; D_n(6) != A_n(6) for every n >= 3. '
        'Rational SL(2) matrix-entry algebra; integral free-group lower central series; D acts on the whole J quotient. '
        'Classical Burde and Razmyslov identity credit retained; no new PI identity or general PI method claimed. '
        'No degree-5 rank-3, every-degree, higher-SL_m, character-algebra or ordinary IA lower-central claim. '
        'Bounded priority audit retains 2017/2021 journal and 2025/2026 related-journal access limits; '
        'no historical firstness or current-openness certificate. Extensively AI-assisted, unrefereed preprint '
        + doi + '; internal AI review is not human peer review. '
        '[Original proof and audit](attempts/30003703/README.md); '
        '[published note and current priority status](publications/30003703/PUBLICATION.md). ').encode()
    ending = b'\r\n' if before.endswith(b'\r\n') else b'\n' if before.endswith(b'\n') else b''
    after = b'|'.join(cells) + ending
    patched = b''.join(rows[:i] + [after] + rows[i + 1:])
    require(patched.splitlines(keepends=True)[:i] == rows[:i]
            and patched.splitlines(keepends=True)[i + 1:] == rows[i + 1:], 'unselected queue bytes changed')
    old_cells = before.rstrip(b'\r\n').split(b'|')
    require([j for j in range(14) if old_cells[j] != cells[j]] == [8, 9, 11], 'unexpected queue cells changed')
    return patched, {'path': QPATH, 'before_sha256': sha(data), 'after_sha256': sha(patched),
                     'before_row': before.rstrip(b'\r\n').decode(), 'after_row': after.rstrip(b'\r\n').decode(),
                     'changed_cells': ['Status', 'Turns', 'Findings'],
                     'original_claimed_solved_and_1_of_5_preserved': True,
                     'all_unselected_bytes_unchanged': True}


def inventory(root):
    require(root.is_dir() and not root.is_symlink(), 'invalid native root')
    files, directories = set(), set()
    for base, dnames, fnames in os.walk(root, followlinks=False):
        for name in dnames + fnames:
            path = Path(base) / name
            relative = safe_name(path.relative_to(root).as_posix())
            mode = path.lstat().st_mode
            require(stat.S_ISDIR(mode) or stat.S_ISREG(mode), 'native link/nonregular object')
            (directories if stat.S_ISDIR(mode) else files).add(relative)
    parents = {str(p) for name in files for p in PurePosixPath(name).parents if str(p) != '.'}
    require(directories == parents, 'unexpected native empty directory')
    return files


def load_snapshot():
    captured = regular_bytes(A / 'SCOPE_AND_SNAPSHOT.json')
    require(sha(captured) == SNAPSHOT_SHA, 'immutable scope/snapshot changed')
    snapshot = parse_json(captured)
    require(snapshot['original_head'] == ORIGINAL and snapshot['problem_id'] == PROBLEM
            and snapshot['status'] == 'claimed_solved', 'native snapshot target/status')
    records = snapshot['original_blobs']
    require(type(records) is dict and len(records) == 23, 'native snapshot must contain 23 files')
    names = set()
    root = A / 'native' / PREFIX
    files = {}
    for full, record in records.items():
        safe_name(full)
        require(full.startswith(PREFIX), 'snapshot path outside selected attempt')
        name = safe_name(full[len(PREFIX):]); names.add(name)
        data = regular_bytes(root / name)
        require(record['git_mode'] == '100644' and type(record['size']) is int
                and len(data) == record['size'] and sha(data) == record['sha256'], 'native binding: ' + name)
        require(re.fullmatch('[0-9a-f]{40}', record['git_blob']) is not None, 'native blob identity')
        files[name] = data
    require(inventory(root) == names, 'native snapshot exact inventory changed')
    return files, snapshot, captured


def accepted_inputs(publication):
    accepted_bytes = regular_bytes(ACCEPTANCE)
    accepted = parse_json(accepted_bytes)
    require(type(accepted) is dict and accepted.get('schema') == 'pr681-accepted-publication-inputs-v1'
            and accepted.get('pr') == PR and accepted.get('problem_id') == PROBLEM
            and accepted.get('original_head') == ORIGINAL and accepted.get('ready_for_publication') is True
            and accepted.get('final_live_gate_required_before_writes') is True,
            'missing or invalid accepted publication gate')
    accepted_time = timestamp(accepted.get('created_utc'), 'accepted gate')
    require(accepted_time <= datetime.datetime.now(datetime.timezone.utc), 'accepted gate is future dated')
    records = accepted.get('files')
    require(type(records) is dict and set(records) == set(PUB_NAMES), 'accepted gate requires exact ten publication inputs')
    files = {}
    for name, record in records.items():
        require(valid_pin(record), 'accepted file pin schema')
        data = regular_bytes(publication / name)
        require(file_pin(data) == record, 'unreviewed publication bytes: ' + name)
        files[name] = data
    helpers = helper_pins()
    require(accepted.get('helper_sha256') == helpers, 'unreviewed operational helper source')
    bindings = accepted.get('gate_bindings')
    require(type(bindings) is dict and set(bindings) == set(GATE_NAMES), 'math and bounded priority gate bindings required')
    gate_files = {}
    for name in GATE_NAMES:
        require(valid_pin(bindings[name]), 'invalid research gate pin')
        data = regular_bytes(A / name)
        require(file_pin(data) == bindings[name], 'research gate changed: ' + name)
        gate_files[name] = data
    math = parse_json(gate_files[GATE_NAMES[0]])
    require(math.get('status') == 'ACCEPTED_COMPLETE_COUNTEREXAMPLE_MATH_AND_LITERAL_SOURCE'
            and math.get('original_head') == ORIGINAL and math.get('native23_unchanged') is True
            and math.get('human_peer_review') is False, 'mathematical/source gate not accepted')
    priority = parse_json(gate_files[GATE_NAMES[1]])
    require(priority.get('status') == 'ACCEPTED_BOUNDED_PRIORITY_AUDIT' and priority.get('original_head') == ORIGINAL
            and priority.get('historical_firstness_certified') is False
            and priority.get('current_literature_openness_certified') is False
            and priority.get('human_peer_review') is False, 'bounded priority gate not accepted')
    rounds = accepted.get('whole_package_review_rounds')
    require(type(rounds) is list and len(rounds) >= 2, 'two sequential fresh zero-finding whole-package reviews required')
    reviewers, report_paths, review_files = set(), set(), {}
    previous_hash, previous_end = None, None
    for i, item in enumerate(rounds, 1):
        require(type(item) is dict and set(item) == {'reviewer_id', 'report_path', 'report_sha256',
                                                  'mandatory_findings', 'optional_findings'}, 'review gate entry schema')
        reviewer = item['reviewer_id']
        require(type(reviewer) is str and reviewer.strip() and reviewer not in reviewers, 'fresh distinct reviewer required')
        require(type(item['mandatory_findings']) is int and item['mandatory_findings'] == 0
                and type(item['optional_findings']) is int and item['optional_findings'] == 0, 'unresolved review findings')
        relative = safe_name(item['report_path'])
        require(relative.startswith('reviews/') and type(item['report_sha256']) is str
                and re.fullmatch('[0-9a-f]{64}', item['report_sha256']) is not None, 'review must be pinned local artifact')
        require(relative not in report_paths, 'review report artifacts must be distinct')
        data = regular_bytes(A / relative)
        require(sha(data) == item['report_sha256'], 'whole-package report hash differs')
        report = parse_json(data)
        require(type(report) is dict and report.get('schema') == 'pr681-whole-package-review-verdict-v1'
                and report.get('verdict') == 'PASS' and report.get('reviewer_id') == reviewer
                and report.get('pr') == PR and report.get('problem_id') == PROBLEM and report.get('original_head') == ORIGINAL,
                'review verdict/target differs')
        require(type(report.get('mandatory_findings')) is int and report['mandatory_findings'] == 0
                and type(report.get('optional_findings')) is int and report['optional_findings'] == 0
                and report.get('findings') == [] and report.get('findings_waived') is False,
                'whole-package review is not unwaived zero-finding')
        require(report.get('publication_files') == records and report.get('helper_sha256') == helpers
                and report.get('gate_bindings') == bindings,
                'whole-package review did not bind all exact final scientific and operational inputs')
        require(report.get('human_peer_review') is False and report.get('AI_tools_used_extensively') is True,
                'review disclosure differs')
        require('previous_report_sha256' in report and report['previous_report_sha256'] == previous_hash,
                'sequential whole-package review chain broken')
        start, end = timestamp(report.get('started_utc'), 'review start'), timestamp(report.get('completed_utc'), 'review end')
        require(start <= end <= accepted_time and (previous_end is None or previous_end <= start),
                'reviews must be sequential and complete before acceptance')
        previous_hash, previous_end = sha(data), end
        reviewers.add(reviewer); report_paths.add(relative)
        review_files[f'whole_package_reviews/round-{i:02d}/' + PurePosixPath(relative).name] = data
    final_bytes = regular_bytes(A / 'PUBLICATION_FINAL_ACCEPTANCE.json')
    final = parse_json(final_bytes)
    require(final.get('schema') == 'pr681-publication-final-acceptance-v1' and final.get('status') == 'PASS'
            and final.get('pr') == PR and final.get('problem_id') == PROBLEM and final.get('original_head') == ORIGINAL
            and final.get('accepted_input_gate_sha256') == sha(accepted_bytes)
            and json.dumps(final.get('claim_scope'), sort_keys=True) == json.dumps(EXPECTED_SCOPE, sort_keys=True),
            'final publication acceptance absent or stale')
    require(accepted_time <= timestamp(final.get('created_utc'), 'final acceptance')
            <= datetime.datetime.now(datetime.timezone.utc), 'final acceptance timing differs')
    review_files.update({'research_gate_bindings/' + name: data for name, data in gate_files.items()})
    review_files['PUBLICATION_FINAL_ACCEPTANCE.json'] = final_bytes
    return files, accepted_bytes, accepted, review_files


def archive_binding(data, original, paper_files, snapshot_bytes):
    """Validate the captured ZIP without executing or extracting unchecked paths."""
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        require(len(entries) <= 500 and len(entries) == len({e.filename for e in entries}), 'archive count or duplicate member')
        require(sum(e.file_size for e in entries) <= 64_000_000, 'archive expanded size exceeds reviewed-package limit')
        members = {}
        for entry in entries:
            name = safe_name(entry.filename)
            require(not entry.is_dir() and stat.S_IFMT(entry.external_attr >> 16) == stat.S_IFREG
                    and stat.S_IMODE(entry.external_attr >> 16) == 0o644
                    and not entry.flag_bits & 1 and entry.file_size <= 8_000_000,
                    'nonregular/non-0644/encrypted/oversized archive member')
            members[name] = archive.read(entry)
        require(archive.testzip() is None, 'archive CRC mismatch')
    require('PACKAGE_MANIFEST.json' in members, 'archive manifest missing')
    manifest = parse_json(members['PACKAGE_MANIFEST.json'])
    require(type(manifest) is dict and set(manifest) == {'schema', 'problem_id', 'original_head', 'file_count',
                'raw_third_party_fulltexts_included', 'files'} and type(manifest['schema']) is int
            and manifest['schema'] == 1 and manifest['problem_id'] == PROBLEM and manifest['original_head'] == ORIGINAL
            and manifest['raw_third_party_fulltexts_included'] is False, 'archive manifest scope/schema')
    require(type(manifest['files']) is list and type(manifest['file_count']) is int
            and len(manifest['files']) == manifest['file_count'] == len(members) - 1, 'archive manifested inventory count')
    seen = set()
    for record in manifest['files']:
        require(type(record) is dict and set(record) == {'path', 'bytes', 'sha256'}, 'archive member schema')
        name = safe_name(record['path'])
        require(name != 'PACKAGE_MANIFEST.json' and name not in seen and name in members, 'archive manifest duplicate/missing path')
        require(type(record['bytes']) is int and record['bytes'] >= 0 and len(members[name]) == record['bytes']
                and sha(members[name]) == record['sha256'], 'archive member hash/size: ' + name)
        seen.add(name)
    require(seen == set(members) - {'PACKAGE_MANIFEST.json'}, 'unmanifested archive member')
    require({name for name in members if name.startswith('native/')} == {'native/' + PREFIX + n for n in original},
            'archive native inventory must be exactly the original 23 files')
    for name, data in original.items():
        require(members['native/' + PREFIX + name] == data, 'archive original native bytes differ: ' + name)
    require(members.get('SCOPE_AND_SNAPSHOT.json') == snapshot_bytes, 'archive immutable snapshot differs')
    for name, data in paper_files.items():
        if name != 'satoh_filtration_verification.zip':
            member = 'README.md' if name == 'PACKAGE_README.md' else name
            require(members.get(member) == data, 'archive accepted publication input differs: ' + name)
    return members, {'manifest_sha256': sha(members['PACKAGE_MANIFEST.json']),
                     'manifested_members': len(seen), 'original_candidate_files_bound': 23,
                     'paper_source_metadata_and_current_scope_bound': True}


def publication_inputs(publication, doi, receipt_path, inspection_path):
    """Read each payload once; all later checks/construction use captured bytes."""
    valid_doi(doi)
    require(Path(receipt_path).absolute() != Path(inspection_path).absolute(), 'publication and inspection receipts must be distinct')
    files, accepted_bytes, accepted, review_files = accepted_inputs(publication)
    original, snapshot, snapshot_bytes = load_snapshot()
    require(files[UPLOAD_NAMES[0]].startswith(b'%PDF-'), 'paper is not a PDF')
    scope = parse_json(files['CLAIM_SCOPE.json'])
    require(json.dumps(scope, sort_keys=True) == json.dumps(EXPECTED_SCOPE, sort_keys=True),
            'exact counterexample scope or AI/unrefereed disclosure differs')
    deposit = parse_json(files['zenodo-deposit.json'])
    require(type(deposit) is dict and set(deposit) == {'metadata', 'files'} and
            deposit['files'] == [{'path': name} for name in UPLOAD_NAMES], 'deposit exact upload inventory')
    meta = deposit['metadata']
    require(meta.get('title') == TITLE and meta.get('upload_type') == 'publication'
            and meta.get('publication_type') == 'preprint' and meta.get('access_right') == 'open'
            and meta.get('license') == 'cc-by-4.0' and meta.get('creators') == [{
                'name': 'Kriebel, Alec', 'affiliation': 'Independent researcher', 'orcid': '0009-0001-9320-500X'}],
            'publication title/type/author/license metadata differs')
    description = meta.get('description', '')
    require(type(description) is str and all(text in description for text in (
        'rational', 'integral', 'Burde', 'Razmyslov', '2018', '2017', '2021', '2025', '2026',
        'unrefereed', 'AI tools', 'firstness'))
        and any(text in description for text in ('current-openness', 'continuously open status')),
        'metadata must retain exact component/integral scope, classical credit, source limits and disclosure')
    expected_files = {name: {'name': name, 'size': len(files[name]), 'sha256': sha(files[name])} for name in UPLOAD_NAMES}
    receipt_bytes = [regular_bytes(path) for path in (receipt_path, inspection_path)]
    require(receipt_bytes[0] != receipt_bytes[1], 'independent publication inspection is missing')
    receipts = [parse_json(data) for data in receipt_bytes]
    for receipt in receipts:
        require(receipt.get('environment') == 'production' and receipt.get('state') == 'published'
                and receipt.get('receipt_saved') is True and receipt.get('title') == TITLE, 'not a confirmed production publication')
        require(type(receipt.get('id')) is int and receipt['id'] > 0
                and str(receipt['id']) == doi.split('.')[-1] and receipt.get('doi') == doi
                and receipt.get('doi_url') == 'https://doi.org/' + doi
                and receipt.get('record_url') == 'https://zenodo.org/records/' + str(receipt['id']), 'published DOI/record mismatch')
        require(timestamp(receipt.get('verified_utc'), 'public receipt') <= datetime.datetime.now(datetime.timezone.utc),
                'publication verification timestamp is future dated')
        resolution = receipt.get('doi_resolution', {})
        require(resolution.get('status') == 'resolved' and type(resolution.get('http_status')) is int
                and resolution['http_status'] == 200
                and resolution.get('url') == 'https://doi.org/' + doi
                and resolution.get('resolved_url') == 'https://zenodo.org/records/' + str(receipt['id']),
                'public DOI resolution not confirmed for exact production record')
        listed = receipt.get('files')
        require(type(listed) is list and len(listed) == 2 and all(type(e) is dict for e in listed)
                and len({e.get('name') for e in listed}) == 2
                and {e.get('name'): e for e in listed} == expected_files, 'published/local upload bytes differ')
        require(receipt.get('metadata_normalizations') == [], 'unreviewed metadata normalization; reconcile explicitly')
    require(timestamp(receipts[0]['verified_utc'], 'publication receipt')
            <= timestamp(receipts[1]['verified_utc'], 'post-publication inspection'), 'inspection predates publication confirmation')
    members, binding = archive_binding(files['satoh_filtration_verification.zip'], original, files, snapshot_bytes)
    source_bindings = {'ACCEPTED_PUBLICATION_INPUTS.json': file_pin(accepted_bytes),
                       'SCOPE_AND_SNAPSHOT.json': file_pin(snapshot_bytes)}
    source_bindings.update({'publication/' + name: file_pin(data) for name, data in files.items()})
    source_bindings.update({'native/' + PREFIX + name: file_pin(data) for name, data in original.items()})
    for name in HELPER_NAMES:
        captured = regular_bytes(A / name)
        require(sha(captured) == accepted['helper_sha256'][name], 'helper changed during source binding')
        source_bindings[name] = file_pin(captured)
    for name in GATE_NAMES:
        source_bindings[name] = file_pin(review_files['research_gate_bindings/' + name])
    source_bindings['PUBLICATION_FINAL_ACCEPTANCE.json'] = file_pin(review_files['PUBLICATION_FINAL_ACCEPTANCE.json'])
    for index, item in enumerate(accepted['whole_package_review_rounds'], 1):
        source_bindings[item['report_path']] = file_pin(review_files[
            f'whole_package_reviews/round-{index:02d}/' + PurePosixPath(item['report_path']).name])
    for path, data in zip((receipt_path, inspection_path), receipt_bytes):
        relative = safe_name(Path(path).absolute().relative_to(A).as_posix())
        source_bindings[relative] = file_pin(data)
    validation = {'accepted_input_gate_sha256': sha(accepted_bytes), 'whole_package_reviewers': [r['reviewer_id'] for r in accepted['whole_package_review_rounds']],
                  'publication_receipt_sha256': sha(receipt_bytes[0]), 'inspection_receipt_sha256': sha(receipt_bytes[1]),
                  'deposit_metadata_sha256': sha(files['zenodo-deposit.json']), 'archive_binding': binding,
                  'helper_sha256': accepted['helper_sha256'],
                  'publication_confirmed_utc': receipts[0]['verified_utc'],
                  'inspection_verified_utc': receipts[1]['verified_utc'], 'source_bindings': source_bindings,
                  'files': {name: {'bytes': len(data), 'sha256': sha(data)} for name, data in sorted(files.items())}}
    return {'files': files, 'original': original, 'snapshot': snapshot, 'members': members,
            'accepted_bytes': accepted_bytes, 'review_files': review_files,
            'receipt_bytes': receipt_bytes, 'validation': validation}


def build_publication(inputs, doi, now):
    files = {('README.md' if name == 'PACKAGE_README.md' else name): data for name, data in inputs['files'].items()}
    files.update(inputs['review_files'])
    files['ACCEPTED_PUBLICATION_INPUTS.json'] = inputs['accepted_bytes']
    files['ZENODO_PUBLICATION_RECEIPT.json'], files['ZENODO_POST_PUBLICATION_INSPECTION.json'] = inputs['receipt_bytes']
    files['PUBLICATION.md'] = (
        '# Published counterexample note\n\n' + TITLE + '\n\n'
        'Preprint and exact verification archive: https://doi.org/' + doi + '\n\n'
        'The note gives explicit counterexamples to the equality posed by Satoh in OWR 2018: '
        'D_n(5) != A_n(5) for every n >= 4, and D_n(6) != A_n(6) for every n >= 3. '
        'The component algebra is the rational SL(2) matrix-entry algebra; A uses the integral free-group '
        'lower central series, and D acts on the whole J quotient. The classical Burde and Razmyslov '
        'identity credit is explicit. Neither a new PI identity nor a new general PI method is claimed.\n\n'
        'The note makes no degree-5 rank-3, every-degree, higher-SL_m, character-algebra, or ordinary '
        'IA lower-central conjecture claim. It gives no historical firstness, exhaustive novelty clearance, '
        'or current-literature-openness certificate. The 2017/2021 journal and 2025/2026 related-journal '
        'source-access limits remain explicit in [CURRENT_PRIORITY_AND_STATUS.md](CURRENT_PRIORITY_AND_STATUS.md). '
        'AI tools were used extensively; this is an unrefereed preprint, and internal AI review is not human peer review.\n\n'
        'The [original attempt](../../attempts/30003703/README.md) has exactly its original 23 files '
        'with all bytes and Git modes preserved. New publication files live in this sibling directory because '
        'adding files to the attempt would invalidate its strict inventory verifier. From the attempt directory run '
        '`python3 -B verify_publication.py --replay --selftest`. To replay the complete supplement, extract '
        '`satoh_filtration_verification.zip` into an empty directory and run '
        '`python3 -B verify_package.py --replay --selftest`; see its README for dependencies.\n').encode()
    confirmed_utc = inputs['validation']['publication_confirmed_utc']
    files['PUBLICATION_LOG.md'] = (f'# Publication checkpoint\n\n{now}: integration preparation for DOI {doi}; '
        f'public publication was confirmed at {confirmed_utc}. Accepted degree/rank scope only; original '
        '23-file attempt unchanged. Classical credit, extensive AI use, unrefereed status, and source-access '
        'limits retained. Completion estimate: 100% of this scoped publication package; no firstness or '
        'current-openness certification. This preparation timestamp does not claim the actual publication instant.\n').encode()
    files['PUBLICATION.json'] = json_bytes({'schema': 'pr681-published-counterexample-note-v1', 'pr': PR,
        'problem_id': PROBLEM, 'historical_candidate_commit': ORIGINAL, 'doi': doi, 'doi_url': 'https://doi.org/' + doi,
        'publication_confirmed_utc': confirmed_utc, 'integration_prepared_utc': now,
        'claim_scope': parse_json(inputs['files']['CLAIM_SCOPE.json']),
        'native_attempt': PREFIX.rstrip('/'), 'native_files': 23, 'native_all_bytes_preserved': True,
        'native_all_git_modes_preserved': True,
        'acceptance_report_paths_are_relative_to_audit_root': A.relative_to(REPO).as_posix(),
        'copied_review_and_gate_files': sorted(inputs['review_files']), 'publication_validation': inputs['validation']})
    files['PUBLICATION_MANIFEST.json'] = json_bytes({'schema': 'pr681-publication-directory-manifest-v1',
        'files': [{'path': name, 'bytes': len(data), 'sha256': sha(data)} for name, data in sorted(files.items())]})
    return files


def recheck_sources(validation):
    for relative, pin in validation['source_bindings'].items():
        safe_name(relative)
        require(file_pin(regular_bytes(A / relative)) == pin, 'captured accepted input changed: ' + relative)
    require(helper_pins() == validation['helper_sha256'], 'executed helper source changed')


def validate_live_write_gate(kind, doi, validation, main_base=None):
    require(kind in ('integration', 'tracker'), 'unsupported live write gate')
    recheck_sources(validation)
    path = A / ('FINAL_' + kind.upper() + '_GATE.json')
    raw = regular_bytes(path); gate = parse_json(raw)
    require(gate.get('schema') == 'pr681-final-' + kind + '-gate-v1' and gate.get('status') == 'PASS'
            and gate.get('pr') == PR and gate.get('problem_id') == PROBLEM and gate.get('original_head') == ORIGINAL
            and gate.get('doi') == doi, 'final live write gate target differs')
    age = datetime.datetime.now(datetime.timezone.utc) - timestamp(gate.get('created_utc'), 'final live write gate')
    require(datetime.timedelta(0) <= age <= datetime.timedelta(minutes=15), 'final live write gate expired or future dated')
    for key in ('accepted_input_gate_sha256', 'publication_receipt_sha256', 'inspection_receipt_sha256', 'helper_sha256'):
        require(gate.get(key) == validation[key], 'final live write gate source binding differs: ' + key)
    live = pr_metadata(); check_known_head(live)
    fields = ('number', 'state', 'isDraft', 'baseRefName', 'headRefName', 'headRefOid')
    expected_live = {key: live[key] for key in fields}
    require(gate.get('live_pr') == expected_live, 'final gate live PR identity differs')
    if kind == 'integration':
        require(gate.get('integration_allowed') is True and gate.get('main_base') == main_base,
                'final integration gate does not bind freshly advertised main')
    else:
        require(gate.get('tracker_append_allowed') is True
                and gate.get('spreadsheet_id') == '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
                and type(gate.get('sheet_id')) is int and gate['sheet_id'] == 1254632077
                and gate.get('sheet_title') == 'Math Puzzles', 'final tracker gate target differs')
    return {'path': path.name, 'sha256': sha(raw), 'verified_utc': utc()}


def local_state():
    require(git('symbolic-ref', '-q', 'HEAD').decode().strip() == 'refs/heads/main', 'shared checkout must select main')
    index = Path(git('rev-parse', '--git-path', 'index').decode().strip())
    if not index.is_absolute(): index = REPO / index
    return {'head': git('rev-parse', 'HEAD').decode().strip(),
            'index_sha256': sha(regular_bytes(index)) if index.exists() else None}


def tree_entries(tree):
    entries = {}
    for entry in git('ls-tree', '-z', tree).split(b'\0'):
        if not entry: continue
        details, name = entry.split(b'\t', 1)
        require(name not in entries, 'duplicate Git tree entry')
        entries[name] = details
    return entries


def make_tree(entries):
    data = b''.join(details + b'\t' + name + b'\0' for name, details in sorted(entries.items()))
    return git('mktree', '-z', input=data).decode().strip()


def files_tree(files):
    """No index: construct only the tiny publication/attempt directory trees."""
    nodes = {}
    for name, data in files.items():
        safe_name(name)
        pieces = name.split('/')
        node = nodes
        for component in pieces[:-1]:
            child = node.setdefault(component, {})
            require(type(child) is dict, 'file/directory collision')
            node = child
        require(pieces[-1] not in node, 'duplicate tree path')
        node[pieces[-1]] = data
    def build(node):
        entries = {}
        for name, value in node.items():
            if type(value) is dict:
                details = b'040000 tree ' + build(value).encode()
            else:
                require(type(value) is bytes, 'tree payload must be captured bytes')
                details = b'100644 blob ' + git('hash-object', '-w', '--stdin', input=value).strip()
            entries[name.encode()] = details
        return make_tree(entries)
    return build(nodes)


def splice(tree, path, details):
    """Replace exactly one path, forwarding every unrelated tree entry unchanged."""
    safe_name(path)
    first, separator, rest = path.partition('/')
    name = first.encode(); entries = tree_entries(tree) if tree else {}
    if separator:
        previous = entries.get(name)
        require(previous is None or previous.startswith(b'040000 tree '), 'non-tree path ancestor')
        child = previous.split(b' ')[2].decode() if previous else None
        entries[name] = b'040000 tree ' + splice(child, rest, details).encode()
    else:
        entries[name] = details
    return make_tree(entries)


def capture_replay(inputs, temporary, publication):
    native = Path(temporary) / 'proposed-target' / PREFIX
    for name, data in inputs['original'].items():
        path = native / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data); path.chmod(0o644)
    sibling = Path(temporary) / 'proposed-target' / PUB_PREFIX
    for name, data in publication.items():
        path = sibling / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data); path.chmod(0o644)
    package = Path(temporary) / 'archive'
    for name, data in inputs['members'].items():
        path = package / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data); path.chmod(0o644)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(temporary), PYTHONOPTIMIZE='0')
    environment.pop('PYTHONPATH', None); environment.pop('PYTHONHOME', None)
    def run(script, args):
        result = subprocess.run([sys.executable, '-I', '-B', str(script), *args], cwd=script.parent,
                                env=environment, capture_output=True, timeout=900)
        require(result.returncode == 0, 'isolated proposed-tree replay failed: ' + result.stderr.decode(errors='replace'))
        return parse_json(result.stdout)
    native_report = run(native / 'verify_publication.py', ['--replay', '--selftest'])
    require(native_report.get('result') == 'PASS' and native_report.get('packet_files') == 23
            and native_report.get('problem_id') == PROBLEM and native_report.get('status') == 'claimed_solved'
            and native_report.get('turns') == '1/5' and native_report.get('author_negative_controls') == 5
            and native_report.get('independent_negative_controls') == 12
            and native_report.get('assertions_enabled_in_frozen_subprocesses') is True
            and native_report.get('author_replay_byte_equal') is True
            and native_report.get('independent_replay_byte_equal') is True,
            'original verifier did not retain exact 23-file native validation and 5/12 negative controls')
    package_report = run(package / 'verify_package.py', ['--replay', '--selftest'])
    require(package_report.get('status') == 'PASS' and package_report.get('native_files') == 23
            and package_report.get('problem_id') == PROBLEM and package_report.get('original_head') == ORIGINAL,
            'accepted supplement target/integrity failed')
    package_replay = package_report.get('replay', {})
    require(package_replay.get('status') == 'PASS' and package_replay.get('native') == native_report
            and package_replay.get('native_wrapper_assertions_enabled') is True
            and package_replay.get('temporary_copies_only') is True, 'accepted supplement replay did not execute')
    controls = package_report.get('selftest', {})
    count = controls.get('case_count')
    require(controls.get('status') == 'PASS' and type(count) is int and count >= 30
            and controls.get('negative_controls_rejected_per_mode') == count
            and controls.get('total_rejections') == 2 * count
            and controls.get('modes') == ['normal', 'optimized']
            and controls.get('temporary_copies_only') is True
            and controls.get('unverified_packet_code_executed') is False,
            'accepted supplement must reject at least thirty offline hostile cases in each mode')
    rejected = controls.get('rejected', {})
    require(type(rejected) is dict and set(rejected) == {'normal', 'optimized'}
            and all(type(rejected[mode]) is list and len(rejected[mode]) == count
                    and all(type(case) is str for case in rejected[mode]) and len(set(rejected[mode])) == count
                    for mode in rejected) and rejected['normal'] == rejected['optimized'],
            'accepted supplement offline hostile-case inventory differs between modes')
    require(all(regular_bytes(native / name) == data for name, data in inputs['original'].items())
            and inventory(native) == set(inputs['original']), 'native changed during proposed-tree replay')
    require(all(regular_bytes(sibling / name) == data for name, data in publication.items())
            and inventory(sibling) == set(publication), 'publication sibling changed during replay')
    require(all(regular_bytes(package / name) == data for name, data in inputs['members'].items())
            and inventory(package) == set(inputs['members']), 'accepted archive changed during replay')
    return {'native_proposed_tree': native_report, 'accepted_archive': package_report,
            'publication_is_sibling_not_inside_native_inventory': True, 'temporary_copies_only': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--doi', required=True)
    parser.add_argument('--push', action='store_true')
    args = parser.parse_args(); valid_doi(args.doi)
    with action_lock('INTEGRATION_OPERATION.lock'):
        require(not PUSH_INTENT.exists() and not PUSH_INTENT.is_symlink()
                and not PUSHED_RECEIPT.exists() and not PUSHED_RECEIPT.is_symlink(),
                'push was already dispatched or confirmed; reconcile identities, never blindly retry')
        initial = local_state()
        head = check_known_head(pr_metadata())
        inputs = publication_inputs(A / 'publication', args.doi, A / 'ZENODO_PUBLICATION_RECEIPT.json',
                                    A / 'ZENODO_POST_PUBLICATION_INSPECTION.json')
        tmp_root = A / 'tmp'; tmp_root.mkdir(exist_ok=True)
        require(not tmp_root.is_symlink(), 'temporary root is linked')
        # Retain the dedicated object store for reviewers; no shared objects or refs are written.
        temporary = tempfile.mkdtemp(prefix='integration-', dir=tmp_root)
        with isolated_objects(temporary) as object_directory:
            base, fetch_validation = fetch_main()
            live_queue = git('show', head + ':' + QPATH)
            _, _, selected_line, selected_cells = queue_row(live_queue)
            require(selected_cells[8].strip() == b'claimed_solved' and selected_cells[9].strip() == b'1/5', 'live PR scope gate')
            require(selected_line.rstrip(b'\r\n').decode() == inputs['snapshot']['queue_row'], 'selected reviewed row changed')
            actual_records = {}
            for entry in git('ls-tree', '-r', '-z', head, '--', PREFIX).split(b'\0'):
                if not entry: continue
                details, name = entry.split(b'\t', 1)
                mode, kind, oid = details.decode().split()
                require(mode == '100644' and kind == 'blob', 'nonregular original Git object')
                actual_records[name.decode()] = {'git_mode': mode, 'git_blob': oid}
            require(actual_records == {name: {key: record[key] for key in ('git_mode', 'git_blob')}
                    for name, record in inputs['snapshot']['original_blobs'].items()}, 'immutable Git attempt inventory/modes/blobs differ')
            for name, data in inputs['original'].items():
                require(git('show', ORIGINAL + ':' + PREFIX + name) == data, 'original Git/native capture mismatch: ' + name)
            for prefix in (PREFIX, PUB_PREFIX):
                require(not git('ls-tree', '--name-only', base, '--', prefix.rstrip('/')).strip(),
                        'selected target exists on remote main; reconcile without overwrite')
            queue_entry = git('ls-tree', base, '--', QPATH).split(b'\t', 1)[0]
            require(queue_entry.startswith(b'100644 blob '), 'remote main queue mode differs')
            patched, queue_patch = patch_queue(git('show', base + ':' + QPATH), args.doi, inputs['snapshot']['queue_row'])
            now = utc(); publication = build_publication(inputs, args.doi, now)
            replay = capture_replay(inputs, temporary, publication)
            tree = git('rev-parse', base + '^{tree}').decode().strip()
            tree = splice(tree, PREFIX.rstrip('/'), b'040000 tree ' + files_tree(inputs['original']).encode())
            tree = splice(tree, PUB_PREFIX.rstrip('/'), b'040000 tree ' + files_tree(publication).encode())
            tree = splice(tree, QPATH, b'100644 blob ' + git('hash-object', '-w', '--stdin', input=patched).strip())
            expected = {QPATH: patched} | {PREFIX + n: d for n, d in inputs['original'].items()} | {PUB_PREFIX + n: d for n, d in publication.items()}
            changed = [name.decode() for name in git('diff', '--no-ext-diff', '--no-textconv', '--name-only', '-z', base, tree).split(b'\0') if name]
            require(set(changed) == set(expected), 'integration changed paths outside exact target allowlist')
            for name, data in expected.items():
                require(git('show', tree + ':' + name) == data, 'proposed tree bytes differ: ' + name)
                require(git('ls-tree', tree, '--', name).split(b'\t', 1)[0].startswith(b'100644 blob '),
                        'proposed Git file mode differs: ' + name)
            require(git('diff', '--no-ext-diff', '--no-textconv', '--numstat', base, tree, '--', QPATH).decode().split()[:2] == ['1', '1'], 'queue change is not one row')
            commit = git('commit-tree', tree, '-p', base, '-p', head,
                         input=b'Accept PR681 Satoh component-filtration counterexamples with bounded priority disclosures\n').decode().strip()
            require(local_state() == initial, 'shared checkout/index changed during preparation; abort push')
            require(helper_pins() == inputs['validation']['helper_sha256'], 'operational sources changed during preparation')
            receipt = {'schema': 'pr681-scoped-integration-receipt-v1', 'integration_prepared_utc': now, 'pr': PR,
                'problem_id': PROBLEM, 'branch': BRANCH, 'historical_candidate_commit': ORIGINAL,
                'main_base': base, 'existing_pr_head': head, 'integration_commit': commit, 'tree': tree,
                'object_directory': object_directory, 'retained_isolated_preparation_directory': temporary,
                'doi': args.doi, 'changed_paths': changed, 'queue_patch': queue_patch,
                'native_files': 23, 'native_all_bytes_unchanged': True, 'native_all_git_modes_unchanged': True,
                'attempt_sha256': {n: sha(d) for n, d in sorted(inputs['original'].items())},
                'publication_sha256': {n: sha(d) for n, d in sorted(publication.items())},
                'publication_validation': inputs['validation'], 'proposed_tree_replay': replay, 'main_fetch': fetch_validation,
                'shared_checkout_and_index_untouched': True, 'all_shared_git_refs_and_objects_untouched': True,
                'whole_repository_index_created': False, 'helper_sha256': EXECUTED_SOURCE_SHA256, 'pushed': False}
            recheck_sources(inputs['validation'])
            write_json(A / 'INTEGRATION_PREPARED_RECEIPT.json', receipt)
            if args.push:
                final_gate = validate_live_write_gate('integration', args.doi, inputs['validation'], base)
                require(check_known_head(pr_metadata()) == head, 'PR head changed after preparation')
                require(remote_oid('refs/heads/' + BRANCH) == head, 'remote PR branch head changed before push')
                require(remote_oid('refs/heads/main') == base, 'remote main advanced; rebuild and obtain a fresh live gate')
                require(local_state() == initial, 'shared checkout/index drifted before push')
                require(helper_pins() == inputs['validation']['helper_sha256'], 'helper source changed before push')
                write_json(PUSH_INTENT, {'schema': 'pr681-push-intent-v1', 'dispatch_utc': utc(),
                    'doi': args.doi, 'branch': BRANCH, 'expected_old_head': head, 'main_base': base,
                    'integration_commit': commit, 'object_directory': object_directory,
                    'final_live_gate': final_gate, 'outcome': 'unconfirmed; read remote branch before any retry'})
                # The original head is a parent: an ordinary push must fast-forward it.
                # Using the verified URL avoids push's automatic local remote-tracking ref update.
                git('push', origin_url(push=True), commit + ':refs/heads/' + BRANCH)
                receipt.update(pushed=True, pushed_utc=utc(), final_live_gate=final_gate)
                write_json(PUSHED_RECEIPT, receipt)
                require(remote_oid('refs/heads/' + BRANCH) == commit,
                        'push returned but branch readback differs; durable receipt saved, reconcile without retry')
                after = pr_metadata()
                receipt['remote_branch_head_verified'] = True
                receipt['github_metadata_head_verified'] = after.get('headRefOid') == commit and after.get('state') == 'OPEN'
                receipt['github_metadata_readback_pending'] = not receipt['github_metadata_head_verified']
                write_json(PUSHED_RECEIPT, receipt)
                # Keep the original dispatch identity when the durable intent becomes confirmed.
                intent = parse_json(regular_bytes(PUSH_INTENT))
                write_json(PUSH_INTENT, intent | {'confirmed_utc': utc(), 'outcome': 'confirmed'})
            print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
