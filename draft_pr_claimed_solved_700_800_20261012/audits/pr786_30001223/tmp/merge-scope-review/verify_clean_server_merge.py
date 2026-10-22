#!/usr/bin/env python3
"""Read-only actual server merge verification, bound to the direct-route verdict."""
import json,datetime,subprocess
from readonly_merkle import T,O,need,digest,api,write_json,load_initial,check_sources,Merkle
pre=json.loads((O/'PRE_MUTATION_VERDICT.json').read_text())
direct=json.loads((O/'DIRECT_PREMERGE_VERDICT.json').read_text())
initial=load_initial()
need(pre['result']==direct['result']=='PASS','premerge verdicts')
need(pre['plan_sha256']==digest((T/'root-receipts/MERGE_CONFLICT_PLAN.json').read_bytes()),'unchanged source scope plan')
need(direct['plan_sha256']==digest((T/'root-receipts/DIRECT_MERGE_PLAN.json').read_bytes()),'unchanged direct plan')
need(direct['source_scope_verdict_sha256']==digest((O/'PRE_MUTATION_VERDICT.json').read_bytes()),'direct route binds full proof')
source=check_sources(initial)
pr=api('pulls/786')
need(pr['merged'] and pr['state']=='closed','server PR actually merged')
old=pre['original_reviewed_candidate_head'];head=pr['merge_commit_sha']
need(pr['head']['sha']==old,'original reviewed PR head retained')
commit=api('git/commits/'+head)
need(commit['sha']==head,'server merge commit identity')
parents=[p['sha'] for p in commit['parents']]
need(parents==direct['intended_parents']==[pre['main_parent'],old],'clean-path ordered server merge parents')
need(commit['tree']['sha']==pre['expected_resulting_tree'],'actual server merge full root')
m=Merkle('actual_server_merge')
changes=m.diff(pre['main_tree'],commit['tree']['sha'])
need(json.loads(json.dumps(changes))==pre['actual_relative_main_changes'],'actual full tree changes match independently reviewed42paths')
q=changes['unsolved_math_prioritization/QUEUE.md']
before=m.blob(q['before'][2]);after=m.blob(q['after'][2])
need(before.replace(initial['original_queue_before_row'].encode(),initial['original_queue_after_row'].encode(),1)==after==(T/'root-receipts/MERGE_CONFLICT_QUEUE.txt').read_bytes(),'actual queue exact single-row byte splice')
branch=api('git/ref/heads/research/30001223-young-module-counterexamples-20261006')
need(branch['object']['sha']==old,'PR branch unchanged at original head')
currentmain=api('git/ref/heads/main')['object']['sha']
ancestry=api('compare/'+head+'...'+currentmain+'?per_page=1&page=2')
need(ancestry['merge_base_commit']['sha']==head and ancestry['behind_by']==0 and ancestry['status'] in ('ahead','identical'),'server merge on current main ancestry')
need(subprocess.run(['git','branch','--show-current'],capture_output=True,text=True,check=True).stdout.strip()=='main','local branch remains main')
need(check_sources(initial)==source,'source preserved through final readback')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={'utc':now,'result':'PASS','issues':[],'actionable_issue_count':0,'pr':786,'problem':'30001223','scope':'Independent administrative actual-merge/tree/source-preservation review only','path_taken':'Clean original-head official merge; proposed conflict integration unnecessary and unused','direct_plan_sha256':direct['plan_sha256'],'source_scope_plan_sha256':pre['plan_sha256'],'original_reviewed_candidate_head':old,'reviewed_head':old,'original_historical_parent':pre['original_historical_parent'],'original_parent_ancestor_of_pinned_main':True,'main_parent':pre['main_parent'],'server_merge_commit':head,'server_merge_parents':parents,'server_merge_tree':commit['tree']['sha'],'current_remote_main':currentmain,'server_merge_ancestor_of_current_main':True,'PR_branch_head_after_merge':branch['object']['sha'],'PR_branch_unchanged':True,'PR_branch_integration_mutation_needed':False,'original_source_files':41,'current_source_files_including_manifest':213,'six_frozen_release_artifacts':6,'source_preservation':source,'exact_relative_main_changes':changes,'all_other_main_paths_preserved':True,'every_unrelated_QUEUE_byte_preserved':True,'extra_whole_paper_review_required':False,'new_substantive_review_claimed':False,'Git_API_read_receipts':m.receipts,'server_PR_state':{'state':pr['state'],'merged':pr['merged'],'draft':pr['draft'],'head':pr['head']['sha'],'merge_commit':pr['merge_commit_sha'],'merged_at':pr['merged_at']},'completion_estimate_percent':100,'exceptions':['100% refers only to assigned administrative merge-scope review; parent native/accounting closeout is separate','No Git/API mutations, source/native/readiness edits, publication, or external-person communication by reviewer','No additional mathematical, whole-paper, metadata-adapter, or priority review claimed','Original substantive review/source identity retains original candidate head; server merge commit is separate integration evidence','Raw read-only Git API data compressed in sibling scratch to conserve RAM']}
write_json(O/'VERDICT.json',result)
write_json(O/'ACTUAL_SERVER_MERGE.json',{'commit':{'sha':commit['sha'],'parents':parents,'tree':commit['tree']['sha']},'PR':result['server_PR_state'],'branch_sha':branch['object']['sha'],'current_main':currentmain,'merge_to_current_main':{'status':ancestry['status'],'merge_base':ancestry['merge_base_commit']['sha'],'behind_by':ancestry['behind_by']}})
report=f'''# PR786 administrative merge-scope review

PASS; zero actionable issues. GitHub merged the exact original reviewed PR head {old} through server merge commit {head}. The PR branch remains at the original head. The prepared conflict-integration route was safe but unnecessary; no new branch integration or whole-paper review is claimed.

The actual server merge has ordered parents {pre['main_parent']} and {old}, and full tree {commit['tree']['sha']}, exactly the independently reconstructed post-publication/tracker direct plan. Original historical parent {pre['original_historical_parent']} is an ancestor of pinned main. The actual delta is precisely 41 immutable original source additions plus the original own claimed_solved 1/5 QUEUE row; every other main path and unrelated QUEUE byte is preserved.

All 41 frozen originals, the exact closed 213-file current source, original source identity and six release artifacts remain unchanged. The server merge is on current main ancestry. Substantive review identity remains the original candidate; the server merge hash is separate administrative integration evidence.

Completion estimate: 100% of assigned administrative review. Native acceptance/accounting are parent closeout gates. This reviewer performed only read-only Git/API operations and writes within its own review/scratch directories.
'''
(O/'REPORT.md').write_text(report)
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Actual clean original-head server merge verified: exact parents/root and 42 changes; 41 originals, 213 current source files and six artifacts unchanged; original PR branch unchanged. Completion estimate: 100% of assigned administrative verification, packet custody pending.\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('exact_relative_main_changes','Git_API_read_receipts')},indent=2))
