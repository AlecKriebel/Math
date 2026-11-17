#!/usr/bin/env python3
"""One root-authorized ordinary GET per fixed URL. Default performs no action.

No retry, redirect following, cache bypass, browser, project import or Git route.
Retain every exposed response/failure and all received/decoded body evidence.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urldefrag, unquote
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError
import datetime, gzip, hashlib, json, os, re, stat, sys, time, traceback, zlib

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N = P/'verification/outer-pedal-godbillon-vey-live-http-sol-20261116'
EXPECT_SHA = 'e4cee460b30d48ac6dac0f00bf4eefaa8225fe7e51ab35045d2f5375118c9908'

def need(ok, why):
    if not ok: raise ValueError(why)
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(b): return {'bytes':len(b),'SHA256':sha(b)}
def packed(x): return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def utc(): return datetime.datetime.now(datetime.timezone.utc)
def safe(q):
    need(q.is_absolute() and '..' not in q.parts and all(not x.is_symlink() for x in [q,*q.parents]),'canonical non-symlink path')
def read(q):
    safe(q); before=q.lstat(); need(stat.S_ISREG(before.st_mode),'ordinary source file')
    with q.open('rb') as f:
        first=os.fstat(f.fileno()); need((first.st_dev,first.st_ino)==(before.st_dev,before.st_ino),'opened identity'); b=f.read(); last=os.fstat(f.fileno())
    need((first.st_size,first.st_mtime_ns,first.st_ctime_ns)==(last.st_size,last.st_mtime_ns,last.st_ctime_ns) and len(b)==first.st_size,'stable whole source read')
    need((q.lstat().st_dev,q.lstat().st_ino)==(first.st_dev,first.st_ino),'live source identity'); return b
def bound(row):
    q=Path(row['path']); q=q if q.is_absolute() else P/q; b=read(q)
    need(pin(b)=={k:row[k] for k in ('bytes','SHA256')},'whole pinned input: '+str(q))
    if 'mode' in row: need(stat.S_IMODE(q.lstat().st_mode)==row['mode'],'source mode unchanged')
    return b
def sync_dir(q):
    fd=os.open(q,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try: os.fsync(fd)
    finally: os.close(fd)
def write(q,b):
    safe(q); need(q.is_relative_to(N) and q!=N,'owned output only'); fd=os.open(q,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        with os.fdopen(fd,'wb',closefd=False) as f: f.write(b); f.flush(); os.fchmod(fd,0o600); os.fsync(fd)
    finally: os.close(fd)
    sync_dir(q.parent)

class Page(HTMLParser):
    def __init__(self,b):
        super().__init__(convert_charrefs=True); self.tags=[]; self.ids=set(); self.scripts=[]; self.script=None; self.feed(b.decode('utf-8')); self.close()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if a.get('id'): need(a['id'] not in self.ids,'unique HTML fragment ID'); self.ids.add(a['id'])
        if tag=='script' and a.get('type')=='application/ld+json': self.script=[]
    def handle_data(self,data):
        if self.script is not None: self.script.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.script is not None: self.scripts.append(json.loads(''.join(self.script))); self.script=None
    def values(self,tag,key,value,field): return [a[field] for t,a in self.tags if t==tag and a.get(key)==value and field in a]
    def metadata(self): return [(t,a) for t,a in self.tags if t in ('meta','link','title')]

def typed_spans(raw):
    start=raw.index('[',raw.index('"itemListElement"')); decoder=json.JSONDecoder(); items,end=decoder.raw_decode(raw,start); pos=start+1; spans=[]
    for unused in items:
        while raw[pos].isspace() or raw[pos]==',': pos+=1
        unused,end=decoder.raw_decode(raw,pos); spans.append(raw[pos:end]); pos=end
    return spans

def semantics(e,bodies,expected,results,baseline):
    rows={r['url']:r for r in e['rows']}; pages={u:Page(b) for u,b in bodies.items() if rows[u]['kind']=='html'}; links=[]; metadata=[]
    for url,page in pages.items():
        row=rows[url]; source=Page(expected[url]); need(page.metadata()==source.metadata() and page.scripts==source.scripts,'complete source head/schema metadata exact')
        need(page.values('link','rel','canonical','href')==[url],'canonical exact GET URL'); need(page.values('meta','property','og:url','content')==[url],'OG URL exact')
        need(not any('noindex' in v.lower() for v in page.values('meta','name','robots','content')),'public page indexable')
        if row['category']=='article':
            pdf=[r['url'] for r in e['rows'] if r['record']==row['record'] and r['kind']=='pdf']; need(len(pdf)==1 and page.values('meta','name','citation_pdf_url','content')==pdf,'original PDF citation URL')
        metadata.append({'url':url,'canonical':url,'whole_head_schema_source_equal':True,'HTML_fragment_IDs':sorted(page.ids)})
        for tag,a in page.tags:
            for attr in ('href','src','data'):
                raw=a.get(attr)
                if not raw: continue
                resolved=urljoin(url,raw); base,fragment=urldefrag(resolved); parts=urlsplit(base)
                if parts.scheme not in ('http','https') or parts.netloc!='aleckriebel.com':
                    links.append({'page':url,'tag':tag,'attribute':attr,'literal':raw,'resolved':resolved,'evidence':'EXTERNAL_OR_NON_HTTP_NOT_CONTACTED'}); continue
                need(parts.scheme=='https' and not parts.query,'HTTPS same-site link without unexpected query')
                if base in rows:
                    need(base in bodies and results[base]['PASS'],'in-scope linked response matched')
                    if fragment:
                        if rows[base]['kind']=='html': need(unquote(fragment) in pages[base].ids,'same-batch HTML fragment exists')
                        else: need(rows[base]['kind']=='pdf' and fragment=='view=FitH','literal PDF viewer parameter, not an HTML ID')
                    evidence='MATCHED23_HTTP_BODY;PDF_VIEW_PARAMETER_IS_NOT_READER_EVIDENCE' if fragment and rows[base]['kind']=='pdf' else 'MATCHED23_HTTP_BODY_AND_FRAGMENT_IF_PRESENT'
                else:
                    name=unquote(parts.path).lstrip('/'); name=(name+'index.html') if not name or name.endswith('/') else name
                    need(name in baseline['public_files'],'existing link belongs to frozen filesystem baseline')
                    if fragment:
                        if name.endswith('.html'):
                            q=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')/name; b=read(q); need(pin(b)=={k:baseline['public_files'][name][k] for k in ('bytes','SHA256')},'frozen linked HTML source'); need(unquote(fragment) in Page(b).ids,'existing source fragment')
                        else: need(name.endswith('.pdf') and fragment=='view=FitH','existing PDF viewer parameter')
                    evidence='FROZEN_SOURCE_CLOSURE_ONLY;NO_LIVE_GET_FOR_THIS_LINK'
                links.append({'page':url,'tag':tag,'attribute':attr,'literal':raw,'resolved':resolved,'evidence':evidence})
    index='https://aleckriebel.com/research/'; raw=bodies[index].decode(); visible=re.findall(r'<li\b[^>]*>[\s\S]*?</li>',raw)
    script=re.search(r'<script type="application/ld\+json">(.*?)</script>',raw,re.S)[1]; entity=json.loads(script)['mainEntity']
    nodes=re.findall(r'<url>[\s\S]*?</url>',bodies['https://aleckriebel.com/research/sitemap.xml'].decode())
    need(len(visible)==len(entity['itemListElement'])==entity['numberOfItems']==121 and len(nodes)==122,'actual121 index and122 sitemap counts')
    need(visible[:118]==baseline['visible_items_raw'] and typed_spans(script)[:118]==typed_spans(baseline['typed_script_complete_raw']) and nodes[:119]==baseline['sitemap_nodes_raw'],'old118 visible/typed and119 XML prefix units exact')
    return {'PASS':True,'whole_HTML_metadata':metadata,'resolved_links':links,'visible_index_items':121,'typed_index_items':121,'sitemap_nodes':122,'old_prefixes_exact':True,'HTTP_evidence_only_for23_URLs':True,'browser_PDF_mobile_native_SaveAs_or_download_certification':False}

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl): return None

def fetch(row,directory,opener):
    start=time.time(); receipt={'url':row['url'],'method':'GET','attempts':1,'status':None,'effective_URL':None,'header_fields_ordered':[],'body_complete':False,'errors':[]}; parts=[]; response=None
    try:
        request=Request(row['url'],headers={'Accept-Encoding':'identity'},method='GET')
        try: response=opener.open(request,timeout=30)
        except HTTPError as error: response=error; receipt['HTTPError_literal']=repr(error)
        receipt.update(status=response.status,reason=response.reason,http_version=getattr(response,'version',None),effective_URL=response.geturl(),header_fields_ordered=list(response.headers.raw_items()))
        write(directory/'headers.exposed.txt',response.headers.as_bytes())
        with response:
            while True:
                block=response.read(65536)
                if not block: break
                parts.append(block)
        lengths=response.headers.get_all('Content-Length',[]); need(len(lengths)<=1,'unambiguous Content-Length')
        if lengths: need(re.fullmatch('[0-9]+',lengths[0]) and int(lengths[0])==sum(map(len,parts)),'complete declared entity length')
        receipt['body_complete']=True
    except Exception as error:
        partial=getattr(error,'partial',b'')
        if isinstance(partial,bytes): parts.append(partial)
        receipt['errors'].append({'exception':repr(error),'traceback':traceback.format_exc()})
    received=b''.join(parts); write(directory/'body.received.bin',received); receipt['received_entity']=pin(received); decoded=None
    if response is not None:
        encoding=response.headers.get('Content-Encoding','identity').strip().lower(); receipt['content_encoding']=encoding
        try:
            need(len(response.headers.get_all('Content-Encoding',[]))<=1,'unambiguous content encoding')
            if encoding in ('','identity'): decoded=received
            elif encoding=='gzip': decoded=gzip.decompress(received)
            elif encoding=='deflate': decoded=zlib.decompress(received)
            else: raise ValueError('unsupported content encoding: '+encoding)
            write(directory/'body.decoded.bin',decoded); receipt['decoded_entity']=pin(decoded)
            content_type=response.headers.get_content_type(); charset=response.headers.get_content_charset(); receipt.update(content_type=content_type,charset=charset)
            need(receipt['body_complete'] and receipt['status']==200 and receipt['effective_URL']==row['url'],'whole direct canonical200 response')
            need(len(response.headers.get_all('Content-Type',[]))==1 and content_type in row['accepted_content_types'],'suitable unambiguous content type')
            if row['kind']=='html': need(all('noindex' not in v.lower() for v in response.headers.get_all('X-Robots-Tag',[])),'no HTTP noindex directive')
            if charset is not None and row['kind'] not in ('pdf','zip'): need(charset.lower() in ('utf-8','utf8') or (charset.lower()=='us-ascii' and all(c<128 for c in decoded)),'compatible declared charset')
            need(pin(decoded)=={k:row['source'][k] for k in ('bytes','SHA256')},'complete decoded body exact expected bytes')
        except Exception as error: receipt['errors'].append({'exception':repr(error),'traceback':traceback.format_exc()})
    receipt['elapsed_seconds']=time.time()-start; receipt['PASS']=not receipt['errors'] and decoded is not None and receipt['body_complete']; write(directory/'RECEIPT.json',packed(receipt)); return receipt,decoded

def main():
    need(sys.argv[1:] in ([],['--fetch']),'literal default or explicit single-run --fetch only')
    if not sys.argv[1:]: print(json.dumps({'status':'NO_ACTION_HTTP_GO_REQUIRED','network_calls':0,'repository_reads':0,'writes':0})); return
    need(Path(__file__).absolute()==N/'fetch_http23.py','fixed helper location'); raw=read(N/'SOURCE_EXPECTATIONS.json'); need(sha(raw)==EXPECT_SHA,'exact source expectations'); e=json.loads(raw)
    rows=e['rows']; need(len(rows)==len({r['url'] for r in rows})==23,'fixed23 inventory'); need(all(urlsplit(r['url']).scheme=='https' and urlsplit(r['url']).netloc=='aleckriebel.com' and not urlsplit(r['url']).query and not urlsplit(r['url']).fragment for r in rows),'finite ordinary canonical origin URLs')
    adoption=json.loads(bound(e['root_stage_adoption'])); need(adoption['status']=='ROOT_ADOPTED_PRIVATE_22_PATH_THREE_PAGE_STAGE' and adoption['production_install_Git_deploy_or_tracker_authority'] is False,'private stage authority only')
    need({r['website_relative_path'] for r in rows if r['category']!='existing CSS'}==set(adoption['candidate_exact_paths']),'same adopted22 plus CSS')
    expected={r['url']:bound(r['source']) for r in rows}; baseline=json.loads(bound(e['baseline'])); go_raw=read(N/'HTTP_GO.json'); go=json.loads(go_raw)
    fixed={'schema':'root-http23-single-run-v1','status':'ROOT_ACTUAL_DEPLOYMENT_HTTP23_GO','action':'GET_EXACT23_AFTER_FIREBASE_DEPLOYMENT','helper_SHA256':sha(read(N/'fetch_http23.py')),'expectations_SHA256':EXPECT_SHA,'root_stage_adoption':e['root_stage_adoption'],'attempts_per_URL':1,'automatic_retries':False,'automatic_redirects':False,'browser_or_reader_certification':False,'W_Git_source_Sheet_mutation_authority':False}
    need(set(go)==set(fixed)|{'hosting_version','deployment_receipt','issued_UTC','expires_UTC','nonce'} and all(go[k]==v for k,v in fixed.items()),'exact separate root deployment/HTTP GO')
    need(isinstance(go['hosting_version'],str) and go['hosting_version'] and '\n' not in go['hosting_version'],'actual root-bound Firebase version'); json.loads(bound(go['deployment_receipt']))
    issued=datetime.datetime.fromisoformat(go['issued_UTC']); expiry=datetime.datetime.fromisoformat(go['expires_UTC']); need(issued.utcoffset() is not None and expiry.utcoffset() is not None and re.fullmatch('[0-9a-f]{32}',go['nonce']),'qualified time and fresh nonce')
    def current(): need(issued<=utc()<expiry and read(N/'HTTP_GO.json')==go_raw and sha(read(N/'fetch_http23.py'))==go['helper_SHA256'] and sha(read(N/'SOURCE_EXPECTATIONS.json'))==EXPECT_SHA,'current exact HTTP authority/source edition')
    current(); write(N/'ACTIVE_HTTP.lock',packed({'GO_SHA256':sha(go_raw),'nonce':go['nonce'],'PID':os.getpid()})); parent=N/'runs'
    if not parent.exists(): parent.mkdir(mode=0o700); sync_dir(N)
    safe(parent); need(stat.S_IMODE(parent.lstat().st_mode)==0o700,'private run root'); run=parent/sha(go_raw); run.mkdir(mode=0o700); sync_dir(parent)
    write(run/'AUTHORITY.json',go_raw); write(run/'EXPECTATIONS.json',raw); opener=build_opener(NoRedirect()); results={}; bodies={}
    try:
        for row in rows:
            current(); directory=run/('%02d'%row['ordinal']); directory.mkdir(mode=0o700); sync_dir(run); result,decoded=fetch(row,directory,opener); results[row['url']]=result
            if decoded is not None: bodies[row['url']]=decoded
            print(json.dumps({'ordinal':row['ordinal'],'url':row['url'],'status':result['status'],'PASS':result['PASS']}),flush=True)
        current(); checks={'PASS':False,'reason':'One or more HTTP bodies/status/type/routing checks failed'}
        if all(r['PASS'] for r in results.values()): checks=semantics(e,bodies,expected,results,baseline)
        check_raw=packed(checks); write(run/'CHECKS.json',check_raw); final={'status':'PASS_EXACT23_HTTP_ONLY' if checks['PASS'] else 'FAIL_RETAINED_EXACT23_ATTEMPTS','hosting_version_from_root_GO':go['hosting_version'],'run':str(run),'attempted_URLs':len(results),'checks':{'path':'CHECKS.json',**pin(check_raw),'PASS':checks['PASS']},'no_retries_or_redirects':True,'browser_or_reader_download_certification':False,'AA':None,'follow_up':None}; write(run/'RESULT.json',packed(final)); print(json.dumps(final,ensure_ascii=False),flush=True)
        if not checks['PASS']: raise SystemExit(1)
    except Exception as error:
        write(run/'STOPPED.json',packed({'UTC':utc().isoformat(),'exception':repr(error),'traceback':traceback.format_exc(),'attempted_URLs':list(results),'unattempted_URLs':[r['url'] for r in rows if r['url'] not in results],'all_evidence_and_lock_retained':True})); raise

if __name__=='__main__':
    try: main()
    except Exception: traceback.print_exc(); raise SystemExit(1)
