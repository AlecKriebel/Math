#!/usr/bin/env python3
"""Source-only. --acquire ID creates one absent source root; --seal ID freezes it.
Default is a literal no-action response. No native/source program executes.
Only pdfinfo metadata is inspected; no manuscript text or page pixels are read.
"""
from pathlib import Path, PurePosixPath
import bz2, datetime, gzip, hashlib, http.client, io, json, lzma, os, re, ssl, stat, struct, subprocess, sys, tarfile, traceback, unicodedata, urllib.parse, zipfile

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N=P/'verification/source185-nextthree-sol-20261116'
WORKS={23527793:185,23205294:186,23203323:187}
EXPECTED={23527793:('1.0','2026-10-21'),23205294:('1.0.0','2026-10-06'),23203323:('1.0.0','2026-10-06')}
PDFINFO='/opt/homebrew/bin/pdfinfo'
TERMINALS={'SOURCE_MANIFEST.json','SOURCE_FINAL.json'}

def need(ok,why):
    if not ok: raise ValueError(why)
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(b): return {'bytes':len(b),'SHA256':sha(b)}
def js(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def safe(p):
    need(p.is_absolute() and '..' not in p.parts and all(not q.is_symlink() for q in [p,*p.parents]),'safe ordinary path')
def write(p,b):
    safe(p); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f: f.write(b)
def field(obj,key): return {'present':key in obj,'original_value':obj.get(key)}
def readjson(p): return json.loads(p.read_bytes())
def root(rid): return P/'papers'/str(rid)/'sources'

def bound_zip_directory(data,remaining):
    start=max(0,len(data)-65557); end=data.rfind(b'PK\x05\x06',start)
    need(end>=0 and end+22<=len(data),'ordinary ZIP end record')
    signature,disk,central_disk,disk_count,count,size,offset,comment=struct.unpack_from('<4s4H2LH',data,end)
    need(end+22+comment==len(data),'ZIP whole end/comment boundary')
    need(disk==central_disk==0 and disk_count==count,'single-disk ordinary ZIP only')
    need(count!=65535 and size!=4294967295 and offset!=4294967295,'ZIP64 unsupported; preserved without parser expansion')
    need(0<=count<=remaining and size<=8388608 and offset+size==end,'ZIP directory pre-parser count/8MiB bounds')
    if end>=20: need(data[end-20:end-16]!=b'PK\x06\x07','ZIP64 locator unsupported')
    position=offset; actual=0
    while position<end:
        need(actual<remaining and position+46<=end and data[position:position+4]==b'PK\x01\x02','bounded ZIP central header')
        name,extra,note=struct.unpack_from('<3H',data,position+28)
        position+=46+name+extra+note; actual+=1
        need(position<=end,'whole bounded ZIP directory record')
    need(position==end and actual==count,'ZIP directory exact physical entry count')

def bound_tar_headers(data,remaining):
    position=0; count=0
    while position+512<=len(data):
        header=data[position:position+512]
        if header==bytes(512):
            need(not any(data[position:]),'ordinary TAR zero-only trailer'); return
        count+=1; need(count<=remaining,'TAR pre-parser header count')
        kind=header[156:157]
        need(kind in (b'0',b'\x00',b'5'),'extended/sparse/link TAR metadata unsupported before parser')
        size=tarfile.nti(header[124:136])
        need(0<=size<=268435456 and (kind!=b'5' or size==0),'TAR pre-parser regular/dir size')
        position+=512+((size+511)//512)*512
        need(position<=len(data),'TAR physical payload boundary')
    need(position==len(data),'TAR whole header boundary')

class Intake:
    def __init__(self,rid):
        self.rid=rid; self.R=root(rid); self.receipts=[]; self.containers=[]; self.members=[]; self.pdfs=[]; self.pdf_cache={}; self.tex=[]; self.expanded=0; self.entries=0
        safe(self.R); need(not os.path.lexists(self.R),'exclusive absent source root'); self.R.parent.mkdir(exist_ok=True); need(self.R.parent.is_dir(),'ordinary record parent'); self.R.mkdir()
        self.event('SOURCE_INTAKE_STARTED',completion_percent=5)
    def event(self,name,**fields):
        value={'UTC':utc(),'event':name,**fields}
        with (self.R/'SOURCE_LOG.jsonl').open('ab') as f: f.write((json.dumps(value,ensure_ascii=False)+'\n').encode())
        print(json.dumps({'record_id':self.rid,**value},ensure_ascii=False),flush=True)
    def get(self,url,role):
        current=url
        for hop in range(9):
            u=urllib.parse.urlsplit(current); need(u.scheme=='https' and u.hostname=='zenodo.org' and u.port in (None,443) and not u.username and not u.password,'ordinary public native Zenodo HTTPS only')
            stem=role+('' if hop==0 else '.redirect-'+str(hop).zfill(2)); bodypath=self.R/(stem+'.response.body')
            headers=[['Host','zenodo.org'],['User-Agent','Python source-only native custody'],['Accept','*/*'],['Connection','close']]
            target=urllib.parse.quote(u.path or '/',safe="/%:@!$&'()*+,;=-._~")+('?' + u.query if u.query else '')
            receipt={'started_UTC':utc(),'role':role,'redirect_hop':hop,'method':'GET','URL':current,'request_target':target,'request_headers_in_sent_order':headers,'body_path':str(bodypath)}
            conn=http.client.HTTPSConnection('zenodo.org',timeout=120,context=ssl.create_default_context()); data=b''
            try:
                conn.putrequest('GET',target,skip_host=True,skip_accept_encoding=True)
                for k,v in headers: conn.putheader(k,v)
                conn.endheaders(); response=conn.getresponse()
                receipt.update(HTTP_status=response.status,HTTP_reason=response.reason,response_headers_in_received_order=[list(x) for x in response.getheaders()],response_HTTP_version=response.version)
                data=response.read(536870913)
                need(len(data)<=536870912,'native response exceeds512MiB custody cap')
                declared=response.getheader('Content-Length'); need(declared is None or int(declared)==len(data),'whole declared HTTP response body')
                receipt.update(whole_response_read=True)
            except BaseException as error:
                if isinstance(error,http.client.IncompleteRead): data=error.partial
                receipt.update(error=repr(error),whole_response_read=False); raise
            finally:
                conn.close(); write(bodypath,data); receipt.update(completed_UTC=utc(),MD5=hashlib.md5(data).hexdigest(),**pin(data)); write(self.R/(stem+'.transport.json'),js(receipt)); self.receipts.append(receipt)
            self.event('NATIVE_GET_COMPLETE',role=role,status=receipt['HTTP_status'],bytes=len(data))
            if receipt['HTTP_status'] in (301,302,303,307,308):
                locations=[v for k,v in receipt['response_headers_in_received_order'] if k.lower()=='location']; need(len(locations)==1,'one actual native redirect Location'); current=urllib.parse.urljoin(current,locations[0]); continue
            need(receipt['HTTP_status']==200,'native GET failed; preserved raw response, no bypass: '+str(receipt['HTTP_status']))
            return data,bodypath
        raise ValueError('native redirect limit')
    def pdf(self,path,record_id,origin):
        b=path.read_bytes(); need(b.startswith(b'%PDF-'),'actual PDF signature'); digest=sha(b)
        reused=digest in self.pdf_cache
        if reused: pages,code,tag=self.pdf_cache[digest]
        else:
            tag='pdfinfo-'+str(len(self.pdf_cache)+1).zfill(3)
            try: result=subprocess.run([PDFINFO,'-isodates',str(path)],capture_output=True,timeout=30)
            except subprocess.TimeoutExpired as error:
                write(self.R/(tag+'.stdout'),error.stdout or b''); write(self.R/(tag+'.stderr'),error.stderr or b''); write(self.R/(tag+'.exit'),b'TIMEOUT\\n'); self.pdfs.append({'path':str(path),**pin(b),'record_id':record_id,'origin':origin,'pages':None,'pdfinfo_exit':'TIMEOUT','pdfinfo_stdout':tag+'.stdout','pdfinfo_stderr':tag+'.stderr','pdfinfo_exit_stream':tag+'.exit','pixels_or_extracted_text_read':False}); raise
            write(self.R/(tag+'.stdout'),result.stdout); write(self.R/(tag+'.stderr'),result.stderr); write(self.R/(tag+'.exit'),(str(result.returncode)+'\n').encode())
            pages=None; code=result.returncode
            if code==0:
                for line in result.stdout.decode(errors='replace').splitlines():
                    if line.startswith('Pages:'): pages=int(line.split(':',1)[1].strip())
            self.pdf_cache[digest]=(pages,code,tag)
        self.pdfs.append({'path':str(path),**pin(b),'record_id':record_id,'origin':origin,'pages':pages,'pdfinfo_exit':code,'pdfinfo_stdout':tag+'.stdout','pdfinfo_stderr':tag+'.stderr','pdfinfo_exit_stream':tag+'.exit','metadata_reused_only_for_exact_same_SHA256':reused,'pixels_or_extracted_text_read':False})
    def inspect(self,path,record_id,origin,depth=0):
        data=path.read_bytes()
        if data.startswith(b'%PDF-'): self.pdf(path,record_id,origin)
        if path.suffix.lower() in ('.tex','.ltx','.latex'):
            self.tex.append({'path':str(path),**pin(data),'record_id':record_id,'origin':origin,'opaque_byte_splitlines':len(data.splitlines()),'has_documentclass_marker':b'\\documentclass' in data,'has_begin_document_marker':b'\\begin{document}' in data,'scientific_body_read':False})
        iszip=zipfile.is_zipfile(io.BytesIO(data))
        istar=(len(data)>262 and data[257:262]==b'ustar') or path.name.lower().endswith(('.tar','.tar.gz','.tgz','.tar.bz2','.tbz2','.tar.xz','.txz'))
        compressed = 'gzip' if data.startswith(b'\x1f\x8b') else 'bzip2' if data.startswith(b'BZh') else 'xz' if data.startswith(b'\xfd7zXZ\x00') else None
        if data.startswith((b'7z\xbc\xaf\x27\x1c',b'Rar!\x1a\x07')):
            self.containers.append({'path':str(path),**pin(data),'kind':'UNSUPPORTED_CONTAINER_PRESERVED','record_id':record_id,'depth':depth}); raise ValueError('unsupported native container; no installation or bypass')
        need(path.suffix.lower()!='.zip' or iszip,'advertised ZIP must parse')
        if compressed and not iszip:
            need(depth<8,'nested archive depth cap8'); cid='container-'+str(len(self.containers)+1).zfill(3); out=self.R/'published-source'/cid/'tree'; out.mkdir(parents=True)
            self.containers.append({'container_id':cid,'record_id':record_id,'depth':depth,'path':str(path),**pin(data),'kind':compressed,'origin':origin})
            stream=gzip.GzipFile(fileobj=io.BytesIO(data)) if compressed=='gzip' else bz2.BZ2File(io.BytesIO(data)) if compressed=='bzip2' else lzma.LZMAFile(io.BytesIO(data))
            with stream: body=stream.read(268435457)
            need(len(body)<=268435456 and len(body)<=1000*max(1,len(data)),'single compressed payload/ratio cap'); self.expanded+=len(body); need(self.expanded<=1073741824,'expanded custody cap1GiB'); self.entries+=1; need(self.entries<=20000,'archive occurrence cap20000')
            name=path.stem if path.suffix.lower() in ('.gz','.bz2','.xz') else 'decoded-member'; destination=out/name; write(destination,body)
            self.members.append({'container_id':cid,'record_id':record_id,'ordinal_zero_based':0,'original_name':None,'decoded_name':name,'directory':False,'extracted_path':str(destination),**pin(body)})
            self.inspect(destination,record_id,{'container_id':cid,'single_compressed_payload':True},depth+1); return
        if not iszip and not istar: return
        need(depth<8,'nested archive depth cap8')
        cid='container-'+str(len(self.containers)+1).zfill(3); out=self.R/'published-source'/cid; (out/'tree').mkdir(parents=True)
        container={'container_id':cid,'record_id':record_id,'depth':depth,'path':str(path),**pin(data),'kind':'zip' if iszip else 'tar','origin':origin}; self.containers.append(container)
        bound_zip_directory(data,20000-self.entries) if iszip else bound_tar_headers(data,20000-self.entries)
        archive=zipfile.ZipFile(io.BytesIO(data)) if iszip else tarfile.open(fileobj=io.BytesIO(data),mode='r:')
        names={}; spellings={}
        try:
            items=archive.infolist() if iszip else archive
            for ordinal,entry in enumerate(items):
                self.entries+=1; need(self.entries<=20000,'archive occurrence cap20000')
                name=entry.orig_filename if iszip else entry.name
                q=PurePosixPath(name); need(name and '\x00' not in name and '\\' not in name and not q.is_absolute() and '..' not in q.parts and not (q.parts and ':' in q.parts[0]),'unsafe archive path')
                size=entry.file_size if iszip else entry.size; directory=entry.is_dir() if iszip else entry.isdir()
                permissions=(entry.external_attr>>16) if iszip else entry.mode
                regular=(stat.S_IFMT(permissions) in (0,stat.S_IFREG)) if iszip else entry.isfile()
                need((directory and (not iszip or stat.S_IFMT(permissions) in (0,stat.S_IFDIR))) or (not directory and regular),'archive special/link member refused')
                if iszip: need(not entry.flag_bits&1 and (size==0 or (entry.compress_size>0 and size<=1000*entry.compress_size)),'encrypted/archive-ratio member refused')
                need(q.parts or directory,'nonempty regular member path')
                folded=unicodedata.normalize('NFC',q.as_posix()).casefold(); previous=names.get(folded)
                for component in [q,*q.parents]:
                    if component.as_posix()=='.': continue
                    folded_component=unicodedata.normalize('NFC',component.as_posix()).casefold()
                    need(folded_component not in spellings or spellings[folded_component]==component.as_posix(),'implicit directory case/Unicode collision refused'); spellings[folded_component]=component.as_posix()
                need(previous is None or (directory and previous==('directory',name)),'archive duplicate/case/Unicode collision refused')
                need(all(names.get(unicodedata.normalize('NFC',parent.as_posix()).casefold(),('directory',None))[0]!='file' for parent in q.parents),'archive file-as-parent collision refused')
                if not directory: need(not any(key.startswith(folded+'/') for key in names),'archive directory-as-file collision refused')
                names[folded]=('directory' if directory else 'file',name)
                member={'container_id':cid,'record_id':record_id,'ordinal_zero_based':ordinal,'original_name':name,'bytes':size,'directory':directory,'native_mode':permissions}
                if iszip: member.update(CRC32=hex(entry.CRC),compressed_bytes=entry.compress_size,compression_method=entry.compress_type,flags=entry.flag_bits,date_time=list(entry.date_time),create_system=entry.create_system)
                self.members.append(member)
                if directory:
                    destination=out/'tree'/Path(*q.parts); safe(destination); destination.mkdir(parents=True,exist_ok=True); member['extracted_directory_path']=str(destination); continue
                need(size<=268435456,'member cap256MiB'); self.expanded+=size; need(self.expanded<=1073741824,'expanded custody cap1GiB')
                destination=out/'tree'/Path(*q.parts)
                stream=archive.open(entry) if iszip else archive.extractfile(entry)
                with stream: body=stream.read(268435457)
                need(len(body)==size,'whole archive member'); write(destination,body)
                member.update(extracted_path=str(destination),**pin(body),collision_free_native_path=True)
                self.inspect(destination,record_id,{'container_id':cid,'ordinal_zero_based':ordinal,'original_name':name},depth+1)
        finally: archive.close()
    def acquire(self):
        given_raw,given_path=self.get('https://zenodo.org/api/records/'+str(self.rid),'record'); given=json.loads(given_raw); need(given['id']==self.rid,'queued exact native record ID')
        need((given['metadata'].get('version'),given['metadata'].get('publication_date'))==EXPECTED[self.rid],'DECLARED_VERSION_DATE_MISMATCH_STOP_BEFORE_DEPENDENT_WORK')
        native_links=given['links']; need(all(isinstance(native_links.get(k),str) for k in ('latest','versions','files')),'actual returned native API links required')
        latest_raw,latest_path=self.get(native_links['latest'],'latest'); latest=json.loads(latest_raw)
        need(latest['id']==self.rid and (latest['metadata'].get('version'),latest['metadata'].get('publication_date'))==EXPECTED[self.rid],'FRESH_LATEST_VERSION_MISMATCH_STOP_BEFORE_DEPENDENT_WORK')
        url=native_links['versions']; versions=[]; pages=[]
        while url:
            need(len(pages)<20,'native version-page cap20'); raw,path=self.get(url,'versions-'+str(len(pages)+1).zfill(3)); obj=json.loads(raw); pages.append({'path':str(path),**pin(raw)}); versions.extend(obj['hits']['hits']); url=obj.get('links',{}).get('next')
        ids=list(dict.fromkeys([self.rid,latest['id'],*[x['id'] for x in versions]])); need(len(ids)<=20,'published version cap20')
        records={self.rid:(given,given_path)}; summaries=[]; assets=[]
        if latest['id']!=self.rid: records[latest['id']]=(latest,latest_path)
        for rid in ids:
            if rid not in records:
                matches=[v for v in versions if v['id']==rid]; need(len(matches)==1 and isinstance(matches[0].get('links',{}).get('self'),str),'one actual returned historical record self URL'); raw,path=self.get(matches[0]['links']['self'],'version-'+str(rid)); records[rid]=(json.loads(raw),path)
            record,path=records[rid]; meta=record['metadata']; need(record['id']==rid and record.get('doi','').lower()=='10.5281/zenodo.'+str(rid),'native ID/DOI association')
            need(meta.get('resource_type',{}).get('type')=='publication','native publication-type record')
            need(record.get('state')=='done','actual published native record state done')
            creators=meta.get('creators',[]); need(any('kriebel' in c.get('name','').lower() and 'alec' in c.get('name','').lower() for c in creators),'native Alec Kriebel creator identity')
            for c in creators:
                if 'kriebel' in c.get('name','').lower() and c.get('orcid'): need(c['orcid'].endswith('0009-0001-9320-500X'),'native author ORCID')
            need(record.get('conceptrecid')==given.get('conceptrecid'),'same native concept/version family')
            need(isinstance(record.get('links',{}).get('files'),str),'actual returned files endpoint URL'); files_raw,files_path=self.get(record['links']['files'],'files-'+str(rid)); files_obj=json.loads(files_raw)
            native=record['files']; need(isinstance(native,list),'original native file ordering must be list')
            entries=files_obj.get('entries',files_obj.get('files')) if isinstance(files_obj,dict) else files_obj
            endpoint_keys=list(entries) if isinstance(entries,dict) else [x['key'] for x in entries] if isinstance(entries,list) else None
            need(endpoint_keys is not None and len(endpoint_keys)==len(native) and set(endpoint_keys)=={x['key'] for x in native},'complete native record/files endpoint membership')
            local_assets=[]; native_names=set()
            for ordinal,item in enumerate(native):
                key=item['key']; need(key and Path(key).name==key and key not in ('.','..') and '\\' not in key,'ordinary native asset name')
                folded_key=unicodedata.normalize('NFC',key).casefold(); need(folded_key not in native_names,'native filename case/Unicode collision refused'); native_names.add(folded_key)
                links=item['links']; link=links.get('content',links.get('self')); need(isinstance(link,str),'native actual asset link')
                data,body_path=self.get(link,'asset-'+str(rid)+'-'+str(ordinal+1).zfill(3))
                need(len(data)==item['size'] and item['checksum'].startswith('md5:') and hashlib.md5(data).hexdigest()==item['checksum'][4:],'native MD5/size exact')
                local=self.R/('assets' if rid==self.rid else 'versions/'+str(rid)+'/assets')/key; write(local,data)
                asset={'MD5':hashlib.md5(data).hexdigest(),'ordinal_zero_based':ordinal,'record_id':rid,'key':key,'original_API_file_object':item,'path':str(local),'transport_body_path':str(body_path),**pin(data),'native_MD5_verified':True,'fresh_ordinary_native_GET':True,'cached_bytes_reused':False}
                local_assets.append(asset); assets.append(asset); self.inspect(local,rid,{'native_asset':key,'ordinal_zero_based':ordinal})
            summaries.append({'record_id':rid,'record_body_path':str(path),'title':meta['title'],'DOI':record['doi'],'creators':creators,'publication_date':meta.get('publication_date'),'publication_date_whole_field':field(meta,'publication_date'),'created':record.get('created'),'created_whole_field':field(record,'created'),'updated':record.get('updated'),'updated_whole_field':field(record,'updated'),'native_record_state':field(record,'state'),'native_is_published':field(record,'is_published'),'native_version_whole_field':field(meta,'version'),'native_conceptrecid_whole_field':field(record,'conceptrecid'),'license_whole_field':field(meta,'license'),'rights_whole_field':field(meta,'rights'),'access_right_whole_field':field(meta,'access_right'),'resource_type_whole_field':field(meta,'resource_type'),'description_whole_field':field(meta,'description'),'files_endpoint_body_path':str(files_path),'files_endpoint_original_order_and_fields':files_obj,'all_native_assets_in_original_order':local_assets})
        need(any(x['record_id']==latest['id'] and x['origin'].get('native_asset') for x in self.pdfs),'latest published native actual PDF exists')
        need(any(x['record_id']==self.rid and x['origin'].get('native_asset') for x in self.pdfs),'queued published native actual PDF exists')
        pairs=[]
        for pdf in self.pdfs:
            candidates=[t for t in self.tex if t['record_id']==pdf['record_id'] and Path(t['path']).stem==Path(pdf['path']).stem]
            if not candidates:
                same=[t for t in self.tex if t['record_id']==pdf['record_id']]; candidates=same if len(same)==1 else []
            pairs.append({'PDF':pdf['path'],'record_id':pdf['record_id'],'source_candidates':candidates,'basis':'same basename; otherwise sole version-specific TeX candidate; filename-only association, no build/scientific correspondence asserted'})
        self.event('NATIVE_PDF_SOURCE_ACQUISITION_COMPLETE',completion_percent=90,native_assets=len(assets),PDF_readers=len(self.pdfs),TeX_candidates=len(self.tex))
        result={'schema':'source-only-native-acquired-v1','UTC':utc(),'queued_record_id':self.rid,'sheet_row':WORKS[self.rid],'latest_record_id':latest['id'],'latest_matches_queued_record':latest['id']==self.rid,'latest_raw_body_path':str(latest_path),'all_enumerated_version_ids_in_native_order':[x['id'] for x in versions],'version_pages':pages,'version_enumeration_no_next_link':True,'records':summaries,'all_native_assets':assets,'all_actual_PDF_readers':self.pdfs,'all_TeX_candidates':self.tex,'manuscript_source_associations':pairs,'containers':self.containers,'members':self.members,'actual_HTTP_receipts':self.receipts,'expanded_regular_bytes':self.expanded,'archive_member_occurrences':self.entries,'source_custody_completion_percent':90,'safe_limits':{'download_bytes':536870912,'member_bytes':268435456,'expanded_bytes':1073741824,'archive_occurrences':20000,'container_depth':8,'compression_ratio':1000,'version_pages':20,'published_versions':20},'archive_actual_extracted_mode_policy':'new ordinary non-executable files/default safe directories; actual local modes in manifest and native header modes retained verbatim','scientific_body_code_results_opinions_or_PDF_pixels_text_read':False,'printed_date_version_inspected':False,'scientific_verdict':None,'AA':None,'canonical_url':None,'publication_authority':False,'outside_contact_or_prepared_outreach':False}
        write(self.R/'ACQUIRED.json',js(result)); return result

def inventory(R):
    files=[]; dirs=[]
    for p in sorted(R.rglob('*')):
        s=p.lstat(); rel=p.relative_to(R).as_posix()
        if stat.S_ISDIR(s.st_mode): dirs.append({'path':rel,'mode':stat.S_IMODE(s.st_mode)})
        else: need(stat.S_ISREG(s.st_mode),'ordinary source namespace'); files.append({'path':rel,**pin(p.read_bytes()),'mode':stat.S_IMODE(s.st_mode)})
    return files,dirs
def seal(rid):
    R=root(rid); need(not any((R/x).exists() for x in TERMINALS),'seal exclusively once'); acquired=readjson(R/'ACQUIRED.json')
    need(acquired['queued_record_id']==rid and acquired['scientific_verdict'] is None,'source-only acquired association')
    ready={'schema':'source-only-ready-unread-science-v1','UTC':utc(),'record_id':rid,'sheet_row':WORKS[rid],'latest_record_id':acquired['latest_record_id'],'native_version_records':len(acquired['records']),'native_assets':acquired['all_native_assets'],'actual_PDF_readers':acquired['all_actual_PDF_readers'],'all_TeX_candidates':acquired['all_TeX_candidates'],'source_associations':acquired['manuscript_source_associations'],'archive_containers':len(acquired['containers']),'archive_occurrences':len(acquired['members']),'all_native_MD5_verified':True,'all_original_native_metadata_description_license_dates_and_asset_order_preserved_in':'ACQUIRED.json and raw API bodies','source_custody_completion_percent':100,'native_mathematical_bodies_code_results_opinions_and_PDF_pixels_text_read':False,'scientific_verdict':None,'printed_date_version_inspected':False,'AA':None,'canonical_url':None,'publication_authority':False,'source_program_executions':[],'metadata_tool_executed':'pdfinfo only'}
    write(R/'SOURCE_READY.json',js(ready)); files,dirs=inventory(R)
    manifest={'schema':'finite-source-manifest-v1','root':str(R),'root_mode':stat.S_IMODE(R.lstat().st_mode),'files':files,'directories':dirs,'exact_terminal_exclusions':sorted(TERMINALS),'no_future_or_subtree_exclusions':True}
    body=js(manifest); write(R/'SOURCE_MANIFEST.json',body)
    final={'schema':'source-only-final-v1','UTC':utc(),'record_id':rid,'sheet_row':WORKS[rid],'status':'SOURCE_READY_UNREAD_SCIENCE','manifest':{'path':'SOURCE_MANIFEST.json',**pin(body)},'payload_files':len(files),'actual_files':len(files)+2,'child_directories':len(dirs),'exact_terminal_names':sorted(TERMINALS),'native_assets':len(acquired['all_native_assets']),'PDF_readers':len(acquired['all_actual_PDF_readers']),'PDF_pages_total_known':sum(x['pages'] or 0 for x in acquired['all_actual_PDF_readers']),'PDF_pages_unknown':sum(x['pages'] is None for x in acquired['all_actual_PDF_readers']),'TeX_candidates':len(acquired['all_TeX_candidates']),'source_custody_completion_percent':100,'scientific_verdict':None,'source_program_executions':[],'postseal_writes_allowed':False,'AA':None,'canonical_url':None,'publication_authority':False}
    write(R/'SOURCE_FINAL.json',js(final)); checked=verify(rid); checked['writes']=3; checked['seal_files_written']=3; return checked
def verify(rid):
    R=root(rid); final=readjson(R/'SOURCE_FINAL.json'); body=(R/'SOURCE_MANIFEST.json').read_bytes(); need(pin(body)=={k:final['manifest'][k] for k in ('bytes','SHA256')},'whole source manifest pin')
    manifest=json.loads(body); files,dirs=inventory(R); actual={x['path']:x for x in files}; need(set(actual)=={x['path'] for x in manifest['files']}|TERMINALS and dirs==manifest['directories'],'exact finite source namespace')
    for item in manifest['files']: need(actual[item['path']]==item,'whole source payload pin')
    need(len(files)==final['actual_files'] and len(dirs)==final['child_directories'],'exact source counts')
    acquired=readjson(R/'ACQUIRED.json')
    for asset in acquired['all_native_assets']:
        b=Path(asset['path']).read_bytes(); need(pin(b)=={k:asset[k] for k in ('bytes','SHA256')} and hashlib.md5(b).hexdigest()==asset['original_API_file_object']['checksum'][4:],'actual native asset identity')
    return {'status':'SOURCE_READY_CUSTODY_UNREAD_SCIENCE','record_id':rid,'final':{'path':str(R/'SOURCE_FINAL.json'),**pin((R/'SOURCE_FINAL.json').read_bytes())},'manifest':{'path':str(R/'SOURCE_MANIFEST.json'),**pin(body)},'files':len(files),'directories':len(dirs),'native_assets':final['native_assets'],'PDF_readers':final['PDF_readers'],'PDF_pages_total_known':final['PDF_pages_total_known'],'PDF_pages_unknown':final['PDF_pages_unknown'],'TeX_candidates':final['TeX_candidates'],'scientific_verdict':None,'writes':0}

def main():
    need(Path(__file__).absolute()==N/'acquire_sources_guarded.py','fixed new helper location')
    if not sys.argv[1:]: print(json.dumps({'status':'NO_ACTION_EXPLICIT_FIXED_ID_MODE_REQUIRED','network_calls':0,'writes':0})); return
    need(len(sys.argv)==3 and sys.argv[1] in ('--acquire','--seal') and int(sys.argv[2]) in WORKS,'fixed source-only modes/IDs')
    rid=int(sys.argv[2])
    if sys.argv[1]=='--seal': print(json.dumps(seal(rid),indent=2)); return
    intake=Intake(rid)
    try:
        result=intake.acquire(); print(json.dumps({'status':'ACQUIRED_UNREAD_SCIENCE','record_id':rid,'ACQUIRED':{'path':str(intake.R/'ACQUIRED.json'),**pin((intake.R/'ACQUIRED.json').read_bytes())},'native_assets':len(result['all_native_assets']),'PDF_readers':len(result['all_actual_PDF_readers']),'TeX_candidates':len(result['all_TeX_candidates'])}),flush=True)
    except BaseException as error:
        failure={'UTC':utc(),'record_id':rid,'status':'SOURCE_INCOMPLETE_PRESERVED_FAILURE','error':repr(error),'traceback':traceback.format_exc(),'actual_receipts':intake.receipts,'containers_seen':intake.containers,'members_seen':intake.members,'PDF_metadata_seen':intake.pdfs,'TeX_candidates_seen':intake.tex,'scientific_verdict':None}; write(intake.R/'ACQUISITION_FAILURE.json',js(failure)); print(json.dumps({'record_id':rid,'error':repr(error)}),flush=True); raise

if __name__=='__main__': main()
