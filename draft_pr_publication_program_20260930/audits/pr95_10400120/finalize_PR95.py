"""Record actual qualified completion after verified source-acceptance push."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent; C=A.parents[2]; P=A.parents[1]
def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
    if not ok: raise RuntimeError(message)
def dump(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def git(*args): return subprocess.check_output(['/usr/bin/git',*args],cwd=C)
ready=load(A/'ROOT_READY_FOR_PUBLICATION.json')
source=load(A/'actual_checkpoints/source_acceptance/RECEIPT.json')
native=load(A/'native_acceptance_20261005/PREPARED_RECEIPT.json')
pub=load(A/'actual_operations/zenodo_publish/stdout.bin')
ins=load(A/'actual_operations/zenodo_published_inspect/stdout.bin')
tracker=load(A/'ROOT_TRACKER_RECORD.json'); download=load(A/'ROOT_PUBLIC_DEPOSIT_VERIFICATION.json')
pr=load(A/'actual_operations/pr95_final_readback/stdout.bin')
require(source['remote_verified'] and source['parent']==native['base_commit'],'source ancestry')
require(git('rev-parse','HEAD').strip().decode()==source['commit'],'current source checkpoint')
require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==source['commit'],'current remote main')
require(pr['state']=='MERGED' and pr['headRefOid']==ready['source_head'] and pr['mergeCommit']['oid']==native['merge_commit'],'merged same source')
require(pr['body']==(A/'PR95_ACCEPTED_BODY.md').read_text(),'final qualified PR body')
subprocess.run(['/usr/bin/git','merge-base','--is-ancestor',native['merge_commit'],source['commit']],cwd=C,check=True)
require(pub['state']==ins['state']=='published' and pub['environment']==ins['environment']=='production','publication state')
require(all(pub[k]==ins[k] for k in ['title','files','metadata_normalizations','id','doi','doi_url','record_url']),'exact publication inspection')
require(pub['metadata_normalizations']==[] and pub['doi_resolution']['status']==ins['doi_resolution']['status']=='resolved','metadata and DOI')
require(download['verified'] and download['all_seven_downloaded_bytes_match_reviewed_payloads'] and download['DOI']==pub['doi'],'public bytes')
require(tracker['unique_verified'] and tracker['DOI']==pub['doi'],'unique tracker')
require(ready['publication_clearance'] and not ready['priority_clearance'] and ready['qualified_publication_user_authorized'],'qualified authority')
require(ready['whole_package_rounds']==2 and not ready['required_repairs'],'review rounds')
for row in ready['upload_pins']:
    f=A/ready['package_relative_path']/'publicfiles'/row['file']
    require(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'frozen public file')
orig=load(A/'original_source_authentication_20261005/ORIGINAL_BLOB_MANIFEST.json')
for row in orig['files']: require(sha(Path(row['preserved_path']))==row['sha256'],'incoming archive')
require(len(orig['files'])==17 and native['native_optimized_runs_passed'],'native gate')
for row in native['native_pins']:
    f=C/row['file']; b=git('show',source['commit']+':'+row['file'])
    require(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'] and len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'committed native pin')
N=C/'unsolved_math_prioritization/attempts/10400120'; accepted=load(N/'ACCEPTANCE.json')
require(accepted['DOI']==pub['doi'] and not accepted['priority_clearance'] and accepted['qualified_publication_user_authorized'],'native qualification')
for line in (N/'SHA256SUMS').read_text().splitlines():
    digest,rel=line.split('  ',1); require(sha(N/rel)==digest,'native digest')
queue=git('show',source['commit']+':unsolved_math_prioritization/QUEUE.md').decode().splitlines()
base=git('show',native['base_commit']+':unsolved_math_prioritization/QUEUE.md').decode().splitlines()
which=lambda ss:[i for i,s in enumerate(ss) if '| 10400120 / AMR-103-0120 |' in s]
require(which(queue)==which(base) and len(which(queue))==1,'unique queue row')
i=which(queue)[0]; require([s for j,s in enumerate(queue) if j!=i]==[s for j,s in enumerate(base) if j!=i],'other queue rows preserved')
cells=queue[i].split('|');require(cells[8].strip()=='claimed_solved' and cells[9].strip()=='2/5' and cells[12].strip()==pub['doi_url'],'queue status budget DOI')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
x={'schema':'pr95-actual-qualified-completion/v1','UTC':now,'actual_operator_PID':os.getpid(),'PR':95,'head':ready['source_head'],'literal_submitted_status':'claimed_solved','original_budget':'2/5','new_central_proof_search_turns':0,'DOI':pub['doi'],'record_url':pub['record_url'],'tracker_range':tracker['range'],'merge_commit':native['merge_commit'],'scientific_acceptance_commit':source['commit'],'source_checkpoint_remote_verified':True,'full_printed_claim_counterexample_verified':True,'whole_package_rounds':2,'mandatory_findings_remaining':[],'priority_clearance':False,'historical_priority_established':False,'qualified_publication_user_authorized':True,'priority_disposition':'Kuriya preprint unobtained; credited; unresolved priority explicitly disclosed; no firstness, current global openness or new historical resolution claim','incoming_bodies_preserved':17,'all_seven_published_downloads_byte_identical':True,'exact_metadata_verified':True,'native_optimized_checks':[7,7,2005],'human_peer_review':False,'workflow_estimate_percent':100,'dated_program_completed':13,'dated_program_total':99,'dated_program_percent':100*13/99,'metadata_checkpoint_push_pending':True,'advance_to_next_status_intake_after_metadata_push':True,'primary_checkout_mutated':False,'primary_synchronization_pending':True,'persistent_goal_complete':False}
dump(A/'ROOT_FINAL_COMPLETION_ACTUAL_RECEIPT_20261005.json',x)
progress=load(P/'CURRENT_PROGRESS.json')
progress.update({'UTC':now,'current_PR_workflow_percent':100,'current_actual_completion_record':'audits/pr95_10400120/ROOT_FINAL_COMPLETION_ACTUAL_RECEIPT_20261005.json','current_native_integration_complete':True,'current_isolated_native_lifecycle_complete':True,'current_merge_commit':native['merge_commit'],'completion_metadata_checkpoint_pending_at_snapshot':True,'advance_to_next_PR_authorized_now':False,'fully_completed_count':13,'fully_completed_eligible_PRs':sorted(set(progress['fully_completed_eligible_PRs']+[95])),'fully_completed_fraction_percent':100*13/99,'workflow_estimate_percent':100*13/99,'published_PRs':sorted(set(progress['published_PRs']+[95])),'last_completed_PR':95,'last_published_PR':95,'last_completed_DOI':pub['doi'],'last_published_DOI':pub['doi'],'last_completed_PR_workflow_percent':100,'last_completed_acceptance_commit':source['commit'],'last_completed_scientific_checkpoint_commit':source['commit'],'last_completed_merge_commit':native['merge_commit'],'last_completed_tracker_range':tracker['range'],'last_completed_actual_final_gate':'audits/pr95_10400120/ROOT_FINAL_COMPLETION_ACTUAL_RECEIPT_20261005.json','last_completed_record':'audits/pr95_10400120/ROOT_FINAL_COMPLETION_ACTUAL_RECEIPT_20261005.json','last_completed_final_completion_readback':None,'last_completed_metadata_checkpoint_commit':None,'last_completed_outcome':'verified_full_SU5_counterexample_published_with_human_authorized_unresolved_priority','last_completed_mathematical_and_package_review_percent':100,'last_completed_priority_audit_percent':85,'last_completed_priority_clearance':False,'last_completed_priority_hold':'Kuriya full text unobtained; explicitly qualified publication authorized','last_completed_full_source_solved':True,'last_completed_publication_authorization':True,'last_completed_scientific_disposition_record':'audits/pr95_10400120/ROOT_READY_FOR_PUBLICATION.json','next_eligible_PR_after_current_completion':None,'next_eligible_order_requires_fresh_status_check':True,'next_numeric_intake_cursor':96,'remaining_current_step':'PR95 qualified scientific workflow complete: published, uniquely tracked, merged and accepted native source pushed. Completion metadata checkpoint pending; next status-only intake follows verified push and coordination release.','workflow_estimate_definition':'Nine published workflows, three credited prior-result dispositions and one verified partial disposition divided by dated 99-PR census.'})
dump(P/'CURRENT_PROGRESS.json',progress)
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n## '+now+' — actual qualified scientific completion\n\nDOI '+pub['doi']+' resolves; seven public files authenticated and exact metadata verified; unique tracker '+tracker['range']+'; unchanged source merged and current native acceptance pushed in main '+source['commit']+'. Two fresh sequential whole-package reviews completed with required repair propagated. Incoming17 bodies, claimed_solved status and2/5 effort preserved; zero new central proof-search turns. Historical priority unresolved, Kuriya credited; human authorized qualified publication. AI use and unrefereed status disclosed. Workflow100%; program13/99 (13.13%); metadata checkpoint and coordination release precede next ordered status intake.\n')
paths=[str((A/n).relative_to(C)) for n in ['ROOT_FINAL_COMPLETION_ACTUAL_RECEIPT_20261005.json','RESEARCH_LOG.md','finalize_PR95.py','SOURCE_ACCEPTANCE_CHECKPOINT_SELECTION.json','PR95_ACCEPTED_BODY.md','actual_checkpoints/source_acceptance/RECEIPT.json','actual_checkpoints/source_acceptance/PROCESS_JOURNAL.json']]+[str((P/'CURRENT_PROGRESS.json').relative_to(C))]
for label in ['checkpoint_source_acceptance','pr95_final_readback']:
    paths.extend(str(p.relative_to(C)) for p in (A/'actual_operations'/label).iterdir() if p.is_file())
dump(A/'COMPLETION_METADATA_SELECTION.json',{'paths':sorted(set(paths))})
print(json.dumps(x))
