#!/usr/bin/env python3
"""Prepare the reviewed PR662 publication using immutable captures and small trees.

Default execution only reads remote state and creates local Git objects/receipts.
Only --push updates the existing PR branch, by an ordinary non-force push. The
shared checkout, selected main branch and index are never written. The exact
24-file attempt is preserved; new material goes in publications/2306086 because
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
PR = 662
PROBLEM = '2306086'
BRANCH = 'research/2306086-qualitative-preschwarzian'
ORIGINAL = 'e31701151c331a6eed9224fb37a75a374ea1043e'
PREFIX = 'unsolved_math_prioritization/attempts/2306086/'
PUB_PREFIX = 'unsolved_math_prioritization/publications/2306086/'
QPATH = 'unsolved_math_prioritization/QUEUE.md'
KEY = '2306086 / AMR-022-6086'
TITLE = 'A qualitative pre-Schwarzian improvement for real schlicht functions'
SNAPSHOT_SHA = '53736a33a43e4291cf51de8a7cbdd15f4cfedbc10ee3c585d7381723b2329e13'
PUB_NAMES = (
    'real_schlicht_preschwarzian.pdf', 'real_schlicht_preschwarzian.tex',
    'real_schlicht_verification.zip', 'zenodo-deposit.json', 'PACKAGE_README.md',
    'CURRENT_PRIORITY_AND_STATUS.md', 'CLAIM_SCOPE.json', 'requirements.txt',
    'requirements_numerical.txt', 'verify_package.py', 'build_package.py',
)
UPLOAD_NAMES = ('real_schlicht_preschwarzian.pdf', 'real_schlicht_verification.zip')
FALSE_FLAGS = (
    'explicit_upper_gap_formula', 'sharp_quantitative_radius',
    'general_nonreal_extremizers', 'full_variability_region',
    'numerical_interval_certification', 'formal_proof_certificate',
    'historical_firstness_claim', 'exhaustive_novelty_clearance',
    'current_literature_openness_certified', 'AI_reviews_are_human_peer_review',
)
EXPECTED_SCOPE = {
    'problem_id': PROBLEM, 'original_pr': PR, 'original_head': ORIGINAL,
    'claim': 'qualitative_fixed_nonreal_point_improvement_uniform_in_f',
    'real_diameter_radius_sharp': True, 'source_expression_at_zero': 0,
    'compact_nonreal_sets_uniform_gap': True,
    **{flag: False for flag in FALSE_FLAGS},
    'methods': 'classical_coefficient_rigidity_real_symmetry_compactness',
    'AI_tools_used_extensively': True, 'unrefereed': True,
}
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
    path = Path(path).absolute()
    require(all(not p.is_symlink() for p in path.parents), 'linked input parent: ' + str(path))
    require(stat.S_ISREG(path.lstat().st_mode), 'missing/linked/nonregular file: ' + str(path))
    return path.read_bytes()


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
    return subprocess.check_output(['git', *args], cwd=REPO, input=input, stderr=subprocess.PIPE)


def fetch_main():
    """A concurrent ref-CAS failure can only be reconciled by matching identities."""
    reconciled = False
    try:
        git('fetch', '--no-write-fetch-head', 'origin', 'refs/heads/main:refs/remotes/origin/main')
    except subprocess.CalledProcessError as error:
        message = (error.stderr or b'').decode(errors='replace')
        require("cannot lock ref 'refs/remotes/origin/main'" in message
                and 'is at ' in message and 'but expected ' in message,
                'fetch failed; preserve shared Git state and reconcile without cleanup or an automatic retry')
        advertised = git('ls-remote', '--exit-code', 'origin', 'refs/heads/main').decode().split()[0]
        current = git('rev-parse', 'refs/remotes/origin/main').decode().strip()
        require(re.fullmatch('[0-9a-f]{40}', advertised) and current == advertised,
                'concurrent fetch ref differs from advertised main; abort without modifying locks or refs')
        reconciled = True
    base = git('rev-parse', 'refs/remotes/origin/main').decode().strip()
    require(re.fullmatch('[0-9a-f]{40}', base), 'remote main identity malformed')
    return base, {'concurrent_fetch_ref_CAS_reconciled_by_exact_readback': reconciled,
                  'no_shared_git_cleanup_or_automatic_fetch_retry': True}


def pr_metadata():
    return parse_json(subprocess.check_output(
        ['gh', 'pr', 'view', str(PR), '--json',
         'number,state,isDraft,baseRefName,headRefOid,headRefName,headRepositoryOwner,isCrossRepository'], cwd=REPO))


def check_known_head(meta):
    """Run before reading any live candidate, frozen attempt or paper contents."""
    require(meta.get('number') == PR and meta.get('state') == 'OPEN' and meta.get('isDraft') is True,
            'selected PR must remain the open draft PR662')
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
    require(len(cells) == 14 and cells[1].strip() == b'687', 'unexpected selected row shape/rank')
    return rows, i, line, cells


def patch_queue(data, doi, original_row):
    valid_doi(doi)
    rows, i, before, cells = queue_row(data)
    _, _, _, original_cells = queue_row(original_row.encode() + b'\n')
    require(original_cells[8].strip() == b'claimed_solved' and original_cells[9].strip() == b'5/5',
            'historical target is not the reviewed qualitative claimed_solved 5/5 row')
    require(cells[8].strip() == b'queued' and cells[9].strip() == b'0/5' and not cells[11].strip(),
            'remote main target is no longer the unattempted queued row; reconcile without overwrite')
    require(all(cells[j] == original_cells[j] for j in range(14) if j not in (8, 9, 11)),
            'remote main target identity/source/other fields differ from reviewed row')
    cells[8], cells[9] = original_cells[8], original_cells[9]
    cells[11] = (
        ' Accepted qualitative fixed-point improvement for the normalized real-coefficient schlicht class: '
        'M(z)<4 at every fixed nonreal point, uniformly in the class and on compact nonreal sets; '
        'M(x)=4 on the real diameter and the source expression is zero at zero. '
        'Classical coefficient equality, slit rigidity and compactness; explicit upper gap, sharp quantitative radius '
        'and general extremizers are undetermined. Bounded priority audit retains Jenkins (1960) and '
        'Aleksandrov-Popova (1973) original-source limits; no historical firstness or current-openness guarantee. '
        'Extensively AI-assisted, unrefereed preprint ' + doi + '. '
        '[Original proof and controlling scope](attempts/2306086/README.md); '
        '[published note and current priority status](publications/2306086/PUBLICATION.md). ').encode()
    ending = b'\r\n' if before.endswith(b'\r\n') else b'\n' if before.endswith(b'\n') else b''
    after = b'|'.join(cells) + ending
    patched = b''.join(rows[:i] + [after] + rows[i + 1:])
    require(patched.splitlines(keepends=True)[:i] == rows[:i]
            and patched.splitlines(keepends=True)[i + 1:] == rows[i + 1:], 'unselected queue bytes changed')
    old_cells = before.rstrip(b'\r\n').split(b'|')
    require([j for j in range(14) if old_cells[j] != cells[j]] == [8, 9, 11], 'unexpected queue cells changed')
    return patched, {'path': QPATH, 'before_sha256': sha(data), 'after_sha256': sha(patched),
                     'before_row': before.rstrip(b'\r\n').decode(),
                     'after_row': after.rstrip(b'\r\n').decode(),
                     'changed_cells': ['Status', 'Turns', 'Findings'],
                     'original_claimed_solved_and_5_of_5_preserved': True,
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
    require(type(records) is dict and len(records) == 24, 'native snapshot must contain 24 files')
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
    require(accepted.get('schema') == 'pr662-accepted-publication-inputs-v1'
            and accepted.get('pr') == PR and accepted.get('problem_id') == PROBLEM
            and accepted.get('original_head') == ORIGINAL and accepted.get('ready_for_publication') is True,
            'missing or invalid accepted publication gate')
    records = accepted.get('files')
    require(type(records) is dict and set(records) == set(PUB_NAMES), 'accepted gate requires exact eleven publication inputs')
    files = {}
    for name, record in records.items():
        require(type(record) is dict and set(record) == {'bytes', 'sha256'}
                and type(record['bytes']) is int and record['bytes'] >= 0
                and re.fullmatch('[0-9a-f]{64}', record['sha256']) is not None, 'accepted file pin schema')
        data = regular_bytes(publication / name)
        require(len(data) == record['bytes'] and sha(data) == record['sha256'], 'unreviewed publication bytes: ' + name)
        files[name] = data
    rounds = accepted.get('whole_package_review_rounds')
    require(type(rounds) is list and len(rounds) >= 2, 'two fresh zero-finding whole-package reviews are required')
    reviewers, report_paths, review_files = set(), set(), {}
    for i, item in enumerate(rounds, 1):
        require(type(item) is dict and set(item) == {'reviewer_id', 'report_path', 'report_sha256',
                                                  'mandatory_findings', 'optional_findings'}, 'review gate entry schema')
        reviewer = item['reviewer_id']
        require(type(reviewer) is str and reviewer.strip() and reviewer not in reviewers, 'whole-package reviewer must be distinct')
        require(type(item['mandatory_findings']) is int and item['mandatory_findings'] == 0
                and type(item['optional_findings']) is int and item['optional_findings'] == 0,
                'unresolved whole-package findings')
        relative = safe_name(item['report_path'])
        require(relative.startswith('reviews/') and re.fullmatch('[0-9a-f]{64}', item['report_sha256']),
                'review report must be a pinned local review artifact')
        require(relative not in report_paths, 'review reports must be distinct artifacts')
        data = regular_bytes(A / relative)
        require(sha(data) == item['report_sha256'], 'whole-package report hash differs')
        reviewers.add(reviewer); report_paths.add(relative)
        review_files[f'whole_package_reviews/round-{i:02d}/' + PurePosixPath(relative).name] = data
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
                    and not entry.flag_bits & 1 and entry.file_size <= 8_000_000, 'nonregular/encrypted/oversized archive member')
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
            'archive native inventory must be exactly the original 24 files')
    for name, data in original.items():
        require(members['native/' + PREFIX + name] == data, 'archive original native bytes differ: ' + name)
    require(members.get('SCOPE_AND_SNAPSHOT.json') == snapshot_bytes, 'archive immutable snapshot differs')
    for name, data in paper_files.items():
        if name != 'real_schlicht_verification.zip':
            member = 'README.md' if name == 'PACKAGE_README.md' else name
            require(members.get(member) == data, 'archive accepted publication input differs: ' + name)
    return members, {'manifest_sha256': sha(members['PACKAGE_MANIFEST.json']),
                     'manifested_members': len(seen), 'original_candidate_files_bound': 24,
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
            'exact qualitative scope or AI/unrefereed disclosure differs')
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
        'qualitative', 'Jenkins (1960)', 'Aleksandrov', '1973', 'unrefereed', 'AI tools', 'firstness', 'current-openness')),
        'metadata must retain accepted qualitative scope, priority limits and disclosure')
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
        require(type(receipt.get('verified_utc')) is str and receipt['verified_utc'], 'publication verification timestamp absent')
        resolution = receipt.get('doi_resolution', {})
        require(resolution.get('status') == 'resolved' and type(resolution.get('http_status')) is int
                and resolution['http_status'] == 200, 'DOI resolution not confirmed')
        listed = receipt.get('files')
        require(type(listed) is list and len(listed) == 2 and all(type(e) is dict for e in listed)
                and len({e.get('name') for e in listed}) == 2
                and {e.get('name'): e for e in listed} == expected_files, 'published/local upload bytes differ')
        require(receipt.get('metadata_normalizations') == [], 'unreviewed metadata normalization; reconcile explicitly')
    members, binding = archive_binding(files['real_schlicht_verification.zip'], original, files, snapshot_bytes)
    validation = {'accepted_input_gate_sha256': sha(accepted_bytes), 'whole_package_reviewers': [r['reviewer_id'] for r in accepted['whole_package_review_rounds']],
                  'publication_receipt_sha256': sha(receipt_bytes[0]), 'inspection_receipt_sha256': sha(receipt_bytes[1]),
                  'deposit_metadata_sha256': sha(files['zenodo-deposit.json']), 'archive_binding': binding,
                  'files': {name: {'bytes': len(data), 'sha256': sha(data)} for name, data in sorted(files.items())}}
    return {'files': files, 'original': original, 'snapshot': snapshot, 'members': members,
            'accepted_bytes': accepted_bytes, 'review_files': review_files,
            'receipt_bytes': receipt_bytes, 'validation': validation}


def build_publication(inputs, doi, now):
    files = {('README.md' if name == 'PACKAGE_README.md' else name): data
             for name, data in inputs['files'].items()}
    files.update(inputs['review_files'])
    files['ACCEPTED_PUBLICATION_INPUTS.json'] = inputs['accepted_bytes']
    files['ZENODO_PUBLICATION_RECEIPT.json'], files['ZENODO_POST_PUBLICATION_INSPECTION.json'] = inputs['receipt_bytes']
    files['PUBLICATION.md'] = (
        '# Published qualitative research note\n\n' + TITLE + '\n\n'
        'Preprint and exact verification archive: https://doi.org/' + doi + '\n\n'
        'The normalized real-coefficient schlicht class admits M(z)<4 at each fixed nonreal point, '
        'uniformly over the class and on compact nonreal sets. The classical real-diameter radius is sharp; '
        'the original displayed expression is zero at zero. An explicit upper gap, the sharp quantitative radius, '
        'and general nonreal extremizers remain undetermined in this note.\n\n'
        'This is an application of classical coefficient equality, slit-domain rigidity and compactness. '
        'No historical firstness, exhaustive novelty clearance or present-openness guarantee is claimed. '
        'The original-source limits for Jenkins (1960) and Aleksandrov-Popova (1973) remain explicit in '
        '[CURRENT_PRIORITY_AND_STATUS.md](CURRENT_PRIORITY_AND_STATUS.md). AI tools were used extensively; '
        'the preprint is unrefereed, and internal AI review is not human peer review.\n\n'
        'The [original attempt](../../attempts/2306086/README.md), including its controlling scope note, '
        'has exactly the original 24 files with all bytes preserved. New publication files live in this sibling '
        'directory because adding files to the attempt would invalidate its exact-inventory verifier. '
        'Run the original verifier from its own attempt directory. For the complete supplement, extract '
        '`real_schlicht_verification.zip` to an empty directory and run `python3 -B verify_package.py --replay`; '
        'see the included README for dependencies and optional uncertified numerical replay.\n').encode()
    files['PUBLICATION_LOG.md'] = (f'# Publication checkpoint\n\n{now}: DOI {doi}; accepted qualitative '
                                  'claim only; original 24-file attempt unchanged; extensiveness of AI use and '
                                  'unrefereed status disclosed; historical priority source gaps retained. '
                                  'Completion estimate: 100% of this scoped publication package, not of the '
                                  'unresolved quantitative or historical-priority questions.\n').encode()
    files['PUBLICATION.json'] = json_bytes({'schema': 'pr662-published-qualitative-note-v1', 'pr': PR,
        'problem_id': PROBLEM, 'historical_candidate_commit': ORIGINAL, 'doi': doi, 'doi_url': 'https://doi.org/' + doi,
        'published_utc': now, 'claim_scope': parse_json(inputs['files']['CLAIM_SCOPE.json']),
        'native_attempt': PREFIX.rstrip('/'), 'native_files': 24, 'native_all_bytes_preserved': True,
        'acceptance_report_paths_are_relative_to_audit_root': A.relative_to(REPO).as_posix(),
        'copied_whole_package_report_files': sorted(inputs['review_files']), 'publication_validation': inputs['validation']})
    files['PUBLICATION_MANIFEST.json'] = json_bytes({'schema': 'pr662-publication-directory-manifest-v1',
        'files': [{'path': name, 'bytes': len(data), 'sha256': sha(data)} for name, data in sorted(files.items())]})
    return files


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
        path = native / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    # The new publication is a sibling, never a descendant of the strict attempt.
    sibling = Path(temporary) / 'proposed-target' / PUB_PREFIX
    for name, data in publication.items():
        path = sibling / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    package = Path(temporary) / 'archive'
    for name, data in inputs['members'].items():
        path = package / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(temporary))
    environment.pop('PYTHONOPTIMIZE', None)
    def run(script, args):
        result = subprocess.run([sys.executable, '-I', '-B', str(script), *args], cwd=script.parent,
                                env=environment, capture_output=True, timeout=900)
        require(result.returncode == 0, 'isolated proposed-tree replay failed: ' + result.stderr.decode(errors='replace'))
        return parse_json(result.stdout)
    native_report = run(native / 'verify_publication.py', ['--replay', '--selftest'])
    require(native_report.get('status') == 'PASS' and native_report.get('files') == 24
            and len(native_report.get('publication_negative_controls_rejected', [])) == 24,
            'original verifier did not retain exact 24-file validation')
    package_report = run(package / 'verify_package.py', ['--replay'])
    require(package_report.get('status') == 'PASS' and package_report.get('native_files') == 24,
            'accepted supplement replay failed')
    require(all(regular_bytes(native / name) == data for name, data in inputs['original'].items()), 'native changed during proposed-tree replay')
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
                'a push was already dispatched or confirmed; reconcile recorded identities, never blindly retry')
        initial = local_state()
        head = check_known_head(pr_metadata())
        live_queue = git('show', head + ':' + QPATH)
        _, _, selected_line, selected_cells = queue_row(live_queue)
        require(selected_cells[8].strip() == b'claimed_solved' and selected_cells[9].strip() == b'5/5', 'live selected PR scope gate')
        inputs = publication_inputs(A / 'publication', args.doi, A / 'ZENODO_PUBLICATION_RECEIPT.json',
                                    A / 'ZENODO_POST_PUBLICATION_INSPECTION.json')
        require(selected_line.rstrip(b'\r\n').decode() == inputs['snapshot']['queue_row'], 'selected reviewed row changed')
        original_names = git('ls-tree', '-r', '-z', head, '--', PREFIX).split(b'\0')
        actual_records = {}
        for entry in original_names:
            if not entry: continue
            details, name = entry.split(b'\t', 1)
            mode, kind, oid = details.decode().split()
            require(mode == '100644' and kind == 'blob', 'nonregular original Git object')
            actual_records[name.decode()] = oid
        require(actual_records == {name: record['git_blob'] for name, record in inputs['snapshot']['original_blobs'].items()},
                'immutable Git attempt inventory/blob identity differs')
        for name, data in inputs['original'].items():
            require(git('show', ORIGINAL + ':' + PREFIX + name) == data, 'original Git/native capture mismatch: ' + name)
        base, fetch_validation = fetch_main()
        for prefix in (PREFIX, PUB_PREFIX):
            require(not git('ls-tree', '--name-only', base, '--', prefix.rstrip('/')).strip(),
                    'selected target already exists on remote main; reconcile without overwrite')
        patched, queue_patch = patch_queue(git('show', base + ':' + QPATH), args.doi, inputs['snapshot']['queue_row'])
        now = utc(); publication = build_publication(inputs, args.doi, now)
        tmp_root = A / 'tmp'; tmp_root.mkdir(exist_ok=True)
        require(not tmp_root.is_symlink(), 'temporary root is linked')
        with tempfile.TemporaryDirectory(prefix='integration-', dir=tmp_root) as temporary:
            replay = capture_replay(inputs, temporary, publication)
            tree = git('rev-parse', base + '^{tree}').decode().strip()
            tree = splice(tree, PREFIX.rstrip('/'), b'040000 tree ' + files_tree(inputs['original']).encode())
            tree = splice(tree, PUB_PREFIX.rstrip('/'), b'040000 tree ' + files_tree(publication).encode())
            tree = splice(tree, QPATH, b'100644 blob ' + git('hash-object', '-w', '--stdin', input=patched).strip())
            expected = {QPATH: patched} | {PREFIX + n: d for n, d in inputs['original'].items()} | {PUB_PREFIX + n: d for n, d in publication.items()}
            changed = git('diff', '--name-only', '-z', base, tree).split(b'\0')
            changed = [name.decode() for name in changed if name]
            require(set(changed) == set(expected), 'integration tree changed paths outside the exact target allowlist')
            for name, data in expected.items():
                require(git('show', tree + ':' + name) == data, 'proposed tree bytes differ: ' + name)
            require(git('diff', '--numstat', base, tree, '--', QPATH).decode().split()[:2] == ['1', '1'], 'queue change is not one selected row')
            commit = git('commit-tree', tree, '-p', base, '-p', head,
                         input=b'Accept PR662 qualitative pre-Schwarzian note with bounded priority disclosures\n').decode().strip()
        require(local_state() == initial, 'shared checkout/index changed during preparation; abort push')
        receipt = {'schema': 'pr662-scoped-integration-receipt-v1', 'prepared_utc': now, 'pr': PR,
            'problem_id': PROBLEM, 'branch': BRANCH, 'historical_candidate_commit': ORIGINAL,
            'main_base': base, 'existing_pr_head': head, 'integration_commit': commit, 'tree': tree,
            'doi': args.doi, 'changed_paths': changed, 'queue_patch': queue_patch,
            'native_files': 24, 'native_all_bytes_unchanged': True,
            'attempt_sha256': {n: sha(d) for n, d in sorted(inputs['original'].items())},
            'publication_sha256': {n: sha(d) for n, d in sorted(publication.items())},
            'publication_validation': inputs['validation'], 'proposed_tree_replay': replay,
            'main_fetch': fetch_validation,
            'shared_checkout_and_index_untouched': True, 'whole_repository_index_created': False,
            'helper_sha256': sha(regular_bytes(Path(__file__).absolute())), 'pushed': False}
        write_json(A / 'INTEGRATION_PREPARED_RECEIPT.json', receipt)
        if args.push:
            require(check_known_head(pr_metadata()) == head, 'PR head changed after preparation')
            remote_main = git('ls-remote', '--exit-code', 'origin', 'refs/heads/main').decode().split()[0]
            require(remote_main == base, 'remote main advanced; rebuild against latest main')
            require(local_state() == initial, 'shared checkout/index drifted before push')
            write_json(PUSH_INTENT, {'schema': 'pr662-push-intent-v1', 'dispatch_utc': utc(),
                       'doi': args.doi, 'branch': BRANCH, 'expected_old_head': head,
                       'integration_commit': commit, 'outcome': 'unconfirmed; read remote branch before any retry'})
            git('push', 'origin', commit + ':refs/heads/' + BRANCH)
            receipt.update(pushed=True, pushed_utc=utc())
            write_json(PUSHED_RECEIPT, receipt)
            branch_head = git('ls-remote', '--exit-code', 'origin', 'refs/heads/' + BRANCH).decode().split()[0]
            require(branch_head == commit, 'push success but branch readback differs; receipt saved, reconcile without retry')
            after = pr_metadata()
            receipt['remote_branch_head_verified'] = True
            receipt['github_metadata_head_verified'] = after.get('headRefOid') == commit and after.get('state') == 'OPEN'
            receipt['github_metadata_readback_pending'] = not receipt['github_metadata_head_verified']
            write_json(PUSHED_RECEIPT, receipt)
            write_json(PUSH_INTENT, {'schema': 'pr662-push-intent-v1', 'confirmed_utc': utc(),
                       'doi': args.doi, 'branch': BRANCH, 'integration_commit': commit, 'outcome': 'confirmed'})
        print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
