#!/usr/bin/env python3
"""Independent outside-namespace replay, precise approval and native closure."""
import argparse, datetime, hashlib, json, pathlib, stat, subprocess, sys
A=pathlib.Path(__file__).resolve().parent
N=A/'semilinear_modules'
ENV={'PATH':'/opt/homebrew/bin:/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1'}
APPROVED={
 'semilinear_proof.md':'ec0882f914aa8b24c2363dc82000dc689678a8a0ea9429768afd3a46f1e55f3b',
 'audit_report.md':'d88240b5c781f5d79addb61c5db43a3751424fc9cd48fcf6b961b32e7253e238',
 'verify_semilinear.py':'6f60d6e915949201fe4bcd3596ab8efe543bd22da1041c20ffc2d8309e2e5f42',
 'closure_plan.md':'7df574d6789ab6b3dc0c156643ae30598a3ed8fca0bf1547e9909cc55d6ee6bb',
 'seal_audit.py':'e1cb9f0220a8fe0c33fc658d492be0441f7a56996ec398e62500c7a21bcf05ae',
 'authorization_protocol.md':'c423828e60abc10f21229993ff067d3b829387b50861b52acba93ee8c5c0bab0',
 'incidental_team_status_exposure.md':'5da413f6e2d112f8f0b963722bb034534d22a5e2005ca2c6e125b60d5031b42b',
 'research_log_after_release.md':'dbd751b49a9a99eb8250078ea0767e14ce51ab2d8c8fdf9865554a48d44292ec',
 'historical_input_versions.json':'93886340e313081e1cee9aea94f341af9fee3fafe15b24dcc0b628f8d13a0254'}
FINAL={'closure_research_log.md','final_inventory.json','closure_record.json','closure_native_receipt.json'}
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    data=p.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}
def inv(base):
    output={}
    for p in sorted(base.rglob('*')):
        if p.is_symlink(): raise RuntimeError('Unexpected symlink: '+str(p))
        if p.is_file(): output[p.relative_to(base).as_posix()]=pin(p)
    return output
def require(x,s):
    if not x: raise RuntimeError(s)
def save(p,x):
    with p.open('x') as f: f.write(json.dumps(x,indent=2)+'\n')
def common(): return {'snapshot':inv(A/'snapshot'),'sources':inv(A/'root_sources_private')}
ap=argparse.ArgumentParser()
ap.add_argument('operation',choices=['replay','close','postcheck'])
args=ap.parse_args()
for name,digest in APPROVED.items(): require(pin(N/name)['sha256']==digest,'Reviewed file changed: '+name)
OUT=A/'root_family_capture_private'/'semilinear_modules'/(args.operation+'001')
require(not OUT.exists(),'One-shot capture exists')
OUT.mkdir(parents=True)
before=inv(N); common_before=common(); self_before=pin(pathlib.Path(__file__))
save(OUT/'whole_before.json',{'namespace':before,'common':common_before,'capturer':self_before})
executions=[]
def capture(label,argv,expected=None):
    executable=pathlib.Path(argv[0]).resolve()
    pre={'utc':now(),'argv':argv,'cwd':str(N),'environment_exact':ENV,'executable':str(executable),'executable_pin':pin(executable),'capturer_pin':self_before,'namespace_before':pin(OUT/'whole_before.json')}
    if expected is not None:
        (OUT/(label+'.expected.stdout')).write_bytes(expected)
        pre['expected_stdout']=pin(OUT/(label+'.expected.stdout'))
    save(OUT/(label+'.preexecution.json'),pre)
    process=subprocess.run(argv,cwd=N,env=ENV,capture_output=True)
    (OUT/(label+'.stdout')).write_bytes(process.stdout)
    (OUT/(label+'.stderr')).write_bytes(process.stderr)
    result=dict(pre,completed_utc=now(),exit_status=process.returncode,stdout=pin(OUT/(label+'.stdout')),stderr=pin(OUT/(label+'.stderr')),stdout_text=process.stdout.decode(),stderr_text=process.stderr.decode(),executable_after=pin(executable))
    save(OUT/(label+'.json'),result)
    executions.append({'label':label,'receipt':pin(OUT/(label+'.json')),'exit_status':process.returncode})
    require(process.returncode==0 and process.stderr==b'' and result['executable_after']==pre['executable_pin'],label+' native failure; no silent retry')
    if expected is not None: require(process.stdout==expected,label+' whole stdout mismatch')
    return process.stdout
if args.operation=='replay':
    require(not any((N/name).exists() for name in FINAL),'Already closed')
    version=capture('interpreter_version',['/usr/bin/python3','--version']).decode().strip()
    expected=json.loads((N/'independent_semilinear_controls_native_receipt.json').read_text())['stdout'].encode()
    result=json.loads(capture('independent_controls',['/usr/bin/python3','-B',str(N/'verify_semilinear.py')],expected))
    require(result['status']=='pass' and result['checks']==33802,'Mathematical controls scope mismatch')
    preflight=json.loads(capture('full_preflight',['/opt/homebrew/bin/python3.11','-B',str(N/'seal_audit.py'),'--preflight']))
    require(preflight['preflight']=='pass' and preflight['closure_performed'] is False,'Preflight did not pass')
    require(before==inv(N) and common_before==common(),'Replay input bodies/modes changed')
    receipt={'utc':now(),'status':'PASS_EXTERNAL_ROOT_SEMILINEAR_FULL_REPLAY','exit_status':0,'input_stability':True,'namespace_file_count':len(before),'all_namespace_and_common_source_bodies_modes_unchanged':True,'actual_system_python_version':version,'historical_child_version_limitation_preserved':True,'executions':executions,'whole_before':pin(OUT/'whole_before.json'),'approved_hashes':APPROVED,'capturer':self_before}
elif args.operation=='close':
    replay=A/'root_family_capture_private/semilinear_modules/replay001/ROOT_RECEIPT.json'
    replay_record=json.loads(replay.read_text())
    replay_before=json.loads((replay.parent/'whole_before.json').read_text())
    require(replay_record['status']=='PASS_EXTERNAL_ROOT_SEMILINEAR_FULL_REPLAY' and replay_record['exit_status']==0 and replay_record['input_stability'],'Replay not accepted')
    require(replay_before['namespace']==before and replay_before['common']==common_before,'Reviewed replay namespace changed')
    require(not any((N/name).exists() for name in FINAL),'Already closed; no retry')
    token='ROOT_PR344_SEMILINEAR_ONCE_AFTER_FULL_PROOF_CODE_PROVENANCE_AND_EXTERNAL_REPLAY_20261004'
    auth={'utc':now(),'authorized':True,'authorization_text':token,'approved_hashes':APPROVED,'external_replay':{'receipt_path':str(replay),'sha256':pin(replay)['sha256'],'exit_status':0,'input_stability':True},'source':'Root explicit precise one-time authorization after complete proof/report/code/plan/gate/historical/current provenance adjudication and independent external whole-namespace replay. Only closure_authorization.json replacement and four declared final additions are authorized; no subsequent namespace writes. Priority and publication gates remain pending.','root_closure_program':self_before,'allowed_final_additions':sorted(FINAL)}
    authpath=A/'ROOT_SEMILINEAR_MODULES_CLOSURE_AUTHORIZATION.json'
    save(authpath,auth)
    (N/'closure_authorization.json').write_text(json.dumps(auth,indent=2)+'\n')
    actual=capture('actual_outer_sealer',['/opt/homebrew/bin/python3.11','-B',str(N/'seal_audit.py'),'--seal'])
    internal=json.loads((N/'closure_native_receipt.json').read_text())
    require(internal['record_kind']=='internally_assembled_execution_record' and internal['actual_external_process_return_code'] is None and internal['exit_status_declaration']==0 and internal['input_stability'],'Internal declaration invalid')
    require(actual==internal['stdout'].encode() and internal['stderr']=='','Actual outer streams disagree with internal declaration')
    after=inv(N)
    require(set(after)-set(before)==FINAL,'Unexpected additions')
    require(all(after[k]==v for k,v in before.items() if k!='closure_authorization.json'),'Existing reviewed body/mode changed')
    require(common_before==common(),'Common inputs changed')
    receipt={'utc':now(),'status':'PASS_ONE_TIME_SEMILINEAR_NATIVE_EXTERNAL_CLOSURE','family_completion_estimate_percent':100,'namespace_file_count':len(after),'old_files_unchanged_except_precisely_authorized_authorization_record':True,'common_inputs_unchanged':True,'authorization':pin(authpath),'actual_outer_execution':executions,'whole_namespace_after':after,'priority_complete':False,'preprint_approved':False}
else:
    close=A/'root_family_capture_private/semilinear_modules/close001/ROOT_RECEIPT.json'
    closed=json.loads(close.read_text())
    require(closed['status']=='PASS_ONE_TIME_SEMILINEAR_NATIVE_EXTERNAL_CLOSURE' and before==closed['whole_namespace_after'],'Closed namespace changed')
    inventory=json.loads((N/'final_inventory.json').read_text())
    expected_existing={p['path'] for p in inventory['artifact_inputs']}
    actual_existing={str(N/k) for k in before if k not in FINAL}
    require(expected_existing==actual_existing,'Final recursive input inventory incomplete')
    for p in inventory['artifact_inputs']+inventory['checked_external_inputs']+[inventory['generated_final_log']]:
        observed=pin(pathlib.Path(p['path']))
        require(observed['sha256']==p['sha256'] and observed['bytes']==p['size'],'Closed inventory pin mismatch')
    declaration=json.loads((N/'closure_record.json').read_text())
    require(declaration['status']=='COMPLETE_SEALED' and declaration['completion_estimate_audit_percent']==100,'Closure verdict wrong')
    expected=json.loads((N/'independent_semilinear_controls_native_receipt.json').read_text())['stdout'].encode()
    capture('portable_closed_controls',['/usr/bin/python3','-B',str(N/'verify_semilinear.py')],expected)
    require(before==inv(N) and common_before==common(),'Postcheck changed a file')
    receipt={'utc':now(),'status':'PASS_COMPLETE_CLOSED_SEMILINEAR_NAMESPACE_ROOT_READBACK','family_completion_estimate_percent':100,'namespace_file_count':len(before),'closed_inventory_count':len(expected_existing),'whole_closed_bodies_modes_unchanged':True,'external_inputs_checked':True,'native_controls_whole_stdout_reproduced':True,'executions':executions,'closure_receipt':pin(close)}
require(self_before==pin(pathlib.Path(__file__)),'Root capture code changed')
save(OUT/'ROOT_RECEIPT.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='whole_namespace_after'},indent=2))
