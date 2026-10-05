"""Prepare an exact partial research checkpoint; no shared map or Git writes."""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json,os,stat
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';W=Path(__file__).resolve().parent;A=W.parent
utc=lambda:datetime.now(timezone.utc).isoformat()
def need(v,m):
    if not v:raise RuntimeError(m)
def pin(p):
    p=Path(p);need(p.is_file() and not p.is_symlink(),'literal file');b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
def load(p):return json.loads(Path(p).read_bytes())
def encoded(x):return (json.dumps(x,indent=2)+'\n').encode()
def main():
    need(not (W/'CONTENT_PLAN.json').exists(),'fresh preparation')
    stamp=utc();targets=[];payload=W/'payloads';payload.mkdir(exist_ok=False)
    def prepared(target,name,body):
        f=payload/name;f.write_bytes(body);f.chmod(0o644)
        targets.append(dict(target=str(target.relative_to(R)),input=pin(f),original_target=pin(target) if target.exists() else None))
    proof=pin(A/'CURRENT_CORRECTED_PROOF.md')
    status=load(A/'CURRENT_AUDIT_STATUS.json')
    status.update(UTC=stamp,mathematical_review_percent=85,workflow_percent=15,
                  claim_under_review='Terminating theoretical complete-invariant algorithm, with explicit zero-algebra extension; no efficiency or full implementation claim.',
                  strongest_verified_result='Immutable original intake authenticated; original controls reproduced in two runtimes; three independent mathematical families and ROOT replays support construction, effectivity and the numerical key. Exact two-family puncture counterexample requires an additive classification proof repair.',
                  independent_families={'surface_construction_adversary_01':'closed scoped PASS; independent puncture counterexample cross-check PASS',
                    'effectivity_termination_adversary_01':'closed scoped PASS with maximal-portion and seam clarification',
                    'classification_invariant_adversary_01':'closed conditional PASS; mandatory all-end LP sufficiency repair',
                    'corrected_math_adversary_02':'active fresh adversarial review of current corrected proof'},
                  current_corrected_proof=proof,mathematical_acceptance=False,priority_acceptance=False,
                  exact_remaining_gap='Fresh corrected whole mathematical proof adversary and ROOT adjudication; then deep priority, preprint, sequential fresh package reviews, Zenodo, one tracker row, original-head integration and final acceptance.')
    prepared(A/'CURRENT_AUDIT_STATUS.json','CURRENT_AUDIT_STATUS.json',encoded(status))
    inventory=load(P/'inventory.json');before=copy.deepcopy(inventory);items=[x for x in inventory['items'] if x['number']==301];need(len(items)==1,'one exact PR301 inventory entry')
    items[0].update(original_submitted_status='claimed_solved',original_author_budget='1/5',
                    disposition='mathematical_audit_additive_proof_correction_under_fresh_review',
                    mathematical_review_percent=85,priority_percent=0,workflow_percent=15,
                    audit='audits/pr301_30004365',mathematical_acceptance=False,merged=False)
    need([x for x in before['items'] if x['number']!=301]==[x for x in inventory['items'] if x['number']!=301],'all foreign inventory entries literal preservation')
    need({k:v for k,v in before.items() if k!='items'}=={k:v for k,v in inventory.items() if k!='items'},'no completion/publication count change')
    prepared(P/'inventory.json','inventory.json',encoded(inventory))
    scope=load(P/'CURRENT_SCOPE.json')
    scope.update(utc=stamp,scope='Process only submitted QUEUE.md status exactly claimed_solved; skip all others entirely and PR8; descending current301.',
                 current_eligible_pr=301,current_original_head='125d90fa3f5a4f90b813fec7a7c0f1918914d885',current_original_status='claimed_solved',
                 current_original_author_budget='1/5',next_descending_filter_pending=False,next_candidate_status_not_yet_authenticated=False,
                 mathematical_verification_percent=85,priority_percent=0,workflow_percent=15,publication_complete=False,
                 DOI=None,tracker_range=None,actual_merge=None,native_merge_pending=False,
                 last_completed_actual_merge='6d59e1d29b34ea6c18ccb70f25dd4335c8a7594f',last_completed_DOI='10.5281/zenodo.23157237',
                 last_completed_tracker_range="'Math Puzzles'!A26:D26",last_completed_checkpoint='c5bbb350b24a4a612b1dc64e30f51100c4de2eb0',
                 current_mathematical_acceptance=False,current_priority_acceptance=False)
    prepared(P/'CURRENT_SCOPE.json','CURRENT_SCOPE.json',encoded(scope))
    note=(f'\n{stamp} — PR301 partial research checkpoint. Exact original head125d90fa3f5a4f90b813fec7a7c0f1918914d885 original QUEUE status claimed_solved1/5 authenticated; PR302 remains fully completed at c5bbb350b24a4a612b1dc64e30f51100c4de2eb0, DOI10.5281/zenodo.23157237, exactly one A26:D26 tracker row. Three fresh independent mathematical families support construction, effective search and complete numerical key; two families independently verify A(3,5)/A(4,4), exposing the false printed puncture-truncated classification range. Corrected proof uses LP1.2.4 on every compact-core boundary followed by APS6.1, clarifies maximal crosscuts/canonical seams and returns empty multiset for zero input. Fresh whole corrected-math adversary02 is active; no mathematical or priority acceptance yet. ROOT reproduced all three fresh finite controls (surface25inputs/47completions, effectivity239 assertions, classification457019 assertions plus983040 separately counted orbit edges) and both original controls in two runtimes; these are supplementary, not full implementation or empirical proof of halting. Full22 native intake captures and seven ROOT replays independently authenticated. Original snapshots and historical claims/failures preserved. Best-guess mathematical discovery85%, priority0%, workflow15%; overall goal active, eligible total unknown. No PR301 paper/upload/tracker/native merge or external individual communication.\n')
    for f,name in [(A/'RESEARCH_LOG.md','AUDIT_RESEARCH_LOG.md'),(P/'RESEARCH_LOG.md','GLOBAL_RESEARCH_LOG.md')]:prepared(f,name,f.read_bytes()+note.encode())
    selected=[A/n for n in ['CURRENT_CORRECTED_PROOF.md','ROOT_SOURCE_AND_PROOF_OBLIGATIONS.md','snapshot_manifest.json',
       'ROOT_ORIGINAL_FINITE_CONTROLS_REPRODUCTION.json','ROOT_FAMILY_CONTROLS_REPRODUCTION.json','ROOT_FULL_ORIGINAL_AND_REPRODUCTION_CUSTODY.json',
       'root_authenticate_reproduction.py','root_reproduce_family_controls.py','root_reproduce_original_controls.py','snapshot_original.py','root_fetch_primary_sources.py']]
    original=load(A/'snapshot_manifest.json')
    selected += [Path(x['snapshot']['path']) for x in original['files'] if x['path']!='unsolved_math_prioritization/QUEUE.md']
    for family,names in [
      ('surface_construction_adversary_01',['REPORT.md','CHECKABLE_DERIVATIONS.md','surface_fixture_audit.py','surface_fixture_results.json','RESEARCH_LOG.md']),
      ('effectivity_termination_adversary_01',['EFFECTIVITY_AUDIT.md','INDEPENDENT_DERIVATION.md','exact_edge_controls.py','EXACT_EDGE_CONTROLS.json','RESEARCH_LOG.md']),
      ('classification_invariant_adversary_01',['AUDIT_REPORT.md','INDEPENDENT_CLASSIFICATION_THEOREM.md','PRINTED_RANGE_COUNTEREXAMPLE.md','CLASSIFICATION_ADDENDUM.md','check_classification.py','CONTROL_RESULTS.json','FINAL_MANIFEST.json','RESEARCH_LOG.md']),
      ('surface_construction_adversary_01/cross_family_puncture_range_01',['REPORT.md','RESULTS.json','RESEARCH_LOG.md','FROZEN_PRESERVATION.json','verify_witness.py','verify_frozen.py'])]:
        selected += [A/family/n for n in names]
    selected += [P/'status_filter_after_pr302_20261005.py',P/'status_filter_after_pr302_20261005_v02.py',
                 P/'status_filter_after_pr302_20261005/PRESERVED_FAILURE.json',P/'status_filter_after_pr302_20261005_v02/RESULT.json']
    old=A.parent/'pr302_30003508'
    selected += [old/'ROOT_ACTUAL_COMPLETION_CHECKPOINT038_ACCEPTANCE.json',P/'checkpoint_302_final_038_receipt.json']
    selected += [old/'final_checkpoint038_adversary_01'/n for n in ['REPORT.md','DERIVATION.md','READ_SCOPE_LEDGER.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json']]
    selected += [Path(__file__),W/'root_checkpoint039.py']
    for f in sorted(set(selected)):
        need(f.is_relative_to(P),'descending namespace only');targets.append(dict(target=str(f.relative_to(R)),input=pin(f),original_target=pin(f)))
    base=load(old/'final_checkpoint_038_preparation/KNOWN_HELD_BASELINE.json')
    need(len(base['files'])==41253,'full prior held path baseline')
    held=W/'KNOWN_HELD_BASELINE.json';held.write_bytes(encoded(dict(status='CURRENT_FULL_PRIOR_HELD_PATH_BASELINE',UTC=stamp,
                   inventory_scope='All41253 prior checkpoint-held paths; new active scientific namespaces not included and never written by operator.',
                   prior=pin(old/'final_checkpoint_038_preparation/KNOWN_HELD_BASELINE.json'),files=[pin(x['path']) for x in base['files']])));held.chmod(0o444)
    frame=P/'audits/pr305_5100034/root_during_peer_pause_20261005/native_integration_preparation/integrate_pr305.py'
    roles=[frame,A/'ROOT_FULL_ORIGINAL_AND_REPRODUCTION_CUSTODY.json',A/'ROOT_FAMILY_CONTROLS_REPRODUCTION.json',A/'snapshot_manifest.json',old/'ROOT_ACTUAL_COMPLETION_CHECKPOINT038_ACCEPTANCE.json',held]
    source=W/'root_checkpoint039.py';source.chmod(0o444);Path(__file__).chmod(0o444)
    for x in targets:
        if x['input']['path'] in [str(source),str(Path(__file__))]:x['input']=pin(x['input']['path']);x['original_target']=x['input']
    need(len(targets)==len({x['target'] for x in targets}),'exact unique selected paths')
    plan=W/'CONTENT_PLAN.json';allowed=sorted([x['target'] for x in targets]+[str(plan.relative_to(R))])
    value=dict(status='PREPARED_PR301_PARTIAL_RESEARCH_CHECKPOINT039_NO_AUTHORITY',UTC=stamp,actual_preparer_PID=os.getpid(),
      starting_main='c5bbb350b24a4a612b1dc64e30f51100c4de2eb0',endpoint='https://github.com/AlecKriebel/Math.git',
      source=pin(source),bound_inputs=[pin(x) for x in roles],targets=targets,allowed_paths=allowed,
      scope='Publish exact partial mathematical evidence, five progress maps and prior verified PR302 completion controls. No QUEUE, original-head merge, paper, Zenodo, tracker or GitHub write.',
      raw_source_body_and_execution_policy='Primary PDFs and complete raw native captures remain local; published manifests bind their exact bodies. Original full QUEUE snapshot remains local. No assertion of portable full enumeration software.',
      no_mathematical_or_priority_acceptance=True,no_completion_or_publication_count_increment=True,
      corrected_math_fresh_review_still_pending=True,review_clearance_and_postcommit_receipts_outside_plan=True)
    plan.write_bytes(encoded(value));plan.chmod(0o444)
    print(json.dumps(dict(status=value['status'],plan=pin(plan),source=pin(source),targets=len(targets),allowed=len(allowed)),indent=2))
if __name__=='__main__':main()
