"""Terminal read-only input recheck and acyclic review output seal."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p,rel):return {'path':str(rel),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(n,o):(D/n).write_text(json.dumps(o,indent=2)+'\n')
need(not (D/'SEAL.json').exists(),'Already sealed; do not overwrite')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();frozen=read(D/'FROZEN_INPUTS.json');A=Path(frozen['root']);checked=[]
for r in frozen['rows']:
    p=A/r['path'];need(p.is_file() and not p.is_symlink() and p.stat().st_size==r['size'] and sha(p)==r['sha256'],'Preexisting drift '+r['path'])
    checked.append({'path':r['path'],'bytes':r['size'],'sha256':r['sha256'],'unchanged':True})
need(not (D/'scratch').exists(),'Scratch cleanup incomplete')
early=read(D/'EARLY_DERIVATION_PIN.json');need(sha(D/'INDEPENDENT_DERIVATION.md')==early['sha256'],'Early derivation changed')
need(read(D/'INDEPENDENT_CHECKS_NORMAL.json')==read(D/'INDEPENDENT_CHECKS_OPTIMIZED.json'),'Independent normal/-O mismatch')
need(read(D/'VERDICT.json')['finding_counts']=={'P0':0,'P1':0,'P2':0,'P3':1},'Finding count changed')
save('FINAL_INPUT_RECHECK.json',{'utc':now,'status':'PASS','all_preexisting_inputs_unchanged':True,'rows':checked})
external=[read(D/'SOURCE_READ_LEDGER.json')['native_code_read'],read(A/'NEWpreprint_v1_0/FROZEN_INPUTS.json')['workspace_AGENTS']]
for r in external:
    p=Path(r['path']);need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'External input drift')
save('EXTERNAL_INPUT_PINS.json',{'scope':'Additional local input identities outside the audit freeze; source browser URLs/read scopes are separately recorded.','records':external})
rows=[pin(p,p.relative_to(D)) for p in sorted(D.rglob('*')) if p.is_file() and not p.is_symlink() and p not in {D/'OUTPUT_PINS.json',D/'SEAL.json'}]
save('OUTPUT_PINS.json',{'utc':now,'scope':'All settled review regular files except this self-excluded inventory and its separate seal. Includes every authored driver, report, ledger, complete receipt and preserved computed3.11 result. Disposable derivatives are removed only after individual SCRATCH_FINAL_PINS.','records':rows})
save('SEAL.json',{'utc':now,'status':'NEW_COMPLETE_WHOLE03_ONE_ACTIONABLE_P3_PENDING_ROOT_ADOPTION_BOUNDED_REPAIR_AND_NEW_COMPLETE_WHOLE04','output_pins':pin(D/'OUTPUT_PINS.json','OUTPUT_PINS.json'),'output_records':len(rows),'input_freeze':pin(D/'FROZEN_INPUTS.json','FROZEN_INPUTS.json'),'frozen_preexisting_inputs':len(checked),'all_preexisting_unchanged':True,'independent_early_derivation_sha256':early['sha256'],'finding_counts':{'P0':0,'P1':0,'P2':0,'P3':1},'finding':'WHOLE03-P3-01','delegated_review_execution_percent':100,'next_required_new_complete_whole_review':4,'root_finding_adoption_required':True,'root_terminal_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'all_writes_settled':True,'scratch_removed_after_exact_pins':True,'no_candidate_or_prior_artifact_mutation':True,'no_outreach_services_git_mutation_or_new_agent':True,'meaning':'Full review execution completion is distinct from readiness, mathematical formal certification, novelty and priority clearance.'})
for r in rows:need(pin(D/r['path'],r['path'])==r,'Post-seal output drift '+r['path'])
need(sha(D/'OUTPUT_PINS.json')==read(D/'SEAL.json')['output_pins']['sha256'],'Separate seal mismatch')
print(json.dumps({'status':'SEALED','outputs':len(rows),'frozen_inputs':len(checked),'finding_counts':read(D/'VERDICT.json')['finding_counts'],'output_pins_sha256':sha(D/'OUTPUT_PINS.json'),'seal_sha256':sha(D/'SEAL.json'),'all_writes_settled':True},indent=2))
