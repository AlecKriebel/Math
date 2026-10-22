#!/usr/bin/env python3
"""Prepare a scoped PR623 merge commit using an alternate index.

Default mode creates only local objects and a review receipt. --push updates
the existing research branch without force, after a second head/main check.
The shared checkout, its selected main branch, and its index are never written.
"""
import argparse
import ast
import datetime
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import zipfile

A = Path(__file__).resolve().parent
REPO = A.parents[2]
PR = 623
PROBLEM = '30001184'
BRANCH = 'research/30001184-generation-only-gns-counterexample'
ORIGINAL = '947442c091ae617804c6a0d07b98ff2c50368798'
PREFIX = 'unsolved_math_prioritization/attempts/30001184/'
QPATH = 'unsolved_math_prioritization/QUEUE.md'
KEY = '30001184 / OWR-3392-012'
TITLE = 'Forward generation does not ensure GNS descent: an explicit continuous counterexample'
PROOF_SHA = 'f2a1b3b4233c2850d8dd79ba17b464d74343aa66e7d22d12104d17fc5470e8a3'
FROZEN_MANIFESTS = {
    'packet/SHA256SUMS.json': 'a99e4e28c91d7f51ed116f868a698e2d718fec97a4ee82cf5b94aba409100f98',
    'audit/AUDIT_SHA256SUMS.json': 'b0485e8e9a11aacfb567ad76bfb47614cebb06d4336b845939232c96427b69d3',
}
BASE_OUTER = {'README.md', 'PUBLICATION.json', 'verify_publication.py', 'test_integrity.py'}
PUB_NAMES = ('gns_generation_counterexample.pdf', 'gns_generation_counterexample.tex',
             'gns_verification.zip', 'zenodo-deposit.json')
ADDED = {'CURRENT_SOURCE_AUDIT.md', 'PUBLICATION.md', 'publication.log'} | {
    'publication/' + n for n in PUB_NAMES}
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
    return json.loads(data, object_pairs_hook=unique_pairs)


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def valid_doi(doi):
    require(type(doi) is str and re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*', doi), 'invalid Zenodo DOI')
    return doi


def safe_name(name):
    require(type(name) is str, 'path must be a string')
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in name
            and name == p.as_posix(), 'unsafe file path: ' + name)
    return name


def regular_bytes(path):
    require(not path.is_symlink() and path.is_file(), 'missing/unsafe required file: ' + str(path))
    require(not any(p.is_symlink() for p in path.parents), 'symlink parent: ' + str(path))
    return path.read_bytes()


def write_json(path, value):
    require(not path.is_symlink(), 'receipt path is a symlink')
    temp = path.with_suffix(path.suffix + '.tmp')
    require(not temp.exists() and not temp.is_symlink(), 'temporary receipt already exists')
    temp.write_bytes(json_bytes(value))
    temp.replace(path)


def git(*args, env=None, input=None):
    return subprocess.check_output(['git', *args], cwd=REPO, env=env, input=input)


def pr_metadata():
    return parse_json(subprocess.check_output(
        ['gh', 'pr', 'view', str(PR), '--json',
         'number,state,baseRefName,headRefOid,headRefName,headRepositoryOwner,isCrossRepository'], cwd=REPO))


def check_known_head(meta, doi, prior=None):
    """This gate runs before reading the live candidate, native snapshot, or paper."""
    valid_doi(doi)
    require(meta.get('number') == PR and meta.get('state') == 'OPEN', 'selected PR is not open PR623')
    require(meta.get('baseRefName') == 'main' and meta.get('headRefName') == BRANCH,
            'selected PR branch/base differs')
    require(meta.get('isCrossRepository') is False
            and meta.get('headRepositoryOwner', {}).get('login') == 'AlecKriebel', 'unexpected head repository')
    allowed = {ORIGINAL}
    if prior is not None:
        require(prior.get('schema') == 'pr623-scoped-integration-receipt-v1'
                and prior.get('pr') == PR and prior.get('problem_id') == PROBLEM
                and prior.get('branch') == BRANCH and prior.get('pushed') is True
                and prior.get('historical_candidate_commit') == ORIGINAL
                and prior.get('proof_sha256') == PROOF_SHA,
                'invalid prior successful integration receipt')
        require(re.fullmatch('[0-9a-f]{40}', prior.get('integration_commit', '')) is not None,
                'invalid prior integration commit')
        if prior.get('doi') == doi:
            allowed.add(prior['integration_commit'])
    require(meta.get('headRefOid') in allowed,
            'unreviewed PR head; abort before reading or overwriting candidate files')
    return meta['headRefOid']


def queue_row(data):
    rows = data.splitlines(keepends=True)
    matches = []
    for i, line in enumerate(rows):
        cells = line.rstrip(b'\r\n').split(b'|')
        if len(cells) > 2 and cells[2].strip() == KEY.encode():
            matches.append((i, line, cells))
    require(len(matches) == 1, 'queue must contain exactly one selected problem row')
    i, line, cells = matches[0]
    require(len(cells) == 14 and cells[1].strip() == b'651', 'unexpected selected queue row shape/rank')
    return rows, i, line, cells


def patch_queue(data, doi):
    valid_doi(doi)
    rows, i, line, cells = queue_row(data)
    require(cells[8].strip() == b'queued' and cells[9].strip() == b'0/5',
            'remote main target is no longer queued at 0/5')
    ending = b'\r\n' if line.endswith(b'\r\n') else b'\n' if line.endswith(b'\n') else b''
    cells[8] = b' claimed_solved '
    cells[9] = b' 1/5 '
    cells[11] = (" Accepted generation-only universal GNS-descent counterexample for general unital C*-E0 dilations; "
                 "explicit corollary of Burgarth-Facchi-Hillier's established clock/evaluation/translated-unitary dilation mechanism; "
                 "extensively AI-assisted, unrefereed preprint " + doi + "; no exhaustive first-priority claim. "
                 "Conditional extension after kernel invariance, stronger minimality and normal W*-promotion remain open here. "
                 "[Proof, current sources and frozen audit](attempts/30001184/README.md). ").encode()
    after = b'|'.join(cells) + ending
    new = b''.join(rows[:i] + [after] + rows[i+1:])
    require(data[:sum(map(len, rows[:i]))] == new[:sum(map(len, rows[:i]))], 'queue prefix changed')
    require(b''.join(rows[i+1:]) == b''.join(new.splitlines(keepends=True)[i+1:]), 'queue suffix changed')
    before_cells = line.rstrip(b'\r\n').split(b'|')
    require([j for j, (a, b) in enumerate(zip(before_cells, cells)) if a != b] == [8, 9, 11],
            'unexpected queue cells changed')
    return new, {'path': QPATH, 'before_sha256': sha(data), 'after_sha256': sha(new),
                 'before_bytes': len(data), 'after_bytes': len(new),
                 'before_row': line.rstrip(b'\r\n').decode(), 'after_row': after.rstrip(b'\r\n').decode(),
                 'changed_cells': ['Status', 'Turns', 'Findings'], 'all_other_bytes_unchanged': True}


def frozen_inventory(files):
    names = set()
    for manifest, expected in FROZEN_MANIFESTS.items():
        require(manifest in files and sha(files[manifest]) == expected, 'frozen manifest changed: ' + manifest)
        group = manifest.split('/')[0]
        m = parse_json(files[manifest])
        require(type(m) is dict and len(m) == (12 if group == 'packet' else 10), 'frozen manifest inventory count')
        for leaf, entry in m.items():
            safe_name(leaf)
            require('/' not in leaf and type(entry) is dict and set(entry) == {'bytes', 'sha256'}, 'frozen entry schema')
            name = group + '/' + leaf
            require(name in files and type(entry['bytes']) is int and len(files[name]) == entry['bytes']
                    and sha(files[name]) == entry['sha256'], 'frozen input bytes changed: ' + name)
            names.add(name)
        names.add(manifest)
    require(len(names) == 24 and sha(files['packet/PROOF.md']) == PROOF_SHA, 'historical proof/count mismatch')
    return names


def load_snapshot(native):
    paths = list(native.rglob('*'))
    require(not native.is_symlink() and not any(p.is_symlink() for p in paths), 'symlink in native snapshot')
    files = {p.relative_to(native).as_posix(): p.read_bytes() for p in paths if p.is_file()}
    frozen = frozen_inventory(files)
    require(set(files) == frozen | BASE_OUTER | {'PUBLICATION_MANIFEST.json'}, 'native snapshot inventory mismatch')
    require({p.relative_to(native).as_posix() for p in paths if p.is_dir()} == {'packet', 'audit'},
            'native snapshot directory mismatch')
    manifest = parse_json(files['PUBLICATION_MANIFEST.json'])
    require(manifest.get('schema') == 'math-research-publication-v1', 'original outer manifest schema')
    entries = manifest.get('files')
    require(type(entries) is list and len(entries) == 28, 'original outer inventory count')
    seen = set()
    for entry in entries:
        require(type(entry) is dict and set(entry) == {'path', 'bytes', 'sha256'}, 'outer manifest entry')
        name = safe_name(entry['path'])
        require(name not in seen and name in files and name != 'PUBLICATION_MANIFEST.json', 'outer manifest path')
        require(type(entry['bytes']) is int and len(files[name]) == entry['bytes']
                and sha(files[name]) == entry['sha256'], 'native outer hash mismatch: ' + name)
        seen.add(name)
    require(seen == frozen | BASE_OUTER, 'outer manifest names mismatch')
    return files, frozen


def archive_binding(data, original, paper_files, source):
    """Bind the immutable upload to every candidate file, paper and status prose."""
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        require(len(names) == len(set(names)) and 'PACKAGE_MANIFEST.json' in names, 'duplicate/missing archive member')
        for entry in entries:
            safe_name(entry.filename)
            require(not entry.is_dir() and (entry.external_attr >> 16) & 0o170000 != 0o120000,
                    'directory/symlink archive member')
        require(archive.testzip() is None, 'archive CRC mismatch')
        members = {name: archive.read(name) for name in names}
    manifest = parse_json(members['PACKAGE_MANIFEST.json'])
    require(type(manifest) is dict and set(manifest) == {'schema', 'file_count', 'files', 'raw_third_party_fulltexts_included'}
            and type(manifest['schema']) is int and manifest['schema'] == 1 and type(manifest['file_count']) is int
            and manifest['raw_third_party_fulltexts_included'] is False, 'package manifest schema')
    entries = manifest['files']
    require(type(entries) is list and len(entries) == manifest['file_count'] == len(members) - 1,
            'package manifest inventory count')
    seen = set()
    for entry in entries:
        require(type(entry) is dict and set(entry) == {'path', 'bytes', 'sha256'}, 'package manifest entry schema')
        name = safe_name(entry['path'])
        require(name not in seen and name in members and name != 'PACKAGE_MANIFEST.json', 'duplicate/unexpected package path')
        require(type(entry['bytes']) is int and len(members[name]) == entry['bytes']
                and sha(members[name]) == entry['sha256'], 'package member hash mismatch: ' + name)
        seen.add(name)
    require(seen == set(members) - {'PACKAGE_MANIFEST.json'}, 'extra/unmanifested package member')
    require({n for n in members if n.startswith('candidate/')} == {'candidate/' + n for n in original},
            'archive candidate must contain exactly the original 29 files')
    for name, data in original.items():
        require(members['candidate/' + name] == data, 'published archive differs from original candidate: ' + name)
    for name in ('gns_generation_counterexample.pdf', 'gns_generation_counterexample.tex'):
        require(members.get(name) == paper_files[name], 'published archive/local paper differs: ' + name)
    require(members.get('CURRENT_PRIORITY_AND_STATUS.md') == source, 'published archive/local source notice differs')
    return {'manifest_sha256': sha(members['PACKAGE_MANIFEST.json']), 'manifested_members': len(seen),
            'original_candidate_files_bound': 29, 'paper_and_source_notice_bound': True}


def publication_inputs(publication, doi, receipt_path, inspection_path, source_audit=None, original=None):
    """Return (file bytes, archive-bound notice bytes, validation) from one capture.

    Each payload, notice and receipt path is read once. All parsing, validation,
    hashes and downstream construction use those captured immutable bytes;
    later filesystem changes cannot substitute different attested contents.
    """
    valid_doi(doi)
    files = {name: regular_bytes(publication / name) for name in PUB_NAMES}
    require(files[PUB_NAMES[0]].startswith(b'%PDF-'), 'paper is not a PDF')
    receipt_bytes = tuple(regular_bytes(path) for path in (receipt_path, inspection_path))
    receipts = [parse_json(data) for data in receipt_bytes]
    expected_files = {name: {'name': name, 'size': len(files[name]), 'sha256': sha(files[name])}
                      for name in ('gns_generation_counterexample.pdf', 'gns_verification.zip')}
    for r in receipts:
        require(r.get('environment') == 'production' and r.get('state') == 'published'
                and r.get('receipt_saved') is True and r.get('title') == TITLE, 'Zenodo receipt is not confirmed production publication')
        require(r.get('doi') == doi and r.get('doi_url') == 'https://doi.org/' + doi
                and str(r.get('id')) == doi.split('.')[-1]
                and r.get('record_url') == 'https://zenodo.org/records/' + str(r.get('id')), 'Zenodo DOI/record mismatch')
        require(type(r.get('verified_utc')) is str and r['verified_utc'], 'receipt timestamp absent')
        resolution = r.get('doi_resolution', {})
        require(resolution.get('status') == 'resolved' and resolution.get('http_status') == 200,
                'DOI resolution not confirmed')
        require(type(r.get('files')) is list and len(r['files']) == 2, 'unexpected published file inventory')
        actual = {e.get('name'): e for e in r['files']}
        require(actual == expected_files, 'published/local file hashes differ')
    deposit = parse_json(files['zenodo-deposit.json'])
    require(deposit.get('metadata', {}).get('title') == TITLE, 'deposit title mismatch')
    require({e.get('path') for e in deposit.get('files', [])} == set(expected_files), 'deposit upload names mismatch')
    source = regular_bytes(source_audit or publication / 'CURRENT_PRIORITY_AND_STATUS.md')
    if original is None:
        original, _ = load_snapshot(A / 'native' / PREFIX)
    archive = archive_binding(files['gns_verification.zip'], original, files, source)
    return files, source, {'publication_receipt_sha256': sha(receipt_bytes[0]),
                   'inspection_receipt_sha256': sha(receipt_bytes[1]),
                   'archive_binding': archive, 'current_source_notice_sha256': sha(source),
                   'files': [{'path': n, 'bytes': len(d), 'sha256': sha(d)} for n, d in sorted(files.items())]}


def extend_wrapper(wrapper, expected):
    """Change only outer file/directory allowlists; retain the frozen checking body."""
    source = wrapper.decode()
    module = ast.parse(source)
    assignment = [n for n in module.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'EXPECTED' for t in n.targets)]
    require(len(assignment) == 1, 'wrapper EXPECTED assignment missing/duplicated')
    node = assignment[0]
    require(ast.literal_eval(node.value) == expected - ADDED, 'wrapper original EXPECTED differs')
    lines = source.splitlines(keepends=True)
    replacement = 'EXPECTED = {\n' + ''.join('    ' + repr(n) + ',\n' for n in sorted(expected)) + '}\n'
    source = ''.join(lines[:node.lineno-1]) + replacement + ''.join(lines[node.end_lineno:])
    needle = "dirs == {'packet', 'audit'}"
    require(source.count(needle) == 1, 'wrapper directory gate missing/duplicated')
    source = source.replace(needle, "dirs == {'packet', 'audit', 'publication'}")
    # In integrity-only mode, also bind every frozen file to its pinned inner
    # inventory, so rehashing the outer inventory cannot disguise tampering.
    needle = "    return {'integrity': 'PASS',"
    require(source.count(needle) == 1, 'wrapper integrity return missing/duplicated')
    extra = """    for manifest in FROZEN_MANIFESTS:
        group = manifest.split('/')[0]
        pinned = json.loads((HERE / manifest).read_text(), object_pairs_hook=unique_pairs)
        require(type(pinned) is dict and len(pinned) == (12 if group == 'packet' else 10), 'frozen inventory count')
        for leaf, entry in pinned.items():
            require(type(leaf) is str and '/' not in leaf and '\\\\' not in leaf and leaf not in {'', '.', '..'}, 'frozen leaf')
            require(type(entry) is dict and set(entry) == {'bytes', 'sha256'}, 'frozen entry schema')
            data = (HERE / group / leaf).read_bytes()
            require(len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'], 'frozen input changed: ' + group + '/' + leaf)
"""
    return source.replace(needle, extra + needle).encode()


def build_current_files(original, frozen, publication, source_audit, doi, now, queue_patch):
    source = source_audit.decode()
    require('Burgarth' in source and 'Facchi' in source and 'Hillier' in source
            and 'corollary' in source.lower(), 'source notice must credit BFH and corollary framing')
    notice = (f'Current publication assessment ({now}): the generation-only universal GNS-descent assertion '
              'for general unital C*-E0 dilations has an accepted explicit negative counterexample. '
              "The counterexample is an explicit corollary of Burgarth-Facchi-Hillier's established clock/evaluation/translated-unitary mechanism. "
              f'The extensively AI-assisted, unrefereed paper and exact verification archive are published at https://doi.org/{doi}. '
              'No exhaustive first-priority, independent-development or independent human peer-review claim is made. '
              'The conditional problem after imposed kernel invariance, stronger minimality and normal W*-promotion remain outside this result. '
              'All 13 original packet files and all 11 original audit files below are historical and remain byte-identical; '
              'their earlier priority/pending-review prose is superseded by CURRENT_SOURCE_AUDIT.md.\n\n')
    files = {n: d for n, d in original.items() if n != 'PUBLICATION_MANIFEST.json'}
    files['README.md'] = (notice + original['README.md'].decode()).encode()
    files['CURRENT_SOURCE_AUDIT.md'] = (notice + source).encode()
    files['PUBLICATION.md'] = ('# Published unrefereed counterexample\n\n' + notice
                              + 'Paper, source, exact verification archive and deposit metadata are in `publication/`. '
                              'Run `python3 verify_publication.py` and `python3 test_integrity.py`. '
                              'The frozen packet/audit integrity checks remain mandatory.\n').encode()
    files['publication.log'] = (f'{now} publication DOI={doi}; scoped claim accepted; BFH corollary credit; '
                                'packet13/audit11 byte-preserved; discovery/workflow completion estimate 100%; '
                                'human peer review unclaimed.\n').encode()
    meta = parse_json(original['PUBLICATION.json'])
    meta.update(publication_status='published_unrefereed_preprint', doi=doi, doi_url='https://doi.org/' + doi,
                current_source_audit='CURRENT_SOURCE_AUDIT.md',
                current_priority_assessment='Explicit generation-only counterexample corollary of Burgarth-Facchi-Hillier; no exhaustive first-priority claim',
                historical_candidate_commit=ORIGINAL, current_publication_utc=now,
                queue_edit=queue_patch, extensively_ai_assisted=True, independent_human_peer_review=False)
    files['PUBLICATION.json'] = json_bytes(meta)
    files.update({'publication/' + n: d for n, d in publication.items()})
    expected = frozen | BASE_OUTER | ADDED
    files['verify_publication.py'] = extend_wrapper(original['verify_publication.py'], expected)
    require(set(files) == expected, 'current publication inventory mismatch')
    require(all(files[n] == original[n] for n in frozen), 'historical packet/audit changed during preparation')
    files['PUBLICATION_MANIFEST.json'] = json_bytes({
        'schema': 'math-research-publication-v1',
        'files': [{'path': n, 'bytes': len(d), 'sha256': sha(d)} for n, d in sorted(files.items())]})
    return files


def local_state():
    require(git('symbolic-ref', '-q', 'HEAD').decode().strip() == 'refs/heads/main', 'shared checkout must select main')
    index_path = Path(git('rev-parse', '--git-path', 'index').decode().strip())
    if not index_path.is_absolute():
        index_path = REPO / index_path
    return {'head': git('rev-parse', 'HEAD').decode().strip(),
            'index_sha256': sha(index_path.read_bytes()) if index_path.exists() else None}


def verify_prior_tree(prior, head):
    if head == ORIGINAL:
        return
    require(prior is not None and prior['integration_commit'] == head, 'prior receipt/head mismatch')
    require(prior.get('all_frozen_bytes_unchanged') is True and prior.get('shared_checkout_and_index_untouched') is True
            and prior.get('frozen_packet_files') == 13 and prior.get('frozen_audit_files') == 11,
            'prior receipt lacks immutable/scoped integration guarantees')
    hashes = prior.get('attempt_sha256')
    require(type(hashes) is dict and len(hashes) == 36
            and all(type(v) is str and re.fullmatch('[0-9a-f]{64}', v) for v in hashes.values()),
            'prior receipt attempt inventory/hash shape')
    actual_names = git('ls-tree', '-r', '--name-only', head, '--', PREFIX).decode().splitlines()
    require(set(actual_names) == {PREFIX + safe_name(n) for n in hashes}, 'prior receipt attempt inventory differs')
    parents = git('show', '-s', '--format=%P', head).decode().split()
    require(parents == [prior['main_base'], prior['existing_pr_head']], 'prior receipt parents differ')
    changed = git('diff', '--name-only', prior['main_base'], head).decode().splitlines()
    require(changed == prior['changed_paths'] and all(p == QPATH or p.startswith(PREFIX) for p in changed),
            'prior successful integration has unexpected scope')
    prior_files = {}
    for name, expected in hashes.items():
        prior_files[name] = git('show', head + ':' + PREFIX + safe_name(name))
        require(sha(prior_files[name]) == expected, 'prior integration bytes differ')
    frozen = frozen_inventory(prior_files)
    require(set(prior_files) == frozen | BASE_OUTER | ADDED | {'PUBLICATION_MANIFEST.json'}, 'prior receipt exact allowlist differs')
    require(sha(git('show', head + ':' + QPATH)) == prior['queue_patch']['after_sha256'], 'prior integration queue differs')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--doi', required=True)
    ap.add_argument('--push', action='store_true')
    ap.add_argument('--source-audit', type=Path, default=A / 'publication/CURRENT_PRIORITY_AND_STATUS.md')
    args = ap.parse_args()
    valid_doi(args.doi)
    initial = local_state()
    prior = parse_json(regular_bytes(PUSHED_RECEIPT)) if PUSHED_RECEIPT.exists() else None
    meta = pr_metadata()
    head = check_known_head(meta, args.doi, prior)
    verify_prior_tree(prior, head)
    # Only the known head may now be inspected. Reject drift in exact scope.
    _, _, _, cells = queue_row(git('show', head + ':' + QPATH))
    require(cells[8].strip() == b'claimed_solved' and cells[9].strip() == b'1/5', 'live selected PR scope gate')
    native = A / 'native' / PREFIX
    original, frozen = load_snapshot(native)
    for name in original:
        require(git('show', ORIGINAL + ':' + PREFIX + name) == original[name], 'native differs from original immutable PR: ' + name)
    publication, source, publication_validation = publication_inputs(
        A / 'publication', args.doi, A / 'ZENODO_PUBLICATION_RECEIPT.json', A / 'ZENODO_POST_PUBLICATION_INSPECTION.json',
        args.source_audit, original)
    git('fetch', '--no-write-fetch-head', 'origin', 'refs/heads/main:refs/remotes/origin/main')
    base = git('rev-parse', 'refs/remotes/origin/main').decode().strip()
    existing = git('ls-tree', '-r', '--name-only', base, '--', PREFIX).decode().splitlines()
    require(not existing, 'target already exists on remote main; abort rather than overwrite: ' + repr(existing))
    queue = git('show', base + ':' + QPATH)
    newqueue, queue_patch = patch_queue(queue, args.doi)
    now = utc()
    files = build_current_files(original, frozen, publication, source, args.doi, now, queue_patch)
    # Disposable replay cannot write into the shared checkout or original packet.
    with tempfile.TemporaryDirectory(prefix='pr623-integration-', dir=A) as td:
        root = Path(td) / 'attempt'
        root.mkdir()
        for name, data in files.items():
            dest = root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        clean = os.environ.copy()
        clean.pop('PYTHONOPTIMIZE', None)
        clean['TMPDIR'] = td
        replay = parse_json(subprocess.check_output([sys.executable, '-I', str(root / 'verify_publication.py')], cwd=root, env=clean))
        controls = parse_json(subprocess.check_output([sys.executable, '-I', str(root / 'test_integrity.py')], cwd=root, env=clean))
        env = os.environ.copy()
        env['GIT_INDEX_FILE'] = str(Path(td) / 'index')
        git('read-tree', base, env=env)
        for name, data in {QPATH: newqueue, **{PREFIX + n: d for n, d in files.items()}}.items():
            oid = git('hash-object', '-w', '--stdin', input=data).decode().strip()
            git('update-index', '--add', '--cacheinfo', '100644,' + oid + ',' + name, env=env)
        tree = git('write-tree', env=env).decode().strip()
        changed = git('diff', '--name-only', base, tree).decode().splitlines()
        require(set(changed) == {QPATH} | {PREFIX + n for n in files}, 'integration tree has unexpected paths')
        require(git('diff', '--numstat', base, tree, '--', QPATH).decode().split()[:2] == ['1', '1'], 'QUEUE diff is not one row')
        commit = git('commit-tree', tree, '-p', base, '-p', head,
                     input=b'Accept PR623 published GNS counterexample with BFH corollary credit and scoped queue update\n').decode().strip()
    require(local_state() == initial, 'shared main/index changed; abort push and inspect concurrent local work')
    receipt = {'schema': 'pr623-scoped-integration-receipt-v1', 'prepared_utc': now,
               'pr': PR, 'problem_id': PROBLEM, 'branch': BRANCH, 'main_base': base,
               'existing_pr_head': head, 'historical_candidate_commit': ORIGINAL,
               'integration_commit': commit, 'tree': tree, 'changed_paths': changed,
               'queue_patch': queue_patch, 'proof_sha256': PROOF_SHA,
               'attempt_sha256': {n: sha(d) for n, d in sorted(files.items())},
               'frozen_packet_files': 13, 'frozen_audit_files': 11, 'all_frozen_bytes_unchanged': True,
               'current_attempt_replay': replay, 'integrity_controls': controls,
               'publication_validation': publication_validation, 'doi': args.doi,
               'shared_checkout_and_index_untouched': True, 'pushed': False,
               'helper_sha256': sha(regular_bytes(Path(__file__).resolve()))}
    write_json(A / 'INTEGRATION_PREPARED_RECEIPT.json', receipt)
    if args.push:
        # Unknown concurrent edits are never overwritten. Non-force push also
        # closes the check-to-push race against non-ancestor concurrent heads.
        live = pr_metadata()
        require(check_known_head(live, args.doi, prior) == head, 'PR head changed after preparation')
        remote_main = git('ls-remote', '--exit-code', 'origin', 'refs/heads/main').decode().split()[0]
        require(remote_main == base, 'remote main advanced after preparation; rebuild against latest main')
        require(local_state() == initial, 'shared checkout/index drifted before push')
        git('push', 'origin', commit + ':refs/heads/' + BRANCH)
        receipt['pushed'] = True
        receipt['pushed_utc'] = utc()
        # Save exact successful identity immediately; ambiguous push failures
        # leave only the prepared receipt and require read-only reconciliation.
        write_json(PUSHED_RECEIPT, receipt)
        after = pr_metadata()
        require(after.get('headRefOid') == commit and after.get('state') == 'OPEN',
                'push returned success but selected PR head readback differs; inspect receipt, do not retry blindly')
    print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
