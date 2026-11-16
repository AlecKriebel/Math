#!/usr/bin/env python3
"""Finite standalone offline custody only. Default makes no writes, network,
subprocesses, project imports, scientific calculations or native checker calls.
--preseal checks the same finite payloads with existing exact root placeholders.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import stat
import sys
import zipfile
import zlib

A = Path(__file__).resolve().parent
S = A.parents[1]/'sources'
P = A.parents[3]
MATH = P.parent
TERMINALS = ['FINAL_CLOSURE.json','FINAL_MANIFEST.json','FINAL_SEAL.json']
COUNT = 0

def need(condition, message):
    global COUNT
    COUNT += 1
    if not condition:
        raise ValueError(message)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def literal(a, b, label):
    need(type(a) is type(b), label+': literal type')
    if isinstance(a, dict):
        need(list(a) == list(b), label+': exact key order/namespace')
        for key in a:
            literal(a[key], b[key], label+'/'+key)
    elif isinstance(a, list):
        need(len(a) == len(b), label+': list length')
        for i, pair in enumerate(zip(a,b)):
            literal(pair[0], pair[1], label+'/'+str(i))
    else:
        need(a == b, label+': literal value')

def path_in(value, root):
    path = Path(value)
    if not path.is_absolute():
        path = root/path
    need(path.is_relative_to(root) and path.resolve() == path and not path.is_symlink(), 'outside/symlink/nonliteral path')
    return path

def pin(row, root):
    path = path_in(row['path'], root)
    need(path.is_file() and stat.S_ISREG(path.stat().st_mode), 'regular file required')
    body = path.read_bytes()
    need(len(body) == row['bytes'] and sha(body) == row['SHA256'], 'whole file byte/SHA pin: '+str(path))
    return path

def inventory(root):
    files, dirs = [], []
    def walk(base):
        for entry in sorted(os.scandir(base),key=lambda x:x.name):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            need(not stat.S_ISLNK(mode), 'symlink rejected')
            if stat.S_ISDIR(mode):
                dirs.append(path.relative_to(root).as_posix())
                walk(path)
            else:
                need(stat.S_ISREG(mode), 'special file rejected')
                files.append(path.relative_to(root).as_posix())
    walk(root)
    return sorted(files),sorted(dirs)

def source():
    files, dirs = inventory(S)
    initial = load(A/'SOURCE_INPUT_MANIFEST.json')
    rows = initial['complete_source_files']
    need(len(files) == len(rows) == 128 and len(dirs) == 18, 'original128files18dirs')
    need(files == sorted(Path(r['path']).relative_to(S).as_posix() for r in rows), 'whole source file namespace')
    need(dirs == initial['exact_complete_source_directories'], 'whole source directory namespace')
    for row in rows:
        pin(row,S)
    need(sha((S/'SOURCE_READY_SEAL.json').read_bytes()) == '7327ed767e15386ae633b54ea6ba90152d87de7addbbf44136212af2b5ff5d36', 'source SEAL anchor')
    seal = load(S/'SOURCE_READY_SEAL.json')
    for name,key in [('SOURCE_READY.json','SOURCE_READY_SHA256'),('SOURCE_READY_MANIFEST.json','MANIFEST_SHA256'),('SOURCE_READY_CLOSURE.json','CLOSURE_SHA256')]:
        need(sha((S/name).read_bytes()) == seal[key], 'source terminal binding')
    need(seal['owned_payload_count'] == 125 and seal['actual_file_count'] == 128, '125plus3 qualification')
    objects = load(A/'NATIVE_LITERAL_BINDINGS.json')['objects']
    for row in objects:
        path = pin(row['original_file'],S)
        obj = load(path) if row['parse_mode'] == 'JSON' else [json.loads(line) for line in path.read_text().splitlines() if line]
        literal(obj,row['whole_original_typed_object'],'whole original '+str(path.relative_to(S)))
    ready, record = load(S/'SOURCE_READY.json'),load(S/'record.response.body')
    literal(ready['version'],'1.0','native version')
    literal(ready['version_field_present'],True,'native version presence')
    literal(ready['current_native_sheet_identity_subset'],None,'historical current Sheet unobserved')
    for key in ['printed_title_date_version_inspected','target_PDF_rasters_visually_read','mathematical_PDF_TeX_or_pixels_read','TeX_preamble_or_mathematical_body_read']:
        literal(ready[key],False,'historical source '+key)
    literal(ready['printed_date'],None,'historical printed date')
    literal(ready['printed_version'],None,'historical printed version')
    literal(ready['source_programmes_executed'],[],'historical source execution list')
    need(record['id'] == 23130727 and record['status'] == 'published', 'published native identity')
    literal(record['metadata']['license'],{'id':'cc-by-4.0'},'whole original license')
    need(record['metadata']['publication_date'] == '2026-10-03', 'native original publication date')
    assets = ready['all_native_assets_in_original_order']
    need([r['original_api_file_object']['key'] for r in assets] == ['alternating-antimorphic-verification.zip','alternating-antimorphic-fine-wilf.pdf'], 'literal ZIP/PDF order')
    for i,row in enumerate(assets):
        literal(row['original_api_file_object'],record['files'][i],'whole native asset object')
        body = pin(row,S).read_bytes()
        need(body == path_in(row['transport_body_path'],S).read_bytes(),'native asset/response whole equality')
        kind,value = row['original_api_file_object']['checksum'].split(':',1)
        need(kind == 'md5' and hashlib.md5(body).hexdigest() == value,'native checksum')
    for t in load(S/'ALL_TRANSPORT_RECEIPTS.json'):
        body = path_in(t['body_path'],S).read_bytes()
        need(len(body) == t['bytes'] and sha(body) == t['SHA256'],'native whole transport body')
    arc = load(S/'ARCHIVE_CUSTODY.json')
    need(arc['top_level_archive_count'] == 1 and arc['nested_archive_count'] == 0,'one native nonnested ZIP')
    observed = []
    for container in arc['containers']:
        archive = path_in(container['input_path'],S)
        need(sha(archive.read_bytes()) == container['input_SHA256'],'whole ZIP SHA')
        with zipfile.ZipFile(archive) as z:
            need(z.comment.hex() == container['original_archive_comment_hex'],'whole ZIP comment')
            infos = z.infolist()
            need(len(infos) == len(container['members']) == len(container['whole_original_central_directory']),'complete ordered central list')
            names = set()
            for i,(info,member,central) in enumerate(zip(infos,container['members'],container['whole_original_central_directory'])):
                name = info.filename
                parts = PurePosixPath(name)
                need(not parts.is_absolute() and '..' not in parts.parts and '\\' not in name and '\x00' not in name,'unsafe ZIP path')
                need(name.casefold() not in names,'duplicate/case collision')
                names.add(name.casefold())
                need(not info.is_dir() and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG) and not info.flag_bits&1,'only unencrypted regular native members')
                actual = {'ordinal_zero_based':i,'filename':name,'original_filename':info.orig_filename,'is_directory':info.is_dir(),
                    'bytes':info.file_size,'compressed_bytes':info.compress_size,'CRC32':format(info.CRC,'08x'),'flags':info.flag_bits,
                    'compression':info.compress_type,'native_date_time':list(info.date_time),'external_attr':info.external_attr,
                    'internal_attr':info.internal_attr,'create_system':info.create_system,'create_version':info.create_version,
                    'extract_version':info.extract_version,'header_offset':info.header_offset,'extra_hex':info.extra.hex(),'comment_hex':info.comment.hex()}
                literal(actual,central,'whole actual central object')
                need(name == member['original_member_name'] and i == member['ordinal_zero_based'],'archive member identity/order')
                body = z.read(info)
                need(len(body) == member['bytes'] == info.file_size and sha(body) == member['SHA256'],'whole regular payload')
                need(zlib.crc32(body)&0xffffffff == info.CRC and format(info.CRC,'08x') == member['CRC32'],'whole CRC')
                extracted = path_in(member['extracted_path'],S)
                need(extracted == path_in(container['extraction_root'],S)/name and extracted.read_bytes() == body,'whole archive/extracted equality')
                observed.append(member)
    literal(observed,arc['regular_payload_occurrences'],'all ordered regular occurrences')
    need(len(observed) == 69,'all69 regular native occurrences')
    return len(objects)

def references_and_core():
    core = load(A/'CORE_BINDINGS.json')
    contract = pin(core['whole_root_contract_binding'],P)
    need(sha(contract.read_bytes()) == '0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104','neutral qualified core anchor')
    literal(load(contract),core['whole_original_root_contract'],'whole qualified core object')
    need(len(core['actual_byreference_core_files']) == 18,'17originals plus sole405b')
    for row in core['actual_byreference_core_files']:
        pin(row,P)
    checkpoint = [r for r in core['actual_byreference_core_files'] if Path(r['path']).name == 'checkpoint_subtree.py']
    need(len(checkpoint) == 1 and checkpoint[0]['bytes'] == 6213 and checkpoint[0]['SHA256'] == '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0','sole405b qualification')
    need(core['generated_caches_opaque_no_immutability_claim'] is True,'opaque cache qualification')
    for name,anchor in [('INITIAL_SEAL.json','fdc72cc386c1024956de533e3de5b0247de96ec9e129c3d722f584407bc51365'),('OWN_PROOF_CONTROL_SEAL.json','e6de783d93556cfb08579f69338a0a85983a4c0f1d0a9ac9d74c40965b6d5fac'),('PRIMARY_PROOF_SEAL.json','3d33f32ba107f3800ab48720603b3fca5df5a431caff983e0b1c5ce41a64cde6')]:
        need(sha((A/name).read_bytes()) == anchor,'immutable early seal')
        manifest = load(pin(load(A/name)['manifest'],A))
        for row in manifest.get('files',manifest.get('payloads',[])):
            pin(row,A)
    handoff = load(A/'RAW_PRIMARY_HANDOFF_01.json')
    need(sha((A/'RAW_PRIMARY_HANDOFF_01.json').read_bytes()) == 'e3b46063528a9c35332c72ba061b12c20801b632cb8a408da3b98d4597817c3d','raw handoff anchor')
    literal(load(pin(handoff['root_authority'],P)),handoff['whole_root_authority'],'whole root primary GO')
    need(handoff['new_GETs'] == 0 and handoff['old_raw_corpora_copied'] is False and len(handoff['records']) == 6,'zero fresh acquisition/six byreference raw bodies')
    for row in handoff['records']:
        body = pin(row['whole_original_raw_body'],MATH)
        if 'legacy_transport_metadata_container' in row:
            container = pin(row['legacy_transport_metadata_container'],MATH)
            records = [json.loads(line) for line in container.read_text().splitlines() if line]
            selected = [r for r in records if Path(r.get('file',r.get('path',''))).name == body.name]
            literal(selected,row['whole_original_selected_legacy_transport_objects_in_recorded_order'],'whole literal legacy transport metadata; absent fields not filled')
        else:
            literal(load(pin(row['legacy_metadata_container'],MATH)),row['whole_original_legacy_metadata_object'],'whole literal legacy identity metadata')

def main():
    need(sys.argv[1:] in ([],['--preseal']),'only pure default or explicit preseal')
    files,dirs = inventory(A)
    for name in TERMINALS:
        need(name in files,'all three exact root controls already ordinary files')
    manifest = load(A/'FINAL_MANIFEST.json')
    literal(manifest['exact_root_terminal_exclusions'],TERMINALS,'exact root-only terminal exclusions')
    need(dirs == manifest['directories'],'whole finite directory namespace including ignored directories')
    payloads = sorted(n for n in files if n not in TERMINALS)
    need(payloads == [r['path'] for r in manifest['files']],'whole finite file namespace; no basename/cache/future carveouts')
    for row in manifest['files']:
        pin(row,A)
    objects = source()
    references_and_core()
    verdict = load(A/'VERDICT.json')
    need(verdict['followup'] is None and verdict['publication_authority'] is False and verdict['canonical_url'] is None and verdict['AA'] is None,'no followup/production/canonical/AA authority')
    if not sys.argv[1:]:
        seal = load(A/'FINAL_SEAL.json')
        need(seal['status'] == 'FINAL_SEALED','immutable final required on default')
        need(sha((A/'FINAL_MANIFEST.json').read_bytes()) == seal['MANIFEST_SHA256'] and sha((A/'FINAL_CLOSURE.json').read_bytes()) == seal['CLOSURE_SHA256'],'final exact terminal whole hashes')
        need(seal['owned_payload_count'] == len(payloads) and seal['actual_file_count'] == len(files) and seal['owned_directory_count'] == len(dirs),'exact final extent')
    print(json.dumps({'status':'PASS_CUSTODY_PRESEAL' if sys.argv[1:] else 'PASS_CUSTODY_FINAL','custody_predicates':COUNT,
        'owned_payloads':len(payloads),'actual_owned_files':len(files),'owned_directories':len(dirs),
        'original_source_files':128,'original_source_directories':18,'whole_ZIP_regular_occurrences':69,
        'whole_typed_source_objects':objects,'external_raw_bodies_byreference':6,'fresh_primary_GETs':0,
        'qualified_original_core_files':17,'sole_authorized405b':True,'network_subprocess_writes_scientific_execution':False,'scientific_findings_emitted':False}))

if __name__ == '__main__':
    main()
