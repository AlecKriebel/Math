"""One root-authorized fixed16 ordinary GET route; default performs no action."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urldefrag, unquote
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError
import datetime, gzip, hashlib, json, re, stat, sys, traceback, zlib

N=Path(__file__).resolve().parent
EXPECT_SHA='cd2ad4f0447e8592913e216d426cedcc6f0ab9ef341e65e1653d876d5948116b'

def need(ok,message):
    if not ok:raise ValueError(message)
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def packed(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def read(p):
    need(p.is_absolute() and not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode),'Regular local input: '+str(p))
    return p.read_bytes()
def write(p,b):
    need(p.is_relative_to(N),'Owned output only')
    with p.open('xb') as f:f.write(b)

class Page(HTMLParser):
    def __init__(self,b):
        super().__init__(convert_charrefs=True);self.tags=[];self.ids=set();self.script=None;self.scripts=[];self.abstract=[];self.active=False;self.feed(b.decode('utf-8'));self.close()
    def handle_starttag(self,t,attrs):
        a=dict(attrs);self.tags.append((t,a))
        if a.get('id'):need(a['id'] not in self.ids,'Unique fragment IDs');self.ids.add(a['id'])
        if a.get('id')=='original-abstract':self.active=True
        if t=='script' and a.get('type')=='application/ld+json':self.script=[]
    def handle_data(self,d):
        if self.active:self.abstract.append(d)
        if self.script is not None:self.script.append(d)
    def handle_endtag(self,t):
        if t=='p' and self.active:self.active=False
        if t=='script' and self.script is not None:self.scripts.append(json.loads(''.join(self.script)));self.script=None
    def values(self,t,k,v,field):return [a[field] for tag,a in self.tags if tag==t and a.get(k)==v and field in a]

def typed_spans(script):
    pos=script.index('[',script.index('"itemListElement"'));d=json.JSONDecoder();items,end=d.raw_decode(script,pos);pos+=1;out=[]
    for item in items:
        while script[pos].isspace() or script[pos]==',':pos+=1
        item,end=d.raw_decode(script,pos);out.append(script[pos:end]);pos=end
    return out

def local_inputs(e):
    out={};W=Path(e['website_root']);S=Path(e['stage_root'])
    for r in e['rows']:
        expected={k:r[k] for k in ('bytes','SHA256')};w=read(W/r['path']);need(pin(w)==expected,'Installed target exact: '+r['path'])
        s=w if r['category']=='existing CSS' else read(S/r['path'])
        need(pin(s)==expected,'Adopted stage exact: '+r['path']);out[r['url']]=s
    return out

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None

def fetch(r,directory,opener):
    receipt={'URL':r['url'],'method':'GET','attempts':1,'status':None,'effective_URL':None,'header_fields_ordered':[],'body_complete':False,'errors':[]}
    chunks=[];response=None;decoded=None
    try:
        request=Request(r['url'],headers={'Accept-Encoding':'identity'},method='GET')
        try:response=opener.open(request,timeout=30)
        except HTTPError as error:response=error;receipt['HTTPError_literal']=repr(error)
        receipt.update(status=response.status,reason=response.reason,effective_URL=response.geturl(),http_version=getattr(response,'version',None),header_fields_ordered=list(response.headers.raw_items()))
        write(directory/'headers.exposed.txt',response.headers.as_bytes())
        with response:
            while True:
                block=response.read(65536)
                if not block:break
                chunks.append(block);need(sum(map(len,chunks))<=max(2097152,2*r['bytes']),'Bounded response entity')
        length=response.headers.get_all('Content-Length',[]);need(len(length)<=1,'Unambiguous Content-Length')
        if length:need(re.fullmatch('[0-9]+',length[0]) and int(length[0])==sum(map(len,chunks)),'Complete declared length')
        receipt['body_complete']=True
    except Exception as error:
        partial=getattr(error,'partial',b'')
        if isinstance(partial,bytes):chunks.append(partial)
        receipt['errors'].append({'exception':repr(error),'traceback':traceback.format_exc()})
    received=b''.join(chunks);write(directory/'body.received.bin',received);receipt['received']=pin(received)
    if response is not None:
        try:
            encoding=response.headers.get('Content-Encoding','identity').strip().lower();receipt['content_encoding']=encoding
            need(len(response.headers.get_all('Content-Encoding',[]))<=1,'Unambiguous encoding')
            if encoding in ('','identity'):decoded=received
            elif encoding=='gzip':decoded=gzip.decompress(received)
            elif encoding=='deflate':decoded=zlib.decompress(received)
            else:raise ValueError('Unsupported Content-Encoding '+encoding)
            write(directory/'body.decoded.bin',decoded);receipt['decoded']=pin(decoded)
            content_type=response.headers.get_content_type();receipt['content_type']=content_type;receipt['charset']=response.headers.get_content_charset()
            need(receipt['body_complete'] and receipt['status']==200 and receipt['effective_URL']==r['url'],'Direct complete canonical 200')
            need(len(response.headers.get_all('Content-Type',[]))==1 and content_type in r['types'],'Suitable unambiguous MIME')
            charset=receipt['charset']
            if charset and r['kind'] not in ('pdf','zip'):need(charset.lower() in ('utf-8','utf8') or (charset.lower()=='us-ascii' and all(c<128 for c in decoded)),'Compatible declared text charset')
            need(all(not re.search(r'\b(noindex|nofollow|none)\b',v,re.I) for v in response.headers.get_all('X-Robots-Tag',[])),'Crawlable response headers')
            need(pin(decoded)=={k:r[k] for k in ('bytes','SHA256')},'Whole decoded body exact')
        except Exception as error:receipt['errors'].append({'exception':repr(error),'traceback':traceback.format_exc()})
    receipt['PASS']=not receipt['errors'] and decoded is not None and receipt['body_complete']
    write(directory/'RECEIPT.json',packed(receipt));return receipt,decoded

def semantics(e,bodies,expected):
    rows={r['url']:r for r in e['rows']};pages={u:Page(b) for u,b in bodies.items() if rows[u]['kind']=='html'};links=[];metadata=[]
    for url,page in pages.items():
        source=Page(expected[url]);need(page.tags==source.tags and page.scripts==source.scripts,'Whole parsed HTML metadata/schema/source equality')
        need(page.values('link','rel','canonical','href')==[url] and page.values('meta','property','og:url','content')==[url],'Canonical and OG exact')
        for tag,a in page.tags:
            if tag=='meta' and a.get('name','').lower() in ('robots','googlebot','bingbot'):
                need(not re.search(r'\b(noindex|nofollow|none)\b',a.get('content',''),re.I),'No HTML noindex/nofollow')
        if rows[url]['category']=='article':
            entity=next(s for s in page.scripts if s.get('@type')=='ScholarlyArticle')
            need(''.join(page.abstract)==page.values('meta','name','DC.description','content')[0]==entity['abstract']==''.join(source.abstract),'Complete visible/schema/DC abstract')
            pdf=[r['url'] for r in e['rows'] if r['record']==rows[url]['record'] and r['kind']=='pdf']
            need(page.values('meta','name','citation_pdf_url','content')==pdf,'Original PDF citation exact')
            need(entity['url']==entity['mainEntityOfPage']==url and entity['@id']==url+'#article','Scholarly canonical identity')
        metadata.append({'URL':url,'head_schema_abstract_source_exact':True,'IDs':sorted(page.ids)})
        for tag,a in page.tags:
            for attr in ('href','src','data'):
                if not a.get(attr):continue
                resolved=urljoin(url,a[attr]);base,fragment=urldefrag(resolved);u=urlsplit(base)
                if u.scheme not in ('http','https') or u.netloc!='aleckriebel.com':
                    evidence='EXTERNAL_OR_NON_HTTP_NOT_REQUESTED'
                elif base in rows:
                    need(base in bodies,'In-scope local response present')
                    if fragment:
                        need((rows[base]['kind']=='html' and unquote(fragment) in pages[base].ids) or (rows[base]['kind']=='pdf' and fragment=='view=FitH'),'Local fragment or PDF view hint')
                    evidence='MATCHED_FIXED_HTTP_BODY;PDF_HINT_IS_NOT_READER_EVIDENCE'
                else:
                    need(u.scheme=='https' and not u.query,'Same-site HTTPS ordinary reference')
                    name=unquote(u.path).lstrip('/');name=name+'index.html' if not name or name.endswith('/') else name
                    p=Path(e['website_root'])/name;need(p.is_relative_to(Path(e['website_root'])) and '..' not in p.parts,'Local source reference scope');b=read(p)
                    if fragment:need(name.endswith('.html') and unquote(fragment) in Page(b).ids,'Existing source fragment')
                    evidence='EXISTING_LOCAL_SOURCE_ONLY;NO_EXTRA_LIVE_GET'
                links.append({'page':url,'literal':a[attr],'resolved':resolved,'evidence':evidence})
    index='https://aleckriebel.com/research/';sitemap='https://aleckriebel.com/research/sitemap.xml'
    def units(b):
        raw=b.decode();script=re.search(r'<script type="application/ld\+json">(.*?)</script>',raw,re.S)[1]
        return re.findall(r'<li\b[^>]*>[\s\S]*?</li>',raw),typed_spans(script),json.loads(script)['mainEntity']
    visible,typed,entity=units(bodies[index]);old_visible,old_typed,unused=units(expected[index])
    nodes=re.findall(r'<url>[\s\S]*?</url>',bodies[sitemap].decode());old_nodes=re.findall(r'<url>[\s\S]*?</url>',expected[sitemap].decode())
    need(len(visible)==len(typed)==entity['numberOfItems']==len(entity['itemListElement'])==123 and len(nodes)==124,'123 index and124 sitemap counts')
    need(visible[:121]==old_visible[:121] and typed[:121]==old_typed[:121] and nodes[:122]==old_nodes[:122],'Adopted old raw121/122 prefixes exact')
    return {'PASS':True,'metadata':metadata,'links':links,'index':123,'sitemap':124,'old121_visible_typed_and122_XML_prefix_exact':True,'browser_native_reader_mobile_SaveAs_download_or_AA_certificate':False}

def main():
    need(sys.argv[1:] in ([],['--fetch']),'Literal no-action default or explicit --fetch only')
    if not sys.argv[1:]:print(json.dumps({'status':'NO_ACTION_ROOT_LIVE_GO_REQUIRED','network':0,'writes':0}));return
    raw=read(N/'EXPECTED.json');need(hashlib.sha256(raw).hexdigest()==EXPECT_SHA,'Exact fixed expectations')
    e=json.loads(raw);rows=e['rows'];need(len(rows)==len({r['url'] for r in rows})==16,'Fixed sixteen URLs')
    need(e['deployment_version_from_root']=='projects/261930987155/sites/aleckriebel-bd92e/versions/250cf0666d1a3ba6' and e['website_commit_from_root']=='b767102567ad89aff909f9f11c0e8b7d72b75c40','Actual root deployment identity')
    need(all(urlsplit(r['url']).scheme=='https' and urlsplit(r['url']).netloc=='aleckriebel.com' and not urlsplit(r['url']).query and not urlsplit(r['url']).fragment for r in rows),'Only finite canonical origin GETs')
    expected=local_inputs(e);run=N/'run';run.mkdir(mode=0o700);write(run/'EXPECTED.json',raw)
    opener=build_opener(NoRedirect());bodies={};results=[]
    try:
        for i,r in enumerate(rows,1):
            need(read(N/'EXPECTED.json')==raw,'Expectations unchanged');directory=run/('%02d'%i);directory.mkdir(mode=0o700)
            receipt,decoded=fetch(r,directory,opener);results.append(receipt)
            print(json.dumps({'ordinal':i,'URL':r['url'],'status':receipt['status'],'PASS':receipt['PASS']}),flush=True)
            need(receipt['PASS'],'Stop at first failed response; no retry')
            bodies[r['url']]=decoded
        checks=semantics(e,bodies,expected);need(local_inputs(e)==expected,'Scoped source/W sixteen buffers unchanged')
        write(run/'CHECKS.json',packed(checks));write(run/'RESULT.json',packed({'status':'PASS_FIXED16_HTTP_ONLY','deployment_version_from_root':e['deployment_version_from_root'],'attempts':16,'all_whole_bodies_exact':True,'browser_reader_mobile_download_or_AA_certification':False}));print(json.dumps({'status':'PASS_FIXED16_HTTP_ONLY','responses':16}),flush=True)
    except Exception as error:
        write(run/'STOPPED.json',packed({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exception':repr(error),'traceback':traceback.format_exc(),'attempted':[r['URL'] for r in results],'unattempted':[r['url'] for r in rows[len(results):]],'all_partial_evidence_retained':True}));raise

if __name__=='__main__':
    try:main()
    except Exception:traceback.print_exc();raise SystemExit(1)
