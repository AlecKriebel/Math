#!/usr/bin/env python3
"""One family capture: source/argv/environment before launch and full child streams."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
label,script_name=sys.argv[1:]
assert label.replace('_','').isalnum() and pathlib.Path(script_name).name==script_name
prefix=root/'captures'/label
assert not prefix.with_suffix('.prelaunch.json').exists()
desc=lambda p:{'path':str(p),'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
environment={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','PYTHONHASHSEED':'0','PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','PYTHONIOENCODING':'utf-8'}
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
argv=[sys.executable,'-B',str(root/script_name)]
pre={'operator':'PR61 knot-invariant subagent /root/algebra_reproduction_audit','capture_pid':os.getpid(),'prelaunch_utc':utc(),'argv':argv,'cwd':str(root),'environment':environment,'python':sys.version,'dependencies':'Python standard library only','sources':[desc(pathlib.Path(__file__)),desc(root/script_name),desc(root/'INDEPENDENT_CORE.md')]}
prefix.with_suffix('.prelaunch.json').write_text(json.dumps(pre,indent=2)+'\n')
child=subprocess.Popen(argv,cwd=root,env=environment,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=child.communicate()
post={'operator':pre['operator'],'capture_pid':os.getpid(),'child_pid':child.pid,'prelaunch_utc':pre['prelaunch_utc'],'ended_utc':utc(),'returncode':child.returncode,'prelaunch_sha256':hashlib.sha256(prefix.with_suffix('.prelaunch.json').read_bytes()).hexdigest(),'stdout':{'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'stderr':{'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
prefix.with_suffix('.stdout').write_bytes(out);prefix.with_suffix('.stderr').write_bytes(err);prefix.with_suffix('.post.json').write_text(json.dumps(post,indent=2)+'\n')
print(json.dumps(post));raise SystemExit(child.returncode)
