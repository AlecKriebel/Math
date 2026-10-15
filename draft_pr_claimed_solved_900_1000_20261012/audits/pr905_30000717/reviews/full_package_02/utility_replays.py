from pathlib import Path
import shutil,subprocess,json,datetime,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE/'tmp/extracted'; AUDIT=HERE.parent.parent;PY=str(AUDIT/'tmp/venv/bin/python');results=[]
for name,script,args in [('verify_review','reviews/proof_family/verify_review.py',[]),('seal_manifest','reviews/proof_family/seal_manifest.py',[]),('computation_diagnostics','reviews/computation_family/checks/replay_and_attack.py',['--result-name','fresh_review02.json'])]:
 root=HERE/'tmp'/('utility_'+name);shutil.copytree(BASE,root)
 p=subprocess.run([PY,str(root/script),*args],cwd=root/script.rsplit('/',1)[0],capture_output=True,text=True,timeout=600)
 (HERE/f'evidence/utility_{name}.stdout').write_text(p.stdout);(HERE/f'evidence/utility_{name}.stderr').write_text(p.stderr)
 if p.returncode:raise RuntimeError(name+' '+p.stderr)
 rec={'utility':name,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'disposable_copy':True}
 if name=='computation_diagnostics':
  out=json.loads((root/'reviews/computation_family/results/fresh_review02.json').read_text());rec['verdict']=out['verdict'];rec['unchanged_original']=out['original_file_set_and_bytes_unchanged'];rec['attack_count']=len(out['attacks'])
  (HERE/'evidence/supplemental_computation_diagnostics.json').write_text(json.dumps(out,indent=2)+'\n')
 results.append(rec)
(HERE/'evidence/utility_replays.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':results},indent=2)+'\n')
print(json.dumps([{'utility':r['utility'],'returncode':r['returncode']} for r in results],indent=2))
