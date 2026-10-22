from pathlib import Path
from datetime import datetime,timezone
import subprocess,hashlib,json,sys
W=Path(__file__).absolute().parent; P=W.parent/'preprint'; S=P/'source'; pin='6287da0dabdad505f3d312dfeefc9e75f34caaeccb267fada3f9119502cfa6be'
results=[]
for name,exe in [('python314','/opt/homebrew/bin/python3'),('python312','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')]:
 for outer_opt in [False,True]:
  mode=name+('_optimized' if outer_opt else '_normal'); cmd=[exe,'-I','-B']+(['-O']if outer_opt else[])+[str(S/'verify_source.py'),'--expected-manifest-sha256',pin,'--pdf',str(P/'output/pdf/paper.pdf'),'--replay']
  started=datetime.now(timezone.utc).isoformat();p=subprocess.run(cmd,cwd='/',capture_output=True,timeout=1800)
  (W/(mode+'.stdout.json')).write_bytes(p.stdout);(W/(mode+'.stderr.txt')).write_bytes(p.stderr)
  results.append({'mode':mode,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'command':cmd,'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_bytes':len(p.stderr)})
  (W/'SOURCE_REPRODUCTION_RUNS.json').write_text(json.dumps(results,indent=2)+'\n');print(mode,p.returncode,len(p.stdout),len(p.stderr),flush=True)
  if p.returncode!=0 or p.stderr:raise ValueError("source replay rejected")
print('DONE',flush=True)
