"""Standalone stdlib-only custody/data verifier. No project imports or execution.

Default checks the audit, sealed writer packet,607 originals/snapshots and prior
packets. --live-baseline additionally requires the pre-install585 public fence.
--payload-only is the explicitly recorded audit-preseal receipt mode.
"""
from pathlib import Path
import hashlib
import json
import sys

CONTROL = {'OWNED_MANIFEST.json', 'FINAL_SEAL.json', 'PAYLOAD_NORMAL.stdout.json',
           'PAYLOAD_NORMAL.stderr', 'PAYLOAD_OPTIMIZED.stdout.json',
           'PAYLOAD_OPTIMIZED.stderr', 'PAYLOAD_RECEIPT.json'}


def need(value, why):
    if not value: raise ValueError(why)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def obj(path): return json.loads(Path(path).read_bytes())


def same(a, b):
    need(type(a) is type(b) and json.dumps(a, ensure_ascii=False, separators=(',', ':'), allow_nan=False) ==
         json.dumps(b, ensure_ascii=False, separators=(',', ':'), allow_nan=False), 'whole typed/ordered literal object differs')


def file_binding(path, row):
    path = Path(path); need(path.is_file() and not path.is_symlink(), 'absent/symlink: ' + str(path))
    raw = path.read_bytes(); need(len(raw) == row['bytes'] and sha(raw) == row['SHA256'], 'whole byte binding differs: ' + str(path))
    return raw


def literal_native(root, writer, contracts, frozen):
    actual = obj(writer / 'NATIVE_CONTRACTS.json')['records']; need(len(actual) == 2, 'native record count')
    verdicts = 0; api = 0; wrapper_count = 0
    def wrappers(value):
        nonlocal wrapper_count
        if isinstance(value, dict):
            if 'whole_literal_object' in value and 'path' in value:
                raw = file_binding(value['path'], value)
                same(json.loads(raw), value['whole_literal_object']); wrapper_count += 1
                need(value['path'] in frozen, 'whole wrapper not in607 originals')
            for child in value.values(): wrappers(child)
        elif isinstance(value, list):
            for child in value: wrappers(child)
    for approved, row in zip(contracts['records'], actual):
        rid = approved['record_id']; need(row['record_id'] == rid, 'native record order/identity')
        pub = approved['whole_original_publication']; pro = approved['whole_original_promotion']; sb = pub['source_binding']
        for key in ['publication', 'promotion', 'adapter']:
            binding = approved['source_paths'][key]; raw = file_binding(binding['path'], binding)
            same(json.loads(raw), approved['whole_original_' + key])
        same(row['whole_original_source_ready'], sb['whole_original_source_ready'])
        same(row['whole_original_native_API_objects'], sb['whole_original_native_API_objects'])
        api += len(sb['whole_original_native_API_objects'])
        protocol_path = sb['source_protocol_binding_file'] if rid == '23439582' else sb['source_protocol_binding_path']
        raw = file_binding(protocol_path, frozen[protocol_path]); same(row['whole_native_transport_protocol'], json.loads(raw))
        wrappers(row['whole_native_transport_protocol'])
        vk = 'whole_original_two_scientific_custom_verdicts' if rid == '23439582' else 'whole_original_custom_scientific_verdicts'
        same(row['whole_original_two_scientific_custom_verdicts'], pro[vk]); same(pro[vk], pub['review_metadata'][vk])
        for v in pro[vk]: same(v['whole_literal_object'], json.loads(file_binding(v['path'], v))); verdicts += 1
        same(row['historical_publication_flags_unchanged'], pro)
        need(pub['canonical_url'] is None and pub['AA'] is None and pub['follow_up'] is None and pro['follow_up'] is None, 'original canonical/AA/followup boundary')
        need(row['authored_package_license'] == pub['license'] == 'CC BY 4.0', 'actual CC license')
        need(row['separate_code_instrument'] == pub['code_license'] == ('CC BY 4.0' if rid == '23439582' else None), 'literal separate code-license field')
        if rid == '23439582':
            need(sb['historical_ready_completion_percent'] == 95 and sb['final_source_seal_completion_percent'] == 100 and sb['native_ZIP_fresh_GET_claimed'] is False, '121 source history normalized')
            need(len(sb['whole_six_actual_new_transport_objects']) == 6 and len(sb['whole_three_historical_403_transport_objects']) == 3, '121 transport history cardinality')
        else: need(len(sb['whole_original_seven_transport_objects']) == 7, '122 seven transports')
    need(verdicts == 4 and api == 8, 'whole custom verdict/API cardinality')
    return {'whole_literal_scientific_verdicts': verdicts, 'whole_native_API_objects': api,
            'whole_json_wrappers_against_original_raw_bytes': wrapper_count,
            '121_new_transports': 6, '121_retained_old403_transports': 3, '122_transports': 7}


def verify_payload(root, live=False):
    root = Path(root); manifest = obj(root / 'OWNED_MANIFEST.json')
    need(set(manifest['excluded_control_files']) == CONTROL, 'audit control exclusions')
    names = []
    for row in manifest['files']:
        p = Path(row['path']); need(not p.is_absolute() and '..' not in p.parts, 'unsafe audit relative path')
        names.append(row['path']); file_binding(root / p, row)
    need(len(names) == len(set(names)), 'duplicate owned path')
    need({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()} - CONTROL == set(names), 'audit closed namespace')
    initial = obj(root / 'INDEPENDENT_INITIAL_SEAL.json')
    need(sha((root / 'INDEPENDENT_INITIAL_SEAL.json').read_bytes()) == 'f85a2ddbe21c8b0212fe74b34cdb09a584d40af04e5578e6042c023c6adbbcbe', 'pre-writer-exposure independent initial seal')
    need(sha((root / 'INDEPENDENT_INITIAL_MANIFEST.json').read_bytes()) == initial['INDEPENDENT_INITIAL_MANIFEST_SHA256'], 'independent initial manifest')
    for row in obj(root / 'INDEPENDENT_INITIAL_MANIFEST.json')['files']: file_binding(root / row['path'], row)
    for row in obj(root / 'PRESENTATION_SUPPLEMENT_SEAL.json')['files']: file_binding(root / row['path'], row)
    intake = obj(root / 'WRITER_INTAKE.json'); writer = Path(intake['writer_root'])
    for name, row in intake['advertised_pins_authenticated'].items(): file_binding(writer / name, row)
    need(sha((writer / 'FINAL_SEAL.json').read_bytes()) == '93f0f4409c29185d4947b6050a15db3da82beb674dc6dfb5eef1d4bfcd084a34', 'exact adopted-for-audit writer seal')
    wm = obj(writer / 'OWNED_MANIFEST.json'); wn = set()
    for row in wm['files']:
        p = Path(row['path']); need(not p.is_absolute() and '..' not in p.parts and row['path'] not in wn, 'writer owned namespace safety')
        wn.add(row['path']); file_binding(writer / p, row)
    need(len(wn) == 541 and {p.relative_to(writer).as_posix() for p in writer.rglob('*') if p.is_file()} == wn | {'OWNED_MANIFEST.json', 'FINAL_SEAL.json'}, 'whole writer closed541 payloads')
    need(not any(p.is_symlink() for p in writer.rglob('*')), 'writer symlink')
    frozen_rows = obj(writer / 'FROZEN_INPUTS.json')['files']; frozen = {r['original_path']: r for r in frozen_rows}
    need(len(frozen) == len(frozen_rows) == 607, 'exact607 original bindings')
    same(obj(root / 'WRITER_FROZEN_INPUTS.json'), obj(writer / 'FROZEN_INPUTS.json'))
    snapshots = set()
    for row in frozen_rows:
        file_binding(row['original_path'], row); file_binding(writer / row['snapshot_path'], row)
        need(row['snapshot_path'].startswith('inputs/blobs/'), 'raw snapshot private boundary')
        snapshots.add(row['snapshot_path'])
    need(len(snapshots) == 452 and '/inputs/blobs/' in (writer / '.gitignore').read_text().splitlines(), 'all452 raw bodies private-ignored and authenticated')
    baseline = obj(root / 'INDEPENDENT_BASELINE.json')
    for row in baseline['original_pair_files']:
        file_binding(row['path'], row); need(row['path'] in frozen, 'independently captured original paper omitted')
        need(row['SHA256'] == frozen[row['path']]['SHA256'] and row['bytes'] == frozen[row['path']]['bytes'], 'independent source607 consistency')
    need(len(baseline['original_pair_files']) == 597, 'independent original pair cardinality')
    for packet in baseline['prior_two_and_five_packets']:
        for row in packet['whole_fresh_file_bindings']: file_binding(row['path'], row)
    for row in obj(root / 'PAIRED_INDEPENDENT_OUTPUTS.json')['full_ten_files_compared']:
        a = file_binding(writer / 'candidate-a/public' / row['path'], row)
        need(a == file_binding(writer / 'candidate-b/public' / row['path'], row), 'paired whole ten-path bytes differ')
    native = literal_native(root, writer, obj(root / 'APPROVED_CONTRACTS.json'), frozen)
    supplement = obj(writer / 'ROOT_AUTHORIZED_CORE_SUPPLEMENT.json')
    need(supplement['authorized_current_SHA256'] == '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0' and
         supplement['original_baseline_binding']['SHA256'] == '91d5c5d285502e5a82f3eb090cf3399458c96416a873a674439ef5a1b435af5b', 'exact one-helper authority qualification')
    verdict = obj(root / 'CUSTOM_VERDICT.json')
    need(verdict['literal_custom_verdict'] == 'PRIVATE_PAIRED_INTEGRATION_FIDELITY_CONFIRMED_WITH_DISCLOSED_PRESENTATION_SUPPLEMENT_ROOT_ADOPTION_PENDING', 'own full literal qualified verdict')
    need(verdict['root_installation_or_publication_authority'] is False and verdict['canonical_url'] is None and verdict['AA'] is None and verdict['follow_up'] is None, 'own final authority boundary')
    if live:
        public = Path(baseline['public_root']); rows = baseline['public_files']
        need({str(p) for p in public.rglob('*') if p.is_file()} == {r['path'] for r in rows}, 'current585 public namespace')
        for row in rows: file_binding(row['path'], row)
        for row in baseline['current_core18_and_exact_authorized_single_helper_delta']: file_binding(row['fresh_current']['path'], row['fresh_current'])
        for row in obj(writer / 'FRESH_BASELINE.json')['site_configurations']: file_binding(row['path'], row)
    return {'literal_custom_status': 'READ_ONLY_INDEPENDENT_AUDIT_AND_SEALED_PRIVATE_STAGE_CUSTODY_CONFIRMED',
            'own_payloads': len(names), 'writer_payloads': len(wn), 'original_inputs': 607, 'raw_private_snapshots': 452,
            'independently_prefrozen_original_paper_files': 597, 'paired_identical_outputs': 10,
            'native_literal_comparison': native, 'live_preinstall_baseline_explicitly_checked': live,
            'historical_core_qualification': '17 original entries plus one exact root-authorized checkpoint helper405b0357; no other drift',
            'project_imports_subprocess_science_network_or_writes': False}


def verify(root, live=False, payload_only=False):
    root = Path(root); result = verify_payload(root, live)
    if not payload_only:
        seal = obj(root / 'FINAL_SEAL.json')
        need(sha((root / 'OWNED_MANIFEST.json').read_bytes()) == seal['OWNED_MANIFEST_SHA256'], 'audit final manifest seal')
        for row in seal['terminal_payload_receipts']: file_binding(root / row['path'], row)
        need(len(seal['terminal_payload_receipts']) == 5, 'terminal receipt count')
        result['final_audit_seal_receipts_confirmed'] = True
    return result


if __name__ == '__main__':
    allowed = {'--live-baseline', '--payload-only'}; need(set(sys.argv[1:]) <= allowed, 'unknown arguments')
    print(json.dumps(verify(Path(__file__).resolve().parent, '--live-baseline' in sys.argv, '--payload-only' in sys.argv), indent=2))
