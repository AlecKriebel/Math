import hashlib,json,os,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;D=R.parents[1]/'publication';W=R/'private/cold';E=W/'extracted';MAN='5f86b1126a90ffa4a7d9725a039b89e5ab1653f8a6c3fcd1f96a4b11e4553fa4';PIN='7f661daf498cd151ddd5fd44eb0d7d763b8bdfdbf7c12262dc5255a0133a4bc6';PY=sys.executable
if hashlib.sha256((E/'verify_package.py').read_bytes()).hexdigest()!=PIN:raise RuntimeError('Verifier drift')
rows=[]
for mode,flags,opt in [('normal',[],None),('O',['-O'],None),('OO',['-OO'],None),('env2',[],'2')]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
 if opt:env['PYTHONOPTIMIZE']=opt
 outer=int(subprocess.check_output([PY,*flags,'-c','import sys;print(sys.flags.optimize)'],env=env,text=True))
 work=W/('work_'+mode);work.mkdir(exist_ok=True)
 p=subprocess.run([PY,*flags,str(E/'verify_package.py'),'--expected-manifest',MAN,'--pdf',str(D/'output/pdf/note.pdf'),'--workdir',str(work)],env=env,text=True,capture_output=True,timeout=600)
 (W/(mode+'.stdout')).write_text(p.stdout);(W/(mode+'.stderr')).write_text(p.stderr)
 if p.returncode:raise RuntimeError(p.stderr)
 receipt=json.loads(p.stdout);saved=json.loads((D/('PACKAGE_REPLAY_'+mode+'.json')).read_text())
 if json.dumps(receipt,sort_keys=True)!=json.dumps(saved,sort_keys=True):raise RuntimeError('Exact receipt drift')
 rows.append(dict(mode=mode,observed_outer_optimization=outer,returncode=p.returncode,receipt=receipt))
 print('Full replay '+mode+' observed '+str(outer)+' PASS',flush=True)
out=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',package_manifest_sha256=MAN,externally_pinned_verifier_sha256=PIN,cold_extraction=True,modes=rows)
(R/'COLD_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
