#!/usr/bin/env python3
"""V2 SOURCE ONLY: rejected V1 S1 repaired; independent clean SOURCE audit remains required."""
"""Future root present acceptance mirror: one event, zero new proof turns."""
import argparse
import copy
import fcntl
import sys
sys.dont_write_bytecode = True
import pr46_guards as g
from integrate_reviewed_partial import BODY, inventory_guard, queue_after


def accepted(a,frozen,pins):
    pre=g.preflight_record(pins)
    canonical=g.load(g.K/'acceptance.json'); audit=g.load(g.A/'acceptance.json')
    g.accepted_invariants(canonical,pins,pre); g.accepted_invariants(audit,pins,pre,audit=True)
    g.require(g.equal(canonical,{k:v for k,v in audit.items() if k not in {'canonical_manifest_sha256','canonical_manifest_entries'}}),'Exact audit/canonical accepted objects differ')
    g.manifest(g.K,'MANIFEST.json',audit['canonical_manifest_sha256'],audit['canonical_manifest_entries'],frozen=True); g.canonical(frozen,True)
    observed=g.remote(); g.require(g.equal(observed,g.load(g.A/'remote_merge_receipt.json')),'Full fresh actual remote differs')
    g.required(observed,{'state':'MERGED','isDraft':False,'body':BODY,'mergedAt':canonical['merged_at'],'mergeCommit':{'oid':canonical['merge_commit']}},'Actual remote accepted binding')
    queue=(g.A/'integration_queue_before.md').read_bytes(); after,row=queue_after(queue); g.require(g.Q.read_bytes()==after,'Whole named-only queue differs')
    patch=g.load(g.K/'ACCEPTED_QUEUE_PATCH.json'); g.required(patch,{'header_names':g.HEADER,'column_count':12,'named_changes':['Status','Turns','Findings'],'whole_before_sha256':g.sha(queue),'whole_after_sha256':g.sha(after),'row_before':g.selected(queue),'row_after':row,'all_other_bytes_preserved':True,'selected_chat_DOI_preserved':True},'Exact accepted queue receipt')
    overlay=g.overlay_record(pins,frozen); tree=g.tree(canonical['merge_commit'],pre,overlay,after)
    expected_patch={'utc':overlay['utc'],'header_names':g.HEADER,'column_count':12,'named_changes':['Status','Turns','Findings'],'whole_before_sha256':g.sha(queue),'whole_after_sha256':g.sha(after),'row_before':g.selected(queue),'row_after':row,'all_other_bytes_preserved':True,'selected_chat_DOI_preserved':True,'fresh_preimage_sha256':a.fresh_preimage_sha256}
    g.require(g.equal(patch,expected_patch),'Entire typed accepted queue receipt, no meaningful extension')
    push=g.prepush_record(pins); g.require(tree==canonical['merge_tree']==push['merge_tree'] and push['merge_commit']==canonical['merge_commit'],'Actual original-head tree/parents/prepush differ')
    final,retained_remote=g.finalization(pins,pre)
    inv=g.load(g.B/'inventory.json'); inventory_guard(g.load(g.A/'integration_inventory_before.json'),inv,retained_remote,final['utc']); g.required(inv,{'current_pr':47,'completed_count':36},'PostPR46 next-target metadata'); g.require(inv['completed_count']==36 and sum(z.get('stage')=='complete' for z in inv['items'])==36,'Exactly36 primary completions')
    item=next(z for z in inv['items'] if z['number']==46); g.required(item,{'stage':'complete','outcome':'already_solved_accepted_known_result','queue_status':'already_solved','audited_head':g.HEAD,'merge_commit':canonical['merge_commit'],'merged_at':canonical['merged_at'],'original_attempts':'0/5','cumulative_attempts':'0/5','original_source_verification_responses':1,'new_substantive_attempts':0,'paper_or_new_doi_or_tracker':False},'Exact selected accepted inventory')
    g.fresh_check(pre,{'unsolved_math_prioritization/QUEUE.md','draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'})
    g.owned_log_append_check(pre)
    return pre,canonical


def main():
    p=argparse.ArgumentParser(description=__doc__); g.args(p); a=p.parse_args(); frozen,pins=g.gates(a); pre,acceptance=accepted(a,frozen,pins)
    g.require(not (g.A/'state_mirror_intent.json').exists(),'Inspect retained intent before retry')
    state=g.R/'unsolved_math_prioritization/state.json'; history=g.R/'unsolved_math_prioritization/history.jsonl'; old_state,old_history=state.read_bytes(),history.read_bytes(); prior=g.parse(old_state)
    g.require(g.sha(old_state)==pre['state_before_sha256'] and g.sha(old_history)==pre['history_before_sha256'],'Exact full preflight state/history differs')
    g.require(len(prior)==36 and g.ID not in prior and sum(z['turns_used'] for z in prior.values())==44,'Require36targets/44turns and selected identity absent')
    proposal=copy.deepcopy(g.load(g.R/a.previous_mirror)); old_entries=copy.deepcopy(proposal['entries']); old_duplicates=copy.deepcopy(proposal.get('duplicate_mirrors'))
    proposal.update(created_at_utc=g.stamp(),scope='Incremental present accepted primary PR46 exact known rational-map result credited to Kozhasov–Kummer2020preprint; original0/5 plus source-verification responses1, no new proof turn or historical reconstruction.')
    for k in ['inventory','queue']: proposal[k]=g.binding(g.R/proposal[k]['path'])
    proposal['required_completed_prs']=sorted(proposal['required_completed_prs']+[46])
    proposal['entries'].append({'pr':46,'id':g.ID,'status':'already_solved','acceptance':g.binding(g.K/'acceptance.json'),'audit_acceptance':g.binding(g.A/'acceptance.json'),'remote':g.binding(g.A/'remote_merge_receipt.json'),'accepted_source':g.binding(g.K/'source_record.json'),'canonical_acceptance_text':g.binding(g.K/'ACCEPTANCE.md'),'canonical_manifest':g.binding(g.K/'MANIFEST.json'),'artifact':{**g.binding(g.K/'SOURCE_STATUS.md'),'acceptance_hash_field':'canonical_scientific_artifact_sha256'},'budget':{'used':0,'limit':5,'kind':'pr46_exact_original_zero_turn_object','ledger':g.binding(g.K/'turns.json')},'duplicates':[]})
    g.require(g.equal(proposal['entries'][:-1],old_entries) and g.equal(proposal.get('duplicate_mirrors'),old_duplicates),'All prior proposal entries/duplicate accounting preserved')
    g.mirror_proposal(proposal,pins)
    m=g.mirror_module(proposal);negatives=[]
    for label,raw,used,limit in [('empty',b'',0,5),('whitespace_only',b'\n',0,5),('invented_object',b'{"substantive_turns_used":0}\n',0,5),('bool_used',g.regular(g.K,'turns.json').read_bytes(),False,5),('wrong_used',g.regular(g.K,'turns.json').read_bytes(),1,5),('wrong_limit',g.regular(g.K,'turns.json').read_bytes(),0,4)]:
        try:m.ledger_budget(raw,'pr46_exact_original_zero_turn_object',used,limit)
        except m.Rejected:negatives.append(label)
        else:raise ValueError('Exact zero-turn-object-ledger guard accepted mutant '+label)
    plan=m.build_plan(g.R,proposal); validation=m.validate_plan(g.R,plan)
    g.require(plan['primary_count']==36 and plan['duplicate_count']==1 and len(plan['state_after'])==37 and sum(z['turns_used'] for z in plan['state_after'].values())==44,'Exactly37targets/44turns/36primary/one preserved duplicate required')
    g.require(len(plan['history_append'])==1 and plan['history_append'][0]['id']==g.ID and plan['history_append'][0]['event']=='acceptance_mirror_import','Exactly one present primary acceptance event')
    g.require(all(g.equal(plan['state_after'][k],v) for k,v in prior.items()),'Every prior state unchanged; no new duplicate')
    event=plan['history_append'][0]; g.required(event,{'turns_used':0,'turn_limit':5,'status':'already_solved'},'Native original0/5 exact zero-turn object ledger budget'); g.required(event['evidence'],{'historical_transitions_asserted':False,'import_is_present_day_mirror':True,'duplicate_ids':[]},'Present event only')
    g.dump(g.A/'state_mirror_bindings.json',proposal,exclusive=True); g.dump(g.A/'state_mirror_plan.json',plan,exclusive=True)
    protected={}
    for z in plan['bindings']:
        g.relative(z['path']); g.digest(z['sha256']); raw=g.regular(g.R,z['path']).read_bytes(); g.require(g.sha(raw)==z['sha256'],'Strict regular protected binding changed')
        g.require(z['path'] not in protected or protected[z['path']]==z['sha256'],'Conflicting protected binding'); protected[z['path']]=z['sha256']
    lock=g.BASE/'tmp/root-accepted-state.lock'; g.require(lock.parent.is_dir() and not lock.is_symlink(),'Existing cooperative regular lock required')
    with lock.open('a+b') as stream:
        fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB); m.validate_plan(g.R,plan); accepted(a,frozen,pins)
        g.require(state.read_bytes()==old_state and history.read_bytes()==old_history,'Exact state/history preimage changed before locked write')
        intent={'schema':'pr46-present-acceptance-mirror/v1','status':'PREPARED','utc':g.stamp(),**pins,'plan_sha256':g.sha(m.encode(plan)),'before':plan['preconditions'],'before_state_bytes':old_state.decode(),'before_history_bytes':old_history.decode(),'state_after_sha256':plan['state_after_sha256'],'history_after_sha256':plan['history_after_sha256'],'write_order':['history.jsonl','state.json'],'new_event':g.ID,'new_proof_turns':0,'lock_limitation':'Cooperative advisory lock; noncooperating writers remain outside protocol.'}
        g.dump(g.A/'state_mirror_intent.json',intent,exclusive=True)
        for n,h in protected.items(): g.require(g.sha(g.regular(g.R,n).read_bytes())==h,'Protected binding changed before write')
        g.write(history,old_history+plan['history_append_bytes'].encode()); g.require(state.read_bytes()==old_state and g.sha(history.read_bytes())==plan['history_after_sha256'],'History-first outcome differs')
        g.write(state,plan['state_after_bytes'].encode()); g.require(g.sha(state.read_bytes())==plan['state_after_sha256'],'State outcome differs')
        for n,h in protected.items(): g.require(g.sha(g.regular(g.R,n).read_bytes())==h,'Protected binding changed by mirror')
        g.foreign_check(pre); intent.update(status='COMPLETED',completed_utc=g.stamp()); g.dump(g.A/'state_mirror_intent.json',intent)
        g.dump(g.A/'state_mirror_receipt.json',{'utc':g.stamp(),'status':'COMPLETED',**pins,'validation':validation,'negative_ledger_controls':negatives,'history_events_added':1,'prior_state_entries_preserved':36,'current_targets':37,'consumed_substantive_turns':44,'primary_acceptances':36,'duplicate_count':1,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'state_sha256':g.sha(state.read_bytes()),'history_sha256':g.sha(history.read_bytes())},exclusive=True)
    print(g.encode({'status':'COMPLETED','pr':46,'targets':37,'consumed_turns':44,'primary_acceptances':36,'new_proof_turns':0}).decode(),end='')


if __name__=='__main__': main()
