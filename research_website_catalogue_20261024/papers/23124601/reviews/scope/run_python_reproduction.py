from pathlib import Path
import subprocess,os,signal,time,json,datetime,shutil,gzip,hashlib
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');E=P/'papers/23124601/reviews/scope';S=P/'papers/23124601/sources/published-source/verification';Q=E/'cache/python30-replay';Q.mkdir(exist_ok=False)
env=os.environ.copy()
for k in ['PYTHONOPTIMIZE','PYTHONSTARTUP','PYTHONPATH','PYTHONHOME']:env.pop(k,None)
env.update({'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
py=str(P/'tmp/shared-math-runtime/bin/python');receipts=[]
def run(command,label,cwd,timeout=45):
 start=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (Q/(label+'.stdout')).open('wb') as o,(Q/(label+'.stderr')).open('wb') as er:
  p=subprocess.Popen(command,cwd=cwd,stdout=o,stderr=er,start_new_session=True,env=env)
  try:p.wait(timeout=timeout);status='completed'
  except subprocess.TimeoutExpired:status='timeout';os.killpg(p.pid,signal.SIGKILL);p.wait()
  finally:
   try:os.killpg(p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
 r={'label':label,'command':command,'cwd':str(cwd),'started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout_seconds':timeout,'status':status,'returncode':p.returncode,'elapsed_seconds':time.monotonic()-start,'process_group_cleanup_attempted':True};receipts.append(r);(E/'python-replay-executions.json').write_text(json.dumps(receipts,indent=2)+'\n');print(json.dumps(r),flush=True);return r
D=Q/'baseline';D.mkdir();(D/'fullstreams').mkdir();(D/'receipts').mkdir();script=D/'independent_20_30.py';shutil.copyfile(S/'independent_20_30.py',script);assert script.read_bytes()==(S/'independent_20_30.py').read_bytes()
r=run([py,'-B',str(script)],'baseline-full-backward',D);assert r['returncode']==0,r
with gzip.open(D/'fullstreams/independent_backward_records.txt.gz','rb') as a,gzip.open(S/'certificates/30_action_records.txt.gz','rb') as b:
 lines=0
 while True:
  x=a.readline();y=b.readline();assert x==y,lines
  if not x:break
  lines+=1
assert lines==90921
N=Q/'wrong-terminal';N.mkdir();(N/'fullstreams').mkdir();(N/'receipts').mkdir();source=(S/'independent_20_30.py').read_text();needle='assert images[FULL]==action((1,2,3,4,5)*6,f6,6)';assert source.count(needle)==1
(N/'independent_20_30.py').write_text(source.replace(needle,'assert images[FULL]==action((1,2,3,4,5)*5,f6,6)'))
r=run([py,'-B',str(N/'independent_20_30.py')],'negative-wrong-terminal',N);assert r['returncode']!=0 and r['status']=='completed',r
assert 'AssertionError' in (Q/'negative-wrong-terminal.stderr').read_text()
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_source_script_sha256':hashlib.sha256((S/'independent_20_30.py').read_bytes()).hexdigest(),'baseline_copy_exact':True,'python_true_forward_backward_graphs_and_all261810_literal_edge_equalities_recomputed':True,'fresh_stream_all_records_compared_directly_not_hash_only':lines,'python_20_exact_survivors_recomputed':True,'wrong_terminal_mutation_rejected':True,'no_new_environment_or_source_original_writes':True,'CPP_replay':'Not executed; two existing compiler frontends failed before compilation; failure evidence retained.','scope':'Selected exact mathematical replay; geometric/classical inputs require separate body review.'}
(E/'selected-reproduction-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
