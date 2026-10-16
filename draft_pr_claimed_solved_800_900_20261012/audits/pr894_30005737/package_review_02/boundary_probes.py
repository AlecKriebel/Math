from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time,importlib.util
R=Path(__file__).resolve().parent;C=R.parent/'package_assembly_01/candidate';T=R/'private_tmp/boundaries';T.mkdir();tool=C/'portable.py';pin='746ca08c65b489a216edfc3962f7001ac6750945f8468fdb96bd9ba4c7739f0c';records=[];checks=[]
def ph(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def run(label,args,env=None):
 start=now();t=time.monotonic_ns();p=subprocess.Popen([sys.executable,*args],cwd=T,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate(timeout=120);m={'label':label,'started_utc':start,'ended_utc':now(),'elapsed_monotonic_ns':time.monotonic_ns()-t,'pid':p.pid,'returncode':p.returncode,'stdout':ph(out),'stderr':ph(err)}
 save(T/(label+'.stdout.bin'),out);save(T/(label+'.stderr.bin'),err);save(T/(label+'.json'),(json.dumps(m,indent=2)+'\n').encode());records.append(m);return p.returncode,out,err
def test(label,ok):
 checks.append({'label':label,'passed':bool(ok)})
 if not ok:raise ValueError(label)
base=['-I','-S','-B',str(tool),'current',pin,'--root',str(C)]
rc,b,e=run('verify_only',base+['--verify-only']);d=json.loads(b);test('verify-only byte authentication label and no archival execution',rc==0 and d['portable']['replay']['label']=='VERIFY_ONLY_BYTE_AUTHENTICATION_NO_ARCHIVAL_EXECUTION' and d['portable']['replay']['archival_code_executed'] is False)
rc,b,e=run('wrong_pin',base[:5]+['0'*64]+base[6:]+['--verify-only']);test('independent manifest pin rejects',rc!=0 and b'pin mismatch' in b)
requested=T/'must-not-be-created';rc,b,e=run('verify_only_receipt',base+['--verify-only','--receipt-dir',str(requested)]);test('verify-only receipt misuse rejects before directory',rc!=0 and not requested.exists())
rc,b,e=run('double_optimization',['-I','-S','-B','-OO',str(tool),'current',pin,'--root',str(C),'--verify-only']);test('double optimization rejects',rc!=0 and b'single -O' in b)
rc,b,e=run('missing_no_site',['-I','-B',str(tool),'current',pin,'--root',str(C),'--verify-only']);test('missing no-site rejects',rc!=0 and b'actual -I -S -B' in b)
# In-memory malformed-input tests use authenticated current code, never mutated files.
spec=importlib.util.spec_from_file_location('reviewed_tool',tool);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for text in [b'{"x":1,"x":2}',b'{"n":{"x":1,"x":2}}',b'NaN',b'Infinity',b'-Infinity',b'1e9999']:
 try:m.strict_json(text);rejected=False
 except ValueError:rejected=True
 test('strict JSON rejects '+text.decode(),rejected)
for name in ['../x','/x','a//b','a/./b','a/../b','A\\B']:
 try:m.safe_name(name);rejected=False
 except ValueError:rejected=True
 test('unsafe path rejects '+name,rejected)
for size in [True,1.5,-1,'1',None]:
 try:m.pin_row({'path':'x','bytes':size,'sha256':'0'*64});rejected=False
 except ValueError:rejected=True
 test('typed byte count rejects '+repr(size),rejected)
fixture=T/'regular';fixture.write_bytes(b'x');link=T/'symlink';link.symlink_to(fixture)
try:m.read_regular(link);rejected=False
except ValueError:rejected=True
test('symlink leaf rejects before open',rejected)
# Demonstrate a capable hostile startup hook before the isolated resistance run.
hostile=T/'hostile';hostile.mkdir();marker=T/'hook-was-executed';expected=C/'verification/source/authored/CHECK_RESULTS.json'
(hostile/'sitecustomize.py').write_text('import os,sys\nfrom pathlib import Path\nPath('+repr(str(marker))+').write_bytes(b"HOOK_EXECUTED")\nsys.stdout.buffer.write(Path('+repr(str(expected))+').read_bytes())\nsys.stdout.flush()\nos._exit(0)\n')
env=os.environ.copy();env['PYTHONPATH']=str(hostile);env['PYTHONOPTIMIZE']='2';env['PYTHONSTARTUP']=str(hostile/'sitecustomize.py')
rc,b,e=run('hostile_capability',['-B','-c','raise RuntimeError("hook should have exited")'],env);test('hostile hook capable of output forgery before script',rc==0 and marker.read_bytes()==b'HOOK_EXECUTED' and b==expected.read_bytes());marker.unlink()
receipt=T/'resisted_receipts';rc,b,e=run('hostile_resistance',base+['--receipt-dir',str(receipt)],env);d=json.loads(b);rp=d['portable']['replay'];test('actual isolated current resists startup hook',rc==0 and not marker.exists() and rp['status']=='PASS');events=rp['launcher']['events'];test('hostile replay has eight genuine expected child modes',[x['measured_flags']['optimize'] for x in events]==[0,1,0,0,0,1,1,1]);test('hostile replay contains actual positive execution and controls',all(x['original_execution_began']==(x['kind']!='corrupt') for x in events) and all((x['process']['returncode']==0)==(x['kind']=='positive') for x in events))
result={'timestamp_utc':now(),'status':'PASS','checks':checks,'actual_top_level_processes':records,'hostile_runtime_scope':'actual selected interpreter and standard library; no OS sandbox or arbitrary concurrent-mutation guarantee','source_and_candidate_mutations':False}
(R/'BOUNDARY_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'processes':len(records),'hostile_capability_and_isolated_resistance':True}))
