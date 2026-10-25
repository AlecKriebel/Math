from pathlib import Path
from html.parser import HTMLParser
from io import BytesIO
from pypdf import PdfReader
import subprocess,json,hashlib,re,datetime,time
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');G=Path('/Users/alec/Documents/Math');O=P/'redirects/ambient-block-modulus-preflight-sol-20261025'
receipt=json.loads((O/'REMOTE_HTTPS_RECEIPT.json').read_text());PIN=receipt['body']['object']['sha'];START=time.time()
def git(*args,timeout=30):return subprocess.run(['git',*args],cwd=G,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,check=True).stdout
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
raw=git('ls-tree','-r','-l','--full-tree',PIN,'--','docs');(O/'docs-tree.raw.txt').write_bytes(raw)
rows=[]
for line in raw.decode().splitlines():
 head,path=line.split('\t',1);mode,kind,blob,size=head.split();rows.append({'path':path,'mode':mode,'type':kind,'blob':blob,'bytes':int(size)})
write('docs-tree.json',rows);tree=git('rev-parse',PIN+':docs').decode().strip()
queries=[
('97-title','Ambient Dependence of Extremal-Exchangeable Independence'),('98-title','An effective criterion for prescribed block-code extensions'),('99-title','Infinite modulus between a compact real set and its real complement'),('97-id','23333353'),('98-id','23416806'),('99-id','23441617'),
('97-extreme','extremal[-– ]exchangeable|extreme exchangeable'),('97-person','Liebscher|quantum independence'),('97-ambient','ambient dependence|ambient independence'),('97-freeproduct','exchangeab|free.product'),('97-loose','independence|ambient'),
('98-core','block[-– ]code|steadiness|sofic'),('98-import','van Rooijen|Zeitoun|LT.separ|locally testable'),('98-loose','block'),
('99-core','real complement|compact real set|Gon.?ar|7[.]58|Hayman|Lingham'),('99-modulus','conformal.*capacity|modulus'),('99-loose','capacity|modul')]
search=[]
for num,(label,term) in enumerate(queries,1):
 p=subprocess.run(['git','grep','-I','-n','-i','-E',term,PIN,'--','docs'],cwd=G,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=15)
 if p.returncode not in [0,1]:raise RuntimeError((term,p.stderr.decode()))
 name='search-%02d.txt'%num;(O/name).write_bytes(p.stdout);search.append({'label':label,'term':term,'returncode':p.returncode,'output':name,'bytes':len(p.stdout),'sha256':sha(p.stdout),'paths':sorted(set(x.split(':',2)[1] for x in p.stdout.decode(errors='replace').splitlines()))})
write('search-inventory.json',{'pin':PIN,'scope':'All tracked textual docs blobs via git grep -I -n -i -E; PDFs separately parsed.','queries':search})
class H(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.head=False;self.ignore=0;self.title=[];self.headings=[];self.current=None;self.text=[];self.meta=[];self.canonical=[];self.refs=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.stack.append(t)
  if t=='head':self.head=True
  if t in ['script','style','svg']:self.ignore+=1
  if t in ['h1','h2','h3']:self.current=[t,[]]
  if t=='meta':self.meta.append(a)
  if t=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
  for k in ['href','src','data']:
   if a.get(k):self.refs.append({'tag':t,'attribute':k,'value':a[k]})
 def handle_endtag(self,t):
  if t in ['h1','h2','h3'] and self.current:self.headings.append({'tag':self.current[0],'text':' '.join(''.join(self.current[1]).split())});self.current=None
  if t in ['script','style','svg']:self.ignore=max(0,self.ignore-1)
  if t=='head':self.head=False
  if t in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(t)]
 def handle_data(self,d):
  if not self.ignore:
   self.text.append(d)
   if self.head and 'title' in self.stack:self.title.append(d)
   if self.current:self.current[1].append(d)
core={
 '97':re.compile(r'extremal[-– ]exchangeable|extreme exchangeable|ambient dependence|ambient independence|Liebscher|quantum independence',re.I),
 '98':re.compile(r'block[-– ]code|steadiness|sofic|van Rooijen|Zeitoun|LT.separ|locally testable',re.I),
 '99':re.compile(r'real complement|compact real set|Gon.?ar|7[.]58|Hayman|Lingham|conformal.{0,30}capacity|modulus',re.I)}
loose=re.compile(r'exchangeab|free.product|independen|ambient|block|capacity|modul',re.I)
html=[];pdfs=[];texts=[];preserved=[];targets={}
for rid,pdf,tex,zipname in [('23333353','ambient_independence.pdf','published-source/ambient_independence_verification/ambient_independence.tex','verification_package.zip'),('23416806','paper.pdf','published-source/paper.tex','source-and-verification.zip'),('23441617','Real_Complement_Modulus_Note_v1.0.pdf','published-source/manuscript/main.tex','Real_Complement_Modulus_Verification_v1.0.zip')]:
 base=P/'papers'/rid/'sources';paths=[pdf,tex,zipname,'SOURCE_READY.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json'];targets[rid]={'inputs':[{'path':str((base/x).relative_to(P)),'bytes':(base/x).stat().st_size,'sha256':sha((base/x).read_bytes())} for x in paths],'PDF_pages':len(PdfReader(base/pdf).pages),'reader_sha256':sha((base/pdf).read_bytes())}
write('TARGET_CUSTODY.json',targets)
def hits(text,pat):return [{'match':m.group(),'context':text[max(0,m.start()-170):min(len(text),m.end()+240)]} for m in pat.finditer(text)]
for row in rows:
 path=row['path'];suffix=Path(path).suffix.lower()
 if suffix not in ['.html','.pdf','.xml','.txt','.md','.tex','.cff','.json','.css','.js','.yml','.yaml','.bib']:continue
 b=git('cat-file','blob',row['blob'])
 if len(b)!=row['bytes'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=row['blob']:raise ValueError(('blob identity',path))
 if suffix=='.pdf':
  doc=PdfReader(BytesIO(b));meta={str(k):str(v) for k,v in (doc.metadata or {}).items()};pagehits=[];characters=0
  for i,pg in enumerate(doc.pages):
   t=pg.extract_text() or '';characters+=len(t);ch={k:hits(t,v) for k,v in core.items()};lh=hits(t,loose)
   if any(ch.values()) or lh:pagehits.append({'PDF_page':i+1,'core_hits':ch,'loose_hits':lh})
  pdfs.append({**row,'sha256':sha(b),'PDF_pages':len(doc.pages),'extracted_characters':characters,'metadata':meta,'identical_target_readers':[rid for rid,x in targets.items() if x['reader_sha256']==sha(b)],'page_hits':pagehits})
  continue
 text=b.decode('utf-8',errors='replace');ch={k:hits(text,v) for k,v in core.items()};lh=hits(text,loose)
 if suffix=='.html':
  h=H();h.feed(text);visible=' '.join(' '.join(h.text).split());x={**row,'sha256':sha(b),'document_title':' '.join(''.join(h.title).split()),'headings':h.headings,'canonical':h.canonical,'metadata':h.meta,'reader_and_support_references':[v for v in h.refs if re.search(r'\.pdf(?:[?#]|$)|\.zip(?:[?#]|$)|\.tex(?:[?#]|$)|zenodo|doi[.]org',v['value'],re.I)],'all_references':h.refs,'core_hits':ch,'loose_hits':lh};html.append(x)
  if path=='docs/index.html':(O/'index-visible-text.txt').write_text(visible+'\n')
 if path in ['docs/index.html','docs/sitemap.xml']:
  dst=O/'legacy'/path.removeprefix('docs/');dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b);preserved.append({**row,'saved_as':str(dst.relative_to(O)),'sha256':sha(b)})
  if path=='docs/sitemap.xml':write('sitemap-urls.json',re.findall(r'<loc>\s*(.*?)\s*</loc>',text))
 texts.append({**row,'sha256':sha(b),'core_hits':ch,'loose_hits':lh})
write('html-identity-inventory.json',html);write('pdf-identity-inventory.json',pdfs);write('text-identity-inventory.json',texts);write('preserved-legacy-bindings.json',preserved)
write('CORPUS_RECEIPT.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fresh_remote_pin':PIN,'docs_tree':tree,'tracked_docs_files':len(rows),'html_files':len(html),'pdf_files':len(pdfs),'PDF_pages':sum(x['PDF_pages'] for x in pdfs),'PDF_text_empty':[x['path'] for x in pdfs if not x['extracted_characters']],'identical_target_PDFs':[(x['path'],x['identical_target_readers']) for x in pdfs if x['identical_target_readers']],'elapsed_seconds':time.time()-START,'preserved_legacy_bytes':sum(x['bytes'] for x in preserved),'method':'All cached Git blobs inspected read-only; only index/sitemap exact bytes saved. PDF text extraction/search is machine inventory, not full human reading.'})
print(json.dumps(json.loads((O/'CORPUS_RECEIPT.json').read_text()),indent=2))
print('HTML_IDENTITIES')
for x in html:print(x['path'],'|',x['document_title'],'|',[v['text'] for v in x['headings'] if v['tag']=='h1'])
print('CORE_MATCHES')
for x in pdfs:
 for p in x['page_hits']:
  for k,h in p['core_hits'].items():
   if h:print(x['path'],'PDF',p['PDF_page'],k,h)
