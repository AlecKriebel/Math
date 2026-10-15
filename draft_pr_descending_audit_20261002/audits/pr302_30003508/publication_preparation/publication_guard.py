"""Exact candidate and final scientific clearance for PR302 service operations.

Preparation grants nothing. This module performs no action on import.
"""
from pathlib import Path
from datetime import datetime,timezone
import fcntl,gzip,hashlib,json,os,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math')
D=Path(__file__).resolve().parent
A=D.parent
F=A/'preprint_package_v02'
OUT=A/'publication_actual'
OPERATORS=('publication_guard.py','run_zenodo_step.py','verify_public_record.py','append_tracker.py')
PYTHON='/opt/homebrew/bin/python3'
CLI='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws'
KIT=R/'zenodo_deposit_tool/zenodo.py'
SCIENCE_GATE=A/'ROOT_FINAL_PREPRINT_PUBLICATION_CLEARANCE.json'
OPERATIONS_GATE=A/'ROOT_FINAL_PUBLICATION_OPERATIONS_CLEARANCE.json'
OPERATOR_MANIFEST=D/'REVISED_OPERATOR_MANIFEST.json'
def require(ok,msg):
    if not ok:raise RuntimeError(msg+'; preserve partial outcome and reconcile read-only')
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def pin(p):
    p=Path(p);require(p.is_file() and not p.is_symlink(),'Literal artifact required')
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def write(p,x):
    with p.open('x') as f:f.write(json.dumps(x,indent=2,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
def exact_pins(rows,expected):
    require(type(rows)==list and len(rows)==len(expected),'Mandatory exact pin count differs')
    require(all(type(x)==dict and set(x)=={'path','bytes','sha256','mode'} for x in rows),'Malformed mandatory pin')
    require({x['path'] for x in rows}=={str(p) for p in expected} and len({x['path'] for x in rows})==len(rows),'Mandatory exact unique paths differ')
    for row in rows:require(pin(row['path'])==row,'Approved full body or mode changed '+row['path'])
    return rows
def science_evidence_paths():
    names=('REPORT.md','DERIVATION.md','READ_LEDGER.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json')
    return [A/folder/name for folder in ('preprint_adversary_01','preprint_adversary_02') for name in names]+[A/'ROOT_FIRST_PREPRINT_REVIEW_ADJUDICATION.json',A/'ROOT_SECOND_PREPRINT_REVIEW_ADJUDICATION.json']
def clearance():
    require(not sys.flags.optimize,'Optimization forbidden')
    clear=load(SCIENCE_GATE)
    require(clear['status']=='PASS_PR302_REVISED_PREPRINT_AFTER_TWO_FRESH_WHOLE_PACKAGE_REVIEWS' and clear['original_PR']==302 and clear['original_head']=='eb6e0e999521d84a65f9857d338cad76b84d30db' and clear['original_status']=='claimed_solved','Exact final scientific clearance required')
    require(clear['unresolved_material_issues']==[] and clear['unresolved_nonmandatory_issues']==[] and clear['fresh_whole_package_reviews']==2 and clear['publication_clearance'] is True,'Review loop incomplete')
    manifest=F/'SECOND_CANDIDATE_MANIFEST.json';require(pin(manifest)['sha256']=='b38a09c6768e11c2954892cdaa345a485557082c464d950f573a945f48b5ec71','Exact revised candidate differs')
    require(clear['candidate_manifest']==pin(manifest),'Clearance candidate binding differs')
    candidate=load(manifest);require(len(candidate['files'])==23,'Public scope differs')
    for row in candidate['files']:require(pin(row['path'])==row and row['mode']==0o444,'Frozen public file differs')
    exact_pins(clear['closed_evidence_pins'],science_evidence_paths())
    require(load(A/'ROOT_FIRST_PREPRINT_REVIEW_ADJUDICATION.json')['ROOT_accepts_mathematics'] is True and load(A/'ROOT_SECOND_PREPRINT_REVIEW_ADJUDICATION.json')['ROOT_accepts_mathematics'] is True,'ROOT science decisions absent')
    local=load(F/'zenodo-deposit.json')
    require(local['metadata']==load(F/'record_metadata.json') and local['files']==[{'path':'spectral_tensor_consistency.pdf'},{'path':'spectral_tensor_verification.zip'}],'Exact upload metadata/scope differs')
    require(pin(KIT)['sha256']=='26f264df93b657137b343acc05ae87a3e8e60d46cbbb8b822bc327d77b89c277','Reviewed repository kit changed')
    ops=load(OPERATIONS_GATE)
    require(ops['status']=='PASS_PR302_REPAIRED_PUBLICATION_OPERATORS_AND_COMPLETE_EVIDENCE' and ops['original_PR']==302 and ops['publication_operations_clearance'] is True and ops['unresolved_material_issues']==[] and ops['unresolved_nonmandatory_issues']==[],'Fresh repaired operational review required')
    require(ops['science_gate']==pin(SCIENCE_GATE) and ops['candidate_manifest']==pin(manifest),'Operational/scientific approval differs')
    require(ops['operator_manifest']==pin(OPERATOR_MANIFEST),'Reviewed operator manifest differs')
    registry=load(OPERATOR_MANIFEST)
    require(registry['status']=='FROZEN_REPAIRED_OPERATOR_VERSION_PENDING_FRESH_REVIEW','Unexpected reviewed source registry')
    sources=exact_pins(registry['approved_operational_sources'],[D/n for n in OPERATORS])
    require(ops['approved_operational_sources']==sources,'ROOT approval source version differs')
    review=Path(ops['review_namespace']);require(review.parent==A and review.name.startswith('publication_operations_adversary_') and review.name!='publication_operations_adversary_01','Fresh repaired review namespace required')
    exact_pins(ops['closed_operations_evidence_pins'],[review/n for n in ('REPORT.md','READ_SCOPE.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json')])
    verdict=load(review/'VERDICT.json');require(verdict['mandatory_issues']==[] and verdict['nonmandatory_issues']==[] and verdict['publication_clearance'] is False,'Operational review unresolved or wrong authority')
    expected_runtimes=[Path(x).resolve() for x in (PYTHON,'/usr/bin/curl',CLI)]
    exact_pins(ops['approved_runtime_targets'],expected_runtimes)
    return clear
def acquire():
    OUT.mkdir(exist_ok=True)
    fd=os.open(OUT/'SERVICE_OPERATION.lock',os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
    handle=os.fdopen(fd,'r+b');fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
    clearance();return handle
def execute(label,argv,capture_dir=None,parse_json=True):
    """One actual invocation, retaining before-launch sources and complete streams."""
    clearance();require(Path(label).name==label,'Safe capture label required')
    base=Path(capture_dir) if capture_dir else OUT/'private_processes'
    base.mkdir(parents=True,exist_ok=True);w=base/label;w.mkdir(exist_ok=False)
    source_arguments=[sys.argv[0],*argv]
    sources=list(dict.fromkeys([str(D/n) for n in OPERATORS]+[str(Path(x).resolve()) for x in source_arguments if str(x).endswith('.py') and Path(x).is_file()]))
    require(set(sources)<={str(D/n) for n in OPERATORS}|{str(KIT)},'Unapproved executable operational dependency')
    full=[]
    for i,source in enumerate(sources):
        p=Path(source);q=w/(str(i)+'_'+p.name+'.gz');q.write_bytes(gzip.compress(p.read_bytes(),mtime=0));q.chmod(0o444)
        require(gzip.decompress(q.read_bytes())==p.read_bytes(),'Source archive roundtrip differs')
        full.append(dict(input=pin(p),stored_full_source=pin(q)))
    approvals=[]
    for i,p in enumerate((SCIENCE_GATE,OPERATIONS_GATE,OPERATOR_MANIFEST)):
        q=w/('approval_'+str(i)+'.bin.gz');q.write_bytes(gzip.compress(p.read_bytes(),mtime=0));q.chmod(0o444)
        require(gzip.decompress(q.read_bytes())==p.read_bytes(),'Full approval archive differs')
        approvals.append(dict(input=pin(p),stored_full_source=pin(q)))
    request=dict(actual_launcher_PID=os.getpid(),argv=[str(x) for x in argv],cwd=str(R),requested_UTC=utc(),full_prelaunch_sources=full,full_prelaunch_approvals=approvals,resolved_executable=pin(Path(argv[0]).resolve()),resolved_caller_interpreter=pin(Path(sys.executable).resolve()),automatic_retry=False,custody_limit='Actual recorder/Popen observations and complete retained bodies, without independent OS/clock or upstream-launch attestation')
    write(w/'request.json',request);start=utc()
    clearance()
    child=subprocess.Popen(request['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    write(w/'started.json',dict(actual_PID=child.pid,start_UTC=start,state='STARTED_OUTCOME_PENDING'))
    timed_out=False
    try:out,err=child.communicate(timeout=55)
    except subprocess.TimeoutExpired:
        timed_out=True;child.kill();out,err=child.communicate()
    result=dict(request,actual_PID=child.pid,start_UTC=start,end_UTC=utc(),exit_code=child.returncode,timed_out=timed_out)
    for name,body in [('stdout',out),('stderr',err)]:
        p=w/(name+'.bin.gz');p.write_bytes(gzip.compress(body,mtime=0));require(gzip.decompress(p.read_bytes())==body,'Full stream roundtrip differs')
        result[name]=dict(logical_bytes=len(body),logical_sha256=sha(body),stored=pin(p))
    write(w/'execution.json',result)
    require(child.returncode==0 and not timed_out,'Actual service invocation failed or uncertain; no automatic retry')
    clearance()
    return (json.loads(out) if parse_json else out),result

def authenticate_execution(label,argv,capture_dir=None):
    """Reconstruct a successful actual capture from all retained whole bodies."""
    clearance();base=Path(capture_dir) if capture_dir else OUT/'private_processes';w=base/label
    request=load(w/'request.json');started=load(w/'started.json');result=load(w/'execution.json')
    require(result['argv']==[str(x) for x in argv] and result['cwd']==str(R),'Actual endpoint/argv/cwd differs')
    require(all(result[k]==v for k,v in request.items()),'Actual request/result fields differ')
    require(type(result['actual_PID'])==int and result['actual_PID']>0 and type(result['actual_launcher_PID'])==int and result['actual_launcher_PID']>0,'Actual native PIDs absent')
    require(started==dict(actual_PID=result['actual_PID'],start_UTC=result['start_UTC'],state='STARTED_OUTCOME_PENDING'),'Actual started record differs')
    times=[datetime.fromisoformat(result[k]) for k in ('requested_UTC','start_UTC','end_UTC')]
    require(all(t.tzinfo is not None for t in times) and times[0]<=times[1]<=times[2],'Actual UTC ordering differs')
    require(result['exit_code']==0 and result['timed_out'] is False and result['automatic_retry'] is False,'Actual execution failed/uncertain')
    require(result['resolved_executable']==pin(Path(argv[0]).resolve()) and result['resolved_caller_interpreter']==pin(Path(PYTHON).resolve()),'Actual binary/interpreter target differs')
    expected_sources={str(D/n) for n in OPERATORS}|({str(KIT)} if str(KIT) in argv else set())
    for key,expected in (('full_prelaunch_sources',expected_sources),('full_prelaunch_approvals',{str(SCIENCE_GATE),str(OPERATIONS_GATE),str(OPERATOR_MANIFEST)})):
        copies=result[key];require(type(copies)==list and len(copies)==len(expected) and {x['input']['path'] for x in copies}==expected,'Incomplete exact actual source/approval dependency archives')
        for row in copies:
            require(pin(row['input']['path'])==row['input'] and pin(row['stored_full_source']['path'])==row['stored_full_source'],'Actual retained source/approval pin differs')
            require(gzip.decompress(Path(row['stored_full_source']['path']).read_bytes())==Path(row['input']['path']).read_bytes(),'Full archived actual source/approval bytes differ')
    bodies=[]
    for name in ('stdout','stderr'):
        row=result[name];require(pin(row['stored']['path'])==row['stored'],'Actual stored stream differs')
        require(Path(row['stored']['path'])==w/(name+'.bin.gz'),'Actual stream path differs')
        b=gzip.decompress(Path(row['stored']['path']).read_bytes());require(len(b)==row['logical_bytes'] and sha(b)==row['logical_sha256'],'Actual entire logical stream differs');bodies.append(b)
    return bodies[0],bodies[1],result
