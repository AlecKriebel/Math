#!/usr/bin/env python3
"""Pure offline source custody: metadata/opaque bytes only, no science reading.

No project/supplied-code imports, subprocesses, network or writes. Reads this
source packet and the explicitly qualified18core source inputs by reference.
"""
from pathlib import Path,PurePosixPath
from urllib.parse import urlsplit,urljoin
import binascii,hashlib,io,json,os,stat,struct,sys,unicodedata,zipfile

R=Path(__file__).absolute().parent
TERMS={'SOURCE_READY_CLOSURE.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json'}
N=0
external={}
ownedpins={}

def need(ok,why):
    global N
    N+=1
    if not ok:
        raise ValueError(why)

def pin(body):
    return {'bytes':len(body),'SHA256':hashlib.sha256(body).hexdigest()}

def read(path):
    path=Path(path)
    need(path.is_absolute() and '..' not in path.parts,'canonical absolute path')
    need(path.is_relative_to(R) or str(path) in external,'unbound external read')
    before=path.lstat();need(stat.S_ISREG(before.st_mode),'ordinary input file')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        held=os.fstat(fd);need((held.st_dev,held.st_ino)==(before.st_dev,before.st_ino),'open identity')
        parts=[]
        while True:
            part=os.read(fd,1048576)
            if not part:break
            parts.append(part)
        after=os.fstat(fd)
        need((held.st_size,held.st_mtime_ns,held.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns),'held file stable')
        final=path.lstat();need((final.st_dev,final.st_ino)==(held.st_dev,held.st_ino),'final pathname identity')
        body=b''.join(parts);need(len(body)==held.st_size,'complete file read')
        if str(path) in external:need(pin(body)==external[str(path)],'qualified input pin')
        if path.is_relative_to(R):
            rel=path.relative_to(R).as_posix()
            if rel in ownedpins:need(pin(body)==ownedpins[rel],'same-buffer owned payload authentication')
        return body
    finally:os.close(fd)

def obj(path):
    return json.loads(read(path))

def bound(row):
    body=read(Path(row['path']))
    need(pin(body)=={k:row[k] for k in ['bytes','SHA256']},'whole declared byte identity')
    return body

def typed(a,b):
    need(type(a) is type(b),'literal type')
    if type(a) is dict:
        need(list(a)==list(b),'key/order')
        for k in a:typed(a[k],b[k])
    elif type(a) is list:
        need(len(a)==len(b),'list length')
        for x,y in zip(a,b):typed(x,y)
    else:need(a==b,'literal value')

def scan():
    files=[];dirs=[]
    def visit(path):
        before=path.lstat();need(stat.S_ISDIR(before.st_mode),'ordinary directory')
        with os.scandir(path) as it:entries=sorted(it,key=lambda x:x.name)
        for e in entries:
            p=path/e.name;rel=p.relative_to(R).as_posix();mode=p.lstat().st_mode
            if stat.S_ISDIR(mode):dirs.append(rel);visit(p)
            elif stat.S_ISREG(mode):files.append({'path':rel,**pin(read(p))})
            else:raise ValueError('symlink/FIFO/special namespace entry '+rel)
        after=path.lstat()
        need((before.st_dev,before.st_ino,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_mtime_ns,after.st_ctime_ns),'stable directory enumeration')
    visit(R)
    return sorted(files,key=lambda x:x['path']),sorted(dirs)

def main():
    need(sys.argv[1:]==[],'only offline read-only default supported')
    mf_body=read(R/'SOURCE_READY_MANIFEST.json');mf=json.loads(mf_body)
    need(mf['excluded_terminal_files']==sorted(TERMS),'exact root terminal schema')
    for row in mf['files']:ownedpins[row['path']]={k:row[k] for k in ['bytes','SHA256']}
    files,dirs=scan()
    need(TERMS <= {r['path'] for r in files},'all three root terminals already exist as ordinary files')
    actual=[r for r in files if r['path'] not in TERMS]
    typed(actual,mf['files']);typed(dirs,mf['directories'])
    need(mf['no_basename_directory_or_future_file_exclusions'] is True,'no future carveout')
    seal=obj(R/'SOURCE_READY_SEAL.json')
    finalized=seal.get('status')=='SOURCE_READY_SEALED'
    if finalized:
        need(seal['MANIFEST_SHA256']==pin(mf_body)['SHA256'],'same-buffer final manifest binding')
        need(seal['SOURCE_READY_SHA256']==pin(read(R/'SOURCE_READY.json'))['SHA256'],'whole final READY binding')
        need(seal['CLOSURE_SHA256']==pin(read(R/'SOURCE_READY_CLOSURE.json'))['SHA256'],'whole final literal closure binding')
    else:
        need(seal.get('status')=='SOURCE_READY_SEAL_FINALIZATION_IN_PROGRESS','explicit unsealed finalizer phase only')
    for row in obj(R/'INPUT_MANIFEST.json')['files']:
        path=Path(row['path'])
        if path.is_relative_to(R):bound(row)
        else:
            need(row['role']=='read-only governing instruction at intake; historical by-reference pin','declared historical input role')
    core=obj(R/'QUALIFIED_CORE_BINDINGS.json')
    for row in core['files']+[core['reference']]:external[row['path']]={k:row[k] for k in ['bytes','SHA256']}
    for row in core['files']+[core['reference']]:bound(row)
    need(len(core['files'])==18 and core['original17_plus_sole_authorized405b'] is True and core['all18_original_unchanged_claim'] is False,'qualified source core only')
    need(core['reference']['SHA256']=='0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104','actual authorized qualified-core reference')
    prior_core=obj(Path(core['reference']['path']))
    typed(core['files'],[{k:r[k] for k in ['path','bytes','SHA256']} for r in prior_core['files']])
    q=obj(R/'QUEUE_BINDING.json');ready=obj(R/'SOURCE_READY.json');a=obj(R/'ACQUIRED_NATIVE.json')
    record=obj(R/'record.response.body');meta=record['metadata']
    need(record['id']==q['identity_only']['record_id']==ready['record_id']==23430927,'exact record identity')
    need(ready['sheet_row']==q['identity_only']['sheet_row']==144,'queue row identity')
    need(meta['title']==q['identity_only']['title']==ready['title'] and record['doi']==q['identity_only']['doi']==ready['DOI'],'title DOI identity')
    need(q['current_native_Sheet_read'] is False and q['root144_scientific_gate']=='CLOSED','neutral existing-queue gate')
    for field in ['publication_date','created','updated']:
        need(ready[field]==(meta[field] if field=='publication_date' else record[field]),'literal native date')
    need(type(ready['version_field_present']) is bool and ready['version_field_present']==('version' in meta),'native version presence')
    typed(ready['version'],meta.get('version'))
    for parent,key,target in [(record,'conceptrecid','native_conceptrecid_whole_field'),(meta,'version','native_version_whole_field'),(meta,'license','native_license_metadata_whole_field'),(meta,'resource_type','native_resource_type_whole_field')]:
        typed({'present':key in parent,'original_value':parent.get(key)},ready[target])
    native={}
    for row in a['whole_native_API_objects']:native[row['role']]=json.loads(bound(row))
    latest=native['latest'];need(latest['id']==record['id'] and latest['doi']==record['doi'],'native latest identity')
    need(record['status']==latest['status']=='published' and record['state']==latest['state']=='done','published native states')
    pages=[(role,value) for role,value in native.items() if role.startswith('versions-page')]
    hits=[v for role,page in pages for v in page['hits']['hits']]
    need([v['id'] for v in hits]==ready['all_enumerated_version_ids']==a['all_version_ids'],'original complete version order')
    need(len(hits)==len({str(v['id']) for v in hits}),'no duplicate version ids')
    for i,(role,page) in enumerate(pages):
        total=page['hits']['total'];count=total if type(total) is int else total.get('value') if type(total) is dict else None
        need(type(count) is int and count==len(hits),'native version total original shape')
        need(bool(page.get('links',{}).get('next'))==(i+1<len(pages)),'actual next-link exhaustion')
    need(a['version_pagination_exhaustive'] is True and ready['version_enumeration_exhaustive_no_next_link'] is True,'complete native versions')
    fileobj=native['files'];entries=fileobj['entries'];pairs=list(entries.items()) if type(entries) is dict else [(None,x) for x in entries]
    typed(record['files'],[x['original_api_file_object'] for x in a['all_assets_in_original_order']])
    for asset in a['all_assets_in_original_order']:
        original=asset['original_api_file_object'];matches=[x for k,x in pairs if x.get('key',k)==original['key']]
        need(len(matches)==1,'unique native files entry');typed(matches[0],asset['whole_original_native_files_entry'])
        body=bound(asset);algorithm,checksum=original['checksum'].split(':',1)
        need(len(body)==original['size'] and hashlib.new(algorithm,body).hexdigest()==checksum,'actual native size/checksum')
        need(body==read(Path(asset['transport_body_path'])),'whole actual transport and asset bytes')
    typed(a['all_assets_in_original_order'],ready['all_native_assets_in_original_order']);typed(a['whole_native_API_objects'],ready['whole_native_API_objects'])
    transports=obj(R/'ALL_TRANSPORT_RECEIPTS.json')
    need([x['HTTP_status'] for x in transports]==ready['HTTP_status_sequence'],'literal request/status order')
    for i,t in enumerate(transports):
        need(t['method']=='GET' and urlsplit(t['request_URL']).scheme=='https' and urlsplit(t['request_URL']).hostname=='zenodo.org','ordinary native request only')
        need(type(t['actual_request_headers_in_sent_order']) is list and type(t['response_headers_in_received_order']) is list,'whole ordered headers')
        bound({'path':t['body_path'],'bytes':t['bytes'],'SHA256':t['SHA256']})
        if t['redirect_hop']:
            previous=transports[i-1];locations=[v for k,v in previous['response_headers_in_received_order'] if k.lower()=='location']
            need(len(locations)==1 and urljoin(previous['request_URL'],locations[0])==t['request_URL'],'only actual Location followed')
    typed([x for x in transports if x.get('HTTP_status') is not None and x['HTTP_status']!=200],ready['raw_non_200_response_bodies'])
    typed([x for x in transports if x.get('error_type') is not None],ready['failed_transports_preserved_whole'])
    expected_dist={'record_swh':{'present':'swh' in record,'original_value':record.get('swh')},'latest_swh':{'present':'swh' in latest,'original_value':latest.get('swh')},'versions_swh_fields':[{'present':'swh' in x,'original_value':x.get('swh')} for x in hits],'versions_total_original_fields':a['all_versions_total_original_fields'],'files_entries_original_type':type(entries).__name__,'files_order':{'present':'order' in fileobj,'original_value':fileobj.get('order')},'files_default_preview':{'present':'default_preview' in fileobj,'original_value':fileobj.get('default_preview')},'original_header_order_and_duplicates_preserved':True}
    typed(expected_dist,ready['native_schema_distinctions'])
    shapes=[]
    def shape(value,path,role):
        row={'role':role,'JSON_pointer':path,'original_type':type(value).__name__}
        if value is None or value=={} or value==[]:row['original_empty_or_null_value']=value
        shapes.append(row)
        if type(value) is dict:
            for k,v in value.items():shape(v,path+'/'+str(k).replace('~','~0').replace('/','~1'),role)
        elif type(value) is list:
            for i,v in enumerate(value):shape(v,path+'/'+str(i),role)
    for row in a['whole_native_API_objects']:shape(native[row['role']],'',row['role'])
    typed(shapes,obj(R/'NATIVE_SCHEMA_TYPES.json'))
    arc=obj(R/'ARCHIVE_CUSTODY.json');occurrences=[];expanded=0
    need(all(c['kind']=='zip' for c in arc['containers']),'this actual packet contains ZIP containers only')
    for container in arc['containers']:
        cb=read(Path(container['input_path']));need(pin(cb)['SHA256']==container['input_SHA256'],'whole archive bytes')
        with zipfile.ZipFile(io.BytesIO(cb)) as z:
            infos=z.infolist();need(len(infos)==len(container['members']),'all original member occurrences')
            directory=[{'ordinal_zero_based':i,'filename':t.filename,'original_filename':t.orig_filename,'is_directory':t.is_dir(),'bytes':t.file_size,'compressed_bytes':t.compress_size,'CRC32':'%08x'%t.CRC,'flags':t.flag_bits,'compression':t.compress_type,'native_date_time':list(t.date_time),'external_attr':t.external_attr,'internal_attr':t.internal_attr,'create_system':t.create_system,'create_version':t.create_version,'extract_version':t.extract_version,'header_offset':t.header_offset,'extra_hex':t.extra.hex(),'comment_hex':t.comment.hex()} for i,t in enumerate(infos)]
            typed(directory,container['whole_original_central_directory']);need(z.comment.hex()==container['original_archive_comment_hex'],'whole archive comment')
            seen=set()
            for info,item in zip(infos,container['members']):
                need(info.filename==info.orig_filename==item['original_member_name'],'whole member name')
                name=PurePosixPath(info.filename);need(not name.is_absolute() and '..' not in name.parts and '\\' not in info.filename,'safe member path')
                folded=unicodedata.normalize('NFC',info.filename.rstrip('/')).casefold();need(folded not in seen,'duplicate/case collision');seen.add(folded)
                mode=stat.S_IFMT(info.external_attr>>16);need(mode in ([0,stat.S_IFDIR] if info.is_dir() else [0,stat.S_IFREG]) and not(info.flag_bits&1),'regular unencrypted member')
                if info.is_dir():
                    need(stat.S_ISDIR((Path(container['extraction_root'])/info.filename).lstat().st_mode),'explicit archive directory retained')
                    continue
                body=z.read(info);need(len(body)==info.file_size==item['bytes'] and '%08x'%(binascii.crc32(body)&0xffffffff)==item['CRC32']=='%08x'%info.CRC,'full CRC and size')
                need(pin(body)['SHA256']==item['SHA256'] and body==read(Path(item['extracted_path'])),'complete extracted body identity')
                occurrences.append((container['container_id'],item['ordinal_zero_based']));expanded+=len(body)
    need(len(occurrences)==arc['whole_regular_payload_occurrences']==ready['whole_regular_payload_occurrences'],'all regular members')
    need(set(occurrences)=={(x['container_id'],x['ordinal_zero_based']) for x in arc['regular_payload_occurrences']} and expanded==arc['expanded_bytes_all_depths'],'full occurrence coverage')
    m=obj(R/'MANUSCRIPT_CUSTODY.json');typed(m['selected_actual_PDF'],ready['selected_actual_PDF']);typed(m['controlling_TeX'],ready['controlling_TeX'])
    native_readers=[x for x in a['all_assets_in_original_order'] if Path(x['path']).suffix.lower()=='.pdf']
    need(len(native_readers)==len(m['actual_standalone_readers'])==len(ready['actual_standalone_readers']),'all actual native readers')
    for asset,reader,enriched in zip(native_readers,m['actual_standalone_readers'],ready['actual_standalone_readers']):
        for k,v in asset.items():typed(v,reader[k])
        for k,v in reader.items():typed(v,enriched[k])
        need(type(reader['pages']) is int and reader['pages']>0 and enriched['scientific_role_or_typeset_equivalence_assessed'] is False,'actual metadata-only reader count')
    texs=[x for x in arc['regular_payload_occurrences'] if x['original_member_name'].lower().endswith('.tex')]
    need(len(texs)==len(ready['all_TeX_candidates']),'every original TeX occurrence')
    for raw,enriched in zip(texs,ready['all_TeX_candidates']):
        for k,v in raw.items():typed(v,enriched[k])
        need(len(bound({'path':raw['extracted_path'],'bytes':raw['bytes'],'SHA256':raw['SHA256']}).splitlines())==enriched['opaque_byte_splitlines_count'] and enriched['preamble_or_mathematical_body_read'] is False,'actual opaque TeX byte lines')
    typed(ready['all_TeX_candidates'],ready['controlling_TeX_sources_in_original_archive_order'])
    need(ready['actual_standalone_TeX_assets']==m['actual_standalone_TeX_assets']==[],'actual absence of standalone native TeX')
    images=m['fresh_page_rasters'];need(len(images)==sum(x['pages'] for x in m['actual_standalone_readers'])==ready['all_native_reader_total_pages'],'all native reader raster coverage')
    for image in images:
        body=bound(image);need(body[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',body[16:24])==(image['width'],image['height']),'actual PNG format/dimensions')
        need(image['visually_read'] is False,'unread raster exposure')
    identity=obj(R/'NATIVE_IDENTITY_MATCH.json')
    need(identity['queue_and_fresh_native_record_match'] is True and identity['current_native_Sheet_read'] is False and identity['current_native_identifier_and_queued_status_match'] is None,'queue versus unobserved Sheet distinction')
    need(ready['current_native_sheet_identity_subset'] is None and ready['current_sheet_tab_and_bounds'] is None and ready['current_native_sheet_and_fresh_published_record_identity_match'] is None,'no synthetic Sheet verification')
    need(ready['printed_title_date_version_inspected'] is False and ready['printed_date'] is None and ready['printed_version'] is None,'unread printed fields')
    need(ready['target_PDF_text_extracted'] is False and ready['target_PDF_rasters_visually_read'] is False and ready['mathematical_PDF_TeX_or_pixels_read'] is False and ready['TeX_preamble_or_mathematical_body_read'] is False,'no scientific reading')
    need(ready['source_programmes_executed']==[] and ready['source_scientific_proofs_code_results_triage_reviews_or_opinions_read'] is False and ready['scientific_verdict'] is None and ready['publication_authority'] is False,'closed science/publication gate')
    base=obj(R/'READY_KEY_SCHEMA.json')
    suffix=['source_custody_schema_additions','additional_controlling_TeX_sources','controlling_TeX_sources_in_original_archive_order','native_reader_source_structural_associations','whole_record_source_reading_requirement_for_future_science','all_native_reader_total_pages','source_mapping_is_structural_only_no_typeset_or_scientific_equivalence_certified','source_identity_binding','source_identity_provenance_qualification','qualified_core_original17_plus_authorized405b']
    need(list(ready)==base['SOURCE_READY_key_order']+suffix and ready['schema']==base['schema'],'same established READY order plus exact declared additions')
    print(json.dumps({'status':'SOURCE_CUSTODY_PASS','record_id':23430927,'mode':'pure-offline-default','checks':N,
        'owned_payloads':len(actual),'owned_directories':len(dirs),'exact_root_terminal_files':sorted(TERMS),
        'whole_regular_payload_occurrences':len(occurrences),'nested_archives':arc['nested_archive_count'],
        'PDF_pages':m['PDF_pages'],'all_native_reader_pages':ready['all_native_reader_total_pages'],
        'native_readers':len(native_readers),'TeX_sources':len(texs),'TeX_lines':ready['controlling_TeX']['opaque_byte_splitlines_count'],
        'actual_HTTP_requests':len(transports),'seal_finalized_and_bound':finalized,
        'native_Sheet_read':False,'scientific_reading_or_execution':False,'network_requests':0,'writes':0},sort_keys=True))

if __name__=='__main__':main()
