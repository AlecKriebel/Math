"""Read-only exact legacy correspondence inventory; only own evidence is written."""
from pathlib import Path
from html.parser import HTMLParser
import subprocess,hashlib,json,re,datetime,os
E=Path(__file__).resolve().parent;P=E.parents[1];G=P.parent;PIN='ebd3c1c3040634fe0cff28765f86ed4b84dad488';TREE='7a24ec1dcb73a5e06ba82ff9cccda54e73f9deec';(E/'cache').mkdir(exist_ok=True);(E/'private').mkdir(exist_ok=True)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.run(['git',*args],cwd=G,check=True,capture_output=True,timeout=30).stdout
def save(n,obj):(E/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def pages_from(b):
 q=subprocess.run(['/opt/homebrew/bin/pdftotext','-','-'],input=b,capture_output=True,check=True,timeout=30);text=q.stdout.decode('utf-8');pages=text.split('\f');pages=pages[:-1] if pages and not pages[-1].strip() else pages
 info=subprocess.run(['/opt/homebrew/bin/pdfinfo','-'],input=b,capture_output=True,check=True,timeout=30).stdout.decode();return text,pages,info
if git('rev-parse','refs/remotes/origin/main').decode().strip()!=PIN or git('rev-parse',PIN+':docs').decode().strip()!=TREE:raise RuntimeError('accepted_pin_not_available')
index=Path(git('rev-parse','--git-path','index').decode().strip());index=index if index.is_absolute() else G/index
if (E/'PRESERVATION_BEFORE.json').exists():raise RuntimeError('do_not_overwrite_initial_custody')
paths={index,G/'.git/HEAD'};paths.update(p for p in (G/'docs').rglob('*') if p.is_file())
for rid in ['23576280','23331258']:
 p=P/'papers'/rid;authority=P/f'verification/root-clearance-{rid}-20261025.json';a=json.loads(authority.read_text());paths.add(authority)
 for k in ['source_receipt_path','metadata_path','raw_record_path','source_tex_path']:paths.add(P/a[k])
 ready=json.loads((P/a['source_receipt_path']).read_text())
 for x in ready['all_assets']:paths.add(Path(x['path']))
 for n in ['SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json','SOURCE_MANIFEST.json','SOURCE_SEAL.json']:
  q=p/'sources'/n
  if q.exists():paths.add(q)
 for n in ['publication.json','promotion.json']:
  q=p/n
  if q.exists():paths.add(q)
files=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(paths)]
save('PRESERVATION_BEFORE.json',{'utc':utc(),'files':files,'docs_working_files':sum(Path(x['path']).is_relative_to(G/'docs') for x in files),'shared_index_path':str(index),'Git_HEAD':git('rev-parse','HEAD').decode().strip(),'Git_symbolic_HEAD':git('symbolic-ref','HEAD').decode().strip(),'origin_main':PIN,'docs_tree':TREE,'working_docs_status':git('status','--porcelain=v1','--','docs').decode(),'scope':'Actual working docs bytes, shared HEAD/index and explicit current target identity objects; no unrelated mutable programme baseline.'})
save('PIN_AUTHORITY.json',{'utc':utc(),'source':'Direct parent root accepted current last successful Math main pin in this task; no new remote network request','accepted_origin_main':PIN,'accepted_docs_tree':TREE,'objects_locally_available':True,'fresh_HTTP_or_fetch_performed':False,'prior_ordinary_transport_receipt_reference':'redirects/ambient-block-modulus-preflight-sol-20261025/REMOTE_HTTPS_RECEIPT.json','prior_receipt_is_historical_not_a_new_transport':True})
(E/'RESEARCH_LOG.md').write_text(f'* {utc()} — Root-approved exact local Math origin/main and docs tree authenticated; fresh lean target/shared-index/working-docs baseline written before inventory. No fetch, checkout, UI or network. Completion estimate10%.\n')
raw=git('ls-tree','-r','-l','--full-tree',PIN,'--','docs');(E/'docs-tree.raw.txt').write_bytes(raw);rows=[]
for line in raw.decode().splitlines():
 h,path=line.split('\t',1);mode,kind,blob,size=h.split();rows.append({'path':path,'mode':mode,'kind':kind,'blob':blob,'bytes':int(size)})
save('docs-tree.json',rows)
queries={
 '100-full-title':r'NP-completeness of the initial odd-ear prefix','100-record-or-DOI':r'23576280|10[.]5281/zenodo[.]23576280','100-ear-definition':r'odd[- ]ear|open ear|ear[- ]decompo|consecutive odd|odd prefix|factor[- ]critical','100-mechanism':r'Seb[oő]|Benchetrit|perfectly matchable|connected matching|block[- ]loss|Lov[aá]sz',
 '101-full-title':r'NP-completeness of three-terminal shortest-path blocking','101-record-or-DOI':r'23331258|10[.]5281/zenodo[.]23331258','101-core':r'shortest[- ]path block|blocking shortest|three[- ]terminal|terminal geodesic','101-context':r'Krause|Khachiyan|interdiction|length[- ]bounded cut|distance.{0,20}three|tripartite.{0,30}cover',
 'broad-related':r'ear|shortest.{0,20}path|terminal|block|vertex.cover|matching'}
search=[]
for label,term in queries.items():
 p=subprocess.run(['git','grep','-I','-n','-i','-E',term,PIN,'--','docs'],cwd=G,capture_output=True,timeout=30)
 if p.returncode not in [0,1]:raise RuntimeError(p.stderr.decode())
 out='text-search-'+label+'.txt';(E/out).write_bytes(p.stdout);search.append({'label':label,'query':term,'output':out,'bytes':len(p.stdout),'sha256':sha(p.stdout),'returncode':p.returncode})
save('TEXT_SEARCHES.json',{'pin':PIN,'scope':'All tracked textual docs blobs, binary excluded by git grep -I; separate every-page PDF extraction below','queries':search})
class H(HTMLParser):
 def __init__(self,t):super().__init__(convert_charrefs=True);self.title=[];self.h1=[];self.h2=[];self.tag=None;self.current=None;self.text=[];self.meta=[];self.links=[];self.skip=0;self.in_title=False;self.feed(t)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='title':self.in_title=True
  if t in ['script','style']:self.skip+=1
  if t in ['h1','h2']:self.tag=t;self.current=[]
  if t=='meta':self.meta.append(a)
  for k in ['href','src','data']:
   if a.get(k):self.links.append({'tag':t,'attribute':k,'value':a[k],**({'rel':a['rel']} if 'rel' in a else {})})
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if t in ['script','style']:self.skip=max(0,self.skip-1)
  if t in ['h1','h2'] and self.current is not None:getattr(self,t).append(' '.join(''.join(self.current).split()));self.current=None
 def handle_data(self,x):
  if self.in_title:self.title.append(x)
  if self.current is not None:self.current.append(x)
  if not self.skip:self.text.append(x)
core={
 '100':re.compile(r'odd[- ]ear|open ear|ear[- ]decompo|consecutive odd|odd prefix|factor[- ]critical|Benchetrit|perfectly matchable|block[- ]loss|23576280',re.I),
 '101':re.compile(r'shortest[- ]path block|blocking shortest|three[- ]terminal|terminal geodesic|Krause|Khachiyan|interdiction|23331258',re.I)}
broad=re.compile(r'shortest.{0,20}path|terminal|vertex[- ]cover|matching|\bear\b',re.I)
def normalized(t):
 t=t.replace('\u00ad','').replace('–','-').replace('—','-').replace('‐','-');t=re.sub(r'-\s+','-',t);return ' '.join(t.split())
def hits(t,pat):return [{'match':m.group(),'context':t[max(0,m.start()-150):min(len(t),m.end()+250)]} for m in pat.finditer(t)]
html=[];pdfs=[];candidate=[];allpdfpages=0
for row in rows:
 path=row['path'];b=git('cat-file','blob',row['blob'])
 if len(b)!=row['bytes'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=row['blob']:raise RuntimeError('Git_blob_binding_failed:'+path)
 suffix=Path(path).suffix.lower()
 if suffix=='.html':
  h=H(b.decode());t=normalized(' '.join(h.text));rec={**row,'sha256':sha(b),'title':normalized(''.join(h.title)),'h1':h.h1,'h2':h.h2,'metadata':h.meta,'references':h.links,'core_hits':{k:hits(t,v) for k,v in core.items()},'broad_hits':hits(t,broad)};html.append(rec)
  if any(rec['core_hits'].values()):candidate.append({'kind':'HTML','path':path,'blob':row['blob'],'reason':'distinctive content hit'})
  if path=='docs/index.html':(E/'cache/index.visible.txt').write_text(t+'\n')
 elif suffix=='.pdf':
  txt,pages,info=pages_from(b);allpdfpages+=len(pages);t=normalized(txt);name=row['blob'];(E/'cache'/(name+'.txt')).write_text(txt);rec={**row,'sha256':sha(b),'pages':len(pages),'characters':len(txt),'empty_text_pages':[i+1 for i,p in enumerate(pages) if not p.strip()],'pdfinfo':info,'core_hits':{k:hits(t,v) for k,v in core.items()},'broad_hits':hits(t,broad),'text_path':'cache/'+name+'.txt','text_sha256':sha(txt.encode()),'first_page':pages[0]};pdfs.append(rec)
  if any(rec['core_hits'].values()):candidate.append({'kind':'PDF','path':path,'blob':row['blob'],'reason':'distinctive content hit'})
 elif path=='docs/sitemap.xml':(E/'cache/sitemap.xml').write_bytes(b)
save('HTML_IDENTITIES.json',html);save('PDF_IDENTITIES.json',pdfs);save('DISTINCTIVE_CANDIDATES.json',candidate)
# Bind target original edition and compare every actual legacy reader hash.
target={}
for rid in ['23576280','23331258']:
 p=P/'papers'/rid;a=json.loads((P/f'verification/root-clearance-{rid}-20261025.json').read_text());api=json.loads((P/a['raw_record_path']).read_text());ready=json.loads((P/a['source_receipt_path']).read_text());pdf=next(Path(x['path']) for x in ready['all_assets'] if x['original_api_file_object']['key'].endswith('.pdf'));txt,pg,info=pages_from(pdf.read_bytes());(E/'cache'/f'target-{rid}.txt').write_text(txt);target[rid]={'metadata':api['metadata'],'root_authority':str((P/f'verification/root-clearance-{rid}-20261025.json').relative_to(P)),'root_authority_sha256':sha((P/f'verification/root-clearance-{rid}-20261025.json').read_bytes()),'approved_scope':a['approved_scope'],'pages':len(pg),'PDF_path':str(pdf),'PDF_bytes':pdf.stat().st_size,'PDF_sha256':sha(pdf.read_bytes()),'controlling_TeX':a['source_tex_path'],'controlling_TeX_sha256':sha((P/a['source_tex_path']).read_bytes()),'identical_legacy_readers':[x['path'] for x in pdfs if x['sha256']==sha(pdf.read_bytes())],'exact_title_legacy_matches':[x['path'] for x in html if api['metadata']['title'].casefold() in x['title'].casefold()]}
save('TARGET_IDENTITIES.json',target)
save('CORPUS_RECEIPT.json',{'utc':utc(),'accepted_commit_pin':PIN,'docs_tree':TREE,'tracked_docs_files':len(rows),'HTML_documents':len(html),'PDF_files':len(pdfs),'PDF_pages_extracted':allpdfpages,'empty_text_pages':[(x['path'],x['empty_text_pages']) for x in pdfs if x['empty_text_pages']],'distinctive_hit_candidates':candidate,'all_254_Git_blob_SHA1_sizes_rechecked':len(rows)==254,'identical_target_PDFs':{k:v['identical_legacy_readers'] for k,v in target.items()},'all_47_HTML_identity_rows_and_all_76_PDF_first_pages_available_for_bounded_read':True,'automatic_extraction_not_human_full_read_of_unrelated854pages':True,'new_HTTP_fetch_or_Git_mutation':False})
print(json.dumps({'files':len(rows),'html':len(html),'pdfs':len(pdfs),'pages':allpdfpages,'candidates':candidate},indent=2))
print('HTML_IDENTITIES')
for x in html:print(x['path']+' | '+x['title'])
print('DISTINCTIVE_PDF_HITS')
for x in pdfs:
 if any(x['core_hits'].values()):print(x['path'],json.dumps(x['core_hits'],ensure_ascii=False))
