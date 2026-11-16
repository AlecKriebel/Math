#!/usr/bin/env python3
"""Source-only. --acquire ID creates one absent source root; --seal ID freezes it.
Default verifies existing seals read-only. No native/source program executes.
Only pdfinfo metadata is inspected; no manuscript text or page pixels are read.
"""
from pathlib import Path, PurePosixPath
import datetime, hashlib, http.client, io, json, os, ssl, stat, subprocess, sys, tarfile, traceback, urllib.parse, zipfile

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N=P/'verification/source146-148-sol-20261116'
WORKS={23425412:146,23443039:147,22929556:148}
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

class Intake:
    def __init__(self,rid):
        self.rid=rid; self.R=root(rid); self.receipts=[]; self.containers=[]; self.members=[]; self.pdfs=[]; self.tex=[]; self.expanded=0; self.entries=0
        safe(self.R); need(self.R.parent.is_dir() and not os.path.lexists(self.R),'exclusive absent source root'); self.R.mkdir()
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
                conn.close(); write(bodypath,data); receipt.update(completed_UTC=utc(),**pin(data)); write(self.R/(stem+'.transport.json'),js(receipt)); self.receipts.append(receipt)
            self.event('NATIVE_GET_COMPLETE',role=role,status=receipt['HTTP_status'],bytes=len(data))
            if receipt['HTTP_status'] in (301,302,303,307,308):
                locations=[v for k,v in receipt['response_headers_in_received_order'] if k.lower()=='location']; need(len(locations)==1,'one actual native redirect Location'); current=urllib.parse.urljoin(current,locations[0]); continue
            need(receipt['HTTP_status']==200,'native GET failed; preserved raw response, no bypass: '+str(receipt['HTTP_status']))
            return data,bodypath
        raise ValueError('native redirect limit')
    def pdf(self,path,record_id,origin):
        b=path.read_bytes(); need(b.startswith(b'%PDF-'),'actual PDF signature')
        result=subprocess.run(['pdfinfo','-isodates',str(path)],capture_output=True)
        tag='pdfinfo-'+str(len(self.pdfs)+1).zfill(3)
        write(self.R/(tag+'.stdout'),result.stdout); write(self.R/(tag+'.stderr'),result.stderr)
        pages=None
        if result.returncode==0:
            for line in result.stdout.decode(errors='replace').splitlines():
                if line.startswith('Pages:'): pages=int(line.split(':',1)[1].strip())
        item={'path':str(path),**pin(b),'record_id':record_id,'origin':origin,'pages':pages,'pdfinfo_exit':result.returncode,'pdfinfo_stdout':tag+'.stdout','pdfinfo_stderr':tag+'.stderr','pixels_or_extracted_text_read':False}
        self.pdfs.append(item)
    def inspect(self,path,record_id,origin,depth=0):
        data=path.read_bytes()
        if data.startswith(b'%PDF-'): self.pdf(path,record_id,origin)
        if path.suffix.lower() in ('.tex','.ltx','.latex'):
            self.tex.append({'path':str(path),**pin(data),'record_id':record_id,'origin':origin,'opaque_byte_splitlines':len(data.splitlines()),'scientific_body_read':False})
        iszip=zipfile.is_zipfile(io.BytesIO(data))
        istar=(len(data)>262 and data[257:262]==b'ustar') or path.name.lower().endswith(('.tar','.tar.gz','.tgz','.tar.bz2','.tbz2','.tar.xz','.txz'))
        if not iszip and not istar: return
        need(depth<8,'nested archive depth cap8')
        cid='container-'+str(len(self.containers)+1).zfill(3); out=self.R/'published-source'/cid
        container={'container_id':cid,'record_id':record_id,'depth':depth,'path':str(path),**pin(data),'kind':'zip' if iszip else 'tar','origin':origin}; self.containers.append(container)
        archive=zipfile.ZipFile(io.BytesIO(data)) if iszip else tarfile.open(fileobj=io.BytesIO(data),mode='r:*')
        names={}
        try:
            items=archive.infolist() if iszip else archive
            for ordinal,entry in enumerate(items):
                self.entries+=1; need(self.entries<=20000,'archive occurrence cap20000')
                name=entry.filename if iszip else entry.name
                q=PurePosixPath(name); need(name and '\x00' not in name and '\\' not in name and not q.is_absolute() and '..' not in q.parts and not (q.parts and ':' in q.parts[0]),'unsafe archive path')
                size=entry.file_size if iszip else entry.size; directory=entry.is_dir() if iszip else entry.isdir()
                permissions=(entry.external_attr>>16) if iszip else entry.mode
                regular=(stat.S_IFMT(permissions) in (0,stat.S_IFREG)) if iszip else entry.isfile()
                need(directory or regular,'archive special/link member refused')
                member={'container_id':cid,'record_id':record_id,'ordinal_zero_based':ordinal,'original_name':name,'bytes':size,'directory':directory,'native_mode':permissions}
                if iszip: member.update(CRC32=hex(entry.CRC),compressed_bytes=entry.compress_size,compression_method=entry.compress_type,flags=entry.flag_bits,date_time=list(entry.date_time),create_system=entry.create_system)
                self.members.append(member)
                if directory:
                    destination=out/'tree'/Path(*q.parts); safe(destination); destination.mkdir(parents=True,exist_ok=True); member['extracted_directory_path']=str(destination); continue
                need(size<=268435456,'member cap256MiB'); self.expanded+=size; need(self.expanded<=1073741824,'expanded custody cap1GiB')
                occurrence=names.get(name,0); names[name]=occurrence+1
                destination=out/('tree' if occurrence==0 else 'duplicates/'+str(ordinal).zfill(6))/Path(*q.parts)
                stream=archive.open(entry) if iszip else archive.extractfile(entry)
                with stream: body=stream.read(268435457)
                need(len(body)==size,'whole archive member'); write(destination,body)
                member.update(extracted_path=str(destination),**pin(body),duplicate_occurrence=occurrence)
                self.inspect(destination,record_id,{'container_id':cid,'ordinal_zero_based':ordinal,'original_name':name},depth+1)
        finally: archive.close()
    def acquire(self):
        given_raw,given_path=self.get('https://zenodo.org/api/records/'+str(self.rid),'record'); given=json.loads(given_raw); need(given['id']==self.rid,'queued exact native record ID')
        latest_raw,latest_path=self.get('https://zenodo.org/api/records/'+str(self.rid)+'/versions/latest','latest'); latest=json.loads(latest_raw)
        url='https://zenodo.org/api/records/'+str(self.rid)+'/versions'; versions=[]; pages=[]
        while url:
            need(len(pages)<20,'native version-page cap20'); raw,path=self.get(url,'versions-'+str(len(pages)+1).zfill(3)); obj=json.loads(raw); pages.append({'path':str(path),**pin(raw)}); versions.extend(obj['hits']['hits']); url=obj.get('links',{}).get('next')
        ids=list(dict.fromkeys([self.rid,latest['id'],*[x['id'] for x in versions]])); need(len(ids)<=20,'published version cap20')
        records={self.rid:(given,given_path),latest['id']:(latest,latest_path)}; summaries=[]; assets=[]
        for rid in ids:
            if rid not in records:
                raw,path=self.get('https://zenodo.org/api/records/'+str(rid),'version-'+str(rid)); records[rid]=(json.loads(raw),path)
            record,path=records[rid]; meta=record['metadata']; need(record['id']==rid and record.get('doi','').lower()=='10.5281/zenodo.'+str(rid),'native ID/DOI association')
            need(meta.get('resource_type',{}).get('type')=='publication','native publication-type record')
            creators=meta.get('creators',[]); need(any('kriebel' in c.get('name','').lower() and 'alec' in c.get('name','').lower() for c in creators),'native Alec Kriebel creator identity')
            for c in creators:
                if 'kriebel' in c.get('name','').lower() and c.get('orcid'): need(c['orcid'].endswith('0009-0001-9320-500X'),'native author ORCID')
            need(record.get('conceptrecid')==given.get('conceptrecid'),'same native concept/version family')
            files_raw,files_path=self.get('https://zenodo.org/api/records/'+str(rid)+'/files','files-'+str(rid)); files_obj=json.loads(files_raw)
            native=record['files']; need(isinstance(native,list),'original native file ordering must be list')
            local_assets=[]
            for ordinal,item in enumerate(native):
                key=item['key']; need(key and Path(key).name==key and key not in ('.','..') and '\\' not in key,'ordinary native asset name')
                links=item['links']; link=links.get('content',links.get('self')); need(isinstance(link,str),'native actual asset link')
                data,body_path=self.get(link,'asset-'+str(rid)+'-'+str(ordinal+1).zfill(3))
                need(len(data)==item['size'] and item['checksum'].startswith('md5:') and hashlib.md5(data).hexdigest()==item['checksum'][4:],'native MD5/size exact')
                local=self.R/('assets' if rid==self.rid else 'versions/'+str(rid)+'/assets')/key; write(local,data)
                asset={'ordinal_zero_based':ordinal,'record_id':rid,'key':key,'original_API_file_object':item,'path':str(local),'transport_body_path':str(body_path),**pin(data),'native_MD5_verified':True,'fresh_ordinary_native_GET':True,'cached_bytes_reused':False}
                local_assets.append(asset); assets.append(asset); self.inspect(local,rid,{'native_asset':key,'ordinal_zero_based':ordinal})
            summaries.append({'record_id':rid,'record_body_path':str(path),'title':meta['title'],'DOI':record['doi'],'creators':creators,'publication_date':meta.get('publication_date'),'created':record.get('created'),'updated':record.get('updated'),'native_record_state':field(record,'state'),'native_is_published':field(record,'is_published'),'native_version_whole_field':field(meta,'version'),'native_conceptrecid_whole_field':field(record,'conceptrecid'),'license_whole_field':field(meta,'license'),'resource_type_whole_field':field(meta,'resource_type'),'description_whole_field':field(meta,'description'),'files_endpoint_body_path':str(files_path),'files_endpoint_original_order_and_fields':files_obj,'all_native_assets_in_original_order':local_assets})
        need(any(x['record_id']==latest['id'] and x['origin'].get('native_asset') for x in self.pdfs),'latest published native actual PDF exists')
        pairs=[]
        for pdf in self.pdfs:
            candidates=[t for t in self.tex if t['record_id']==pdf['record_id'] and Path(t['path']).stem==Path(pdf['path']).stem]
            if not candidates:
                same=[t for t in self.tex if t['record_id']==pdf['record_id']]; candidates=same if len(same)==1 else []
            pairs.append({'PDF':pdf['path'],'record_id':pdf['record_id'],'source_candidates':candidates,'basis':'same basename; otherwise sole version-specific TeX candidate; filename-only association, no build/scientific correspondence asserted'})
        self.event('NATIVE_PDF_SOURCE_ACQUISITION_COMPLETE',completion_percent=90,native_assets=len(assets),PDF_readers=len(self.pdfs),TeX_candidates=len(self.tex))
        result={'schema':'source-only-native-acquired-v1','UTC':utc(),'queued_record_id':self.rid,'sheet_row':WORKS[self.rid],'latest_record_id':latest['id'],'all_enumerated_version_ids_in_native_order':[x['id'] for x in versions],'version_pages':pages,'version_enumeration_no_next_link':True,'records':summaries,'all_native_assets':assets,'all_actual_PDF_readers':self.pdfs,'all_TeX_candidates':self.tex,'manuscript_source_associations':pairs,'containers':self.containers,'members':self.members,'actual_HTTP_receipts':self.receipts,'expanded_regular_bytes':self.expanded,'archive_member_occurrences':self.entries,'source_custody_completion_percent':90,'scientific_body_code_results_opinions_or_PDF_pixels_text_read':False,'printed_date_version_inspected':False,'scientific_verdict':None,'AA':None,'canonical_url':None,'publication_authority':False,'outside_contact_or_prepared_outreach':False}
        write(self.R/'ACQUIRED.json',js(result)); return result

def inventory(R):
    files=[]; dirs=[]
    for p in sorted(R.rglob('*')):
        s=p.lstat(); rel=p.relative_to(R).as_posix()
        if stat.S_ISDIR(s.st_mode): dirs.append(rel)
        else: need(stat.S_ISREG(s.st_mode),'ordinary source namespace'); files.append({'path':rel,**pin(p.read_bytes()),'mode':stat.S_IMODE(s.st_mode)})
    return files,dirs
def seal(rid):
    R=root(rid); need(not any((R/x).exists() for x in TERMINALS),'seal exclusively once'); acquired=readjson(R/'ACQUIRED.json')
    need(acquired['queued_record_id']==rid and acquired['scientific_verdict'] is None,'source-only acquired association')
    ready={'schema':'source-only-ready-unread-science-v1','UTC':utc(),'record_id':rid,'sheet_row':WORKS[rid],'latest_record_id':acquired['latest_record_id'],'native_version_records':len(acquired['records']),'native_assets':acquired['all_native_assets'],'actual_PDF_readers':acquired['all_actual_PDF_readers'],'all_TeX_candidates':acquired['all_TeX_candidates'],'source_associations':acquired['manuscript_source_associations'],'archive_containers':len(acquired['containers']),'archive_occurrences':len(acquired['members']),'all_native_MD5_verified':True,'all_original_native_metadata_description_license_dates_and_asset_order_preserved_in':'ACQUIRED.json and raw API bodies','source_custody_completion_percent':100,'native_mathematical_bodies_code_results_opinions_and_PDF_pixels_text_read':False,'scientific_verdict':None,'printed_date_version_inspected':False,'AA':None,'canonical_url':None,'publication_authority':False,'source_program_executions':[],'metadata_tool_executed':'pdfinfo only'}
    write(R/'SOURCE_READY.json',js(ready)); files,dirs=inventory(R)
    manifest={'schema':'finite-source-manifest-v1','root':str(R),'files':files,'directories':dirs,'exact_terminal_exclusions':sorted(TERMINALS),'no_future_or_subtree_exclusions':True}
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
    return {'status':'PASS_SOURCE_ONLY_CUSTODY','record_id':rid,'final':{'path':str(R/'SOURCE_FINAL.json'),**pin((R/'SOURCE_FINAL.json').read_bytes())},'manifest':{'path':str(R/'SOURCE_MANIFEST.json'),**pin(body)},'files':len(files),'directories':len(dirs),'native_assets':final['native_assets'],'PDF_readers':final['PDF_readers'],'PDF_pages_total_known':final['PDF_pages_total_known'],'PDF_pages_unknown':final['PDF_pages_unknown'],'TeX_candidates':final['TeX_candidates'],'scientific_verdict':None,'writes':0}

def main():
    need(Path(__file__).absolute()==N/'acquire_sources.py','fixed new helper location')
    if not sys.argv[1:]: print(json.dumps([verify(rid) for rid in WORKS],indent=2)); return
    need(len(sys.argv)==3 and sys.argv[1] in ('--acquire','--seal') and int(sys.argv[2]) in WORKS,'fixed source-only modes/IDs')
    rid=int(sys.argv[2])
    if sys.argv[1]=='--seal': print(json.dumps(seal(rid),indent=2)); return
    intake=Intake(rid)
    try:
        result=intake.acquire(); print(json.dumps({'status':'ACQUIRED_UNREAD_SCIENCE','record_id':rid,'ACQUIRED':{'path':str(intake.R/'ACQUIRED.json'),**pin((intake.R/'ACQUIRED.json').read_bytes())},'native_assets':len(result['all_native_assets']),'PDF_readers':len(result['all_actual_PDF_readers']),'TeX_candidates':len(result['all_TeX_candidates'])}),flush=True)
    except BaseException as error:
        failure={'UTC':utc(),'record_id':rid,'status':'SOURCE_INCOMPLETE_PRESERVED_FAILURE','error':repr(error),'traceback':traceback.format_exc(),'actual_receipts':intake.receipts,'containers_seen':intake.containers,'members_seen':intake.members,'PDF_metadata_seen':intake.pdfs,'TeX_candidates_seen':intake.tex,'scientific_verdict':None}; write(intake.R/'ACQUISITION_FAILURE.json',js(failure)); print(json.dumps({'record_id':rid,'error':repr(error)}),flush=True); raise

if __name__=='__main__': main()
