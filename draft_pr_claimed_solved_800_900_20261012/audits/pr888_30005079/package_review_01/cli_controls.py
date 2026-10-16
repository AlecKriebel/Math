"""Actual CLI checks for the independently authenticated frozen candidate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

H=Path(__file__).resolve().parent
A=H.parent
C=A/'candidate'
T=H/'private_tmp'
CP='db1810399e605970d022afc971438561bbf4f3bca60ee93f457919d7b7a051c1'
IP='a41885c94a6a7d97ac16700256d10a29b616895b80b37db693239e59f7475480'
TOOL=C/'portable.py'
W=A/'publication_tools_01/private_tmp/wheels'

def require(x,s):
    if not x: raise ValueError(s)

def pin(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def clean(s):
    return s.replace(str(A),'<AUDIT_ROOT>').replace(str(A.parents[2]),'<PROJECT_ROOT>').replace(str(Path(sys.executable)),'<PYTHON>')

receipts=[]
def run(label,args,expected,env_extra=None,code=True):
    require(hashlib.sha256(TOOL.read_bytes()).hexdigest()=='bcaac73bf1620098e0d24f2a2cb9399613567be6018b99329c0a58b6e0101910','prelaunch startup pin')
    env=os.environ.copy(); env['TMPDIR']=str(T)
    if env_extra: env.update(env_extra)
    start=datetime.now(timezone.utc).isoformat()
    p=subprocess.run([sys.executable,'-I','-S','-B',*map(str,args)],cwd=T,env=env,capture_output=True,timeout=1200)
    completed=datetime.now(timezone.utc).isoformat()
    (T/('fresh_'+label+'.stdout')).write_bytes(p.stdout)
    (T/('fresh_'+label+'.stderr')).write_bytes(p.stderr)
    item={'label':label,'started_utc':start,'completed_utc':completed,
          'returncode':p.returncode,'expected_returncode':expected,
          'stdout_raw_pin':pin(p.stdout),'stderr_raw_pin':pin(p.stderr),
          'stderr_redacted':clean(p.stderr.decode(errors='replace')),
          'argv_redacted':[clean(str(x)) for x in args],
          'returncode_record_provenance':'Direct actual subprocess.run returncode, immediately persisted before outcome/semantic assertions.'}
    direct=(json.dumps(item,indent=2)+'\n').encode()
    (T/('fresh_'+label+'.process_record.json')).write_bytes(direct)
    item['direct_process_record_pin']=pin(direct)
    require(p.returncode==expected,label+' return code')
    if code and p.stdout:
        item['result']=json.loads(p.stdout)
    receipts.append(item)
    return item

if __name__=='__main__':
    base=[TOOL,'current',CP]
    wrong=run('wrong_current_pin',[TOOL,'current','0'*64,'--verify-only'],1)
    require(wrong['result']['status']=='REJECTED','wrong pin rejected')
    auth=run('current_authentication_only',base+['--verify-only'],0)
    require(auth['result']['portable']['replay']=='NOT_RUN','authentication does not claim replay')
    run('build_forbids_verify_only',[TOOL,'build',IP,T/'blocked_build/rank-two-fano-verification.zip','--root',C/'verification','--verify-only'],2,code=False)
    old=T/'default_build/rank-two-fano-verification.zip'
    before=old.read_bytes()
    existing=run('build_existing_output',[TOOL,'build',IP,old,'--root',C/'verification','--dependency-dir',W],1)
    require('output must be fresh' in existing['result']['reason'] and old.read_bytes()==before,'existing output intact')
    no_dep=T/'missing_dependency_output'; no_dep.mkdir(exist_ok=True)
    requested=no_dep/'rank-two-fano-verification.zip'
    missing=run('default_build_missing_dependencies',[TOOL,'build',IP,requested,'--root',C/'verification'],1)
    require('dependency-dir' in missing['result']['reason'] and not requested.exists(),'missing dependencies no fallback/output')
    original=run('original_root_actual_optimized',['-O',C/'verification/source/verify_publication.py'],1,code=False)
    require('Run with assertions enabled' in original['stderr_redacted'],'original actual optimized rejection')
    native=A.parents[2]/'unsolved_math_prioritization'
    source=run('source_only_complete_corpora',[TOOL,'source-only','--catalog',native/'catalog.json',
                '--problems',native/'cache/problems.json','--reports',native/'cache/research_results.json',
                '--primary-dir',A/'private_sources'],0)
    require(source['result']['archival_code_executed'] is False and source['result']['target_report']=='ABSENT','source-only isolation')
    hostile=T/'hostile_startup'; hostile.mkdir(exist_ok=True)
    canary=hostile/'EXECUTED_CANARY'
    text='from pathlib import Path\nPath('+repr(str(canary))+').write_text("EXECUTED")\nraise RuntimeError("HOSTILE_STARTUP_EXECUTED")\n'
    for n in ['sitecustomize.py','sympy.py','mpmath.py']:(hostile/n).write_text(text)
    full=run('hostile_environment_full_replay',base+['--dependency-dir',W],0,
              {'PYTHONPATH':str(hostile),'PYTHONOPTIMIZE':'2','PYTHONDONTWRITEBYTECODE':'0'})
    require(not canary.exists() and full['result']['portable']['replay']['status']=='PASS','hostile hook absent full replay passed')
    # Preserve prior actual success receipts unchanged; their command return codes
    # were observed separately by the caller before this collector was authored.
    prior=[]
    for label,name in [('current_normal','current_normal_raw.json'),('current_optimized','current_optimized_raw.json'),('default_fresh_outside_build','default_build_raw.json')]:
        raw=(T/name).read_bytes(); value=json.loads(raw)
        require(value['status']=='PASS','prior actual success')
        if label=='default_fresh_outside_build':
            require(value['sha256']=='0d1d415108c0fede7405ef6e2704d348782121d879571d123532676ed6f8f957' and old.read_bytes()==(C/'rank-two-fano-verification.zip').read_bytes(),'default build exact published bytes')
        require('/Users/' not in raw.decode() and '/private/' not in raw.decode(),'success receipt private-path scan')
        (H/(label.upper()+'_RECEIPT.json')).write_bytes(raw)
        prior.append({'label':label,'observed_returncode':0,'raw_receipt_pin':pin(raw)})
    out={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS',
         'actual_fresh_cli_invocations':len(receipts),'earlier_actual_success_receipts':prior,
         'receipts':receipts,'private_redaction':'Raw stdout/stderr are retained privately by pin; only local audit/interpreter prefixes in argv/stderr are redacted. Successful tool JSON is unmodified.',
         'scope':'Four qualifying directly recorded full replays: initial manual normal/optimized/default-build plus fresh hostile-environment replay. Historical collector eight cases are separate; authentication-only/source-only execute zero archival code.'}
    out['collector_incident']={'initial_collection_exit':1,
        'cause':'Reviewer expected-hash literal accidentally appended the archive member count 150; actual archive SHA256 is the 64-hex value ending f8f957.',
        'all_eight_actual_case_returncodes_had_passed_before_failure':True,
        'raw_outputs_preserved':True,'candidate_defect':False,
        'historical_initial_cli_cases':8,
        'historical_status_provenance':'Guard-inferred only; qualified separately in HISTORICAL_CLI_RECOVERY_QUALIFIED.json. Original raw outputs and first recovered receipt preserved privately.',
        'fresh_cli_cases_after_evidence_repair':8,
        'total_actual_full_replays_including_historical_hostile':5,
        'qualifying_directly_recorded_full_replays':4,
        'initial_collector_code_pin':pin((T/'cli_controls_failed_collection.py').read_bytes()),
        'timestamps':'Historical collector starts were not retained and completion metadata was observed later. Every new case directly records start/end and actual returncode before later assertions.'}
    (H/'CLI_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','fresh_actual_cli_invocations':len(receipts),'qualifying_full_replays':4,'historical_collector_cases_separate':8,'hostile_canary_absent':True}))
