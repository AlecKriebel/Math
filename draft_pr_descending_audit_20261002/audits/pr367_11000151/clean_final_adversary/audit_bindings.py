from pathlib import Path
from datetime import datetime,timezone
import base64,concurrent.futures,gzip,hashlib,json,subprocess
R=Path('/Users/alec/Documents/Math');O=R/'draft_pr_descending_audit_20261002/audits/pr367_11000151/clean_final_adversary';P='problems/11000151_artin_a5_quotient';H='d977c9564f079cde975a7b4261776eb9061c5f5f';B='efd29c05204703acca9a0860812f54b94fae54b1';D=O/'private_runtime/without_sources'
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def api(a):return subprocess.check_output(['gh','api','repos/AlecKriebel/Math/'+a])
def bind(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def stream(n):
 p=O/'fullstreams'/n
 return p.read_bytes() if p.exists() else gzip.decompress(p.with_name(p.name+'.gz').read_bytes())
ht,bt={},{}
(O/'receipts/api_trees').mkdir(exist_ok=True)
tree_cache={}
def tree(ref):
 if ref is None:return {}
 if ref not in tree_cache:
  raw=api('git/trees/'+ref);obj=json.loads(raw);assert not obj['truncated'];(O/'receipts/api_trees'/(ref+'.json.gz')).write_bytes(gzip.compress(raw,mtime=0));tree_cache[ref]={x['path']:x for x in obj['tree']}
 return tree_cache[ref]
def recurse(old,new,prefix=''):
 if old==new:return
 before,after=tree(old),tree(new)
 for name in sorted(set(before)|set(after)):
  a,b=before.get(name),after.get(name);path=prefix+name
  if a==b:continue
  if (a or b)['type']=='tree':
   assert a is None or a['type']=='tree';assert b is None or b['type']=='tree';recurse(a['sha'] if a else None,b['sha'] if b else None,path+'/')
  else:
   if a:bt[path]={**a,'path':path}
   if b:ht[path]={**b,'path':path}
recurse(B,H)
changes=sorted(set(ht)|set(bt))
assert changes==git('diff','--name-only',B,H).decode().splitlines() and len(changes)==44
assert all(p.startswith(P+'/') or p=='unsolved_math_prioritization/QUEUE.md' for p in changes)
pr=json.loads((O/'receipts/pr367_api.json').read_bytes());assert pr['head']['sha']==H and pr['base']['sha']==B
assert sorted(x['filename'] for x in json.loads((O/'receipts/pr367_files_api.json').read_bytes()))==changes
(O/'receipts/api_blobs').mkdir(exist_ok=True)
def checkfile(path):
 remote=ht[path];mode,kind,sha,_=git('ls-tree',H,'--',path).decode().split(None,3);assert (mode,kind,sha)==(remote['mode'],remote['type'],remote['sha']) and mode=='100644' and kind=='blob'
 cached=O/'receipts/api_blobs'/(sha+'.json.gz');raw=gzip.decompress(cached.read_bytes()) if cached.exists() else api('git/blobs/'+sha);obj=json.loads(raw);b=git('show',H+':'+path);assert base64.b64decode(obj['content'])==b and bind(b)['git_blob_sha']==sha
 cached.write_bytes(gzip.compress(raw,mtime=0))
 if path.startswith(P+'/'):assert (D/Path(path).relative_to(P)).read_bytes()==b
 return {'path':path,'mode':mode,'type':kind,'sha':sha,**bind(b),'api_full_bytes_equal':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:files=list(pool.map(checkfile,changes))
q0=git('show',B+':unsolved_math_prioritization/QUEUE.md').decode().splitlines();q1=git('show',H+':unsolved_math_prioritization/QUEUE.md').decode().splitlines();assert len(q0)==len(q1);qd=[(i,a,b) for i,(a,b) in enumerate(zip(q0,q1),1) if a!=b];assert len(qd)==1
line,a,b=qd[0];aa,bb=a.split('|'),b.split('|');cells=[i for i,(x,y) in enumerate(zip(aa,bb)) if x!=y];assert cells==[8,9] and aa[2].strip().startswith('11000151 ') and bb[8].strip()=='claimed_solved' and bb[9].strip()=='4/5'
aliases={'mcgbook.pdf':'mcgbook.pdf','positive-factorizations.pdf':'arxiv_1412.0352.pdf','positive-factorizations-published.pdf':'agt-v17-n3-p06-s.pdf'};manifests=[]
for f in sorted(D.rglob('*MANIFEST.json')):
 rows=[]
 for x in json.loads(f.read_bytes())['files']:
  name=x.get('path',x.get('name'));path=f.parent/name
  if f.name=='SOURCE_MANIFEST.json':path=O/'private_sources'/aliases[name]
  z=bind(path.read_bytes());assert z['bytes']==x['bytes'] and z['sha256']==x['sha256'];rows.append({'reference':name,'resolved':str(path.relative_to(O)),**x,'verified':True})
 manifests.append({'manifest':str(f.relative_to(D)),**bind(f.read_bytes()),'all_binding_records':rows})
add=json.loads((D/'SOURCE_ADDITION_T2.json').read_bytes());fresh=bind((O/'private_sources/basic-braids.pdf').read_bytes());assert fresh['bytes']==add['bytes'] and fresh['sha256']==add['sha256']
commits=['4a0d60738ffc0fe06668c5a85156717501196aa5','87962a85c66ca2b3448f2fe54c526443b25e72f4','52d0f255942d882f60e1fc1a23256cff7f886431','a440a519393bf4c68433c6a8cdd49b384d3bfca6'];history=[]
for turn,commit in enumerate(commits,1):
 paths=git('ls-tree','-r','--name-only',commit,'--',P).decode().splitlines();meta=git('show','-s','--format=%H%n%P%n%aI%n%cI%n%s',commit).decode().splitlines();rows=[]
 remote_raw=api('git/commits/'+commit);remote=json.loads(remote_raw);assert remote['sha']==commit and remote['tree']['sha']==git('rev-parse',commit+'^{tree}').decode().strip();(O/'receipts'/('checkpoint_'+str(turn)+'_api.json.gz')).write_bytes(gzip.compress(remote_raw,mtime=0))
 for path in paths:
  b=git('show',commit+':'+path);assert b==git('show',H+':'+path);rows.append({'path':path,**bind(b),'head_bytes_preserved':True})
 assert P+f'/TURN_{turn}.md' in paths;history.append({'turn':turn,'actual_commit':commit,'metadata':meta,'api_commit_tree_equal':True,'actual_recursive_files':rows})
for turn in [1,2,3]:
 receipt=json.loads((D/f'TURN_{turn}_REMOTE_RECEIPT.json').read_bytes());assert receipt['commit']==commits[turn-1]
 for x in receipt['files']:
  b=git('show',receipt['commit']+':'+P+'/'+x['name']);assert bind(b)['git_blob_sha']==x['sha'] and len(b)==x['size']
checks=[]
for mode in ['without_sources','with_sources']:
 for turn in range(1,5):
  assert stream(f'{mode}_check_turn_{turn}.stdout')==(D/f'TURN_{turn}_CHECKS.json').read_bytes();checks.append({'mode':mode,'turn':turn,'complete_stdout_byte_equal':True})
 for stem,expected in [('verify_turn_4_cpp','TURN_4_CPP_CHECKS.json'),('review_independent_check','review/INDEPENDENT_CHECKS.json'),('review_replay_author','review/AUTHOR_REPLAY.json')]:
  assert stream(f'{mode}_{stem}.stdout')==(D/expected).read_bytes();checks.append({'mode':mode,'program':stem,'complete_stdout_byte_equal':True})
 lines=stream(f'{mode}_cpp_stream.stdout').splitlines(keepends=True);records=[x for x in lines if x.startswith(b'S|')];assert len(records)==90921 and len(lines)==90922;sha=hashlib.sha256(b''.join(records)).hexdigest();assert sha==json.loads((D/'TURN_4_CHECKS.json').read_bytes())['canonical_action_stream_sha256'];checks.append({'mode':mode,'cpp_complete_record_stream_bytes':sum(map(len,records)),'records':len(records),'sha256':sha,'summary':json.loads(lines[-1])})
for row in json.loads((O/'receipts/replays.json').read_bytes()):
 assert row['exit_code']==0 and row['stderr']['bytes']==0
 if row['label'].startswith('without_sources_'):
  other=row['label'].replace('without_sources_','with_sources_',1)
  for channel in ['stdout','stderr']:assert stream(row['label']+'.'+channel)==stream(other+'.'+channel)
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','frozen_head':H,'base':B,'actual_git_api_file_count':len(files),'all_file_bindings':files,'full_recursive_scope_paths':changes,'queue_changed_line':line,'queue_only_changed_cell_indexes':cells,'all_nested_manifest_bindings':manifests,'source_addition_binding':{**add,**fresh},'actual_author_checkpoints':history,'all_complete_replay_byte_checks':checks,'source_presence_all_output_streams_identical':True,'publication_manifest_self_excluded':not any(x['path']=='PUBLICATION_MANIFEST.json' for x in json.loads((D/'PUBLICATION_MANIFEST.json').read_bytes())['files'])}
(O/'receipts/bindings_history_replays.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: all44 Git/API files, recursive scope, queue cells, all nested bindings, actual four checkpoints and complete replay bytes')
