"""Prepare three private PR140 checkpoint drafts, without shared-state writes."""
from pathlib import Path
import copy,datetime,hashlib,json,os,stat

D=Path(__file__).resolve().parent
A=D.parent
P=A.parent.parent
OLD=A/'program3_active_snapshot_preparation_20261007'
NAMES=('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')
EXPECTED={
 'CURRENT_PROGRESS.json':'04719198e465d420f809824d88dd6c3469f2deea7bc2114e7d333bfcc3b5a796',
 'CURRENT_PROGRESS.md':'83075b82fd5d11bd417cac5656aa32ef87acf12408d9c1cee6cc743c098185c7',
 'RESEARCH_LOG.md':'6c9436d892aec951f425ed21f50fe4a6c55526e14b2f796ca7c309c33f2e4623',
 'audits/pr140_5100023/ROOT_PRIORITY_GATE.json':'ab0ce030ecb1923740bc78342587bfef4e6ec8c1ef263a697b3e5f1ac0af5795',
 'audits/pr140_5100023/ROOT_PACKAGE_CANDIDATE_READBACK.json':'029e84edc16f3c1086ec6eb52dae2c818172a9c0f56c8c4750ab51aede9d8ffd',
 'audits/pr140_5100023/program3_active_snapshot_preparation_20261007/MANIFEST.json':'4a19bf27cc9f936e87f28573c28036bee3b8cfd3e73a36603a86196a85e06f41',
 'audits/pr134_2306064/scoped_completion_transaction_20261007/ROOT_FINAL_METADATA_ACCEPTANCE_RECEIPT.json':'dea4622811f9e62e5a200c3cb2ce5b00ec9476af782ff33d551ab9e18d4425f6',
}
def require(ok,message):
 if not ok:raise RuntimeError(message)
def pin(p):
 st=p.lstat();require(stat.S_ISREG(st.st_mode),'Regular input required')
 b=p.read_bytes();after=p.lstat()
 require((st.st_dev,st.st_ino,st.st_mode,st.st_mtime_ns,st.st_size)==(after.st_dev,after.st_ino,after.st_mode,after.st_mtime_ns,after.st_size),'Input changed while read')
 require(stat.S_IMODE(after.st_mode)==0o644,'Expected mode 0644')
 return b,{'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':'0644','Git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def encoded(obj):return (json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()
inputs={};pins={}
for rel,h in EXPECTED.items():
 b,info=pin(P/rel);require(info['sha256']==h,'Frozen source/preimage drift: '+rel);inputs[rel]=b;pins[rel]=info
manifest_rel='audits/pr140_5100023/program3_active_snapshot_preparation_20261007/MANIFEST.json'
oldmanifest=json.loads(inputs[manifest_rel])
for member in oldmanifest['members']:
 name=member['program_relative_path'];p=OLD/'postimages'/name
 b,info=pin(p);require(info==member['proposed_postimage'],'Former candidate changed')
 inputs['former_postimage/'+name]=b;pins['former_postimage/'+name]=info
priority_rel='audits/pr140_5100023/ROOT_PRIORITY_GATE.json'
package_rel='audits/pr140_5100023/ROOT_PACKAGE_CANDIDATE_READBACK.json'
priority=json.loads(inputs[priority_rel]);package=json.loads(inputs[package_rel])
receipt_rel='audits/pr134_2306064/scoped_completion_transaction_20261007/ROOT_FINAL_METADATA_ACCEPTANCE_RECEIPT.json'
receipt=json.loads(inputs[receipt_rel])
require(priority['status']=='BOUNDED_PRIORITY_SUPPORTS_QUALIFIED_RESOLUTION_NOTE' and priority['publication_upload_clearance'] is False,'Priority gate differs')
require(priority['absolute_priority']=='UNESTABLISHED' and priority['independent_discovery']=='UNESTABLISHED' and priority['exclusive_theorem_novelty_over_later_note'] is False,'Priority scope upgraded')
require(priority['later_exact_note_DOI']=='10.5281/zenodo.23092466' and priority['PR50_exception_used'] is False,'Wrong later note/exception')
require(package['case_best_guess_percent']==80 and package['fresh_package_reviews_pending'] is True and package['upload_clearance'] is False,'Package gate differs')
require(receipt['status']=='ACCEPTED_COMPLETE' and receipt['metadata_commit']=='fa9050ddaa5fa8b8696baedd56adbfd67b287a94','Prior completion unavailable')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();pid=os.getpid()
current=json.loads(inputs['former_postimage/CURRENT_PROGRESS.json'])
former=copy.deepcopy(current)
current['historical_preparation_snapshots']=[{
 'UTC':former['UTC'],'source_manifest':manifest_rel,'source_manifest_sha256':pins[manifest_rel]['sha256'],
 'case_percent':60,'priority_status':'in_progress','status':'SUPERSEDED_UNINSTALLED_PREPARATION',
 'commit_push_or_install_occurred':False,
 'scope':'Prior dated PR140 program-three proposal. ROOT reports failed checkpoint created no commit, push or installation; physical program preimages still equal PR134 acceptance postimages.'}]
current.update({
 'UTC':utc,'updated_UTC':utc,'program_snapshot_semantics':'PACKAGE_REVIEW_CHECKPOINT_PROPOSAL',
 'current_PR_workflow_percent':80,'current_workflow_estimate_percent':80,
 'current_priority_status':'completed_bounded_qualified_support',
 'current_priority_audit_percent':100,
 'current_priority_clearance':True,
 'current_priority_clearance_scope':'Bounded support for preparing a qualified resolution note only; no absolute/exclusive priority or independent-discovery claim, and no upload clearance.',
 'current_bounded_priority_support_for_qualified_resolution_note':True,
 'current_priority_gate':priority_rel,'current_priority_gate_sha256':pins[priority_rel]['sha256'],
 'current_priority_status_source':priority_rel,
 'current_priority_audit_scope':'The inspected primary literature did not establish an earlier complete answer to the target. The project public PR is documented on September 30, before the specific October 1 Ferudun deposit with exact target overlap. That later result is credited. This bounded audit establishes neither absolute priority nor exclusive theorem novelty nor independent discovery.',
 'current_later_exact_note_author':'Ferudun',
 'current_later_exact_note_DOI':priority['later_exact_note_DOI'],
 'current_later_exact_note_created_at':priority['later_exact_note_created_at'],
 'current_project_public_PR_created_at':priority['project_public_PR_created_at'],
 'current_absolute_priority_established':False,'current_exclusive_theorem_novelty_over_later_note':False,
 'current_independent_discovery_established':False,'current_copying_or_collaboration_inferred':False,
 'current_novelty_established':False,'current_PR50_exception_used':False,
 'current_publication_package_prepared':True,
 'current_publication_package_candidate_readback':package_rel,
 'current_publication_package_candidate_readback_sha256':pins[package_rel]['sha256'],
 'current_publication_package_manifest_sha256':package['package_manifest_sha256'],
 'current_publication_package_review_status':'round_1_in_progress',
 'current_publication_package_reviews_required':True,
 'current_publication_package_review_clearance':False,
 'current_publication_upload_clearance':False,'current_publication_ready':False,
 'current_disposition':'qualified_resolution_package_under_fresh_adversarial_review',
 'current_core_disposition_complete':False,
 'current_mathematical_scope':[
   'a>b>0','nondegenerate nested confocal elliptical caustic 0<lambda<b^2',
   'even least period N >= 4 with distinct vertices',
   'simple or primitive star family; either orientation; antipedal intersections of full lines'],
 'current_remaining_required_steps':'Complete the fresh adversarial package review, fix findings consistently and repeat with a new reviewer until none remain; obtain actual upload clearance and then follow the authorized publication/tracker/disposition process. Scoped checkpoint publication, installation and readbacks have not occurred.',
 'next_step':'Continue active PR140 fresh package-review loop; repair all findings and repeat independently. Upload clearance is false; no completed case, publication, tracker update or intake past PR140 is asserted.',
 'remaining_current_step':'PR140 qualified resolution package is prepared and round 1 adversarial review is in progress. Exact program checkpoint and later publication/disposition actions remain unperformed.',
 'active_checkpoint_commit':None,'active_checkpoint_acceptance_receipt':None,
 'advance_to_next_PR_authorized_now':False,
})
for key in ['current_priority_status','current_priority_status_source','current_priority_audit_scope','current_remaining_required_steps','next_step','remaining_current_step']:
 require('comparison_pending' not in str(current[key]) and 'priority_in_progress' not in str(current[key]),'Stale current priority pending label')
require(current['fully_completed_count']==23 and len(current['published_PRs'])==11 and 140 not in current['fully_completed_eligible_PRs'],'Counts promoted early')
require(current['last_completed_PR']==134 and current['last_completed_PR_workflow_percent']==100 and current['last_completed_metadata_checkpoint_commit']==receipt['metadata_commit'],'PR134 completion changed')
require(current['current_DOI'] is None and current['current_Zenodo_published'] is False and current['current_tracker_updated'] is False and current['persistent_goal_complete'] is False and current['persistent_goal_status']=='active','Future publication/completion fabricated')
note=f'''\n\n## {utc} — PR140 qualified package review checkpoint; case 80%, program 23/99 = 23.23%, 11 published

This supersedes the dated 60% PR140 preparation snapshot as current proposed state while retaining that entire text as history. The earlier checkpoint attempt created no commit, push or installation; actual physical program files still equal the PR134 acceptance postimages. This new three-file proposal is also preparation only. It asserts no accepted checkpoint, Zenodo deposit, DOI, spreadsheet row, merge or new completed case.

The explicit primitive-even mathematical gate remains PASS for even least period N >= 4, distinct vertices, a > b > 0, a nondegenerate confocal elliptical caustic 0 < lambda < b², full-line unweighted unprimed k405 antipedals, simple or primitive star families, and either orientation. The circle is separate; the source's least-period convention remains a supported interpretation rather than a formal definition. Original PR140 effort remains 2/5 and zero central proof-search turns were added.

The actual bounded priority gate {priority_rel} is complete and supports preparation of a qualified resolution note. Inspected primary literature did not establish an earlier complete target answer. The documented project public PR date is {priority['project_public_PR_created_at']}, preceding the specific Ferudun deposit at {priority['later_exact_note_created_at']} (DOI {priority['later_exact_note_DOI']}); its exact overlap is credited. Absolute priority, exclusive theorem novelty and independent discovery remain unestablished; no copying or collaboration is inferred. The existing authorized process supports this qualified note, and no PR50 exception was used. Earlier priority-in-progress and comparison-pending records are dated history, superseded by this gate.

The actual package candidate readback {package_rel} records a five-page compiled and visually checked PDF, matching deposit metadata, a checked support archive, six positive portable verifier runs and eight rejected negative controls with all 14 children reaped and process groups empty. A fresh whole-package adversarial review round 1 is now running; findings must be fixed consistently and review repeated with a new reviewer until none remain. Upload clearance remains false. The manuscript/package and this proposed checkpoint are not claims of an actual publication, installation or disposition.

PR134 retains its actual 100% completion: metadata commit fa9050ddaa5fa8b8696baedd56adbfd67b287a94, native commit 6c0c941ff4eaa0abe5df9c37003a7eb555b3688f, and authenticated acceptance receipt {receipt_rel}. Its qualified already-solved findings remain scoped to that historical case. PR135–PR139 remain untouched, unreviewed and unaudited status-only skips. Counts stay 23 of the dated 99 cases (23.23%) and 11 published; active PR140 is excluded. The persistent goal remains ACTIVE and incomplete; no intake past PR140 is claimed. This UTC is actual preparation time, not a future acceptance or publication time.
'''
post={NAMES[0]:encoded(current)}
for name in NAMES[1:]:post[name]=inputs['former_postimage/'+name]+note.encode()
out=D/'postimages3';out.mkdir(exist_ok=False)
members=[]
for name in NAMES:
 p=out/name
 with p.open('xb') as f:f.write(post[name])
 p.chmod(0o644);b,info=pin(p);require(b==post[name],'Postimage readback mismatch')
 if name!=NAMES[0]:require(b.startswith(inputs[name]) and b.startswith(inputs['former_postimage/'+name]),'Historical prefix changed')
 members.append({'program_relative_path':name,'preimage':pins[name],'proposed_postimage':info,'former_proposal_body':pins['former_postimage/'+name]})
for rel,info in pins.items():
 p=Path(info['path']);require(pin(p)[1]==info,'Input changed during source-only preparation: '+rel)
manifest={
 'schema':'pr140-program-three-package-review-snapshot-preparation/v1','status':'PREPARATION_ONLY_REQUIRES_INDEPENDENT_REVIEW',
 'UTC':utc,'actual_preparer_PID':pid,'members':members,'whole_body_source_bindings':pins,
 'case_best_guess_percent':80,'preparation_completion_percent':100,
 'invariants':{'completed':23,'dated_eligible_total':99,'published':11,'last_completed_PR':134,'last_completed_case_percent':100,
   'current_PR':140,'priority_review_completed_bounded':True,'absolute_exclusive_priority_or_independent_discovery_established':False,
   'round_1_fresh_package_review_in_progress':True,'upload_clearance':False,'PR50_exception_used':False,
   'old_physical_program_preimages_unchanged':True,'old_proposal_and_history_unchanged':True,'PR135_to_139_untouched_skips':True,
   'persistent_goal_status':'active','persistent_objective_complete':False,'no_intake_past_PR140':True},
 'actions_performed':{'own_source_and_three_private_postimages_only':True,'global_files_or_native_changed':False,'Git_index_ref_remote_or_API_write':False,'manuscript_or_frozen_verifiers_changed':False,'Zenodo_Sheet_or_PR_mutation':False},
 'authority_condition':'Exact source/plan independent review and future scoped publication, local installation and actual complete readbacks remain required. This is not an accepted checkpoint or final completion snapshot.',
 'actual_checkpoint_commit':None,'actual_checkpoint_receipt':None,
}
mp=D/'MANIFEST.json'
with mp.open('xb') as f:f.write(encoded(manifest))
report=f'# PR140 package-review progress preparation\n\n{utc}; actual preparer PID {pid}. Preparation 100%; case 80%. Read actual bounded priority/package gates and exact frozen former proposal; actual global preimages remain PR134 postimages. Prepared exactly three new private postimages. Prior proposal and all historical MD/log prefixes preserved. Priority complete only in bounded qualified-note scope; fresh package round 1 in progress and upload clearance false. Counts 23/99 and 11 published unchanged. Goal ACTIVE/incomplete. No global/native/Git/API/manuscript/verifier/Zenodo/Sheet/PR write; no intake beyond PR140. Independent checkpoint source/plan review and actual transaction/readbacks remain required.\n'
(D/'REPORT.md').write_text(report)
print(json.dumps({'manifest':pin(mp)[1],'members':members,'UTC':utc,'PID':pid},sort_keys=True))
