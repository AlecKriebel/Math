"""Additive authorization and original-prefix guard. Never writes a CASE/authority."""
from pathlib import Path,PurePosixPath
import hashlib,json,re
ACTIONS=['integrate','describe','ready','merge','stage','publish','verify-public','ledger','reconcile']
OLD_SHA='34a3efd811f7e3eb5946ab06de612f0f651d2c64c7e30bc32892e468e6079672'
SOURCE07='193013d467111f11726f151ddc2a4f38b0dfa5868950042d860cfdb7f4845148';BOOT07='22c4e8c67a657798c4ffd93c2ab4fcfd33868c716bf7c29c17607692f88b762d'
def need(v,m):
 if not v:raise RuntimeError(m)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def strict(raw):
 def pairs(items):
  d={}
  for k,v in items:need(k not in d,'Duplicate JSON key');d[k]=v
  return d
 def bad(v):raise RuntimeError('Nonfinite JSON')
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad)
def readpin(path,expected):
 need(not any(p.is_symlink() for p in [path,*path.parents]),'Pinned path symlink');raw=path.read_bytes();need(pin(raw)==expected,'Pinned input changed');return raw

def prefix_check(prefix,case):
 need(prefix['case_path']==str(case),'Prefix CASE differs');expected={e['path'] for e in prefix['entries']}
 for e in prefix['entries']:
  path=case if e['path']=='.' else case/e['path'];s=path.lstat();need(not path.is_symlink() and s.st_dev==e['device'] and s.st_ino==e['inode'] and s.st_mode&0o777==e['mode'],'Original prefix identity/mode changed')
  if e['kind']=='file':need(path.is_file() and s.st_nlink==e['nlink'] and s.st_mtime_ns==e['mtime_ns'] and pin(path.read_bytes())=={k:e[k] for k in ['bytes','sha256']},'Original prefix file changed')
  else:need(path.is_dir(),'Original directory replaced')
 need({'.'}|{x.relative_to(case).as_posix() for x in case.rglob('*')}>=expected,'Original prefix path removed');return True

def contract(root,source_sha):
 audit=root.parent;bindings=strict((root/'INPUT_BINDINGS.json').read_bytes());case=audit/'execution_PR1208_ops07_action01';old=audit/'ROOT_PR1208_OPS07_ACTION_ADOPTION.json';new=audit/'ROOT_PR1208_SAMECASE_RECOVERY01_ADOPTION.json';prefixpath=root/'private/ACTUAL_CASE_PREFIX_MANIFEST.json';prefix=strict(readpin(prefixpath,bindings['actual_CASE_prefix_manifest']));phase=next(e for e in prefix['entries'] if e['path']=='INTEGRATE_PHASE_INTENT.json');return {'root':root,'case':case,'old':old,'new':new,'bindings':bindings,'prefix_path':prefixpath,'prefix':prefix,'phase_pin':{k:phase[k] for k in ['bytes','sha256']},'source_sha':source_sha}

def preserved(c):
 for name,e in c['bindings']['refs'].items():readpin(Path(name),e)
 need(pin(c['old'].read_bytes())['sha256']==OLD_SHA,'Original actual authority changed');prefix_check(c['prefix'],c['case'])

def verify_authorization(c,auth_sha,action,source_check,receipt_read=None):
 need(action in ACTIONS and type(auth_sha) is str and re.fullmatch('[a-f0-9]{64}',auth_sha),'Explicit recovery authority/action required');raw=c['new'].read_bytes();need(pin(raw)['sha256']==auth_sha,'Additive recovery authority changed');a=strict(raw)
 need(type(a) is dict and a.get('schema')=='pr1208-additive-samecase-recovery-v1' and a.get('template_only') is False and a.get('root_complete_recovery_sources_and_review_read') is True and a.get('ready_for_execution') is True and a.get('unresolved_findings')==[],'Fresh root recovery adoption absent')
 expected={'pr':1208,'original_authority_sha256':OLD_SHA,'source07_sha256':SOURCE07,'bootstrap07_sha256':BOOT07,'adapter_source_sha256':c['source_sha'],'case_path':str(c['case']),'original_CASE_prefix_pin':c['bindings']['actual_CASE_prefix_manifest'],'original_phase_intent_pin':c['phase_pin'],'allowed_actions':ACTIONS,'allow_one_unattempted_integration_continuation':True,'main_policy':'fresh_latest_main_with_original13leaf_scope_and_all_core_guards','canonical_manifest':str(c['root'].parent/'publication_operations_preparation_07/proposed/preprint/zenodo-deposit.json'),'canonical_state_key':'34d22e072d53f77e6492fbfe-production.json'}
 def typed(x,y):
  if type(x) is not type(y):return False
  if type(x) is dict:return set(x)==set(y) and all(typed(x[k],y[k]) for k in x)
  if type(x) is list:return len(x)==len(y) and all(typed(v,w) for v,w in zip(x,y))
  return x==y
 for key,value in expected.items():need(typed(a.get(key),value),'Additive recovery target/policy mismatch: '+key)
 need(set(a)==set(expected)|{'schema','template_only','root_complete_recovery_sources_and_review_read','ready_for_execution','unresolved_findings','fresh_independent_recovery_review','recovery_packet_manifest_sha256'},'Unknown/missing recovery authority fields')
 source_check();packet=c['root']/'RECOVERY_MANIFEST.json';need(pin(packet.read_bytes())['sha256']==a['recovery_packet_manifest_sha256'],'Recovery packet differs');review=a['fresh_independent_recovery_review'];need(type(review) is dict and set(review)=={'receipt_path','receipt_pin','manifest_path','manifest_pin'},'Exact new recovery review required')
 def repo_read(name,expected):
  need(type(name) is str and name and not any(ch in name for ch in ['\\',':','\0']),'Unsafe recovery review path');rel=PurePosixPath(name);need(not rel.is_absolute() and rel.as_posix()==name and all(x not in {'','.','..'} for x in name.split('/')),'Recovery review path escapes repository');return readpin(c['root'].parents[3]/name,expected)
 read=receipt_read or repo_read;receipt=strict(read(review['receipt_path'],review['receipt_pin']));read(review['manifest_path'],review['manifest_pin']);need(receipt.get('schema')=='pr1208-samecase-recovery-review-v1' and receipt.get('pr')==1208 and receipt.get('adapter_source_sha256')==c['source_sha'] and receipt.get('status')=='PASS' and receipt.get('fresh_independent_review') is True and receipt.get('unresolved_findings')==[],'Fresh exact recovery review has not passed');preserved(c);return a

def action_precheck(c,action):
 if action=='integrate':
  names={p.name for p in c['case'].iterdir()};need(not any(n.startswith('GIT_') for n in names) and not names&{'INTEGRATION_VERIFIED.json','INTEGRATION_OBJECTS_VERIFIED.json','RECOVERY01_INTEGRATION_RESUME_INTENT.json'},'Prior Git/recovery attempt forbids integration retry')

def head_for(c,action):
 if action=='integrate':return '5b238897f7e3f1008bd44c2cc5b5a01d8fbeae51'
 for name in ['INTEGRATION_VERIFIED.json','GIT_BRANCH_INTENT.json']:
  p=c['case']/name
  if p.exists():
   v=strict(p.read_bytes());h=v.get('head') if name.startswith('INTEGRATION_') else v['request']['sha'];need(type(h) is str and re.fullmatch('[a-f0-9]{40}',h),'Known head differs');return h
 need(action=='reconcile','No known integrated/attempted head; GET-only reconcile required');return '5b238897f7e3f1008bd44c2cc5b5a01d8fbeae51'


def packet_check(root,expected_sha):
 raw=(root/'RECOVERY_MANIFEST.json').read_bytes();need(pin(raw)['sha256']==expected_sha and (root/'RECOVERY_MANIFEST.sha256').read_text()==expected_sha+'  RECOVERY_MANIFEST.json\n','Exact recovery outer seal differs');m=strict(raw)
 files={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file()};dirs={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_dir()};need(files=={e['path'] for e in m['files']}|{'RECOVERY_MANIFEST.json','RECOVERY_MANIFEST.sha256'} and dirs=={e['path'] for e in m['directories']},'Exact recovery packet namespace differs')
 for e in m['files']+m['directories']:
  path=root/e['path'];st=path.lstat();need(not path.is_symlink() and st.st_mode&0o777==e['mode'] and st.st_mtime_ns==e['mtime_ns'] and st.st_nlink==e['nlink'],'Exact recovery packet stat differs')
  if 'sha256' in e:need(pin(path.read_bytes())=={k:e[k] for k in ['bytes','sha256']},'Recovery packet bytes differ')
 return True
