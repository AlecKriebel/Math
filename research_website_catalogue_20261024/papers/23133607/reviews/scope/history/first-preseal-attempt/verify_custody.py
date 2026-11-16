#!/usr/bin/env python3
"""Standalone finite read-only custody closure, with no scientific execution.

Default: authenticate the exact final namespace, original source, literal typed
objects, archives, core references and raw HTTP receipts. No project imports,
network, subprocesses, writes, or mathematical checker invocation. Explicit
--preseal checks existing exact terminal placeholders before the final seal.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import stat
import sys
import zipfile
import zlib
from urllib.parse import urlsplit, urljoin

A = Path(__file__).resolve().parent
S = A.parents[1] / 'sources'
TERMINALS = ['FINAL_CLOSURE.json', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json']
COUNT = 0

def need(condition, message):
    global COUNT
    COUNT += 1
    if not condition:
        raise ValueError(message)

def digest(body):
    return hashlib.sha256(body).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def literal(left, right, label):
    need(type(left) is type(right), label + ': literal JSON type changed')
    if isinstance(left, dict):
        need(list(left) == list(right), label + ': key order or namespace changed')
        for key in left:
            literal(left[key], right[key], label + '/' + key)
    elif isinstance(left, list):
        need(len(left) == len(right), label + ': list length changed')
        for i, pair in enumerate(zip(left, right)):
            literal(pair[0], pair[1], label + '/' + str(i))
    else:
        need(left == right, label + ': literal value changed')

def inside(path, root):
    p = Path(path)
    if not p.is_absolute():
        p = root / p
    need(p.is_relative_to(root), 'reference outside authorized root: ' + str(p))
    need(p.resolve() == p and not p.is_symlink(), 'nonliteral or symlink path: ' + str(p))
    return p

def pin(row, root):
    p = inside(row['path'], root)
    need(p.is_file() and stat.S_ISREG(p.stat().st_mode), 'not regular: ' + str(p))
    b = p.read_bytes()
    need(len(b) == row['bytes'], 'byte count: ' + str(p))
    need(digest(b) == row['SHA256'], 'SHA256: ' + str(p))
    return p

def inventory(root):
    files = []
    dirs = []
    def walk(path):
        for entry in sorted(os.scandir(path), key=lambda e: e.name):
            p = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            need(not stat.S_ISLNK(mode), 'symlink rejected: ' + str(p))
            if stat.S_ISDIR(mode):
                dirs.append(p.relative_to(root).as_posix())
                walk(p)
            else:
                need(stat.S_ISREG(mode), 'nonregular rejected: ' + str(p))
                files.append(p.relative_to(root).as_posix())
    walk(root)
    return sorted(files), sorted(dirs)

def verify_source():
    binding = load(A / 'SOURCE_INPUT_MANIFEST.json')
    files, dirs = inventory(S)
    rows = binding['complete_source_files']
    need(len(rows) == 97 and len(files) == 97, 'full original97 source files required')
    need(dirs == sorted(binding['exact_complete_source_directories']) and len(dirs) == 9, 'source9 directory namespace')
    need(files == sorted(Path(r['path']).relative_to(S).as_posix() for r in rows), 'source complete file namespace')
    for row in rows:
        pin(row, S)
    seal = load(S / 'SOURCE_READY_SEAL.json')
    ready = load(S / 'SOURCE_READY.json')
    need(digest((S/'SOURCE_READY.json').read_bytes()) == '34854844ee902600ec563d89501d3878fa303915e9ac1442929feaffef7ec816', 'READY anchor')
    need(digest((S/'SOURCE_READY_SEAL.json').read_bytes()) == 'e3175bda643f60efb02575f4bbdefd0f67a5ea89c85a5b7d055d92b80447f012', 'source SEAL anchor')
    for name, field in [('SOURCE_READY.json','SOURCE_READY_SHA256'), ('SOURCE_READY_MANIFEST.json','MANIFEST_SHA256'), ('SOURCE_READY_CLOSURE.json','CLOSURE_SHA256')]:
        need(digest((S/name).read_bytes()) == seal[field], 'source terminal binding: ' + name)
    need(seal['owned_payload_count'] == 94 and seal['actual_file_count'] == 97, 'source94+3 count qualification')
    literal(ready['version'], '1.0', 'native version literal')
    literal(ready['version_field_present'], True, 'native version presence')
    for name in ['printed_title_date_version_inspected', 'target_PDF_rasters_visually_read', 'mathematical_PDF_TeX_or_pixels_read', 'TeX_preamble_or_mathematical_body_read']:
        literal(ready[name], False, 'source historical ' + name)
    literal(ready['printed_date'], None, 'source historical printed date')
    literal(ready['printed_version'], None, 'source historical printed version')
    literal(ready['source_programmes_executed'], [], 'source historical programme list')
    objects = load(A / 'NATIVE_LITERAL_BINDINGS.json')['objects']
    for row in objects:
        p = pin(row['original_file'], S)
        literal(load(p), row['whole_original_typed_object'], 'whole original object ' + str(p.relative_to(S)))
    record = load(S/'record.response.body')
    need(record['id'] == 23133607 and record['status'] == 'published', 'original published record identity')
    literal(record['metadata']['license'], {'id':'cc-by-4.0'}, 'native whole license')
    need(record['metadata']['publication_date'] == '2026-10-04', 'native original publication date')
    assets = ready['all_native_assets_in_original_order']
    need([r['original_api_file_object']['key'] for r in assets] == ['qss-self-duality-note.pdf','qss-self-duality-verification.zip'], 'literal PDF then ZIP order')
    for i, asset in enumerate(assets):
        literal(asset['original_api_file_object'], record['files'][i], 'whole ordered native file object')
        p = pin(asset, S)
        body = p.read_bytes()
        need(body == Path(asset['transport_body_path']).read_bytes(), 'asset whole transport-body equality')
        scheme, checksum = asset['original_api_file_object']['checksum'].split(':',1)
        need(scheme == 'md5' and hashlib.md5(body).hexdigest() == checksum, 'normal native checksum')
    for transport in load(S/'ALL_TRANSPORT_RECEIPTS.json'):
        p = inside(transport['body_path'], S)
        body = p.read_bytes()
        need(len(body) == transport['bytes'] and digest(body) == transport['SHA256'], 'whole original native transport body')
    arc = load(S/'ARCHIVE_CUSTODY.json')
    need(arc['top_level_archive_count'] == 1 and arc['nested_archive_count'] == 0, 'actual one nonnested ZIP')
    need(len(arc['regular_payload_occurrences']) == 33, 'all33 ZIP occurrences')
    observed = []
    for container in arc['containers']:
        archive = inside(container['input_path'], S)
        need(digest(archive.read_bytes()) == container['input_SHA256'], 'whole native ZIP')
        root = inside(container['extraction_root'], S)
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            need(len(infos) == len(container['members']), 'complete native ZIP central list')
            names = set()
            for i, pair in enumerate(zip(infos, container['members'])):
                info, member = pair
                name = info.filename
                parts = PurePosixPath(name)
                need(not parts.is_absolute() and '..' not in parts.parts and '\\' not in name and '\x00' not in name, 'unsafe ZIP name')
                need(name.casefold() not in names, 'ZIP duplicate/case collision')
                names.add(name.casefold())
                mode = info.external_attr >> 16
                need(stat.S_IFMT(mode) in (0,stat.S_IFREG) and not info.is_dir() and not info.flag_bits & 1, 'nonregular/encrypted ZIP occurrence')
                literal(name, member['original_member_name'], 'native ZIP name/order')
                need(member['ordinal_zero_based'] == i, 'native central ordinal')
                for actual, key in [(info.file_size,'bytes'), (info.compress_size,'compressed_bytes'), (info.compress_type,'compression_method'), (info.external_attr,'native_external_attr'), (info.create_system,'native_create_system'), (info.flag_bits,'native_flags')]:
                    literal(actual, member[key], 'native central field ' + key)
                literal(list(info.date_time), member['native_date_time'], 'native central timestamp')
                need(format(info.CRC,'08x') == member['CRC32'], 'native central CRC')
                body = z.read(info)
                need(len(body) == info.file_size and zlib.crc32(body) & 0xffffffff == info.CRC, 'whole CRC/size read')
                need(digest(body) == member['SHA256'], 'whole ZIP payload SHA')
                extracted = inside(member['extracted_path'], S)
                need(extracted == root/name and extracted.read_bytes() == body, 'whole native ZIP/extracted equality')
                observed.append(member)
    literal(observed, arc['regular_payload_occurrences'], 'whole ordered archive occurrences')
    return len(files), len(dirs), len(observed), len(objects)

def verify_core():
    core = load(A/'CORE_BINDINGS.json')
    project = A.parents[3]
    p = pin(core['whole_root_contract_binding'], project)
    literal(load(p), core['whole_original_root_contract'], 'whole qualified core contract')
    rows = core['actual_byreference_core_files']
    need(len(rows) == 18, 'qualified17 original plus one authorized checkpoint')
    for row in rows:
        pin(row, project)
    checkpoints = [r for r in rows if Path(r['path']).name == 'checkpoint_subtree.py']
    need(len(checkpoints) == 1 and checkpoints[0]['bytes'] == 6213 and checkpoints[0]['SHA256'] == '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0', 'sole authorized405b checkpoint')
    need(core['generated_caches_opaque_no_immutability_claim'] is True, 'cache qualification')

def verify_early_freezes():
    specs = [('INITIAL_SEAL.json','92959fdf51fa0d58b9b782d00d9a38ab12ec7c3a106902d05210bd40712ec73b','INITIAL_MANIFEST.json','files'),
             ('OWN_PROOF_CONTROL_SEAL.json','c734a8a17fcee7452fef17cb62ccd8e35bff81f97eff7dd16c0fe036465eeecd','OWN_PROOF_CONTROL_MANIFEST.json','files'),
             ('PRIMARY_PROOF_SEAL.json','8f99749866e048aec957810a6d11cd5fcc43970d44a06fa82731917d10ced620','PRIMARY_PROOF_MANIFEST.json','payloads')]
    for sealname, anchor, manifestname, field in specs:
        need(digest((A/sealname).read_bytes()) == anchor, 'immutable earlier seal: ' + sealname)
        pin(load(A/sealname)['manifest'], A)
        for row in load(A/manifestname)[field]:
            pin(row, A)

def verify_primary():
    handoff = load(A/'RAW_PRIMARY_HANDOFF_01.json')
    need(digest((A/'RAW_PRIMARY_HANDOFF_01.json').read_bytes()) == '3ec453a4ed2cdfac4d71d7e516bac73e4b24a9037cab69ec614910a18c401b10', 'raw handoff anchor')
    authority = pin(handoff['root_authority'], A.parents[3])
    need(digest(authority.read_bytes()) == 'f2df5de1ee52b02569585806e2c4725e2708c129ce6bc7be640268f05776874c', 'root primary GO anchor')
    hops = 0
    for acquisition in handoff['fresh_actual_acquisitions']:
        need(acquisition['process_exit'] == 0, 'actual acquisition exit')
        pin(acquisition['stdout_file'], A)
        need(pin(acquisition['stderr_file'], A).read_bytes() == b'', 'acquisition exact empty stderr')
        previous = None
        for row in acquisition['actual_hops_in_order']:
            p = pin(row['transport_file'], A)
            transport = load(p)
            literal(transport, row['whole_literal_transport'], 'whole actual primary transport')
            body = pin(row['body_file'], A).read_bytes()
            request = pin(row['actual_request_file'], A).read_bytes()
            need(len(body) == transport['bytes'] and digest(body) == transport['SHA256'], 'primary whole body')
            need(transport['body_complete'] is True and transport['error'] is None, 'complete primary response')
            need(transport['response_obtained'] is True, 'actual response')
            need(transport['authentication_cookies_proxy_retry_or_bypass'] is False, 'ordinary primary acquisition')
            parsed = urlsplit(transport['URL'])
            target = parsed.path or '/'
            if parsed.query:
                target += '?' + parsed.query
            expected = ('GET ' + target + ' HTTP/1.1\r\n' + ''.join(k+': '+v+'\r\n' for k,v in transport['actual_request_headers_in_sent_order']) + '\r\n').encode('ascii')
            need(request == expected, 'exact actual sent request bytes/header order')
            if previous is not None:
                locations = [v for k,v in previous['response_headers_in_received_order'] if k.lower() == 'location']
                need(previous['HTTP_status'] in (301,302,303,307,308) and len(locations) == 1, 'actual redirect location')
                need(transport['URL'] == urljoin(previous['URL'], locations[0]), 'follow actual Location only')
            previous = transport
            hops += 1
    need(hops == 9, 'all nine actual primary HTTP hops')
    return hops

def main():
    need(sys.argv[1:] in ([], ['--preseal']), 'only default read-only final closure or explicit --preseal')
    preseal = sys.argv[1:] == ['--preseal']
    files, dirs = inventory(A)
    for name in TERMINALS:
        need(name in files and stat.S_ISREG((A/name).stat().st_mode), 'existing exact root terminal required')
    manifest = load(A/'FINAL_MANIFEST.json')
    literal(manifest['exact_root_terminal_exclusions'], TERMINALS, 'only exact root terminal exclusions')
    need(dirs == manifest['directories'], 'complete owned directory namespace')
    actual = sorted(n for n in files if n not in TERMINALS)
    need(actual == [r['path'] for r in manifest['files']], 'complete owned finite file namespace; no basename/cache/future exclusions')
    for row in manifest['files']:
        pin(row, A)
    sourcefiles, sourcedirs, zipcount, objectcount = verify_source()
    verify_core()
    verify_early_freezes()
    hops = verify_primary()
    verdict = load(A/'VERDICT.json')
    need(verdict['publication_authority'] is False and verdict['canonical_url'] is None and verdict['AA'] is None and verdict['followup'] is None, 'no publication/canonical/AA/followup authority')
    if not preseal:
        seal = load(A/'FINAL_SEAL.json')
        need(seal['status'] == 'FINAL_SEALED', 'final seal required on default')
        need(digest((A/'FINAL_MANIFEST.json').read_bytes()) == seal['MANIFEST_SHA256'], 'final manifest whole SHA')
        need(digest((A/'FINAL_CLOSURE.json').read_bytes()) == seal['CLOSURE_SHA256'], 'final closure whole SHA')
        need(seal['actual_file_count'] == len(files) and seal['owned_payload_count'] == len(actual) and seal['owned_directory_count'] == len(dirs), 'exact final namespace extent')
    print(json.dumps({'status':'PASS_CUSTODY_PRESEAL' if preseal else 'PASS_CUSTODY_FINAL', 'custody_predicates':COUNT,
                      'owned_payloads':len(actual), 'actual_owned_files':len(files), 'owned_directories':len(dirs),
                      'original_source_files':sourcefiles, 'original_source_directories':sourcedirs,
                      'whole_ZIP_regular_occurrences':zipcount, 'whole_typed_objects':objectcount,
                      'actual_primary_HTTP_hops':hops, 'qualified_original_core_files':17,
                      'authorized_checkpoint_405b':True, 'network_subprocess_writes_scientific_execution':False,
                      'scientific_findings_emitted':False}, sort_keys=False))

if __name__ == '__main__':
    main()
