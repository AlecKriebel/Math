"""Pure custody closure: stdlib only; no project/native import or execution.

Reads pinned files/ZIP payload bytes and JSON; never writes, invokes programs,
loads supplied code, accesses a network, or reruns a scientific campaign.
--preseal checks inputs/initial checkpoint before final manifest construction.
Default additionally requires the exact full final namespace and seal.
"""
import hashlib
import json
import pathlib
import stat
import sys
import zipfile
import zlib

A = pathlib.Path(__file__).resolve().parent
S = A.parent.parent / 'sources'
READY = '388fbf673c3f14886f9da3628be04a1f7c019b0d6d1c6c936fb084d8a245d972'
SOURCE_SEAL = '0b056ecf4a219a11f44b0461de41b1ba80320b950323b17e6f1e52ebd45a64bc'
INITIAL = 'd04168f39dcc41859f7b112cc8dbb677de24863e0656ae362b16a9fc98c64213'
INITIAL_MANIFEST = 'ed5dfc35d4bd955db5bd08f7e21f865a95356ff4a4cb0683b681e7fe6a0cca7c'
checks = 0


def need(ok, label):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def body(path):
    need(path.is_file() and not path.is_symlink(), 'regular nonsymlink: ' + str(path))
    return path.read_bytes()


def obj(path):
    return json.loads(body(path))


def pinned(path, digest, size=None):
    b = body(path)
    need(sha(b) == digest, 'SHA256: ' + str(path))
    if size is not None:
        need(len(b) == size, 'size: ' + str(path))
    return b


def typed_ordered_equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(typed_ordered_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(typed_ordered_equal(x, y) for x, y in zip(a, b))
    return a == b


def files(root):
    result = []
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'namespace has no symlinks: ' + str(p))
        if p.is_file():
            result.append(p)
    return result


need(sys.argv[1:] in ([], ['--preseal']), 'only supported read-only option')
preseal = sys.argv[1:] == ['--preseal']
pinned(S / 'SOURCE_READY.json', READY)
pinned(S / 'SOURCE_READY_SEAL.json', SOURCE_SEAL)
pinned(A / 'INITIAL_SEAL.json', INITIAL)
pinned(A / 'INITIAL_OWNED_MANIFEST.json', INITIAL_MANIFEST)
initial = obj(A / 'INITIAL_SEAL.json')
pinned(A / 'INPUT_MANIFEST.json', initial['input_manifest_sha256'])
inputs = obj(A / 'INPUT_MANIFEST.json')['all_original_source_files']
need(len(inputs) == 121, 'whole original source count121')
need({str(p) for p in files(S)} == {r['path'] for r in inputs}, 'exact121-source namespace')
for r in inputs:
    pinned(pathlib.Path(r['path']), r['sha256'], r['bytes'])
early = obj(A / 'INITIAL_OWNED_MANIFEST.json')['files']
need(len(early) == 14, '14 immutable early payloads')
for r in early:
    pinned(A / r['path'], r['sha256'], r['bytes'])

whole = obj(A / 'WHOLE_INPUT_BINDINGS.json')['objects']
need(len(whole) == 10, 'ten whole heterogeneous original objects')
for r in whole:
    b = pinned(pathlib.Path(r['original_path']), r['sha256'], r['bytes'])
    c = pinned(A / r['raw_copy'], r['sha256'], r['bytes'])
    need(b == c, 'raw whole-byte identity: ' + r['original_path'])
    need(typed_ordered_equal(json.loads(b), r['whole_original_json_object']),
         'whole typed ordered object: ' + r['original_path'])

r = obj(S / 'SOURCE_READY.json')
api = {q['role']: json.loads(pinned(pathlib.Path(q['path']), q['SHA256'], q['bytes']))
       for q in r['whole_native_API_objects']}
need(list(api) == ['record', 'latest', 'versions-page001', 'files'], 'API original object order')
for q in [api['record'], api['latest']] + api['versions-page001']['hits']['hits']:
    need('version' not in q['metadata'], 'native metadata.version remains ABSENT')
need(api['record']['swh'] == {} and type(api['record']['swh']) is dict, 'record emptydict swh')
need(api['latest']['swh'] == {} and type(api['latest']['swh']) is dict, 'latest emptydict swh')
need(api['versions-page001']['hits']['hits'][0]['swh'] is None, 'version swh original null')
need(type(api['versions-page001']['hits']['total']) is int and
     api['versions-page001']['hits']['total'] == 1, 'original integer version total')
need(type(api['files']['entries']) is list, 'native entries original list')
need(api['files']['order'] == [] and type(api['files']['order']) is list, 'native order emptylist')
need(api['files']['default_preview'] is None, 'native default_preview null')
need(r['HTTP_status_sequence'] == [200, 301, 200, 200, 200, 200, 200, 200], 'transport history intact')
need(r['actual_ordinary_native_HTTP_requests'] == 8 and r['logical_requests'] == 7, 'actual vs logical requests')
need(r['printed_date'] is None and r['printed_version'] is None and
     r['printed_title_date_version_inspected'] is False, 'acquirer historical unread flags unchanged')
need(r['source_programmes_executed'] == [] and r['scientific_verdict'] is None,
     'original source-only history unchanged')
assets = r['all_native_assets_in_original_order']
need(len(assets) == 3, 'all three native assets')
need([x['key'] for x in api['record']['files']] ==
     ['five_centers.pdf', 'five_centers.tex', 'verification-package.zip'], 'native asset key order')
for q in assets:
    # SOURCE_READY retains whole original native file objects and byte pins.
    p = pathlib.Path(q['path'])
    b = pinned(p, q['SHA256'], q['bytes'])
    original = q['original_api_file_object']
    need(hashlib.md5(b).hexdigest() == original['checksum'].split(':', 1)[1], 'native MD5 ' + original['key'])

archive = obj(S / 'ARCHIVE_CUSTODY.json')
need(archive['whole_regular_payload_occurrences'] == 64 and
     archive['expanded_bytes_all_depths'] == 874094 and
     archive['recursive_archive_container_count'] == 1 and
     archive['nested_archive_count'] == 0, 'whole archive scope')
rows = archive['regular_payload_occurrences']
need(len(rows) == 64 and len({x['original_member_name'].casefold() for x in rows}) == 64,
     'all64 unique casefold-safe regular members')
c = archive['containers'][0]
with zipfile.ZipFile(c['input_path'], 'r') as z:
    members = [i for i in z.infolist() if not i.is_dir()]
    need(len(members) == 64, 'actual ZIP full regular member count')
    for i, row in zip(members, rows):
        parts = pathlib.PurePosixPath(i.filename)
        need(not parts.is_absolute() and '..' not in parts.parts and '\\' not in i.filename,
             'safe exact member name')
        need(i.filename == row['original_member_name'], 'ZIP original member order')
        mode = i.external_attr >> 16
        need(stat.S_IFMT(mode) in (0, stat.S_IFREG), 'regular ZIP mode')
        b = z.read(i)  # zipfile validates CRC; also compare recorded native CRC explicitly.
        need(len(b) == row['bytes'] == i.file_size and sha(b) == row['SHA256'], 'whole ZIP bytes')
        need(format(zlib.crc32(b) & 0xffffffff, '08x') == row['CRC32'] == format(i.CRC, '08x'),
             'native ZIP CRC32')
        need(body(pathlib.Path(row['extracted_path'])) == b, 'whole extracted payload identity')
        need(not b.startswith((b'PK\x03\x04', b'\x1f\x8b')), 'no nested ZIP/GZIP payload magic')
need(body(S / 'assets/five_centers.pdf') == body(S / 'published-source/asset-003/five_centers.pdf'),
     'whole standalone/embedded PDF identity')
need(body(S / 'assets/five_centers.tex') == body(S / 'published-source/asset-003/five_centers.tex'),
     'whole standalone/controlling TeX identity')
need(len(body(S / 'published-source/asset-003/five_centers.tex').splitlines()) == 285, 'full285 controlling lines')
own = obj(A / 'independent-dyadic.stdout.json')
need(own['own_checks'] == 8963 and own['certified_dyadic_radical_endpoints'] == 3774,
     'bound own recorded interval-check scope; no rerun')
need(body(A / 'independent-dyadic.stderr') == b'', 'own recorded empty stderr')

owned_count = None
if not preseal:
    seal = obj(A / 'SEAL.json')
    pinned(A / 'OWNED_MANIFEST.json', seal['owned_manifest_sha256'])
    manifest = obj(A / 'OWNED_MANIFEST.json')['files']
    names = [x['path'] for x in manifest]
    need(len(names) == len(set(names)), 'unique complete owned paths')
    actual = {str(p.relative_to(A)) for p in files(A)} - {'OWNED_MANIFEST.json', 'SEAL.json'}
    need(actual == set(names), 'exact final namespace; only exact root terminal files excluded')
    need(seal['owned_payload_count'] == len(manifest), 'whole final owned count')
    for row in manifest:
        rel = pathlib.PurePosixPath(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts, 'owned path bounded')
        pinned(A / row['path'], row['sha256'], row['bytes'])
    for name in ['REPORT.md', 'VERDICT.json', 'DERIVATION.md', 'PRIMARY_READ_LEDGER.md', 'verify_read_only.py']:
        pinned(A / name, seal['critical_files_sha256'][name])
    need(obj(A / 'VERDICT.json')['follow_up'] is None, 'literal null follow-up')
    owned_count = len(manifest)

print(json.dumps({'mode': 'preseal' if preseal else 'final', 'custody_checks': checks,
                  'unchanged_original_source_files': 121, 'whole_original_objects': 10,
                  'immutable_initial_payloads': 14, 'whole_ZIP_regular_payloads': 64,
                  'native_version_field': 'ABSENT', 'native_assets': 3,
                  'actual_HTTP_requests': 8, 'logical_requests': 7,
                  'owned_payload_count': owned_count, 'source_scientific_execution': False,
                  'network_or_writes_or_subprocesses': False}, indent=2))
