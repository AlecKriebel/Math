#!/usr/bin/env python3
"""Metadata/opaque-byte custody only. No scientific body decoding or replay."""
from pathlib import Path
import hashlib
import json
import stat
import zipfile
import zlib

OWN = Path(__file__).resolve().parent
PARENT = OWN.parent
SOURCE = PARENT.parent.parent/'sources'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def data(p):
    return json.loads(p.read_text())


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def strict(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(strict(a[k],b[k]) for k in a)
    if isinstance(a,list):
        return len(a) == len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a == b


def bytes_check(p, row):
    require(p.is_file() and not p.is_symlink(), 'Missing/nonregular file: '+str(p))
    require(p.stat().st_size == row['bytes'] and sha(p) == row['SHA256'], 'Byte mismatch: '+str(p))


authority = data(OWN/'AUTHORITY_BINDINGS.json')
for row in authority['metadata_only_authorities']:
    original, copy = Path(row['original_path']), OWN/row['copy']
    bytes_check(original,row);bytes_check(copy,row)
    require(original.read_bytes() == copy.read_bytes(), 'Authority copy changed')
manifest = data(PARENT/'INPUT_MANIFEST.json')
custody = data(PARENT/'SOURCE_CUSTODY.json')
rows = manifest['whole_source_directory']
require(len(rows) == 81, 'Source count mismatch')
actual = {str(f) for f in SOURCE.rglob('*') if f.is_file()}
require(actual == {r['path'] for r in rows}, 'Whole source file namespace changed')
for row in rows:
    bytes_check(Path(row['path']),row)
copies = custody['literal_native_copies']
require(len(copies) == 21, 'Native copy count mismatch')
for row in copies:
    original, copy = Path(row['original_path']), PARENT/row['copy_path']
    bytes_check(original,row);bytes_check(copy,row)
    require(original.read_bytes() == copy.read_bytes(), 'Native literal byte copy mismatch')

ready = data(SOURCE/'SOURCE_READY.json')
archive = data(SOURCE/'ARCHIVE_CUSTODY.json')
transports = data(SOURCE/'ALL_TRANSPORT_RECEIPTS.json')
schema = data(SOURCE/'NATIVE_SCHEMA_TYPES.json')
require(strict(custody['whole_original_source_ready_object'],ready),'Whole SOURCE_READY type/order/value mismatch')
require(strict(custody['whole_original_archive_custody_object'],archive),'Whole archive custody mismatch')
require(strict(custody['all_actual_transport_receipts_whole'],transports),'Whole transport order/type/value mismatch')
require(strict(custody['whole_native_schema_types'],schema),'Whole schema inventory mismatch')
for key in ['native_schema_types','actual_transport_receipts']:
    descriptor = ready[key]
    bytes_check(Path(descriptor['path']),descriptor)
apis = custody['whole_actual_native_API_objects']
require(len(apis) == 4 and len(transports) == 7, 'API/transport counts mismatch')
require(strict([x['original_custody_object'] for x in apis],ready['whole_native_API_objects']),'API custody descriptor mismatch')
schema_fresh = []
def walk(role, obj, pointer=''):
    row = {'role':role,'JSON_pointer':pointer,'original_type':type(obj).__name__}
    if obj is None or (isinstance(obj,(dict,list)) and len(obj)==0):
        row['original_empty_or_null_value'] = obj
    schema_fresh.append(row)
    if isinstance(obj,dict):
        for k,v in obj.items():
            walk(role,v,pointer+'/'+k.replace('~','~0').replace('/','~1'))
    elif isinstance(obj,list):
        for k,v in enumerate(obj):
            walk(role,v,pointer+'/'+str(k))
for row in apis:
    descriptor = row['original_custody_object'];f = Path(descriptor['path'])
    bytes_check(f,descriptor)
    raw = data(f)
    require(strict(row['whole_original_object'],raw),'Whole API type/key/list-order mismatch')
    walk(descriptor['role'],raw)
require(strict(schema_fresh,schema) and len(schema_fresh)==499, 'Reconstructed native schema inventory mismatch')
record,latest,versions,files = [x['whole_original_object'] for x in apis]
require(type(record['swh']) is dict and record['swh']=={} and type(latest['swh']) is dict and latest['swh']=={}, 'Native empty object distinction lost')
require(versions['hits']['hits'][0]['swh'] is None, 'Native null distinction lost')
require(type(files['entries']) is list and type(files['order']) is list and files['order']==[] and files['default_preview'] is None, 'Native file schema distinction lost')
for receipt in transports:
    bytes_check(Path(receipt['body_path']),receipt)
    transport_path = Path(receipt['body_path']+'.transport.json')
    require(strict(data(transport_path),receipt), 'Individual receipt differs from aggregate')
    require(type(receipt['response_headers_in_received_order']) is list, 'Ordered headers flattened')
duplicate_header_receipts = sum(len([x for x in r['response_headers_in_received_order'] if x[0].lower()=='content-type'])>1 for r in transports)
require(duplicate_header_receipts == 2, 'Native duplicate header distinction changed')

containers = archive['containers']
require(len(containers)==1 and archive['nested_archive_count']==0,'Archive container count mismatch')
member_rows = archive['regular_payload_occurrences']
require(len(member_rows)==29 and len(custody['all_original_members_checked'])==29,'Member count mismatch')
require(strict([x['whole_original_member_object'] for x in custody['all_original_members_checked']],member_rows),'Parent member objects differ from originals')
checked = 0
for container in containers:
    zpath = Path(container['input_path'])
    require(zpath.stat().st_size==container['input_bytes'] and sha(zpath)==container['input_SHA256'],'Whole ZIP binding mismatch')
    require(strict(container['members'],member_rows),'Native ZIP inventory ordering mismatch')
    with zipfile.ZipFile(zpath) as z:
        infos=z.infolist();require(len(infos)==29,'Native ZIP directory size mismatch')
        require(z.testzip() is None,'Native ZIP CRC failure')
        for row in container['members']:
            zi=infos[row['ordinal_zero_based']]
            require(zi.filename==row['original_member_name'] and not zi.is_dir(),'Native member name/order/type mismatch')
            require(not Path(zi.filename).is_absolute() and '..' not in Path(zi.filename).parts,'Unsafe native path')
            require(not stat.S_ISLNK(zi.external_attr>>16),'Symlink native member')
            require(zi.file_size==row['bytes'] and zi.compress_size==row['compressed_bytes'] and zi.compress_type==row['compression_method'],'Native member size/compression mismatch')
            require(zi.external_attr==row['native_external_attr'] and zi.create_system==row['native_create_system'] and zi.flag_bits==row['native_flags'] and list(zi.date_time)==row['native_date_time'],'Native member attributes/timestamp mismatch')
            body=z.read(zi)
            require(format(zi.CRC,'08x')==row['CRC32']==format(zlib.crc32(body)&0xffffffff,'08x'),'Native member CRC mismatch')
            require(hashlib.sha256(body).hexdigest()==row['SHA256'],'Native member SHA mismatch')
            extracted=Path(row['extracted_path']);bytes_check(extracted,row)
            require(body==extracted.read_bytes(),'Whole extracted bytes mismatch')
            checked+=1

print(json.dumps({'status':'PASS_METADATA_ONLY_SOURCE_NATIVE_AND_ZIP_CUSTODY','source_files_checked':len(rows),'literal_native_byte_copies_checked':len(copies),'whole_native_API_objects_checked':len(apis),'whole_transport_receipts_checked':len(transports),'native_schema_pointer_types_reconstructed':len(schema_fresh),'duplicate_content_type_header_receipts_preserved':duplicate_header_receipts,'record_latest_swh_empty_object_versions_swh_null_preserved':True,'native_file_entries_list_order_empty_list_and_default_preview_null_preserved':True,'ZIP_containers_checked':len(containers),'nested_archives':0,'ZIP_members_CRC_sizes_compression_attributes_dates_order_SHA_and_extracted_bytes_checked':checked,'errors':[],'scientific_manuscript_code_results_or_archived_opinions_semantically_read':False,'scientific_programmes_or_source_builders_executed':False,'network_or_preexisting_writes':False,'root131_gate':'CLOSED','publication_authority':False},indent=2))
