from pathlib import Path
import json,subprocess,hashlib,base64,datetime
AUDIT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
PLAN=AUDIT/'tmp/root-receipts/MERGE_CONFLICT_PLAN.json'
plan=json.loads(PLAN.read_text())
source=json.loads((AUDIT/'ROOT_SOURCE_IDENTITY.json').read_text())
readiness=json.loads((AUDIT/'FINAL_READINESS.json').read_text())
checks={}; cache={}
def require(k,test):
 checks[k]=bool(test)
 if not test: raise RuntimeError('FAILED '+k)
def api(path):
 r=subprocess.run(['gh','api','repos/AlecKriebel/Math/'+path],capture_output=True,check=True)
 return json.loads(r.stdout)
def tree(sha):
 if sha in cache:return cache[sha]
 p=OUT/('tree_'+sha+'.json')
 d=json.loads(p.read_text()) if p.exists() else api('git/trees/'+sha)
 if not p.exists():p.write_text(json.dumps(d,indent=2)+'\n')
 require('tree_not_truncated_'+sha,d.get('truncated') is False)
 require('tree_declared_sha_'+sha,d['sha']==sha)
 entries=d['tree']; require('tree_unique_names_'+sha,len({e['path'] for e in entries})==len(entries))
 require('tree_flat_names_'+sha,all('/' not in e['path'] and '\x00' not in e['path'] for e in entries))
 # Git sorts tree entries as directories with a trailing slash.
 body=b''
 for e in sorted(entries,key=lambda e:e['path'].encode()+ (b'/' if e['type']=='tree' else b'')):
  mode=e['mode'].lstrip('0')
  body+=mode.encode()+b' '+e['path'].encode()+b'\x00'+bytes.fromhex(e['sha'])
 digest=hashlib.sha1(b'tree '+str(len(body)).encode()+b'\x00'+body).hexdigest()
 require('tree_hash_'+sha,digest==sha)
 cache[sha]={e['path']:e for e in entries};return cache[sha]
def leaves(sha,prefix):
 result={}
 for name,e in tree(sha).items():
  path=prefix+name
  if e['type']=='tree':result.update(leaves(e['sha'],path+'/'))
  else:result[path]=(e['mode'],e['type'],e['sha'])
 return result
def diff(a,b,prefix=''):
 ta=tree(a);tb=tree(b); result={}
 for name in sorted(set(ta)|set(tb)):
  ea=ta.get(name);eb=tb.get(name)
  if ea==eb:continue
  # JSON size property may differ only if sha changes; identity ignores incidental fields.
  if ea and eb and (ea['mode'],ea['type'],ea['sha'])==(eb['mode'],eb['type'],eb['sha']):continue
  p=prefix+name
  if ea and eb and ea['type']==eb['type']=='tree':result.update(diff(ea['sha'],eb['sha'],p+'/'))
  else:
   left=leaves(ea['sha'],p+'/') if ea and ea['type']=='tree' else ({p:(ea['mode'],ea['type'],ea['sha'])} if ea else {})
   right=leaves(eb['sha'],p+'/') if eb and eb['type']=='tree' else ({p:(eb['mode'],eb['type'],eb['sha'])} if eb else {})
   for f in set(left)|set(right):result[f]={'before':left.get(f),'after':right.get(f)}
 return result
def blob(sha):
 p=OUT/('blob_'+sha+'.json')
 d=json.loads(p.read_text()) if p.exists() else api('git/blobs/'+sha)
 if not p.exists():p.write_text(json.dumps(d,indent=2)+'\n')
 require('blob_encoding_'+sha,d['encoding']=='base64')
 b=base64.b64decode(d['content']); require('blob_size_'+sha,len(b)==d['size'])
 require('blob_hash_'+sha,hashlib.sha1(b'blob '+str(len(b)).encode()+b'\x00'+b).hexdigest()==sha)
 return b
commit=api('git/commits/'+plan['main_parent']);(OUT/'main_commit.json').write_text(json.dumps(commit,indent=2)+'\n')
require('main_commit_binds_tree',commit['sha']==plan['main_parent'] and commit['tree']['sha']==plan['main_tree'])
qfile=(AUDIT/'tmp/root-receipts/MERGE_CONFLICT_QUEUE.txt').read_bytes()
queue_sha=hashlib.sha1(b'blob '+str(len(qfile)).encode()+b'\x00'+qfile).hexdigest()
updates={r['path']:('100644','blob',r['git_blob']) for r in source['original_files']}
updates['unsolved_math_prioritization/QUEUE.md']=('100644','blob',queue_sha)
trie={}
for path,value in updates.items():
 t=trie
 parts=path.split('/')
 for part in parts[:-1]:t=t.setdefault(part,{})
 t[parts[-1]]=value
def apply(sha,up,prefix=''):
 entries=dict(tree(sha)) if sha else {}
 for name,value in up.items():
  previous=entries.get(name);path=prefix+name
  if isinstance(value,dict):
   require('no_tree_type_collision_'+path,previous is None or previous['type']=='tree')
   child=apply(previous['sha'] if previous else None,value,path+'/')
   entries[name]={'path':name,'mode':'040000','type':'tree','sha':child}
  else:
   require('source_collision_absent_or_identical_'+path,path=='unsolved_math_prioritization/QUEUE.md' or previous is None or (previous['mode'],previous['type'],previous['sha'])==value)
   entries[name]={'path':name,'mode':value[0],'type':value[1],'sha':value[2]}
 body=b''
 for e in sorted(entries.values(),key=lambda e:e['path'].encode()+(b'/' if e['type']=='tree' else b'')):
  body+=e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\x00'+bytes.fromhex(e['sha'])
 newsha=hashlib.sha1(b'tree '+str(len(body)).encode()+b'\x00'+body).hexdigest()
 cache[newsha]=entries
 return newsha
independent_expected_tree=apply(plan['main_tree'],trie)
require('independent_expected_root_matches_plan',independent_expected_tree==plan['expected_resulting_tree'])
changes=diff(plan['main_tree'],independent_expected_tree)
paths={r['path'] for r in source['original_files']};queue='unsolved_math_prioritization/QUEUE.md'
require('exact_49_changed_paths',len(changes)==49 and set(changes)==paths|{queue})
for r in source['original_files']:
 c=changes[r['path']]
 require('original_add_'+r['path'],c['before'] is None and c['after']==('100644','blob',r['git_blob']))
q=changes[queue]; require('queue_modes',q['before'][:2]==q['after'][:2]==('100644','blob'))
qb=blob(q['before'][2]);qa=qfile
require('candidate_queue_blob_hash',hashlib.sha1(b'blob '+str(len(qa)).encode()+b'\x00'+qa).hexdigest()==q['after'][2])
old=plan['queue_before_row'].encode();new=plan['queue_after_row'].encode()
require('own_before_unique',qb.splitlines(keepends=True).count(old)==1)
require('own_after_unique',qa.splitlines(keepends=True).count(new)==1)
require('queue_exact_single_row_splice',qb.replace(old,new,1)==qa==qfile)
oldqueue=subprocess.run(['git','show',source['reviewed_head']+':'+queue],capture_output=True,check=True).stdout
oldrow=[x for x in oldqueue.splitlines(keepends=True) if b'| 4600024 /' in x]
require('queue_after_exact_original_candidate_row',oldrow==[new])
require('source_original_head_unchanged',source['reviewed_head']==plan['original_reviewed_candidate_head']=='4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f')
release=[]
for r in readiness['publication_files']:
 b=(AUDIT/'preprint'/r['path']).read_bytes();ok=len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']; require('six_frozen_'+r['path'],ok);release.append(dict(r,verified=ok))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS_PRE_MUTATION_TREE_AND_SCOPE','pr':781,'problem':'4600024','original_reviewed_candidate_head':source['reviewed_head'],'main_parent':plan['main_parent'],'main_tree':plan['main_tree'],'expected_resulting_tree':plan['expected_resulting_tree'],'plan_sha256':hashlib.sha256(PLAN.read_bytes()).hexdigest(),'checks':checks,'changed_paths':changes,'six_release_artifacts':release,'all_other_main_paths_preserved':True,'exact_unrelated_queue_bytes_preserved':True,'independent_Git_tree_hash_reconstruction':True,'head_binding_position':'Administrative reviewed_head may bind constructed new commit only with original_reviewed_candidate_head retained, explicit post-review identity/scope basis, exact source-preservation receipt; original ROOT_SOURCE_IDENTITY and frozen paper/review/deposit inputs remain unchanged. No claim of renewed substantive peer review.','extra_whole_paper_peer_review_required':False,'remaining_conditions':['Constructed commit exact ordered parents and tree','Fresh remote PR old-head precondition and ordinary fast-forward update','Exact constructed-head source-preservation readback plus native acceptance','Server merge exact-head verification'],'completion_estimate_percent':70,'exceptions':['No Git refs/index/checkout mutated; read-only GitHub API only','Verification attests pinned main and candidate tree, not future remote main state','No mathematical, literature, or publication-quality review repeated']}
(OUT/'PRE_MUTATION_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
with (OUT/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+result['utc']+' — Reconstructed all fetched nonrecursive Git-tree and blob hashes; compared proposed tree against fresh pinned main, exactly 48 original additions plus own QUEUE-row splice. Six frozen artifacts exact. Completion estimate: 70%; commit/head/native acceptance still pending.\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','changed_paths','six_release_artifacts')},indent=2))
