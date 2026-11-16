#!/usr/bin/env python3
"""Standalone default-only offline finite custody; never runs mathematical code.

No source/project imports, network, subprocesses, live W/Git/Sheet/core reads,
scientific replay or writes. Two exact externally cached primary files are the
only read exceptions to the fixed programme root. Ignored caches are included.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile
import zlib

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R = P / 'papers/22982894/reviews/adversarial'
S = P / 'papers/22982894/sources'
CACHE = Path('/Users/alec/Documents/Math/owr_17293_016_brandes_normalization/sources')
EXTERNAL = {CACHE / 'owr-2019-50.pdf', CACHE / 'inventory.json'}
TERMINALS = {'FINAL_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json'}
CHECKS = 0


def need(ok, why):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(why)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def ordinary(path):
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'absolute read path')
    need(path.is_relative_to(P) or path in EXTERNAL, 'exact read boundary')
    base = P if path.is_relative_to(P) else CACHE
    q = base
    need(stat.S_ISDIR(q.lstat().st_mode), 'ordinary read base')
    for part in path.relative_to(base).parts[:-1]:
        q = q / part
        need(stat.S_ISDIR(q.lstat().st_mode), 'ordinary ancestor')
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1, 'ordinary single-link body')
    return path.read_bytes()


def pin(spec, root=None):
    path = Path(spec['path'])
    if root is not None:
        need(not path.is_absolute() and '..' not in path.parts, 'relative manifest path')
        path = root / path
    body = ordinary(path)
    need(len(body) == spec['bytes'] and sha(body) == spec['SHA256'], 'whole pin ' + str(path))
    return body


def read(name, root=R):
    return json.loads(ordinary(root / name))


def extent(root):
    need(root in {R, S} and stat.S_ISDIR(root.lstat().st_mode), 'finite ordinary root')
    files, dirs = set(), set()
    for here, names, leaves in os.walk(root, followlinks=False):
        for name in names:
            q = Path(here) / name
            need(stat.S_ISDIR(q.lstat().st_mode), 'ordinary directory')
            dirs.add(q.relative_to(root).as_posix())
        for name in leaves:
            q = Path(here) / name
            st = q.lstat()
            need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1, 'ordinary leaf')
            files.add(q.relative_to(root).as_posix())
    return files, dirs


def own_seal(name, digest):
    body = ordinary(R / name)
    need(sha(body) == digest, 'unchanged staged scientific predecessor ' + name)
    obj = json.loads(body)
    for spec in obj['files']:
        pin(spec)
    return obj


def main():
    need(len(sys.argv) == 1, 'default only, no active modes')
    manifest = read('FINAL_MANIFEST.json')
    need(manifest['exact_root_terminal_exclusions'] == sorted(TERMINALS), 'only exact existing root terminals')
    need(manifest['future_directory_subtree_basename_exclusions'] == [], 'no future carveouts')
    expected = {v['path'] for v in manifest['files']}
    need(len(expected) == len(manifest['files']) and not expected & TERMINALS, 'unique finite payload')
    files, dirs = extent(R)
    need(files == expected | TERMINALS and dirs == set(manifest['directories']), 'closed own files AND directories')
    for spec in manifest['files']:
        pin(spec, R)
    for name in TERMINALS:
        need(isinstance(read(name), dict), 'existing ordinary JSON terminal')
    need(ordinary(R / '.gitignore') == b'/primary/raw/\n/manuscript-rasters/\n/manuscript-text/\n/native-copy/\n', 'preinstalled private ignore bytes')
    own_seal('INITIAL_SEAL.json', '1aa50cd585980f9962d017669191a4a4b9518cc9820072a5653a4ccca25f5842')
    own_seal('OWN_RESULTS_SEAL.json', '71a140978ba1f5a2664a9b29ba2a36d9b0c69de26e4ff9792ae291d1860d33ea')
    own_seal('NATIVE_REPLAY_SEAL.json', '0db7704bf9bce313d351102980910ddc33dc688e603e66724b854a3b8d0f6362')
    custody = read('SOURCE_INPUT_CUSTODY.json')
    need(len(custody['whole_original_108_files']) == 108 and len(custody['exact_14_directories']) == 14, 'source original count')
    for spec in custody['whole_original_108_files']:
        pin(spec)
    sf, sd = extent(S)
    sm = read('SOURCE_READY_MANIFEST.json', S)
    source_terms = {'SOURCE_READY_CLOSURE.json', 'SOURCE_READY_MANIFEST.json', 'SOURCE_READY_SEAL.json'}
    need(set(sm['excluded_terminal_files']) == source_terms, 'source exact terminals')
    need(sf == {v['path'] for v in sm['files']} | source_terms and sd == set(sm['directories']), 'source closed extent')
    need(sf == {str(Path(v['path']).relative_to(S)) for v in custody['whole_original_108_files']}, 'all108 originals accounted')
    need(sd == set(custody['exact_14_directories']), 'all14 source directories unchanged')
    need(sha(ordinary(S / 'SOURCE_READY_SEAL.json')) == '24e7b08bda1c3561d9db2040745b2b1b8eb5b2e1f8c37be60426e831511cfb11', 'source final immutable')
    ready = read('SOURCE_READY.json', S)
    need(ready['native_version_whole_field'] == {'present': True, 'original_value': '1.0'}, 'literal native version field')
    need(ready['printed_title_date_version_inspected'] is False and ready['printed_date'] is None and ready['printed_version'] is None, 'historical source unread flags retained')
    need([v['original_api_file_object']['key'] for v in ready['all_native_assets_in_original_order']] == ['source-and-verification.zip', 'paper.pdf'], 'native asset order')
    for spec in ready['whole_native_API_objects']:
        pin(spec)
    for spec in ready['all_native_assets_in_original_order']:
        body = pin(spec)
        need(hashlib.md5(body).hexdigest() == spec['original_api_file_object']['checksum'].split(':')[1], 'native whole asset checksum')
    # Pure archive byte custody only: no extraction, imports or source execution.
    rows, names, total = [], set(), 0
    with zipfile.ZipFile(S / 'assets/source-and-verification.zip') as archive:
        need(len(archive.infolist()) <= 64, 'bounded original archive entries')
        for ordinal, item in enumerate(archive.infolist()):
            name = PurePosixPath(item.filename)
            need(not name.is_absolute() and '..' not in name.parts and '\\' not in item.filename, 'safe original archive name')
            need(item.filename.casefold() not in names, 'unique archive casefold namespace')
            names.add(item.filename.casefold())
            if item.is_dir():
                continue
            need(stat.S_IFMT(item.external_attr >> 16) in (0, stat.S_IFREG), 'regular archive payload')
            total += item.file_size
            need(total <= 1024 * 1024, 'bounded original expanded extent')
            body = archive.read(item)
            need(len(body) == item.file_size and zlib.crc32(body) & 0xffffffff == item.CRC, 'full archive CRC/size')
            need(ordinary(S / 'published-source/asset-001' / item.filename) == body, 'whole original extracted bytes')
            rows.append({'ordinal': ordinal, 'original_member_name': item.filename, 'bytes': len(body), 'SHA256': sha(body), 'CRC32': format(item.CRC, '08x'), 'full_crc_and_original_extraction_equal': True})
    need(rows == custody['archive_original_order_full48_regular_payloads'] and len(rows) == 48, 'all48 exact original-order regular payloads')
    own = read('OWN_CONTROLS_EXECUTION.json')
    own_out, own_err = pin(own['stdout']), pin(own['stderr'])
    need(own['actual_exit'] == 0 and len(own_out) == 24160 and not own_err, 'literal own finite execution')
    need(own_out.decode() == own['literal_whole_stdout'] and own_err.decode() == own['literal_whole_stderr'], 'whole own streams preserved')
    need(json.loads(own_out)['checks'] == 82, 'own historical control count only')
    replay = read('NATIVE_REPLAY_EXECUTION.json')
    out, err = pin(replay['stdout']), pin(replay['stderr'])
    expected_out = pin(replay['whole_expected'])
    need(replay['actual_exit'] == 0 and len(out) == 239 and not err, 'actual once selected native streams')
    need(out == expected_out and json.loads(out) == json.loads(expected_out), 'whole byte and typed expected equality')
    need(out.decode() == replay['literal_whole_stdout'] and err.decode() == replay['literal_whole_stderr'], 'literal complete native streams')
    need(replay['actual_normal_selected_native_runs'] == 1 and replay['actual_optimized_native_runs'] == 0 and replay['default_or_wider_campaign_runs'] == 0, 'no replay inflation')
    need(pin(replay['original_program_after']) == pin(replay['private_program_after']), 'byteidentical selected program')
    plan = read('NATIVE_REPLAY_PLAN.json')
    need(pin(plan['original_selected_input']) == pin(plan['byteidentical_private_selected_input']), 'byteidentical selected input')
    need(sorted(q.name for q in (R / 'native-copy').iterdir()) == ['nonconvex-quartic.json', 'verify.py'], 'private exact two-file extent')
    need(replay['all108_original_before'] == replay['all108_original_after'] == custody['whole_original_108_files'], 'full native source fences')
    need(sha(ordinary(P / 'verification/root-primary-acquisition-22982894-20261115.json')) == 'a20575b9e27b296cf075a890a1b71cf713a1c4d36a9024ea1aaa5e4bd3ed7a9c', 'actual root raw-only authority')
    ref1 = read('PRIMARY_REFERENCE_01.json')
    pin(ref1['whole_handoff'])
    raw_owr = pin(ref1['actual_raw_original_body'])
    old_meta = json.loads(pin(ref1['whole_actual_original_metadata']))
    need(sha(raw_owr) == old_meta['sources'][0]['sha256'] == '549b3c1ecb3abb2a970f622e499b1b5aac23a02f4c73567408dfd8c457aff021', 'exact cached OWR primary')
    need(ref1['own_network_GETs'] == 0 and ref1['legacy_HTTP_status_headers_requests_redirects'].startswith('ABSENT'), 'legacy transport absence honest')
    ref2 = read('PRIMARY_REFERENCE_02.json')
    handoff = json.loads(pin(ref2['whole_handoff']))
    for spec in handoff['files']:
        pin(spec)
    pin(ref2['raw_PDF'])
    need([v['HTTP_status'] for v in handoff['whole_transports']] == [302, 403, 200, 200], 'actual ordered primary transport statuses')
    need(ref2['GETs_here'] == 0, 'no primary GET by this lane')
    need(read('PRIMARY_READ_LEDGER_01.json')['all66_report_pages_scientifically_read'] is False and read('PRIMARY_READ_LEDGER_02.json')['whole20_page_PDF_scientifically_read'] is False, 'bounded reading scope retained')
    for name in ['REPORT.md', 'DERIVATIONS.md', 'VERDICT.json', 'FINAL_READ_LEDGER.json', 'POSTINITIAL_FAILURE_AND_LIMIT_HISTORY.json']:
        need(len(ordinary(R / name)) > 0, 'final authored artifact')
    verdict = read('VERDICT.json')
    need(verdict['root143_scientific_comparison_gate'] == 'CLOSED' and verdict['scientific_findings_to_root_or_peer_disclosed'] is False, 'comparison gate retained')
    need(verdict['follow_up'] is None and verdict['publication_authority'] is False and verdict['AA'] is None, 'no ungranted authority')
    seal = read('FINAL_SEAL.json')
    sealed = seal.get('status') == 'IMMUTABLE_COMPLETE_INDEPENDENT_REVIEW'
    if sealed:
        for key in ['MANIFEST', 'CLOSURE', 'REPORT', 'VERDICT', 'helper', 'helper_full_read']:
            pin(seal[key])
        need(seal['ordinary_files'] == len(files) and seal['ordinary_directories'] == len(dirs), 'sealed exact extent')
    print(json.dumps({'status': 'PASS_OFFLINE_STRICT_REVIEW_CUSTODY', 'checks': CHECKS, 'own_files': len(files), 'own_directories': len(dirs), 'source_files': len(sf), 'source_directories': len(sd), 'full_original_ZIP_regular_payloads': len(rows), 'native_replay_runs_not_repeated': True, 'primary_GETs': 0, 'science_or_source_helpers_executed_by_this_default': False, 'network_or_W_Git_Sheet_core_access': False, 'writes': False, 'sealed': sealed}, sort_keys=True))


if __name__ == '__main__':
    main()
