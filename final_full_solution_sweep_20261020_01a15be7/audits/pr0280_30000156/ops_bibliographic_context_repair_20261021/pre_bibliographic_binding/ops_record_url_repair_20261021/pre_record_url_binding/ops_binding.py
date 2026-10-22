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


# Shared conservative DOI identity recognizer.
_ASCII_LOWER=str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')
_UNRESERVED=frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~')
_TERMINATORS=frozenset(")]}>\"',;:!?&#")
_PERCENT=re.compile(r'%([0-9A-Fa-f]{2})')
_NAME=re.compile(r'10\.5281/zenodo\.([0-9]+)')
_FRAGMENT=re.compile(r'zenodo\.([0-9]+)')
_RECORD=re.compile(r'https?://(?:www\.)?zenodo\.org/(?:api/)?records?/([0-9]+)')


def ascii_lower(value):
    return value.translate(_ASCII_LOWER)


def _bounded_token(text,start,end):
    if start and (text[start-1].isalnum() or text[start-1] in '._'):
        return False
    rest=text[end:]
    if not rest:
        return True
    first=rest[0]
    if first=='.':
        tail=rest.lstrip('.')
        return not tail or tail[0].isspace() or tail[0] in _TERMINATORS
    return first.isspace() or first in _TERMINATORS


def _names(text):
    lowered=ascii_lower(text)
    return {'10.5281/zenodo.'+m.group(1) for m in _NAME.finditer(lowered)
            if _bounded_token(lowered,m.start(),m.end())}


def _review_names(text):
    lowered=ascii_lower(text)
    result={'10.5281/zenodo.'+m.group(1) for m in _FRAGMENT.finditer(lowered)
            if _bounded_token(lowered,m.start(),m.end()) and (not m.start() or lowered[m.start()-1]!='/')}
    for match in _RECORD.finditer(lowered):
        rest=lowered[match.end():]
        if _bounded_token(lowered,match.start(),match.end()) or rest.startswith('/files/'):
            # Leading-zero record-URL IDs are only conservative aliases/leads;
            # leading zeros in an actual DOI suffix are never discarded.
            result.add('10.5281/zenodo.'+str(int(match.group(1))))
    return result


def _decode(text,unreserved_only):
    def replace(match):
        character=chr(int(match.group(1),16))
        return character if not unreserved_only or character in _UNRESERVED else match.group(0)
    return _PERCENT.sub(replace,text)


def inspect_identity(value):
    if not isinstance(value,str):
        raise RuntimeError('DOI identity input must be text')
    if len(value)>1_000_000:
        raise RuntimeError('DOI identity text exceeds review bound')
    normalized=_decode(value,True)
    canonical=_names(value)|_names(normalized)
    review=_review_names(value)|_review_names(normalized)
    current=value
    depth_limited=False
    for count in range(8):
        decoded=_decode(current,False)
        if decoded==current:
            break
        current=decoded
        review|=_names(current)|_review_names(current)
    else:
        depth_limited=_decode(current,False)!=current
    malformed=False
    for token in re.findall(r'\S+',current):
        lowered=ascii_lower(token)
        if any(hint in lowered for hint in ['10.5281','zenodo.','doi.org','zenodo.org']):
            if re.search(r'%(?![0-9A-Fa-f]{2})',token):
                malformed=True
    return {'canonical_names':frozenset(canonical),'review_names':frozenset(review-canonical),
            'ambiguous_encoding':depth_limited or malformed or bool(
                re.search(r'(?<![a-z0-9.])10/[a-z0-9]+(?:$|[\s?#.,;)])',ascii_lower(current))
                or re.search(r'https?://(?:www\.)?shortdoi\.org(?:/|$)',ascii_lower(current))
                or re.search(r'https?://(?:dx\.)?doi\.org/[a-z][a-z0-9]*(?:$|[\s?#.,;)])',ascii_lower(current))),
            'scope':'Lexical identity/dedup leads only; reserved/nested encodings are not certified URI equivalence.'}


def zenodo_doi_leads(value):
    result=inspect_identity(value)
    if result['ambiguous_encoding']:
        raise RuntimeError('Unresolved DOI/URL encoding requires root identity review')
    return result['canonical_names']|result['review_names']


def target_in_row(row,identifier,family_ids=()):
    if type(identifier) is not int or identifier<=0:
        raise RuntimeError('Expected target record ID must be an exact positive integer')
    if not isinstance(row,(list,tuple)):
        raise RuntimeError('Identity row must be a sequence of text cells')
    ids={identifier}
    for value in family_ids:
        if type(value) is not int or value<=0:raise RuntimeError('Malformed family ID requires root review')
        ids.add(value)
    targets={'10.5281/zenodo.'+str(value) for value in ids}
    # Evaluate every cell so a later unresolved encoding cannot be hidden by an
    # earlier match. This recognizer never writes a canonically rewritten row.
    identities=[zenodo_doi_leads(value) for value in row]
    return any(targets & names for names in identities)


def record_identity_ids(record,identifier):
    """Target/concept/typed version-parent IDs are conservative family leads only."""
    def integer(value):
        if type(value) is int and value>0:return value
        if isinstance(value,str) and re.fullmatch('[1-9][0-9]*',value):return int(value)
        raise RuntimeError('Malformed recognized record-family identity requires root review')
    if not isinstance(record,dict) or integer(record.get('id'))!=identifier:
        raise RuntimeError('Expected record-family identity missing')
    result={identifier}
    parents=set()
    def add_parent(value):
        parsed=integer(value);parents.add(parsed);result.add(parsed)
    if record.get('conceptrecid') is not None:add_parent(record['conceptrecid'])
    if record.get('conceptdoi') is not None:
        value=record['conceptdoi']
        match=re.fullmatch(r'10\.5281/zenodo\.([1-9][0-9]*)',ascii_lower(value)) if isinstance(value,str) else None
        if not match:raise RuntimeError('Unparsed concept DOI requires root identity review')
        add_parent(match.group(1))
    metadata=record.get('metadata',{})
    relations=metadata.get('relations',{})
    if not isinstance(relations,dict):raise RuntimeError('Unparsed record relations require root identity review')
    versions=relations.get('version',[])
    if not isinstance(versions,list):raise RuntimeError('Unparsed version relations require root identity review')
    for version in versions:
        parent=version.get('parent') if isinstance(version,dict) else None
        if not isinstance(parent,dict) or parent.get('pid_type')!='recid':
            raise RuntimeError('Unparsed version parent requires root identity review')
        add_parent(parent.get('pid_value'))
    if record.get('parent') is not None:
        parent=record['parent']
        if not isinstance(parent,dict) or 'id' not in parent:raise RuntimeError('Unparsed parent record requires root review')
        add_parent(parent['id'])
    if len(parents)>1:raise RuntimeError('Contradictory concept/version-parent IDs require root review')
    return sorted(result)
