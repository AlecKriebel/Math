"""Independent read-only post-merge scope, integrity and claims evaluation."""
from pathlib import Path,PurePosixPath
import base64,datetime,gzip,hashlib,json,subprocess
R=Path(__file__).resolve().parent;A=R.parent;W=A.parents[2]
BASE='04c40062219cc9fa20834d98db2b270fdad1a848';HEAD='7821af7ddd84a4b3bb3168a11246f4b49ab0c5e8';MERGE='a7931795d85cd86c414200c5828d175046f707d5';ORIGINAL='f4039c9c093b10e651ee7fd2e6379073b84238c7'
TREE='194ef7dbd1f1a0d050400e68a61c6d166a54ef6e';BODY='90a8ee71e425f5b1c8f0873102ae6d3d6cb904fb5509d4a2b75b0fc4056a1626';MERGED_AT='2026-10-03T18:10:21Z'
REPO='repos/AlecKriebel/Math';PREFIX='unsolved_math_prioritization/attempts/2303016/';QUEUE='unsolved_math_prioritization/QUEUE.md'
PUB=R/'streams';PRIVATE=R/'private';PUB.mkdir(exist_ok=True);PRIVATE.mkdir(exist_ok=True)
commands=[];checks=0
sha=lambda b:hashlib.sha256(b).hexdigest()
def check(value):
    global checks
    assert value;checks+=1

def run(label,argv,private=False,compressed=False):
    result=subprocess.run(argv,cwd=W,capture_output=True)
    record={'label':label,'argv':argv,'cwd':str(W),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':result.returncode,'private':private,'compressed':compressed}
    directory=PRIVATE if private else PUB
    for stream,data in [('stdout',result.stdout),('stderr',result.stderr)]:
        p=directory/(label+'.'+stream+('.gz' if compressed else ''))
        p.write_bytes(gzip.compress(data,mtime=0) if compressed else data)
        record[stream+'_path']=str(p.relative_to(R));record[stream+'_bytes']=len(data);record[stream+'_sha256']=sha(data);record[stream+'_stored_sha256']=sha(p.read_bytes())
    commands.append(record)
    (R/'COMMANDS_PROGRESS.json').write_text(json.dumps(commands,indent=2)+'\n')
    check(result.returncode==0 and not result.stderr)
    return result.stdout

def api(label,endpoint):return json.loads(run(label,['gh','api',REPO+endpoint],private=True,compressed=True))
def tree(label,revision):
    data=run(label,['git','ls-tree','-rz',revision],compressed=True)
    entries={}
    for row in data.split(b'\0'):
        if not row:continue
        meta,path=row.split(b'\t',1);mode,kind,oid=meta.decode().split()
        entries[path.decode()]={'mode':mode,'type':kind,'blob':oid}
    return entries

def validate_tree(value):check(value==TREE)
def validate_body(value):check(sha(value)==BODY)
def validate_paths(paths,expected):check(paths==expected and len(paths)==22)
def validate_queue(base,merged):
    old=base.decode().splitlines(keepends=True);new=merged.decode().splitlines(keepends=True)
    check(len(old)==len(new)==1966)
    changes=[(i+1,a,b) for i,(a,b) in enumerate(zip(old,new)) if a!=b];check(len(changes)==1)
    line,before,after=changes[0];check(line==406 and '2303016 / AMR-022-3016' in before)
    check([i for i,(a,b) in enumerate(zip(before.split('|'),after.split('|'))) if a!=b]==[8,9])
    check(after==before.replace('| queued | 0/5 |','| already_solved | 1/5 |'))
    check(base.count(before.encode())==1 and base.replace(before.encode(),after.encode(),1)==merged)
    return {'line':line,'lines':len(old),'changed_cells':[8,9],'base_bytes':len(base),'merged_bytes':len(merged),'all_other_bytes_equal':True,'status':'already_solved','turns':'1/5'}

check(run('branch_start',['git','branch','--show-current']).decode().strip()=='main')
check(run('main_start',['git','rev-parse','main']).decode().strip()==MERGE)
check(run('checkout_start',['git','rev-parse','HEAD']).decode().strip()==MERGE)
check(run('remote_main_start',['git','ls-remote','origin','refs/heads/main']).decode().split()==[MERGE,'refs/heads/main'])
main_api=api('raw_api_main_start','/git/ref/heads/main');check(main_api['object']['sha']==MERGE)
pr=api('raw_merged_pr_start','/pulls/366')
check(pr['state']=='closed' and pr['merged'] is True and pr['merged_at']==MERGED_AT and pr['merge_commit_sha']==MERGE)
check(pr['head']['sha']==HEAD and pr['base']['sha']==BASE and pr['base']['ref']=='main')
body=pr['body'].encode();validate_body(body)
check(body==(A/'accepted_pr_body.txt').read_bytes()==(A/'clean_final_adversary/LIVE_ACCEPTED_PR_BODY.md').read_bytes())
(R/'ACTUAL_MERGED_PR_BODY.md').write_bytes(body)
merge_api=api('raw_actual_merge_commit','/git/commits/'+MERGE)
check([e['sha'] for e in merge_api['parents']]==[BASE,HEAD]);validate_tree(merge_api['tree']['sha'])
local_parents=run('actual_local_merge_parents',['git','show','-s','--format=%P',MERGE]).decode().split();check(local_parents==[BASE,HEAD])
validate_tree(run('actual_local_merge_tree',['git','rev-parse',MERGE+'^{tree}']).decode().strip())
validate_tree(run('prepared_local_tree',['git','rev-parse',HEAD+'^{tree}']).decode().strip())
for label,ancestor in [('base',BASE),('prepared',HEAD),('actual_merge',MERGE)]:
    run('main_ancestry_'+label,['git','merge-base','--is-ancestor',ancestor,'main'])
base_tree=tree('whole_base_tree',BASE);head_tree=tree('whole_prepared_tree',HEAD);merge_tree=tree('whole_actual_merge_tree',MERGE);original_tree=tree('whole_original_tree',ORIGINAL)
check(head_tree==merge_tree)
original_manifest=json.loads((A/'snapshot_manifest.json').read_text());expected={e['path'] for e in original_manifest['files']};check(len(expected)==22)
changed={p for p in base_tree.keys()|merge_tree.keys() if base_tree.get(p)!=merge_tree.get(p)};validate_paths(changed,expected)
check({p for p in merge_tree if p.startswith(PREFIX)}==expected-{QUEUE})
file_receipts=[];all_delta=[];original_bytes={}
for i,e in enumerate(original_manifest['files']):
    path=e['path'];original=(A/'snapshot'/path).read_bytes();original_bytes[path]=original
    check(len(original)==e['bytes'] and sha(original)==e['sha256'])
    actual=run('actual_blob_'+str(i),['git','show',MERGE+':'+path])
    entry=merge_tree[path];blob=hashlib.sha1(('blob '+str(len(actual))+'\0').encode()+actual).hexdigest()
    check(entry=={'mode':'100644','type':'blob','blob':blob})
    check(actual==(W/path).read_bytes() and not (W/path).is_symlink())
    source=api('remote_merge_content_'+str(i),'/contents/'+path+'?ref='+MERGE)
    check(source['path']==path and source['type']=='file' and source['sha']==blob and source['size']==len(actual))
    check(source['encoding']=='base64' and base64.b64decode(source['content'])==actual)
    if path!=QUEUE:
        head_source=api('remote_head_content_'+str(i),'/contents/'+path+'?ref='+HEAD)
        check(head_source['path']==path and head_source['type']=='file' and head_source['sha']==blob and head_source['size']==len(actual))
        check(head_source['encoding']=='base64' and base64.b64decode(head_source['content'])==actual==original)
        check(original_tree[path]==entry==head_tree[path])
    file_receipts.append({'path':path,'bytes':len(actual),'sha256':sha(actual),'git_blob':blob,'mode':entry['mode'],'type':entry['type'],'actual_worktree_equal':True,'whole_actual_merge_remote_equal':True,'whole_prepared_remote_equal':path!=QUEUE,'original_target_equal':path!=QUEUE})
    all_delta.append({'path':path,'before':base_tree.get(path),'after':entry})
check(len(file_receipts)==22 and sum(e['original_target_equal'] for e in file_receipts)==21)
baseq=run('entire_literal_base_queue',['git','show',BASE+':'+QUEUE]);actualq=(W/QUEUE).read_bytes()
queue=validate_queue(baseq,actualq)
run('actual_queue_diff',['git','diff','--unified=2',BASE,MERGE,'--',QUEUE])
# All nested bindings are evaluated directly from the actual merged files.
nested=[]
packet=W/PREFIX
for manifest in ['TURN_1_MANIFEST.json','FINAL_FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json','final_review/REVIEW_MANIFEST.json']:
    mp=packet/manifest
    for e in json.loads(mp.read_text())['files']:
        q=PurePosixPath(e['path']);check(not q.is_absolute() and '..' not in q.parts)
        b=(mp.parent/e['path']).read_bytes();check(len(b)==e['bytes'] and sha(b)==e['sha256'])
        nested.append({'manifest':manifest,**e})
check(len(nested)==48)
publication=json.loads((packet/'PUBLICATION_MANIFEST.json').read_text())
check(publication['author_manifest_sha256']==sha((packet/'FINAL_FROZEN_MANIFEST.json').read_bytes()))
check(publication['review_manifest_sha256']==sha((packet/'final_review/REVIEW_MANIFEST.json').read_bytes()))
# Earlier independent baselines, all three closed public inventories and immutable seals remain unchanged.
manifest_pins=[('priority_method_review','REVIEW_MANIFEST.json','c37d071fcafdb11d26332a185676a381b2af8746e9855669075c98ec1e0d646d',8,{'private_replays','private_sources','replays','__pycache__'}),('variational_capacity_review','IMMUTABLE_MANIFEST.json','aa86e6f71ddeb7ea73ac13729035cbe0bb846a5aac7d12a9b6200e4ed97d2358',26,{'private'}),('clean_final_adversary','IMMUTABLE_MANIFEST.json','aa40b05b683b74d4d24e34bb9eb3c76bacc8fb6f9c37f4da183faad29e320636',194,{'private_sources','private_replay','__pycache__'})]
closed=[]
for family,manifest,pin,count,ignored in manifest_pins:
    directory=A/family;raw=(directory/manifest).read_bytes();check(sha(raw)==pin)
    entries=json.loads(raw)['files'];check(len(entries)==count and len({e['path'] for e in entries})==count)
    actual_names={p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file() and not set(p.relative_to(directory).parts)&ignored and p.name not in {manifest,'FINAL_SEAL.json'}}
    check(actual_names=={e['path'] for e in entries})
    for e in entries:
        b=(directory/e['path']).read_bytes();check(len(b)==e['bytes'] and sha(b)==e['sha256'])
    closed.append({'family':family,'manifest':manifest,'sha256':pin,'public_files':count,'all_closed_files_unchanged':True})
check(sha((A/'clean_final_adversary/FINAL_SEAL.json').read_bytes())=='326455cb355e429c8e397776326a38d1f8b7d1f403f8e8b5d2fde6887eedc634')
check(sha((A/'clean_final_adversary/verify_audit.py').read_bytes())=='6707098856437479b6b40f78cc878b96e8da18020557d47dd7af6c1f42454700')
source_receipt=json.loads((A/'clean_final_adversary/PRIMARY_SOURCE_RECEIPTS.json').read_text())
source_pins={'hayman_lingham_2018':(1706228,'8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0'),'hedberg_wolff_1983':(1782353,'f351a967ae723f590d85da9a886ca4f6d8a1a21f7de8315f83180d9dcf3b5006')}
for e in source_receipt['receipts']:
    check((e['size'],e['sha256'])==source_pins[e['name']]);p=Path(e['original_pdf_path']);b=p.read_bytes();check(len(b)==e['size'] and sha(b)==e['sha256'])
# Deliberate wrong-tree/body/path/queue hypotheses must be rejected by the real invariants.
negative=[]
def reject(label,func):
    try:func()
    except AssertionError:negative.append({'mutation':label,'rejected':True});return
    raise AssertionError('negative control survived: '+label)
reject('wrong actual merge tree',lambda:validate_tree('0'*40))
reject('altered full remote PR body',lambda:validate_body(body+b'\n'))
reject('unexpected outside-target changed path',lambda:validate_paths(changed|{'unexpected.txt'},expected))
reject('wrong target queue turn cell',lambda:validate_queue(baseq,actualq.replace(b'| already_solved | 1/5 |',b'| already_solved | 2/5 |',1)))
check(len(negative)==4)
# Fresh raw actual state is checked again after all complete remote bytes were retrieved.
check(run('local_main_end',['git','rev-parse','main']).decode().strip()==MERGE)
check(run('remote_main_end',['git','ls-remote','origin','refs/heads/main']).decode().split()==[MERGE,'refs/heads/main'])
check(api('raw_api_main_end','/git/ref/heads/main')['object']['sha']==MERGE)
end=api('raw_merged_pr_end','/pulls/366')
check(end['state']=='closed' and end['merged'] is True and end['merged_at']==MERGED_AT and end['merge_commit_sha']==MERGE and end['head']['sha']==HEAD and end['base']['sha']==BASE)
check(end['body'].encode()==body)
out={'status':'PASS actual independent post-merge scope/claims review','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'assertions':checks,'actual_merge':MERGE,'actual_parents':local_parents,'actual_tree':TREE,'prepared_head':HEAD,'literal_base':BASE,'original_head':ORIGINAL,'merged_at':MERGED_AT,'body_sha256':BODY,'remote_state':'CLOSED and merged','local_remote_main_at_both_ends':MERGE,'all_root_changed_entries':all_delta,'whole_file_receipts':file_receipts,'original_target_files_unchanged':21,'remote_contents_fetched':43,'queue':queue,'nested_bindings':nested,'nested_binding_count':48,'earlier_closed_manifests':closed,'clean_final_194_file_seal_sha256':'326455cb355e429c8e397776326a38d1f8b7d1f403f8e8b5d2fde6887eedc634','primary_pdf_pins':source_pins,'negative_controls':negative,'commands':commands,'mathematical_evidence_transfer':'All 21 source/proof/code/review bytes and mode/type/blob entries are identical to the independently sealed original; exact 2690/1909/2590 controls and analytical verdict remain valid. No heavy mathematical recomputation was needed.','completion':{'post_merge_review_percent':100,'credited_method_percent':100,'new_theorem_percent':0,'program_completed':23,'program_total':349,'program_percent':23/349*100},'remaining_gaps':['No essential mathematical or actual merge-scope gap within the credited direct-proof and precisely limited sharpness claims.','Novelty, exhaustive historical priority and arbitrary nonintegrable-gauge optimality are unproved and outside the accepted claim.','Root must independently replay this closed evidence and make its final publication checkpoint; no paper/Zenodo/DOI/tracker/release is warranted.']}
(R/'ACTUAL_POST_MERGE_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'assertions':checks,'actual_merge':MERGE,'actual_tree':TREE,'target_files':21,'scoped_remote_contents':43,'nested_bindings':48,'negative_controls':4,'queue_lines':queue['lines'],'closed_prior_public_files':228,'commands':len(commands),'post_merge_review_percent':100},indent=2))
