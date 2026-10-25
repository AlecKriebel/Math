"""Read-only manifest/source preservation verification, with honest ref boundary."""
from pathlib import Path
import hashlib,json,subprocess
O=Path(__file__).resolve().parent;P=O.parents[1];G=P.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,tag):
    if not x:raise ValueError('preflight_verify:'+tag)
seal=json.loads((O/'FINAL_SEAL.json').read_text());mf=O/'FINAL_MANIFEST.json';need(sha(mf)==seal['manifest_SHA256'],'owned_manifest_seal')
owned=json.loads(mf.read_text())['files'];cache=json.loads((O/'CACHE_MANIFEST.json').read_text())['files']
for item in owned+cache:
    rel=Path(item['path']);need(not rel.is_absolute() and '..' not in rel.parts,'contained_owned_path');p=O/rel
    need(p.is_file() and not p.is_symlink() and p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],'owned_binding:'+str(rel))
    if p.is_relative_to(O/'tmp'):subprocess.run(['git','check-ignore','-q',str(p)],cwd=G,check=True)
before=json.loads((O/'protected-before.json').read_text());changed=[]
for item in before['files']:
    p=Path(item['path'])
    if not p.is_file() or sha(p)!=item['SHA256']:changed.append(str(p))
documented=json.loads((O/'PRESERVATION_RECEIPT.json').read_text())['only_concurrent_ref_changes'];need(set(changed)=={x['path'] for x in documented},'undocumented_original_change')
for x in documented:need(sha(Path(x['path']))==x['after_SHA256'],'concurrent_ref_moved_after_seal')
verdict=json.loads((O/'IDENTITY_VERDICT.json').read_text());need(len(verdict['targets'])==3 and all(not x['redirect_candidates'] and x['corresponding_legacy_URL'] is None for x in verdict['targets']),'no_candidate_disposition')
tree=subprocess.check_output(['git','rev-parse',verdict['end_pin']+':docs'],cwd=G,text=True).strip();need(tree==verdict['docs_tree'],'exact_pinned_docs_tree')
print(json.dumps({'status':'PASS_READ_ONLY_PREFLIGHT_VERIFICATION','owned_bindings':len(owned),'ignored_cache_bindings':len(cache),'protected_nonref_bindings_unchanged':len(before['files'])-len(documented),'documented_concurrent_ref_changes':len(documented),'no_corresponding_article_targets':3,'writes':0,'redirects_prepared_or_installed':False,'next_three_stage_started':False},indent=2))
