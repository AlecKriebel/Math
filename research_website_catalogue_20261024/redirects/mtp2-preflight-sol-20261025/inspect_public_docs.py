"""Read-only Git-public-docs preflight; outputs only within this namespace.

No fetch/checkout/index update; old PDF full extracts reused in place.
"""
from pathlib import Path
from datetime import datetime,timezone
from html.parser import HTMLParser
from pypdf import PdfReader
from io import BytesIO
import hashlib,json,os,re,subprocess,unicodedata

O=Path(__file__).resolve().parent;P=O.parent.parent;REPO=P.parent
OLD=P/'redirects/odd-ear-blocking-preflight-sol-20261025'
BAN=P/'redirects/banach-rigidity-preflight-sol-20261025'
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
utc=lambda:datetime.now(timezone.utc).isoformat()
def need(c,msg):
 if not c:raise RuntimeError(msg)
def run(*args):return subprocess.run(['git',*args],cwd=REPO,env=ENV,capture_output=True,check=True,timeout=45).stdout
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b))
def write(name,value):(O/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def load(p):return json.loads(p.read_text())
def normalize(s):
 s=unicodedata.normalize('NFKC',s).replace('\u00ad','')
 s=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',s)
 s=re.sub('[‐‑‒–—−]','-',s)
 s=re.sub(r'mtp\s*[_-]?\s*2','mtp2',s,flags=re.I)
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

need(not (O/'REMOTE_PIN.json').exists(),'Refusing an existing preflight run')
(O/'.gitignore').write_text('cache/\n');(O/'cache').mkdir(exist_ok=True)
protected={}
for folder in [OLD,BAN]:
 manifest=load(folder/'FINAL_MANIFEST.json');seal=load(folder/'FINAL_SEAL.json')
 need(sha((folder/'FINAL_MANIFEST.json').read_bytes())==seal['manifest_sha256'],'Earlier preflight manifest seal')
 for item in manifest['files']:
  p=folder/item['path'];need(bind(p)==dict(bytes=item['bytes'],sha256=item['sha256']),'Earlier payload changed')
  protected[str(p)]=bind(p)
 protected[str(folder/'FINAL_MANIFEST.json')]=bind(folder/'FINAL_MANIFEST.json')
 protected[str(folder/'FINAL_SEAL.json')]=bind(folder/'FINAL_SEAL.json')
target=P/'papers/23146753'
for p in [*target.joinpath('sources').rglob('*'),*target.joinpath('reviews/editorial').rglob('*'),target/'publication.json',target/'promotion.json']:
 if p.is_file():protected[str(p)]=bind(p)
write('PROTECTED_INPUTS.json',dict(utc=utc(),bindings=protected,no_mutable_prior_baselines_followed=True))

def local_snapshot():
 docs={str(p.relative_to(REPO)):bind(p) for p in sorted((REPO/'docs').rglob('*')) if p.is_file()}
 refs={}
 for name in ['index','HEAD','refs/heads/main','refs/remotes/origin/main']:
  p=Path(run('rev-parse','--git-path',name).decode().strip())
  if not p.is_absolute():p=REPO/p
  refs[name]=dict(path=str(p),**bind(p)) if p.exists() else dict(path=str(p),absent=True)
 return dict(utc=utc(),docs_files=docs,git_files=refs,
   HEAD=run('rev-parse','HEAD').decode().strip(),main=run('rev-parse','refs/heads/main').decode().strip(),
   origin_main=run('rev-parse','refs/remotes/origin/main').decode().strip(),
   dirty_docs_status=run('status','--porcelain=v1','--untracked-files=all','--','docs').decode())
write('LOCAL_BEFORE.json',local_snapshot())
started=utc();advert=run('ls-remote','origin','refs/heads/main');ended=utc()
(O/'remote-main.raw.txt').write_bytes(advert)
commit=advert.decode().split()[0];docs=run('rev-parse',commit+':docs').decode().strip()
need(docs=='7a24ec1dcb73a5e06ba82ff9cccda54e73f9deec','Public docs changed; prior extracts cannot be reused blindly')
tree=run('rev-parse',commit+'^{tree}').decode().strip()
for kind,oid in [('commit',commit),('tree',tree),('tree',docs)]:
 b=run('cat-file',kind,oid);need(hashlib.sha1((kind+' '+str(len(b))+'\0').encode()+b).hexdigest()==oid,'Git object identity')
 (O/('git-object-'+oid+'.raw')).write_bytes(b)
listing=run('ls-tree','-r','-l','-z',commit,'--','docs')
(O/'docs-tree.raw.z').write_bytes(listing)
rows=[]
for part in listing.rstrip(b'\0').split(b'\0'):
 fields,path=part.split(b'\t',1);mode,kind,oid,size=fields.decode().split()
 need(kind=='blob','Unexpected nonblob')
 rows.append(dict(path=path.decode(),mode=mode,kind=kind,blob=oid,bytes=int(size)))
old=load(BAN/'DOCS_OBJECT_BINDINGS.json')
need([{k:r[k]for k in ['path','mode','kind','blob','bytes']}for r in old]==rows,'Complete docs listing changed')
write('REMOTE_PIN.json',dict(started_utc=started,completed_utc=ended,actual_command='git ls-remote origin refs/heads/main',
 actual_output=advert.decode(),commit=commit,root_tree=tree,docs_tree=docs,tracked_docs_blobs=len(rows),
 prior_odd_ear_pin='ebd3c1c3040634fe0cff28765f86ed4b84dad488',
 prior_banach_initial_pin='a3c4ad43fb04070dfe5a928080a8198ebc3ad885',
 prior_banach_authorized_root_closing_pin='c645005caaf33f8a81fe277bde3749c647f379fd',
 interpretation='Fresh current remote observed; exact docs tree/list unchanged despite separately authorized programme checkpoints. No programme path is part of public search corpus.'))
pdfrows=load(OLD/'PDF_IDENTITIES.json');pdfby={r['path']:r for r in pdfrows}
queries={
 'record_or_DOI':[r'23146753',r'23146752',r'10\.5281/zenodo\.23146753'],
 'exact_title':[re.escape(normalize('Closedness and attractive approximation of binary MTP2 edge models'))],
 'MTP2':[r'\bmtp2\b',r'multivariate total positivity',r'multivariate totally positive'],
 'attractive_Ising':[r'attractive ising',r'ising distributions?',r'ising models?'],
 'edge_factor_closure':[r'finite.{0,25}(unary|edge).{0,35}factors?',r'(closedness|closure).{0,45}(edge models?|factor class)',r'nonnegative.{0,20}edge factors?'],
 'distinctive_primary_names':[r'\blauritzen\b',r'\bgandolfi\b',r'\blenarda\b',r'\bzwiernik\b',r'\bsullivant\b',r'\bkahle\b'],
 'broader_topic':[r'graphical models?',r'markov random fields?',r'hammersley.{0,3}clifford',r'log.{0,3}supermodular',r'\bising\b',r'\battractive\b']}
representations=[];bindings=[];reuse=[];html=[];hash_matches=[]
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=REPO,env=ENV,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
proc.stdin.write(('\n'.join(x['blob']for x in rows)+'\n').encode());proc.stdin.close()
for row in rows:
 header=proc.stdout.readline().decode().split();need(header==[row['blob'],'blob',str(row['bytes'])],'Batch object header')
 data=proc.stdout.read(row['bytes']);need(proc.stdout.read(1)==b'\n','Batch framing')
 need(hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()==row['blob'],'Actual Git blob SHA1')
 identity={**row,'sha256':sha(data)};need(identity==old[len(bindings)],'Blob differs from authenticated prior inventory');bindings.append(identity)
 if sha(data)in [load(target/'sources/SOURCE_READY.json')['all_assets'][j]['sha256']for j in range(2)]:hash_matches.append(row['path'])
 if row['path'].lower().endswith('.pdf'):
  pdf=pdfby[row['path']];need(pdf['blob']==row['blob'] and pdf['sha256']==sha(data),'PDF/extract source mismatch')
  path=OLD/pdf['text_path'];need(sha(path.read_bytes())==pdf['text_sha256'],'Reused full extract changed')
  reuse.append(dict(public_path=row['path'],pdf_blob=row['blob'],pdf_sha256=sha(data),pages=pdf['pages'],path=str(path),**bind(path)))
  representations.append(dict(path=row['path'],kind='complete_reused_PDF_text',text=path.read_text()))
 else:
  try:t=data.decode('utf8')
  except UnicodeDecodeError:continue
  if '\0' in t:continue
  representations.append(dict(path=row['path'],kind='raw_UTF8_blob',text=t))
  if row['path'].lower().endswith('.html'):
   parser=Visible();parser.feed(t);v=''.join(parser.parts)
   representations.append(dict(path=row['path'],kind='decoded_visible_HTML',text=v))
   title=re.search(r'<title[^>]*>(.*?)</title>',t,re.S|re.I)
   headings=re.findall(r'<h[12][^>]*>(.*?)</h[12]>',t,re.S|re.I)
   html.append(dict(path=row['path'],blob=row['blob'],title=re.sub('<[^>]+>','',title.group(1))if title else None,headings=[re.sub('<[^>]+>','',x)for x in headings]))
need(proc.wait(timeout=30)==0 and not proc.stderr.read(),'Batch process failed')
search=[]
for item in representations:
 t=normalize(item['text']);groups={}
 for group,pats in queries.items():
  hits=[]
  for pat in pats:
   for m in re.finditer(pat,t):hits.append(dict(pattern=pat,match=m.group(),context=t[max(0,m.start()-140):m.end()+220]))
  groups[group]=hits
 search.append(dict(path=item['path'],kind=item['kind'],normalized_characters=len(t),groups=groups))
write('DOCS_OBJECT_BINDINGS.json',bindings);write('REUSED_EXTRACT_BINDINGS.json',reuse);write('HTML_IDENTITIES.json',html)
write('SEARCH_RESULTS.json',dict(utc=utc(),queries=queries,representations=search,
 exact_target_asset_hash_matches=hash_matches,public_universe_only=True,nested_support_archives_text_expanded=False))
write('CORPUS_RECEIPT.json',dict(utc=utc(),docs_tree=docs,actual_git_blobs=len(bindings),HTML=len(html),PDF=len(reuse),PDF_pages=sum(x['pages']for x in reuse),
 representations=len(representations),raw_UTF8_blobs=sum(x['kind']=='raw_UTF8_blob'for x in representations),
 old_PDFs_newly_extracted=0,all_reused_extracts_source_blob_and_hash_bound=True,exact_target_asset_hash_matches=hash_matches))
targetbytes=(target/'sources/mtp2-edge-closure-note.pdf').read_bytes()
targettext='\n'.join(p.extract_text()or''for p in PdfReader(BytesIO(targetbytes)).pages)
title='Closedness and attractive approximation of binary MTP2 edge models'
controls=[dict(name='actual_target_complete_title',pass_=normalize(title)in normalize(targettext)),
 dict(name='actual_target_MTP2_pattern',pass_=bool(re.search(queries['MTP2'][0],normalize(targettext)))),
 dict(name='known_public_positive_recurrence',pass_=any('positive recurrence for single-linkage bimolecular' in normalize(x['text'])for x in representations)),
 dict(name='Unicode_subscript_and_wrap',pass_=normalize('MTP₂\nedge models')==normalize('MTP2 edge models')),
 dict(name='Soft_hyphen_and_ligature',pass_=normalize('ﬁnite non\u00adnegative')==normalize('finite nonnegative'))]
need(all(x['pass_']for x in controls),'Positive query control failed')
write('QUERY_CONTROLS.json',dict(controls=controls,target_control_excluded_from_legacy_corpus=True,actual_target_PDF_SHA256=sha(targetbytes),new_target_control_pages=5,old_854_pages_not_reextracted=True))
write('LOCAL_AFTER_SCAN.json',local_snapshot())
with(O/'RESEARCH_LOG.md').open('a')as f:f.write(f'{utc()} — checkpoint65%: fresh remote/docs objects and254 actual blobs authenticated;76complete extracts/854pages reused unchanged;260search representations and fivepositivecontrols complete. Boundedcandidate/exclusionreading and closingpreservation/seal remain.\n')
print(json.dumps(dict(remote=commit,docs_tree=docs,blobs=len(bindings),representations=len(search),
 matches={g:sum(bool(x['groups'][g])for x in search)for g in queries},
 paths_with_any_hits=sorted({x['path']for x in search if any(x['groups'].values())}),hash_matches=hash_matches),indent=2))
