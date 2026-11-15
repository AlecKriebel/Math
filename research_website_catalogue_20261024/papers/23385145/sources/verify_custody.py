#!/usr/bin/env python3
"""Read-only native custody closure. No network, extraction or source execution."""
from pathlib import Path, PurePosixPath
from hashlib import sha256, md5
from datetime import datetime, timezone
import io
import json
import stat
import sys
import zipfile
import zlib

S=Path(__file__).resolve().parent
P=S/'attempts/20261115T022501Z'
EXCLUDED={'SOURCE_READY_MANIFEST.json','SOURCE_READY_CLOSURE.json','SOURCE_READY_SEAL.json'}
READY_HASH='398351e05ac4ddc92510ea191c109dd22a48a177869872a8008ff2f8328581e5'


def need(ok,label):
    if not ok:raise ValueError(label)


def h(body):return sha256(body).hexdigest()


def read(path):return json.loads(path.read_bytes())


def check_blob(path,size,expected):
    body=path.read_bytes()
    need(len(body)==size and h(body)==expected,'whole byte identity: '+str(path))
    return body


def names_safe(names):
    seen=set()
    for name in names:
        q=PurePosixPath(name)
        need(not q.is_absolute() and '..' not in q.parts and '\\' not in name
             and ':' not in name and q.parts,'unsafe archive path')
        need(name.casefold() not in seen,'duplicate archive name')
        seen.add(name.casefold())


def main():
    args=sys.argv[1:]
    need(args in ([],['--preseal'],['--inputs-only']),'unsupported arguments')
    need(h((S/'SOURCE_READY.json').read_bytes())==READY_HASH,'SOURCE_READY changed')
    ready=read(S/'SOURCE_READY.json')
    record=read(P/'retry-02/record.raw.json')
    latest=read(P/'latest.raw.json')
    versions=read(P/'versions.page-001.raw.json')
    files=read(P/'files.raw.json')
    need(record['id']==latest['id']==ready['record_id']==23385145,'record/latest identity')
    need(record['metadata']['version']==ready['version']=='1.0','native version')
    need(record['metadata']['publication_date']==ready['publication_date']=='2026-10-14'
         and record['created']==ready['created']=='2026-10-15T05:18:05.239497+00:00',
         'publication/created distinction')
    need(type(versions['hits']['total']) is int and versions['hits']['total']==1
         and [x['id'] for x in versions['hits']['hits']]==[23385145]
         and 'next' not in versions['links'],'complete all versions')
    need(record['swh']=={} and latest['swh']=={} and
         versions['hits']['hits'][0]['swh'] is None,'native swh object/null')
    need(type(files['entries']) is list and files['order']==[] and
         files['default_preview'] is None,'native files schema')
    assets=ready['all_assets_in_original_order']
    need([a['original_api_file_object'] for a in assets]==record['files'],'whole file objects')
    need([a['key'] for a in record['files']]==[a['key'] for a in files['entries']]==
         ['weighted_centers.pdf','verification_package.zip'],'actual native asset order')
    for entry,asset in zip(files['entries'],assets):
        body=check_blob(Path(asset['path']),asset['bytes'],asset['sha256'])
        need('md5:'+md5(body).hexdigest()==entry['checksum']==
             asset['original_api_file_object']['checksum'],'native MD5')
        need(entry['size']==len(body)==asset['original_api_file_object']['size'],'native size')
    for obj in ready['whole_native_API_objects']:
        check_blob(Path(obj['path']),obj['bytes'],obj['SHA256'])
    for field,hashfield in [('whole_archive_custody_path','whole_archive_custody_SHA256'),
                          ('native_schema_types_path','native_schema_types_SHA256'),
                          ('actual_transport_receipt_path','actual_transport_receipt_SHA256')]:
        need(h(Path(ready[field]).read_bytes())==ready[hashfield],'native evidence binding')
    schemas=read(P/'NATIVE_SCHEMA_TYPES.json')
    for relative,item in schemas.items():
        check_blob(P/relative,item['bytes'],item['SHA256'])
    receipts=read(P/'ALL_TRANSPORT_RECEIPTS.json')['receipts']
    need(len(receipts)==7 and [x['HTTP_status'] for x in receipts]==[403,200,200,200,200,200,200],
         'all failed/successful transports')
    for rec in receipts:
        check_blob(Path(rec['path']),rec['bytes'],rec['SHA256'])
        need(isinstance(rec['headers_in_received_order'],list),'ordered headers')
    for rec in receipts[-2:]:
        need(sum(k.lower()=='content-type' for k,v in rec['headers_in_received_order'])==2,
             'duplicate native headers preserved')
    first=read(P/'START.json')
    need(first['preexisting_paper_directory'] is False and
         (S/'.gitignore').read_text()==first['ignore_rules_installed_before_downloads'],
         'absence/ignore guard')
    need(all(datetime.fromisoformat(r['started_UTC'])>datetime.fromisoformat(first['UTC'])
             for r in receipts),'ignore/setup precedes network')
    archive=read(P/'archive-custody.json')
    stored=archive['all_safe_regular_occurrences']
    need(len(stored)==93 and archive['nested_archives']==0,'complete archive count')
    total=0;embedded=0
    with zipfile.ZipFile(P/'assets/verification_package.zip') as z:
        members=z.infolist();names_safe([m.filename for m in members])
        need(len(members)==len(stored),'archive native entry count')
        for ordinal,(m,entry) in enumerate(zip(members,stored)):
            need(m.orig_filename==m.filename and not m.is_dir() and not m.flag_bits&1 and
                 stat.S_IFMT(m.external_attr>>16) in (0,stat.S_IFREG),'safe native member')
            body=z.read(m)
            need(entry['original_member_name']==m.filename and
                 entry['ordinal_zero_based']==ordinal and entry['bytes']==len(body)==m.file_size
                 and entry['CRC32']=='%08x'%m.CRC and zlib.crc32(body)&0xffffffff==m.CRC
                 and entry['SHA256']==h(body),'complete member size/CRC/SHA256')
            need(Path(entry['extracted_path']).read_bytes()==body,'whole extracted body')
            need(not zipfile.is_zipfile(io.BytesIO(body)),'unrecorded nested ZIP')
            embedded+=body.startswith(b'%PDF-')
            total+=len(body)
    need(total==archive['expanded_bytes_all_depths']==705178 and embedded==0,
         'full package expanded/PDF inventory')
    identity=read(P/'MANUSCRIPT_IDENTITY.json')
    tex=ready['controlling_TeX'];body=check_blob(Path(tex['extracted_path']),tex['bytes'],tex['SHA256'])
    need(len(body.splitlines())==tex['lines']==311 and len(body)==16269,'controlling TeX size/lines')
    need(identity['PDF']['pages']==ready['selected_actual_PDF']['pages']==5 and
         identity['controlling_TeX']['date_preamble_command']=='October 14, 2026' and
         identity['PDF']['printed_front_matter_before_abstract'].endswith('October 14, 2026'),
         'actual printed identity/page count')
    need(ready['target_manuscript_scientifically_read'] is False and
         ready['source_programs_executed_or_scientifically_read'] is False and
         ready['archived_current_opinions_or_inventory_triage_read'] is False and
         ready['target_PDF_pages_rendered'] is False,'custody-only exposure contract')
    count=None
    if args!=['--inputs-only']:
        manifest=read(S/'SOURCE_READY_MANIFEST.json');paths=set()
        for entry in manifest['files']:
            q=S/entry['path'];need(q.is_relative_to(S) and not q.is_symlink(),'owned regular path')
            check_blob(q,entry['bytes'],entry['SHA256']);paths.add(entry['path'])
        actual={str(q.relative_to(S)) for q in S.rglob('*') if q.is_file()
                and str(q.relative_to(S)) not in EXCLUDED}
        need(actual==paths,'complete source-custody manifest membership');count=len(paths)
    if not args:
        seal=read(S/'SOURCE_READY_SEAL.json')
        for filename,field in [('SOURCE_READY.json','SOURCE_READY_SHA256'),
          ('SOURCE_READY_MANIFEST.json','SOURCE_READY_MANIFEST_SHA256'),
          ('SOURCE_READY_CLOSURE.json','SOURCE_READY_CLOSURE_SHA256')]:
            need(h((S/filename).read_bytes())==seal[field],'terminal custody seal')
        closure=read(S/'SOURCE_READY_CLOSURE.json')
        need(closure['exit_code']==0 and closure['result']['verdict']=='PASS'
             and closure['verifier_SHA256']==h(Path(__file__).read_bytes()),'actual read-only closure')
    print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'verdict':'PASS',
      'mode':args[0] if args else 'terminal-read-only','record_id':23385145,
      'native_original_assets':2,'whole_archive_payloads':len(stored),'expanded_bytes':total,
      'native_objects':4,'all_native_versions':1,'failed_transports_preserved':1,
      'PDF_pages':5,'controlling_TeX_bytes':len(body),'controlling_TeX_lines':311,
      'manifest_payloads':count,'scientific_reading_or_source_execution':False,
      'network_requests':[],'writes':[]},indent=2))


if __name__=='__main__':main()
