"""Replay actual archive without changing reviewed inputs."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,zipfile
R=Path(__file__).resolve().parent; A=R.parents[1]; P=A/'publication'; L=R/'own_local'; target=L/'archive'; target.mkdir(exist_ok=True)
build=json.loads((P/'BUILD_RECEIPT.json').read_text()); z=P/build['verification_zip']['path']
with zipfile.ZipFile(z) as archive:
    names=archive.namelist()
    if len(names)!=len(set(names)) or any(n.startswith('/') or '..' in Path(n).parts for n in names): raise RuntimeError('archive inventory unsafe')
    archive.extractall(target)
anchors=build['verification_anchors'];args=[x for k,v in anchors.items() for x in ['--expected-'+k+'-sha256',v]]
runs=[]
for flag in [[],['-O'],['-OO']]:
    env=dict(os.environ,TMPDIR=str(L),PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
    r=subprocess.run(['python3','-B',*flag,str(target/'verify.py'),*args],capture_output=True,text=True,env=env,timeout=180)
    (L/('verify'+(''.join(flag) or '-normal')+'.stdout')).write_text(r.stdout);(L/('verify'+(''.join(flag) or '-normal')+'.stderr')).write_text(r.stderr)
    if r.returncode:raise RuntimeError(r.stderr)
    runs.append({'mode':flag or ['normal'],'returncode':r.returncode,'result':json.loads(r.stdout)})
result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_zip':{'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'members':len(names)},'runs':runs,'scratch_only':True}
(R/'ARCHIVE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print({'archive_members':len(names),'modes':len(runs),'status':'PASS'})
