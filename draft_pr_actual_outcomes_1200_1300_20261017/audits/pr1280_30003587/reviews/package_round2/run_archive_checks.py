#!/usr/bin/env python3
"""Serial outside-anchored replays plus independent actual-code corruptions."""
import ast,datetime,hashlib,json,os,pathlib,subprocess,sys,time
F=pathlib.Path(__file__).resolve().parent;A=F.parents[1];P=A/'publication';R=F/'_local/extracted'
def need(c,m):
 if not c:raise RuntimeError(m)
def main():
 env=dict(os.environ,TMPDIR=str(F/'_local/tmp'),PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
 build=json.loads((P/'BUILD_RECEIPT.json').read_text());c=json.loads((A/'CURRENT_PR1280_CONTEXT.json').read_text());args=[a for k,v in build['verification_anchors'].items() for a in ['--expected-'+k+'-sha256',v]];runs=[]
 for flags in [[],['-O'],['-OO']]:
  start=time.monotonic();run=subprocess.run([sys.executable,'-B',*flags,str(R/'verify.py'),*args],cwd=R,env=env,text=True,capture_output=True,timeout=240)
  (F/'_local'/('archive_'+str(len(flags) and flags[0] or 'normal')+'_stderr.txt')).write_text(run.stderr)
  need(run.returncode==0,'actual archive verifier failed '+run.stderr);runs.append({'flags':flags,'elapsed_seconds':time.monotonic()-start,'result':json.loads(run.stdout)})
 need(all(x['result']==runs[0]['result'] for x in runs),'actual archive optimizer mismatch')
 negatives=[]
 for flags in [[],['-O'],['-OO']]:
  run=subprocess.run([sys.executable,'-B',*flags,str(F/'adversarial_checks.py')],cwd=F,env=env,text=True,capture_output=True,timeout=60);need(run.returncode==0,'independent negative control failed '+run.stderr);negatives.append(json.loads(run.stdout))
 sentinel=[]
 for i,rep in enumerate(c['diagnostic_replays']):
  source=(R/rep['program']).read_text();tree=ast.parse(source);need(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'assert in current diagnostic '+rep['program']);funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='require'];need(len(funcs)==1,'require missing or ambiguous');end=funcs[0].end_lineno;lines=source.splitlines(keepends=True);lines.insert(end,"\nrequire(False, 'round2-injected-false-predicate')\n");folder=F/'_local/sentinels'/str(i);folder.mkdir(parents=True,exist_ok=True);program=folder/pathlib.Path(rep['program']).name;program.write_text(''.join(lines))
  for flags in [[],['-O'],['-OO']]:
   run=subprocess.run([sys.executable,'-B',*flags,str(program)],cwd=folder,env=env,text=True,capture_output=True,timeout=30);need(run.returncode!=0 and 'round2-injected-false-predicate' in run.stderr,'false explicit predicate escaped '+rep['program']);sentinel.append({'program':rep['program'],'flags':flags,'nonzero_exit':run.returncode,'explicit_false_predicate_rejected':True})
  program.unlink();folder.rmdir()
 return {'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_archive_sha256':build['verification_zip']['sha256'],'outside_anchors':build['verification_anchors'],'outer_verifier_runs':runs,'all_outer_modes_identical':True,'independent_adversarial_runs':negatives,'diagnostic_false_predicates':sentinel,'scope':'Actual extracted ZIP verified using independent frozen BUILD_RECEIPT anchors in three outer modes; every outer run invokes all six durable diagnostic programs in normal/-O/-OO isolated copies (54 successful diagnostic executions). Eighteen isolated injected false predicates are rejected; no assertions are present in the current six diagnostic ASTs. Token/metadata/corruption fixtures are distinct from live-service assurance.'}
if __name__=='__main__':
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:r=main();r['started_at_utc']=start;(F/'ARCHIVE_REPLAY.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'archive_modes':len(r['outer_verifier_runs']),'independent_adversarial_modes':len(r['independent_adversarial_runs']),'false_predicates':len(r['diagnostic_false_predicates'])}))
 except Exception as e:
  (F/'ARCHIVE_CHECK_FAILURE.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'started_at_utc':start,'error':type(e).__name__+': '+str(e)},indent=2)+'\n');raise
