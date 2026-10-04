"""ROOT performs fresh checks and branches on every actual result before PR43 merge."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_checked_ready_and_original_merge_v2'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def check_inputs():
    f=read(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json');p=read(A/'integration_preflight.json')
    assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==f['current_head']==p['main_before']
    assert subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R)==b''
    assert not (R/'unsolved_math_prioritization/attempts/30004386').exists()
    assert subprocess.run(['git','rev-parse','-q','--verify','MERGE_HEAD'],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==1
    for z in f['files']:
        q=R/z['path'];b=q.read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']and stat.S_IMODE(q.stat().st_mode)==z['worktree_mode']
    for k,name in [('whole_queue_before_sha256','integration_queue_before.md'),('inventory_before_sha256','integration_inventory_before.json'),('state_before_sha256','integration_state_before.json'),('history_before_sha256','integration_history_before.jsonl')]:assert sha((A/name).read_bytes())==p[k]
    for z in p['foreign_logs']:
        q=R/z['path'];b=q.read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']and stat.S_IMODE(q.stat().st_mode)==z['worktree_mode']
    return f,p
def command(name,argv,expected):
    d=D/name;d.mkdir();start=dt.datetime.now(dt.timezone.utc).isoformat()
    c=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);b,e=c.communicate()
    r={'schema':'root-pr43-checked-command/v1','argv':argv,'cwd':str(R),'pid':c.pid,'started_utc':start,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_execution':True,'completed':True,'exit_code':c.returncode,'expected_exit':expected}
    for k,v in [('stdout',b),('stderr',e)]:
        (d/(k+'.bin')).write_bytes(v);r[k]={'path':k+'.bin','bytes':len(v),'sha256':sha(v)}
    (d/'CAPTURE.json').write_text(json.dumps(r,indent=2)+'\n')
    assert c.returncode==expected,(name,c.returncode,e.decode(errors='replace'))
    return b

def main():
    assert __debug__;D.mkdir();(D/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    f,p=check_inputs()
    b=command('remote_before',['gh','pr','view','43','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,body,mergeCommit,mergedAt'],0);remote=json.loads(b)
    assert remote['number']==43 and remote['state']=='OPEN'and remote['isDraft']is True and remote['headRefOid']=='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62'and remote['mergeCommit']is None and remote['mergedAt']is None
    check_inputs()
    command('body_edit',['gh','pr','edit','43','--repo','AlecKriebel/Math','--body-file',str(A/'accepted_pr_body.md')],0)
    remote=json.loads(command('remote_after_body',['gh','pr','view','43','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,body,mergeCommit,mergedAt'],0))
    assert remote['body']==(A/'accepted_pr_body.md').read_text()and remote['headRefOid']=='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62'and remote['state']=='OPEN'and remote['isDraft']is True
    check_inputs()
    command('ready',['gh','pr','ready','43','--repo','AlecKriebel/Math'],0)
    check_inputs() # A failed main/index/body check stops this script before the merge.
    command('original_merge',['git','merge','--no-ff','--no-commit','86be0f85c7a37a5cad8d24abd16a32d8d1f27e62'],1)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==f['current_head']
    assert subprocess.check_output(['git','rev-parse','MERGE_HEAD'],cwd=R).decode().strip()=='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62'
    assert subprocess.check_output(['git','diff','--name-only','--diff-filter=U'],cwd=R).decode().splitlines()==['unsolved_math_prioritization/QUEUE.md']
    m=read(A/'snapshot_manifest.json');rows=m['files'];assert len(rows)==16
    for z in rows:
        rel=z['path'];q=A/'source_snapshot'/rel;candidate=R/'unsolved_math_prioritization/attempts/30004386'/rel
        assert candidate.read_bytes()==q.read_bytes()and len(q.read_bytes())==z['bytes']and sha(q.read_bytes())==z['sha256']
        assert subprocess.check_output(['git','ls-files','-s','--','unsolved_math_prioritization/attempts/30004386/'+rel],cwd=R).decode().startswith('100644 ')
    queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();(D/'merge_conflict_queue.md').write_bytes(queue)
    result={'schema':'root-pr43-checked-original-merge/v1','status':'PASS_EXPECTED_QUEUE_CONFLICT_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'main_before':f['current_head'],'original_head':'86be0f85c7a37a5cad8d24abd16a32d8d1f27e62','original16_bytes_and_modes_verified':True,'merge_queue_preimage_sha256':sha(queue),'ready_and_merge_actual_child_captures_retained':True}
    (D/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
