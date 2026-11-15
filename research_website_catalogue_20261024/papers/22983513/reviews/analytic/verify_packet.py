#!/usr/bin/env python3
"""Read-only local custody closure; no network or scientific program replay."""
from pathlib import Path
import hashlib
import json
import zipfile
import zlib


E = Path(__file__).resolve().parent
COUNT = 0


def need(ok, label):
    global COUNT
    COUNT += 1
    if not ok:
        raise RuntimeError(label)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bound_file(root, row):
    p = root / row['path']
    need(p.is_file(), 'file exists: ' + str(p))
    need(p.stat().st_size == row['bytes'], 'size: ' + str(p))
    need(sha(p) == row['sha256'], 'SHA256: ' + str(p))


def main():
    m = json.loads((E/'FINAL_MANIFEST.json').read_text())
    for row in m['files']:
        need(not Path(row['path']).is_absolute() and '..' not in Path(row['path']).parts,
             'owned path remains in lane')
        bound_file(E, row)
    excluded = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json', 'CLOSURE_EXECUTIONS.json'}
    actual = {str(p.relative_to(E)) for p in E.rglob('*') if p.is_file()
              and str(p.relative_to(E)) not in excluded}
    need(actual == {x['path'] for x in m['files']}, 'complete owned manifest')
    initial = json.loads((E/'INITIAL_SEAL.json').read_text())
    need(sha(E/'INITIAL_SEAL.json') == '042591bae1c2a24b8c2009d8e64ef731426276f11300ebf721b00b52215c1f1d',
         'immutable initial seal')
    need(sha(E/initial['manifest_path']) == initial['manifest_sha256'], 'initial manifest')
    for row in json.loads((E/initial['manifest_path']).read_text())['files']:
        bound_file(E, row)
    native = json.loads((E/'NATIVE_CUSTODY_BINDINGS.json').read_text())
    for row in native['bindings']:
        bound_file(Path('/'), row)
    ready = json.loads((E/'native-custody/SOURCE_READY.original.json').read_text())
    need(sha(Path(native['bindings'][0]['path'])) ==
         '9ab3aa2364dbc078c0cae228e9a627b75586a6da5f9a1a4c2111391c5bd5ca20', 'pinned original SOURCE_READY')
    for item in ready['whole_native_API_objects']:
        need(Path(item['path']).read_bytes() == (E/'native-custody'/Path(item['path']).name).read_bytes(),
             'literal native API snapshot')
    for key in ['native_schema_types_path', 'whole_archive_custody_path', 'actual_transport_receipt_path']:
        need(Path(ready[key]).read_bytes() == (E/'native-custody'/Path(ready[key]).name).read_bytes(),
             'literal native custody/transport snapshot')
    transport = json.loads(Path(ready['actual_transport_receipt_path']).read_text())
    need(isinstance(transport, list) and len(transport) == 8, 'actual receipt array schema')
    need([x['HTTP_status'] for x in transport] == [200,200,400,200,200,200,200,200],
         'failed transport retained in actual order')
    for x in transport:
        need(isinstance(x['response_headers_in_order'], list), 'ordered native response headers')
        need(sha(Path(x['body_path'])) == x['SHA256'], 'transport body')
    archive = json.loads(Path(ready['whole_archive_custody_path']).read_text())
    rows = archive['archive_containers'][0]['entries_in_original_order']
    with zipfile.ZipFile(ready['all_assets_in_original_order'][0]['path']) as z:
        need(z.testzip() is None, 'ZIP CRC')
        need(z.namelist() == [x['original_member_name'] for x in rows], 'native member order')
        for info, row in zip(z.infolist(), rows):
            b = z.read(info)
            need(b == Path(row['extracted_path']).read_bytes(), 'all member extracted bytes')
            need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['SHA256'], 'member size/SHA')
            need(f'{zlib.crc32(b)&0xffffffff:08x}' == row['CRC32'], 'member CRC32')
    repro = json.loads((E/'NATIVE_REPRODUCTION.json').read_text())
    a = (E/'reproduction/normal-results.json').read_bytes()
    need(a == (E/'reproduction/optimized-results.json').read_bytes() ==
         (E/'reproduction/deposited-results.json').read_bytes(), 'native normal/optimized/deposited identity')
    need(hashlib.sha256(a).hexdigest() == repro['results_sha256'], 'native results receipt')
    r = json.loads(a)
    need(r['check_count'] == 7016 and r['boxes']['J_cases'] == 1312, 'bounded native counts')
    own = json.loads((E/'INDEPENDENT_CHECK_RESULTS.json').read_text())
    need(len(own['threshold_cases']) == 7 and own['closed_form_J_cases'] == 128,
         'independent bounded evidence present; no replay')
    v = json.loads((E/'VERDICT.json').read_text())
    need(v['followup'] is None and v['publication_or_promotion_authorized'] is False,
         'no unsolicited follow-up or action authorization')
    if (E/'FINAL_SEAL.json').exists():
        s = json.loads((E/'FINAL_SEAL.json').read_text())
        need(sha(E/'FINAL_MANIFEST.json') == s['manifest_sha256'], 'final manifest seal')
        need(sha(E/'CLOSURE_EXECUTIONS.json') == s['closure_executions_sha256'], 'sealed closure receipt')
    print(json.dumps(dict(status='PASS_READ_ONLY_ANALYTIC_CUSTODY', checks=COUNT,
                          owned_manifest_files=len(m['files']), external_source_bindings=len(native['bindings']),
                          zip_members=len(rows), network_calls=0, scientific_replays=0, writes=0)))


if __name__ == '__main__':
    main()
