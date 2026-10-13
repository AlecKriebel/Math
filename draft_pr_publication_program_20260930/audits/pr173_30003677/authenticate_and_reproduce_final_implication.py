from pathlib import Path
import json,hashlib,stat,subprocess,datetime
A=Path(__file__).resolve().parent;B=A/'general_theorem_implication_adversary';PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
def require(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
def authenticated_rows(base,rows):
 seen=set()
 for r in rows:
  n=r['path'];q=Path(n);require(not q.is_absolute() and '..' not in q.parts and n not in seen,'Unsafe or repeated member');seen.add(n);p=base/n;require(p.is_file() and not p.is_symlink(),'Missing or symlink member');d=pin(p);require(d['bytes']==r['bytes'] and d['sha256']==r['sha256'] and d['mode']=='0444','Changed member '+n)
 return seen
if __name__=='__main__':
 fp=B/'FINAL_INVENTORY.json';require(pin(fp)['sha256']=='15d8b0a247da974dac836cfe95e8d3e1a2a0525a504acd7729b2b902da5601d8','Final external anchor differs');j=json.loads(fp.read_text());seen=authenticated_rows(B,j['files']);seen.add('FINAL_INVENTORY.json');require(seen=={p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file()} and len(seen)==43,'Incomplete/extra final members');require(pin(fp)['mode']=='0444','Final inventory writable')
 f=B/'FIRST_MANIFEST.json';require(pin(f)['sha256']=='423b8197bec75210edf712ab6c06ea8bad117ade78c3b3a1a3dbb82f522f9ae4','First substantive seal changed');authenticated_rows(B,json.loads(f.read_text())['files'])
 owner_al=[r['path'] for r in j['files'] if r['public_allowlist']];require(all(not n.startswith('private/') for n in owner_al),'Private source in release selection');al=[n for n in owner_al if not n.endswith('.stderr.txt')];require({'FIRST_ASSESSMENT.md','POST_SEAL_ADDENDUM.md','SCIENTIFIC_DISPOSITION.md','finite_comparison_checks.py'}<=set(al),'Missing substantive public companion')
 runs=[];outputs={}
 for src,negative in [(A/'priority_config_multiseed/public/support_checks.py',None),(A/'priority_config_multiseed/public/normalization_checks.py',None),(B/'finite_comparison_checks.py','--negative-control')]:
  for opt in [False,True]:
   for neg in ([False,True] if negative else [False]):
    argv=[PY,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(src)]+([negative] if neg else []);r=subprocess.run(argv,cwd=A,capture_output=True,text=True,timeout=45);require(r.returncode!=0 if neg else r.returncode==0,'Unexpected control outcome')
    if neg:require('Jump-mark normalization mismatch' in r.stderr and not r.stdout,'Negative failed for wrong reason')
    else:
     z=json.loads(r.stdout);z.pop('optimized',None);require(z.get('result',z.get('status'))=='PASS','No actual positive control pass');key=src.relative_to(A).as_posix();previous=outputs.get(key);require(previous is None or previous==z,'Ordinary/optimized positive results differ');outputs[key]=z
    runs.append({'source':src.relative_to(A).as_posix(),'source_identity':pin(src),'optimized':opt,'negative':neg,'exit_code':r.returncode,'stdout_bytes':len(r.stdout.encode()),'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr_bytes':len(r.stderr.encode()),'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest(),'accepted':True,'raw_traceback_not_publicly_supplied':neg})
 out=A/'ROOT_FINAL_IMPLICATION_EVIDENCE_AND_CONTROLS.json';require(not out.exists(),'Preserve previous acceptance');o={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'ALL_43_IMPLICATION_FILES_FIRST_SEAL_AUTHENTICATED_FINITE_CONTROLS_REPRODUCED','family':'general_theorem_implication_adversary','retained_file_count':43,'first_manifest':pin(f),'final_inventory':pin(fp),'public_allowlist':al,'owner_allowed_raw_stderr_additionally_excluded':[n for n in owner_al if n not in al],'all_retained_files':[{'path':n,**pin(B/n)} for n in sorted(seen)],'runs':runs,'clean_positive_results':outputs,'scope':'Complete artifact authentication and finite exact diagnostic reproduction; ROOT separately read the first assessment, final mathematical addendum and scientific disposition in full. No stochastic theorem is established by finite computation.','source_script':pin(Path(__file__))};out.write_text(json.dumps(o,indent=2)+'\n');out.chmod(0o444);print(json.dumps({'status':o['status'],'runs':len(runs),'public_files':len(al)}))
