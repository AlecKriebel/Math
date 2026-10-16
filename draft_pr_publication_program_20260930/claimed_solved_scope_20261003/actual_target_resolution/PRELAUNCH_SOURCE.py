"""Administrative target resolution and dated scope report, never acceptance.

Reads only metadata, status ledgers and existing administrative decisions. Writes
only this dedicated folder. No PR/science/helper/native/Git-index/ref mutation.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import stat
import subprocess

R=Path('/Users/alec/Documents/Math')
P=R/'draft_pr_publication_program_20260930'
D=P/'claimed_solved_scope_20261003'
C=D/'actual_target_resolution'
Q='unsolved_math_prioritization/QUEUE.md'
COMMANDS=[]
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2,sort_keys=True);f.write('\n')
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.lstat().st_mode)}
def run(argv,retain=True):
    n=len(COMMANDS)+1;start=utc()
    p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate();end=utc()
    ep=C/f'{n:02d}.stderr.bin';ep.write_bytes(err)
    row={'argv':argv,'actual_pid':p.pid,'started_utc':start,'ended_utc':end,'exit_code':p.returncode,
         'stderr':pin(ep),'stdout_bytes':len(out),'stdout_sha256':sha(out)}
    if retain:
        op=C/f'{n:02d}.stdout.bin';op.write_bytes(out);row['stdout']=pin(op)
        row['stdout_custody']='ENTIRE_RAW_STREAM_RETAINED'
    else:row['stdout_custody']='ENTIRE_QUEUE_STATUS_STREAM_HASHED_IN_MEMORY_NOT_RETAINED'
    COMMANDS.append(row);dump(C/f'{n:02d}.COMMAND.json',row)
    assert p.returncode==0,row
    return out
def scalar_rows(body):
    text=body.decode();header=next(l for l in text.splitlines() if l.startswith('| Rank |'))
    h=[c.strip() for c in header.split('|')[1:-1]];si=h.index('Status');ti=h.index('Turns')
    result={}
    for line in text.splitlines():
        if not line.startswith('|'):continue
        cells=[c.strip() for c in line.split('|')[1:-1]]
        if len(cells)<=ti:continue
        pid=cells[1].split(' / ')[0]
        if not pid.isdigit():continue
        assert pid not in result,pid
        result[pid]={'problem_id':pid,'code':cells[1],'status':cells[si],'turns':cells[ti],
                     'selected_row_sha256':sha(line.encode())}
    return result

def main():
    started=utc();C.mkdir(mode=0o755);(C/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    live=json.loads((D/'LIVE_DRAFT_ELIGIBILITY_REGISTRY.json').read_text())
    roster=json.loads((D/'SCOPE_LEDGER.json').read_text())
    inv=json.loads((P/'inventory.json').read_text())
    fields='number,title,state,isDraft,headRefName,headRefOid,url,updatedAt'
    metadata={n:json.loads(run(['gh','pr','view',str(n),'--repo','AlecKriebel/Math','--json',fields])) for n in [328,415]}
    m=metadata[328];assert m['headRefName']=='dot/math-159' and m['state']=='OPEN' and m['isDraft']
    body=run(['gh','api',f'repos/AlecKriebel/Math/contents/{Q}?ref={m["headRefOid"]}','-H','Accept: application/vnd.github.raw+json'],retain=False)
    selected=scalar_rows(body)['159'];assert selected['status']=='unsolved'
    blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    admin=metadata[415]
    assert admin['headRefName']=='repair/queue-header-metadata' and admin['title']=='Restore original QUEUE title and source header'
    resolution={'schema':'claimed-solved-status-target-resolution/v1','actual_pid':os.getpid(),'utc':utc(),
                'initial_registry':pin(D/'LIVE_DRAFT_ELIGIBILITY_REGISTRY.json'),
                'resolutions':[{'pr':328,'metadata':m,'target':selected,'whole_QUEUE_bytes':len(body),'whole_QUEUE_sha256':sha(body),
                                'git_blob_oid':blob,'method':'literal_exact_small_ID159_from_branch_verified_against_QUEUE_row',
                                'action':'SKIP_ENTIRELY_NONCLAIM_STATUS','science_body_retained':False},
                               {'pr':415,'metadata':admin,'action':'SKIP_ADMINISTRATIVE_NO_MATHEMATICAL_QUEUE_TARGET',
                                'method':'exact_metadata_title_and_branch_identity_only_no_PR_body_or_diff_read',
                                'mathematical_QUEUE_status':None,'eligible_claimed_solution':False}],
                'remaining_target_gaps':[],'no_new_mathematical_credit':True}
    dump(D/'TARGET_METADATA_RESOLUTION.json',resolution)
    # Dated canonical state is context, not a replacement for submitted-head status.
    head=run(['git','rev-parse','HEAD']).decode().strip()
    qbody=(R/Q).read_bytes();global_rows=scalar_rows(qbody)
    ids=sorted({t['problem_id'] for row in live['rows'] for t in row['status_projection']['targets']},key=int)
    context={'schema':'claimed-solved-current-canonical-status-context/v1','actual_pid':os.getpid(),'utc':utc(),
             'local_HEAD_observed':head,'working_QUEUE':pin(R/Q),'projected_status_rows':[global_rows[i] for i in ids if i in global_rows],
             'eligibility_source':'submitted/current_literal_PR_head_QUEUE status plus OPEN draft metadata',
             'canonical_main_may_be_queued_before_draft_acceptance':True,'does_not_reclassify_or_accept_any_result':True}
    dump(D/'CANONICAL_STATUS_CONTEXT.json',context)
    priority=P/'audits/pr18_30001075/PRIORITY_ASSESSMENT.json'
    fifty=P/'audits/pr50_10600042/ROOT_FINAL_SUBMISSION_DECISION.json'
    fiftyseven=P/'audits/pr57_30003354/ROOT_FINAL_PREPRINT_PACKAGE_ADJUDICATION_20261003.json'
    p18=json.loads(priority.read_text());p50=json.loads(fifty.read_text());p57=json.loads(fiftyseven.read_text())
    published=[]
    for n in [9,16]:
        item=next(i for i in inv['items'] if i['number']==n)
        old=next(i for i in roster['rows'] if i['pr']==n)
        assert item['stage']=='complete' and item['doi'] and old['current_GitHub_metadata']['state']=='MERGED'
        published.append({'pr':n,'DOI':item['doi'],'historical_outcome':item['outcome'],'fresh_dated_metadata':old['current_GitHub_metadata']})
    eligible=live['current_eligible_open_draft_order']
    summary={'schema':'claimed-solved-scope-status-handoff/v1','status':'READY_ADMINISTRATIVE_SCOPE_ONLY',
             'actual_author_pid':os.getpid(),'utc':utc(),'objective':pin(Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')),
             'original_inventory_unchanged_sha256':pin(P/'inventory.json')['sha256'],
             'historical_original_roster_count':180,'historical_completed_count':37,'historical_completed_publications':published,
             'historical_completed_partial_count':35,'old_counts_do_not_define_new_eligible_progress':True,
             'live_metadata_observation_ended_utc':live['ended_utc'],'live_OPEN_draft_count':440,
             'eligible_claimed_solved_OPEN_draft_count':len(eligible),'ordered_unpublished_eligible_PRs':eligible,
             'nonclaim_drafts_skipped_count':342,'administrative_no_problem_target_skipped_count':1,'remaining_metadata_target_gaps':[],
             'known_published_plus_observed_eligible_count':2+len(eligible),'eligible_publication_progress_percent':200/(2+len(eligible)),
             'estimate_denominator_is_dated_and_changes_with_new_arrivals':True,'scope_inventory_completion_percent':100,
             'first_eligible_unpublished_PR':18,
             'PR18_existing_partial_progress':{'evidence':pin(priority),'math_gate':p18['math_gate'],'priority_gate':p18['priority_gate'],
                'exact_gap':p18['remaining_requirement'],'positive_exact_prior_verified':p18['positive_exact_prior_verified'],
                'paper_preparation_started':p18['paper_preparation_started'],'historical_workflow_estimate_percent':p18['workflow_completion_estimate_percent'],
                'new_priority_or_math_audit_conferred':False},
             'prepared_unpublished_packages':[{'pr':50,'existing_decision':pin(fifty),'historical_status':p50['status'],
                'published':p50['zenodo_publication_completed'],'DOI_created':p50['doi_created'],'tracker_row_appended':p50['tracker_row_appended'],
                'old_requires48_49_order_superseded_by_revised_scope':True,'new_acceptance_clearance_conferred':False},
                {'pr':57,'existing_decision':pin(fiftyseven),'historical_package_ready':p57['preprint_package_ready_for_ordered_publication'],
                 'published':p57['actual_external_upload_performed'],'DOI':p57['DOI'],'tracker_row':p57['tracker_row'],
                 'new_acceptance_clearance_conferred':False}],
             'PR55_is_eligible_and_precedes57':55 in eligible and eligible.index(55)<eligible.index(57),
             'cancelled_nonclaim_work_PRs':[48,49,63,64],'prior_families_and_native_state_untouched':True,
             'ROOT_alone_handles_publication_PR_actions_and_checkpoints':True,
             'scope_only_no_new_math_priority_paper_DOI_tracker_or_acceptance_code':True}
    assert summary['original_inventory_unchanged_sha256']=='171061fc88b5ca06e200cc2cead9d11fe1e7435f8f98435907937bdc0f9df0d8'
    dump(D/'SCOPE_HANDOFF.json',summary)
    report=f'''# Claimed-solved-only scope inventory

The revised objective admits only exact `claimed_solved` statuses, proceeding from PR9 in PR-number order. This administrative inventory performs no mathematical review or new acceptance. It writes only this dedicated folder; old inventories, QUEUE/state/history, PR48/49/63/64 work, logs, index and refs are preserved.

The live metadata observation ending {live['ended_utc']} found 440 OPEN draft PRs at or above9, excluding8, through observed PR510. Their literal-head QUEUE status projections identify97 eligible claims,342 nonclaim skips, and one administrative header PR415 with no mathematical target. PR328's exact short ID159 was independently resolved as `unsolved`; its initial selector gap is retained. There are no remaining metadata-target gaps in that dated registry. A final metadata reread found no new heads or arrivals; later arrivals require another status-only check. No timeless all-repository coverage is asserted.

PR9 and16 are already recorded as published and merged, with their historical DOIs retained. Their publication records are not new publication checks. The earlier37 completed PRs comprise these2 publications and35 partial dispositions; those historical completions remain unchanged and do not become new eligible completions. The original180 dated submitted heads contain44 claims,34 known results and102 unsolved outcomes. The first dated roster action list failed to exclude already-MERGED former claims; the live OPEN-draft registry explicitly supersedes those preliminary labels and its44 denominator. Progress under the observed revised scope is2/(97+2) = {200/99:.6f}%, a denominator that can change as new drafts arrive. The administrative inventory itself is100% complete for the stated observation.

The first unpublished eligible PR is18. Its existing three-family mathematical gate passed, but its existing priority gate remains `{p18['priority_gate']}`. The precise recorded gap is: {p18['remaining_requirement']} No positive exact prior resolution has been verified in that record. This inventory grants no priority clearance and does not start its paper. Its historical workflow estimate is50%.

PR50 and57 already have prepared, reviewed but unpublished packages according to the separately pinned ROOT decisions. No actual Zenodo publication, new DOI, tracker row or native acceptance is created here. PR50's former instruction to wait for nonclaim PR48/49 is historical and superseded by the revised scope. The current order begins18,50,55,57,65,66: PR55 also submits an exact claim and must not be silently skipped before57.

Eligibility comes from the selected submitted/current literal PR-head QUEUE row together with current OPEN+draft metadata. Current canonical main QUEUE statuses are retained separately as dated scalar context: main can remain `queued` before draft acceptance, and those context rows do not grant mathematical credit or overwrite submitted claims. Any later classification change, duplicate-target issue, or shared-chat disposition must be reconciled before that PR is processed.

Evidence is compact: actual source/prelaunch, child PID/time/argv/full stderr and complete metadata stdout are retained. Large QUEUE API/batch stdout is observed and hashed in memory and explicitly not retained; only target scalar projections, row hashes and whole-body hashes/OIDs remain. These projections are administrative evidence, not full scientific-body custody. Full eligible source/QUEUE verification is deferred to the later authorized mathematical workflow. The initial collector refusal on missing local original objects remains intact; the V2 collector read immutable-head QUEUE status data via primary GitHub APIs, with no source-code/proof fetch, Git fetch or ref/index body mutation. No external individuals were contacted.
'''
    (D/'REPORT.md').write_text(report)
    (D/'RESEARCH_LOG.md').write_text(f'''{started} — Administrative eligibility mechanism started; completion estimate10%. Prior nonclaim work is preserved and discontinued.
{roster['ended_utc']} — Dated180 status projection:44 claimed,34 already_solved,102 unsolved. First failed collector/source retained. Its draft-eligibility action labels require the explicit later metadata qualification; inventory completion estimate45%.
{live['ended_utc']} — Fresh440 OPEN drafts,97 exact claims; PR18 first. Two target-only selector gaps identified; estimate95%.
{utc()} — Short ID159=unsolved and administrative PR415 resolved by metadata/status only. Exact PR18 hold and existing50/57 unpublished decisions recorded; PR55 ordering preserved. Scope inventory100%; observed eligible publication progress2/99={200/99:.6f}%. New discovery/publication/acceptance0%. ROOT owns any later checkpoint/publication actions.
''')
    dump(C/'COMPLETE_COMMANDS.json',COMMANDS)
    dump(C/'COLLECTION_RECEIPT.json',{'schema':'claimed-solved-target-resolution-actual-collection/v1','status':'PASS_METADATA_STATUS_ONLY',
         'actual_pid':os.getpid(),'started_utc':started,'ended_utc':utc(),'source':pin(Path(__file__)),'source_prelaunch':pin(C/'PRELAUNCH_SOURCE.py'),
         'command_count':len(COMMANDS),'no_production_or_mathematical_helper_execution':True})
    rows=[]
    for p in sorted(D.rglob('*')):
        s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
        if stat.S_ISREG(s.st_mode):rows.append(pin(p))
        else:assert stat.S_ISDIR(s.st_mode)
    dump(D/'READY.json',{'schema':'claimed-solved-scope-administrative-readiness/v1','status':'READY_SCOPE_INVENTORY_ONLY',
          'actual_author_pid':os.getpid(),'utc':utc(),'self_excluded':'READY.json','all_current_payload_files':rows,
          'handoff':pin(D/'SCOPE_HANDOFF.json'),'report':pin(D/'REPORT.md'),'metadata_target_gaps_remaining':[],
          'no_new_mathematical_priority_acceptance_publication_authority':True,'ROOT_review_and_checkpoint_pending':True})
    print(json.dumps({'status':'READY_SCOPE_INVENTORY_ONLY','actual_pid':os.getpid(),'eligible_OPEN_drafts':len(eligible),
                      'first':eligible[:6],'scope_inventory_percent':100,'READY':pin(D/'READY.json')}))

if __name__=='__main__':
    try:main()
    except BaseException:
        import traceback
        if C.exists():
            dump(C/'FAILED_COMPLETE_COMMANDS.json',COMMANDS)
            (C/'COLLECTION_FAILURE.txt').write_text(traceback.format_exc())
        raise
