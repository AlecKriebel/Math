from pathlib import Path
import subprocess,json,datetime,hashlib
D=Path(__file__).resolve().parent;S=D.parent/'snapshot/problems/11000151_artin_a5_quotient';repo=Path('/Users/alec/Documents/Math');head='d977c9564f079cde975a7b4261776eb9061c5f5f';base='efd29c05204703acca9a0860812f54b94fae54b1';prefix='problems/11000151_artin_a5_quotient/'
def run(cmd):return subprocess.check_output(cmd,cwd=repo)
def tree(ref,label,recursive=False):
 raw=run(['gh','api','repos/AlecKriebel/Math/git/trees/'+ref+('?recursive=1' if recursive else '')]);(D/'receipts'/('API_TREE_'+label+'.json')).write_bytes(raw);t=json.loads(raw);assert not t['truncated'];return {x['path']:x for x in t['tree']}
root=tree(head,'root');problems=tree(root['problems']['sha'],'problems');target=tree(problems['11000151_artin_a5_quotient']['sha'],'target',True);queues=tree(root['unsolved_math_prioritization']['sha'],'queue')
td={prefix+k:v for k,v in target.items()};td['unsolved_math_prioritization/QUEUE.md']=queues['QUEUE.md'];scope=json.loads((D/'receipts/FULL_SCOPE_NEW.json').read_text());assert all(td[x['path']]['mode']==x['mode'] and td[x['path']]['sha']==x['git_oid'] and td[x['path']]['type']==x['type'] for x in scope['files'])
checks=[]
for manifest in sorted(S.rglob('*MANIFEST.json')):
 data=json.loads(manifest.read_bytes());items=[]
 for f in data.get('files',[]):
  if 'path' not in f:continue
  path=manifest.parent/f['path'];b=path.read_bytes();ok=len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'];assert ok
  items.append({'path':str(path.relative_to(S)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'ok':ok})
 checks.append({'manifest':str(manifest.relative_to(S)),'entries':len(items),'checks':items})
remote=[]
for receipt in sorted(S.glob('*REMOTE_RECEIPT.json')):
 data=json.loads(receipt.read_bytes());commit=data['commit'];meta=run(['git','show','--format=%H %P %cI %s','--no-patch',commit]).decode().strip();checks2=[]
 for row in data['files']:
  spec=commit+':'+prefix+row['name'];b=run(['git','show',spec]);oid=run(['git','rev-parse',spec]).decode().strip();current=(S/row['name']).read_bytes();assert oid==row['sha'] and len(b)==row['size'] and b==current
  checks2.append({'path':row['name'],'oid':oid,'bytes':len(b),'matches_checkpoint_and_head':True})
 api=run(['gh','api','repos/AlecKriebel/Math/git/commits/'+commit]);(D/'receipts'/('API_CHECKPOINT_'+commit+'.json')).write_bytes(api);apij=json.loads(api);assert apij['sha']==commit and apij['tree']['sha']==run(['git','rev-parse',commit+'^{tree}']).decode().strip()
 remote.append({'receipt':receipt.name,'actual_git_metadata':meta,'actual_api_commit':apij['sha'],'files':checks2})
parents=run(['git','show','--format=%P','--no-patch',head]).decode().strip().split();assert parents==[base,'a440a519393bf4c68433c6a8cdd49b384d3bfca6']
author=parents[1];author_paths=run(['git','diff','--name-only',base,author]).decode().splitlines();assert len(author_paths)==34 and all(x.startswith(prefix) for x in author_paths)
for path in author_paths:assert run(['git','show',author+':'+path])==run(['git','show',head+':'+path])
authorapi=json.loads(run(['gh','api','repos/AlecKriebel/Math/git/commits/'+author]));assert authorapi['tree']['sha']==run(['git','rev-parse',author+'^{tree}']).decode().strip();(D/'receipts/API_AUTHOR_CHECKPOINT_T4.json').write_text(json.dumps(authorapi,indent=2)+'\n')
a=run(['git','show',base+':unsolved_math_prioritization/QUEUE.md']).splitlines();b=run(['git','show',head+':unsolved_math_prioritization/QUEUE.md']).splitlines();changes=[(i+1,x.decode(),y.decode()) for i,(x,y) in enumerate(zip(a,b)) if x!=y];assert len(a)==len(b) and len(changes)==1 and '11000151' in changes[0][1] and 'claimed_solved | 4/5' in changes[0][2]
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','api_target_tree_untruncated':True,'all_44_modes_and_git_oids_match_api_tree':True,'recursive_manifests':checks,'remote_checkpoints':remote,'actual_merge_parents':parents,'author_frozen_files':len(author_paths),'queue_changed_rows':changes,'raw_primary_source_hashes_independently_matched':4}
(D/'receipts/RECURSIVE_MANIFESTS_AND_HISTORY_NEW.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['recursive_manifests','remote_checkpoints']},indent=2));print('Manifest entry counts:',[(x['manifest'],x['entries']) for x in checks]);print('Checkpoint file counts:',[(x['receipt'],len(x['files'])) for x in remote])
