from pathlib import Path
import base64,datetime,gzip,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent;A=R.parent
HEAD='7821af7ddd84a4b3bb3168a11246f4b49ab0c5e8';BASE='04c40062219cc9fa20834d98db2b270fdad1a848';ORIGINAL='f4039c9c093b10e651ee7fd2e6379073b84238c7'
BODY_SHA='90a8ee71e425f5b1c8f0873102ae6d3d6cb904fb5509d4a2b75b0fc4056a1626'
REPO='repos/AlecKriebel/Math';PUB=R/'prepared_streams';PRIVATE=R/'private_replay';PUB.mkdir(exist_ok=True);PRIVATE.mkdir(exist_ok=True)
commands=[]
def sha(data):return hashlib.sha256(data).hexdigest()
def run(label,argv,private=False,compressed=False):
    z=subprocess.run(argv,capture_output=True)
    row={'label':label,'argv':argv,'exit':z.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'private':private,'compressed':compressed}
    directory=PRIVATE if private else PUB
    for name,data in [('stdout',z.stdout),('stderr',z.stderr)]:
        path=directory/(label+'.'+name+('.gz' if compressed else ''))
        path.write_bytes(gzip.compress(data,mtime=0) if compressed else data)
        row[name+'_path']=str(path.relative_to(R));row[name+'_bytes']=len(data);row[name+'_sha256']=sha(data)
        row[name+'_stored_sha256']=sha(path.read_bytes())
    commands.append(row)
    (R/'PREPARED_COMMANDS_PROGRESS.json').write_text(json.dumps(commands,indent=2)+'\n')
    assert z.returncode==0,(label,z.returncode,z.stderr.decode(errors='replace'))
    return z.stdout

def api(label,path):return json.loads(run(label,['gh','api',path],private=True,compressed=True))
def tree(label,ref):
    raw=run(label,['git','ls-tree','-rz',ref],compressed=True)
    result={}
    for row in raw.split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);mode,kind,blob=meta.split(b' ')
        result[path.decode()]={'mode':mode.decode(),'type':kind.decode(),'blob':blob.decode()}
    return result

source_manifest=json.loads((A/'snapshot_manifest.json').read_text())
repaired_manifest=json.loads((A/'repaired_snapshot_manifest.json').read_text())
assert repaired_manifest['head']==HEAD and repaired_manifest['base']==BASE and len(repaired_manifest['files'])==22
assert run('local_branch',['git','branch','--show-current']).decode().strip()=='main'
assert run('local_main',['git','rev-parse','main']).decode().strip()==BASE
remote_main=run('remote_main',['git','ls-remote','origin','refs/heads/main']).decode().split();assert remote_main==[BASE,'refs/heads/main']
remote_ref=api('api_main_ref',REPO+'/git/ref/heads/main');assert remote_ref['object']['sha']==BASE
pr=api('live_pr_start',REPO+'/pulls/366')
assert pr['state']=='open' and pr['draft'] is False and pr['head']['sha']==HEAD and pr['base']['sha']==BASE
assert pr['base']['ref']=='main' and pr['head']['repo']['full_name']=='AlecKriebel/Math'
assert pr['mergeable'] is True and pr['mergeable_state']=='clean'
body=pr['body'].encode();assert sha(body)==BODY_SHA and body==(A/'accepted_pr_body.txt').read_bytes()
(R/'LIVE_ACCEPTED_PR_BODY.md').write_bytes(body)
branch_ref=api('api_pr_branch_ref',REPO+'/git/ref/heads/'+pr['head']['ref']);assert branch_ref['object']['sha']==HEAD
head_commit=api('api_head_commit',REPO+'/git/commits/'+HEAD)
assert [p['sha'] for p in head_commit['parents']]==[ORIGINAL,BASE]
parents=run('local_head_parents',['git','show','-s','--format=%P',HEAD]).decode().strip().split();assert parents==[ORIGINAL,BASE]
base_tree=tree('entire_base_tree',BASE);head_tree=tree('entire_head_tree',HEAD);old_tree=tree('entire_original_tree',ORIGINAL)
changed={p for p in base_tree.keys()|head_tree.keys() if base_tree.get(p)!=head_tree.get(p)}
expected={e['path'] for e in repaired_manifest['files']};assert changed==expected and len(changed)==22
all_delta=[];target_bindings=[];contents_receipts=[]
for i,e in enumerate(repaired_manifest['files']):
    path=e['path'];data=(A/'repaired_snapshot'/path).read_bytes()
    assert len(data)==e['bytes'] and sha(data)==e['sha256']
    git_data=run('prepared_blob_'+str(i),['git','show',HEAD+':'+path]);assert git_data==data
    info=head_tree[path];assert info['mode']=='100644' and info['type']=='blob'
    blob=hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest();assert info['blob']==blob
    content=api('remote_content_'+str(i),REPO+'/contents/'+path+'?ref='+HEAD)
    assert content['path']==path and content['type']=='file' and content['sha']==blob and content['size']==len(data)
    assert content['encoding']=='base64';decoded=base64.b64decode(content['content']);assert decoded==data
    contents_receipts.append({'path':path,'bytes':len(data),'sha256':sha(data),'blob':blob,'remote_whole_bytes_equal':True})
    all_delta.append({'path':path,'before':base_tree.get(path),'after':info})
    if '/attempts/2303016/' in path:
        assert old_tree[path]==info
        assert data==(A/'snapshot'/path).read_bytes()
        target_bindings.append({'path':path,'mode_type_blob_unchanged':True,'bytes_sha256_unchanged':True})
assert len(target_bindings)==21
prfiles=api('remote_pr_files',REPO+'/pulls/366/files?per_page=100')
assert len(prfiles)==22 and {e['filename'] for e in prfiles}==expected
for e in prfiles:
    assert e['sha']==head_tree[e['filename']]['blob']
    assert e['status']==('modified' if e['filename']=='unsolved_math_prioritization/QUEUE.md' else 'added')
queue_path='unsolved_math_prioritization/QUEUE.md'
base_queue=run('literal_base_queue',['git','show',BASE+':'+queue_path]);head_queue=(A/'repaired_snapshot'/queue_path).read_bytes()
old=base_queue.decode().splitlines(keepends=True);new=head_queue.decode().splitlines(keepends=True)
assert len(old)==len(new)
diff=[(i+1,a,b) for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert len(diff)==1
line,before,after=diff[0];assert line==406 and '2303016 / AMR-022-3016' in before
old_cells=before.split('|');new_cells=after.split('|');assert len(old_cells)==len(new_cells)
cell_delta=[i for i,(a,b) in enumerate(zip(old_cells,new_cells)) if a!=b];assert cell_delta==[8,9]
assert after==before.replace('| queued | 0/5 |','| already_solved | 1/5 |')
# Reconstruct the entire queue; this validates every non-target byte as well as its line count.
reconstruction=bytearray(base_queue)
assert base_queue.count(before.encode())==1
assert base_queue.replace(before.encode(),after.encode(),1)==head_queue
run('literal_queue_diff',['git','diff','--unified=2',BASE,HEAD,'--',queue_path])
# All 48 bindings are rechecked against the prepared full bytes, not inherited PASS labels.
packet=A/'repaired_snapshot/unsolved_math_prioritization/attempts/2303016';nested=[]
for name in ['TURN_1_MANIFEST.json','FINAL_FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json','final_review/REVIEW_MANIFEST.json']:
    mp=packet/name
    for e in json.loads(mp.read_text())['files']:
        data=(mp.parent/e['path']).read_bytes();assert len(data)==e['bytes'] and sha(data)==e['sha256']
        nested.append({'manifest':name,'path':e['path'],'bytes':len(data),'sha256':sha(data)})
assert len(nested)==48
# Independently evaluate immutable approach evidence: every public hash and complete command capture.
family_pins=[('priority_method_review','REVIEW_MANIFEST.json','c37d071fcafdb11d26332a185676a381b2af8746e9855669075c98ec1e0d646d',8),('variational_capacity_review','IMMUTABLE_MANIFEST.json','aa86e6f71ddeb7ea73ac13729035cbe0bb846a5aac7d12a9b6200e4ed97d2358',26)]
family_results=[]
for family,manifest,pin,count in family_pins:
    fp=A/family;raw=(fp/manifest).read_bytes();assert sha(raw)==pin
    entries=json.loads(raw)['files'];assert len(entries)==count
    for e in entries:
        data=(fp/e['path']).read_bytes();assert len(data)==e['bytes'] and sha(data)==e['sha256'],(family,e['path'])
    family_results.append({'family':family,'manifest':manifest,'sha256':pin,'public_files':count,'all_public_hashes_equal':True})
# GitHub's actual test merge is independently bound to [literal base, literal head].
merge=pr['merge_commit_sha'];assert merge
merge_ref=run('actual_test_merge_ref',['git','ls-remote','origin','refs/pull/366/merge']).decode().split();assert merge_ref==[merge,'refs/pull/366/merge']
merge_commit=api('actual_test_merge_commit',REPO+'/git/commits/'+merge)
assert [p['sha'] for p in merge_commit['parents']]==[BASE,HEAD]
head_tree_oid=run('local_head_tree_oid',['git','rev-parse',HEAD+'^{tree}']).decode().strip()
assert merge_commit['tree']['sha']==head_tree_oid==head_commit['tree']['sha']
# Recheck the raw refs and full PR metadata/body after all contents were independently retrieved.
assert run('remote_main_end',['git','ls-remote','origin','refs/heads/main']).decode().split()==[BASE,'refs/heads/main']
assert run('local_main_end',['git','rev-parse','main']).decode().strip()==BASE
pr_end=api('live_pr_end',REPO+'/pulls/366')
assert pr_end['state']=='open' and not pr_end['draft'] and pr_end['head']['sha']==HEAD and pr_end['base']['sha']==BASE
assert pr_end['mergeable'] is True and pr_end['mergeable_state']=='clean' and pr_end['merge_commit_sha']==merge
assert pr_end['body'].encode()==body
receipt={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prepared_head':HEAD,'literal_base_local_remote_main':BASE,'original_head':ORIGINAL,'body_sha256':sha(body),'remote_state':'OPEN ready mergeable clean','refresh_parents':parents,'original_target_files_preserved':21,'live_scoped_remote_files':22,'full_root_changed_entries':all_delta,'remote_whole_file_receipts':contents_receipts,'target_preservation':target_bindings,'nested_bindings':nested,'queue':{'line':line,'lines':len(old),'base_bytes':len(base_queue),'head_bytes':len(head_queue),'changed_cells':cell_delta,'whole_non_target_bytes_preserved':True},'test_merge':{'sha':merge,'parents':[p['sha'] for p in merge_commit['parents']],'tree':merge_commit['tree']['sha'],'equal_to_prepared_head_tree':True},'family_manifests':family_results,'commands':commands,'no_mathematical_replay_required':'All 21 source/proof/code/review packet files and modes match the already wholly verified original. Original full captured checker outputs remain hash-bound.','limitations':['Snapshot evidence applies only to these literal pins and the recorded UTC observations. Root must enforce its own final guarded integration gate.','No merge, index, ref, publication or external-person mutation was performed.']}
(R/'PREPARED_HEAD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','head':HEAD,'base':BASE,'original_target_files_preserved':21,'remote_whole_files':22,'nested_bindings':48,'queue_line':line,'queue_lines':len(old),'test_merge':merge,'body_sha256':sha(body),'commands':len(commands)},indent=2))
