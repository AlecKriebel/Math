"""Independent ROOT check of the complete real PR43 merge and present native event."""
from pathlib import Path
import copy,datetime as dt,hashlib,json,stat,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];K=R/'unsolved_math_prioritization/attempts/30004386';B=A.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def eq(x,y):
    if type(x)is not type(y):return False
    if type(x)is dict:return set(x)==set(y)and all(eq(x[k],y[k])for k in x)
    if type(x)is list:return len(x)==len(y)and all(eq(a,b)for a,b in zip(x,y))
    return x==y
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def main():
    assert __debug__
    (A/'ROOT_POST_INSPECTION_PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    pre=load(A/'integration_preflight.json');post=load(A/'post_acceptance_verification.json');accept=load(A/'acceptance.json');canonical=load(K/'acceptance.json');overlay=load(A/'integration_check.json');final=load(A/'integration_finalization.json');fresh=load(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json')
    assert post['status']=='PASS'and type(post['program_completed_count'])is int and post['program_completed_count']==33 and post['full_problem_solved']is False
    merge=accept['merge_commit'];assert merge==post['merge_commit']==final['merge_commit']
    assert git('show','-s','--format=%P',merge).decode().strip().split()==[pre['main_before'],'86be0f85c7a37a5cad8d24abd16a32d8d1f27e62']
    assert git('show','-s','--format=%T',merge).decode().strip()==post['merge_tree']==accept['merge_tree']
    assert eq(canonical,{k:v for k,v in accept.items()if k not in {'canonical_manifest_entries','canonical_manifest_sha256'}})
    m=load(K/'MANIFEST.json');assert len(m['files'])==m['files_count']==accept['canonical_manifest_entries']==357 and m['self_excluded']==['MANIFEST.json']and sha((K/'MANIFEST.json').read_bytes())==accept['canonical_manifest_sha256']
    files={p.relative_to(K).as_posix()for p in K.rglob('*')if p.is_file()};assert files=={z['path']for z in m['files']}|{'MANIFEST.json'}
    for q in K.rglob('*'):assert not q.is_symlink()and(q.is_dir()or(q.is_file()and stat.S_IMODE(q.stat().st_mode)==0o444))
    for z in m['files']:
        b=(K/z['path']).read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
    expected_paths={K.relative_to(R).as_posix()+'/'+z['path']for z in overlay['canonical_overlay_files']}|{'unsolved_math_prioritization/QUEUE.md'}
    assert set(git('diff','--name-only',pre['main_before'],merge).decode().splitlines())==expected_paths
    for z in overlay['canonical_overlay_files']:
        b=git('show',merge+':'+K.relative_to(R).as_posix()+'/'+z['path']);assert len(b)==z['bytes']and sha(b)==z['sha256']
    patch=load(K/'ACCEPTED_QUEUE_PATCH.json');before=(A/'integration_queue_before.md').read_bytes();queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();old=patch['row_before'].encode();new=patch['row_after'].encode()
    assert sha(before)==patch['whole_before_sha256']and sha(queue)==patch['whole_after_sha256']and before.replace(old,new,1)==queue and queue.replace(new,old,1)==before
    oc=old.split(b'|');nc=new.split(b'|');assert [i for i in range(len(oc))if oc[i]!=nc[i]]==[8,11]and oc[10]==nc[10]and oc[12]==nc[12]
    assert git('show',merge+':unsolved_math_prioritization/QUEUE.md')==queue
    prior=load(A/'integration_state_before.json');state=load(R/'unsolved_math_prioritization/state.json');plan=load(A/'state_mirror_plan.json');intent=load(A/'state_mirror_intent.json');receipt=load(A/'state_mirror_receipt.json')
    assert len(prior)==33 and len(state)==34 and set(state)==set(prior)|{'30004386'}and all(eq(v,state[k])for k,v in prior.items())and eq(state,plan['state_after'])
    oldh=(A/'integration_history_before.jsonl').read_bytes();newh=(R/'unsolved_math_prioritization/history.jsonl').read_bytes();assert newh==oldh+plan['history_append_bytes'].encode()and len(plan['history_append'])==1
    event=json.loads(newh[len(oldh):]);assert eq(event,plan['history_append'][0])and event['id']=='30004386'and event['event']=='acceptance_mirror_import'and event['turns_used']==0 and event['turn_limit']==5 and event['status']=='already_solved'
    assert sum(v['turns_used']for v in state.values())==41 and intent['status']=='COMPLETED'and receipt['current_targets']==34 and receipt['primary_acceptances']==33 and receipt['history_events_added']==1 and receipt['new_proof_turns']==0
    inv=load(B/'inventory.json');before_inv=load(A/'integration_inventory_before.json');assert len(inv['items'])==180 and inv['completed_count']==33 and inv['current_pr']==44
    for olditem,newitem in zip(before_inv['items'],inv['items']):
        if olditem['number']!=43:assert eq(olditem,newitem)
    assert sum(z.get('stage')=='complete'for z in inv['items'])==33
    # Entire inventory is independently reconstructed, including all metadata.
    expected=copy.deepcopy(before_inv);chosen=next(z for z in expected['items']if z['number']==43)
    remote=load(A/'remote_merge_receipt.json')
    chosen.update(stage='complete',outcome='already_solved_accepted_partial',queue_status='already_solved',audited_head='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62',merge_commit=merge,merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='0/5',new_substantive_attempts=0,cumulative_attempts='0/5',paper_or_new_doi_or_tracker=False)
    expected.update(updated_at_utc=final['utc'],last_checkpoint_utc=final['utc'],completed_count=33,program_completion_estimate_percent=33/180*100,completion_estimate_percent=33/180*100,current_pr=44)
    assert eq(inv,expected)
    changed={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'};current13=[]
    for z in fresh['files']:
        q=R/z['path'];p=pin(q);assert stat.S_IMODE(q.stat().st_mode)==z['worktree_mode']
        if z['path']not in changed:assert p=={k:z[k]for k in ['path','bytes','sha256']}
        current13.append({**p,'worktree_mode':stat.S_IMODE(q.stat().st_mode)})
    captures=[]
    for phase,pid in [('preflight',71754),('overlay',73424),('prepush',73916),('finalize',74553),('mirror',75182),('post',76559)]:
        d=A/('root_'+phase+'_v2_actual_capture');c=load(d/'CAPTURE.json')
        assert c['actual_execution']is True and c['completed']is True and c['status']=='PASS'and c['exit_code']==0 and c['pid']==pid and c['source_unchanged']is True
        assert sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256']and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==sha((A/'run_actual_acceptance_phases_v2.py').read_bytes())
        for stream in ['stdout','stderr']:
            b=(d/c[stream]['path']).read_bytes();assert len(b)==c[stream]['bytes']and sha(b)==c[stream]['sha256']
        assert dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(c['finished_utc']);captures.append(pin(d/'CAPTURE.json'))
    observed=json.loads(subprocess.check_output(['gh','pr','view','43','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,headRefName,body,mergeCommit,mergedAt,url'],cwd=R));assert eq(observed,remote)
    result={'schema':'pr43-root-complete-actual-post-inspection/v1','status':'PASS','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'completed_primary_prs':33,'all33_prior_states_and_full_history_prefix_preserved':True,'current13_match_exact_allowed_acceptance_changes':True,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'entire_post':post,'canonical357_plus_manifest_fullbytes_modes':True,'merge355_overlay_plus_queue_Git_bodies_and_parents':True,'entire_current_inventory_reconstructed':True,'all_six_real_phase_captures':captures,'current13':current13,'original_attempts':0,'program_completion_percent':33/180*100}
    with(A/'ROOT_ACTUAL_POST_INSPECTION.json').open('x')as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'status':'PASS_COMPLETE_ACTUAL_ROOT_POST_INSPECTION','merge_commit':merge,'primary_acceptances':33,'targets':34,'consumed_substantive_turns':41,'inspection':pin(A/'ROOT_ACTUAL_POST_INSPECTION.json')}))
if __name__=='__main__':main()
