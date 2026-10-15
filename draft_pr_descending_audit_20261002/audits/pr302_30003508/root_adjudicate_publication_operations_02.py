"""Whole closed operational custody; approve exact version after ROOT reading."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat,sys
A=Path(__file__).resolve().parent;V=A/'publication_operations_adversary_02';D=A/'publication_preparation';F=A/'preprint_package_v02'
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p);require(p.is_file() and not p.is_symlink(),'Literal file required '+str(p));b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def match(r,mode=True):
    p=Path(r['path']);x=pin(p);require(all(x[k]==r[k] for k in ('bytes','sha256')),'Full body differs '+str(p))
    if mode:require(x['mode']==r['mode'],'Final mode differs '+str(p))
    return p
def time(s):
    x=datetime.fromisoformat(s);require(x.tzinfo is not None,'Missing timezone');return x
def main():
    require(not sys.flags.optimize,'Optimization forbidden')
    m=V/'OUTPUT_MANIFEST.json';s=V/'CLOSURE_SEAL.json'
    require(pin(m)['bytes']==63888 and pin(m)['sha256']=='e9b5e34204ce02047dd91ebb01642970adfb0b2a047c6a238b3661b9602e0aea' and pin(s)['sha256']=='633a4627a5cc32a5edae46e2e5f0070ae3c872bb18900662c611436fd33aa816','External closure anchors differ')
    md=load(m);rows=md['files'];require(len(rows)==133,'Payload count differs')
    for r in rows:match(r)
    files=[p for p in V.rglob('*') if p.is_file()];dirs=[V]+[p for p in V.rglob('*') if p.is_dir()]
    require({str(p) for p in files}=={r['path'] for r in rows}|{str(m),str(s)},'Exact literal closure files differ')
    require(len(files)==135 and len(dirs)==17 and all(not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o444 for p in files) and all(not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o555 for p in dirs),'Closed modes/directories differ')
    require({str(p) for p in dirs}=={r['path'] for r in md['directories']},'Literal closed directory inventory differs')
    physical=sum(p.stat().st_blocks*512 for p in files+dirs);require(physical<20*1024*1024,'Physical archive limit')
    match(load(s)['output_manifest'])
    initial=load(V/'INITIAL_INPUTS.json')
    for r in initial['sources']:
        require(gzip.decompress(match(r['full_body_archive']).read_bytes())==match(r['input']).read_bytes(),'Entire reviewed initial source archive differs')
    for r in initial['candidate_files']+initial['science_evidence_pins']+initial['runtime_targets']:match(r)
    native=[]
    for p in sorted(V.glob('actual_*/execution.json')):
        x=load(p);q=load(p.parent/'request.json');started=load(p.parent/'started.json')
        require(all(x[k]==v for k,v in q.items()),'Actual request/result differs')
        require(started['actual_PID']==x['actual_PID'] and started['start_UTC']==x['start_UTC'],'Actual start differs')
        require(type(x['actual_PID'])==int and type(x['actual_launcher_PID'])==int and x['actual_PID']>0 and x['actual_launcher_PID']>0 and time(x['requested_UTC'])<=time(x['start_UTC'])<=time(x['end_UTC']),'Actual PID/timestamp differs')
        require(x['exit_code']==0 and x['timed_out'] is False and x['automatic_retry'] is False and x['cwd']=='/Users/alec/Documents/Math','Actual outcome/cwd differs')
        for key in ('resolved_executable','resolved_caller_interpreter'):match(x[key])
        for r in x['full_prelaunch_sources']:
            b=gzip.decompress(match(r['full_source_archive']).read_bytes());require(len(b)==r['input']['bytes'] and sha(b)==r['input']['sha256'] and b==match(r['input'],False).read_bytes(),'Actual full prelaunch source differs')
        streams=[]
        for name in ('stdout','stderr'):
            r=x[name];b=gzip.decompress(match(r['stored'],False).read_bytes());require(len(b)==r['logical_bytes'] and sha(b)==r['logical_sha256'],'Entire actual native stream differs')
            if name=='stderr':require(not b,'Successful runner stderr')
            streams.append(dict(name=name,stored_current=pin(r['stored']['path']),logical_bytes=len(b),logical_sha256=sha(b)))
        native.append(dict(receipt=pin(p),actual_PID=x['actual_PID'],actual_launcher_PID=x['actual_launcher_PID'],argv=x['argv'],cwd=x['cwd'],requested_UTC=x['requested_UTC'],start_UTC=x['start_UTC'],end_UTC=x['end_UTC'],exit_code=0,complete_streams=streams))
    require(len(native)==2 and {r['actual_PID'] for r in native}=={83756,85633},'Actual two-runner inventory differs')
    verdict=load(V/'VERDICT.json');require(verdict['mandatory_issues']==[] and verdict['nonmandatory_issues']==[] and verdict['actual_local_case_count']==96 and verdict['publication_clearance'] is False,'Actual operational verdict differs')
    require(not (A/'publication_actual').exists() and not (A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json').exists(),'Unexpected prior service or approval')
    reg=D/'REVISED_OPERATOR_MANIFEST.json';require(pin(reg)['sha256']=='aabb136882570e39d3646a67137fe1d49a8e73132e2c8fea67388feab654f6a4','Operator registry differs')
    sources=load(reg)['approved_operational_sources']
    for r in sources:match(r)
    kit=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py');require(pin(kit)['sha256']=='26f264df93b657137b343acc05ae87a3e8e60d46cbbb8b822bc327d77b89c277' and len(kit.read_text().splitlines())==512,'Reviewed actual kit identity/line count differs')
    output=dict(UTC=datetime.now(timezone.utc).isoformat(),actual_ROOT_recorder_PID=os.getpid(),source=pin(__file__),resolved_interpreter=pin(Path(sys.executable).resolve()),status='PASS_PR302_REPAIRED_PUBLICATION_OPERATORS_AND_COMPLETE_EVIDENCE',original_PR=302,original_head='eb6e0e999521d84a65f9857d338cad76b84d30db',unresolved_material_issues=[],unresolved_nonmandatory_issues=[],publication_operations_clearance=True,science_gate=pin(A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json'),candidate_manifest=pin(F/'SECOND_CANDIDATE_MANIFEST.json'),operator_manifest=pin(reg),approved_operational_sources=sources,review_namespace=str(V),closed_operations_evidence_pins=[pin(V/n) for n in ('REPORT.md','READ_SCOPE.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json')],approved_runtime_targets=initial['runtime_targets'],full_closed_custody=dict(files=[pin(p) for p in sorted(files)],directories=len(dirs),physical_bytes=physical),actual_independent_local_runs=native,actual_cases=96,mandatory_G1_G2_closed_globally=True,ROOT_semantic_scope='ROOT read all current repaired sources, full closed report/reading scope/verdict and original mandatory findings; own actual custody authenticates all135 literal files, current original/repaired sources, all14 science pins/all23public and all three runtime targets, both real test sources and full streams. Strong complete positive fixture and coupled corruptions reach substantive evidence checks. No extra science replay needed.',clerical_read_scope_erratum='The unchanged23925-byte reviewed kit has512 source lines, not529 as stated in the closed REPORT/READ_SCOPE. Their advertised264–555 display reaches the actual end at512. The exact entire pinned source body and all relevant code are unchanged; this count correction does not change program behavior or scientific conclusions. The closed historical report is preserved verbatim.',original_review_packaging_failures_preserved=True,service_execution_has_not_occurred=True,shared_Git_pause_not_changed=True,authorization='User explicitly authorized exact-metadata Zenodo publication and one DOI tracker row after cleared preprint reviews. This clears only reviewed service operators; no shared Git/native/PR write lease is granted.',limits='Local cooperative pins/approval records and actual recorder observations, no hostile-host guarantee, OS/clock or human referee certificate. Unknown external outcomes require read-only reconciliation and no automatic mutation replay.',estimates_percent=dict(mathematics=100,bounded_priority=100,preprint_science=100,publication_operator_review=100,publication_workflow=75))
    p=A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json'
    with p.open('x') as h:json.dump(output,h,indent=2,ensure_ascii=False);h.write('\n')
    p.chmod(0o444)
    print(json.dumps(dict(status=output['status'],actual_ROOT_recorder_PID=os.getpid(),closed_files=135,actual_cases=96,clearance=pin(p),service_actions=0)))
if __name__=='__main__':main()
