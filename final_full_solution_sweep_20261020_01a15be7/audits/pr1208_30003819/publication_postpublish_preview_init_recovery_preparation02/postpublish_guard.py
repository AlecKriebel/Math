"""Fixed additive authority, full current append prefix, and prior authority guards."""
from pathlib import Path,PurePosixPath
import hashlib,json,re
ALLOWED=['reconcile','verify-public','ledger']
SOURCE07='193013d467111f11726f151ddc2a4f38b0dfa5868950042d860cfdb7f4845148'
BOOT07='22c4e8c67a657798c4ffd93c2ab4fcfd33868c716bf7c29c17607692f88b762d'
def need(ok,message):
 if not ok:raise RuntimeError(message)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def strict(raw):
 def pairs(items):
  out={}
  for k,v in items:need(k not in out,'Duplicate JSON key');out[k]=v
  return out
 def bad(v):raise RuntimeError('Nonfinite JSON')
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
def typed(x,y):
 if type(x) is not type(y):return False
 if type(x) is dict:return set(x)==set(y) and all(typed(x[k],y[k]) for k in x)
 if type(x) is list:return len(x)==len(y) and all(typed(a,b) for a,b in zip(x,y))
 return x==y
def readpin(path,expected):
 need(not any(p.is_symlink() for p in [path,*path.parents]),'Pinned path symlink');body=path.read_bytes();need(pin(body)==expected,'Pinned input differs: '+str(path));return body
def contract(root,source_sha,oldguard):
 bindings=strict((root/'INPUT_BINDINGS.json').read_bytes());audit=root.parent;oldroot=audit/'publication_samecase_recovery_preparation01';old=oldguard['contract'](oldroot,bindings['recovery01_source_sha256']);case=audit/'execution_PR1208_ops07_action01';prefix=strict(readpin(root/'private/CURRENT_CASE_PREFIX.json',bindings['current_prefix']))
 need(bindings['case_path']==str(case) and prefix['case_path']==str(case),'Fixed currentCASE required')
 return {'root':root,'case':case,'bindings':bindings,'prefix':prefix,'source_sha':source_sha,'oldguard':oldguard,'old':old,'new':audit/'ROOT_PR1208_POSTPUBLISH_PREVIEW_INIT_RECOVERY02_ADOPTION.json'}
def preserved(c):
 for path,p in c['bindings']['refs'].items():readpin(Path(path),p)
 c['oldguard']['preserved'](c['old']);c['oldguard']['prefix_check'](c['prefix'],c['case'])
def expected_authority(c):
 b=c['bindings'];return {'pr':1208,'record':23578142,'concept':23578141,'case_path':str(c['case']),'source07_sha256':SOURCE07,'bootstrap07_sha256':BOOT07,'recovery01_source_sha256':b['recovery01_source_sha256'],'original_authority_sha256':b['original_authority_sha256'],'recovery01_authority_sha256':b['recovery01_authority_sha256'],'postpublish02_source_sha256':c['source_sha'],'current_CASE_prefix_pin':b['current_prefix'],'original_publish_response':b['original_publish_response'],'original_publish_intent':b['original_publish_intent'],'original_publish_phase_intent':b['original_publish_phase_intent'],'allowed_actions':ALLOWED,'canonical_manifest':str(c['root'].parent/'publication_operations_preparation_07/proposed/preprint/zenodo-deposit.json'),'canonical_state_key':'34d22e072d53f77e6492fbfe-production.json','preview_rule':'Exact23578142 hidden zero-byte init media with pinned PDF/preview IDs and unchanged original checks; no remote normalization','effect_rule':'No publication/Git/cursor effects; first single original appendCells ledger request only; prior intent GET-only'}
def verify_authorization(c,sha,action,source_check,read_authority=None,read_review=None):
 need(action in ALLOWED and type(sha) is str and re.fullmatch('[a-f0-9]{64}',sha),'Explicit new root authority/action required')
 raw=(read_authority or (lambda:c['new'].read_bytes()))();need(pin(raw)['sha256']==sha,'Postpublish02 authority changed');a=strict(raw);expected=expected_authority(c)
 for key,value in expected.items():need(typed(a.get(key),value),'New authority target/policy differs: '+key)
 extra={'schema','template_only','root_complete_sources_and_fresh_review_read','ready_for_execution','unresolved_findings','packet_manifest_sha256','fresh_independent_review'}
 need(set(a)==set(expected)|extra and a['schema']=='pr1208-postpublish-preview-init-recovery-v2' and a['template_only'] is False and a['root_complete_sources_and_fresh_review_read'] is True and a['ready_for_execution'] is True and typed(a['unresolved_findings'],[]),'New independent/root adoption absent')
 source_check();need(pin((c['root']/'RECOVERY_MANIFEST.json').read_bytes())['sha256']==a['packet_manifest_sha256'],'New packet differs')
 r=a['fresh_independent_review'];need(type(r) is dict and set(r)=={'receipt_path','receipt_pin','manifest_path','manifest_pin'},'Exact fresh new review required')
 def repo_read(name,p):
  need(type(name) is str and name and not any(x in name for x in ['\\',':','\0']),'Unsafe review path');rel=PurePosixPath(name);need(not rel.is_absolute() and rel.as_posix()==name and all(x not in {'','.','..'} for x in name.split('/')),'Review path escape');return readpin(c['root'].parents[3]/name,p)
 read=read_review or repo_read;receipt=strict(read(r['receipt_path'],r['receipt_pin']));read(r['manifest_path'],r['manifest_pin'])
 need(set(receipt)=={'schema','pr','record','source_sha256','status','fresh_independent_review','unresolved_findings'} and receipt['schema']=='pr1208-postpublish-preview-init-review-v2' and type(receipt['pr']) is int and receipt['pr']==1208 and type(receipt['record']) is int and receipt['record']==23578142 and receipt['source_sha256']==c['source_sha'] and receipt['status']=='PASS' and receipt['fresh_independent_review'] is True and typed(receipt['unresolved_findings'],[]),'Fresh exact whole02 independent PASS absent')
 c['oldguard']['verify_authorization'](c['old'],c['bindings']['recovery01_authority_sha256'],action,source_check);preserved(c);return a
