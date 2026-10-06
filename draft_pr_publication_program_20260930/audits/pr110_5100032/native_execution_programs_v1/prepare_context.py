"""Read-only full Git-blob inspection; descriptive preparation, never live preflight."""
import datetime,hashlib,json,os,pathlib,subprocess
D=pathlib.Path(__file__).parent;C=D.parent.parents[2]
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def canonical(x):return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
records=[];env=dict(os.environ)
def git(*args):
    argv=['git','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null',*args];begin=now()
    child=subprocess.Popen(argv,cwd=C,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(timeout=30)
    records.append({'actual_readonly_process':True,'PID':child.pid,'argv':argv,'cwd':str(C),'environment_sha256':pin(canonical(env))['sha256'],
      'UTC_start':begin,'UTC_end':now(),'exit_code':child.returncode,'reaped':child.returncode is not None,
      'stdout_full_pin':pin(out),'stderr_full_pin':pin(err),'large_stdout_not_duplicated':True})
    if child.returncode or err:raise ValueError('Read-only Git inspection failed')
    return out
head=git('rev-parse','HEAD').decode().strip();branch=git('symbolic-ref','--short','HEAD').decode().strip()
names=['queue.py','manifest.json','policy.json','catalog.json','assessments.json','state.json','history.jsonl','assessment_history.jsonl','ranking.csv','summary.json','SHORTLIST.md','QUEUE.md','README.md','AGENTS.md']
bodies={name:git('show',head+':unsolved_math_prioritization/'+name) for name in names}
catalog=json.loads(bodies['catalog.json']);target=next(x for x in catalog if x['id']=='5100032')
assessments=json.loads(bodies['assessments.json']);state=json.loads(bodies['state.json'])
campaign=[line for line in bodies['QUEUE.md'].decode().splitlines() if '5100032 / AMR-050-0032' in line]
end=git('rev-parse','HEAD').decode().strip()
result={'schema':'pr110-program-preparation-full-native-inspection/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'descriptive_only_not_execution_preflight':True,'captured_main':head,'branch':branch,'main_unchanged_during_capture':head==end,
 'full_native_blob_pins':{name:{'path':'unsolved_math_prioritization/'+name,**pin(body)} for name,body in bodies.items()},
 'records':len(catalog),'assessments':len(assessments),'state_entries':len(state),'target_state_present':'5100032' in state,
 'target_catalog':target,'target_assessment':assessments['5100032'],'campaign_target_rows':campaign,
 'queue_source_fully_read':True,'all_runtime_data_blobs_fully_read_and_hashed':True,'processes':records,
 'actual_native_assess_calls':0,'actual_export_calls':0,'actual_service_calls':0,'Git_mutations':0}
out=D/'CONTEXT_INSPECTION.json';fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'wb') as f:f.write(canonical(result))
print(json.dumps({'context_pin':pin(out.read_bytes()),'captured_main':head,'branch':branch,'native_records':len(catalog),'target_status':target['local_status'],'target_turns':target['turns_used'],'target_state_present':'5100032' in state}))
