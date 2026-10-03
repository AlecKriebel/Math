from pathlib import Path
import datetime
import hashlib
import json
import os
import pwd
import subprocess

root=Path(__file__).resolve().parent
operator=root/'replay_original_controls.py'
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources={'author':root.parent/'source_snapshot'/'verify.py',
         'prior_review':root.parent/'source_snapshot'/'independent_review'/'independent_checks.py'}
for selection,source in sources.items():
    prefix=root/('original_'+selection+'_capture')
    prefix.mkdir(exist_ok=True)
    command=['/usr/bin/python3','-B',str(operator),selection]
    pre={'utc':utc(),'operator':'Codex projective-algebra audit subagent',
         'os_user':pwd.getpwuid(os.getuid()).pw_name,'uid':os.getuid(),
         'launcher_pid':os.getpid(),'parent_pid':os.getppid(),'cwd':str(root),
         'command':command,'operator_source_sha256':sha(operator),
         'frozen_control_source_path':str(source),'frozen_control_source_sha256':sha(source),
         'launcher_source_sha256':sha(Path(__file__)),
         'execution':'Unmodified frozen source exec; __file__ output base redirects receipts to owned replay directory.'}
    (prefix/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
    with (prefix/'stdout.txt').open('wb') as out,(prefix/'stderr.txt').open('wb') as err:
        process=subprocess.Popen(command,cwd=root,stdout=out,stderr=err)
        (prefix/'LAUNCHED.json').write_text(json.dumps({'utc':utc(),'child_pid':process.pid,
             'launcher_pid':os.getpid()},indent=2)+'\n')
        code=process.wait()
    post={'utc':utc(),'returncode':code,'child_pid':process.pid,
          'operator_source_sha256_after':sha(operator),
          'frozen_control_source_sha256_after':sha(source),
          'stdout_sha256':sha(prefix/'stdout.txt'),'stderr_sha256':sha(prefix/'stderr.txt')}
    (prefix/'COMPLETION.json').write_text(json.dumps(post,indent=2)+'\n')
    print(selection,json.dumps(post))
    if code:raise SystemExit(code)
