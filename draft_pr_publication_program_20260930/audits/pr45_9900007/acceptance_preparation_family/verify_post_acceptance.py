#!/usr/bin/env python3
"""Future root final exact acceptance/mirror/source verification; writes only own receipt."""
import argparse
import sys
sys.dont_write_bytecode = True
import pr45_guards as g
from state_mirror_reconciliation import accepted


def main():
    p=argparse.ArgumentParser(description=__doc__); g.args(p); a=p.parse_args(); frozen,pins=g.gates(a); pre,acceptance=accepted(a,frozen,pins)
    intent=g.load(g.A/'state_mirror_intent.json'); receipt=g.load(g.A/'state_mirror_receipt.json'); plan=g.load(g.A/'state_mirror_plan.json'); proposal=g.load(g.A/'state_mirror_bindings.json')
    g.mirror_records(pins,pre,plan,intent,receipt,proposal)
    g.required(intent,{'schema':'pr45-present-acceptance-mirror/v1','status':'COMPLETED','write_order':['history.jsonl','state.json'],'new_event':g.ID,'new_proof_turns':0,**pins},'Completed actual mirror intent')
    g.required(receipt,{'status':'COMPLETED','history_events_added':1,'prior_state_entries_preserved':35,'current_targets':36,'consumed_substantive_turns':44,'primary_acceptances':35,'duplicate_count':1,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,**pins},'Actual complete mirror receipt')
    old=g.parse(intent['before_state_bytes']); old_history=intent['before_history_bytes'].encode(); state=(g.R/'unsolved_math_prioritization/state.json').read_bytes(); history=(g.R/'unsolved_math_prioritization/history.jsonl').read_bytes(); current=g.parse(state)
    g.require(g.sha(intent['before_state_bytes'].encode())==pre['state_before_sha256'] and g.sha(old_history)==pre['history_before_sha256'],'Entire old state/history prefix binding differs')
    g.require(history==old_history+plan['history_append_bytes'].encode() and history.startswith(old_history),'Exactly one full-prefix-preserving event append required')
    g.require(state==plan['state_after_bytes'].encode() and g.equal(current,plan['state_after']) and set(current)==set(old)|{g.ID},'Exact native planned state membership/content differs')
    g.require(all(g.equal(current[k],v) for k,v in old.items()) and len(current)==36 and sum(z['turns_used'] for z in current.values())==44,'Prior states/budget/duplicate source-only disposition differ')
    for k,raw in [('state',state),('history',history)]: g.require(g.sha(raw)==intent[k+'_after_sha256']==receipt[k+'_sha256']==plan[k+'_after_sha256'],'Actual state/history receipt SHA differs')
    g.required(current[g.ID],{'id':g.ID,'pr':45,'status':'unsolved','turns_used':1,'turn_limit':5,'event':'acceptance_mirror_import'},'Native present original1/5 exact one-turn ledger budget')
    g.required(current[g.ID]['evidence'],{'historical_transitions_asserted':False,'import_is_present_day_mirror':True,'duplicate_ids':[]},'No invented historical/duplicate transition')
    previous=g.load(g.R/a.previous_mirror); g.require(g.equal(proposal['entries'][:-1],previous['entries']) and g.equal(proposal.get('duplicate_mirrors'),previous.get('duplicate_mirrors')),'Prior proposal accounting differs')
    m=g.mirror_module(proposal); g.require(g.sha(m.encode(plan))==intent['plan_sha256'],'Actual complete plan binding differs')
    replay=m.build_plan(g.R,proposal); m.validate_plan(g.R,replay)
    g.require(replay['history_append']==[] and replay['state_after_bytes'].encode()==state and replay['history_after_sha256']==g.sha(history),'Fresh mirror validation must be byte-preserving no-op')
    g.source(g.K); g.source(g.C); g.accepted_invariants(acceptance,pins,pre); g.foreign_check(pre)
    final,remote=g.finalization(pins,pre);inventory=g.load(g.B/'inventory.json')
    g.require(g.equal(inventory,g.derive_inventory(g.load(g.A/'integration_inventory_before.json'),remote,final['utc'])),'Complete final typed derived inventory differs')
    g.dump(g.A/'post_acceptance_verification.json',{'utc':g.stamp(),'status':'PASS','pr':45,**pins,'merge_commit':acceptance['merge_commit'],'merge_tree':acceptance['merge_tree'],'actual_remote_state':'MERGED','targets':36,'consumed_substantive_turns':44,'primary_acceptances':35,'program_completed_count':35,'program_completion_estimate_percent':inventory['program_completion_estimate_percent'],'exact_original18_and_PARTIAL_unchanged':True,'whole_current497_and416dependencies_bound':True,'entire_history_prefix_and35prior_states_preserved':True,'one_present_primary_event':True,'new_duplicate_native_acceptance_added':False,'new_proof_turns':0,'current_metadata_present_null':True,'fresh_native_mirror_noop':True,'full_target_resolved_in_prior_published_literature':False,'prior_publication_doi':None,'full_problem_solved_by_project':False,'full_problem_solved':False,'novelty_claimed':False,'scientific_completion_estimate_percent':0,'workflow_completion_estimate_percent':100,'paper_or_new_doi_or_tracker':False},exclusive=True)
    print(g.encode({'status':'PASS','pr':45,'targets':36,'turns':44,'primary_acceptances':35,'new_proof_turns':0}).decode(),end='')


if __name__=='__main__': main()
