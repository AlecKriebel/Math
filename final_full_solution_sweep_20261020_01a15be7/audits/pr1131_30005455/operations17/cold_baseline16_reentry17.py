"""Fresh process: persistent-HOLD reentry rejects before any provider adapter."""
from pathlib import Path
import sys,json,hashlib,stat,io,contextlib,os
ROOT=Path(__file__).resolve().parent;S=ROOT.parent/'operations16/source';OLD=ROOT.parent/'operations'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
need(sys.flags.optimize==0 and sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,'Nonoptimized -I -S -B only')
need(len(sys.argv)==5,'Exact case/action/source/bootstrap arguments')
case=Path(sys.argv[1]).resolve();action=sys.argv[2];MS,BS=sys.argv[3:]
need(ROOT/'private'in case.parents and case.is_dir()and not case.is_symlink(),'Own inert case only')
need(action in {'resume-stage','publish'},'Fixed reentry action')
def inventory():
 out={}
 for q in [case,*case.rglob('*')]:
  st=q.lstat();need(not q.is_symlink(),'Symlink in case')
  out[q.relative_to(case).as_posix()]={'mode':stat.S_IMODE(st.st_mode),'mtime_ns':st.st_mtime_ns,'kind':'dir'if q.is_dir()else'file',**({}if q.is_dir()else{'bytes':st.st_size,'sha256':sha(q.read_bytes())})}
 return out
before=inventory()
b=(OLD/'bootstrap.py').read_bytes();need(sha(b)=='960b33e83135968ab40ef069b1b8876df47b70d1c4ef528bf0d8c836213ac58b','Original bootstrap')
n={'__file__':str(OLD/'bootstrap.py'),'__name__':'cold_immutable05'};exec(compile(b,str(OLD/'bootstrap.py'),'exec',dont_inherit=True,optimize=0),n)
load,_=n['load_verified'](OLD,'eab69e53e9d32510bbf00d74c1b94b70542a8b29cf326c42f5d974e510f09d00',sha(b));model=load('full_controls')
b=(S/'bootstrap16.py').read_bytes();need(sha(b)==BS,'External bootstrap anchor');n={'__file__':str(S/'bootstrap16.py'),'__name__':'cold_verified17'}
exec(compile(b,str(S/'bootstrap16.py'),'exec',dont_inherit=True,optimize=0),n);m=n['load_verified'](S,MS,BS);c=m.c
m.RUNTIME=case/'runtime';m.PRIVATE=case/'private';m.PRIOR_RUNTIME=case/'preserved05_runtime';m.CONTEXT['source_root']=case/'checked_source'
m.CONTEXT['check_sources']=lambda:n['source_bytes'](case/'checked_source',MS,BS)
for name in ['ops_common','publish_and_ledger','collect_live','integrate_remote','native_policy']:
 mod=m.LOAD05(name);mod.RUNTIME=m.RUNTIME;mod.PRIVATE=m.PRIVATE
c.zenodo.STATE_DIR=case/'mock_repo/.zenodo-state';m.live.REPO=case/'mock_repo'
attempts=[]
def blocked(*a,**k):attempts.append('provider/process/credential');raise RuntimeError('Cold reentry must not reach any provider/credential adapter')
c.command=m.pl.command=m.ir.command=blocked;c.zenodo.token_for=blocked;c.zenodo.ZenodoClient=blocked;m.pl.fetch=blocked
args=[action,'--expected-pr-head',m.HEAD,'--clearance-sha256',sha((m.RUNTIME/'ROOT_OPERATIONAL_CLEARANCE16.json').read_bytes())]
if action!='resume-stage':args+=['--deposit-id','777']
error=None
try:
 with contextlib.redirect_stdout(io.StringIO()):m.main(args)
except Exception as e:error={'type':type(e).__name__,'message':str(e)}
need(error and 'Consumed response/context is on HOLD'in error['message'],'Cold reentry did not stop at persistent HOLD')
need(not attempts and not model.ATTEMPTS,'Cold external adapter attempted')
need(inventory()==before,'Cold reentry changed case bytes/metadata/namespace')
print(json.dumps({'status':'PASS','pid':os.getpid(),'action':action,'error':error,'provider_credential_process_attempts':0,'case_bytes_modes_nsmtimes_namespace_preserved':True,'actual_effects':0}))
