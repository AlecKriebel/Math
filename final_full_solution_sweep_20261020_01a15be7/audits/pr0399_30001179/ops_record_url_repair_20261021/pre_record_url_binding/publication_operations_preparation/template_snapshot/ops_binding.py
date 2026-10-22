#!/usr/bin/env python3
"""PR280 constants and fail-closed custody checks; no remote mutations."""
import datetime as dt
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
REPO = ROOT.parent
PRIVATE = ROOT / 'private/pr0280_ops'
PUBLICATION = AUDIT / 'preprint/publication'
ORIGINAL = '091bdecef6f84154f5d5c205a4b07eeb6391b8f8'
ORIGINAL_PARENT = 'c053681c57cb775eaa8782312e98db430e40b43b'
PROBLEM = 'unsolved_math_prioritization/attempts/30000156'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
TITLE = 'A fixed birational map without a prime-field cycle-distribution limit'
PREFIX = 'birational-cycle-verification/'
RELEASE_SHA = '548b7a4ae1f13a92029255fc9ef485002b7c33376b9dd9168ffcdb532fc4c20e'
NAMES = {'fixed-birational-cycle-nonlimit.pdf', 'fixed-birational-cycle-nonlimit.tex',
         'fixed-birational-cycle-nonlimit-verification.zip', 'zenodo-deposit.json', 'README.md'}
UPLOADS = {'fixed-birational-cycle-nonlimit.pdf', 'fixed-birational-cycle-nonlimit-verification.zip'}
HELPERS = {'ops_binding.py', 'prepublication_check.py', 'publication_live_gates.py',
           'repository_integration.py', 'publication_lifecycle.py',
           'record_publication_ledger.py', 'verify_published_files.py'}
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
HEADERS = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']
PATTERN = re.compile(r'(?<!\d)30000156(?!\d)|OWR.?768.?006|/pull/280(?!\d)|\bPR\s*#?280(?!\d)|birational|cycle.distribution|fixed.triangular.map|Vivaldi|primitive.fib(?:er|re)s|positive.density.nonconvergence', re.I)
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(REPO / 'zenodo_deposit_tool'))
from sweep_io import atomic_json, atomic_bytes
from checkpoint import verify_destination
import zenodo


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return sha(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode())


def safe_file(root, name):
    p = PurePosixPath(name)
    if (p.is_absolute() or '..' in p.parts or p.as_posix() != name or not p.parts
            or any((root.joinpath(*p.parts[:i])).is_symlink() for i in range(1, len(p.parts)+1))):
        raise RuntimeError('Unsafe artifact path: ' + str(name))
    return root / name


def verify_entries(root, entries):
    if not isinstance(entries, list) or not entries:
        raise RuntimeError('Absent bound artifacts')
    seen = set()
    for entry in entries:
        name = entry['path']
        if name in seen or type(entry['bytes']) is not int or entry['bytes'] < 0:
            raise RuntimeError('Duplicate or invalid bound artifact')
        seen.add(name)
        data = safe_file(root, name).read_bytes()
        if len(data) != entry['bytes'] or sha(data) != entry['sha256']:
            raise RuntimeError('Bound artifact changed: ' + name)
    return seen


def release():
    path = PUBLICATION / 'RELEASE_FILES.json'
    if sha(path.read_bytes()) != RELEASE_SHA:
        raise RuntimeError('Release manifest differs from reviewed version; reopen operations review')
    value = json.loads(path.read_text())
    if verify_entries(PUBLICATION, value['files']) != NAMES:
        raise RuntimeError('Unexpected exact five-file publication inventory')
    if (value.get('intended_uploads') != ['fixed-birational-cycle-nonlimit.pdf',
            'fixed-birational-cycle-nonlimit-verification.zip']
            or value.get('archive_members') != 65 or value.get('archive_payloads') != 64):
        raise RuntimeError('Unexpected upload/archive inventory')
    return value


def check_zip(data):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        if len(names) != 65 or len(set(names)) != 65 or archive.testzip() is not None:
            raise RuntimeError('ZIP inventory, duplicates or CRC invalid')
        for info in archive.infolist():
            safe_file(Path('/synthetic'), info.filename)
            if info.is_dir() or (info.external_attr >> 16 & 0o170000) == 0o120000:
                raise RuntimeError('Directory or symlink ZIP member')
        declared = json.loads(archive.read(PREFIX + 'MANIFEST.json'))['files']
        if not isinstance(declared, list) or len(declared) != 64:
            raise RuntimeError('PR280 manifest must be a list of 64 payloads')
        keys = [v['path'] for v in declared]
        if len(set(keys)) != 64 or set(names) != {PREFIX+'MANIFEST.json'} | {PREFIX+p for p in keys}:
            raise RuntimeError('ZIP manifest member set differs')
        for item in declared:
            safe_file(Path('/synthetic'), item['path'])
            body = archive.read(PREFIX + item['path'])
            if len(body) != item['bytes'] or sha(body) != item['sha256']:
                raise RuntimeError('ZIP manifest payload changed: ' + item['path'])
        return {'members': 65, 'all_manifest_payloads_verified': 64, 'zip_crc_safe_unique_pass': True}


def manifest():
    release()
    path = PUBLICATION / 'zenodo-deposit.json'
    raw = json.loads(path.read_text())
    if raw.get('files') != [{'path': n, 'name': n} for n in [
            'fixed-birational-cycle-nonlimit.pdf', 'fixed-birational-cycle-nonlimit-verification.zip']]:
        raise RuntimeError('Manifest local paths/names must be the exact two adjacent uploads')
    metadata, files = zenodo.load_manifest(path)
    if (metadata['title'] != TITLE or metadata.get('version') != '1.0'
            or not any(v.get('identifier') == 'https://github.com/AlecKriebel/Math/pull/280'
                       for v in metadata.get('related_identifiers', []))):
        raise RuntimeError('Publication metadata identity changed')
    check_zip((PUBLICATION / 'fixed-birational-cycle-nonlimit-verification.zip').read_bytes())
    return metadata, files


def require_release_clearance():
    value = release()
    c = json.loads((AUDIT / 'ROOT_PUBLICATION_CLEARANCE.json').read_text())
    if (c.get('pr') != 280 or c.get('problem_id') != '30000156'
            or c.get('original_head') != ORIGINAL or c.get('publication_ready') is not True
            or c.get('unresolved_material_findings') != [] or c.get('files') != value['files']
            or c.get('release_manifest_sha256') != RELEASE_SHA
            or c.get('root_complete_reports_read_and_all_seals_verified') is not True):
        raise RuntimeError('Exact PR280 root scientific/package clearance missing')
    reviewers = c.get('sequential_new_reviewers', [])
    if (len(reviewers) < 2 or len({r['reviewer'] for r in reviewers}) != len(reviewers)
            or any(not r.get('report_path') or not r.get('seal_path') for r in reviewers)):
        raise RuntimeError('Fresh sequential reviewer report/seal binding absent')
    reviews = verify_entries(AUDIT, c.get('bound_review_artifacts'))
    if any(r[k] not in reviews for r in reviewers for k in ['report_path', 'seal_path']):
        raise RuntimeError('Every reviewer report/seal must be hash-bound')
    if verify_entries(AUDIT, c.get('bound_operational_files')) != HELPERS | {'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json'}:
        raise RuntimeError('All seven operational helpers and root lead reconciliation must be bound')
    manifest()
    return c


def fresh(value, seconds=180):
    when = dt.datetime.fromisoformat(value)
    if when.tzinfo is None:
        raise RuntimeError('Gate timestamp lacks timezone')
    age = (dt.datetime.now(dt.timezone.utc) - when).total_seconds()
    if age < -5 or age > seconds:
        raise RuntimeError('Expired or future live gate')


def schema_rows(value):
    if not isinstance(value, dict) or not isinstance(value.get('values'), list):
        raise RuntimeError('Unexpected GWS sheet wrapper')
    rows = value['values']
    if (not rows or rows[0] != HEADERS or any(not isinstance(r, list) or len(r) > 4
            or any(not isinstance(v, str) for v in r) for r in rows)):
        raise RuntimeError('Full-sheet four-column schema changed')
    return rows


def ledger_baseline(value):
    # The historical initial PR280 snapshot is {checked_at,response}; direct
    # provider values objects are also accepted explicitly, never guessed.
    if isinstance(value, dict) and set(value) == {'checked_at', 'response'}:
        return schema_rows(value['response'])
    return schema_rows(value)


def identity_projection(record):
    if not isinstance(record.get('metadata'), dict) or not isinstance(record.get('files'), list):
        raise RuntimeError('Unexpected account metadata/full files schema')
    return {'metadata': record['metadata'], 'files': record['files']}
