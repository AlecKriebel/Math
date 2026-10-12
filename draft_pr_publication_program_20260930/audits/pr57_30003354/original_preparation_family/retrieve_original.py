#!/usr/bin/env python3
"""Retrieve immutable first-party source and authenticate complete Git blobs/trees."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
from capture_command import HERE,run

REPO='AlecKriebel/Math'
HEAD='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX='unsolved_math_prioritization/attempts/30003354/'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def api(name,path,extra=()):
    cap,out,err=run(name,['gh','api',path]+list(extra))
    if cap['exit_code']!=0:raise RuntimeError(name+' failed; full capture retained')
    return json.loads(out)
cap,out,err=run('local_original_object',['git','cat-file','-t',HEAD],cwd='/Users/alec/Documents/Math')
metadata=api('api_pr_metadata','repos/'+REPO+'/pulls/57')
assert metadata['head']['sha']==HEAD and metadata['base']['sha']==BASE and metadata['draft'] and metadata['state']=='open'
compare=api('actual_merge_base','repos/'+REPO+'/compare/'+BASE+'...'+HEAD)
mergebase=compare['merge_base_commit']['sha']
commit=api('head_commit','repos/'+REPO+'/git/commits/'+HEAD)
trees=[]
def get_tree(name,oid,path):
    value=api(name,'repos/'+REPO+'/git/trees/'+oid)
    assert value['sha']==oid and not value['truncated']
    body=b''
    entries=sorted(value['tree'],key=lambda x:(x['path']+('/' if x['type']=='tree' else '')).encode())
    for item in entries:
        mode=str(int(item['mode'],8)) if False else item['mode'].lstrip('0')
        # Git tree's textual octal mode is 40000, 100644, etc.
        body+=mode.encode()+b' '+item['path'].encode()+b'\0'+bytes.fromhex(item['sha'])
    got=hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()
    assert got==oid,(path,got,oid)
    trees.append({'path':path,'sha':oid,'entry_count':len(entries),'full_binary_tree_hash_authenticated':True})
    return value['tree']
entries=get_tree('root_tree',commit['tree']['sha'],'')
path=''
for name in ['unsolved_math_prioritization','attempts','30003354']:
    item=next(x for x in entries if x['path']==name)
    assert item['type']=='tree'
    path=path+'/'+name if path else name
    entries=get_tree('tree_'+name,item['sha'],path)
blobs={}
def collect(entries,relative=''):
    for item in entries:
        if item['type']=='blob':blobs[PREFIX+relative+item['path']]=item
        else:
            assert item['type']=='tree'
            subrelative=relative+item['path']+'/'
            leaves=get_tree('tree_'+item['path'],item['sha'],PREFIX.rstrip('/')+'/'+subrelative.rstrip('/'))
            collect(leaves,subrelative)
collect(entries)
assert len(blobs)==17
cap,diff,err=run('full_original_diff',['gh','api','repos/'+REPO+'/pulls/57','-H','Accept: application/vnd.github.diff'])
assert cap['exit_code']==0
(HERE/'FULL_PR_DIFF.patch').write_bytes(diff)
parts=re.split(br'(?=^diff --git )',diff,flags=re.M)
original=HERE/'original';original.mkdir(exist_ok=False)
rows=[];queue=None
for part in parts:
    if not part:continue
    first=part.splitlines()[0].decode()
    match=re.match(r'diff --git a/(.+) b/(.+)$',first)
    assert match and match.group(1)==match.group(2)
    repository_path=match.group(2)
    if repository_path=='unsolved_math_prioritization/QUEUE.md':
        queue=part.decode();continue
    assert repository_path in blobs and b'new file mode 100644\n' in part
    lines=part.splitlines(keepends=True);inside=False;content=[]
    for line in lines:
        if line.startswith(b'@@ '):inside=True;continue
        if not inside:continue
        if line.startswith(b'+'):content.append(line[1:])
        elif line.startswith(b'\\ No newline at end of file'):
            assert content and content[-1].endswith(b'\n');content[-1]=content[-1][:-1]
        else:raise AssertionError('unexpected line in new-file diff '+repr(line))
    body=b''.join(content)
    got=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    assert got==blobs[repository_path]['sha']
    rel=repository_path[len(PREFIX):]
    p=original/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body)
    rows.append({'repository_path':repository_path,'relative_path':rel,'git_blob_sha1':got,
                 'git_mode':blobs[repository_path]['mode'],'bytes':len(body),'sha256':sha(body),
                 'local_path':str(p),'all_full_body_bytes_authenticated':True})
assert queue is not None and len(rows)==17 and len(parts)==19
changed=api('changed_files','repos/'+REPO+'/pulls/57/files?per_page=100')
assert len(changed)==18 and {x['filename'] for x in changed}==set(blobs)|{'unsolved_math_prioritization/QUEUE.md'}
for item in changed:
    if item['filename'] in blobs:assert item['sha']==blobs[item['filename']]['sha']
queueitem=next(x for x in changed if x['filename']=='unsolved_math_prioritization/QUEUE.md')
put('ORIGINAL_AUTHENTICATION.json',{'schema':'pr57-original-authentication/v1',
 'utc':datetime.now(timezone.utc).isoformat(),'original_head':HEAD,'github_base_oid':BASE,
 'actual_merge_base_oid':mergebase,'github_base_equals_actual_merge_base':BASE==mergebase,
 'branch':metadata['head']['ref'],'root_tree':commit['tree']['sha'],
 'original_science_file_count':17,'complete_diff_file_count':18,
 'original_science_files':sorted(rows,key=lambda x:x['relative_path']),
 'full_diff':{'path':str(HERE/'FULL_PR_DIFF.patch'),'bytes':len(diff),'sha256':sha(diff)},
 'authenticated_trees':trees,'original_queue_diff':queue,'original_queue_destination_blob_sha1':queueitem['sha'],
 'local_object_check_actual_exit':cap['exit_code'] if False else json.loads((HERE/'captures/local_original_object/CAPTURE.json').read_bytes())['exit_code'],
 'github_api_authority_is_not_a_signed_commit_certificate':True,
 'native_acceptance_ROOT_or_remote_authority':False})
print(json.dumps({'status':'AUTHENTIC_ORIGINAL_SOURCE_PREPARATION_ONLY','head':HEAD,
                  'actual_merge_base':mergebase,'science_files':17,'full_diff_bytes':len(diff),
                  'authenticated_trees':len(trees)},sort_keys=True))
