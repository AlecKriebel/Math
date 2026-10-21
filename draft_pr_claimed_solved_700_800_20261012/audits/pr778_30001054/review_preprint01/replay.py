from pathlib import Path
import subprocess,hashlib,json,datetime,sys,os
B=Path(__file__).resolve().parent
S=B/'extracted'
PDF=B.parent/'preprint/output/pdf/paper.pdf'
def snapshot(root):
 d={}
 for p in sorted(root.rglob('*')):
  if p.is_symlink(): raise RuntimeError('symlink')
  if p.is_file():d[p.relative_to(root).as_posix()]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 return d
temp=B/'tmp';temp.mkdir(exist_ok=True)
env=os.environ.copy();env['TMPDIR']=str(temp)
for key in ('PYTHONPATH','PYTHONHOME','PYTHONOPTIMIZE'):env.pop(key,None)
before=snapshot(S)
rows=[]
for py in ['/opt/homebrew/bin/python3','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']:
 for opt in [False,True]:
  cmd=[py,'-E','-s','-B']+(['-O'] if opt else [])+[str(S/'verify_bundle.py'),'--pdf',str(PDF)]
  start=datetime.datetime.now(datetime.timezone.utc).isoformat()
  r=subprocess.run(cmd,cwd='/',env=env,capture_output=True,timeout=300)
  row={'at_utc':start,'python':py,'version':subprocess.check_output([py,'--version'],text=True).strip(),'optimized':opt,'returncode':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr':r.stderr.decode()}
  if r.returncode==0: row['result']=json.loads(r.stdout)
  else:row['stdout']=r.stdout.decode()
  rows.append(row)
  if snapshot(S)!=before:raise RuntimeError('source changed')
  (B/'REPLAY_RESULTS.json').write_text(json.dumps({'before_files':len(before),'rows':rows,'source_unchanged_after_each':True,'TMPDIR':str(temp)},indent=2)+'\n')
  print(row['version'],opt,r.returncode,flush=True)
  if r.returncode:raise RuntimeError('replay failure')
print('all four PASS')
