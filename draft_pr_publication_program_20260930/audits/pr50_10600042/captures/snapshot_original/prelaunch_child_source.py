"""Exact selected original GitHub Git-object snapshot; no Git refs or live files changed."""
from pathlib import Path
import base64, hashlib, json, os
from datetime import datetime, timezone
from capture_readonly import capture
H=Path(__file__).resolve().parent
HEAD='7260315f8b8b193020c09d4ef6df9d943a3a13ff'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX='unsolved_math_prioritization/attempts/10600042/'
def api(name,path):
    c,out,err=capture(name,['gh','api','repos/AlecKriebel/Math/'+path])
    assert c['exit_code']==0 and not err
    return json.loads(out)
def main():
    assert __debug__
    meta=json.loads((H/'captures/original_gh_metadata/stdout.bin').read_bytes())
    assert meta['number']==50 and meta['headRefOid']==HEAD and meta['baseRefOid']==BASE and meta['isDraft'] is True
    commit=api('git_head_commit','git/commits/'+HEAD);assert commit['sha']==HEAD
    tree=api('git_head_tree','git/trees/'+commit['tree']['sha']);chain=[]
    for name in ['unsolved_math_prioritization','attempts','10600042']:
        matches=[x for x in tree['tree'] if x['path']==name];assert len(matches)==1 and matches[0]['type']=='tree' and matches[0]['mode']=='040000'
        chain.append(matches[0]);tree=api('git_selected_tree_'+name,'git/trees/'+matches[0]['sha'])
    original=H/'original';original.mkdir();rows=[]
    def walk(obj,rel=''):
        assert obj['truncated'] is False
        for entry in obj['tree']:
            name=rel+entry['path'];assert '..' not in Path(name).parts and not Path(name).is_absolute()
            if entry['type']=='tree':
                assert entry['mode']=='040000';walk(api('git_subtree_'+name.replace('/','_'),'git/trees/'+entry['sha']),name+'/')
            else:
                assert entry['type']=='blob' and entry['mode'] in ['100644','100755']
                blob=api('git_blob_'+name.replace('/','_').replace('.','_'),'git/blobs/'+entry['sha']);assert blob['encoding']=='base64' and blob['sha']==entry['sha']
                data=base64.b64decode(blob['content']);assert len(data)==entry['size']==blob['size']
                assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['sha']
                p=original/name;p.parent.mkdir(parents=True,exist_ok=True)
                with p.open('xb') as f:f.write(data)
                p.chmod(0o444);rows.append({'path':name,'original_git_path':PREFIX+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha1':entry['sha'],'git_mode':entry['mode'],'snapshot_full_mode':0o444})
    walk(tree)
    expected={x['path'][len(PREFIX):] for x in meta['files'] if x['path'].startswith(PREFIX)}
    assert {x['path'] for x in rows}==expected and len(rows)==15
    result={'schema':'pr50-selected-original-git-snapshot/v1','created_utc':datetime.now(timezone.utc).isoformat(),'actual_snapshot_pid':os.getpid(),'pr':50,'head':HEAD,'base':BASE,'root_tree':commit['tree']['sha'],'selected_directory_tree':tree['sha'],'selected_tree_chain':chain,'files_count':len(rows),'files':sorted(rows,key=lambda x:x['path']),'snapshot_readonly':True,'live_native_index_ref_or_remote_mutated':False,'acceptance_approved':False}
    with (H/'ORIGINAL_MANIFEST.json').open('x') as f:f.write(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS_EXACT_SELECTED_ORIGINAL_SNAPSHOT','actual_pid':os.getpid(),'files':len(rows),'head':HEAD,'base':BASE,'live_native_index_ref_or_remote_mutated':False},sort_keys=True))
if __name__=='__main__':main()
