#!/usr/bin/env python3
"""Pure offline saved-evidence custody; no scientific execution/import or writes."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile
import zlib

E = Path(__file__).resolve().parent
S = E.parent.parent / 'sources'
CHECKS = 0


def need(ok, label):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(label)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def readj(p):
    return json.loads(p.read_text())


def checkfile(o, override=None):
    p = Path(override if override is not None else o['path'])
    need(p.is_file() and not p.is_symlink(), 'regular file '+str(p))
    b = p.read_bytes()
    need(len(b) == o['bytes'], 'entire size '+str(p))
    need(digest(b) == o['SHA256'], 'entire SHA256 '+str(p))
    return b


def main():
    preseal = sys.argv[1:] == ['--preseal']
    need(not sys.argv[1:] or preseal, 'only optional --preseal accepted')
    inputs = readj(E/'INPUT_MANIFEST.json')['whole_source_directory']
    for o in inputs:
        checkfile(o)
    need(len(inputs) == 81, 'complete original source count')
    need({str(p) for p in S.rglob('*') if p.is_file()} ==
         {o['path'] for o in inputs}, 'complete unchanged source file set')
    for name, pin in [
        ('SOURCE_READY.json', '928fb2b26bd31a0678fc3954c29f8a7897a3d6352e9b5dab791224a72a828235'),
        ('SOURCE_READY_SEAL.json', '0fed874ecff807d3250957b196f39902b124825dd0c5fa90bd1efa2bf406679e')]:
        need(digest((S/name).read_bytes()) == pin, 'native authority pin '+name)
    for name, pin in [
        ('INITIAL_SEAL.json', 'bd14ee78f87c2ade358b7efbb6c4977bbf07ffa0562c4afa07afbb655a1652ee'),
        ('OWN_PROOF_RESULTS_SEAL.json', '8acabe5986362e7bd26b033b25f9db538c3f399d08a1caff979ee4fc75641b92')]:
        need(digest((E/name).read_bytes()) == pin, 'early independence seal '+name)
        for o in readj(E/name)['files']:
            checkfile(o)

    ready = readj(S/'SOURCE_READY.json')
    custody = readj(E/'SOURCE_CUSTODY.json')
    need(custody['whole_original_source_ready_object'] == ready, 'whole READY retained')
    for o in custody['literal_native_copies']:
        b = checkfile(o, E/o['copy_path'])
        need(b == Path(o['original_path']).read_bytes(), 'literal copy, no schema adaptation')
    need(len(custody['literal_native_copies']) == 21, 'complete native copy set')
    native = {}
    for o in ready['whole_native_API_objects']:
        native[o['role']] = json.loads(checkfile(o))
    need(native['record'] == native['latest'], 'whole latest record agreement')
    need(native['record']['swh'] == {} and native['latest']['swh'] == {}, 'native empty objects')
    need(native['versions-page001']['hits']['hits'][0]['swh'] is None, 'version null not normalized')
    f = native['files']
    need(type(f['entries']) is list and f['order'] == [] and f['default_preview'] is None,
         'files entry type / empty order / null preview')
    need([o['key'] for o in native['record']['files']] == [
        'totally-mixed-face-posets-source-and-verification.zip', 'totally-mixed-face-posets.pdf'],
        'original ZIP then PDF order')
    need(ready['source_programmes_executed'] == [] and
         ready['source_scientific_proofs_code_results_triage_reviews_or_opinions_read'] is False,
         'historical acquisition unread flags unchanged')
    transports = readj(S/'ALL_TRANSPORT_RECEIPTS.json')
    need(transports == custody['all_actual_transport_receipts_whole'], 'whole actual transports')
    need(len(transports) == 7 and [x['HTTP_status'] for x in transports] ==
         [200,301,200,200,200,200,200], 'complete actual native status sequence')
    for t in transports:
        checkfile({'path':t['body_path'], 'bytes':t['bytes'], 'SHA256':t['SHA256']})
        need(type(t['response_headers_in_received_order']) is list, 'ordered opaque received headers')
    need(ready['failed_transports_preserved_whole'] == [], 'native empty failure history')

    archive = readj(S/'ARCHIVE_CUSTODY.json')
    need(archive == custody['whole_original_archive_custody_object'], 'whole original archive object')
    count = 0
    for c in archive['containers']:
        checkfile({'path':c['input_path'], 'bytes':c['input_bytes'], 'SHA256':c['input_SHA256']})
        with zipfile.ZipFile(c['input_path']) as z:
            info = z.infolist()
            need(len(info) == len(c['members']), 'whole native central directory')
            for zi, m in zip(info, c['members']):
                b = z.read(zi)
                need(zi.filename == m['original_member_name'], 'native member name and order')
                need(len(b) == zi.file_size == m['bytes'], 'native member whole size')
                need(digest(b) == m['SHA256'], 'native member whole SHA256')
                need(zi.CRC == (zlib.crc32(b)&0xffffffff) == int(m['CRC32'],16), 'full-read native CRC32')
                need((zi.compress_size, zi.compress_type, zi.external_attr, zi.create_system,
                      zi.flag_bits, list(zi.date_time)) ==
                     (m['compressed_bytes'], m['compression_method'], m['native_external_attr'],
                      m['native_create_system'], m['native_flags'], m['native_date_time']),
                     'complete native ZIP metadata')
                need(b == Path(m['extracted_path']).read_bytes(), 'entire extracted payload')
                need(b == (E/'native-isolated'/zi.filename).read_bytes(), 'unchanged isolated payload')
                count += 1
    need(count == 29 and archive['whole_regular_payload_occurrences'] == 29 and
         archive['recursive_archive_container_count'] == 1 and archive['nested_archive_count'] == 0,
         'entire 29-payload native archive')
    need(Path(ready['embedded_PDFs'][0]['extracted_path']).read_bytes() ==
         Path(ready['selected_actual_PDF']['path']).read_bytes(), 'embedded/native PDF identical')

    replay = readj(E/'NATIVE_REPLAY.json')
    expected_path = Path(replay['expected_original_path'])
    b = expected_path.read_bytes()
    need(len(b) == replay['EXPECTED_ORIGINAL_BYTES'] == 6908 and
         digest(b) == replay['EXPECTED_ORIGINAL_SHA256'], 'whole original expected wrapper')
    expected = json.loads(b)
    need(expected == replay['whole_original_expected_object'], 'whole expected wrapper object')
    need([(x['checker'],x['mode']) for x in replay['runs']] ==
         [('geometry','normal'),('geometry','optimized'),('topology','normal'),('topology','optimized')],
         'exact bounded original checker/mode run set')
    for r in replay['runs']:
        prefix = 'NATIVE_'+r['checker']+'_'+r['mode']
        out, err = (E/(prefix+'.stdout')).read_bytes(), (E/(prefix+'.stderr')).read_bytes()
        need(r['exit_code'] == 0 and err == b'', 'saved native successful run')
        need(json.loads(out) == expected[r['checker']], 'entire expected subobject')
        encoded = (json.dumps(expected[r['checker']],indent=2,sort_keys=True)+'\n').encode()
        need(out == encoded, 'whole native stdout versus exact original print encoding')
        need(digest(out) == r['stdout_SHA256'] and digest(err) == r['stderr_SHA256'], 'saved complete stream pins')
    for name in ['geometry','topology']:
        need((E/('NATIVE_'+name+'_normal.stdout')).read_bytes() ==
             (E/('NATIVE_'+name+'_optimized.stdout')).read_bytes(), 'normal/optimized whole byte equality')
    comparison = readj(E/'NATIVE_WHOLE_COMPARISON.json')
    need(comparison['whole_original_expected_wrapper'] == expected, 'whole additional comparison wrapper')
    need(len(comparison['comparisons']) == 4 and all(
        r['entire_saved_stdout_equals_derived_expected_bytes'] and
        r['entire_saved_output_object_equals_original_expected_subobject']
        for r in comparison['comparisons']), 'complete comparison claims consistent')
    for o in readj(E/'OWN_RENDER_RECEIPT.json')['rasters']:
        checkfile(o)

    successful_primaries = failed_primaries = 0
    for rp in sorted((E/'cache/primary').glob('*.receipt.json')):
        r = readj(rp)
        for key in ['body','headers']:
            if r[key] is not None:
                checkfile(r[key], E/r[key]['path'])
        status = r['curl_writeout_whole']['http_code'] if r['curl_writeout_whole'] else None
        if r['curl_exit_code'] == 0 and status == 200:
            successful_primaries += 1
        else:
            failed_primaries += 1
    need(successful_primaries == 7 and failed_primaries == 2, 'bounded primary bodies and actual failures retained')

    # Bind the already-frozen metadata child without importing or replaying it.
    child = E/'custody-child'
    cb = readj(E/'CHILD_CUSTODY_BINDING.json')
    cs = readj(child/'FINAL_SEAL.json')
    cm = readj(child/'MANIFEST.json')
    need(digest((child/'FINAL_SEAL.json').read_bytes()) == cb['CHILD_FINAL_SEAL_SHA256'],
         'frozen metadata child seal')
    need(digest((child/'MANIFEST.json').read_bytes()) == cs['manifest_sha256'],
         'whole metadata child manifest')
    need(readj(child/'RESULT.json') == cb['whole_child_result'] and
         cb['whole_child_result']['errors'] == [], 'whole child metadata result')
    need(digest((E/'INPUT_MANIFEST.json').read_bytes()) == cs['parent_INPUT_MANIFEST_sha256'] and
         digest((E/'SOURCE_CUSTODY.json').read_bytes()) == cs['parent_SOURCE_CUSTODY_sha256'],
         'child bound the unchanged parent custody inputs')
    for o in cm['files']:
        checkfile(o, child/o['relative_path'])
    need({str(p.relative_to(child)) for p in child.rglob('*') if p.is_file()} ==
         {o['relative_path'] for o in cm['files']} | {'MANIFEST.json','FINAL_SEAL.json'},
         'exact frozen child file set')

    owned_count = None
    if not preseal:
        manifest, seal = readj(E/'MANIFEST.json'), readj(E/'SEAL.json')
        need(digest((E/'MANIFEST.json').read_bytes()) == seal['MANIFEST_SHA256'], 'owned manifest seal')
        owned = manifest['owned_files']
        for o in owned:
            checkfile(o, E/o['path'])
        need({str(p.relative_to(E)) for p in E.rglob('*') if p.is_file()} ==
             {o['path'] for o in owned} | {'MANIFEST.json','SEAL.json'}, 'exact owned file set')
        owned_count = len(owned)
        for n, field in [('REPORT.md','REPORT_SHA256'),('VERDICT.json','VERDICT_SHA256'),
                         ('DERIVATIONS.md','DERIVATIONS_SHA256')]:
            need(digest((E/n).read_bytes()) == seal[field], 'final whole body pin '+n)
    print(json.dumps({'status':'PASS_READ_ONLY_SAVED_CUSTODY', 'mode':'preseal' if preseal else 'final',
                      'checks':CHECKS, 'source_inputs':len(inputs), 'original_ZIP_payloads':count,
                      'owned_payloads':owned_count, 'successful_primary_bodies':successful_primaries,
                      'actual_primary_access_failures_retained':failed_primaries,
                      'scientific_code_imported_or_executed':False,
                      'network_or_file_writes':False},indent=2))


if __name__ == '__main__':
    main()
