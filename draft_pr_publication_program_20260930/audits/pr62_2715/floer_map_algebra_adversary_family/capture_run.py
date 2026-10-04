#!/usr/bin/env python3
"""Own prelaunch source/argv/environment capture and complete child streams."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
label,relative,*extras=sys.argv[1:]
assert label.replace('_','').isalnum()
p=pathlib.PurePosixPath(relative);assert not p.is_absolute() and '..' not in p.parts
script=root/p;assert script.is_file() and not script.is_symlink()
prefix=root/'captures'/label;assert not prefix.with_suffix('.prelaunch.json').exists()
def desc(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PYTHONHASHSEED':'0','PYTHONIOENCODING':'utf-8'}
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
argv=[sys.executable,'-B',str(script)]
sources=[pathlib.Path(__file__),script,root/'INDEPENDENT_CORE.md']+[root/x for x in extras]
pre={'operator':'PR62 Floer-map algebra subagent /root/algebra_reproduction_audit','capture_pid':os.getpid(),'prelaunch_utc':utc(),'argv':argv,'cwd':str(root),'environment':env,'python':sys.version,'dependencies':'Python standard library only','sources':[desc(p) for p in sources]}
prefix.with_suffix('.prelaunch.json').write_text(json.dumps(pre,indent=2)+'\n')
child=subprocess.Popen(argv,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=child.communicate()
post={'operator':pre['operator'],'capture_pid':os.getpid(),'child_pid':child.pid,'prelaunch_utc':pre['prelaunch_utc'],'ended_utc':utc(),'returncode':child.returncode,'prelaunch_sha256':hashlib.sha256(prefix.with_suffix('.prelaunch.json').read_bytes()).hexdigest(),'stdout':{'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'stderr':{'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
prefix.with_suffix('.stdout').write_bytes(out);prefix.with_suffix('.stderr').write_bytes(err);prefix.with_suffix('.post.json').write_text(json.dumps(post,indent=2)+'\n')
print(json.dumps(post));raise SystemExit(child.returncode)
