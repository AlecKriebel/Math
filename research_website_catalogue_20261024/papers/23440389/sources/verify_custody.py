#!/usr/bin/env python3
"""Read-only record122 native custody closure; never runs source programs."""
from pathlib import Path,PurePosixPath
from hashlib import sha256,md5
from datetime import datetime,timezone
import json,stat,sys,zipfile,zlib

S=Path(__file__).resolve().parent
READY_SHA='8316224d19c14731bfe4a66946ea1fbe612965bcef284479ebfd9163846147a8'
EXCLUDED={'SOURCE_READY_MANIFEST.json','SOURCE_READY_CLOSURE.json','SOURCE_READY_SEAL.json'}


def need(ok,message):
    if not ok:raise ValueError(message)


def h(body):return sha256(body).hexdigest()


def read(path):return json.loads(path.read_bytes())


def blob(path,size,expected):
    body=path.read_bytes();need(len(body)==size and h(body)==expected,'whole body bytes/SHA256')
    return body


def main():
    args=sys.argv[1:];need(args in ([],['--preseal'],['--inputs-only']),'arguments')
    need(h((S/'SOURCE_READY.json').read_bytes())==READY_SHA,'SOURCE_READY identity')
    ready=read(S/'SOURCE_READY.json')
    need(ready['record_id']==23440389 and ready['version']=='1.0' and
         ready['publication_date']=='2026-10-17' and
         ready['created']=='2026-10-17T18:10:27.832798+00:00','native identity/date/version')
    objects={}
    for rec in ready['whole_native_API_objects']:
        objects[rec['role']]=json.loads(blob(Path(rec['path']),rec['bytes'],rec['SHA256']))
    need(set(objects)=={'record','latest','versions_page001','files'},'complete native objects')
    r,l,v,f=(objects[k] for k in ['record','latest','versions_page001','files'])
    need(r['id']==l['id']==23440389 and type(v['hits']['total']) is int and
         v['hits']['total']==1 and [x['id'] for x in v['hits']['hits']]==[23440389]
         and 'next' not in v['links'],'all native versions/latest')
    need(type(f['entries']) is list and f['order']==[] and f['default_preview'] is None,
         'native files schema')
    distinction=ready['native_schema_distinctions']
    need(distinction['record_swh_original']==r['swh'] and
         distinction['latest_swh_original']==l['swh'] and
         distinction['versions_swh_original']==[x['swh'] for x in v['hits']['hits']],
         'native heterogeneous types preserved')
    assets=ready['all_native_assets_in_original_order']
    need([x['original_api_file_object'] for x in assets]==r['files'] and
         [x['whole_original_native_files_entry'] for x in assets]==f['entries'],
         'whole original asset objects and native order')
    need([x['original_api_file_object']['key'] for x in assets]==
         ['Tree_Five_List_Verification_v1.0.zip','Tree_Five_List_Note_v1.0.pdf'],
         'native ZIP then PDF')
    for asset in assets:
        body=blob(Path(asset['path']),asset['bytes'],asset['SHA256'])
        need('md5:'+md5(body).hexdigest()==asset['original_api_file_object']['checksum'],
             'native asset MD5')
    recfile=Path(ready['actual_transport_receipts_path'])
    need(h(recfile.read_bytes())==ready['actual_transport_receipts_SHA256'],'transport binding')
    records=read(recfile)['receipts']
    need([x['HTTP_status'] for x in records]==[200,301,200,200,200,200,200],
         'actual statuses, including complete redirect')
    for rec in records:
        blob(Path(rec['body_path']),rec['body_bytes'],rec['body_SHA256'])
        need(rec['whole_response_body_captured'] is True and
             isinstance(rec['response_headers_in_received_order'],list) and
             rec['custom_request_headers']==[] and
             rec['custom_proxy_or_authentication_or_query'] is False,
             'ordinary whole native HTTP transport')
    need(records[0]['request_count']==1 and records[1]['HTTP_status']==301 and
         records[1]['body_bytes']==99 and records[2]['requested_url']==records[0]['requested_url'],
         'single first request and actual native latest redirect')
    need(ready['custom_headers_proxy_auth_query_or_retry_tricks_used'] is False,
         'no unauthorized access mechanism')
    custody_path=Path(ready['whole_archive_custody_path'])
    need(h(custody_path.read_bytes())==ready['whole_archive_custody_SHA256'],'archive evidence')
    custody=read(custody_path);payloads=custody['all_safe_regular_occurrences']
    total=0;names=set();embedded=0
    with zipfile.ZipFile(Path(assets[0]['path'])) as z:
        members=z.infolist();need(len(members)==len(payloads)==61,'whole ZIP member count')
        for ordinal,(member,item) in enumerate(zip(members,payloads)):
            q=PurePosixPath(member.filename)
            need(not q.is_absolute() and '..' not in q.parts and '\\' not in member.filename
                 and ':' not in member.filename and member.filename.casefold() not in names,
                 'safe unique archive names')
            names.add(member.filename.casefold())
            need(not member.is_dir() and not member.flag_bits&1 and
                 stat.S_IFMT(member.external_attr>>16) in (0,stat.S_IFREG),'regular native payload')
            body=z.read(member)
            need(len(body)==member.file_size==item['bytes'] and h(body)==item['SHA256']
                 and zlib.crc32(body)&0xffffffff==member.CRC and item['CRC32']=='%08x'%member.CRC
                 and item['ordinal_zero_based']==ordinal and item['original_member_name']==member.filename,
                 'whole payload CRC/bytes/hash/order')
            need(Path(item['extracted_path']).read_bytes()==body,'complete extracted bytes')
            total+=len(body);embedded+=body.startswith(b'%PDF-')
    need(total==386822 and embedded==0 and custody['nested_archives']==0,
         'expanded/nested/PDF inventory')
    tex=ready['controlling_TeX'];body=blob(Path(tex['extracted_path']),tex['bytes'],tex['SHA256'])
    need(len(body)==9402 and len(body.splitlines())==tex['lines']==201,'controlling TeX')
    identity=read(Path(ready['printed_identity_path']))
    need(identity['PDF']['pages']==ready['selected_actual_PDF']['pages']==3 and
         identity['controlling_TeX']['date_preamble']==r'17 October 2026 \quad Version 1.0',
         'actual manuscript pages/date/version')
    need(ready['target_manuscript_scientifically_read'] is False and
         ready['controlling_TeX_mathematical_body_read'] is False and
         ready['source_programs_executed_or_scientifically_read'] is False and
         ready['archived_current_opinions_or_inventory_triage_read'] is False and
         ready['target_PDF_pages_rendered'] is False,'custody-only exposure contract')
    count=None
    if args!=['--inputs-only']:
        manifest=read(S/'SOURCE_READY_MANIFEST.json');listed=set()
        for item in manifest['files']:
            q=S/item['path'];need(q.is_relative_to(S) and not q.is_symlink(),'owned regular path')
            blob(q,item['bytes'],item['SHA256']);listed.add(item['path'])
        actual={str(q.relative_to(S)) for q in S.rglob('*') if q.is_file()
                and str(q.relative_to(S)) not in EXCLUDED}
        need(actual==listed,'complete owned source membership');count=len(listed)
    if not args:
        seal=read(S/'SOURCE_READY_SEAL.json')
        for name,key in [('SOURCE_READY.json','SOURCE_READY_SHA256'),
          ('SOURCE_READY_MANIFEST.json','SOURCE_READY_MANIFEST_SHA256'),
          ('SOURCE_READY_CLOSURE.json','SOURCE_READY_CLOSURE_SHA256')]:
            need(h((S/name).read_bytes())==seal[key],'terminal source seal')
        closure=read(S/'SOURCE_READY_CLOSURE.json')
        need(closure['exit_code']==0 and closure['result']['verdict']=='PASS' and
             closure['verifier_SHA256']==h(Path(__file__).read_bytes()),'actual read-only closure')
    print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'verdict':'PASS',
      'mode':args[0] if args else 'terminal-read-only','record_id':23440389,'native_assets':2,
      'whole_ZIP_payloads':61,'expanded_bytes':total,'actual_ordinary_HTTP_requests':len(records),
      'native_latest_redirect_body_preserved':True,'PDF_pages':3,'controlling_TeX_bytes':9402,
      'controlling_TeX_lines':201,'manifest_payloads':count,
      'mathematics_code_results_opinions_scientifically_read':False,
      'source_programs_executed':[],'network_requests':[],'writes':[]},indent=2))


if __name__=='__main__':main()
