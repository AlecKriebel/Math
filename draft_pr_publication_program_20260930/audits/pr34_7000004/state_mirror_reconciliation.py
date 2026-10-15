"""Incremental present acceptance mirror; original ledgers/history are preserved."""
from pathlib import Path
import argparse, copy, fcntl, importlib.util, json, subprocess
R=Path(__file__).resolve().parents[3]; B=R/'draft_pr_publication_program_20260930'; BASE=B/'infrastructure/accepted_state_sync'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pr',type=int,choices=[34,35],required=True);n=ap.parse_args().pr
    identity='7000004' if n==34 else '2744';used=2 if n==34 else 1;status='already_solved' if n==34 else 'unsolved'
    A=B/'audits'/('pr'+str(n)+'_'+identity);K=R/'unsolved_math_prioritization/attempts'/identity
    spec=importlib.util.spec_from_file_location('mirror',BASE/'revision2/accepted_state_sync_v2.py');mirror=importlib.util.module_from_spec(spec);spec.loader.exec_module(mirror)
    spec=importlib.util.spec_from_file_location('writer',BASE/'root_apply/guarded_import_v2.py');writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)
    old_ledger=mirror.ledger_budget
    def ledger(data,kind,amount,limit):
        if kind=='json_zero_source_triage':
            obj=json.loads(data);mirror.require(str(obj.get('problem_id'))=='30002145','Wrong zero-triage ID')
            mirror.require(amount==obj.get('used')==0 and limit==obj.get('limit')==5,'Zero-triage budget mismatch')
            mirror.require(obj.get('substantive_proof_attempts')==[] and isinstance(obj.get('reason'),str) and obj['reason'],'Ambiguous zero-triage ledger')
        elif kind=='json_substantive_responses':
            obj=json.loads(data);mirror.require(obj.get('problem_id')==2744 and obj.get('problem_number')=='KP-1.85','Wrong response ledger ID')
            mirror.require(type(obj.get('substantive_turns_used')) is int and amount==obj['substantive_turns_used']==1 and limit==obj.get('turn_limit')==5,'Original response budget mismatch')
            mirror.require(obj.get('outcome')=='unsolved' and isinstance(obj.get('responses'),list) and [z.get('turn') for z in obj['responses']]==[1],'Ambiguous response ledger')
            mirror.require(obj['responses'][0].get('outcome')=='unsolved' and obj['responses'][0].get('artifact')=='OBSTRUCTION.md','Changed historical response scope')
        else:old_ledger(data,kind,amount,limit)
    mirror.ledger_budget=ledger
    binding=lambda p:{'path':str(p.relative_to(R)),'sha256':mirror.sha(p.read_bytes())}
    assert not (A/'state_mirror_intent.json').exists(),'Inspect prior intent before retry'
    assert subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()=='main'
    remote=json.loads(subprocess.check_output(['gh','pr','view',str(n),'--json','number,url,state,isDraft,headRefOid,mergeCommit,mergedAt'],cwd=R))
    assert remote==mirror.load(A/'remote_merge_receipt.json')
    accept=mirror.load(K/'acceptance.json');assert remote['state']=='MERGED' and not remote['isDraft'] and remote['headRefOid']==accept['original_head'] and remote['mergeCommit']['oid']==accept['merge_commit']
    previous=B/'audits'/('pr32_6800007' if n==34 else 'pr34_7000004')/'state_mirror_bindings.json'
    proposal=mirror.load(previous);proposal.update(created_at_utc=writer.stamp(),scope='Incremental accepted primary PR'+str(n)+' and all prior source-bound acceptances; original ledgers/history unchanged, no reconstructed historical proof transitions.')
    for key in ['inventory','queue']:proposal[key]=binding(R/proposal[key]['path'])
    assert n not in proposal['required_completed_prs'];proposal['required_completed_prs']=sorted(proposal['required_completed_prs']+[n])
    proposal['entries'].append({'pr':n,'id':identity,'status':status,'acceptance':binding(K/'acceptance.json'),'audit_acceptance':binding(A/'acceptance.json'),'remote':binding(A/'remote_merge_receipt.json'),'accepted_source':binding(K/'source_record.json'),'canonical_acceptance_text':binding(K/'ACCEPTANCE.md'),'canonical_manifest':binding(K/'MANIFEST.json'),'artifact':{**binding(K/('RESULT.md' if n==34 else 'OBSTRUCTION.md')),'acceptance_hash_field':'canonical_scientific_artifact_sha256'},'budget':{'used':used,'limit':5,'kind':'jsonl_turns' if n==34 else 'json_substantive_responses','ledger':binding(K/('turns.jsonl' if n==34 else 'turns.json'))},'duplicates':[]})
    negatives=[]
    if n==34:
        original=[json.loads(x) for x in (K/'turns.jsonl').read_text().splitlines()]
        fixtures=[('missing charged second route',original[:1]),('duplicate turn',original+[original[1]]),('invented third turn',original+[dict(original[1],turn=3)]),('removed original response',original[1:])]
        for label,obj in fixtures:
            try:ledger(('\n'.join(json.dumps(x) for x in obj)+'\n').encode(),'jsonl_turns',2,5)
            except mirror.Rejected:negatives.append(label)
            else:raise AssertionError(label)
    else:
        original=mirror.load(K/'turns.json');fixtures=[]
        for label,key,value in [('wrong original target','problem_id',7000004),('reset consumed count','substantive_turns_used',0),('changed limit','turn_limit',6),('false solved outcome','outcome','claimed_solved'),('missing original response','responses',[]),('duplicate response','responses',original['responses']*2),('invented later response','responses',original['responses']+[dict(original['responses'][0],turn=2)])]:
            obj=copy.deepcopy(original);obj[key]=value;fixtures.append((label,obj))
        for label,obj in fixtures:
            try:ledger(json.dumps(obj).encode(),'json_substantive_responses',1,5)
            except mirror.Rejected:negatives.append(label)
            else:raise AssertionError(label)
    plan=mirror.build_plan(R,proposal);preflight=mirror.validate_plan(R,plan)
    prior=mirror.load(R/'unsolved_math_prioritization/state.json');old_count=24 if n==34 else 25;old_turns=28 if n==34 else 30
    assert len(prior)==old_count and identity not in prior and sum(x['turns_used'] for x in prior.values())==old_turns
    assert plan['primary_count']==old_count and plan['duplicate_count']==1 and [x['id'] for x in plan['history_append']]==[identity]
    assert all(plan['state_after'][k]==v for k,v in prior.items()) and sum(x['turns_used'] for x in plan['state_after'].values())==old_turns+used
    writer.atomic(A/'state_mirror_bindings.json',mirror.encode(proposal));writer.atomic(A/'state_mirror_plan.json',mirror.encode(plan))
    protected={z['path']:z['sha256'] for z in plan['bindings']};state=R/'unsolved_math_prioritization/state.json';history=R/'unsolved_math_prioritization/history.jsonl'
    with open(BASE/'tmp/root-accepted-state.lock','a+b') as lock:
        fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB);mirror.validate_plan(R,plan)
        intent={'status':'PREPARED','at_utc':writer.stamp(),'plan_sha256':mirror.sha(mirror.encode(plan)),'before':plan['preconditions'],'state_after_sha256':plan['state_after_sha256'],'history_after_sha256':plan['history_after_sha256'],'new_event':identity,'new_proof_turns':0}
        writer.atomic(A/'state_mirror_intent.json',mirror.encode(intent));old_state=state.read_bytes();old_history=history.read_bytes()
        assert mirror.sha(old_state)==plan['preconditions']['state_sha256'] and mirror.sha(old_history)==plan['preconditions']['history_sha256']
        writer.atomic(history,old_history+plan['history_append_bytes'].encode());assert state.read_bytes()==old_state
        writer.atomic(state,plan['state_after_bytes'].encode());assert mirror.sha(state.read_bytes())==plan['state_after_sha256'] and mirror.sha(history.read_bytes())==plan['history_after_sha256']
        assert all(mirror.sha((R/p).read_bytes())==s for p,s in protected.items())
        intent.update(status='COMPLETED',completed_at_utc=writer.stamp());writer.atomic(A/'state_mirror_intent.json',mirror.encode(intent))
        writer.atomic(A/'state_mirror_receipt.json',mirror.encode({'at_utc':writer.stamp(),'preflight':preflight,'negative_ledger_controls':negatives,'history_events_added':1,'prior_state_entries_semantically_unchanged':old_count,'current_targets':old_count+1,'consumed_substantive_turns':old_turns+used,'new_proof_turns_added_by_mirror':0,'original_ledger_bytes_unchanged':True,'protected_bindings_unchanged':len(protected),'legacy_generator_run':False,'state_sha256':mirror.sha(state.read_bytes()),'history_sha256':mirror.sha(history.read_bytes()),'scope':'Only current accepted partial appended after actual exact remote/source/canonical verification; cooperative lock guards this writer; no historical proof/readiness transition invented.'}))
    print(json.dumps({'status':'COMPLETED','pr':n,'new_target':identity,'attempts':str(used)+'/5','bindings':preflight['bindings_verified'],'ledger_negative_controls':len(negatives),'targets':old_count+1,'turns':old_turns+used}))
if __name__=='__main__':main()
