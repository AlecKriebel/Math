"""Prepare a literal checkpoint candidate from actually accepted PR302 results.

No Git, service, shared-control or existing-global-map mutation. Full private
streams, primary-source bodies and known-held baseline remain local; published
reports/manifests identify that scope explicitly.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,copy,hashlib,json,os,stat,sys
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';W=Path(__file__).parent;A=W.parent;N=A/'native_integration_preparation';REC=A/'checkpoint037_push_recovery_preparation'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(Path(p).read_bytes())
def need(v,m):
 if not v:raise RuntimeError(m)
def pin(p):
 p=Path(p);need(p.is_file() and not p.is_symlink(),'literal complete file');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def emit(p,b,mode=0o444):
 with p.open('xb') as f:f.write(b)
 p.chmod(mode);return pin(p)
def encoded(v):return (json.dumps(v,indent=2)+'\n').encode()
def main():
 need(not sys.flags.optimize,'no optimization');need(not (W/'CONTENT_PLAN.json').exists(),'concrete plan already exists')
 native=load(N/'ROOT_ACTUAL_NATIVE_MERGE_VERIFICATION.json');accepted=load(A/'ROOT_ACTUAL_NATIVE_INTEGRATION_ACCEPTANCE.json')
 need(native['status']=='PASS_PR302_EXACT_ORIGINAL_HEAD_NATIVE_MERGE_AND_PRESENT_DAY_ACCEPTANCE' and accepted['status']=='ROOT_ACCEPTS_ACTUAL_PR302_ORIGINAL_HEAD_NATIVE_INTEGRATION' and native['actual_merge']==accepted['actual_merge'] and accepted['actual_native_exit_code']==0,'genuine independently accepted native result')
 stamp=utc();base=accepted['actual_merge'];source=W/'root_checkpoint038.py';ast.parse(source.read_bytes());need(pin(source)['sha256']=='22192198e052c93af6dfb884f07e3381ea7babd67d496433e6d4e1290878b2e6','reviewed final source');source.chmod(0o444)
 payload=W/'payloads';payload.mkdir(exist_ok=False);maps=[]
 def prepared(target,name,b):
  p=payload/name;emit(p,b,0o644);maps.append(dict(target=str(target.relative_to(R)),input=pin(p),original_target=pin(target)))
 inventory=load(P/'inventory.json');before=copy.deepcopy(inventory);items=[x for x in inventory['items'] if x['number']==302];need(len(items)==1,'one exact inventory target');item=items[0]
 need(item['original_submitted_status']=='claimed_solved' and item['headRefOid']==native['original_head'] and item['workflow_percent']==85,'original eligibility/current pending entry')
 item.update(disposition='verified_preprint_published_tracker_complete_native_merge_verified',workflow_percent=100,audit_workflow_percent=100,merged=True,actual_merge=base,merged_at=accepted['merged_at'],native_integration_acceptance='audits/pr302_30003508/ROOT_ACTUAL_NATIVE_INTEGRATION_ACCEPTANCE.json',completion_checkpoint_plan='audits/pr302_30003508/final_checkpoint_038_preparation/CONTENT_PLAN.json',checkpoint_release_verification_required=True)
 need(302 not in inventory['claimed_solved_merged_by_descending'],'no duplicated completion');inventory['claimed_solved_merged_by_descending'].append(302);inventory['completed_by_descending']+=1
 need([x for x in inventory['items'] if x['number']!=302]==[x for x in before['items'] if x['number']!=302] and inventory['claimed_solved_published_by_descending']==before['claimed_solved_published_by_descending'],'all foreign inventory facts unchanged')
 prepared(P/'inventory.json','inventory.json',encoded(inventory))
 scope=load(P/'CURRENT_SCOPE.json');scope.update(utc=stamp,current_eligible_pr=None,current_original_head=None,current_original_status=None,last_completed_pr=302,last_completed_disposition='merged_claimed_solved_published_zenodo_tracker_verified',next_descending_filter_pending=True,next_descending_candidate=301,next_candidate_status_not_yet_authenticated=True,workflow_percent=100,native_merge_pending=False,actual_merge=base,checkpoint_release_verification_required=True)
 prepared(P/'CURRENT_SCOPE.json','CURRENT_SCOPE.json',encoded(scope))
 status=load(A/'CURRENT_AUDIT_STATUS.json');status.update(UTC=stamp,workflow_percent=100,merged=True,actual_merge=base,merged_at=accepted['merged_at'],native_integration_acceptance='ROOT_ACTUAL_NATIVE_INTEGRATION_ACCEPTANCE.json',remaining_gap='No unresolved mathematical, bounded-priority, preprint, publication, tracker or native-integration issue within the stated smooth stationary conormal model. The bounded priority edition/access limitations remain disclosed; worldwide firstness is not certified. Final checkpoint release is verified separately by its actual postpush receipt.',checkpoint_release_verification_required=True)
 prepared(A/'CURRENT_AUDIT_STATUS.json','CURRENT_AUDIT_STATUS.json',encoded(status))
 entry=(f'\n{stamp} — PR302 final acceptance checkpoint candidate. Original head {native["original_head"]} was actually merged as second parent of {base}; ROOT independently authenticated all516 genuine native captures, all34 live/index/committed full bodies/modes/blobs, the unchanged original28 contribution files, four target QUEUE cells and one present-day state/history event preserving author2/5. GitHub confirms that exact merge; main equals the explicit remote. DOI10.5281/zenodo.23157237 and the single A26:D26 tracker row were already independently accepted and were not repeated. Checkpoint037 originally exited1 before push; the separately reviewed push-only recovery succeeded without reclassifying that failure. Native review closed with161 boundary cases; the completion checkpoint source was repaired to recheck every owned live/index/commit body/mode/blob after push. Mathematical discovery100%,bounded priority100%,preprint/publication/tracker/native100%; completion records workflow100% subject to the separately recorded actual checkpoint release readback. Overall descending goal remains active with unknown remaining eligible total; next candidate301 requires original-status authentication, and every non-claimed_solved status and PR8 must be skipped without processing. Unrefereed extensive AI assistance and bounded priority access limits remain disclosed.\n')
 for target,name in [(P/'RESEARCH_LOG.md','GLOBAL_RESEARCH_LOG.md'),(A/'RESEARCH_LOG.md','AUDIT_RESEARCH_LOG.md')]:prepared(target,name,target.read_bytes()+entry.encode())
 text=(A/'README.md').read_text();text=text.replace('Native original-head integration is pending a fresh independent operational review.',f'GitHub confirms native original-head merge {base}, with the original head as second parent and all28 original attempt files preserved. ROOT authenticated the complete successful native execution and exact34-file live/index/commit acceptance scope.');text=text.replace('Math/priority/preprint/publication100%; total PR302 workflow85%, pending native merge and final acceptance.','Math/bounded priority/preprint/publication/tracker/native integration100%; PR302 completion records workflow100%, subject to the final checkpoint\'s separately recorded postpush release verification. The overall descending goal remains active.')
 text+='\nCheckpoint037\'s original postcommit mode-check failure and separate successful push-only recovery remain distinguished. The final checkpoint corrects that mode check and rechecks every owned full body/mode/blob after push. Full private tracker/native streams, third-party primary sources and large held-state baselines remain local; published manifests bind their exact full bodies without implying redistribution. Fresh final-checkpoint review controls and postcommit receipts remain outside this noncircular plan and will be checkpointed separately.\n'
 prepared(A/'README.md','README.md',text.encode())
 baseline=load(N/'KNOWN_HELD_BASELINE.json');rows=baseline['files'];need(len(rows)==len({x['path'] for x in rows})==41253,'full held path inventory');current=[pin(x['path']) for x in rows]
 held=W/'KNOWN_HELD_BASELINE.json';emit(held,encoded(dict(status='CURRENT_COMPLETE_KNOWN_HELD_BASELINE_FOR_CHECKPOINT038',UTC=stamp,actual_preparer_PID=os.getpid(),original_path_inventory=pin(N/'KNOWN_HELD_BASELINE.json'),files=current,complete_file_count=len(current),mode_representation='integer POSIX permissions',foreign_scope_preserved=True)))
 frame=P/'audits/pr305_5100034/root_during_peer_pause_20261005/native_integration_preparation/integrate_pr305.py'
 roles=[frame,N/'ROOT_ACTUAL_NATIVE_MERGE_VERIFICATION.json',A/'ROOT_ACTUAL_NATIVE_INTEGRATION_ACCEPTANCE.json',REC/'ROOT_ACTUAL_RECOVERY_ACCEPTANCE.json',A/'ROOT_ACTUAL_PUBLICATION_AND_TRACKER_ACCEPTANCE.json',held]
 selected=[source,Path(__file__),*roles[1:5],A/'ROOT_CHECKPOINT037_FAILED_BOUNDARY.json',P/'checkpoint_302_publication_037_recovery_receipt.json']
 selected += [p for p in N.iterdir() if p.is_file() and p.suffix in ['.py','.json'] and p.name!='KNOWN_HELD_BASELINE.json']
 for namespace in [A/'native_integration_adversary_01',A/'checkpoint037_push_recovery_adversary_02']:
  selected += [namespace/n for n in ['REPORT.md','DERIVATION.md','READ_SCOPE_LEDGER.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json']]
 selected += [p for p in REC.iterdir() if p.is_file() and p.suffix=='.py']
 targets=[]
 for p in sorted(set(selected)):
  need(p.is_relative_to(P) and p.is_file(),'literal published report/source selection');targets.append(dict(target=str(p.relative_to(R)),input=pin(p),original_target=pin(p)))
 targets+=maps;need(len(targets)==len({x['target'] for x in targets}),'unique exact targets')
 planpath=W/'CONTENT_PLAN.json';allowed=sorted([x['target'] for x in targets]+[str(planpath.relative_to(R))]);plan=dict(status='PREPARED_EXACT_PR302_VERIFIED_COMPLETION_CHECKPOINT038_NOT_AUTHORIZED',UTC=stamp,actual_preparer_PID=os.getpid(),starting_main=base,endpoint='https://github.com/AlecKriebel/Math.git',source=pin(source),bound_inputs=[pin(p) for p in roles],targets=targets,allowed_paths=allowed,scope='Literal accepted-results reports and six prepared global maps only; no native PR/QUEUE/service action',noncircular_review_policy='Fresh final checkpoint review controls, ROOT clearance, actual captures and final receipt are outside this plan',local_only_evidence_policy='Full primary-source and private tracker/native capture bodies and held baseline remain local; selected reports/manifests bind those bodies',all_foreign_inventory_items_unchanged=True,only_target_completed_count_increment=1,preexisting_published_list_unchanged=True,no_write_authority=True,estimates_percent=dict(PR302_discovery=100,bounded_priority=100,PR302_workflow=95,final_checkpoint_preparation=100))
 emit(planpath,encoded(plan));print(json.dumps(dict(status=plan['status'],actual_preparer_PID=os.getpid(),source=pin(source),plan=pin(planpath),selected_targets=len(targets),allowed_paths=len(allowed),bound_inputs=len(roles),starting_main=base),indent=2))
if __name__=='__main__':main()
