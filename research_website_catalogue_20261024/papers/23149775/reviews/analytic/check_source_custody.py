#!/usr/bin/env python3
"""Read-only exact native-object/order/archive/initial/primary custody check."""
from pathlib import Path
import hashlib, json, sys, zipfile
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[1]
SOURCE = PAPER / 'sources'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok, label):
    if not ok: raise RuntimeError(label)
def load(p): return json.loads(p.read_text())
def main():
    need(len(sys.argv) == 1, 'no overrides')
    pins = {
      'SOURCE_READY.json': '4cd6366eabab646cbb7837b7b3854cf931b3fa57fc7de0152d0ff210ab35c16a',
      'SOURCE_READY_MANIFEST.json': '75bb9d07346b87e0203862e05fecbb02d9c0a7160e78f880eb8d2cf43c37e91c',
      'SOURCE_READY_SEAL.json': '77e6a3393dcbf34a6328d9c957f9dc6c757910cc1740ab9377cea2ec2848d201'}
    for name, h in pins.items(): need(sha(SOURCE/name) == h, 'native seal pin '+name)
    manifest = load(SOURCE/'SOURCE_READY_MANIFEST.json')
    names = set()
    for row in manifest['files']:
        p = SOURCE/row['path']; names.add(row['path'])
        need(p.stat().st_size == row['bytes'] and sha(p) == row['SHA256'], 'native payload '+row['path'])
    actual = {str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*') if p.is_file()}
    need(actual == names | {'SOURCE_READY_MANIFEST.json', 'SOURCE_READY_SEAL.json'}, 'whole native file set')
    need(len(names) == 38, '38 native sealed payloads')
    ready = load(SOURCE/'SOURCE_READY.json')
    need(ready['schema'] == 'source-ready-23149775-native-custody-v1', 'actual native schema')
    record = load(Path(ready['native_record_body_path']))
    latest = load(SOURCE/'latest.raw.json')
    need(record == latest, 'whole actual record object')
    assets = ready['all_native_assets_in_original_order']
    need(record['files'] == [a['original_api_file_object'] for a in assets], 'complete original file objects/order')
    need([a['original_api_file_object']['key'] for a in assets] == ['focal-pedal-ratios-note.pdf', 'focal-pedal-ratios-verification.zip'], 'PDF-first original order')
    m = record['metadata']
    need(m['publication_date'] == ready['publication_date_declared'] == '2026-10-04', 'declared date')
    need(m['version'] == ready['version'] == '1.0', 'native version')
    need(record['created'] == ready['record_created'] and record['updated'] == ready['record_updated'], 'distinct original creation/update dates')
    need(m['license'] == ready['original_native_license_object'] == {'id':'cc-by-4.0'}, 'entire original license object')
    need(m['resource_type'] == ready['original_native_resource_type_object'], 'whole resource type object')
    need(m['creators'] == ready['original_native_creators'], 'whole original author objects')
    need(record['doi'] == ready['DOI'] == '10.5281/zenodo.23149775', 'version DOI')
    need(str(record['conceptrecid']) == ready['conceptrecid'] == '23149774', 'concept identifier')
    for a in assets:
        p = Path(a['path']); data = p.read_bytes(); md5 = hashlib.md5(data).hexdigest()
        need(len(data) == a['bytes'] == a['original_api_file_object']['size'], 'native asset length')
        need(sha(p) == a['SHA256'], 'native asset SHA256')
        need(md5 == a['MD5'] and 'md5:'+md5 == a['original_api_file_object']['checksum'], 'native asset MD5')
    ac = load(SOURCE/'archive-custody.json')
    members = ac['regular_members']; need(len(members) == 24, '24 archive payloads')
    with zipfile.ZipFile(Path(assets[1]['path'])) as z:
        infos = z.infolist(); need(len(infos) == len(members), 'complete ZIP object list')
        expanded = 0
        for ordinal, (info, row) in enumerate(zip(infos, members), 1):
            need(not info.is_dir(), 'regular ZIP member')
            attrs = {'entry_ordinal':ordinal, 'original_member_name':info.filename,
              'CRC32':format(info.CRC,'08x'), 'declared_uncompressed_bytes':info.file_size,
              'compressed_bytes':info.compress_size, 'flag_bits':info.flag_bits,
              'compression_method':info.compress_type, 'date_time':list(info.date_time),
              'external_attr':info.external_attr, 'create_system':info.create_system,
              'comment_hex':info.comment.hex(), 'extra_hex':info.extra.hex()}
            for key, val in attrs.items(): need(row[key] == val, 'ZIP native attribute '+key+' '+info.filename)
            data = z.read(info); expanded += len(data)
            need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['SHA256'], 'whole ZIP member '+info.filename)
            need(Path(row['extracted_path']).read_bytes() == data, 'unchanged extracted member '+info.filename)
        need(expanded == 148381, 'complete expanded bytes')
    pdf = ready['selected_actual_PDF']; tex = ready['controlling_TeX']
    for r in [pdf, tex]: need(sha(Path(r['path'])) == r['SHA256'] and Path(r['path']).stat().st_size == r['bytes'], 'controlling reader/source identity')
    need(Path(pdf['path']).read_bytes() == (SOURCE/'cache/extracted/container-001/focal_pedal_ratios.pdf').read_bytes(), 'both published PDF copies exact')
    need(sha(HERE/'INITIAL_SEAL.json') == '9aa2324160d7c3febb036bb5665d04e3ce67d93e9c00296fb42c355fb70f9cc7', 'independent initial seal')
    initial = load(HERE/'INITIAL_SEAL.json')
    need(sha(HERE/'INITIAL_MANIFEST.json') == initial['manifest_SHA256'], 'independent initial manifest')
    for row in load(HERE/'INITIAL_MANIFEST.json')['files']:
        p = HERE/row['path']; need(p.stat().st_size == row['bytes'] and sha(p) == row['SHA256'], 'immutable initial '+row['path'])
    primaries = load(HERE/'PRIMARY_BINDINGS.json')['bindings']
    need(len(primaries) == 20, '20 actual primary bindings')
    for row in primaries:
        p = Path(row['path']); need(p.stat().st_size == row['bytes'] and sha(p) == row['SHA256'], 'primary body '+p.name)
    native = SOURCE/'cache/extracted/container-001'
    for name in ['verify_exact', 'verify_triangle', 'verify_historical_power', 'verify_reflection', 'reflection_geometry']:
        need((HERE/'cache/replay'/f'{name}.py').read_bytes() == (native/'verification'/f'{name}.py').read_bytes(), 'isolated unchanged mathematical program '+name)
    comparison = load(HERE/'SUPPLIED_COMPARISON.json')
    for row in comparison['records']:
        need((HERE/row['normal_output']).read_bytes() == Path(row['native_receipt']).read_bytes(), 'entire literal normal stdout '+row['program'])
        need((HERE/(Path(row['normal_output']).stem+'.stderr')).stat().st_size == 0, 'empty normal stderr '+row['program'])
    need(load(HERE/'SUPPLIED_EXACT_NORMAL.json')['status'] == 'PASS', 'literal supplied exact status')
    need(load(HERE/'SUPPLIED_REFLECTION_NORMAL.json')['status'] == 'PASS', 'literal supplied reflection status')
    sens = load(HERE/'ASSERT_MODE_SENSITIVITY.json')
    need(sens['records'][0]['wrong_scalar_rejected'] and not sens['records'][1]['wrong_scalar_rejected'] and sens['records'][1]['literal_stdout_status'] == 'PASS', 'preserved native assert-mode limitation')
    print(json.dumps({'assessment':'FULL_NATIVE_OBJECT_ORDER_BYTES_INITIAL_AND_PRIMARY_CUSTODY_RECONFIRMED',
      'native_manifest_payloads':38, 'native_files_including_manifest_seal':40,
      'native_archive_members':24, 'initial_manifest_payloads':10, 'critical_primary_bindings':20,
      'isolated_native_programs':5, 'selected_normal_stdout_entire_byte_matches':4,
      'native_asset_order':['PDF','ZIP'], 'native_literal_status':'PASS',
      'native_optimized_assert_guards_are_not_validation':True,
      'sources_or_packets_modified':False}, indent=2, sort_keys=True))
if __name__ == '__main__': main()
