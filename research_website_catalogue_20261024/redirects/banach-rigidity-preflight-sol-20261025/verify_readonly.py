"""Verify this bounded correspondence packet without writes or network.
Use --current-working-preservation to compare mutable working docs/refs/index
with the historical task baseline. Later authorized work may change them.
"""
from pathlib import Path
from html.parser import HTMLParser
import argparse,subprocess,os,json,hashlib,re,unicodedata
E=Path(__file__).resolve().parent;P=E.parents[1];G=P.parent
ap=argparse.ArgumentParser();ap.add_argument('--current-working-preservation',action='store_true');args=ap.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.run(['git',*a],cwd=G,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},capture_output=True,check=True,timeout=30).stdout
def norm(t):
 t=unicodedata.normalize('NFKC',t).replace('\u00ad','');t=re.sub('[‐‑‒–—−]','-',t);t=re.sub(r'-\s+','-',t);return ' '.join(t.split())
class Visible(HTMLParser):
 def __init__(self,t):super().__init__(convert_charrefs=True);self.parts=[];self.skip=0;self.feed(t)
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def require_binding(x):
 b=Path(x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path'];return b
manifest=json.loads((E/'FINAL_MANIFEST.json').read_text());seal=json.loads((E/'FINAL_SEAL.json').read_text())
assert sha((E/'FINAL_MANIFEST.json').read_bytes())==seal['manifest_sha256']
assert {p.name for p in E.iterdir() if p.is_file()}=={x['path'] for x in manifest['files']}|{'FINAL_MANIFEST.json','FINAL_SEAL.json'}
for r in manifest['files']:
 b=(E/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
pin=json.loads((E/'REMOTE_PIN.json').read_text());assert require_binding(pin['raw'])==f"{pin['commit']}\trefs/heads/main\n".encode()
assert git('rev-parse',pin['commit']+':docs').decode().strip()==pin['docs_tree']
assert git('ls-tree','-r','-l','--full-tree',pin['commit'],'--','docs')==(E/'docs-tree.raw.txt').read_bytes()
for r in json.loads((E/'GIT_OBJECT_RECEIPT.json').read_text())['objects']:
 b=require_binding(r);assert hashlib.sha1(r['kind'].encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['oid']
tree=json.loads((E/'DOCS_OBJECT_BINDINGS.json').read_text());assert len(tree)==254;rawtexts={}
for r in tree:
 b=git('cat-file','blob',r['blob']);assert len(b)==r['bytes'] and sha(b)==r['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
 if r['path'].endswith('.pdf'):continue
 try:t=b.decode('utf-8')
 except UnicodeDecodeError:continue
 if '\0' not in t:rawtexts[r['path']]=t
extracts=json.loads((E/'REUSED_EXTRACT_BINDINGS.json').read_text());assert len(extracts)==76
for r in extracts:require_binding(r)
search=json.loads((E/'COMPLETE_SEARCH.json').read_text());assert len(search['rows'])==260 and len(rawtexts)==137
for r in search['rows']:
 if r['kind']=='complete_PDF_extract':t=Path(r['source_text']).read_text()
 elif r['kind']=='decoded_visible_HTML':t=' '.join(Visible(rawtexts[r['path']]).parts)
 else:t=rawtexts[r['path']]
 t=norm(t)
 for k,pat in search['queries'].items():
  matches=list(re.finditer(pat,t,re.I));assert len(matches)==len(r['hits'][k]),(r['path'],k)
  if k!='broad_context':assert not matches,(r['path'],k)
assert json.loads((E/'QUERY_CONTROLS.json').read_text())['status']=='PASS'
target=json.loads((E/'TARGET_IDENTITY.json').read_text());assert target['record']==23217863 and target['version'] is None and target['version_field_present'] is False
for k in ['reader','source','ready']:require_binding(target[k])
assert not target['identical_legacy_readers'] and target['reader']['sha256']!=target['foreign_OpenAI_28pp_SHA256']
v=json.loads((E/'VERDICT.json').read_text());assert v['status']=='NO_GENUINE_LEGACY_CORRESPONDENCE_IDENTIFIED' and not v['redirect_candidates']
before=json.loads((E/'PRESERVATION_BEFORE.json').read_text());after=json.loads((E/'PRESERVATION_AFTER.json').read_text());assert after['changed_files']==[] and after['added_or_removed_working_docs']==[] and after['refs_unchanged'] and after['working_docs_status_unchanged']
checked=0
for r in before['files']:
 p=Path(r['path']);mutable=p.is_relative_to(G/'docs') or p.is_relative_to(G/'.git')
 if mutable and not args.current_working_preservation:continue
 require_binding(r);checked+=1
if args.current_working_preservation:
 assert sorted(str(p) for p in (G/'docs').rglob('*') if p.is_file())==before['docs_paths']
 assert git('status','--porcelain=v1','--','docs').decode()==before['working_docs_status']
 for key,ref in [('HEAD','HEAD'),('main','refs/heads/main'),('origin_main_local_ref','refs/remotes/origin/main')]:assert git('rev-parse',ref).decode().strip()==before[key]
 assert git('symbolic-ref','HEAD').decode().strip()==before['symbolic_HEAD']
print(json.dumps({'status':'PASS','owned_payload_files':len(manifest['files']),'immutable_docs_blobs':254,'reused_PDF_extracts':76,'replayed_search_representations':260,'current_originals_rehashed':checked,'current_mutable_preservation_required':args.current_working_preservation,'no_network_or_writes':True}))
