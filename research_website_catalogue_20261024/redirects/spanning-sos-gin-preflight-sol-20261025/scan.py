"""Read exact cached objects of a freshly verified remote pin; no Git writes."""
from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,io,json,os,re,subprocess,xml.etree.ElementTree as ET
from pypdf import PdfReader

O=Path(__file__).resolve().parent;P=O.parents[1];G=P.parent;C=O/'tmp/cache';PIN='d216ab770e26ca8042adb2070c314d2a30b5b9c5';OLD='fcef024e7fec5def93bbc716f33d856f6a93c8af'
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def git(*args):return subprocess.check_output(['git',*args],cwd=G,env=ENV)
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,obj):(O/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def blob(path):return git('show',PIN+':'+path)
def item(p):b=p.read_bytes();return {'path':str(p),'bytes':len(b),'SHA256':sha(b)}
def checkpoint(text,percent):
    with (O/'RESEARCH_LOG.md').open('a') as f:f.write('* '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — '+text+' Completion estimate '+str(percent)+'%.\n')

class HTML(HTMLParser):
    def __init__(self,text):super().__init__();self.meta=[];self.links=[];self.frames=[];self.parts=[];self.title=[];self.h1=[];self.in_title=False;self.in_h1=False;self.skip=0;self.feed(text)
    def handle_starttag(self,t,a):
        d=dict(a)
        if t=='title':self.in_title=True
        if t=='h1':self.in_h1=True
        if t=='meta':self.meta.append(d)
        if t in ['a','link']:self.links.append(d)
        if t in ['iframe','embed','object']:self.frames.append(d)
        if t in ['script','style']:self.skip+=1
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip-=1
        if t=='title':self.in_title=False
        if t=='h1':self.in_h1=False
    def handle_data(self,x):
        if self.in_title:self.title.append(x)
        if self.in_h1:self.h1.append(x)
        if not self.skip:self.parts.append(x)

def main():
    O.mkdir(parents=True,exist_ok=True)
    if (O/'protected-before.json').exists():raise RuntimeError('initial_custody_already_exists')
    ignore=git('check-ignore','-v',str(C/'probe.txt')).decode();C.mkdir(parents=True,exist_ok=True)
    (O/'cache-ignore-receipt.txt').write_text(ignore)
    remote=git('ls-remote','--exit-code','origin','refs/heads/main').decode();assert remote.split()[0]==PIN
    (O/'remote-main-start.txt').write_text(remote)
    assert git('cat-file','-t',PIN).strip()==b'commit'
    revision={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remote_url':git('remote','get-url','origin').decode().strip(),'pinned_remote_main':PIN,'cached_origin_main':git('rev-parse','refs/remotes/origin/main').decode().strip(),'local_HEAD':git('rev-parse','HEAD').decode().strip(),'pinned_docs_tree':git('rev-parse',PIN+':docs').decode().strip(),'no_fetch_or_checkout_required':True,'git_optional_locks':'0','fresh_ls_remote_bytes_SHA256':sha(remote.encode())}
    save('REMOTE_PIN.json',revision)
    raw=git('ls-tree','-r','-l',PIN,'--','docs');(O/'docs-tree.raw.txt').write_bytes(raw)
    entries=[]
    for line in raw.decode().splitlines():
        fields,path=line.split('\t',1);mode,kind,oid,size=fields.split();entries.append({'path':path,'mode':mode,'type':kind,'git_blob':oid,'bytes':int(size)})
    save('docs-tree.json',{'pin':PIN,'tree':revision['pinned_docs_tree'],'entries':entries})
    delta=git('diff-tree','--no-commit-id','--name-status','-r',OLD,PIN,'--','docs').decode();(O/'delta-from-prior-pin.txt').write_text(delta)
    protected=set()
    for base in [G/'docs',Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')]:protected.update(p for p in base.rglob('*') if p.is_file())
    for rid in ['23181280','23442760','23395703']:
        base=P/'papers'/rid;protected.update(p for p in base.rglob('*') if p.is_file() and not {'tmp','cache','__pycache__'}&set(p.relative_to(base).parts))
    protected.update(p for p in (P/'scripts').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    protected.add(P/'verification/final-content-check.py')
    stage=P/'verification/local-cylinder-discotope-stage-sol-20261025';protected.update(p for p in stage.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    for name in ['.git/HEAD','.git/index','.git/config','.git/packed-refs','.git/refs/heads/main','.git/refs/remotes/origin/main']:
        if (G/name).is_file():protected.add(G/name)
    for name in ['firebase.json','.firebaserc']:
        p=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')/name
        if p.is_file():protected.add(p)
    save('protected-before.json',{'UTC':revision['UTC'],'scope':'Before this preflight: actual docs working tree, whole production public, current3 source/review/config packages, current core, prior sealed2stage, Git state bytes and Firebase.','files':[item(p) for p in sorted(protected)]})
    checkpoint('Fresh remote pin authenticated; exact cached blob tree will control, regardless of working-tree staleness. Ignored cache verified before body writes; original protected bytes bound.',10)
    targets={
     '23181280':('root_dependent_spanning_trees.pdf','published-source/source_preparation/root_dependent_spanning_trees.tex'),
     '23442760':('Convex_Body_SOS_Density_Note_v1.0.pdf','published-source/manuscript/main.tex'),
     '23395703':('seven_plane_gin.pdf','seven_plane_gin.tex')}
    identities=[]
    for rid,(pdf,tex) in targets.items():
        s=P/'papers'/rid/'sources';reader=PdfReader(s/pdf);texts=[p.extract_text() or '' for p in reader.pages];text='\n\f\n'.join(texts)
        (C/('current-'+rid+'.txt')).write_text(text)
        identities.append({'record_id':rid,'PDF':item(s/pdf),'pages':len(reader.pages),'extracted_chars_by_page':[len(t) for t in texts],'controlling_TeX':item(s/tex),'source_ready':item(s/'SOURCE_READY.json'),'source_ready_seal':item(s/'SOURCE_READY_SEAL.json'),'actual_full_PDF_text_path':str(C/('current-'+rid+'.txt')),'title':json.loads((s/'SOURCE_READY.json').read_text())['title']})
    save('CURRENT_IDENTITIES.json',{'targets':identities})
    queries={
     'spanning_record_or_title':r'23181280|NP.completeness of aggregate root.dependent spanning.tree cost|root.dependent.spanning',
     'spanning_core':r'Kaibel|arborescenc|spanning.tree|root.dependent|aggregate.root|entire.rooted',
     'SOS_record_or_title':r'23442760|Quadratic convergence of SOS.density|SOS.density',
     'SOS_core':r'Lasserre|Slot.{0,20}Laurent|de.Klerk|sum.of.squares|sum.of.squares.density|convex.bod|Dirichlet.polynomial',
     'GIN_record_or_title':r'23395703|seven.hyperplane|generic.initial.degree|seven.plane.gin',
     'GIN_core':r'generic.initial|Bigatti|Palezzato|Torielli|Jacobian.ideal|Hilbert.Burch|hyperplane.arrangement',
     'GIN_factor':r'xy.{0,8}\(x.y\).{0,8}\(x.2y\)|pure.second.variable|cutoff.8'}
    compiled={q:re.compile(regex,re.I) for q,regex in queries.items()}
    text_inventory=[];html_inventory=[];searches={q:[] for q in queries};seen_text={}
    for entry in entries:
        path=entry['path']
        if Path(path).suffix.lower() not in ['.html','.xml','.json','.tex','.md','.txt','.cff','.py','.css']:continue
        data=blob(path)
        try:body=data.decode('utf-8')
        except UnicodeDecodeError:continue
        hits={q:[{'line':body.count('\n',0,m.start())+1,'matched':m.group(0)} for m in rx.finditer(body)] for q,rx in compiled.items()};hits={q:x for q,x in hits.items() if x}
        text_inventory.append({**entry,'SHA256':sha(data),'UTF8_chars':len(body),'query_hits':hits})
        for q,x in hits.items():searches[q].append({'path':path,'matches':x})
        if path.endswith('.html'):
            h=HTML(body);visible=' '.join(' '.join(h.parts).split());seen_text[path]=visible
            html_inventory.append({**entry,'SHA256':sha(data),'title':' '.join(h.title),'h1':' '.join(h.h1),'canonical_links':[x.get('href') for x in h.links if x.get('rel')=='canonical'],'meta':h.meta,'reader_references':h.frames,'PDF_links':[x.get('href') for x in h.links if '.pdf' in x.get('href','')],'body_query_hits':{q:len(list(rx.finditer(visible))) for q,rx in compiled.items() if rx.search(visible)}})
            if path=='docs/index.html':(C/'pinned-index.html').write_bytes(data);(C/'pinned-index-visible.txt').write_text(visible)
        if path=='docs/sitemap.xml':(C/'pinned-sitemap.xml').write_bytes(data)
    save('text-inventory.json',{'pin':PIN,'queries':queries,'documents':text_inventory});save('search-results.json',{'pin':PIN,'queries':queries,'results':searches});save('html-identity-inventory.json',{'pin':PIN,'documents':html_inventory})
    xml=ET.fromstring(blob('docs/sitemap.xml'));urls=[e.text for e in xml.iter() if e.tag.endswith('loc')];save('sitemap-URLs.json',{'pin':PIN,'URLs':urls})
    current_hashes={x['PDF']['SHA256']:x['record_id'] for x in identities};pdfs=[]
    for entry in entries:
        if not entry['path'].lower().endswith('.pdf'):continue
        data=blob(entry['path']);record={**entry,'SHA256':sha(data),'same_bytes_as_current':current_hashes.get(sha(data))}
        try:
            reader=PdfReader(io.BytesIO(data));texts=[p.extract_text() or '' for p in reader.pages];body='\n\f\n'.join(texts)
            record.update(pages=len(reader.pages),extracted_chars_by_page=[len(x) for x in texts],PDF_metadata={str(k):str(v) for k,v in (reader.metadata or {}).items()},first_page_identity_prefix=' '.join(texts[0].split())[:250] if texts else '',query_hits={q:[{'page':i+1,'matches':[m.group(0) for m in rx.finditer(t)]} for i,t in enumerate(texts) if rx.search(t)] for q,rx in compiled.items() if rx.search(body)})
            if record['query_hits'] or record['same_bytes_as_current']:
                key=entry['path'].replace('/','__');(C/(key+'.full-text.txt')).write_text(body)
                record['ignored_full_text_cache_path']=str(C/(key+'.full-text.txt'))
        except Exception as e:record['extraction_error']=type(e).__name__+':'+str(e)
        pdfs.append(record)
    save('pdf-identity-inventory.json',{'pin':PIN,'coverage':'Automated extraction/search and byte identity of all tracked PDFs; not a full human reading of all foreign pages.','documents':pdfs})
    checkpoint('Actual current3 full manuscript text and controlling TeX identified; exact pinned HTML/XML/text and all PDF byte/text inventories acquired. Candidate classification and actual-body reading remain.',65)
    print(json.dumps({'pin':PIN,'tracked_docs':len(entries),'HTML':len(html_inventory),'PDF':len(pdfs),'PDF_pages_machine_extracted':sum(x.get('pages',0) for x in pdfs),'PDF_errors':[x for x in pdfs if 'extraction_error' in x],'text_documents':len(text_inventory),'text_hit_paths':{q:[x['path'] for x in v] for q,v in searches.items()},'PDF_hit_paths':{x['path']:list(x.get('query_hits',{})) for x in pdfs if x.get('query_hits')},'exact_PDF_matches':[x['path'] for x in pdfs if x['same_bytes_as_current']]},indent=2))

if __name__=='__main__':main()
