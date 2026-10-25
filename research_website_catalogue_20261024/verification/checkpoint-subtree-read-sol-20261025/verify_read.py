"""Read-only sealed-note and actual tree-boundary verification; never checkpoints."""
from pathlib import Path
import hashlib,json,subprocess
O=Path(__file__).resolve().parent;P=O.parents[1];R=P.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(v,t):
 if not v:raise ValueError(t)
def git(*args):return subprocess.check_output(['git','-c','gc.auto=0',*args],cwd=R)
def entries(ref):return {x.split(b'\t',1)[1]:x for x in git('ls-tree','-z',ref).split(b'\0') if x}
r=json.loads((O/'READ_ONLY_RECEIPT.json').read_text());need(sha(Path(r['helper_path']))==r['helper_SHA256'],'helper');need(sha(Path(r['dry_run_receipt_path']))==r['dry_run_receipt_SHA256'],'original_dryrun')
a,b=entries(r['actual_parent']),entries(r['actual_composed_tree']);key=P.name.encode();need({k:v for k,v in a.items() if k!=key}=={k:v for k,v in b.items() if k!=key},'all_siblings')
files=[x.decode() for x in git('diff-tree','-r','--no-commit-id','--name-only','-z',r['actual_parent'],r['actual_composed_tree']).split(b'\0') if x];need(len(files)==1323 and all(x.startswith(P.name+'/') for x in files) and files==(O/'full-tree-changed-paths.txt').read_text().splitlines(),'full_actual_tree_diff')
manifest=O/'FINAL_MANIFEST.json';seal=json.loads((O/'FINAL_SEAL.json').read_text());need(sha(manifest)==seal['manifest_SHA256'],'manifest')
for x in json.loads(manifest.read_text())['files']:
 q=O/x['path'];need(q.is_file() and q.stat().st_size==x['bytes'] and sha(q)==x['SHA256'],'owned:'+x['path'])
print(json.dumps({'status':'PASS_READ_ONLY','owned_bindings':seal['owned_bindings'],'actual_programme_only_changed_paths':len(files),'unchanged_sibling_root_entries':158,'Git_mutations':0}))
