"""Read-only custody closure; no scientific imports, execution, network or writes.

Importing this module only defines functions. Run with python3 -B. The optional
self-test mutates in-memory metadata copies and never changes a file.
"""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import zipfile

P = Path(__file__).resolve().parent
S = P.parents[1] / 'sources'
TERMINALS = {'OWNED_MANIFEST.json', 'CLOSURE_RESULT.json', 'FINAL_SEAL.json'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def obj(path):
    return json.loads(path.read_text())

def fixtures():
    ready = obj(S / 'SOURCE_READY.json')
    return {
        'ready': ready,
        'record': obj(S / 'record.response.body'),
        'versions': obj(S / 'versions-page001.response.body'),
        'files': obj(S / 'files.response.body'),
        'initial': obj(P / 'INITIAL_SEAL.json'),
        'verdict': obj(P / 'VERDICT.json'),
        'controls': obj(P / 'INDEPENDENT_SCOPE_CONTROLS.json'),
        'support': obj(P / 'SUPPORT_INSPECTION.json'),
        'gate': obj(P / 'ROOT_GATE_NOTICE.json'),
    }

def semantic_errors(f):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    r, rec, ver, files = (f[x] for x in ['ready', 'record', 'versions', 'files'])
    initial, verdict, controls, support, gate = (f[x] for x in ['initial', 'verdict', 'controls', 'support', 'gate'])
    check(r['record_id'] == 23306203 and r['status'] == 'SOURCE_READY', 'exact source identity')
    check(r['native_version_whole_field'] == {'present': True, 'original_value': '1.0.0'}, 'native version field')
    check(r['all_enumerated_version_ids'] == [23306203], 'named published version')
    check(r['HTTP_status_sequence'] == [200,301,200,200,200,200,200], 'whole native transport order')
    check(r['actual_ordinary_native_HTTP_requests'] == 7, 'actual transport count')
    check(r['publication_date'] == '2026-10-11', 'declared date')
    check(r['created'] == '2026-10-11T22:52:53.427906+00:00', 'created date separate')
    check(r['updated'] == '2026-10-11T22:52:54.147843+00:00', 'updated date separate')
    check([a['original_api_file_object']['key'] for a in r['all_native_assets_in_original_order']] == ['focal_product_support.zip','focal_product_period_criterion.pdf'], 'native asset order')
    check(type(rec['swh']) is dict and rec['swh'] == {}, 'record empty object')
    check(ver['hits']['hits'][0]['swh'] is None, 'version hit null')
    check(type(files['entries']) is list and files['order'] == [] and files['default_preview'] is None, 'heterogeneous native files schema')
    check(r['whole_regular_payload_occurrences'] == 13 and r['expanded_bytes_all_depths'] == 95102, 'archive whole payload scope')
    check(r['embedded_PDFs'] == [] and r['nested_archive_count'] == 0, 'archive topology')
    check(r['scientific_verdict'] is None and r['publication_authority'] is False, 'source acquisition authority null/false')
    check(r['printed_version'] is None and r['printed_title_date_version_inspected'] is False, 'historical acquisition unread identity')
    check(r['mathematical_PDF_TeX_or_pixels_read'] is False and r['source_programmes_executed'] == [], 'historical acquisition exposure')
    check(initial['root_gate'] == 'CLOSED' and initial['scientific_findings_released'] is False, 'original CLOSED seal preserved')
    check(initial['all_actual_PDF_pages_personally_read'] == 5 and initial['entire_controlling_TeX_lines_personally_read'] == 307 and initial['all_own_fresh_individual_rasters_personally_viewed'] == 5, 'personal whole reading')
    check(initial['printed_version_field_present'] is False and initial['printed_version'] is None, 'no invented printed version')
    check(initial['native_scientific_code_results_read_or_executed'] is False and initial['foreign_scientific_body_newly_opened_for_target_before_seal'] is False, 'paper-first boundary')
    check(gate['status'] == 'OPEN' and gate['parent_scientific_body_read'] is False, 'subsequent opaque root gate')
    check(verdict['full_original_claim_assessed'] is True and verdict['substantive_defect_found'] is False and verdict['exact_defect'] is None, 'literal scientific disposition')
    check(verdict['narrowed_replacement_proposed'] is False and verdict['repair_attempted'] is False, 'no repaired promotion')
    check(verdict['supported_parts']['each_focal_product_constant_iff'] == 'least n ≡ 2 (mod 4)', 'least-period qualifier')
    check(verdict['followup'] is None and verdict['publication_authority'] is False and verdict['peer_scientific_packets_read'] is False, 'limits and authority')
    check(verdict['native_scientific_replay_here'] is False and support['native_scientific_programs_executed_here'] == [], 'selected replay not duplicated')
    check(controls['status'] == 'PASS' and controls['primitive_cases'] == 982 and controls['nonprimitive_and_repeat_cases'] == 380 and controls['exact_normal_reflection_focal_cases'] == 399 and len(controls['four_bounce_controls']) == 28, 'own bounded controls scope')
    check(len(controls['primitive_rows']) == 982 and len(controls['nonprimitive_rows']) == 380, 'whole own result rows')
    check(len(support['code_personally_read_entire']) == 3 and sum(x['lines'] for x in support['code_personally_read_entire']) == 429, 'whole support code inspection')
    return errors

def file_errors(rows, base=None):
    errors = []
    for row in rows:
        path = Path(row['path'])
        if base is not None:
            if path.is_absolute() or '..' in path.parts:
                errors.append('unsafe owned path ' + str(path)); continue
            path = base / path
        if path.is_symlink() or not path.is_file():
            errors.append('missing or nonregular ' + str(path)); continue
        data = path.read_bytes()
        if len(data) != row['bytes'] or digest(data) != row['SHA256']:
            errors.append('byte binding mismatch ' + str(path))
    return errors

def verify():
    errors = []
    inputs, owned = obj(P/'INPUT_MANIFEST.json'), obj(P/'OWNED_MANIFEST.json')
    errors += file_errors(inputs['inputs'])
    errors += file_errors(owned['owned_files'], P)
    actual = {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f.name not in TERMINALS}
    expected = {x['path'] for x in owned['owned_files']}
    if actual != expected:
        errors.append('owned file universe changed')
    f = fixtures()
    errors += semantic_errors(f)
    r = f['ready']
    anchors = {
        S/'SOURCE_READY.json': '7f0b73ce3dc22426cd7f5db2037e2932594454c21c58dca9d9bfab06a7bcc60e',
        S/'SOURCE_READY_SEAL.json': '0d679ce38d996c2e0aa90cb9bce1c1fde84b0d2a625054af3c9e2491f2576720',
        P/'INITIAL_SEAL.json': '80b9dd8ae806df76347f4b02e126d88bc1bbadaae111805019b4cf31cc37f9e8',
        P/'INITIAL_RECONSTRUCTION.md': 'e7c18a9ab0630e75bb67aab54812e5087d9b1c17b5448ce984e23ae7d80f71c9',
        P/'INDEPENDENT_SCOPE_CONTROLS.json': '9767809f9bb199d31ed6d3eed71cba537849422f2243ceb6f83d08c119c49b4b',
    }
    for path, h in anchors.items():
        if digest(path.read_bytes()) != h:
            errors.append('immutable anchor ' + str(path))
    for asset in r['all_native_assets_in_original_order']:
        data = Path(asset['path']).read_bytes()
        md5 = asset['original_api_file_object']['checksum'].split(':',1)[1]
        if hashlib.md5(data).hexdigest() != md5 or digest(data) != asset['SHA256']:
            errors.append('native original checksum ' + asset['path'])
    custody = obj(S/'ARCHIVE_CUSTODY.json')
    payloads = custody['regular_payload_occurrences']
    with zipfile.ZipFile(Path(r['all_native_assets_in_original_order'][0]['path'])) as z:
        infos = z.infolist()
        if len(infos) != 13:
            errors.append('ZIP central-directory count')
        for info, member in zip(infos, payloads):
            data = z.read(info)
            if (info.filename != member['original_member_name'] or info.file_size != member['bytes'] or f'{info.CRC:08x}' != member['CRC32'] or info.compress_size != member['compressed_bytes'] or info.compress_type != member['compression_method'] or info.external_attr != member['native_external_attr'] or info.create_system != member['native_create_system'] or info.flag_bits != member['native_flags'] or list(info.date_time) != member['native_date_time'] or digest(data) != member['SHA256'] or data != Path(member['extracted_path']).read_bytes()):
                errors.append('ZIP occurrence binding ' + info.filename)
    if (P/'FINAL_SEAL.json').exists():
        seal = obj(P/'FINAL_SEAL.json')
        for name, h in seal['terminal_bindings'].items():
            if digest((P/name).read_bytes()) != h:
                errors.append('final terminal ' + name)
    return {'status': 'PASS' if not errors else 'FAIL', 'errors': errors, 'input_files': len(inputs['inputs']), 'owned_files': len(owned['owned_files']), 'ZIP_regular_occurrences': len(payloads), 'semantic_checks': 30, 'science_executed': False, 'writes': False, 'network': False}

def self_test():
    baseline = fixtures()
    if semantic_errors(baseline):
        raise RuntimeError('baseline metadata invalid')
    mutations = [
        ('source identity', lambda x: x['ready'].__setitem__('record_id',23306202)),
        ('version', lambda x: x['ready']['native_version_whole_field'].__setitem__('original_value','latest')),
        ('HTTP order', lambda x: x['ready'].__setitem__('HTTP_status_sequence',[200]*7)),
        ('date', lambda x: x['ready'].__setitem__('publication_date','2026-10-12')),
        ('created', lambda x: x['ready'].__setitem__('created',x['ready']['updated'])),
        ('asset order', lambda x: x['ready']['all_native_assets_in_original_order'].reverse()),
        ('empty object', lambda x: x['record'].__setitem__('swh',None)),
        ('version null', lambda x: x['versions']['hits']['hits'][0].__setitem__('swh',{})),
        ('files type', lambda x: x['files'].__setitem__('entries',{})),
        ('files null', lambda x: x['files'].__setitem__('default_preview','')),
        ('archive count', lambda x: x['ready'].__setitem__('whole_regular_payload_occurrences',12)),
        ('historical unread', lambda x: x['ready'].__setitem__('mathematical_PDF_TeX_or_pixels_read',True)),
        ('old gate', lambda x: x['initial'].__setitem__('root_gate','OPEN')),
        ('whole reading', lambda x: x['initial'].__setitem__('all_actual_PDF_pages_personally_read',4)),
        ('printed version', lambda x: x['initial'].__setitem__('printed_version','1.0.0')),
        ('paper first', lambda x: x['initial'].__setitem__('native_scientific_code_results_read_or_executed',True)),
        ('least period', lambda x: x['verdict']['supported_parts'].__setitem__('each_focal_product_constant_iff','listed N ≡ 2 (mod 4)')),
        ('scope narrowing', lambda x: x['verdict'].__setitem__('narrowed_replacement_proposed',True)),
        ('follow-up', lambda x: x['verdict'].__setitem__('followup',{})),
        ('duplicate native replay', lambda x: x['support'].__setitem__('native_scientific_programs_executed_here',['verify_exact.py'])),
        ('own counts', lambda x: x['controls'].__setitem__('primitive_cases',0)),
    ]
    rows = []
    for label, mutate in mutations:
        f = deepcopy(baseline)
        mutate(f)
        rejected = bool(semantic_errors(f))
        rows.append({'mutation': label, 'rejected': rejected})
        if not rejected:
            raise RuntimeError('undetected mutation ' + label)
    own = deepcopy(obj(P/'OWNED_MANIFEST.json')['owned_files'][:1])
    own[0]['SHA256'] = '0'*64
    rows.append({'mutation':'forged owned hash','rejected':bool(file_errors(own,P))})
    if not rows[-1]['rejected']:
        raise RuntimeError('forged hash accepted')
    return {'status':'PASS','in_memory_falsifiers':rows,'mutant_count':len(rows),'files_changed':False,'science_executed':False}

if __name__ == '__main__':
    import sys
    result = self_test() if sys.argv[1:] == ['--self-test'] else verify()
    print(json.dumps(result,indent=2))
    if result['status'] != 'PASS':
        raise SystemExit(1)
