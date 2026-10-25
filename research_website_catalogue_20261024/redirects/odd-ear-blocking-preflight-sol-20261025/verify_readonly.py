"""Read-only preflight custody verifier. No receipt, Git or source writes."""
from pathlib import Path
import argparse,json,hashlib,subprocess
E=Path(__file__).resolve().parent;P=E.parents[1];G=P.parent
ap=argparse.ArgumentParser();ap.add_argument('--current-working-preservation',action='store_true',help='Also require mutable working docs/shared index to still equal this historical task snapshot.');a=ap.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.run(['git',*args],cwd=G,capture_output=True,check=True,timeout=30).stdout
m=json.loads((E/'FINAL_MANIFEST.json').read_text());seal=json.loads((E/'FINAL_SEAL.json').read_text());assert seal['manifest_sha256']==sha((E/'FINAL_MANIFEST.json').read_bytes())
for x in m['files']:
 b=(E/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
cm=json.loads((E/'CACHE_MANIFEST.json').read_text())
for x in cm['files']:
 b=(E/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
pin=json.loads((E/'PIN_AUTHORITY.json').read_text());assert git('rev-parse',pin['accepted_origin_main']+':docs').decode().strip()==pin['accepted_docs_tree']
rows=json.loads((E/'docs-tree.json').read_text());assert len(rows)==254;assert git('ls-tree','-r','-l','--full-tree',pin['accepted_origin_main'],'--','docs')==(E/'docs-tree.raw.txt').read_bytes()
for x in rows:
 b=git('cat-file','blob',x['blob']);assert len(b)==x['bytes'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'],x['path']
pdfs=json.loads((E/'PDF_IDENTITIES.json').read_text());pages=0
for x in pdfs:
 b=git('cat-file','blob',x['blob']);assert sha(b)==x['sha256'];text=subprocess.run(['/opt/homebrew/bin/pdftotext','-','-'],input=b,check=True,capture_output=True,timeout=30).stdout;assert text==(E/x['text_path']).read_bytes(),x['path'];pg=text.decode().split('\f');pg=pg[:-1] if not pg[-1].strip() else pg;assert len(pg)==x['pages'];pages+=len(pg)
assert len(pdfs)==76 and pages==854
originals=json.loads((E/'PRESERVATION_BEFORE.json').read_text());target_count=0
for x in originals['files']:
 p=Path(x['path']);is_mutable=p.is_relative_to(G/'docs') or p.is_relative_to(G/'.git')
 if is_mutable and not a.current_working_preservation:continue
 b=p.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path'];target_count+=1
normalized=json.loads((E/'NORMALIZED_IDENTITY_SEARCH.json').read_text());assert len(normalized['rows'])==199 and not normalized['nonempty_target_hits'];assert json.loads((E/'QUERY_CONTROLS.json').read_text())['status']=='PASS'
assert all(not x['identical_legacy_readers'] and not x['exact_title_legacy_matches'] for x in json.loads((E/'TARGET_IDENTITIES.json').read_text()).values())
print(json.dumps({'status':'PASS','owned':len(m['files']),'cache_bindings':len(cm['files']),'Git_docs_objects':len(rows),'PDFs_reextracted':76,'pages':pages,'current_originals_rehashed':target_count,'mutable_working_state_required':a.current_working_preservation,'accepted_immutable_commit':pin['accepted_origin_main'],'new_network_or_Git_writes':False}))
