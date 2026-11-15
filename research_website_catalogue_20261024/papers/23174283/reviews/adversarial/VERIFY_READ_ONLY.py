"""Custody-only closure: python3 -E -B VERIFY_READ_ONLY.py [--preseal].

Reads hashes and archive payloads. No writes, network, or deposited program execution.
This verifier closes evidence identity, not the correctness of an infinite theorem.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import unicodedata
import zipfile


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


require(sys.flags.ignore_environment and sys.dont_write_bytecode,
        'use python3 -E -B for read-only closure')
require(sys.argv[1:] in ([], ['--preseal']), 'unsupported arguments')
preseal = sys.argv[1:] == ['--preseal']
P = Path(__file__).resolve().parent
B = P.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def obj(path):
    return json.loads(path.read_text())


def check_binding(path, entry, label):
    require(path.is_file() and not path.is_symlink(), label+' regular file')
    require(path.stat().st_size == entry['bytes'], label+' byte count')
    require(digest(path) == entry.get('SHA256', entry.get('sha256')), label+' SHA256')


inputs = obj(P/'INPUT_MANIFEST.json')
require(digest(B/'sources/SOURCE_READY.json') ==
        'b9f69bfea594378f8cd69a00d214ce14c894fd33e850047a915327432d96ae20',
        'frozen READY identity')
for entry in inputs['source_files']:
    path = B/entry['path']
    require(path.resolve().is_relative_to(B/'sources'), 'source binding path')
    check_binding(path, entry, entry['path'])
actual_sources = {str(x.relative_to(B)) for x in (B/'sources').rglob('*') if x.is_file()}
require(actual_sources == {x['path'] for x in inputs['source_files']}, 'complete frozen source set')
ready = obj(B/'sources/SOURCE_READY.json')
for entry in ready['all_assets_in_original_order']:
    path = Path(entry['path'])
    check_binding(path, entry, 'native asset')
    data = path.read_bytes()
    require(hashlib.md5(data).hexdigest() == entry['md5'], 'native asset MD5')
    require(entry['original_api_file_object']['checksum'] == 'md5:'+entry['md5'],
            'native API checksum binding')
require(ready['selected_actual_PDF']['pages'] == 3, 'frozen actual reader pages')
check_binding(Path(ready['controlling_TeX']['path']), ready['controlling_TeX'], 'sole controlling TeX')

seen = set()
zip_count = 0
zip_bytes = 0
with zipfile.ZipFile(B/'sources/spherical_fibonacci_verification.zip') as archive:
    for info in archive.infolist():
        name = info.filename
        parts = PurePosixPath(name).parts
        require(parts and not name.startswith('/') and '\\' not in name and ':' not in name
                and all(x not in ('', '.', '..') for x in parts), 'safe ZIP name')
        require(not info.is_dir() and not (info.flag_bits & 1), 'regular unencrypted ZIP member')
        require(stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG), 'no link/device ZIP payload')
        collision = unicodedata.normalize('NFC', name).casefold()
        require(collision not in seen, 'no normalized ZIP collision')
        seen.add(collision)
        data = archive.read(info)  # ZipFile validates actual CRC during the complete read.
        require(len(data) == info.file_size, 'complete ZIP payload')
        target = B/'sources/published-source'/name
        require(target.resolve().is_relative_to(B/'sources/published-source'), 'ZIP custody path')
        require(target.read_bytes() == data, 'whole payload equals frozen extraction')
        zip_count += 1
        zip_bytes += len(data)
require(zip_count == 13 and zip_bytes == 51353, 'complete support package size')
deposited_manifest = obj(B/'sources/published-source/MANIFEST.json')
for name, entry in deposited_manifest['payload'].items():
    check_binding(B/'sources/published-source'/name, entry, 'deposited manifest '+name)

initial = obj(P/'INITIAL_SEAL.json')
require(digest(P/'INITIAL_SEAL.json') ==
        '527cbe8fb0216c1af6a41ef2dbc2c8cd33ebf34cdbf635e1ac0b7154c8337c2c', 'independent initial seal')
require(digest(P/'INITIAL_MANIFEST.json') == initial['manifest_SHA256'], 'initial manifest hash')
for entry in obj(P/'INITIAL_MANIFEST.json')['files']:
    path = Path(entry['path'])
    require(path.resolve().is_relative_to(P), 'initial owned path')
    check_binding(path, entry, 'initial file')
require(digest(P/'INITIAL_RECONSTRUCTION.md') == initial['reconstruction_SHA256'], 'initial reconstruction')

for receipt in obj(P/'PRIMARY_FETCH_RECEIPTS.json'):
    path = Path(receipt['path'])
    require(path.resolve().is_relative_to(P/'private-primary'), 'private primary path')
    check_binding(path, receipt, 'actual primary response')
    require(receipt['HTTP_status'] == 200 and path.read_bytes().startswith(b'%PDF'), 'actual PDF response')

executions = obj(P/'EXECUTION_RECEIPTS.json')
for receipt in executions:
    require(receipt['exit_code'] == 0 and receipt['outcome_status'] == 'PASS', 'bounded initial execution')
    require(digest(P/receipt['stdout_path']) == receipt['stdout_SHA256'], 'bounded stdout custody')
    require(digest(P/receipt['stderr_path']) == receipt['stderr_SHA256'], 'bounded stderr custody')
    script = P/'own_exact_controls.pre-correction.py' if receipt['name'] == 'own-exact-controls' else B/'sources/published-source/proof_controls.py'
    require(digest(script) == receipt['script_SHA256'], 'actual original executed script')
correction = obj(P/'EXECUTION_CORRECTION_RECEIPT.json')
require(correction['exit_code'] == 0 and digest(P/'own_exact_controls.py') == correction['script_SHA256'],
        'corrected actual own script')
require(digest(P/'own-exact-controls-v2.stdout.json') == correction['stdout_SHA256'], 'final own stdout')
require(digest(P/'own-exact-controls-v2.stderr.txt') == correction['stderr_SHA256'], 'final own stderr')
out = obj(P/'own-exact-controls-v2.stdout.json')
require(out['status'] == 'PASS' and out['direct_radical_pairs'] == 42
        and out['arithmetic_offsets'] == 6746, 'bounded final control identities')
certs = out['direct_radical_certificates']
for q in (2, 3, 5, 8):
    selected = [x for x in certs if x['q'] == q]
    require({(x['i'], x['j']) for x in selected} ==
            {(i, j) for i in range(q) for j in range(i+1, q)}, 'complete direct pair set')
    require([(x['i'], x['j']) for x in selected if x['comparison'] == 'equality'] == [(0, 1)],
            'bounded unique minimizing pair')

manifest = obj(P/'OWNED_MANIFEST.json')
for entry in manifest['files']:
    path = P/entry['path']
    require(path.resolve().is_relative_to(P), 'owned packet path')
    check_binding(path, entry, 'owned packet '+entry['path'])
excluded = {'OWNED_MANIFEST.json', 'SEAL.json', 'CLOSURE.json'}
actual_owned = {str(x.relative_to(P)) for x in P.rglob('*') if x.is_file()}
require(actual_owned-excluded == {x['path'] for x in manifest['files']}, 'complete owned packet set')
if not preseal:
    seal = obj(P/'SEAL.json')
    require(digest(P/'OWNED_MANIFEST.json') == seal['OWNED_MANIFEST_SHA256'], 'final owned manifest seal')
    require(digest(P/'CLOSURE.json') == seal['CLOSURE_SHA256'], 'final closure seal')
    require(seal['SOURCE_READY_SHA256'] == digest(B/'sources/SOURCE_READY.json'), 'final source seal')
    require(seal['INITIAL_SEAL_SHA256'] == digest(P/'INITIAL_SEAL.json'), 'final independence seal')
    require(obj(P/'CLOSURE.json')['status'] == 'PASS', 'recorded closure PASS')
print(json.dumps({'status': 'PASS', 'mode': 'preseal' if preseal else 'sealed-read-only',
                  'source_files_unchanged': len(inputs['source_files']),
                  'ZIP_regular_payloads': zip_count, 'ZIP_expanded_bytes': zip_bytes,
                  'native_assets_authenticated': len(ready['all_assets_in_original_order']),
                  'initial_files_unchanged': len(obj(P/'INITIAL_MANIFEST.json')['files']),
                  'owned_files_authenticated': len(manifest['files']),
                  'fresh_actual_primary_PDFs_authenticated': len(obj(P/'PRIMARY_FETCH_RECEIPTS.json')),
                  'source_programs_executed_by_closure': 0, 'network_requests_by_closure': 0,
                  'files_written_by_closure': 0, 'mathematics_or_priority_proved_by_custody': False},
                 sort_keys=True))
