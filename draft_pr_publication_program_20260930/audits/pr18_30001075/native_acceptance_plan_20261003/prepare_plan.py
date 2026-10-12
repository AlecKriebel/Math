"""Small administrative PR18 integration-plan author; no native actions.

Writes only this plan folder. Reuses the existing fifteen-file custody manifest.
Never runs an author, proof helper, acceptance step, Git mutation or publication.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

R=Path('/Users/alec/Documents/Math')
P=R/'draft_pr_publication_program_20260930'
A=P/'audits/pr18_30001075'
D=A/'native_acceptance_plan_20261003'
C=D/'actual_readonly_observation'
K='unsolved_math_prioritization/attempts/30001075'
Q='unsolved_math_prioritization/QUEUE.md'
H='99e403e85d38d92b021198c4a57bbad3cd8775ba'
COMMANDS=[]
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.lstat().st_mode)}
def dump(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2,sort_keys=True);f.write('\n')
def run(argv):
    n=len(COMMANDS)+1;start=utc()
    p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate();end=utc()
    op=C/f'{n:02d}.stdout.bin';ep=C/f'{n:02d}.stderr.bin';op.write_bytes(out);ep.write_bytes(err)
    row={'argv':argv,'cwd':str(R),'actual_pid':p.pid,'started_utc':start,'ended_utc':end,'exit_code':p.returncode,
         'stdout':pin(op),'stderr':pin(ep),'whole_streams_retained':True}
    COMMANDS.append(row);dump(C/f'{n:02d}.COMMAND.json',row)
    assert p.returncode==0,row
    return out
def main():
    started=utc();C.mkdir(mode=0o755);(C/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    branch=run(['git','branch','--show-current']).decode().strip();assert branch=='main'
    mainhead=run(['git','rev-parse','HEAD']).decode().strip()
    base=run(['git','merge-base',mainhead,H]).decode().strip()
    remote=run(['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).decode();remote=json.loads(remote)
    metadata=json.loads(run(['gh','pr','view','18','--repo','AlecKriebel/Math','--json',
                           'number,title,state,isDraft,headRefOid,headRefName,baseRefName,baseRefOid,mergeable,url,files']))
    assert metadata['state']=='OPEN' and metadata['isDraft'] and metadata['headRefOid']==H
    manifest=json.loads((A/'snapshot_manifest.json').read_text());assert manifest['head']==H and len(manifest['files'])==15
    tree=run(['git','ls-tree','-r',H,'--',K]).decode().splitlines()
    entries={line.split('\t')[1]:(line.split()[0],line.split()[2]) for line in tree}
    mappings=[]
    for row in manifest['files']:
        target=K+'/'+row['path'];original=A/'source_snapshot'/row['path'];b=original.read_bytes()
        assert len(b)==row['size'] and sha(b)==row['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob']
        assert entries[target]==(row['mode'],row['git_blob'])
        mappings.append({'canonical_path':target,'existing_custody_path':str(original),'git_blob':row['git_blob'],
                         'git_mode':row['mode'],'bytes':row['size'],'sha256':row['sha256'],
                         'currently_absent_worktree':not (R/target).exists(),'future_action':'merge_exact_original_blob_without_body_edits'})
    assert set(entries)=={m['canonical_path'] for m in mappings}
    assert set(v['path'] for v in metadata['files'])==set(manifest['changed_paths'])
    overlap=run(['git','diff','--name-status',base,mainhead,'--',Q,K]).decode().splitlines()
    owned_diff=run(['git','diff','--name-status',mainhead,'--',Q,'unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl',K]).decode()
    cached=run(['git','diff','--cached','--name-only','-z'])
    staged=[v.decode('utf8') for v in cached.split(b'\0') if v]
    # Read/hash raw index without making a duplicate index or asking Git to refresh it.
    index=R/'.git/index';index_pin=pin(index)
    priority=json.loads((A/'ROOT_CURRENT_PRIORITY_ASSESSMENT_20261003.json').read_text())
    assert priority['eligible_submitted_status']=='claimed_solved' and priority['original_head']==H
    state=json.loads((R/'unsolved_math_prioritization/state.json').read_text())
    history=[json.loads(l) for l in (R/'unsolved_math_prioritization/history.jsonl').read_text().splitlines() if l]
    qbody=(R/Q).read_bytes();qlines=qbody.decode().splitlines()
    target_lines=[l for l in qlines if l.startswith('|') and l.split('|')[2].strip().startswith('30001075 /')]
    assert len(target_lines)==1
    cells=[c.strip() for c in target_lines[0].split('|')[1:-1]]
    assert cells[7]=='queued' and cells[8]=='0/5' and '30001075' not in state
    assert not any(str(h.get('id'))=='30001075' for h in history)
    observations={'schema':'pr18-native-plan-readonly-observation/v1','actual_pid':os.getpid(),'started_utc':started,'ended_utc':utc(),
                  'local_main_HEAD':mainhead,'remote_main_HEAD':remote['object']['sha'],'PR18_metadata':metadata,
                  'GitHub_baseRefOid_is_not_fresh_main_authority':True,'computed_common_base':base,
                  'original_custody_manifest':pin(A/'snapshot_manifest.json'),'original_scientific_files':mappings,
                  'common_base_to_main_overlap_on_original_PR_paths':overlap,
                  'dated_uncommitted_diff_on_native_owned_scope':owned_diff,
                  'dated_foreign_staged_paths':staged,'raw_index_observation':index_pin,
                  'raw_index_body_copied':False,'index_lock_currently_absent':not (R/'.git/index.lock').exists(),
                  'canonical_queue':pin(R/Q),'selected_current_queue_row':target_lines[0],
                  'state':pin(R/'unsolved_math_prioritization/state.json'),'state_target_absent':True,
                  'history':pin(R/'unsolved_math_prioritization/history.jsonl'),'history_target_absent':True,
                  'dated_existing_native_target_entries':len(state),'dated_existing_native_turns':sum(s.get('turns_used',0) for s in state.values()),
                  'current_priority_decision':pin(A/'ROOT_CURRENT_PRIORITY_ASSESSMENT_20261003.json'),
                  'current_draft_manuscript':pin(A/'preprint_v1/paper.tex'),
                  'manuscript_is_not_a_fixed_final_package':True,
                  'mathematical_reverification_performed':False,'native_ref_index_or_publication_mutations':False}
    dump(D/'OBSERVATIONS.json',observations)
    plan={'schema':'pr18-small-native-acceptance-plan/v1','status':'PROPOSED_READONLY_ONLY_PACKAGE_AND_DOI_PENDING',
          'pr':18,'problem_id':'30001075','submitted_head':H,'submitted_status':'claimed_solved','original_budget':'1/5',
          'observations':pin(D/'OBSERVATIONS.json'),'required_later_FIXED_package_reviews_complete':False,
          'actual_future_DOI':None,'actual_future_tracker_row':None,'actual_future_merge_commit':None,
          'original_scientific_files_to_preserve_exactly':mappings,
          'minimal_prospective_paths':[Q,'unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl',
                                      K+'/acceptance.json',K+'/CURRENT_RESULT.md'],
          'fixed_preprint_files_remain_in_the_final_ROOT_selected_A18_package':True,
          'no_need_to_duplicate_all_prior_reviews_or_foreign_evidence':True,
          'QUEUE_authorized_target_cells':['Status','Turns','Findings','DOI'],
          'QUEUE_future_status':'preprint_published','QUEUE_future_turns':'1/5',
          'QUEUE_unrelated_rows_header_and_other_target_cells_preserved':True,
          'state_future_event':'acceptance_mirror_import','state_future_status':'preprint_published',
          'history_append_present_day_real_event_only_no_fabricated_lifecycle':True,
          'import_original_one_turn_no_new_central_attempts':True,
          'native_preserve_all_existing_entries_history_prefix_and_foreign_work':True,
          'prior_scope_inventory_and_historical_180_inventory_remain_unchanged':True,
          'expected_merge_conflict_area':'QUEUE.md is the only original PR path changed on main since the common base; whether Git reports a textual conflict must be checked at execution.',
          'preferred_mechanism':'ROOT controlled two-parent merge of exact original head into current local main during authorized exclusive cross-chat Git-writer window, then ordinary non-force push and independent GitHub/main/DOI/tracker/native readback.',
          'foreign_index_rule':'If any foreign paths are staged, preserve them and defer merge until their owner has committed them and the real index is clean. Never reset, stash, unstage or commit foreign entries.',
          'no_standard_index_lock_held_across_git_merge_add_commit_push':'Git itself needs its standard index lock; exclusivity comes from the authorized shared-writer window.',
          'server_merge_alternative':'Only if freshly mergeable and exact head unchanged; server merge does not itself perform DOI/native reconciliation, and current base must be verified separately from the historical PR baseRefOid.',
          'no_dependency_on_nonclaimed_PR48_PR49_or_other_partial_acceptance':True,
          'ROOT_only_actual_PR_Git_Zenodo_Sheets_native_operations':True,
          'plan_preparation_percent':100,'actual_native_acceptance_percent':0,'new_math_or_priority_credit':False}
    dump(D/'PLAN.json',plan)
    report=f'''# PR18 native acceptance plan

This is a read-only plan for the eligible claimed solution30001075 / OWR-2090-028. The exact submitted head is `{H}`, status `claimed_solved`, original budget1/5. Fresh metadata in the attached genuine observation still reports OPEN draft. No native, Git, PR, Zenodo or Sheets action was performed. No other PR science was inspected. Original source custody is reused, not new mathematical evidence.

ROOT's current bounded priority assessment resolves the former named-article access hold and allows fixed-preprint preparation/review. It does not declare a reviewed final package, DOI, tracker row or acceptance. The present `A18/preprint_v1/paper.tex` observation is a dated draft pin only. Both requested fresh package reviews and all substantive repairs must finish before the plan can be executed. DOI, publication-file manifest, tracker range and merge commit remain unknown.

## Exact file and native mapping

`OBSERVATIONS.json` maps all15 original files from the existing `A18/source_snapshot` custody to `{K}/`. Their Git blobs, Git100644 modes, SHA256 and byte counts agree with the existing snapshot manifest and exact original Git tree. They remain byte-for-byte historical originals. All15 target paths are presently absent from main/worktree. PR18's only other changed path is `{Q}`. The shared QUEUE row currently says queued0/5; native state has no30001075 key and native history has no30001075 event.

At actual completed publication, import these15 original blobs unchanged. Keep the final reviewed manuscript, PDF, verification archive and publication receipts in ROOT's final selected A18 package; no giant evidence copy into the problem folder is needed. Add only `{K}/acceptance.json` and `{K}/CURRENT_RESULT.md` to identify the original files as dated originals and point to the actual operative reviewed result, final package manifest, real DOI, tracker readback and remote merge evidence. The original candidate SHA b04aaf0b5a42d79ad26daf27880774a3f126858ef545b3f366a2b8b62e277252 differs from the already reviewed candidate8ac19b70bd9081107e903ca47bb9dd6ad05274f604d03000a7fd18e3cfb3bf12. Preserve that distinction; do not falsely certify the older candidate as the final paper or modify historical proof/source/turn ledgers. Any final global repair belongs in all operative final-package representations and their explicit links.

Change only the30001075 QUEUE Status/Turns/Findings/DOI cells after actual publication: preprint_published,1/5, a concise accurate accepted-result/source/review summary, and the actual DOI. Preserve every other row, header, rank/score/source/Chat cell. Add one present-day `acceptance_mirror_import` state record and append the identical real event to history, following the existing eligible9/16 schema: preprint_published; turns_used1; turn_limit5; original source/statement/review identity; actual accepted-source, package/priority/review/publication/merge receipts. Do not invent historical readiness/candidate/verification transitions or add new proof-attempt turns. Preserve all other native state entries and the complete history prefix. Dated observation has{len(state)} entries/{sum(s.get('turns_used',0) for s in state.values())} imported turns; actual execution must use its fresh baseline, then add only one target/one original turn. The old180 inventory and fixed revised scope inventory remain unchanged historical records; ROOT can record new progress in separate actual PR18 publication evidence.

## Concrete safe integration order

1. ROOT finishes/fixes and freezes the preprint and support package, obtains clean fresh independent reviews, publishes the exact intended Zenodo metadata/files, verifies public bytes and the actual DOI, and appends/readbacks the one authorized Sheets row without a duplicate. A failed publication or review does not authorize a merge.
2. Obtain the authorized exclusive shared-chat Git-writer window. Recheck current local/remote main, exact PR18 head/OPEN state, selected native row/key/history absence, owned-path cleanliness, full foreign dirty bodies/modes, and real staged domain. The dated observed foreign staged list is in OBSERVATIONS; it is not a waiver. If foreign staging exists, preserve it and defer until its owner has completed it and the index is clean. No reset/stash/unstage or partial commit during a merge. A standard index.lock must not be held across Git's merge/add/commit operations; Git requires that lock itself.
3. On main, ROOT performs the normal local `git merge --no-ff --no-commit {H}`. This is a proposed future command only. The computed common base is `{base}`; GitHub's PR baseRefOid is historical, not current-main authority. Original scientific paths have no overlap with current-main edits. QUEUE is the only shared original PR path changed since base, so expect its possible text conflict. If conflicted, reconcile only the selected row into the fresh current QUEUE body, preserving all unrelated current bytes. Never choose the entire old QUEUE from the PR. An unexpected source conflict or wider staged scope stops integration for inspection.
4. Within the same window, ROOT makes only the described native/canonical administrative changes using actual publication evidence. Review exact staged scope, original15 blobs/modes, complete unrelated preservation, native deltas and real two-parent merge parents(current main,original head). Commit the exact authorized scope, then use an ordinary non-force main push; a remote race requires fresh reconciliation, never force or blind retry. Keep foreign index/worktree entries preserved. GitHub server merge is an alternative only if freshly mergeable with exact head matching, and still requires separate native reconciliation; it does not solve a QUEUE conflict or certify the package.
5. Independently read back remote main/tree/parents, GitHub's actual PR disposition, the final canonical15 identities and operative links, selected QUEUE cells, one state/history event, original1/5 accounting, DOI/public files and tracker row. Do not claim GitHub automatically marked merged until its actual metadata says so. Preserve genuine failures and partial progress; a later phase must never overwrite a failed receipt as PASS.

This route has no dependency on excluded PR48/49 or any nonclaim disposition. It creates no new native acceptance framework or executable production helper. ROOT owns every future mutation and checkpoint; this child authored only the small plan. Plan preparation100%; actual acceptance0%; new mathematical or priority credit0%.
'''
    (D/'REPORT.md').write_text(report)
    (D/'RESEARCH_LOG.md').write_text(f'{started} — Read-only PR18 mapping/merge mechanism preparation; plan completion estimate10%. Original15/source custody retained.\n{utc()} — Exact15 tree/custody identities and fresh PR metadata mapped; native target absent, queued0/5. Current priority decision resolves historical access hold; fixed package/DOI remain future. Foreign index preserved, proposed exclusive-window main mechanism documented. Plan preparation100%, actual native acceptance0%, new discovery0%. No live mutations.\n')
    dump(C/'COMPLETE_COMMANDS.json',COMMANDS)
    dump(C/'RECEIPT.json',{'schema':'pr18-native-plan-actual-readonly-author/v1','actual_pid':os.getpid(),'started_utc':started,'ended_utc':utc(),
                         'status':'PASS_ADMINISTRATIVE_PLAN_AUTHOR','source':pin(Path(__file__)),'prelaunch':pin(C/'PRELAUNCH_SOURCE.py'),
                         'command_count':len(COMMANDS),'native_or_Git_ref_index_publication_action':False})
    rows=[pin(p) for p in sorted(D.rglob('*')) if p.is_file()]
    dump(D/'READY.json',{'schema':'pr18-native-plan-readiness/v1','status':'READY_READONLY_PLAN_ONLY','actual_author_pid':os.getpid(),'utc':utc(),
                        'self_excluded':'READY.json','files':rows,'plan':pin(D/'PLAN.json'),'report':pin(D/'REPORT.md'),
                        'future_DOI':None,'future_acceptance':None,'ROOT_only_mutation':True})
    print(json.dumps({'status':'READY_READONLY_PLAN_ONLY','actual_pid':os.getpid(),'original_files':15,'READY':pin(D/'READY.json'),
                      'main_dated':mainhead,'foreign_staged_count':len(staged),'new_native_or_git_actions':False}))

if __name__=='__main__':
    try:main()
    except BaseException:
        import traceback
        if C.exists():
            dump(C/'FAILED_COMMANDS.json',COMMANDS);(C/'FAILURE.txt').write_text(traceback.format_exc())
        raise
