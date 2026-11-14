"""One bounded read-only public-Git-docs scan; no PDF re-extraction or Git write."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime,timezone
import hashlib,json,os,re,subprocess,unicodedata
O=Path(__file__).resolve().parent;P=O.parent.parent;R=P.parent
OLD=P/'redirects/mtp2-preflight-sol-20261025'
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def bind(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b))
def w(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def git(*a):return subprocess.run(['git',*a],cwd=R,env=ENV,capture_output=True,check=True,timeout=45).stdout
def normalize(s):
 s=unicodedata.normalize('NFKC',s).replace('\u00ad','').replace('’',"'").replace('‘',"'")
 s=''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))
 s=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',s);s=re.sub('[‐‑‒–—−]','-',s)
 return re.sub(r'\s+',' ',s).casefold()
class Visible(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['p','h1','h2','h3','li','div','section','br']:self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)

need(not (O/'SEARCH_RESULTS.json').exists(),'Refusing existing scan')
(O/'cache').mkdir(exist_ok=True);pin=load(O/'REMOTE_PIN.json')
need(pin['docs_tree']=='7a24ec1dcb73a5e06ba82ff9cccda54e73f9deec','Prior corpus no longer eligible')
protected={}
for folder in [OLD,P/'papers/23124601/reviews/editorial',P/'papers/23333046/reviews/editorial']:
 manifest_name='FINAL_MANIFEST.json' if folder==OLD else 'MANIFEST.json'
 seal_name='FINAL_SEAL.json' if folder==OLD else 'SEAL.json'
 manifest=load(folder/manifest_name);seal=load(folder/seal_name)
 need(sha((folder/manifest_name).read_bytes())==seal['manifest_sha256'],'Prior packet seal')
 for x in manifest['files']:
  path=folder/x['path'];need(bind(path)=={k:x[k] for k in ['bytes','sha256']},'Prior owned payload changed')
  protected[str(path)]=bind(path)
 for n in [manifest_name,seal_name]:protected[str(folder/n)]=bind(folder/n)
for ident in ['23124601','23333046']:
 T=P/'papers'/ident
 for path in [*T.joinpath('sources').rglob('*'),T/'publication.json',T/'promotion.json']:
  if path.is_file():protected[str(path)]=bind(path)
w('PROTECTED_INPUTS.json',{'utc':datetime.now(timezone.utc).isoformat(),'bindings':protected,'no_stale_mutable_production_baseline_followed':True})
for kind,oid in [('commit',pin['commit']),('tree',pin['root_tree']),('tree',pin['docs_tree'])]:
 b=git('cat-file',kind,oid);need(hashlib.sha1((kind+' '+str(len(b))+'\0').encode()+b).hexdigest()==oid,'Git object hash')
 (O/('git-object-'+oid+'.raw')).write_bytes(b)
listing=git('ls-tree','-r','-l','-z',pin['commit'],'--','docs');(O/'docs-tree.raw.z').write_bytes(listing)
rows=[]
for part in listing.rstrip(b'\0').split(b'\0'):
 f,n=part.split(b'\t',1);mode,kind,oid,size=f.decode().split()
 rows.append(dict(path=n.decode(),mode=mode,kind=kind,blob=oid,bytes=int(size)))
old=load(OLD/'DOCS_OBJECT_BINDINGS.json')
need(rows==[{k:x[k] for k in ['path','mode','kind','blob','bytes']} for x in old],'Exact complete prior docs inventory differs')
reused=load(OLD/'REUSED_EXTRACT_BINDINGS.json');byPDF={x['public_path']:x for x in reused}
targets={};target_hashes={};controls=[]
for ident in ['23124601','23333046']:
 T=P/'papers'/ident;ready=load(T/'sources/SOURCE_READY.json')
 assets=ready['assets'] if ident=='23124601' else ready['all_assets_in_original_order']
 sourcehashes=[]
 for x in assets:
  path=Path(x['path']);path=path if path.is_absolute() else T/'sources'/path
  need(bind(path)=={k:x[k] for k in ['bytes','sha256']},'Actual target asset')
  sourcehashes.append(x['sha256']);target_hashes[x['sha256']]=ident
 textpath=T/'reviews/editorial/cache/actual-reader.full-text.txt'
 manifest=load(T/'reviews/editorial/MANIFEST.json');entry=next(x for x in manifest['files'] if x['path']=='cache/actual-reader.full-text.txt')
 need(bind(textpath)=={k:entry[k] for k in ['bytes','sha256']},'Sealed actual-reader positive-control text')
 text=textpath.read_text();targets[ident]={'whole_original_source_ready':ready,'source_ready_binding':bind(T/'sources/SOURCE_READY.json'),
 'source_asset_hashes':sourcehashes,'positive_control_full_reader_text':{'path':str(textpath),**bind(textpath)},
 'control_is_not_part_of_legacy_corpus':True}
 controls.append(dict(name=ident+' actual complete title',pass_=normalize(ready['title']) in normalize(text)))
queries={
 '106_record_or_DOI':[r'23124601',r'23124600',r'10\.5281/zenodo\.23124601'],
 '106_exact_title':[re.escape(normalize(targets['23124601']['whole_original_source_ready']['title']))],
 '106_distinctive_terms':[r'\bwajnryb\b',r'artin.{0,12}a.?5',r'\bhurwitz\b',r'fixed.generator.{0,40}(factor|positive|words?)'],
 '106_broad_context':[r'positive.{0,25}factorizations?',r'six.strand',r'\bbraid groups?\b',r'\bcasson\b',r'perron.{0,6}vannier',r'\bmatsumoto\b'],
 '107_record_or_DOI':[r'23333046',r'23333045',r'10\.5281/zenodo\.23333046'],
 '107_exact_title':[re.escape(normalize(targets['23333046']['whole_original_source_ready']['title']))],
 '107_distinctive_terms':[r'\bdevissage\b',r'\bbyszewski\b',r'\bcornelissen\b',r'local.{0,15}deformation.{0,15}functors?'],
 '107_broad_context':[r'weakly.{0,12}ramified',r'restriction.{0,20}induction',r'prorepresentab',r'formal.{0,15}smooth',r'nilpotent.{0,15}constant']}
representations=[];bindings=[];hashmatches=[];html=[]
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,env=ENV,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
proc.stdin.write(('\n'.join(x['blob'] for x in rows)+'\n').encode());proc.stdin.close()
for row in rows:
 need(proc.stdout.readline().decode().split()==[row['blob'],'blob',str(row['bytes'])],'Actual blob batch header')
 data=proc.stdout.read(row['bytes']);need(proc.stdout.read(1)==b'\n','Batch framing')
 need(hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()==row['blob'],'Actual Git blob SHA1')
 b={**row,'sha256':sha(data)};need(b==old[len(bindings)],'Actual blob differs from prior binding');bindings.append(b)
 if sha(data) in target_hashes:hashmatches.append(dict(path=row['path'],target=target_hashes[sha(data)],sha256=sha(data)))
 if row['path'].lower().endswith('.pdf'):
  x=byPDF[row['path']];need(x['pdf_blob']==row['blob'] and x['pdf_sha256']==sha(data),'PDF/extract source identity')
  need(bind(Path(x['path']))=={k:x[k] for k in ['bytes','sha256']},'Reused complete extraction bytes')
  representations.append(dict(path=row['path'],kind='complete_reused_PDF_text',text=Path(x['path']).read_text()))
 else:
  try:text=data.decode('utf8')
  except UnicodeDecodeError:continue
  if '\0' in text:continue
  representations.append(dict(path=row['path'],kind='raw_UTF8_blob',text=text))
  if row['path'].lower().endswith('.html'):
   parser=Visible();parser.feed(text);v=''.join(parser.parts);representations.append(dict(path=row['path'],kind='decoded_visible_HTML',text=v))
   ti=re.search(r'<title[^>]*>(.*?)</title>',text,re.I|re.S)
   html.append(dict(path=row['path'],blob=row['blob'],title=re.sub('<[^>]+>','',ti.group(1)) if ti else None))
need(proc.wait(timeout=30)==0 and not proc.stderr.read(),'Batch process failed')
search=[]
for x in representations:
 text=normalize(x['text']);groups={}
 for g,pats in queries.items():
  hits=[]
  for pat in pats:
   for m in re.finditer(pat,text):hits.append(dict(pattern=pat,match=m.group(),context=text[max(0,m.start()-150):m.end()+250]))
  groups[g]=hits
 search.append(dict(path=x['path'],kind=x['kind'],normalized_characters=len(text),groups=groups))
controls += [dict(name='known public positive-recurrence phrase',pass_=any('positive recurrence for single-linkage bimolecular' in normalize(x['text']) for x in representations)),
 dict(name='curly apostrophe and subscript',pass_=normalize('Wajnryb’s Artin A₅')==normalize("Wajnryb's Artin A5")),
 dict(name='accented versus ASCII devissage',pass_=normalize('dévissage')==normalize('devissage')),
 dict(name='soft hyphen/ligature/line wrap',pass_=normalize('ﬁxed non\u00adnegative\nwords')==normalize('fixed nonnegative words'))]
need(all(x['pass_'] for x in controls),'Positive search control failed')
w('TARGET_IDENTITIES.json',targets);w('DOCS_OBJECT_BINDINGS.json',bindings);w('REUSED_EXTRACT_BINDINGS.json',reused);w('HTML_IDENTITIES.json',html)
w('SEARCH_RESULTS.json',{'utc':datetime.now(timezone.utc).isoformat(),'queries':queries,'representations':search,'exact_asset_hash_matches':hashmatches,
 'only_actual_public_docs':True,'binary_support_archives_text_expanded':False})
w('QUERY_CONTROLS.json',{'controls':controls,'all_passed':True,'target_controls_excluded_from_legacy_corpus':True,'new_PDF_extractions':0})
w('CORPUS_RECEIPT.json',{'docs_tree':pin['docs_tree'],'actual_blobs':len(bindings),'HTML':len(html),'complete_PDFs':len(reused),
 'complete_PDF_pages':sum(x['pages'] for x in reused),'representations':len(search),'raw_UTF8_blobs':sum(x['kind']=='raw_UTF8_blob' for x in search),
 'old_PDF_extractions':0,'target_PDF_extractions':0,'exact_asset_hash_matches':hashmatches,
 'group_hit_representation_counts':{g:sum(bool(x['groups'][g]) for x in search) for g in queries}})
print(json.dumps({'groups':{g:sum(bool(x['groups'][g]) for x in search) for g in queries},
 'candidate_paths':sorted({x['path'] for x in search if any(x['groups'].values())}),'hash_matches':hashmatches,'protected':len(protected)},indent=2))
