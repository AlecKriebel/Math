from pathlib import Path
import subprocess,json,hashlib,base64,datetime,os,shutil
P=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr1131_30005455')
D=P/'root_actual21_known23592692_activation01'
p=P/'known23592692_operations21_preparation01/native_step21.py'
contract=P/'known23592692_operations21_authority01/ROOT_EXECUTION_ADOPTION21.json'
H=lambda b:hashlib.sha256(b).hexdigest()
action=ACTUAL21_ACTION_LITERAL;contractsha=ACTUAL21_CONTRACT_SHA_LITERAL;h=ACTUAL21_NATIVE_CONTROLLER_SHA_LITERAL
assert action in ['stage-known','publish','verify-public','ledger']
assert D.is_dir() and not any(q.is_symlink()for q in[D,*D.parents])
assert H(p.read_bytes())==h and H(contract.read_bytes())==contractsha
out=D/('ROOT_'+action+'_ORIGINAL_PARENT_NATIVE.json')
envp=D/('ROOT_'+action+'_ENVIRONMENT_BEFORE_NATIVE.json')
assert not out.exists() and not envp.exists()
program_specs={'git':('/opt/homebrew/Cellar/git/2.38.2/bin/git','2caa5a792b58b0d09d3e0cba7034eeac4fc2a678812e583a8f68a6d2e07183e0'),'gh':('/opt/homebrew/Cellar/gh/2.85.0/bin/gh','91f6e182bce24da56581ab999088c55ae0216309af19bc6167bbc4396c3f4ea5'),'gws':('/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws','0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e')}
native_env=os.environ.copy()
native_env['PATH']=':'.join(str(Path(path).parent)for path,pin in program_specs.values())+':'+native_env.get('PATH','')
resolved_programs={}
for name,(path,pin)in program_specs.items():
 selected=shutil.which(name,path=native_env['PATH'])
 assert selected is not None and Path(selected).resolve()==Path(path).resolve() and H(Path(selected).read_bytes())==pin
 resolved_programs[name]={'requested_path':path,'resolved_path':str(Path(selected).resolve()),'sha256':pin}
interpreter=Path('/opt/homebrew/bin/python3').resolve()
assert H(interpreter.read_bytes())=='b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf'
launch="from pathlib import Path;import hashlib;p=Path("+repr(str(p))+");b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=="+repr(h)+";n={'__file__':str(p),'__name__':'ROOT_checked_actual_known21_helper'};exec(compile(b,str(p),'exec',dont_inherit=True,optimize=0),n);n['main'](['--action',"+repr(action)+",'--root-contract-sha256',"+repr(contractsha)+"])"
argv=['/opt/homebrew/bin/python3','-I','-S','-B','-c',launch]
before=datetime.datetime.now(datetime.timezone.utc).isoformat()
preflight={'at':before,'action':action,'known_id':23592692,'future_create_allowance':0,'ROOT_contract_sha256':contractsha,'helper_sha256':h,'native_command':argv,'effective_PATH':native_env['PATH'],'resolved_native_programs':resolved_programs,'same_environment_supplied_before_helper_preparation':True,'one_attempt_environment_marker_consumed_before_child':True}
def saved(path,value):
 with path.open('x')as f:
  os.fchmod(f.fileno(),0o600);json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 fd=os.open(D,os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
saved(envp,preflight)
rc=None;error=None
stdoutp=D/('ROOT_'+action+'_ORIGINAL_PARENT_STDOUT.bin')
stderrp=D/('ROOT_'+action+'_ORIGINAL_PARENT_STDERR.bin')
# Allocate physical originals before any child; retain them even on interruption.
with stdoutp.open('xb')as stdout,stderrp.open('xb')as stderr:
 os.fchmod(stdout.fileno(),0o600);os.fchmod(stderr.fileno(),0o600)
 try:
  result=subprocess.run(argv,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,env=native_env,timeout=1800)
  rc=result.returncode
 except subprocess.TimeoutExpired as exc:
  error={'type':'TimeoutExpired','timeout':exc.timeout,'outcome_unknown_GET_only':True,'descendant_may_continue':True}
 except BaseException as exc:
  error={'type':type(exc).__name__,'message':str(exc),'outcome_unknown_GET_only':True,'descendant_may_continue':True}
 finally:
  stdout.flush();os.fsync(stdout.fileno());stderr.flush();os.fsync(stderr.fileno())
ob=stdoutp.read_bytes();eb=stderrp.read_bytes()
physical={'stdout':{'path':str(stdoutp),'bytes_at_snapshot':len(ob),'sha256_at_snapshot':H(ob)},'stderr':{'path':str(stderrp),'bytes_at_snapshot':len(eb),'sha256_at_snapshot':H(eb)}}
complete_native_return=error is None and type(rc)is int
successful_native_return=complete_native_return and rc==0
v={'argv':argv,'before':before,'after':datetime.datetime.now(datetime.timezone.utc).isoformat(),'helper_sha256':h,'ROOT_contract_sha256':contractsha,'action':action,'known_id':23592692,'future_create_allowance':0,'returncode':rc,'error':error,'stdout_base64':base64.b64encode(ob).decode(),'stderr_base64':base64.b64encode(eb).decode(),'interpreter_sha256':H(interpreter.read_bytes()),'physical_raw_stream_custody_saved_before_parse':True,'complete_native_return':complete_native_return,'successful_native_return':successful_native_return,'physical_streams':physical,'stream_snapshot_may_be_incomplete_and_descendant_may_continue':not successful_native_return,'no_automatic_next_action':True,'no_retry_or_alternate_OUT_authorized':True,'native_environment_preflight':{'path':str(envp),'bytes':len(envp.read_bytes()),'sha256':H(envp.read_bytes())},'effective_PATH':native_env['PATH'],'resolved_native_programs':resolved_programs}
saved(out,v)
print(json.dumps({'path':str(out),'sha256':H(out.read_bytes()),'action':action,'returncode':rc,'error':error,'stdout':ob.decode(errors='backslashreplace'),'stderr':eb.decode(errors='backslashreplace')},ensure_ascii=False))
if error is not None or rc!=0:raise RuntimeError('Known21 action stopped; preserve complete native outcome, GET-only reconciliation, no retry')
