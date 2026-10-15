"""Seal only this review's own artifacts; no shared or service mutation."""
from pathlib import Path
import datetime, hashlib, json, os
D=Path(__file__).resolve().parent
A=D.parent
def sha(b): return hashlib.sha256(b).hexdigest()
def require(ok,label):
    if not ok: raise ValueError(label)
def dump(p,obj): p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
receipt=json.loads((D/'READONLY_AUTHENTICATION_AND_GUARD_MODELS.json').read_text())
for name,pin in receipt['exact_reviewed_inputs'].items():
    p=Path(pin['path']); b=p.read_bytes()
    require(not p.is_symlink() and len(b)==pin['bytes'] and sha(b)==pin['sha256'],'Reviewed input changed: '+name)
require(not (A/'actual_closure_20261006').exists(),'Closure began before final review seal')
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
PID=os.getpid()
result={'schema':'pr126-independent-final-closure-only-protocol-review/v1','UTC':UTC,'actual_recorder_PID':PID,
 'verdict':'PASS_FINAL_EXACT_CLOSURE_ONLY_PLAN_AND_OPERATOR_WITH_SEPARATE_AUTHENTIC_FRESH_GRANT_REQUIRED',
 'mandatory_corrections_remaining':[],
 'resolved_finding':'Implicit GitHub service host and absent exact-URL guard corrected before final review',
 'exact_reviewed_inputs':receipt['exact_reviewed_inputs'],
 'read_only_authentication_receipt_sha256':sha((D/'READONLY_AUTHENTICATION_AND_GUARD_MODELS.json').read_bytes()),
 'audit_sha256':sha((D/'AUDIT.md').read_bytes()),
 'all44_science_members_match':True,'all16_original_members_match':True,'all10_complete_physical_pins_match':True,
 'same_head_open_draft_unmerged_observed':True,'existing_marker_count':receipt['existing_exact_marker_comment_count'],
 'independent_guard_models_not_operator_execution':True,'operator_executed':False,'grant_conferred':False,
 'actual_closure_certified':False,'native_completion_certified':False,'service_or_shared_mutation_performed':False,
 'unavoidable_nonatomic_head_race_limit_explicit':True,'ambiguous_outcome_requires_read_only_inspection_before_recovery':True,
 'no_blind_retry_or_expired_grant_reuse':True,'completion_estimate_percent':100,'original_effort':'1/5','new_central_proof_search_turns':0}
dump(D/'RESULT.json',result)
(D/'RESEARCH_LOG.md').write_text('# PR126 closure-protocol adversary research log\n\n'+
 '2026-10-06T22:14:22.943545+00:00: initial read-only independent full-pin observation (PID29927) matched all ten protected physical files. Review completion50%; original effort1/5; new proof-search turns0.\n\n'+
 'Initial operator4bc455… and plan7bd4b8… left hostname implicit and exact URL unguarded. Reported to root before operations; root corrected both. Independent diagnostic AST enumeration then required a source-order repair before it could assess the two nested mutation call sites; diagnostic failed before subprocess calls and was corrected. No closure operator executed. Review completion75%; proof-search turns0.\n\n'+
 '2026-10-06T22:16:00.272612+00:00: actual independent read-only PID31072 authenticated final operator94bd06…/plan09f981…, all44 scientific members, all16 submitted bodies, all ten physical pins, local/primary/remote heads, exact github.com PR126 and absence of a marker/operation folder. Independent host/head/time negative controls passed. Review completion90%; proof-search turns0.\n\n'+
 UTC+': final recorder PID'+str(PID)+' seals PASS for those exact final inputs. One reported binding defect was repaired; no mandatory correction remains. Authentic fresh peer authority is still required, and native/main completion remains separate. Review completion100%; original effort1/5; central proof-search turns0. No service or shared write.\n')
members={}
for p in sorted(D.rglob('*')):
    if p.is_file() and p.name!='FINAL_MANIFEST.json':
        require(not p.is_symlink(),'Own artifact redirected')
        b=p.read_bytes(); members[str(p.relative_to(D))]={'bytes':len(b),'sha256':sha(b)}
dump(D/'FINAL_MANIFEST.json',{'schema':'pr126-closure-only-protocol-review-final-seal/v1','UTC':UTC,
 'actual_recorder_PID':PID,'verdict':result['verdict'],'exact_reviewed_inputs':result['exact_reviewed_inputs'],
 'public_artifacts':members,'result_sha256':sha((D/'RESULT.json').read_bytes()),'manifest_self_included':False,
 'no_service_or_shared_mutation':True,'operator_executed':False,'grant_conferred':False,'original_effort':'1/5',
 'new_central_proof_search_turns':0,'completion_estimate_percent':100})
print(json.dumps({'UTC':UTC,'actual_recorder_PID':PID,'verdict':result['verdict'],'manifest_sha256':sha((D/'FINAL_MANIFEST.json').read_bytes()),'result_sha256':sha((D/'RESULT.json').read_bytes()),'audit_sha256':sha((D/'AUDIT.md').read_bytes()),'members':len(members)},sort_keys=True))
