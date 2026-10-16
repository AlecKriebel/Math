from pathlib import Path
import os,sys,subprocess,json,hashlib,time
ROOT=Path(__file__).resolve().parent.parent
W=ROOT/'preprint/tmp/review03-work'
PKG=W/'extracted'
PDF=ROOT/'preprint/output/pdf/paper.pdf'
OUT=ROOT/'review_preprint03'
runtimes=['/opt/homebrew/bin/python3','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']
env=os.environ.copy();env['TMPDIR']=str(W);env['PYTHONDONTWRITEBYTECODE']='1'
for k in ('PYTHONPATH','PYTHONHOME','PYTHONOPTIMIZE'):env.pop(k,None)
rows=[]
for py in runtimes:
 for opt in (False,True):
  name=('system314' if py==runtimes[0] else 'bundled312')+('-O' if opt else '-normal')
  command=[py,'-E','-s','-B']+(['-O'] if opt else [])+[str(PKG/'verify_bundle.py'),'--pdf',str(PDF)]
  start=time.monotonic();r=subprocess.run(command,env=env,cwd='/',capture_output=True,timeout=600)
  row={'name':name,'version':subprocess.run([py,'--version'],capture_output=True,text=True).stdout.strip(),'command':command,'seconds':round(time.monotonic()-start,3),'returncode':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr':r.stderr.decode(errors='replace')}
  (OUT/(name+'.json')).write_bytes(r.stdout);rows.append(row)
  print(name,r.returncode,flush=True)
(OUT/'RUNTIME_REPLAYS.json').write_text(json.dumps(rows,indent=2)+'\n')
