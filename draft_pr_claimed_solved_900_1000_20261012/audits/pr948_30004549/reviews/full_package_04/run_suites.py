import pathlib,json,subprocess,datetime,hashlib,os
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr948_30004549';O=A/'reviews/full_package_04';W=A/'publication/workflow';PYTHON=P/'audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
changes={
 'test_workflow.py':[("tempfile.TemporaryDirectory(prefix='private-fixture-',dir=W)","tempfile.TemporaryDirectory(prefix='private-fixture-',dir=Path("+repr(str(O))+"))"),("output=W/f'DEVELOPMENT_ATTEMPT_{number:02d}.json'","output=Path("+repr(str(O/'WORKFLOW.json'))+")")],
 'test_review_history.py':[("target=W/f'FULL01_HISTORY_ATTEMPT_{number:02d}.json'","target=Path("+repr(str(O/'HISTORY.json'))+")")],
 'test_root_fixes.py':[("(W/'ROOT_FIXES_RESULT.json').write_text","(Path("+repr(str(O/'ROOT_FIXES.json'))+")).write_text")],
 'test_base_context.py':[("target=W/f'BASE_CONTEXT_ATTEMPT_{number:02d}.json'","target=Path("+repr(str(O/'BASE_CONTEXT.json'))+")")],
 'test_live_base_context.py':[("target=W/f'LIVE_BASE_ATTEMPT_{number:02d}.json'","target=Path("+repr(str(O/'LIVE_BASE.json'))+")")]
}
rows=[]
for name,replacements in changes.items():
 p=W/name;raw=p.read_bytes();s=raw.decode()
 for old,new in replacements:
  if s.count(old)!=1:raise RuntimeError('adaptation occurrence '+name+' '+old)
  s=s.replace(old,new)
 q=O/('adapted_'+name);q.write_text(s)
 # Preserve original __file__, real current core, all sealed fixtures. Only output/temp relocation.
 bootstrap='import sys; p=sys.argv[1]; s=open(sys.argv[2],"rb").read(); exec(compile(s,p,"exec",dont_inherit=True,optimize=0),{"__name__":"__main__","__file__":p})'
 env=os.environ.copy();env['TMPDIR']=str(O/'tmp');env['TMP']=env['TMPDIR'];env['TEMP']=env['TMPDIR'];env.pop('PYTHONOPTIMIZE',None)
 proc=subprocess.run([str(PYTHON),'-I','-S','-B','-c',bootstrap,str(p),str(q)],cwd=R,env=env,capture_output=True,timeout=240)
 rows.append({'suite':name,'source_sha256':hashlib.sha256(raw).hexdigest(),'adapted_sha256':hashlib.sha256(s.encode()).hexdigest(),'replacements':replacements,'__file__':str(p),'returncode':proc.returncode,'stdout':proc.stdout.decode(errors='replace'),'stderr':proc.stderr.decode(errors='replace'),'actual_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 (O/'SUITE_ADAPTATIONS_AND_RUNS.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows[-1]),flush=True)
 if proc.returncode:raise SystemExit(proc.returncode)
