"""ROOT independently inspects complete actual post evidence; no helper import."""
from pathlib import Path
import copy
import datetime as dt
import json
import os
import stat
import subprocess
import author_root_acceptance_inputs as o

A, R = o.A, o.R
K = R / 'unsolved_math_prioritization/attempts/9700035'


def git(*args): return subprocess.check_output(['git',*args],cwd=R)
def typed_equal(a,b): return json.dumps(a,sort_keys=True,separators=(',',':')) == json.dumps(b,sort_keys=True,separators=(',',':'))


def main():
    cb = A/'root_integration_post_actual_capture'; cap = o.load(cb/'CAPTURE.json')
    assert cap['actual_execution'] is True and cap['completed'] is True and cap['status'] == 'PASS'
    assert type(cap['pid']) is int and cap['pid'] == 42797 and cap['exit_code'] == 0
    assert cap['stdin_supplied'] is False and cap['cwd'] == str(A)
    for key in ['stdout','stderr']: o.check(cb,cap[key])
    assert (cb/'stderr.bin').read_bytes() == b''
    assert o.load(cb/'stdout.bin') == {'status':'PASS','pr':41,'targets':32,'turns':39,'primary_acceptances':31,'new_proof_turns':0}
    assert (cb/'prelaunch_source.py').read_bytes() == (A/'acceptance_preparation_family_v2/verify_post_acceptance.py').read_bytes()
    assert cap['source_sha256'] == '48b78bfd9f24025e0aa2530e59493ccfcddba0f7890dcacbf8efa38efadfd1cc'
    start=dt.datetime.fromisoformat(cap['started_utc']); finish=dt.datetime.fromisoformat(cap['finished_utc'])
    post=o.load(A/'post_acceptance_verification.json')
    assert start <= dt.datetime.fromisoformat(post['utc']) <= finish <= dt.datetime.now(dt.timezone.utc)
    expected={'status':'PASS','pr':41,'targets':32,'consumed_substantive_turns':39,
              'primary_acceptances':31,'program_completed_count':31,'new_proof_turns':0,
              'workflow_completion_estimate_percent':100,'scientific_completion_estimate_percent':0}
    for k,v in expected.items(): assert type(post[k]) is type(v) and post[k] == v
    assert type(post['program_completion_estimate_percent']) is float and post['program_completion_estimate_percent'] == 31/180*100
    for k in ['full_problem_solved','novelty_claimed','paper_or_new_doi_or_tracker','new_duplicate_native_acceptance_added']: assert post[k] is False
    for k in ['fresh_native_mirror_noop','current_metadata_present_null','entire_history_prefix_and31prior_states_preserved','one_present_primary_event','exact_original16_and_PROOF_unchanged','whole_current547_and469dependencies_bound']: assert post[k] is True
    acceptance=o.load(A/'acceptance.json'); canonical=o.load(K/'acceptance.json')
    assert typed_equal(canonical,{k:v for k,v in acceptance.items() if k not in ['canonical_manifest_sha256','canonical_manifest_entries']})
    assert acceptance['partial_valid'] is True
    for k in ['full_problem_solved','novelty_claimed','paper_or_new_doi_or_tracker']: assert acceptance[k] is False
    for k,v in [('original_substantive_attempts',2),('new_substantive_attempts',0),('audit_turns',0),('turn_limit',5)]: assert type(acceptance[k]) is int and acceptance[k] == v
    for k in ['current_model','current_reasoning_effort','current_deadline_utc']: assert k in acceptance and acceptance[k] is None
    km=o.load(K/'MANIFEST.json'); assert o.sha((K/'MANIFEST.json').read_bytes()) == acceptance['canonical_manifest_sha256'] == '47a127d2de60ea688d58b880148ec55193cd022cbd45a7f8022681ffa63a09b5'
    assert len(km['files']) == acceptance['canonical_manifest_entries'] == 558
    o.closure(K,'MANIFEST.json',km['files'],True)
    cm=o.load(A/'reviewed_candidate/MANIFEST.json'); assert len(cm['files']) == 547
    assert o.sha((A/'reviewed_candidate/MANIFEST.json').read_bytes()) == '3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'
    o.closure(A/'reviewed_candidate','MANIFEST.json',cm['files'],True)
    deps=o.load(A/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json'); assert len(deps['files']) == 469
    for row in deps['files']: o.check(A,row)
    snapshot=o.load(A/'snapshot_manifest.json'); assert len(snapshot['files']) == 16
    for row in snapshot['files']: o.check(K/'original_archive',row,True)
    assert o.sha((K/'PROOF.md').read_bytes()) == '464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c'
    assert o.sha((K/'turns.json').read_bytes()) == 'bd0a82165c3ac81f7a7d35ace164f20ecb87e6b73a9155815e4eecac655a2549'
    assert o.load(K/'prior_report.json') == o.load(A/'source_snapshot/prior_report.json') and bool(o.load(K/'prior_report.json'))
    remote=o.load(A/'remote_merge_receipt.json'); assert remote['state'] == 'MERGED' and remote['isDraft'] is False and remote['headRefOid'] == '292b95ca601f166e6d246e609cf7ed5ca5653e25'
    merge='85f830ba77016e6d7ef86a3ca1c93547b6f50f72'; assert remote['mergeCommit']['oid'] == post['merge_commit'] == merge
    assert git('rev-parse','HEAD').decode().strip() == merge and git('branch','--show-current').strip() == b'main'
    assert git('show','-s','--format=%P',merge).decode().strip().split() == ['521770c746b2fd48e00ac6dd908afe5085daf4ab',remote['headRefOid']]
    assert git('show','-s','--format=%T',merge).decode().strip() == post['merge_tree'] == '1c2a135516b3035cd5a6c6895cf80bf04e463e10'
    intent=o.load(A/'state_mirror_intent.json'); old=json.loads(intent['before_state_bytes']); state=o.load(R/'unsolved_math_prioritization/state.json')
    assert intent['status'] == 'COMPLETED' and len(old) == 31 and len(state) == 32
    assert set(state)-set(old) == {'9700035'} and all(typed_equal(state[k],v) for k,v in old.items())
    history=(R/'unsolved_math_prioritization/history.jsonl').read_bytes(); prefix=intent['before_history_bytes'].encode()
    assert history.startswith(prefix); events=[json.loads(line) for line in history[len(prefix):].splitlines()]
    assert len(events) == 1 and events[0]['id'] == '9700035' and events[0]['pr'] == 41 and events[0]['turns_used'] == 2
    assert sum(v['turns_used'] for v in state.values()) == 39
    mirror=o.load(A/'state_mirror_receipt.json'); assert o.sha(history) == mirror['history_sha256'] and o.sha((R/'unsolved_math_prioritization/state.json').read_bytes()) == mirror['state_sha256']
    assert mirror['negative_ledger_controls'] == ['bool_turn','phantom_attempt','missing_turn','wrong_order','extra_field']
    previous=o.load(A.parent/'pr40_2814/state_mirror_bindings.json'); proposal=o.load(A/'state_mirror_bindings.json')
    assert typed_equal(proposal['entries'][:-1],previous['entries']) and typed_equal(proposal['duplicate_mirrors'],previous['duplicate_mirrors'])
    before=o.load(A/'integration_inventory_before.json'); final=o.load(A/'integration_finalization.json'); expected_inv=copy.deepcopy(before)
    chosen=next(z for z in expected_inv['items'] if z['number']==41)
    chosen.update(stage='complete',outcome='unsolved_accepted_partial',queue_status='unsolved',audited_head=remote['headRefOid'],merge_commit=merge,merged_at=remote['mergedAt'],workflow_completion_estimate_percent=100,original_attempts='2/5',new_substantive_attempts=0,cumulative_attempts='2/5',paper_or_new_doi_or_tracker=False)
    expected_inv.update(updated_at_utc=final['utc'],last_checkpoint_utc=final['utc'],completed_count=31,program_completion_estimate_percent=31/180*100,completion_estimate_percent=31/180*100,current_pr=42)
    assert typed_equal(o.load(R/'draft_pr_publication_program_20260930/inventory.json'),expected_inv)
    fresh=o.load(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json')
    allowed={'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'}
    for row in fresh['files']:
        if row['path'] not in allowed: o.check(R,row)
        assert stat.S_IMODE((R/row['path']).stat().st_mode) == row['worktree_mode']
    pre=o.load(A/'integration_preflight.json')
    for row in pre['foreign_logs']: o.check(R,row)
    result={'schema':'pr41-root-complete-actual-post-inspection/v1','status':'PASS',
            'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_inspector_pid':os.getpid(),
            'actual_post_pid':cap['pid'],'entire_post':post,'entire_post_capture':cap,
            'entire_remote':remote,'entire_mirror_receipt':mirror,'canonical_members':558,
            'current_members':547,'dependencies':469,'all31_prior_states_and_full_history_prefix_preserved':True,
            'current13_match_exact_allowed_acceptance_changes':True,'completed_primary_prs':31,
            'program_completion_percent':31/180*100,'science_helpers_executed':False,
            'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False}
    o.dump('ROOT_ACTUAL_POST_INSPECTION.json',result)
    print(json.dumps({'status':'PASS','actual_inspector_pid':os.getpid(),'actual_post_pid':42797,
                      'canonical_members':558,'completed_primary_prs':31,'program_completion_percent':31/180*100}))


if __name__ == '__main__': main()
