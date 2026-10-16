import pathlib, os, subprocess, json, time, hashlib
R=pathlib.Path(__file__).resolve().parent; A=R.parent.parent
P=A/'root_reproduction/.cache/venv/bin/python'
C=R/'.cache'; env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(C/'tmp'))
commands=[['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',str(P),'-B','-c',"import socket,json,sympy,mpmath; s=socket.socket();\ntry: s.connect(('1.1.1.1',443)); result={'network_denied':False}\nexcept OSError as e: result={'network_denied':True,'errno':e.errno,'error':str(e)}\nprint(json.dumps(dict(result,sympy=sympy.__version__,mpmath=mpmath.__version__)))"],['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',str(P),'-B',str(C/'extracted/run_all.py')]]
records=[]
for idx,cmd in enumerate(commands):
 start=time.time(); p=subprocess.run(cmd,cwd=C/'extracted',env=env,capture_output=True,text=True)
 (R/(('NETWORK_DENIAL' if idx==0 else 'PACKAGE_REPLAY')+'.stdout.jsonl')).write_text(p.stdout)
 (R/(('NETWORK_DENIAL' if idx==0 else 'PACKAGE_REPLAY')+'.stderr.txt')).write_text(p.stderr)
 record={'command':cmd,'returncode':p.returncode,'seconds':time.time()-start,'stdout':p.stdout,'stderr':p.stderr}; records.append(record)
 assert p.returncode==0,record
 if idx==0: assert json.loads(p.stdout)['network_denied']
assert len(records[1]['stdout'].splitlines())==10
(R/'REPRODUCTION_LEDGER.json').write_text(json.dumps({'status':'PASS','dependency_environment_outside_package':str(P),'TMPDIR':str(C/'tmp'),'os_network_denial':True,'full_unmodified_json_comparison':True,'records':records},indent=2)+'\n')
print(records[1]['stdout'])
