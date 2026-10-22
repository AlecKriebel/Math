import sys,json,hashlib,base64,datetime,subprocess
from pathlib import Path
R=Path('/Users/alec/Documents/Math'); D=R/'draft_pr_claimed_solved_700_800_20261012'; A=D/'audits/pr781_4600024'; M=A/'tmp/root-receipts'
sys.path.insert(0,str(D)); from graphql_scoped_commit import Remote,get_pr
from remote_scoped_commit import api,oid,need
plan=json.loads((M/'MERGE_CONFLICT_PLAN.json').read_text()); old=plan['original_reviewed_candidate_head']; parent=plan['main_parent']; branch=plan['branch']
verdict=json.loads((A/'tmp/merge-scope-review/PRE_MUTATION_VERDICT.json').read_text())
need(verdict['result']=='PASS' and verdict['plan_sha256']==hashlib.sha256((M/'MERGE_CONFLICT_PLAN.json').read_bytes()).hexdigest() and verdict['original_reviewed_candidate_head']==old and verdict['main_parent']==parent and verdict['expected_resulting_tree']==plan['expected_resulting_tree'],'Independent exact-plan pre-mutation gate')
need(subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()=='main','Stay on main')
pr=get_pr(781); need(pr['state']=='open' and not pr['merged'] and pr['head']['sha']==old,'PR changed')
need(api('git/ref/heads/main')['object']['sha']==parent,'Main changed since independently audited plan; rebuild/review plan before mutation')
need(api('git/ref/heads/'+branch)['object']['sha']==old,'Existing PR branch changed')
main=Remote(parent); need(main.root==plan['main_tree'] and main.expected_tree(plan['tree_updates'])==plan['expected_resulting_tree'],'Plan Merkle mismatch')
queue=(M/'MERGE_CONFLICT_QUEUE.txt').read_bytes(); q='unsolved_math_prioritization/QUEUE.md'; need(oid('blob',queue)==plan['tree_updates'][q]['sha'],'Planned queue drift')
g=json.loads((A/'FINAL_READINESS.json').read_text())
for row in g['publication_files']:
 b=(A/'preprint'/row['path']).read_bytes(); need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Frozen release drift')
b=api('git/blobs','POST',{'content':base64.b64encode(queue).decode(),'encoding':'base64'}); need(b['sha']==plan['tree_updates'][q]['sha'],'Uploaded queue blob')
tree=api('git/trees','POST',{'base_tree':main.root,'tree':[dict(path=p,**v) for p,v in plan['tree_updates'].items()]}); need(tree['sha']==plan['expected_resulting_tree'],'Created tree differs from exact planned full root')
message='Merge current main into PR781; preserve all reviewed sources and resolve only its QUEUE row'
commit=api('git/commits','POST',{'message':message,'tree':tree['sha'],'parents':[old,parent]}); c=commit['sha']
checked=api('git/commits/'+c); need(checked['tree']['sha']==plan['expected_resulting_tree'] and [x['sha'] for x in checked['parents']]==[old,parent],'Created commit parents/tree')
pre={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'VERIFIED_UNREFERENCED_COMMIT','commit':c,'parents':[old,parent],'tree':tree['sha'],'message':message,'PR_ref_not_yet_updated':True}; (M/'MERGE_CONFLICT_CREATED_COMMIT.json').write_text(json.dumps(pre,indent=2)+'\n'); print(json.dumps(pre),flush=True)
need(api('git/ref/heads/'+branch)['object']['sha']==old,'Concurrent PR branch changed; do not update')
result=api('git/refs/heads/'+branch,'PATCH',{'sha':c,'force':False},check=False)
fresh=api('git/ref/heads/'+branch)['object']['sha']; need(fresh==c,'Ref update unconfirmed; inspect before retry: '+json.dumps(result))
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','pr':781,'problem':'4600024','branch':branch,'original_reviewed_candidate_head':old,'conflict_resolution_head':c,'parents':[old,parent],'main_parent':parent,'tree':tree['sha'],'expected_tree':plan['expected_resulting_tree'],'paths_relative_to_main':list(plan['tree_updates']),'original_candidate_files_preserved':48,'all_other_main_paths_preserved':True,'unrelated_queue_bytes_preserved':True,'ordinary_two_parent_merge':True,'ref_force':False,'shared_checkout_index_refs_objects_untouched':True,'frozen_six_changed':False}
(M/'MERGE_CONFLICT_RESOLUTION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n'); print(json.dumps(receipt),flush=True)
