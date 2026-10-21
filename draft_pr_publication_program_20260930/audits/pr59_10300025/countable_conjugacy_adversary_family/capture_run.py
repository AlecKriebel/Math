#!/usr/bin/env python3
"""Prelaunch exact argv, environment and source pins, then full child streams."""
import datetime, hashlib, json, os, pathlib, subprocess, sys
root=pathlib.Path(__file__).resolve().parent
label,relative,*args=sys.argv[1:]
assert label.replace('_','').isalnum() and '..' not in pathlib.Path(relative).parts
script=root/relative
prefix=root/'captures'/label
assert not prefix.with_suffix('.prelaunch.json').exists()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
env={'PATH':'/usr/bin:/bin:/opt/homebrew/bin','LANG':'C','LC_ALL':'C',
     'PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1','PYTHONIOENCODING':'utf-8'}
argv=[sys.executable,'-B',str(script),*args]
desc=lambda p:{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
sources=[desc(pathlib.Path(__file__)),desc(script)]
if relative.startswith('reproduction/'): sources.append(desc(root/'reproduction/KNOWN_RESULT.md'))
pre={'operator':'PR59 mathematical subagent /root/algebra_reproduction_audit','capture_pid':os.getpid(),
     'prelaunch_utc':utc(),'argv':argv,'cwd':str(script.parent),'environment':env,'sources':sources,
     'python':sys.version,'executable':sys.executable}
prefix.with_suffix('.prelaunch.json').write_text(json.dumps(pre,indent=2)+'\n')
p=subprocess.Popen(argv,cwd=script.parent,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=p.communicate()
post={'operator':pre['operator'],'capture_pid':os.getpid(),'child_pid':p.pid,
      'prelaunch_utc':pre['prelaunch_utc'],'ended_utc':utc(),'returncode':p.returncode,
      'prelaunch_sha256':hashlib.sha256(prefix.with_suffix('.prelaunch.json').read_bytes()).hexdigest(),
      'stdout':{'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},
      'stderr':{'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
prefix.with_suffix('.stdout').write_bytes(out);prefix.with_suffix('.stderr').write_bytes(err)
prefix.with_suffix('.post.json').write_text(json.dumps(post,indent=2)+'\n')
print(json.dumps(post));raise SystemExit(p.returncode)
