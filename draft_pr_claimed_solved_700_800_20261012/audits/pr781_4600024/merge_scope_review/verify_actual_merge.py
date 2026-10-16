import importlib.util,json,hashlib,datetime
from pathlib import Path
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tree_review',P/'verify_merge_tree.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
pre=json.loads((P/'PRE_MUTATION_VERDICT.json').read_text());receipt=json.loads((m.AUDIT/'tmp/root-receipts/MERGE_CONFLICT_RESOLUTION_RECEIPT.json').read_text())
checks={}
def require(k,v):
 checks[k]=bool(v)
 if not v:raise RuntimeError('FAILED '+k)
head=receipt['conflict_resolution_head'];commit=m.api('git/commits/'+head);(P/'actual_commit.json').write_text(json.dumps(commit,indent=2)+'\n')
require('receipt_binds_pre_reviewed_plan',pre['plan_sha256']==hashlib.sha256(m.PLAN.read_bytes()).hexdigest())
require('actual_commit_sha',commit['sha']==head)
require('actual_exact_ordered_parents',[x['sha'] for x in commit['parents']]==[pre['original_reviewed_candidate_head'],pre['main_parent']])
require('actual_exact_tree',commit['tree']['sha']==pre['expected_resulting_tree'])
# Drop all in-memory proposed nodes: next diff obtains the actual published tree.
m.cache.clear()
actual_changes=m.diff(pre['main_tree'],commit['tree']['sha'])
require('actual_full_tree_delta_matches_independent_plan',json.loads(json.dumps(actual_changes))==json.loads(json.dumps(pre['changed_paths'])))
q='unsolved_math_prioritization/QUEUE.md';qb=m.blob(actual_changes[q]['before'][2]);qa=m.blob(actual_changes[q]['after'][2]);expected=(m.AUDIT/'tmp/root-receipts/MERGE_CONFLICT_QUEUE.txt').read_bytes()
require('actual_queue_exact_byte_splice',qa==expected==qb.replace(m.plan['queue_before_row'].encode(),m.plan['queue_after_row'].encode(),1))
require('source_identity_immutable',hashlib.sha256((m.AUDIT/'ROOT_SOURCE_IDENTITY.json').read_bytes()).hexdigest()==pre['frozen_source_identity_sha256'])
for r in m.source['original_files']:
 b=(m.AUDIT/'original'/r['path']).read_bytes()
 require('physical_source_preserved_'+r['path'],len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'])
manifestpath=m.AUDIT/'preprint/source/MANIFEST.json';manifest=json.loads(manifestpath.read_text())
require('source_manifest_immutable',hashlib.sha256(manifestpath.read_bytes()).hexdigest()==pre['source_manifest_sha256'])
for r in manifest['files']:
 b=(m.AUDIT/'preprint/source'/r['path']).read_bytes()
 require('current_source_frozen_'+r['path'],len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'])
for r in pre['six_release_artifacts']:
 b=(m.AUDIT/'preprint'/r['path']).read_bytes()
 require('six_frozen_'+r['path'],len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'])
branch=m.api('git/ref/heads/'+m.plan['branch']);(P/'actual_branch.json').write_text(json.dumps(branch,indent=2)+'\n')
pr=m.api('pulls/781');(P/'actual_PR781.json').write_text(json.dumps(pr,indent=2)+'\n')
require('remote_branch_exact_new_head',branch['object']['sha']==head)
require('PR781_exact_new_head',pr['head']['sha']==head)
require('PR781_open_ready',pr['state']=='open' and not pr['draft'] and not pr['merged'])
require('main_checkout_branch_unchanged',m.subprocess.run(['git','branch','--show-current'],capture_output=True,check=True,text=True).stdout.strip()=='main')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','issues':[],'issue_count':0,'scope':'Independent adversarial administrative merge-conflict/tree/source-preservation review only','original_reviewed_candidate_head':pre['original_reviewed_candidate_head'],'reviewed_head':head,'main_parent':pre['main_parent'],'tree':commit['tree']['sha'],'plan_sha256':pre['plan_sha256'],'checks':checks,'source_current_files_including_manifest':len(manifest['files'])+1,'original_source_files_preserved':48,'publication_artifacts_preserved':6,'all_other_main_paths_preserved':True,'unrelated_QUEUE_bytes_preserved':True,'actual_diff_relative_to_pinned_main':actual_changes,'extra_whole_paper_peer_review_required':False,'head_binding_requirement':'Administrative FINAL_READINESS must identify original_reviewed_candidate_head and new reviewed_head, state byte-preserving post-review conflict resolution with this receipt, and retain original source identity and frozen paper/review/deposit content. This scope review certifies the administrative new head; it does not claim new substantive whole-paper reviews.','remaining_parent_gates':['Update administrative readiness and body truthfully while preserving frozen source identity','Run native acceptance against exact new head using original statement/review hashes','Merge using exact-head pin, then verify server merged state and intended scope'],'PR_merge_complete':False,'completion_estimate_percent':100,'exceptions':['100% refers only to this assigned independent merge-scope review; parent PR integration/native acceptance remain','No repeat mathematical, priority, or paper review; frozen prior input bytes are verified','No Git refs, index, checkout, or source files mutated by this reviewer','No external individual contacted; public GitHub API reads only','Pinned-main preservation established; future concurrent main movement is outside this receipt']}
(P/'VERDICT.json').write_text(json.dumps(result,indent=2)+'\n')
report='''# PR781 merge-conflict scope review\n\nPASS; zero actionable issues. The actual new head `{head}` has exactly parents `{old}` and `{main}` and exact tree `{tree}`. Independently reconstructed and re-read Git trees show precisely 48 original source additions and the original own QUEUE row copied onto pinned main. Every other main path and every unrelated QUEUE byte is preserved.\n\nAll 48 frozen original files, all 150 current source files including the manifest, ROOT_SOURCE_IDENTITY, and all six release artifacts retain their frozen identities. No additional whole-paper review loop is required for this administrative byte-preserving repair.\n\nTruthful binding requires the administrative gate to retain `original_reviewed_candidate_head` and identify `reviewed_head` as the post-review merge-scope-verified head, with this preservation receipt. The source identity and published package must retain the original candidate evidence. Native exact-head acceptance and server merge verification remain parent integration gates.\n\nCompletion estimate: 100% of assigned merge-scope review. No source/Git-reference mutation or external communication by this reviewer.\n'''.format(head=head,old=pre['original_reviewed_candidate_head'],main=pre['main_parent'],tree=commit['tree']['sha'])
(P/'REPORT.md').write_text(report)
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+result['utc']+' — Final PASS, zero issues. Re-read actual two-parent commit and full relevant Merkle tree, exact queue bytes, 48 originals, six artifacts and all current150 source files; remote PR/head exact and ready. Completion estimate: 100% of assigned review; parent native acceptance/merge still required.\n')
manifest_entries={}
for p in sorted(P.iterdir()):
 if p.is_file() and p.name!='MANIFEST.json':
  b=p.read_bytes();manifest_entries[p.name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(P/'MANIFEST.json').write_text(json.dumps({'schema':'pr781-independent-merge-scope-review/v1','utc':result['utc'],'files':manifest_entries,'explicit_exceptions':['MANIFEST.json'],'result':'PASS'},indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','actual_diff_relative_to_pinned_main')},indent=2))
