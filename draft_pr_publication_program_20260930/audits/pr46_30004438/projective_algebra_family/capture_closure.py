from pathlib import Path
import datetime
import hashlib
import json
import os
import pwd
import subprocess

root=Path(__file__).resolve().parent
source=root/'close_family.py'
capture=root/'closure_actual_capture'
capture.mkdir(exist_ok=False)
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
command=['/usr/bin/python3','-B',str(source)]
pre={'utc':utc(),'operator':'Codex projective-algebra audit subagent',
     'os_user':pwd.getpwuid(os.getuid()).pw_name,'uid':os.getuid(),
     'launcher_pid':os.getpid(),'parent_pid':os.getppid(),'cwd':str(root),
     'command':command,'source_sha256':sha(source),
     'launcher_source_sha256':sha(Path(__file__))}
(capture/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
with (capture/'stdout.txt').open('wb') as out,(capture/'stderr.txt').open('wb') as err:
    process=subprocess.Popen(command,cwd=root,stdout=out,stderr=err)
    (capture/'LAUNCHED.json').write_text(json.dumps({'utc':utc(),'child_pid':process.pid,
         'launcher_pid':os.getpid()},indent=2)+'\n')
    code=process.wait()
post={'utc':utc(),'returncode':code,'child_pid':process.pid,
      'source_sha256_after':sha(source),'stdout_sha256':sha(capture/'stdout.txt'),
      'stderr_sha256':sha(capture/'stderr.txt')}
(capture/'COMPLETION.json').write_text(json.dumps(post,indent=2)+'\n')
if code==0:
    for p in capture.iterdir():p.chmod(0o444)
print(json.dumps(post,indent=2))
raise SystemExit(code)
