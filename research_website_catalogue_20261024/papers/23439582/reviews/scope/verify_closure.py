#!/usr/bin/env python3
"""Read-only offline custody/packet checks, with no target-code imports.

Only standard-library byte/JSON/ZIP operations are used. No subprocess, network,
mathematical campaign, module loading from sources, or file write is performed.
--preseal permits terminal SEAL/CLOSURE absence during packet construction.
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
B = P.parent.parent
S = B / 'source-resume-20261115'
OLD = B / 'sources'
TERMINAL = {'OWNED_MANIFEST.json', 'SEAL.json', 'CLOSURE.json'}
READY = '0795e0631373b473f9d50270532ed8f326f68ba793d4f08c1654ea1a4556a244'
SOURCE_SEAL = 'b46f46fa3798b80d6382a823f7f8a582af5427028c27e6bac2ef465e5f81929c'
SOURCE_MANIFEST = '670db95933cff7701a421e27ec7966eb34a9cac720921fb55ff1825f031b7dbd'
OLD_SEAL = '52c000f32fdde4a5fac49014e7e6f76a788d7d318220d11e6ea770b3a1cd8770'
INITIAL = '61e9ab147e4c4baa1a4ce2d601ab178256d6d8b46799736f79ad8013332294e5'
INITIAL_PROOF = '73368a50db280a0bbe44691ddbc8f65f0278c65a16bdcfdff896c3cd16020ba7'
PDF = 'f11b2f3aa0e1aeec4c5971264e734c0458bd512cbb09e5e5ca11a60f0a037644'
TEX = 'c051fdd5c20882305a04f61aaad4385f1e425c5a893e2c28fd914d8da979c6e0'
ZIP = '1aeab807b46af3836bcce647c6bd24be945c2f1b82fb710684d087538db51933'
NATIVE_CODE = 'cf9e1007a0eea9abd6d7870c231c572cb5fe5ae7df6fdb3e4c5f1af492ed2f24'
TITLE = 'Vanishing of the cellularization map for non-p-nilpotent component groups'
NAMES = ['cellularization-vanishing-source-and-verification.zip', 'cellularization-vanishing.pdf']
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


def file_check(path, size, digest):
    need(path.is_file() and not path.is_symlink(), 'missing/symbolic input: ' + str(path))
    body = path.read_bytes()
    need(len(body) == size and sha(body) == digest, 'byte identity changed: ' + str(path))
    return body


def native_check(record, latest, versions, files, ready):
    for obj in (record, latest):
        need(type(obj) is dict and obj['id'] == 23439582, 'record identity changed')
        need(obj['doi'] == '10.5281/zenodo.23439582' and obj['conceptrecid'] == '23439581', 'DOI/native concept string changed')
        need(obj['metadata']['title'] == TITLE and obj['metadata']['version'] == '1.0.0', 'title/version changed')
        need(obj['metadata']['publication_date'] == '2026-10-17', 'declared date changed')
        need(obj['created'] == '2026-10-17T16:57:54.532142+00:00' and obj['updated'] == '2026-10-17T16:57:54.941306+00:00', 'native dates changed')
        need(obj['status'] == 'published' and obj['state'] == 'done' and obj['submitted'] is True, 'native statuses changed')
        need(obj['metadata']['license'] == {'id': 'cc-by-4.0'}, 'native rights object changed')
        need(type(obj['swh']) is dict and obj['swh'] == {}, 'record empty object normalized')
        need([x['key'] for x in obj['files']] == NAMES, 'native ZIP/PDF order changed')
    need(type(versions['hits']['total']) is int and versions['hits']['total'] == 1, 'native total type/value changed')
    need(len(versions['hits']['hits']) == 1 and versions['hits']['hits'][0]['id'] == 23439582, 'wrong version list')
    need('swh' in versions['hits']['hits'][0] and versions['hits']['hits'][0]['swh'] is None, 'present native version null changed')
    need(type(files['entries']) is list and [x['key'] for x in files['entries']] == NAMES, 'native file entries type/order changed')
    need(type(files['order']) is list and files['order'] == [] and files['default_preview'] is None, 'native empty/null changed')
    need(record['files'] == [x['original_api_file_object'] for x in ready['all_native_assets_in_original_order']], 'whole native API file objects changed')
    need(files['entries'] == [x['whole_original_native_files_entry'] for x in ready['all_native_assets_in_original_order']], 'whole opaque heterogeneous file entries changed')
    need(ready['native_schema_distinctions']['versions_swh_original_when_present'] == [{'present': True, 'whole_value_if_present': None}], 'READY presence wrapper changed')
    need(ready['completion_percent'] == 95 and ready['target_manuscript_scientifically_read'] is False, 'historical READY stage rewritten')
    need(ready['all_native_assets_in_original_order'][0]['native_GET_claimed'] is False and ready['all_native_assets_in_original_order'][1]['native_GET_claimed'] is True, 'cached versus native transport conflated')


def safe_name(name, attributes):
    parts = PurePosixPath(name).parts
    kind = stat.S_IFMT(attributes >> 16)
    return bool(name) and '\\' not in name and not name.startswith('/') and '..' not in parts and ':' not in parts[0] and kind in (0, stat.S_IFREG)


def result_check(result, native, verdict, ledger):
    need(result['status'] == 'PASS' and result['identity_checks_total'] == 83104, 'own exact test receipt changed')
    need([x['characteristic'] for x in result['models']] == [2, 3, 5], 'own field scope changed')
    need([x['tested_ordinary_Hopf_dimension'] for x in result['models']] == [8, 24, 40], 'own model scope changed')
    for model in result['models'][1:]:
        need(model['negative_controls'] == {'omit_coproduct_parity_detected': True, 'omit_antipode_parity_detected': True}, 'own sign controls changed')
    need(native['status'] == 'PASS' and native['source_unmodified_after_execution'] is True and native['native_program_SHA256'] == NATIVE_CODE, 'native code custody changed')
    need(len(native['runs']) == 2 and native['runs'][0]['exit_code'] == 0 and native['runs'][0]['parsed_output_matches_exact_native_expected'] is True, 'native normal replay mismatch')
    need(native['runs'][1]['exit_code'] != 0 and native['runs'][1]['optimized_mode_explicitly_rejected'] is True, 'optimized refusal omitted')
    expected = load(S / 'published-source/verification/expected_results.json')
    need(json.loads(native['runs'][0]['stdout']) == expected, 'actual native output differs from original expected')
    need(verdict['original_scope_preserved'] is True and verdict['remaining_mathematical_gap'] is None, 'literal full-scope verdict changed')
    claims = verdict['verified_claims']
    need(claims['every_characteristic_p_field_including_infinite_extensions'] is True and claims['every_compact_Lie_group_with_non_p_nilpotent_component_group'] is True, 'field/group quantifier weakened')
    need(claims['full_canonical_cellularization_map_zero_on_all_integer_homotopy_degrees'] is True, 'full map/all-degree scope weakened')
    need(verdict['follow_up'] is None and verdict['external_human_peer_review'] is False and verdict['formal_proof_assistant_certification'] is False, 'followup/review status changed')
    need(ledger['paper_first_boundary']['foreign_bodies_code_results_archived_current_opinions_before_initial'] is False and ledger['current_sibling_or_root_scientific_findings_read'] is False, 'independence boundary changed')


def controls(record, latest, versions, files, ready, result, native, verdict, ledger):
    rejected = []

    def reject(label, function):
        try:
            function()
        except (ValueError, KeyError, TypeError, IndexError):
            rejected.append(label)
        else:
            raise ValueError('mutation escaped: ' + label)

    edits = [
        ('native version changed', lambda x: x[0]['metadata'].__setitem__('version', '1.0')),
        ('concept string normalized to integer', lambda x: x[0].__setitem__('conceptrecid', 23439581)),
        ('native record empty object changed to null', lambda x: x[0].__setitem__('swh', None)),
        ('native version present null changed to missing', lambda x: x[2]['hits']['hits'][0].pop('swh')),
        ('files list normalized to mapping', lambda x: x[3].__setitem__('entries', {})),
        ('file order reversed', lambda x: x[3]['entries'].reverse()),
        ('opaque file storage changed', lambda x: x[3]['entries'][0].__setitem__('storage_class', 'OTHER')),
        ('historical READY completion rewritten', lambda x: x[4].__setitem__('completion_percent', 100)),
        ('cached ZIP transport invented', lambda x: x[4]['all_native_assets_in_original_order'][0].__setitem__('native_GET_claimed', True)),
    ]
    for label, edit in edits:
        x = copy.deepcopy([record, latest, versions, files, ready])
        edit(x)
        reject(label, lambda: native_check(*x))
    edits = [
        ('own exact count changed', lambda x: x[0].__setitem__('identity_checks_total', 83103)),
        ('optimized refusal changed to success', lambda x: x[1]['runs'][1].__setitem__('exit_code', 0)),
        ('arbitrary field scope weakened', lambda x: x[2]['verified_claims'].__setitem__('every_characteristic_p_field_including_infinite_extensions', False)),
        ('full homotopy map weakened', lambda x: x[2]['verified_claims'].__setitem__('full_canonical_cellularization_map_zero_on_all_integer_homotopy_degrees', False)),
        ('external review invented', lambda x: x[2].__setitem__('external_human_peer_review', True)),
        ('preinitial body exposure hidden', lambda x: x[3]['paper_first_boundary'].__setitem__('foreign_bodies_code_results_archived_current_opinions_before_initial', True)),
    ]
    for label, edit in edits:
        x = copy.deepcopy([result, native, verdict, ledger])
        edit(x)
        reject(label, lambda: result_check(*x))
    for name, attributes in [('../escape', 27525120), ('/absolute', 27525120), ('link', (stat.S_IFLNK | 0o644) << 16)]:
        reject('unsafe ZIP name/type: ' + name, lambda n=name, a=attributes: need(safe_name(n, a), 'unsafe'))
    body = (S / 'assets/cellularization-vanishing.pdf').read_bytes()
    reject('PDF bytes altered', lambda: need(sha(body + b'x') == PDF, 'PDF corruption'))
    return rejected


def main():
    preseal = sys.argv[1:] == ['--preseal']
    need(preseal or not sys.argv[1:], 'only --preseal supported')
    for path, digest in [(S/'SOURCE_READY.json', READY), (S/'SOURCE_READY_SEAL.json', SOURCE_SEAL), (S/'SOURCE_READY_MANIFEST.json', SOURCE_MANIFEST), (OLD/'ACQUISITION_INCOMPLETE_SEAL.json', OLD_SEAL), (P/'INITIAL_SEAL.json', INITIAL), (P/'INITIAL_RECONSTRUCTION.md', INITIAL_PROOF)]:
        need(sha(path.read_bytes()) == digest, 'fixed seal changed: ' + str(path))
    inputs, owned = load(P/'INPUT_MANIFEST.json'), load(P/'OWNED_MANIFEST.json')
    for item in inputs['files']:
        file_check(Path(item['path']), item['bytes'], item['SHA256'])
    for item in owned['files']:
        rel = PurePosixPath(item['path'])
        need(not rel.is_absolute() and '..' not in rel.parts, 'unsafe owned path')
        file_check(P/item['path'], item['bytes'], item['SHA256'])
    need({str(q.relative_to(P)) for q in P.rglob('*') if q.is_file() and q.name not in TERMINAL} == {x['path'] for x in owned['files']}, 'owned file set changed')
    source_manifest = load(S/'SOURCE_READY_MANIFEST.json')
    for item in source_manifest['files']:
        file_check(S/item['path'], item['bytes'], item['SHA256'])
    need({str(q.relative_to(S)) for q in S.rglob('*') if q.is_file()} == {x['path'] for x in source_manifest['files']} | {'SOURCE_READY_MANIFEST.json','SOURCE_READY_CLOSURE.json','SOURCE_READY_SEAL.json'}, 'additive source set changed')
    source_seal = load(S/'SOURCE_READY_SEAL.json')
    need(source_seal['completion_percent'] == 100 and sha((S/'SOURCE_READY_CLOSURE.json').read_bytes()) == source_seal['SOURCE_READY_CLOSURE_SHA256'], 'final source closure changed')
    baseline = load(S/'PRIOR_SOURCE_BASELINE.json')['files']
    for item in baseline:
        file_check(Path(item['path']), item['bytes'], item['SHA256'])
    need({str(q) for q in OLD.rglob('*') if q.is_file()} == {x['path'] for x in baseline}, 'old sealed history file set changed')
    ready = load(S/'SOURCE_READY.json')
    record, latest, versions, files = [load(S/n) for n in ['record.response.body','latest.response.body.redirect-01','versions.response.body','files.response.body']]
    native_check(record, latest, versions, files, ready)
    transports = load(S/'ALL_TRANSPORT_RECEIPTS.json')
    fresh = transports['new_resumption_receipts_in_chronological_order']
    need([x['HTTP_status'] for x in fresh] == [200,301,200,200,200,200], 'fresh transport order/status changed')
    for receipt in fresh:
        need(type(receipt['response_headers_in_received_order']) is list, 'fresh ordered headers changed')
        file_check(Path(receipt['body_path']), receipt['body_bytes'], receipt['body_SHA256'])
    old_receipts = transports['prior_sealed_failed_transport_receipts_unchanged']
    need([x['whole_literal_original_receipt']['HTTP_status'] for x in old_receipts] == [403,403,403], 'earlier403 failures changed')
    for item in old_receipts:
        identity, raw = item['receipt_identity'], item['whole_literal_original_receipt']
        file_check(Path(identity['path']), identity['bytes'], identity['SHA256'])
        need(load(Path(identity['path'])) == raw and type(raw['response_headers_in_order']) is list, 'old heterogeneous receipt normalized')
        file_check(Path(raw['body_path']), raw['bytes'], raw['SHA256'])
    for asset in ready['all_native_assets_in_original_order']:
        body = file_check(Path(asset['path']), asset['bytes'], asset['SHA256'])
        need(hashlib.md5(body).hexdigest() == asset['MD5'] == asset['original_api_file_object']['checksum'].split(':')[1], 'native MD5 mismatch')
    cache = load(S/'CACHE_ASSOCIATION.json')
    cached = file_check(Path(cache['candidate_original_path']), cache['bytes'], cache['SHA256'])
    need(sha(cached) == ZIP and cache['native_GET_of_cached_ZIP_claimed'] is False, 'cached source mechanism changed')
    need(ready['selected_actual_PDF']['SHA256'] == PDF and ready['selected_actual_PDF']['pages'] == 4, 'actual manuscript binding changed')
    tex = Path(ready['controlling_TeX']['extracted_path']).read_bytes()
    need(len(tex) == 13093 and len(tex.splitlines()) == 157 and sha(tex) == TEX, 'controlling TeX changed')
    for item in ready['all_embedded_PDFs']:
        body = file_check(Path(item['path']), item['bytes'], item['SHA256'])
        need(body == (S/'assets/cellularization-vanishing.pdf').read_bytes(), 'embedded/published PDF mismatch')
    archive = load(S/'archive-custody.json')
    items = archive['all_safe_regular_occurrences']
    need(len(items) == archive['safe_regular_occurrences'] == 20 and archive['expanded_bytes_all_depths'] == 184835 and archive['nested_archives'] == 0, 'archive scope changed')
    need(archive['unsafe_names'] == archive['nonregular_payloads'] == archive['duplicate_or_case_colliding_names'] == [], 'source archive safety changed')
    with zipfile.ZipFile(S/'assets/cellularization-vanishing-source-and-verification.zip') as z:
        need(len(z.infolist()) == 20 and z.testzip() is None, 'whole ZIP directory/CRC changed')
        seen, total = set(), 0
        for i, (info, item) in enumerate(zip(z.infolist(), items)):
            need(safe_name(info.filename, info.external_attr) and not info.is_dir() and info.filename.casefold() not in seen, 'unsafe/nonregular/colliding payload')
            seen.add(info.filename.casefold())
            need(info.filename == item['original_member_name'] and item['ordinal_zero_based'] == i, 'native ZIP directory order changed')
            need(info.external_attr == item['native_external_attr'] and list(info.date_time) == item['native_date_time'] and info.flag_bits == item['zip_flags'] and info.compress_type == item['compression_method'], 'native ZIP metadata changed')
            body = z.read(info)
            need(len(body) == info.file_size == item['bytes'] and info.compress_size == item['compressed_bytes'], 'ZIP size changed')
            need(sha(body) == item['SHA256'] and f'{zlib.crc32(body)&0xffffffff:08x}' == item['CRC32'], 'ZIP payload hash/CRC changed')
            need(body == Path(item['extracted_path']).read_bytes(), 'extracted payload differs')
            total += len(body)
        need(total == 184835, 'expanded total changed')
    for path in sorted((P/'primary').glob('*.receipt.json')):
        receipt = load(path)
        body = file_check(Path(receipt['path']), receipt['bytes'], receipt['SHA256'])
        need(receipt['status'] == 200 and type(receipt['response_headers_in_received_order']) is list, 'primary transport changed')
        need(body.startswith(b'%PDF-') == receipt['actual_PDF'], 'primary body misclassified')
    need(sha((P/'native-reproduction/check_bosonization.py').read_bytes()) == NATIVE_CODE == sha((S/'published-source/verification/check_bosonization.py').read_bytes()), 'native executed copy differs')
    result, native, verdict, ledger = [load(P/n) for n in ['INDEPENDENT_SIGN_CHECKS.json','NATIVE_REPRODUCTION.json','VERDICT.json','READ_LEDGER.json']]
    result_check(result, native, verdict, ledger)
    mutants = controls(record, latest, versions, files, ready, result, native, verdict, ledger)
    if not preseal:
        seal = load(P/'SEAL.json')
        for name, key in [('INPUT_MANIFEST.json','INPUT_MANIFEST_SHA256'),('OWNED_MANIFEST.json','OWNED_MANIFEST_SHA256'),('CLOSURE.json','CLOSURE_SHA256'),('REPORT.md','REPORT_SHA256'),('VERDICT.json','VERDICT_SHA256'),('verify_closure.py','verifier_SHA256')]:
            need(sha((P/name).read_bytes()) == seal[key], 'terminal seal mismatch: ' + name)
    return {'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','mode':'preseal' if preseal else 'sealed','record_id':23439582,'checks':CHECKS,'input_files':len(inputs['files']),'owned_files':len(owned['files']),'native_ZIP_payloads':20,'fresh_native_transport_receipts':6,'prior403_receipts':3,'fresh_primary_PDFs':6,'fresh_primary_metadata_receipts':1,'mutants_rejected':mutants,'network_requests':[],'target_imports':[],'programs_executed':[],'writes':[],'scope':'Pure offline custody and literal packet consistency; analytic proof and bounded formula executions are separately recorded.'}


if __name__ == '__main__':
    try:
        print(json.dumps(main(),indent=2))
    except Exception as error:
        print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'FAIL','checks_completed':CHECKS,'error':str(error),'network_requests':[],'target_imports':[],'programs_executed':[],'writes':[]},indent=2))
        sys.exit(1)
