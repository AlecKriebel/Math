#!/usr/bin/env python3
"""Pure offline custody/consistency verification; no campaign execution or writes.

Run with Python -B. --preseal allows the two terminal closure files to be absent.
Checks hash the literal original native objects, not normalized substitutes.
The in-memory corruptions test this helper, not mathematical universality.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import copy
import hashlib
import json
import stat
import sys
import zipfile
import zlib

P = Path(__file__).resolve().parent
S = P.parent.parent / 'sources'
A = S / 'attempts/20261115T041044Z'
TERMINAL = {'OWNED_MANIFEST.json', 'CLOSURE.json', 'SEAL.json'}
READY_HASH = '8316224d19c14731bfe4a66946ea1fbe612965bcef284479ebfd9163846147a8'
SOURCE_SEAL_HASH = 'a185d2b687de2f7e632c48817b2373587cd41f49f80605d5f40a1ec61ec6a757'
SOURCE_MANIFEST_HASH = '27a84a2c498edc6aef45997c27820f818631702e126572fd3385fe75ebf49284'
INITIAL_HASH = 'e04a2f11e343ddcb1622d482b7419857b0dc12555a18af3a06fdb7eef3ed333d'
INITIAL_PROOF_HASH = '6efdfc9510d57b519c87b4f8f4fb0513dd50b850862e749365944666f6e9b1ed'
PDF_HASH = '2b98b7f4129114bf98434ae285a67736976cb4aa3d49b56298c2ee7fec5c6f6f'
TEX_HASH = '4202d9c50e4be6677fded9db501658df62491ee9ef5b0e79d0cccaa751d0a11c'
ZIP_HASH = '65cf534be55648b0d501a3af2834b8397f8f18e8680804ba96f7d405876c3cbb'
TITLE = 'A five-list obstruction on an eleven-vertex tree'
NAMES = ['Tree_Five_List_Verification_v1.0.zip', 'Tree_Five_List_Note_v1.0.pdf']
CHECKS = 0


def need(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def verify_file(path, size, digest):
    need(path.is_file() and not path.is_symlink(), 'missing or symbolic file: ' + str(path))
    body = path.read_bytes()
    need(len(body) == size and sha(body) == digest, 'byte identity changed: ' + str(path))
    return body


def native_identity(record, latest, versions, files, ready):
    for obj in (record, latest):
        need(type(obj) is dict and obj['id'] == 23440389, 'wrong native record identity')
        need(obj['doi'] == '10.5281/zenodo.23440389' and obj['conceptrecid'] == '23440388', 'wrong DOI/concept')
        need(obj['metadata']['title'] == TITLE and obj['metadata']['version'] == '1.0', 'wrong title/version')
        need(obj['metadata']['publication_date'] == '2026-10-17', 'wrong declared date')
        need(obj['created'] == '2026-10-17T18:10:27.832798+00:00' and obj['updated'] == '2026-10-17T18:10:28.256431+00:00', 'native dates changed')
        need(obj['status'] == 'published' and obj['state'] == 'done' and obj['submitted'] is True, 'native status changed')
        need(obj['metadata']['license'] == {'id': 'cc-by-4.0'}, 'native license changed')
        need(type(obj['swh']) is dict and obj['swh'] == {}, 'empty object became null/list')
        need([x['key'] for x in obj['files']] == NAMES, 'original ZIP/PDF order changed')
    need(type(versions['hits']['total']) is int and versions['hits']['total'] == 1, 'version count/type changed')
    need(len(versions['hits']['hits']) == 1 and versions['hits']['hits'][0]['id'] == 23440389, 'wrong version hit')
    need(versions['hits']['hits'][0]['swh'] is None, 'version hit null changed')
    need(type(files['entries']) is list and [x['key'] for x in files['entries']] == NAMES, 'files entries type/order changed')
    need(files['order'] == [] and type(files['order']) is list and files['default_preview'] is None, 'native empty/null fields changed')
    need(ready['native_schema_distinctions']['versions_swh_original'] == [None], 'aggregate version swh changed')
    need(record['files'] == [x['original_api_file_object'] for x in ready['all_native_assets_in_original_order']], 'whole original record file objects changed')
    need(files['entries'] == [x['whole_original_native_files_entry'] for x in ready['all_native_assets_in_original_order']], 'whole heterogeneous native file entries changed')


def safe_member(name, attrs):
    parts = PurePosixPath(name).parts
    kind = stat.S_IFMT(attrs >> 16)
    return bool(name) and '\\' not in name and not name.startswith('/') and '..' not in parts and ':' not in parts[0] and kind in (0, stat.S_IFREG)


def packet_results(result, verdict):
    need(result['status'] == 'PASS', 'own checks not passing')
    need(result['tree_DP_common_palette_counts'] == {'4': 0, '5': 8, '6': 6336} and result['bad_five_list_count'] == 0, 'fixed counts changed')
    need(result['all_eleven_root_reorientations_checked'] == list(range(11)), 'root checks incomplete')
    need(result['independent_path_length_tuples_checked'] == 729, 'bounded path check count changed')
    need(result['negative_controls']['omitting_sibling_constraint_admits_bad_lists_count'] == 3291, 'critical sibling control changed')
    need(result['actual_primary_FS2001Fig4_reconstruction']['vertices'] == 10 and result['actual_primary_FS2001Fig4_reconstruction']['connected_cycle_rank'] == 3, 'earlier cyclic graph misidentified')
    need(verdict['scope_not_narrowed'] is True and verdict['remaining_mathematical_gap'] is None, 'literal scope/verdict changed')
    need(verdict['verified_claims']['all_six_independent_nonnegative_finite_pendant_path_lengths'] is True, 'full family scope changed')
    need(verdict['verified_claims']['arbitrary_positive_integer_list_cardinality_exact'] == 6, 'list parameter changed')
    need(verdict['follow_up'] is None and verdict['new_native_program_execution'] is False, 'execution/followup boundary changed')
    need(verdict['external_human_peer_review'] is False and verdict['formal_proof_assistant_certification'] is False, 'review status changed')


def self_tests(record, latest, versions, files, ready, results, verdict):
    controls = []

    def rejected(name, operation):
        try:
            operation()
        except (ValueError, KeyError, TypeError, IndexError):
            controls.append(name)
        else:
            raise ValueError('corruption escaped: ' + name)

    for name, edit in [
        ('record empty object changed to null', lambda x: x[0].__setitem__('swh', None)),
        ('native version changed', lambda x: x[0]['metadata'].__setitem__('version', 'latest')),
        ('native DOI changed', lambda x: x[0].__setitem__('doi', '10.5281/zenodo.23440388')),
        ('native declared date replaced with creation date', lambda x: x[0]['metadata'].__setitem__('publication_date', '2026-10-18')),
        ('ZIP PDF order reversed', lambda x: x[0]['files'].reverse()),
        ('version hit null changed to empty object', lambda x: x[2]['hits']['hits'][0].__setitem__('swh', {})),
        ('version total integer changed to object', lambda x: x[2]['hits'].__setitem__('total', {'value': 1})),
        ('file entries changed to mapping', lambda x: x[3].__setitem__('entries', {})),
        ('file preview null changed to empty list', lambda x: x[3].__setitem__('default_preview', [])),
        ('whole opaque native entry changed', lambda x: x[3]['entries'][0]['transfer'].__setitem__('type', 'OTHER')),
    ]:
        mutated = copy.deepcopy([record, latest, versions, files, ready])
        edit(mutated)
        rejected(name, lambda m=mutated: native_identity(*m))
    for name, edit in [
        ('fixed count changed', lambda r, v: r['tree_DP_common_palette_counts'].__setitem__('6', 6335)),
        ('one root omitted', lambda r, v: r['all_eleven_root_reorientations_checked'].pop()),
        ('six-path family weakened', lambda r, v: v['verified_claims'].__setitem__('all_six_independent_nonnegative_finite_pendant_path_lengths', False)),
        ('human review invented', lambda r, v: v.__setitem__('external_human_peer_review', True)),
        ('native execution invented', lambda r, v: v.__setitem__('new_native_program_execution', True)),
    ]:
        r, v = copy.deepcopy([results, verdict])
        edit(r, v)
        rejected(name, lambda: packet_results(r, v))
    for name, attrs in [('../escape', 27525120), ('/absolute', 27525120), ('link', (stat.S_IFLNK | 0o644) << 16)]:
        rejected('unsafe ZIP member ' + name, lambda n=name, a=attrs: need(safe_member(n, a), 'unsafe'))
    body = (A / 'assets/Tree_Five_List_Note_v1.0.pdf').read_bytes()
    rejected('altered PDF bytes', lambda: need(sha(body + b'corrupt') == PDF_HASH, 'PDF byte mutation'))
    return controls


def main():
    preseal = sys.argv[1:] == ['--preseal']
    need(preseal or not sys.argv[1:], 'only --preseal is supported')
    need(sha((S / 'SOURCE_READY.json').read_bytes()) == READY_HASH, 'READY changed')
    need(sha((S / 'SOURCE_READY_SEAL.json').read_bytes()) == SOURCE_SEAL_HASH, 'source seal changed')
    need(sha((S / 'SOURCE_READY_MANIFEST.json').read_bytes()) == SOURCE_MANIFEST_HASH, 'source manifest changed')
    need(sha((P / 'INITIAL_SEAL.json').read_bytes()) == INITIAL_HASH, 'initial seal changed')
    need(sha((P / 'INITIAL_RECONSTRUCTION.md').read_bytes()) == INITIAL_PROOF_HASH, 'initial reconstruction changed')
    inputs = load(P / 'INPUT_MANIFEST.json')
    owned = load(P / 'OWNED_MANIFEST.json')
    for item in inputs['files']:
        verify_file(Path(item['path']), item['bytes'], item['SHA256'])
    for item in owned['files']:
        rel = PurePosixPath(item['path'])
        need(not rel.is_absolute() and '..' not in rel.parts, 'unsafe owned path')
        verify_file(P / item['path'], item['bytes'], item['SHA256'])
    actual_owned = {str(q.relative_to(P)) for q in P.rglob('*') if q.is_file() and q.name not in TERMINAL}
    need(actual_owned == {x['path'] for x in owned['files']}, 'owned file set changed')
    source_manifest = load(S / 'SOURCE_READY_MANIFEST.json')
    for item in source_manifest['files']:
        verify_file(S / item['path'], item['bytes'], item['SHA256'])
    source_files = {str(q.relative_to(S)) for q in S.rglob('*') if q.is_file()}
    need(source_files == {x['path'] for x in source_manifest['files']} | {'SOURCE_READY_MANIFEST.json', 'SOURCE_READY_CLOSURE.json', 'SOURCE_READY_SEAL.json'}, 'sealed source file set changed')
    source_seal = load(S / 'SOURCE_READY_SEAL.json')
    need(sha((S / 'SOURCE_READY_CLOSURE.json').read_bytes()) == source_seal['SOURCE_READY_CLOSURE_SHA256'], 'source closure changed')
    ready = load(S / 'SOURCE_READY.json')
    record = load(A / 'record.response.body')
    latest = load(A / 'latest.response.body.redirect-01')
    versions = load(A / 'versions.response.body')
    files = load(A / 'files.response.body')
    native_identity(record, latest, versions, files, ready)
    receipts = load(A / 'ALL_TRANSPORT_RECEIPTS.json')['receipts']
    need([x['HTTP_status'] for x in receipts] == [200, 301, 200, 200, 200, 200, 200], 'transport status/order changed')
    for receipt in receipts:
        need(type(receipt['response_headers_in_received_order']) is list, 'ordered native headers changed')
        verify_file(Path(receipt['body_path']), receipt['body_bytes'], receipt['body_SHA256'])
    need(receipts[1]['body_bytes'] == 99 and receipts[1]['HTTP_status'] == 301, 'native301 body lost')
    for asset in ready['all_native_assets_in_original_order']:
        body = verify_file(Path(asset['path']), asset['bytes'], asset['SHA256'])
        need(hashlib.md5(body).hexdigest() == asset['MD5'] == asset['original_api_file_object']['checksum'].split(':')[1], 'native MD5 mismatch')
    need(ready['selected_actual_PDF']['SHA256'] == PDF_HASH and ready['selected_actual_PDF']['pages'] == 3, 'actual PDF binding changed')
    tex = Path(ready['controlling_TeX']['extracted_path']).read_bytes()
    need(len(tex) == 9402 and len(tex.splitlines()) == 201 and sha(tex) == TEX_HASH, 'controlling TeX binding changed')
    archive = load(A / 'archive-custody.json')
    members = archive['all_safe_regular_occurrences']
    need(archive['safe_regular_occurrences'] == len(members) == 61 and archive['expanded_bytes_all_depths'] == 386822, 'archive scope changed')
    need(archive['nested_archives'] == 0 and archive['unsafe_names'] == [] and archive['nonregular_payloads'] == [], 'archive safety changed')
    zip_path = Path(ready['all_native_assets_in_original_order'][0]['path'])
    need(sha(zip_path.read_bytes()) == ZIP_HASH, 'complete ZIP changed')
    with zipfile.ZipFile(zip_path) as z:
        infos = z.infolist()
        need(len(infos) == 61 and z.testzip() is None, 'ZIP directory or CRC changed')
        names = []
        total = 0
        for i, (info, item) in enumerate(zip(infos, members)):
            need(safe_member(info.filename, info.external_attr) and not info.is_dir(), 'unsafe/nonregular ZIP member')
            need(info.filename.casefold() not in names, 'duplicate/case-colliding member')
            names.append(info.filename.casefold())
            need(info.filename == item['original_member_name'] and item['ordinal_zero_based'] == i, 'native ZIP member order/name changed')
            need(info.external_attr == item['native_external_attr'] and list(info.date_time) == item['native_date_time'] and info.flag_bits == item['zip_flags'] and info.compress_type == item['compression_method'], 'native ZIP metadata changed')
            body = z.read(info)
            need(len(body) == info.file_size == item['bytes'] and info.compress_size == item['compressed_bytes'], 'ZIP sizes changed')
            need(f'{zlib.crc32(body) & 0xffffffff:08x}' == item['CRC32'] and sha(body) == item['SHA256'], 'ZIP payload CRC/hash changed')
            need(body == Path(item['extracted_path']).read_bytes(), 'extracted bytes differ from ZIP')
            total += len(body)
        need(total == 386822, 'expanded total changed')
    for receipt_path in sorted((P / 'primary').glob('*.receipt.json')):
        receipt = load(receipt_path)
        body = verify_file(Path(receipt['path']), receipt['bytes'], receipt['SHA256'])
        need(receipt['status'] == 200 and type(receipt['headers_ordered']) is list, 'primary transport changed')
        need(body.startswith(b'%PDF-') == receipt['actual_PDF'], 'nonPDF access outcome misclassified')
    results, verdict = load(P / 'INDEPENDENT_CHECKS.json'), load(P / 'VERDICT.json')
    packet_results(results, verdict)
    ledger = load(P / 'READ_LEDGER.json')
    need(ledger['paper_first_boundary']['before_foreign_bodies_supplied_code_results_triage_archived_or_current_opinions'] is True and ledger['current_sibling_scientific_packets_read'] is False, 'independence record changed')
    controls = self_tests(record, latest, versions, files, ready, results, verdict)
    if not preseal:
        seal = load(P / 'SEAL.json')
        for filename, field in [('INPUT_MANIFEST.json', 'INPUT_MANIFEST_SHA256'), ('OWNED_MANIFEST.json', 'OWNED_MANIFEST_SHA256'), ('CLOSURE.json', 'CLOSURE_SHA256'), ('REPORT.md', 'REPORT_SHA256'), ('VERDICT.json', 'VERDICT_SHA256'), ('verify_closure.py', 'verifier_SHA256')]:
            need(sha((P / filename).read_bytes()) == seal[field], 'terminal seal mismatch: ' + filename)
    return {'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS', 'mode': 'preseal' if preseal else 'sealed', 'record_id': 23440389, 'checks': CHECKS, 'input_files': len(inputs['files']), 'owned_files': len(owned['files']), 'native_ZIP_payloads': 61, 'native_transport_receipts': 7, 'primary_HTTP200_PDFs': 3, 'primary_HTTP200_nonPDF_bodies': 2, 'in_memory_mutants_rejected': controls, 'network_requests': [], 'programs_executed': [], 'writes': [], 'scope': 'custody and literal packet consistency; mathematical proofs/checks are separate evidence'}


if __name__ == '__main__':
    try:
        print(json.dumps(main(), indent=2))
    except Exception as error:
        print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'FAIL', 'checks_completed': CHECKS, 'error': str(error), 'writes': [], 'network_requests': [], 'programs_executed': []}, indent=2))
        sys.exit(1)
