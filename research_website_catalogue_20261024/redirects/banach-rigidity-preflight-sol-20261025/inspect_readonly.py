"""Bounded correspondence evidence. Writes only this new evidence directory.
Git operations read immutable objects and refs; no fetch/index/checkout/HTTP.
Existing sealed PDF extracts are authenticated and read in place.
"""
from pathlib import Path
from html.parser import HTMLParser
import subprocess, os, hashlib, json, datetime, re, unicodedata
E=Path(__file__).resolve().parent; P=E.parents[1]; G=P.parent
OLD=P/'redirects/odd-ear-blocking-preflight-sol-20261025'
PIN='a3c4ad43fb04070dfe5a928080a8198ebc3ad885'
TREE='7a24ec1dcb73a5e06ba82ff9cccda54e73f9deec'
ENV={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_TERMINAL_PROMPT':'0'}
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.run(['git',*args],cwd=G,env=ENV,capture_output=True,check=True,timeout=30).stdout
def save(n,x): (E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def binding(p):
 b=p.read_bytes(); return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def norm(t):
 t=unicodedata.normalize('NFKC',t).replace('\u00ad','');t=re.sub('[‐‑‒–—−]','-',t);t=re.sub(r'-\s+','-',t)
 return ' '.join(t.split())
def hits(t,pat):
 return [{'match':m.group(),'context':t[max(0,m.start()-180):min(len(t),m.end()+300)]} for m in re.finditer(pat,t,re.I)]
if (E/'PRESERVATION_BEFORE.json').exists(): raise RuntimeError('refuse to replace original baseline')
paths=set(p for p in (G/'docs').rglob('*') if p.is_file())
for rel in ['.git/HEAD','.git/index','.git/refs/heads/main','.git/refs/remotes/origin/main']:
 p=G/rel
 if p.exists(): paths.add(p)
for root in [P/'papers/23217863/sources',P/'papers/23217863/reviews/editorial',P/'papers/22395326/reviews/adversarial']:
 paths.update(p for p in root.rglob('*') if p.is_file())
for rid in ['23074543','23442760','23395703','23333353','23416806','23441617','23576280','23331258','23217863']:
 q=P/'papers'/rid/'reviews/adversarial'
 paths.update(p for p in q.glob('*') if p.is_file())
for root in [OLD,P/'redirects/ambient-block-modulus-preflight-sol-20261025',P/'verification/cfh-independent-code-audit-sol-20261025']:
 paths.update(p for p in root.glob('*') if p.is_file())
for rel in ['papers/23217863/publication.json','papers/23217863/promotion.json','verification/root-clearance-23217863-20261025.json','papers/23217863/reviews/root/ROOT_REVIEW.md']:
 paths.add(P/rel)
before={'utc':utc(),'HEAD':git('rev-parse','HEAD').decode().strip(),'main':git('rev-parse','refs/heads/main').decode().strip(),'symbolic_HEAD':git('symbolic-ref','HEAD').decode().strip(),'origin_main_local_ref':git('rev-parse','refs/remotes/origin/main').decode().strip(),'working_docs_status':git('status','--porcelain=v1','--','docs').decode(),'docs_paths':sorted(str(p) for p in (G/'docs').rglob('*') if p.is_file()),'files':[binding(p) for p in sorted(paths)]}
save('PRESERVATION_BEFORE.json',before)
start=utc(); remote=git('ls-remote','origin','refs/heads/main');end=utc()
(E/'remote-main.raw.txt').write_bytes(remote)
assert remote==f'{PIN}\trefs/heads/main\n'.encode(),remote
save('REMOTE_PIN.json',{'started_utc':start,'ended_utc':end,'operation':['git','ls-remote','origin','refs/heads/main'],'remote':git('remote','get-url','origin').decode().strip(),'raw':binding(E/'remote-main.raw.txt'),'commit':PIN,'cached_objects_available':True,'network_scope':'Git read-only ref advertisement; no browser or ordinary HTTP requests, no fetch or ref updates','docs_tree':TREE})
assert git('rev-parse',PIN+':docs').decode().strip()==TREE
assert git('rev-parse',before['HEAD']+':docs').decode().strip()!=TREE
save('LOCAL_REMOTE_DISTINCTION.json',{'local_HEAD':before['HEAD'],'local_main':before['main'],'local_HEAD_docs_tree':git('rev-parse',before['HEAD']+':docs').decode().strip(),'remote_commit':PIN,'remote_docs_tree':TREE,'working_docs_status':before['working_docs_status'],'working_tree_used_as_remote_corpus':False})
oldm=json.loads((OLD/'FINAL_MANIFEST.json').read_text());olds=json.loads((OLD/'FINAL_SEAL.json').read_text());assert sha((OLD/'FINAL_MANIFEST.json').read_bytes())==olds['manifest_sha256']
for r in oldm['files']:
 b=(OLD/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
raw=git('ls-tree','-r','-l','--full-tree',PIN,'--','docs');(E/'docs-tree.raw.txt').write_bytes(raw)
assert raw==(OLD/'docs-tree.raw.txt').read_bytes()
rows=json.loads((OLD/'docs-tree.json').read_text()); assert len(rows)==254
queries={
 'record_DOI_concept':r'23217863|23217862|10[.]5281/zenodo[.]23217863',
 'full_title':r'Ordinary Banach[- ]Mazur rigidity of von Neumann algebras',
 'Banach_Mazur':r'Banach[- ]Mazur|Banach.{0,8}Mazur',
 'distinctive_rigidity':r'ordinary.{0,50}rigidity|von Neumann.{0,60}rigidity|rigidity.{0,60}von Neumann|predual.{0,60}isometr',
 'source_variants':r'ordinary_banach|banach_mazur|banach-mazur|banach.rigidity|roydor|actual[- ]image|higher bounded Hochschild|family[- ]?295',
 'broad_context':r'von Neumann|Hochschild|predual|cohomolog|Jordan.{0,30}isomorph|Banach|Mazur'
}
textsuffix={'.html','.xml','.txt','.md','.tex','.json','.bib','.yml','.yaml','.cff','.py','.js','.css'}
pdfs=json.loads((OLD/'PDF_IDENTITIES.json').read_text());pdfmap={r['path']:r for r in pdfs}
texts=[];inventory=[];html=[];cache=[]
class H(HTMLParser):
 def __init__(self,t): super().__init__(convert_charrefs=True);self.title=[];self.h1=[];self.h2=[];self.cur=None;self.level=None;self.intitle=False;self.meta=[];self.links=[];self.feed(t)
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='title': self.intitle=True
  if t in ['h1','h2']: self.cur=[];self.level=t
  if t=='meta':self.meta.append(d)
  for k in ['href','src','data']:
   if k in d:self.links.append({'tag':t,'attribute':k,'value':d[k],**({'rel':d['rel']} if 'rel' in d else {})})
 def handle_endtag(self,t):
  if t=='title':self.intitle=False
  if t in ['h1','h2'] and self.cur is not None:getattr(self,t).append(norm(''.join(self.cur)));self.cur=None
 def handle_data(self,t):
  if self.intitle:self.title.append(t)
  if self.cur is not None:self.cur.append(t)
for row in rows:
 b=git('cat-file','blob',row['blob']);assert len(b)==row['bytes']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob']
 rec={**row,'sha256':sha(b)};inventory.append(rec)
 suffix=Path(row['path']).suffix.lower()
 if suffix=='.pdf':
  r=pdfmap[row['path']];assert r['blob']==row['blob'] and r['sha256']==sha(b)
  p=OLD/r['text_path'];q=p.read_bytes();assert sha(q)==r['text_sha256'];cache.append(binding(p))
  t=norm(q.decode());texts.append({'kind':'complete_PDF_extract','path':row['path'],'blob':row['blob'],'pages':r['pages'],'source_text':str(p),'hits':{k:hits(t,v) for k,v in queries.items()}})
 elif suffix in textsuffix:
  t=b.decode('utf-8');texts.append({'kind':'complete_tracked_text','path':row['path'],'blob':row['blob'],'hits':{k:hits(norm(t),v) for k,v in queries.items()}})
  if suffix=='.html':
   h=H(t);html.append({**rec,'title':norm(''.join(h.title)),'h1':h.h1,'h2':h.h2,'metadata':h.meta,'links':h.links})
save('DOCS_OBJECT_BINDINGS.json',inventory);save('REUSED_EXTRACT_BINDINGS.json',cache);save('HTML_IDENTITIES.json',html)
save('SEARCH_RESULTS.json',{'utc':utc(),'queries':queries,'normalization':'Unicode NFKC; remove soft hyphens; normalize dash/minus; join wrapped hyphens; fold whitespace; ignore case','rows':texts,'nonempty':[r for r in texts if any(r['hits'].values())]})
# Fresh exact target identity, no version invented from absence.
S=P/'papers/23217863/sources';ready=json.loads((S/'SOURCE_READY.json').read_text());api=json.loads((S/'record.raw.json').read_text());source=S/'published-source/manuscript/main.tex';reader=S/'paper.pdf'
assert sha(reader.read_bytes())==ready['selected_actual_PDF']['sha256']
target={'record':23217863,'title':api['metadata']['title'],'doi':api['doi'],'version_field_present':'version' in api['metadata'],'version':api['metadata'].get('version'),'pages':7,'reader':binding(reader),'source':binding(source),'ready':binding(S/'SOURCE_READY.json'),'identical_legacy_readers':[r['path'] for r in inventory if r['sha256']==sha(reader.read_bytes())],'foreign_OpenAI_28pp_SHA256':'56ec913df9fbe4a2daf371eec1cb06ddc5b544cf9defc838aab540f33171f753','foreign_OpenAI_not_target':True}
save('TARGET_IDENTITY.json',target)
# Raw immutable commit/tree bytes, not a checkout or a repeated asset cache.
objects=[]
for kind,oid in [('commit',PIN),('tree',git('rev-parse',PIN+'^{tree}').decode().strip()),('tree',TREE)]:
 b=git('cat-file',kind,oid);assert hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
 name='git-object-'+oid+'.raw';(E/name).write_bytes(b);objects.append({'kind':kind,'oid':oid,**binding(E/name)})
save('GIT_OBJECT_RECEIPT.json',{'utc':utc(),'objects':objects,'recursive_listing':binding(E/'docs-tree.raw.txt'),'same_recursive_listing_as':binding(OLD/'docs-tree.raw.txt'),'prior_manifest':binding(OLD/'FINAL_MANIFEST.json'),'prior_seal':binding(OLD/'FINAL_SEAL.json'),'prior_owned_files_authenticated':len(oldm['files']),'all_Git_objects_rehashed':len(inventory),'all_old_PDF_extracts_rehashed':len(cache),'no_old_reader_bytes_copied':True})
save('CORPUS_RECEIPT.json',{'utc':utc(),'commit':PIN,'docs_tree':TREE,'total_objects':len(rows),'HTML':len(html),'PDF':len(pdfs),'PDF_pages_in_reused_complete_extracts':sum(r['pages'] for r in pdfs),'tracked_texts':len(texts)-len(pdfs),'all_254_blobs_rehashed':True,'all76_existing_extracts_rehashed':True,'fresh_full_PDF_reextraction':False,'search_universe':'Exact complete tree listed in DOCS_OBJECT_BINDINGS; textual suffixes and all complete PDF extracts','other_assets_not_recursively_expanded':[r for r in inventory if Path(r['path']).suffix.lower() not in textsuffix|{'.pdf'}]})
print(json.dumps({'objects':len(rows),'HTML':len(html),'PDF':len(pdfs),'text_blobs':len(texts)-len(pdfs),'nonempty_hits':[{ 'path':r['path'],'hits':{k:v for k,v in r['hits'].items() if v}} for r in texts if any(r['hits'].values())]},ensure_ascii=False,indent=2))
