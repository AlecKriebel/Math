from pathlib import Path
import os,sys,subprocess,json,difflib,datetime
R=Path(__file__).parent;A=R.parents[1];W=A/'publication/workflow';PY=json.loads((A/'preprint/PACKAGE_REPLAY_normal.json').read_bytes())['command'][0]
def save(n,d):
 raw=(json.dumps(d,indent=2)+'\n').encode()
 with (R/n).open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert (R/n).read_bytes()==raw
changes={
 'test_workflow.py':[("existing=list(W.glob('DEVELOPMENT_ATTEMPT_*.json'))","existing=list(Path("+repr(str(R))+ ").glob('INERT_WORKFLOW_*.json'))"),("output=W/f'DEVELOPMENT_ATTEMPT_{number:02d}.json'","output=Path("+repr(str(R))+ ")/f'INERT_WORKFLOW_{number:02d}.json'")],
 'test_root_fixes.py':[("(W/'ROOT_FIXES_RESULT.json').write_text","(Path("+repr(str(R))+ ")/'INERT_ROOT_FIXES.json').write_text")],
 'test_base_context.py':[("target=W/f'BASE_CONTEXT_ATTEMPT_{number:02d}.json'","target=Path("+repr(str(R))+ ")/'INERT_BASE_CONTEXT.json'")],
 'test_live_base_context.py':[("target=W/f'LIVE_BASE_ATTEMPT_{number:02d}.json'","target=Path("+repr(str(R))+ ")/'INERT_LIVE_BASE_CONTEXT.json'")],
 'test_review_history.py':[("target=W/f'FULL01_HISTORY_ATTEMPT_{number:02d}.json'","target=Path("+repr(str(R))+ ")/'INERT_REVIEW_HISTORY.json'")]}
results=[]
for n,replacements in changes.items():
 original=(W/n).read_text();adapted=original
 for before,after in replacements:
  assert adapted.count(before)==1,(n,before);adapted=adapted.replace(before,after)
 # The historical __file__ is kept for all authoritative reads; only receipt outputs change.
 source='__file__='+repr(str(W/n))+'\n'+adapted
 path=R/('adapted_'+n)
 with path.open('w') as f:f.write(source);f.flush();os.fsync(f.fileno())
 assert path.read_text()==source
 save('DIFF_'+n+'.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original':str(W/n),'diff':''.join(difflib.unified_diff(original.splitlines(True),source.splitlines(True))),'scope':'Output-only adaptation plus explicit original absolute __file__; no tested production logic edits.'})
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run([PY,'-I','-S','-B',str(path)],cwd=A.parents[2],capture_output=True,text=True)
 result={'suite':n,'started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr};save('EXECUTION_'+n+'.json',result);results.append(result);print(n,p.returncode,p.stdout,p.stderr,flush=True)
 assert p.returncode==0
save('INERT_SUITE_EXECUTIONS.json',results)
