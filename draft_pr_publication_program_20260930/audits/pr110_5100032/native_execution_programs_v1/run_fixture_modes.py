"""Record two genuine small synthetic-test CLI processes; no services/native/Git writes."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
D=pathlib.Path(__file__).parent;out=D/'fixtures'/('outer_'+str(os.getpid()));out.mkdir(mode=0o700)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
env=dict(os.environ);records=[];success=True
for mode,flags in [('normal',[]),('optimized',['-O'])]:
    argv=[os.path.realpath(sys.executable),'-B',*flags,str(D/'test_programs.py')];start=now()
    child=subprocess.Popen(argv,cwd=D,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);stdout,stderr=child.communicate(timeout=30)
    for kind,b in [('stdout',stdout),('stderr',stderr)]:
        if len(b)>65536:raise ValueError('Unexpected test stream size')
        (out/(mode+'_'+kind+'.bin')).write_bytes(b)
    records.append({'actual_process_record':True,'synthetic_fixture_only':True,'argv':argv,'cwd':str(D),'PID':child.pid,
      'UTC_start':start,'UTC_end':now(),'environment_sha256':pin(json.dumps(env,sort_keys=True).encode())['sha256'],
      'exit_code':child.returncode,'communicate_completed':True,'reaped':child.returncode is not None,
      'stdout':{'path':mode+'_stdout.bin',**pin(stdout)},'stderr':{'path':mode+'_stderr.bin',**pin(stderr)}})
    success=success and child.returncode==0
(out/'RESULT.json').write_text(json.dumps({'schema':'pr110-program-fixture-outer-envelopes/v1','UTC':now(),'operator_PID':os.getpid(),
 'synthetic_fixture_only':True,'actual_service_calls':0,'actual_native_assess_calls':0,'successful':success,'processes':records},sort_keys=True,indent=2)+'\n')
print(json.dumps({'outer_fixture_folder':str(out),'successful':success}));sys.exit(0 if success else 1)
