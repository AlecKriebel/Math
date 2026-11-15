"""Minimal frozen-input/copy/object custody; standard library only.

No project imports, writes, network, subprocess, eval/exec, scientific or owner
checker execution. --inputs-only precedes final sealing; default also checks
this audit's exact full owned namespace. This is not a scientific test suite.
"""
import hashlib
import json
from pathlib import Path
import sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A = P / 'verification/nash-quotient-robinson-editorial-fact-audit-sol-20261115'
RECS = (23578599, 23423736, 23333002)
CONFIG = ('config', 'configs', '')
checks = 0
objects = 0


def need(ok, label):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(label)


def raw(path):
    path = Path(path)
    need(path.is_file() and not path.is_symlink(), 'regular ' + str(path))
    need(path.stat().st_size < 12_000_000, 'bounded ' + str(path))
    return path.read_bytes()


def read(path):
    return json.loads(raw(path))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def typed(x):
    if isinstance(x, dict):
        return ('dict', tuple((k, typed(v)) for k, v in x.items()))
    if isinstance(x, list):
        return ('list', tuple(typed(v) for v in x))
    return (type(x).__name__, x)


def same(a, b, label):
    global objects
    objects += 1
    need(typed(a) == typed(b), label)


def pin(row):
    b = raw(row['path'])
    need(len(b) == row['bytes'] and sha(b) == row.get('SHA256', row.get('sha256')),
         'byte pin ' + row['path'])
    return b


def wrappers(x, budget):
    # Actual heterogeneous wrappers, without normalizing their stored values.
    budget[0] -= 1
    if budget[0] < 0:
        raise AssertionError('bounded object traversal')
    if isinstance(x, dict):
        if 'whole_literal_object' in x and 'path' in x:
            same(x['whole_literal_object'], json.loads(pin(x)), 'whole literal ' + x['path'])
        if 'whole_original_object' in x and isinstance(x.get('file'), dict):
            same(x['whole_original_object'], json.loads(pin(x['file'])), 'whole original API')
        for key, desc in [('whole_original_custom_verdict', 'verdict_file'),
                          ('whole_original_review_seal', 'seal_file')]:
            if key in x and desc in x:
                same(x[key], json.loads(pin(x[desc])), 'whole scientific record ' + desc)
        for v in x.values():
            wrappers(v, budget)
    elif isinstance(x, list):
        for v in x:
            wrappers(v, budget)


need(sys.argv[1:] in ([], ['--inputs-only']), 'bounded mode')
inputs = read(A / 'INPUT_MANIFEST.json')
need(len(inputs['files']) == 613, 'all613 original input bindings')
for row in inputs['files']:
    pin(row)
for rec, code in zip(RECS, CONFIG):
    s = P / ('papers/%s/sources' % rec)
    e = P / ('papers/%s/reviews/editorial' % rec)
    for root in (s, e):
        expected = {x['path'] for x in inputs['files'] if Path(x['path']).is_relative_to(root)}
        actual = {str(f) for f in root.rglob('*') if f.is_file()}
        need(actual == expected, 'complete namespace including ALL terminal names ' + str(root))
    need(sha(raw(e / 'SEAL.json')) == inputs['editorial_seal_pins'][str(rec)], 'editorial seal pin')
    ready = read(s / 'SOURCE_READY.json')
    pub = read(e / code / 'publication.json')
    promotion = read(e / code / 'promotion.json')
    protocol = read(e / 'SOURCE_PROTOCOL_BINDINGS.json')
    for x in (pub, promotion, protocol):
        wrappers(x, [150000])
    if 'source_binding' in pub:
        same(pub['source_binding'], protocol, 'whole private source binding')
    need(pub['publication_date'] == ready['publication_date'] and pub['version'] == ready['version'],
         'declared date/version')
    need(pub['canonical_url'] is None and pub['AA'] is None and pub['follow_up'] is None,
         'private authority/null follow-up')
    for asset in ready['all_native_assets_in_original_order']:
        key = asset['original_api_file_object']['key']
        need(raw(e / 'candidate/assets' / key) == raw(asset['path']), 'complete native asset identity')
    bib = raw(e / 'candidate/assets/citation.bib').decode('utf-8')
    need(pub['prepared_bibtex'] == bib, 'complete prepared BibTeX')
    if rec == 23333002:
        mappings = {'whole_original_SOURCE_READY': 'SOURCE_READY.json',
                    'whole_original_transport_aggregate': 'ALL_TRANSPORT_RECEIPTS.json',
                    'whole_original_archive_custody': 'ARCHIVE_CUSTODY.json',
                    'whole_original_native_schema_types': 'NATIVE_SCHEMA_TYPES.json',
                    'whole_original_source_terminal_seal': 'SOURCE_READY_SEAL.json'}
        for key, name in mappings.items():
            same(protocol[key], read(s / name), 'whole125 ' + name)
        metadata = pub['review_metadata']
        same(metadata['whole_root_scientific_clearance'],
             read(P / 'verification/root-clearance-23333002-20261115.json'), 'whole125 root authority')
        need(metadata['whole_root_scientific_review'] ==
             raw(P / 'papers/23333002/reviews/root/ROOT_REVIEW_20261115.md').decode('utf-8'), 'whole125 root text')
    if rec == 23423736:
        m = pub['review_metadata']
        same(m['whole_root_scientific_clearance_record'],
             read(P / 'verification/root-clearance-23423736-20261115.json'), 'whole124 root authority')
        need(m['root_review_whole_text'] ==
             raw(P / 'papers/23423736/reviews/root/ROOT_REVIEW_20261115.md').decode('utf-8'), 'whole124 root text')

copies = read(A / 'RAW_LITERAL_INPUTS.json')['raw_byte_identical_copies']
for row in copies:
    b = raw(row['original_path'])
    need(b == raw(A / row['copy_path']) and len(b) == row['bytes'] and sha(b) == row['SHA256'],
         'exact fresh raw-copy identity')
owned = None
if not sys.argv[1:]:
    seal = read(A / 'SEAL.json')
    need(sha(raw(A / 'OWNED_MANIFEST.json')) == seal['owned_manifest_sha256'], 'own final manifest pin')
    manifest = read(A / 'OWNED_MANIFEST.json')
    need(len(manifest['files']) < 150, 'bounded own files')
    expected = {'OWNED_MANIFEST.json', 'SEAL.json'}
    for row in manifest['files']:
        rel = Path(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts, 'safe own path')
        expected.add(str(rel))
        b = raw(A / rel)
        need(len(b) == row['bytes'] and sha(b) == row['SHA256'], 'own file binding')
    need({str(f.relative_to(A)) for f in A.rglob('*') if f.is_file()} == expected,
         'full own namespace, no recursive basename exclusion')
    owned = len(manifest['files'])
print(json.dumps({'checks': checks, 'original_input_files': 613,
                  'source_files_by_record': {'23578599': 58, '23423736': 232, '23333002': 122},
                  'complete_editorial_namespace_files_by_record': {'23578599': 56, '23423736': 62, '23333002': 77},
                  'full_namespace_guards': 6, 'root_clearance_review_files': 6,
                  'native_assets_exactly_equal': 6, 'whole_typed_ordered_object_comparisons': objects,
                  'fresh_byte_identical_raw_copies': len(copies), 'owned_payloads': owned,
                  'scientific_or_owner_tests_executed': 0, 'project_imports': 0,
                  'network': 0, 'file_writes': 0, 'mode': 'inputs-only' if sys.argv[1:] else 'final'}, indent=2))
