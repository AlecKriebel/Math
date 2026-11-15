"""Bounded byte/schema custody only. Standard library; no project imports.

No writes, network, subprocess, exec/eval, supplied-program import or science run.
With --inputs-only, authenticate immutable inputs/initial and original objects.
With no argument, additionally authenticate the complete final owned seal.
The externally reported SHA256 of SEAL.json is the independent trust anchor.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile
import zlib

ROOT = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A = ROOT / 'papers/23331295/reviews/scope'
S = ROOT / 'papers/23331295/sources'
checks = 0


def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def raw(path):
    require(path.is_file() and not path.is_symlink(), 'regular: ' + str(path))
    require(path.stat().st_size <= 20_000_000, 'bounded file: ' + str(path))
    return path.read_bytes()


def obj(path):
    return json.loads(raw(path))


def bound(path, entry):
    b = raw(path)
    require(len(b) == entry['bytes'], 'size: ' + str(path))
    require(digest(b) == entry.get('sha256', entry.get('SHA256')), 'SHA: ' + str(path))


def safe_rel(value):
    p = PurePosixPath(value)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in value,
            'safe relative name: ' + value)
    return p


def typed_ordered(x):
    # Equality of JSON values alone would conflate bool/int and lose key order.
    if isinstance(x, dict):
        return ('dict', tuple((k, typed_ordered(v)) for k, v in x.items()))
    if isinstance(x, list):
        return ('list', tuple(typed_ordered(v) for v in x))
    return (type(x).__name__, x)


require(sys.argv[1:] in ([], ['--inputs-only']), 'single bounded mode')
require(digest(raw(S / 'SOURCE_READY.json')) ==
        '1380f9b64a17e237a38020778bc84b38984bfc6d1c05ae6acf5dd5516b665092', 'SOURCE_READY pin')
require(digest(raw(S / 'SOURCE_READY_SEAL.json')) ==
        'e683dda6b1cf61c87807214fe3602605f0fa9eed1118835141f39044f1e85b2b', 'source seal pin')
inputs = obj(A / 'INPUT_MANIFEST.json')
source_rows = inputs['all_original_source_files']
require(len(source_rows) == 65, 'source count65')
source_set = set()
for row in source_rows:
    p = Path(row['path'])
    require(p.is_relative_to(S), 'source path scope')
    require(str(p) not in source_set, 'source uniqueness')
    source_set.add(str(p))
    bound(p, row)
actual_sources = {str(p) for p in S.rglob('*') if p.is_file()}
require(actual_sources == source_set, 'complete unchanged source file set')

require(digest(raw(A / 'INITIAL_SEAL.json')) ==
        '49f50417235d2054ad23f7482149ba1707d3021ac7d273b4082b8dcb8bd21cb1', 'initial seal pin')
require(digest(raw(A / 'INITIAL_OWNED_MANIFEST.json')) ==
        '5500f2d1e1f0a5998f607a75edeb6715ca463094b9b7a50cb1f8f7ef20b40c4e', 'initial manifest pin')
initial = obj(A / 'INITIAL_SEAL.json')
im = obj(A / 'INITIAL_OWNED_MANIFEST.json')
require(len(im['files']) == 12, 'initial12 payloads')
for row in im['files']:
    bound(A / str(safe_rel(row['path'])), row)
require(initial['root128_gate'] == 'CLOSED' and
        initial['samework_foreign_native_code_results_or_opinions_read_before_seal'] is False,
        'original independent historical gate retained')

ready = obj(S / 'SOURCE_READY.json')
native = obj(S / 'record.response.body')
verdict = obj(A / 'VERDICT.json')
require(typed_ordered(verdict['whole_original_source_ready_object']) == typed_ordered(ready),
        'whole SOURCE_READY types/order/null/history preserved')
require(typed_ordered(verdict['whole_original_native_record_object']) == typed_ordered(native),
        'whole native record types/order/null/history preserved')
require(typed_ordered(verdict['whole_original_initial_verdict']) ==
        typed_ordered(obj(A / 'INITIAL_VERDICT.json')), 'whole initial verdict preserved')
require(ready['printed_version'] is None and ready['printed_date'] is None and
        ready['mathematical_PDF_TeX_or_pixels_read'] is False, 'historical unread/null flags retained')
require(verdict['current_lane_reading']['manuscript']['printed_version'] is None,
        'no printed version invented from API1.0')
require(ready['version'] == '1.0' and ready['all_enumerated_version_ids'] == [23331295],
        'native sole version')
require(ready['HTTP_status_sequence'] == [200, 301, 200, 200, 200, 200, 200, 200],
        'transport301 history preserved')
require(ready['native_schema_distinctions']['record_swh']['original_value'] == {} and
        ready['native_schema_distinctions']['versions_swh_fields'][0]['original_value'] is None,
        'empty object distinct from null')
assets = ready['all_native_assets_in_original_order']
require([x['original_api_file_object']['key'] for x in assets] ==
        ['nullstellensatz.tex', 'verification-package.zip', 'nullstellensatz.pdf'], 'native asset order')
for row in assets:
    bound(Path(row['path']), row)
    b = raw(Path(row['path']))
    expected_md5 = row['original_api_file_object']['checksum'].removeprefix('md5:')
    require(hashlib.md5(b).hexdigest() == expected_md5, 'native MD5 ' + row['path'])
    require(b == raw(Path(row['transport_body_path'])), 'asset matches actual transport body')

archive = S / 'assets/verification-package.zip'
expanded = 0
with zipfile.ZipFile(archive) as z:
    infos = z.infolist()
    require(len(infos) == 15, 'whole15 ZIP entries')
    names = set()
    for row in infos:
        rel = safe_rel(row.filename)
        require(not row.is_dir() and row.filename.casefold() not in names,
                'regular/noncolliding ZIP name')
        names.add(row.filename.casefold())
        mode = (row.external_attr >> 16) & 0o170000
        require(mode in (0, stat.S_IFREG), 'ZIP no symlink/special')
        require(row.file_size <= 2_000_000, 'bounded ZIP member')
        b = z.read(row)
        expanded += len(b)
        require(len(b) == row.file_size, 'full ZIP size')
        require((zlib.crc32(b) & 0xffffffff) == row.CRC, 'whole ZIP CRC')
        require(b == raw(S / 'published-source/asset-002' / str(rel)), 'whole extracted match')
        require(not b.startswith(b'%PDF-') and not row.filename.lower().endswith('.pdf'),
                'no embedded PDF')
        require(not b.startswith((b'PK\x03\x04', b'\x1f\x8b')), 'no nested ZIP/gzip')
require(expanded == 112790, 'whole expanded bytes')
tex = raw(S / 'assets/nullstellensatz.tex')
require(tex == raw(S / 'published-source/asset-002/nullstellensatz.tex'), 'standalone/control TeX exact')
require(len(tex.splitlines()) == 235, 'whole235 TeX lines')
require(ready['embedded_PDFs'] == [], 'whole no embeddedPDF list')
require(obj(A / 'independent-exact.stdout.json')['independent_exact_checks'] == 1998,
        'preserved own1998 result; not rerun')
require(raw(A / 'independent-exact.stderr') == b'', 'preserved empty own stderr')

owned_count = None
if not sys.argv[1:]:
    seal = obj(A / 'SEAL.json')
    require(digest(raw(A / 'OWNED_MANIFEST.json')) == seal['owned_manifest_sha256'],
            'final owned manifest binding')
    manifest = obj(A / 'OWNED_MANIFEST.json')
    owned = set()
    require(len(manifest['files']) <= 100, 'bounded owned count')
    for row in manifest['files']:
        rel = str(safe_rel(row['path']))
        require(rel not in owned, 'owned unique')
        owned.add(rel)
        bound(A / rel, row)
    actual = {str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()}
    require(actual == owned | {'OWNED_MANIFEST.json', 'SEAL.json'}, 'exact final owned file set')
    for name, key in [('REPORT.md', 'report_sha256'), ('VERDICT.json', 'verdict_sha256'),
                      ('DERIVATION.md', 'derivation_sha256'),
                      ('verify_custody_read_only.py', 'custody_helper_sha256')]:
        require(digest(raw(A / name)) == seal[key], 'direct seal ' + name)
    require(seal['initial_seal_sha256'] == digest(raw(A / 'INITIAL_SEAL.json')), 'initial bound by final')
    owned_count = len(owned)
print(json.dumps({'custody_checks': checks, 'source_files_unchanged': len(source_rows),
                  'initial_payloads_unchanged': 12, 'ZIP_regular_payloads': 15,
                  'ZIP_expanded_bytes': expanded, 'owned_payloads': owned_count,
                  'whole_original_object_types_order_null_history_preserved': True,
                  'mode': 'inputs-only' if sys.argv[1:] else 'final',
                  'project_imports': 0, 'network': 0, 'exec_or_subprocess': 0,
                  'file_writes': 0, 'science_execution': 0}, indent=2))
