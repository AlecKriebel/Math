"""Evidence closure only: python3 -E -B VERIFY_READ_ONLY.py [--preseal].

No writes, network, source program execution, builder, finalizer or Git action.
The custody checks below do not establish mathematics or worldwide priority.
"""
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import unicodedata
import zipfile


def need(value, label):
    if not value:
        raise RuntimeError(label)


need(sys.flags.ignore_environment and sys.dont_write_bytecode, 'use python3 -E -B')
need(sys.argv[1:] in ([], ['--preseal']), 'supported arguments')
preseal = sys.argv[1:] == ['--preseal']
P = Path(__file__).resolve().parent
B = P.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def bind(path, entry, label):
    need(path.is_file() and not path.is_symlink(), label+' regular file')
    need(path.stat().st_size == entry['bytes'], label+' size')
    need(sha(path) == entry.get('SHA256', entry.get('sha256')), label+' SHA256')


ready_path = B/'sources/SOURCE_READY.json'
ready_hash = '1f728d52dd3bb791833a837fb3bae7eab1b3a37ce7ecd9c4655b94f4d693cf46'
need(sha(ready_path) == ready_hash, 'exact frozen source READY')
ready = load(ready_path)
inputs = load(P/'INPUT_MANIFEST.json')
for entry in inputs['source_files']:
    path = B/entry['path']
    need(path.resolve().is_relative_to(B/'sources'), 'native source path containment')
    bind(path, entry, 'native source '+entry['path'])
actual_source_set = {str(x.relative_to(B)) for x in (B/'sources').rglob('*') if x.is_file()}
need(actual_source_set == {x['path'] for x in inputs['source_files']}, 'complete frozen source set')
for entry in ready['all_native_assets_in_original_order']:
    path = Path(entry['path'])
    need(path.resolve().is_relative_to(B/'sources'), 'native original path')
    bind(path, entry, 'native original')
    need(hashlib.md5(path.read_bytes()).hexdigest() == entry['MD5'], 'native original MD5')
    need(entry['original_api_file_object']['checksum'] == 'md5:'+entry['MD5'], 'actual API checksum')
need(ready['selected_actual_PDF']['pages'] == 13, 'frozen reader page count')
bind(Path(ready['selected_actual_PDF']['path']), ready['selected_actual_PDF'], 'actual native reader')
bind(Path(ready['controlling_TeX']['path']), ready['controlling_TeX'], 'controlling TeX')

zip_asset = next(x for x in ready['all_native_assets_in_original_order'] if x['path'].endswith('.zip'))
count = 0
expanded = 0
seen = set()
extracted_root = B/'sources/cache/extracted/container-001'
with zipfile.ZipFile(zip_asset['path']) as archive:
    for info in archive.infolist():
        name = info.filename
        parts = PurePosixPath(name).parts
        need(parts and not name.startswith('/') and '\\' not in name and ':' not in name
             and all(x not in ('', '.', '..') for x in parts), 'safe native ZIP name')
        need(not info.is_dir() and not(info.flag_bits & 1), 'regular unencrypted native payload')
        need(stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG), 'no link/device payload')
        key = unicodedata.normalize('NFC', name).casefold()
        need(key not in seen, 'no normalized native collision')
        seen.add(key)
        payload = archive.read(info)  # The full read validates actual CRC.
        need(len(payload) == info.file_size, 'complete native member')
        target = extracted_root/name
        need(target.resolve().is_relative_to(extracted_root), 'native extraction path')
        need(target.read_bytes() == payload, 'actual whole native payload/extraction equality')
        count += 1
        expanded += len(payload)
need(count == 194 and expanded == 1866967, 'whole published support archive')

initial_hash = 'e2e5e93862a1abe851d080651203ae454ddeb9eb449c5b16f82d8becc7307194'
need(sha(P/'INITIAL_SEAL.json') == initial_hash, 'independent early seal')
initial = load(P/'INITIAL_SEAL.json')
need(sha(P/'INITIAL_MANIFEST.json') == initial['INITIAL_MANIFEST_SHA256'], 'early manifest binding')
need(sha(P/'INITIAL_RECONSTRUCTION.md') == initial['INITIAL_RECONSTRUCTION_SHA256'], 'early substantive reconstruction')
for entry in load(P/'INITIAL_MANIFEST.json')['files']:
    path = Path(entry['path'])
    need(path.resolve().is_relative_to(P), 'early owned path')
    bind(path, entry, 'unchanged early owned file')

external_inputs = load(P/'PRIMARY_INPUTS.json')['primary_input_files']
external_inputs += load(P/'PRIMARY_INPUTS_02.json')['raw_primary_files']
raw_root = B/'reviews/scope/cache/primary'
for entry in external_inputs:
    path = Path(entry['path'])
    need(path.resolve().is_relative_to(raw_root), 'only expressly authorized raw primary inputs')
    bind(path, entry, 'actual external primary bytes')
need(gzip.decompress((raw_root/'HM-K39.ps.gz').read_bytes()) == (raw_root/'HM-K39.ps').read_bytes(),
     'original primary gzip/PS equality')

receipts = load(P/'EXECUTION_RECEIPTS.json')
need(len(receipts) == 3, 'three bounded execution receipts')
for receipt in receipts:
    need(receipt['exit_code'] == 0 and receipt['outcome'] in ('PASS', True), 'bounded execution result')
    need(sha(Path(receipt['command'][-1])) == receipt['script_SHA256'], 'actual executed script identity')
    need(sha(P/receipt['stdout_path']) == receipt['stdout_SHA256'], 'complete actual stdout')
    need(sha(P/receipt['stderr_path']) == receipt['stderr_SHA256'], 'complete actual stderr')
    need((P/receipt['stderr_path']).stat().st_size == 0, 'normal stderr empty')
original_two = B/'sources/cache/extracted/container-001/reviews/degree_two_01/checks/check_degree_two.py'
copy_two = P/'reproduction/degree_two/check_degree_two.py'
need(original_two.read_bytes() == copy_two.read_bytes(), 'deposited degree-two copy byte identity')
need((P/'reproduction/degree_two/CHECK_RESULT.json').read_bytes() == (P/'source-degree-two.stdout.json').read_bytes(),
     'degree-two output confined to owned copy')
seven = load(P/'source-degree-seven.stdout.json')
need(seven['all_checks_pass'] and seven['term_count'] == 128
     and seven['direct_16_by_16_adjoint_value'] == 6
     and seven['reversed_direct_adjoint_value'] == -6, 'retained bounded wheel result')
own = load(P/'own-exact-controls.stdout.json')
need(own['status'] == 'PASS' and len(own['complete_quadratic_longitude_matrix_certificates']) == 27,
     'retained independent exact-control identity')

owned = load(P/'OWNED_MANIFEST.json')
for entry in owned['files']:
    path = P/entry['path']
    need(path.resolve().is_relative_to(P), 'owned packet containment')
    bind(path, entry, 'owned packet '+entry['path'])
excluded = {'OWNED_MANIFEST.json', 'CLOSURE.json', 'SEAL.json'}
actual_owned_set = {str(x.relative_to(P)) for x in P.rglob('*') if x.is_file()}
need(actual_owned_set-excluded == {x['path'] for x in owned['files']}, 'complete owned packet set')
if not preseal:
    seal = load(P/'SEAL.json')
    need(sha(P/'OWNED_MANIFEST.json') == seal['OWNED_MANIFEST_SHA256'], 'terminal owned manifest')
    need(sha(P/'CLOSURE.json') == seal['CLOSURE_SHA256'], 'terminal closure')
    need(seal['SOURCE_READY_SHA256'] == ready_hash and seal['INITIAL_SEAL_SHA256'] == initial_hash,
         'terminal source and independence seals')
    need(load(P/'CLOSURE.json')['status'] == 'PASS', 'recorded final closure')
print(json.dumps({'status': 'PASS', 'mode': 'preseal' if preseal else 'sealed-read-only',
                  'source_files_unchanged': len(inputs['source_files']),
                  'original_native_assets_authenticated': len(ready['all_native_assets_in_original_order']),
                  'whole_native_ZIP_payloads': count, 'expanded_native_ZIP_bytes': expanded,
                  'initial_files_unchanged': len(load(P/'INITIAL_MANIFEST.json')['files']),
                  'external_raw_primary_files_authenticated': len(external_inputs),
                  'owned_files_authenticated': len(owned['files']),
                  'source_programs_executed_by_closure': 0, 'network_requests_by_closure': 0,
                  'files_written_by_closure': 0, 'mathematics_or_priority_proved_by_custody': False},
                 sort_keys=True))
