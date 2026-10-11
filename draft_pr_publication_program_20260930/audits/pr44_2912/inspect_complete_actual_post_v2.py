"""Independent ROOT check of the complete real PR44 merge and present native event."""
from pathlib import Path
import copy,datetime as dt,hashlib,json,stat,subprocess,sys,os
A=Path(__file__).resolve().parent;R=A.parents[2];K=R/'unsolved_math_prioritization/attempts/2912';B=A.parents[1]
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
    if sys.flags.optimize!=0 or os.environ.get('PYTHONOPTIMIZE','')not in ('','0'):raise RuntimeError('Nonoptimized verification runtime required')
    assert __debug__
    (A/'ROOT_POST_INSPECTION_PRELAUNCH_SOURCE_V2.py').write_bytes(Path(__file__).read_bytes())
    pre=load(A/'integration_preflight.json');post=load(A/'post_acceptance_verification.json');accept=load(A/'acceptance.json');canonical=load(K/'acceptance.json');overlay=load(A/'integration_check.json');final=load(A/'integration_finalization.json');fresh=load(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES_V2.json')
    assert post['status']=='PASS'and type(post['program_completed_count'])is int and post['program_completed_count']==34 and post['full_problem_solved']is False
    merge=accept['merge_commit'];assert merge==post['merge_commit']==final['merge_commit']
    assert git('show','-s','--format=%P',merge).decode().strip().split()==[pre['main_before'],'c772dc5b851ec91da9d46d534577609e5d3ca389']
    assert git('show','-s','--format=%T',merge).decode().strip()==post['merge_tree']==accept['merge_tree']
    assert eq(canonical,{k:v for k,v in accept.items()if k not in {'canonical_manifest_entries','canonical_manifest_sha256'}})
    m=load(K/'MANIFEST.json');assert len(m['files'])==m['files_count']==accept['canonical_manifest_entries']==440 and m['self_excluded']==['MANIFEST.json']and sha((K/'MANIFEST.json').read_bytes())==accept['canonical_manifest_sha256']
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
    oc=old.split(b'|');nc=new.split(b'|');assert [i for i in range(len(oc))if oc[i]!=nc[i]]==[8,9,11]and oc[10]==nc[10]and oc[12]==nc[12]
    assert git('show',merge+':unsolved_math_prioritization/QUEUE.md')==queue
    prior=load(A/'integration_state_before.json');state=load(R/'unsolved_math_prioritization/state.json');plan=load(A/'state_mirror_plan.json');intent=load(A/'state_mirror_intent.json');receipt=load(A/'state_mirror_receipt.json')
    assert len(prior)==34 and len(state)==35 and set(state)==set(prior)|{'2912'}and all(eq(v,state[k])for k,v in prior.items())and eq(state,plan['state_after'])
    oldh=(A/'integration_history_before.jsonl').read_bytes();newh=(R/'unsolved_math_prioritization/history.jsonl').read_bytes();assert newh==oldh+plan['history_append_bytes'].encode()and len(plan['history_append'])==1
    event=json.loads(newh[len(oldh):]);assert eq(event,plan['history_append'][0])and event['id']=='2912'and event['event']=='acceptance_mirror_import'and event['turns_used']==2 and event['turn_limit']==5 and event['status']=='unsolved'
    assert sum(v['turns_used']for v in state.values())==43 and intent['status']=='COMPLETED'and receipt['current_targets']==35 and receipt['primary_acceptances']==34 and receipt['history_events_added']==1 and receipt['new_proof_turns']==0
    inv=load(B/'inventory.json');before_inv=load(A/'integration_inventory_before.json');assert len(inv['items'])==180 and inv['completed_count']==34 and inv['current_pr']==45
    for olditem,newitem in zip(before_inv['items'],inv['items']):
        if olditem['number']!=44:assert eq(olditem,newitem)
    assert sum(z.get('stage')=='complete'for z in inv['items'])==34
    # Entire inventory is independently reconstructed, including all metadata.
    expected=copy.deepcopy(before_inv);chosen=next(z for z in expected['items']if z['number']==44)
    remote=load(A/'remote_merge_receipt.json')
    chosen.update(stage='complete',outcome='unsolved_accepted_partial',queue_status='unsolved',audited_head='c772dc5b851ec91da9d46d534577609e5d3ca389',merge_commit=merge,merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='2/5',new_substantive_attempts=0,cumulative_attempts='2/5',paper_or_new_doi_or_tracker=False)
    expected.update(updated_at_utc=final['utc'],last_checkpoint_utc=final['utc'],completed_count=34,program_completion_estimate_percent=34/180*100,completion_estimate_percent=34/180*100,current_pr=45)
    assert eq(inv,expected)
    changed={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'};current13=[]
    for z in fresh['files']:
        q=R/z['path'];p=pin(q);assert stat.S_IMODE(q.stat().st_mode)==z['worktree_mode']
        if z['path']not in changed:assert p=={k:z[k]for k in ['path','bytes','sha256']}
        current13.append({**p,'worktree_mode':stat.S_IMODE(q.stat().st_mode)})
    captures=[]
    for phase,pid in [('preflight_retry2',33183),('overlay',34249),('prepush',34829),('finalize',35635),('mirror',36340),('post',38024)]:
        d=A/('root_'+phase+'_actual_capture');c=load(d/'CAPTURE.json')
        assert c['actual_execution']is True and c['completed']is True and c['status']=='PASS'and c['exit_code']==0 and c['pid']==pid and c['source_unchanged']is True
        assert sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256']and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==sha((A/'run_actual_acceptance_phases_v2.py').read_bytes())
        for stream in ['stdout','stderr']:
            b=(d/c[stream]['path']).read_bytes();assert len(b)==c[stream]['bytes']and sha(b)==c[stream]['sha256']
        assert dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(c['finished_utc']);captures.append(pin(d/'CAPTURE.json'))
    # Explicit complete predecessor/proposal/saved-plan and fresh-noop replay.
    previous=load(A.parent/'pr43_30004386/state_mirror_bindings.json');proposal=load(A/'state_mirror_bindings.json')
    assert set(proposal)==set(previous)and eq(proposal['entries'][:-1],previous['entries'])and eq(proposal.get('duplicate_mirrors'),previous.get('duplicate_mirrors'))
    mutable={'entries','scope','created_at_utc','inventory','queue','required_completed_prs'}
    assert all(eq(proposal[k],previous[k])for k in previous if k not in mutable)
    assert proposal['required_completed_prs']==sorted(previous['required_completed_prs']+[44])and proposal['entries'][-1]['pr']==44 and proposal['entries'][-1]['id']=='2912'
    sys.path.insert(0,str(A/'acceptance_preparation_family'));import pr44_guards as g
    reconstructed=g.rebuild_saved_mirror_plan(proposal,plan['created_at_utc'],(A/'integration_state_before.json').read_bytes(),oldh)
    assert eq(reconstructed,plan)
    mod=g.mirror_module(proposal);s_before=(R/'unsolved_math_prioritization/state.json').read_bytes();h_before=(R/'unsolved_math_prioritization/history.jsonl').read_bytes();noop=mod.build_plan(R,proposal)
    assert not noop['history_append']and noop['state_after_bytes'].encode()==s_before and noop['history_append_bytes']==''and noop['history_after_sha256']==sha(h_before)
    assert (R/'unsolved_math_prioritization/state.json').read_bytes()==s_before and(R/'unsolved_math_prioritization/history.jsonl').read_bytes()==h_before
    tree_rows=git('ls-tree','-r','-z',merge).decode().split('\0');tree_modes={}
    for line in tree_rows:
        if line:fields,name=line.split('\t');tree_modes[name]=fields.split()[0]
    assert all(tree_modes[n]=='100644'for n in expected_paths)
    for z in load(A/'snapshot_manifest_v2.json')['files']:
        src=(A/'source_snapshot'/z['path']).read_bytes();assert(K/'original_archive'/z['path']).read_bytes()==src and len(src)==z['size']and sha(src)==z['sha256']
    for n in g.IMMUTABLE:assert(K/n).read_bytes()==(A/'source_snapshot'/n).read_bytes()
    contract=load(A/'acceptance_preparation_family/ROOT_POST_CONTRACT.json')
    assert all(eq(post[k],v)for k,v in contract['future44_required_entire_post_values'].items())
    observed=json.loads(subprocess.check_output(['gh','pr','view','44','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,headRefName,body,mergeCommit,mergedAt,url'],cwd=R));assert eq(observed,remote)
    result={'schema':'pr44-root-complete-actual-post-inspection/v1','status':'PASS','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'completed_primary_prs':34,'all34_prior_states_and_full_history_prefix_preserved':True,'current13_match_exact_allowed_acceptance_changes':True,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'entire_post':post,'canonical440_plus_manifest_fullbytes_modes':True,'merge438_overlay_plus_queue_Git_bodies_and_parents':True,'entire_current_inventory_reconstructed':True,'all_six_real_phase_captures':captures,'current13':current13,'original_attempts':2,'program_completion_percent':34/180*100,'entire_native_proposal_and_saved_plan_reconstructed':True,'fresh_noop_replayed_without_writes':True,'final_sealer_actual_capture':pin(A/'root_final_reconciliation_actual_capture/CAPTURE.json')}
    with(A/'ROOT_ACTUAL_POST_INSPECTION.json').open('x')as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'status':'PASS_COMPLETE_ACTUAL_ROOT_POST_INSPECTION','merge_commit':merge,'primary_acceptances':34,'targets':35,'consumed_substantive_turns':43,'inspection':pin(A/'ROOT_ACTUAL_POST_INSPECTION.json')}))
if __name__=='__main__':main()
