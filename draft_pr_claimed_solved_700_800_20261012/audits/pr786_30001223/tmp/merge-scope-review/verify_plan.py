#!/usr/bin/env python3
"""Independent actual-plan receipt. Read-only Git/API; own receipt output only."""
import json,sys,datetime,hashlib,subprocess
from pathlib import Path
from readonly_merkle import T,O,S,P,need,digest,git_oid,api,write_json,load_initial,check_sources,Merkle,trie_for
EXPECTED_PLAN_SHA='b9312747785635f512496d1f6f0c1ff5077f5e22422cbf5728a9d1fb430db432'
planpath=T/'root-receipts/MERGE_CONFLICT_PLAN.json'
body=planpath.read_bytes();need(digest(body)==EXPECTED_PLAN_SHA,'parent supplied exact actual-plan SHA')
plan=json.loads(body);initial=load_initial();source_receipt=check_sources(initial)
old=initial['original_reviewed_candidate_head'];main=plan['main_parent'];q='unsolved_math_prioritization/QUEUE.md'
need(plan['pr']==786 and plan['problem']=='30001223','scope identifiers')
need(plan['original_reviewed_candidate_head']==old,'old head')
need(plan['branch']=='research/30001223-young-module-counterexamples-20261006','existing branch')
need(plan['original_historical_parent']==initial['historical_base'],'original historical parent binding')
need(plan['intended_parents']==[old,main],'ordered parents')
need(plan['queue_before_row']==initial['original_queue_before_row'] and plan['queue_after_row']==initial['original_queue_after_row'],'own original queue rows')
merkle=Merkle('pre_mutation')
maincommit=api('git/commits/'+main);need(maincommit['sha']==main and maincommit['tree']['sha']==plan['main_tree'],'main commit/root binding')
write_json(O/'PINNED_MAIN_COMMIT.json',{'sha':maincommit['sha'],'tree':maincommit['tree']['sha'],'parents':[x['sha'] for x in maincommit['parents']]})
# Page2 with one commit omits the compare endpoint's potentially huge file-patch list.
ancestry=api('compare/'+initial['historical_base']+'...'+main+'?per_page=1&page=2')
need(ancestry['merge_base_commit']['sha']==initial['historical_base'] and ancestry['status'] in ('ahead','identical') and ancestry['behind_by']==0,'original historical parent ancestor of main')
write_json(O/'ORIGINAL_PARENT_ANCESTRY.json',{'base':initial['historical_base'],'head':main,'status':ancestry['status'],'merge_base':ancestry['merge_base_commit']['sha'],'ahead_by':ancestry['ahead_by'],'behind_by':ancestry['behind_by'],'comparison_method':'Read-only GitHub compare, page2 per_page1 to omit large file diffs'})
qfile=(T/'root-receipts/MERGE_CONFLICT_QUEUE.txt').read_bytes()
updates={r['path']:('100644','blob',r['git_blob']) for r in initial['original_files']}
updates[q]=('100644','blob',git_oid('blob',qfile))
canonical_updates={p:{'mode':v[0],'type':v[1],'sha':v[2]} for p,v in updates.items()}
need(plan['tree_updates']==canonical_updates and len(updates)==42,'exact42 source/queue updates')
expected=merkle.apply(plan['main_tree'],trie_for(updates))
need(expected==plan['expected_resulting_tree']=='e378c977f2d4210d3d33b3b0256873262685e02d','independent full root reconstruction')
changes=merkle.diff(plan['main_tree'],expected)
need(set(changes)==set(updates) and len(changes)==42,'exact42 actual changes relative main')
for r in initial['original_files']:
    need(changes[r['path']]['before'] is None and changes[r['path']]['after']==('100644','blob',r['git_blob']),'all41 source additions absent on pinned main '+r['path'])
qc=changes[q];need(qc['before'][:2]==qc['after'][:2]==('100644','blob'),'queue mode/type')
qb=merkle.blob(qc['before'][2]);before=initial['original_queue_before_row'].encode();after=initial['original_queue_after_row'].encode()
need(qb.splitlines(keepends=True).count(before)==1 and qfile.splitlines(keepends=True).count(after)==1,'unique exact own queue rows')
need(qb.replace(before,after,1)==qfile,'every unrelated queue byte preserved')
remote_main=api('git/ref/heads/main');remote_branch=api('git/ref/heads/'+plan['branch']);pr=api('pulls/786')
need(remote_main['object']['sha']==main,'main drifted since plan')
need(remote_branch['object']['sha']==old and pr['head']['sha']==old and pr['state']=='open' and not pr['merged'],'original PR branch/head current')
need(subprocess.run(['git','branch','--show-current'],capture_output=True,text=True,check=True).stdout.strip()=='main','shared checkout remains main')
source_receipt2=check_sources(initial);need(source_receipt==source_receipt2,'source receipt stable')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={'utc':now,'result':'PASS','pr':786,'problem':'30001223','scope':'Exact administrative construction/tree safety; no necessity or execution claim','plan_sha256':EXPECTED_PLAN_SHA,'original_reviewed_candidate_head':old,'main_parent':main,'main_tree':plan['main_tree'],'original_historical_parent':initial['historical_base'],'original_historical_parent_ancestor_of_main':True,'expected_resulting_tree':expected,'intended_parents':[old,main],'tree_updates':canonical_updates,'actual_relative_main_changes':changes,'exact_changed_paths':42,'original_source_additions':41,'all_source_collisions_absent':True,'all_other_main_paths_preserved':True,'every_unrelated_QUEUE_byte_preserved':True,'source_preservation':source_receipt2,'frozen_six_files':initial['six_frozen_files'],'independently_verified_Git_objects':merkle.receipts,'remote_at_review':{'main':remote_main['object']['sha'],'PR_head':pr['head']['sha'],'state':pr['state'],'draft':pr['draft'],'mergeable':pr['mergeable'],'mergeable_state':pr['mergeable_state']},'mutation_necessary_or_executed':False,'preferred_clean_path':'If original head proves clean, merge that exact original head and independently verify resulting merge tree against this pinned expected root; no branch integration needed.','conditional_conflict_path':'Only if an actual merge conflict is confirmed: construct exactly the specified two-parent integration commit and perform ordinary fast-forward force:false on the existing PR branch after exact-head/main rechecks.','required_mutation_guards':['Consume verdict by exact plan_sha256, original head, pinned main and expected tree','Check current PR open at exact old head and remote main exact pinned main before construction; reject drift','Verify created commit exact ordered parents/tree before ref update','Recheck exact old PR ref immediately before non-force update; read back new commit/ref after update','Preserve immutable original source identity and frozen213source/6release artifacts','Do not claim new whole-paper review; bind new administrative head with explicit original candidate preservation receipt'],'head_binding':'Original candidate/source/review identity immutable; any new reviewed_head means independently scope-verified post-review administrative integration only.','extra_whole_paper_review_required':False,'remaining_parent_gates':['Determine clean vs actually conflicted status on unchanged old head','If conflict path chosen, provide mutation code and resulting actual commit/ref for final independent review','Native acceptance on exact eventual PR head; server exact-head merge verification'],'completion_estimate_percent':65,'exceptions':['Pinned-tree scope is safe; this receipt does not assert a merge conflict exists','No Git/API mutations or source/readiness/native/publication edits by reviewer','Full raw Git API receipt data are compressed only in own sibling scratch; packet contains checkable object IDs and independently computed hashes','No mathematical, whole-paper, publication-adapter, or priority review repeated']}
write_json(O/'PRE_MUTATION_VERDICT.json',result)
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now+' — Exact parent-supplied plan SHA verified; independent full Merkle reconstruction matches expected root;42paths,41original additions, source213/6artifacts and original-parent ancestry pass. Conditional construction scope only; necessity not asserted. Completion estimate:65%.\n'.replace(';42paths,41original','; 42 paths, 41 original').replace('source213/6artifacts','source 213 / 6 artifacts').replace('estimate:65%','estimate: 65%'))
print(json.dumps({k:v for k,v in result.items() if k not in ('tree_updates','actual_relative_main_changes','frozen_six_files','independently_verified_Git_objects')},indent=2))
