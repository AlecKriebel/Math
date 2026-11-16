"""Independent default offline custody only; no imports of supplied/project code.
Fixed reference reads and stdout; no network, subprocesses or filesystem writes.
No renderer, numerical/scientific/native/archive execution. No assert controls.
"""
from pathlib import Path
import difflib
import hashlib
import html
import json
import os
import re
import stat
import sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R = P / 'verification/outer-pedal-editorial-correction-v2-fact-audit-sol-20261115'
N = P / 'verification/outer-pedal-editorial-correction-v2-sol-20261115'
E = P / 'papers/23331331/reviews/editorial'
F = P / 'verification/outer-pedal-editorial-fact-audit-sol-20261115'
S = P / 'papers/23331331/sources'
TERMS = ['FINAL_CLOSURE.json', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json']
CHECKS = 0
NODES = 0


def need(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    need(path.is_absolute() and path.is_relative_to(P) and '.git' not in path.parts,
         'Fixed project reference boundary')
    need(path.resolve() == path and stat.S_ISREG(path.lstat().st_mode),
         'Ordinary reference, no symlink or special file')
    return path.read_bytes()


def bound(path, item):
    data = read(path)
    need(type(item['bytes']) is int and type(item['SHA256']) is str,
         'Whole pin schema types')
    need(len(data) == item['bytes'] and sha(data) == item['SHA256'], 'Whole buffer pin: ' + str(path))
    return data


def load(path):
    return json.loads(read(path))


def typed(a, b):
    global NODES
    NODES += 1
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(typed(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(typed(x, y) for x, y in zip(a, b))
    return a == b


def extent(root):
    need(root.resolve() == root and stat.S_ISDIR(root.lstat().st_mode), 'Ordinary root')
    files, dirs = [], []

    def walk(parent):
        for entry in os.scandir(parent):
            path = Path(entry.path)
            name = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.append(name)
                walk(path)
            else:
                need(stat.S_ISREG(mode), 'No symlink/special namespace object')
                files.append(name)

    walk(root)
    return sorted(files), sorted(dirs)


def close(root, rows, dirs, terminals=()):
    files, actual_dirs = extent(root)
    expected = sorted(list(rows) + list(terminals))
    need(files == expected and len(expected) == len(set(expected)), 'Exact closed file namespace')
    need(actual_dirs == sorted(dirs) and len(dirs) == len(set(dirs)), 'Exact closed directory namespace')
    for name in terminals:
        need('/' not in name, 'Only exact root terminal names')
        read(root / name)
    return len(files), len(actual_dirs)


def old_namespace(root, expected, fact=False):
    sb = read(root / 'FINAL_SEAL.json')
    need(sha(sb) == expected, 'Immutable old FINAL')
    seal = json.loads(sb)
    name = 'FINAL_MANIFEST.json' if fact else 'OWNED_MANIFEST.json'
    descriptor = seal['manifest' if fact else 'OWNED_MANIFEST']
    manifest = json.loads(bound(root / name, descriptor))
    entries = manifest['payload_files' if fact else 'files']
    rows = {item['path']: item for item in entries}
    need(len(rows) == len(entries), 'No duplicate original namespace entries')
    dirs = manifest['declared_directories' if fact else 'directories']
    counts = close(root, rows, dirs, [name, 'FINAL_SEAL.json'])
    for name, item in rows.items():
        bound(root / name, item)
    if fact:
        need(seal['status'] == 'NO_GO_EDITORIAL_COPY_FACT_TRANSCRIPTION', 'Old literal NO_GO retained')
    return rows, counts


def main():
    need(len(sys.argv) == 1, 'Only pure default mode')
    manifest = load(R / 'FINAL_MANIFEST.json')
    need(manifest['owned_root'] == str(R) and manifest['exact_root_terminal_exclusions'] == TERMS,
         'Exact owned root terminal contract')
    need(manifest['subtree_exclusions'] == [] and manifest['future_exclusions'] == [] and
         manifest['recursive_basename_exclusions'] is False, 'No future/subtree/basename holes')
    rows = {item['path']: item for item in manifest['payload_files']}
    need(list(rows) == sorted(rows) and len(rows) == len(manifest['payload_files']), 'Unique ordered own paths')
    owned_counts = close(R, rows, manifest['directories'], TERMS)
    for name, item in rows.items():
        bound(R / name, item)
    receipt = load(R / 'OWN_CUSTODY_HELPER_READ.json')
    bound(R / 'verify_audit_custody.py', receipt)
    need(receipt['entire_current_body_read_before_execution'] is True, 'Current own pure full read')
    initial_bytes = read(R / 'INITIAL_SEAL.json')
    need(sha(initial_bytes) == '21510a0e26481abb25fea3c889870e52b743c6a44283f41ee2eaeb923f8e58d2',
         'Immutable independent informed initial')
    for item in json.loads(initial_bytes)['files']:
        bound(Path(item['path']), item)
    initial_inputs = load(R / 'INITIAL_INPUTS.json')
    for item in initial_inputs['source_root_original_history_reference_pins']:
        bound(Path(item['path']), item)
    source_rows = initial_inputs['all_original_source_namespace_full_byte_pins']
    close(S, [str(Path(item['path']).relative_to(S)) for item in source_rows],
          initial_inputs['source_directories'])
    for item in source_rows:
        bound(Path(item['path']), item)
    refs = load(R / 'REFERENCE_CUSTODY.json')
    for item in refs['new_writer_complete_finite_files'] + refs['old_full_namespace_seals_and_manifests']:
        bound(Path(item['path']), item)
    bound(E / 'SOURCE_INPUTS.json', refs['all421_original_contract_reference'])
    ns = read(N / 'FINAL_SEAL.json')
    need(sha(ns) == 'd2be444e52e3049ad2179124f42418e720fcac95c19ab66d4d6db770aaddb710',
         'Exact forwarded new writer FINAL')
    new_seal = json.loads(ns)
    mb = read(N / 'OWNED_MANIFEST.json')
    need(sha(mb) == new_seal['manifest_SHA256'] ==
         'b6e35f4082c3b477476986dce0af7e6391313c8f307955ff352f70c37dc222be', 'New whole manifest')
    nm = json.loads(mb)
    need(nm['exact_root_terminal_exclusions'] == ['OWNED_MANIFEST.json', 'FINAL_SEAL.json'] and
         nm['future_subtree_exclusions'] == [], 'New exact boundary')
    new_counts = close(N, nm['payloads'], nm['directories'], ['OWNED_MANIFEST.json', 'FINAL_SEAL.json'])
    need(new_counts == (41, 7), 'Forwarded exact new writer extent')
    for name, item in nm['payloads'].items():
        bound(N / name, item)
    old_rows, old_counts = old_namespace(E, 'a6199b1d554dcfaae1201c2440ec0b92d97caf5c6d71fc6e24919bf781e898a5')
    _, fact_counts = old_namespace(F, 'fea1ae8be0c778bb6b0a2cb6ed60cb4d4c492c5ae7a306fc098ef7d67f3a9e7b', True)
    need(old_counts == (328, 8) and fact_counts == (799, 76), 'Complete old extents')
    originals = load(E / 'SOURCE_INPUTS.json')
    need(len(originals['original_files']) == 421, 'Whole original reference count')
    source_json = 0
    for item in originals['original_files']:
        a = bound(Path(item['path']), item)
        b = bound(E / item['copy'], item)
        need(a == b, 'Every original whole copy unchanged')
        if Path(item['path']).is_relative_to(S) and Path(item['path']).suffix == '.json':
            need(typed(json.loads(a), json.loads(b)), 'Whole source JSON types/key/list orders')
            source_json += 1
    namespace_counts = []
    for item in originals['namespaces']:
        count = close(Path(item['root']), [row['path'] for row in item['files']], item['directories'])
        namespace_counts.append({'root': item['root'], 'files': count[0], 'directories': count[1]})
    need(typed(originals['whole_original_SOURCE_READY'], load(S / 'SOURCE_READY.json')),
         'Whole original READY/history retained')
    need(typed(originals['whole_root_authority'], load(P / 'verification/root-clearance-23331331-20261115.json')),
         'Whole root authority typed/history retained')
    core_path = Path(refs['qualified_core_reference']['path'])
    core = json.loads(bound(core_path, refs['qualified_core_reference']))
    need(core['original17_plus_sole_authorized405b_checkpoint'] is True and
         core['all18_original_unchanged_claim'] is False and len(core['files']) == 18,
         'Qualified core contract, no global cache obligation')
    for item in core['files']:
        bound(Path(item['path']), item)
    oracle = load(R / 'SOURCE_DERIVED_ORACLES.json')
    diff = []
    corrected = []
    for item in oracle['seven_mechanical_whole_buffer_oracles']:
        name = item['original_relative_path']
        old = bound(E / name, item['whole_original_buffer'])
        before = item['whole_original_paragraph'].encode()
        after = item['exact_replacement_paragraph'].encode()
        for folder in ['overlay-normal', 'overlay-optimized']:
            new = read(N / folder / name)
            need(len(new) == item['expected_complete_corrected_buffer_bytes'] and
                 sha(new) == item['expected_complete_corrected_buffer_SHA256'], 'Independent frozen whole-buffer expectation')
            need(old.count(before) == new.count(after) == 1 and new.replace(after, before, 1) == old,
                 'Exact paragraph reverse patch recovers every old whole byte')
            need(new == read(N / 'overlay-normal' / name), 'Whole paired equality')
        new = read(N / 'overlay-normal' / name)
        diff.extend(difflib.unified_diff(old.decode().splitlines(keepends=True),
                    new.decode().splitlines(keepends=True), fromfile='original-a619/' + name,
                    tofile='effective-correction/' + name, n=0))
        corrected.append({'path': name, 'bytes': len(new), 'SHA256': sha(new)})
    need(''.join(diff).encode() == read(N / 'MINIMAL_DIFF.patch'), 'Full seven-file minimal diff exact')
    bound(E / 'EDITORIAL_CONFIG.json', oracle['configuration_must_remain_whole_byte_identical'])
    main_body = read(N / 'overlay-normal/PUBLIC_MAIN.html').decode()
    tex = read(Path(originals['whole_original_SOURCE_READY']['controlling_TeX']['extracted_path'])).decode()
    printed = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex, re.S).group(1)
    shown = re.search(r'<p id="printed-abstract">(.*?)</p>', main_body, re.S).group(1)
    need(' '.join(printed.split()) == ' '.join(html.unescape(shown).split()), 'Entire printed abstract')
    record = load(S / 'record.response.body')
    shown_native = re.search(r'<p id="native-description">(.*?)</p>', main_body, re.S).group(1)
    need(html.unescape(shown_native) == record['metadata']['description'], 'Entire separate native description')
    head = read(E / 'candidate/PUBLIC_HEAD.html').decode()
    scholarly = load(E / 'candidate/SCHOLARLY_METADATA.json')
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.S).group(1)
    need(typed(json.loads(ld), scholarly), 'Whole scholarly JSONLD typed identity')
    need(scholarly['abstract'] == ' '.join(printed.split()) and scholarly['version'] == '1.0' and
         scholarly['datePublished'] == '2026-10-13', 'Full abstract/version/date in structured metadata')
    for name in ['candidate/index.html', 'optimized-candidate/index.html']:
        page = read(N / 'overlay-normal' / name).decode()
        need(page.count(main_body) == page.count(head) == 1, 'Whole exact read head/main in effective page')
    execution = load(R / 'DESIGNATED_NEW_PURE_EXECUTION.json')
    need(execution['actual_exit_code'] == 0 and execution['literal_stderr'] == '', 'Actual designated pure outcome')
    output = bound(R / 'DESIGNATED_NEW_PURE.stdout', execution['whole_stdout'])
    bound(R / 'DESIGNATED_NEW_PURE.stderr', execution['whole_stderr'])
    need(output.decode() == execution['literal_stdout'], 'Complete actual stdout receipt')
    parsed = json.loads(output)
    need(parsed['fraction_guard']['second_semiaxis'] == '25/144' and
         parsed['fraction_guard']['b_squared_minus_lambda'] == '625/20736' and
         parsed['fraction_guard']['old_value_rejected'] is True, 'Exact positive fraction evidence')
    need(parsed['scientific_execution'] is False and parsed['publication_authority'] is False and
         parsed['root_copy_adopted'] is False and parsed['AA'] is None and parsed['canonical_url'] is None,
         'Actual authority separation')
    print(json.dumps({'status': 'INDEPENDENT_OFFLINE_FACT_CUSTODY_PASS', 'checks': CHECKS,
        'whole_typed_nodes': NODES, 'owned_files': owned_counts[0], 'owned_directories': owned_counts[1],
        'new_writer_files': 41, 'new_writer_directories': 7, 'old_editorial_files': 328,
        'old_editorial_directories': 8, 'old_fact_files': 799, 'old_fact_directories': 76,
        'actual_originals': 421, 'source_JSON_objects': source_json,
        'complete_original_namespaces': namespace_counts, 'paired_exact_replacements': corrected,
        'all_reverse_patches_exact': True, 'whole_printed_and_separate_native_abstracts': True,
        'qualified17original_plus405b_only_global_caches_diagnostic': True,
        'private_thirdparty_bodies_copied': 0, 'source_science_renderer_native_archive_execution': False,
        'network_or_filesystem_writes': False, 'root_copy_or_publication_authority': False}, indent=2))


if __name__ == '__main__':
    main()
