from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
O=Path(__file__).resolve().parent
C=O.parents[3]
mode=sys.argv[1]
if mode not in ['normal','optimized']:raise RuntimeError('bad mode')
label=sys.argv[2] if len(sys.argv)>2 else mode
if not label.replace('_','').isalnum():raise RuntimeError('bad label')
dest=O/('execution_'+label)
dest.mkdir(exist_ok=False)
source=O/'audit_actual_candidate.py'
pin={'bytes':source.stat().st_size,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
argv=['/opt/homebrew/bin/python3','-E','-S','-B']+(['-O'] if mode=='optimized' else [])+[str(source)]
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
proc=subprocess.Popen(argv,cwd=C,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
base={'schema':'pr108-independent-audit-execution/v1','recorder_PID':os.getpid(),'actual_child_PID':proc.pid,'argv':argv,'cwd':str(C),'environment':env,'source':pin,'UTC_start':started}
(dest/'started.json').write_text(json.dumps(base,indent=2)+'\n')
try:out,err=proc.communicate(timeout=55)
except subprocess.TimeoutExpired:
 proc.kill();out,err=proc.communicate();base['timeout']=True
base.update(UTC_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=proc.returncode,child_reaped=True)
for name,b in [('stdout',out),('stderr',err)]:
 (dest/(name+'.bin')).write_bytes(b);base[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'path':name+'.bin'}
(dest/'execution.json').write_text(json.dumps(base,indent=2)+'\n')
print(json.dumps({'mode':mode,'PID':proc.pid,'exit':proc.returncode,'stdout':out.decode('utf8'),'stderr':err.decode('utf8')}))
raise SystemExit(proc.returncode)
