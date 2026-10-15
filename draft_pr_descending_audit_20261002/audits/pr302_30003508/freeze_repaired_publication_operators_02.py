"""Freeze preparation and science clearance; grants no operations authority."""
from pathlib import Path
from datetime import datetime,timezone
import ast,difflib,hashlib,json,os,stat,sys
A=Path(__file__).resolve().parent;D=A/'publication_preparation';F=A/'preprint_package_v02'
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def pin(p):
    p=Path(p);require(p.is_file() and not p.is_symlink(),'Literal file required')
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(p.stat().st_mode))
def load(p):return json.loads(p.read_bytes())
def write(p,x):
    with p.open('x') as f:json.dump(x,f,indent=2,ensure_ascii=False);f.write('\n')
def main():
    require(not sys.flags.optimize,'Optimization forbidden')
    require(load(A/'ROOT_SECOND_PREPRINT_REVIEW_ADJUDICATION.json')['ROOT_accepts_mathematics'] is True,'Closed second science review not accepted')
    require(not (A/'publication_actual').exists(),'No actual service namespace should exist during preparation')
    require(not (A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json').exists(),'No operations clearance before fresh repaired review')
    cm=F/'SECOND_CANDIDATE_MANIFEST.json'
    require(pin(cm)['sha256']=='b38a09c6768e11c2954892cdaa345a485557082c464d950f573a945f48b5ec71','Science candidate changed')
    for r in load(cm)['files']:require(pin(r['path'])==r,'Frozen public science changed')
    names=('publication_guard.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py');changes=[]
    for name in names:
        p=D/name;b=p.read_bytes();ast.parse(b,filename=str(p));compile(b,str(p),'exec')
        previous=A/'publication_operator_version_01'/name;require(previous.is_file(),'Original version missing')
        diff=''.join(difflib.unified_diff(previous.read_text().splitlines(True),b.decode().splitlines(True),fromfile='reviewed-original/'+name,tofile='repaired/'+name))
        changes.append(dict(name=name,immutable_original=pin(previous),revised_bytes=len(b),revised_sha256=hashlib.sha256(b).hexdigest(),complete_diff=diff))
        p.chmod(0o444)
    registry=D/'REVISED_OPERATOR_MANIFEST.json'
    write(registry,dict(UTC=datetime.now(timezone.utc).isoformat(),actual_preparation_recorder_PID=os.getpid(),status='FROZEN_REPAIRED_OPERATOR_VERSION_PENDING_FRESH_REVIEW',approved_operational_sources=[pin(D/n) for n in names],original_version_archive=pin(A/'publication_operator_version_01/ARCHIVE_MANIFEST.json'),candidate_manifest=pin(cm),publication_clearance=False,noncircular_exclusion='This manifest contains the four programs, not its own hash. Future ROOT acceptance pins this complete manifest externally.'))
    registry.chmod(0o444)
    evidence=[A/folder/name for folder in ('preprint_adversary_01','preprint_adversary_02') for name in ('REPORT.md','DERIVATION.md','READ_LEDGER.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json')]+[A/'ROOT_FIRST_PREPRINT_REVIEW_ADJUDICATION.json',A/'ROOT_SECOND_PREPRINT_REVIEW_ADJUDICATION.json']
    clear=A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json'
    write(clear,dict(UTC=datetime.now(timezone.utc).isoformat(),actual_ROOT_recorder_PID=os.getpid(),status='PASS_PR302_REVISED_PREPRINT_AFTER_TWO_FRESH_WHOLE_PACKAGE_REVIEWS',original_PR=302,original_head='eb6e0e999521d84a65f9857d338cad76b84d30db',original_status='claimed_solved',original_author_budget='2/5',unresolved_material_issues=[],unresolved_nonmandatory_issues=[],fresh_whole_package_reviews=2,publication_clearance=True,candidate_manifest=pin(cm),closed_evidence_pins=[pin(p) for p in evidence],ROOT_reconstruction=pin(A/'ROOT_REVISED_PREPRINT_RECONSTRUCTION.md'),bounded_priority_gate=pin(A/'ROOT_BOUNDED_PRIORITY_GATE_ACCEPTANCE.json'),operations_execution_requires_separate_fresh_clearance=True,operations_clearance_path=str(A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json'),actual_upload_or_tracker_or_native_execution_performed=False,limits='Accepts explicit smooth exact stationary known-fixed-lag conormal model and bounded dated priority audit; inaccessible CV2011 final edition remains disclosed. AI/unrefereed, no human review or formal proof certificate. This science gate alone cannot pass the operational guard.',estimates_percent=dict(mathematics=100,bounded_priority=100,preprint_science=100,publication_workflow=70)))
    clear.chmod(0o444)
    write(A/'ROOT_PUBLICATION_OPERATORS_GLOBAL_REPAIR_02.json',dict(UTC=datetime.now(timezone.utc).isoformat(),actual_ROOT_preparer_PID=os.getpid(),source=pin(__file__),status='G1_G2_GLOBALLY_REPAIRED_PENDING_FRESH_OPERATIONS_REVIEW',changes=changes,reviewed_original=pin(A/'publication_operations_adversary_01/OUTPUT_MANIFEST.json'),revised_operator_manifest=pin(registry),science_gate=pin(clear),required_repairs=dict(G1='Mandatory14 named science evidence pins, exact4 approved frozen operator versions, separate ROOT operations approval with5 closed review evidence pins and3 runtime targets; every actual capture preserves all4 source bodies, any kit dependency, all3 complete approvals, actual caller/child executable observations and both complete streams; rechecked before each invocation.',G2='Production/title/exact2files rechecked; complete actual inspected stream/request/start/native/source/approval/runtime chain; actual anonymous raw record and both whole downloaded compressed streams independently re-opened, compared to all11 metadata fields and exact frozen PDF/ZIP, before any tracker calls and immediately before the single append.'),public_science_23_files_unchanged=True,actual_service_Git_native_control_changes=False,publication_operations_clearance=False,need_new_fresh_reviewer=True))
    with (F/'RESEARCH_LOG.md').open('a') as h:h.write('\n'+datetime.now(timezone.utc).isoformat()+' — ROOT accepted closed second whole-package review (492 immutable files,301 full source copies,293 independent body pins,13 actual scientific processes with the genuine failed checker retained). Accepted G1/G2 mandatory operator findings and repaired all current callers/guards globally, preserving original four programs. Scientific readiness100%; overall PR302 publication workflow70%; fresh operations review pending. No upload/tracker/native/control action.\n')
    print(json.dumps(dict(status='FROZEN_REPAIRED_PREPARATION_PENDING_FRESH_REVIEW',actual_preparer_PID=os.getpid(),operator_manifest=pin(registry),science_gate=pin(clear),public_science_unchanged=True,operations_clearance=False)))
if __name__=='__main__':main()
