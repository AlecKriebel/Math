from pathlib import Path
import subprocess,os,signal,time,json,datetime,hashlib,gzip,shutil
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');E=P/'papers/23124601/reviews/scope';S=P/'papers/23124601/sources/published-source/verification';Q=E/'cache/selected-replay-clt';Q.mkdir(exist_ok=False)
env=os.environ.copy()
for k in ['PYTHONOPTIMIZE','PYTHONSTARTUP','PYTHONPATH','PYTHONHOME']:env.pop(k,None)
env.update({'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
py=str(P/'tmp/shared-math-runtime/bin/python');receipts=[]
def run(command,label,cwd=Q,timeout=45):
 start=time.monotonic()
 with (Q/(label+'.stdout')).open('wb') as o,(Q/(label+'.stderr')).open('wb') as er:
  p=subprocess.Popen(command,cwd=cwd,stdout=o,stderr=er,start_new_session=True,env=env)
  try:p.wait(timeout=timeout);status='completed'
  except subprocess.TimeoutExpired:status='timeout';os.killpg(p.pid,signal.SIGKILL);p.wait()
  finally:
   try:os.killpg(p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
 r={'label':label,'command':command,'cwd':str(cwd),'timeout_seconds':timeout,'status':status,'returncode':p.returncode,'elapsed_seconds':time.monotonic()-start,'process_group_cleanup_attempted':True};receipts.append(r);(E/'selected-replay-executions.json').write_text(json.dumps(receipts,indent=2)+'\n');return r
cpp=Q/'check_turn_4.cpp';shutil.copyfile(S/'reference/check_turn_4.cpp',cpp)
assert cpp.read_bytes()==(S/'reference/check_turn_4.cpp').read_bytes()
r=run(['/Library/Developer/CommandLineTools/usr/bin/clang++','-O3','-std=c++17',str(cpp),'-o',str(Q/'check_turn_4')],'compile',timeout=25);assert r['returncode']==0,r
r=run([str(Q/'check_turn_4'),'--stream'],'cpp-full-stream');assert r['returncode']==0,r
actual=Q/'cpp-full-stream.stdout';expected=gzip.open(S/'certificates/30_action_records.txt.gz','rb');n=0;actualhash=hashlib.sha256();size=0;terminal=None
with actual.open('rb') as a,expected:
 for line in a:
  if line.startswith(b'S|'):
   assert line==expected.readline(),n;n+=1;size+=len(line);actualhash.update(line)
  else:terminal=json.loads(line)
 assert expected.read()==b''
assert n==90921 and size==15258431
assert terminal=={'status':'PASS','reachable_states':234368,'outgoing_edges':711342,'coaccessible_states':90921,'coaccessible_edges':261810}
# Preserve fresh generated stream compressed, then remove only own unneeded raw duplicate.
with actual.open('rb') as a,gzip.GzipFile(filename=str(Q/'cpp-fresh-action-stream.gz'),mode='wb',mtime=0) as out:shutil.copyfileobj(a,out)
actual.unlink()
D=Q/'python-backward';D.mkdir();(D/'fullstreams').mkdir();(D/'receipts').mkdir();shutil.copyfile(S/'independent_20_30.py',D/'independent_20_30.py')
r=run([py,'-B',str(D/'independent_20_30.py')],'python-full-backward',D);assert r['returncode']==0,r
with gzip.open(D/'fullstreams/independent_backward_records.txt.gz','rb') as a,gzip.open(S/'certificates/30_action_records.txt.gz','rb') as b:
 lines=0
 while True:
  x=a.readline();y=b.readline();assert x==y,lines
  if not x:break
  lines+=1
assert lines==90921
# A mathematical negative control: valid state graph and edge arithmetic, wrong terminal braid.
N=Q/'wrong-terminal';N.mkdir();(N/'fullstreams').mkdir();(N/'receipts').mkdir();source=(S/'independent_20_30.py').read_text();needle='assert images[FULL]==action((1,2,3,4,5)*6,f6,6)';assert source.count(needle)==1
(N/'independent_20_30.py').write_text(source.replace(needle,'assert images[FULL]==action((1,2,3,4,5)*5,f6,6)'))
r=run([py,'-B',str(N/'independent_20_30.py')],'negative-wrong-terminal',N);assert r['returncode']!=0 and r['status']=='completed',r
assert 'AssertionError' in (Q/'negative-wrong-terminal.stderr').read_text()
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_copies_exact_originals':True,'cpp_all_261810_literal_edge_equalities_and_endpoint_recomputed':True,'cpp_fresh_stream_full_record_comparisons':n,'cpp_fresh_stream_data_bytes':size,'cpp_fresh_stream_data_sha256':actualhash.hexdigest(),'python_independent_true_backward_all_edges_recomputed':True,'python_fresh_stream_full_record_comparisons':lines,'python_20_exact_survivors_recomputed':True,'wrong_terminal_mutation_rejected':True,'no_new_environment_or_source_original_writes':True,'scope':'Selected mathematical reproductions only, not a wrapper PASS promotion or geometric theorem proof.'}
(E/'selected-reproduction-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
