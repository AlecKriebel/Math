#!/usr/bin/env python3
"""Public derivative controls for unchanged finite checkers; not original-bundle replay."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate JSON key');out[k]=v
    return out
def parse(b):
    return json.loads(b,object_pairs_hook=unique,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('nonfinite')))
def same(a,b):
    if type(a) is not type(b):return False
    if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
    if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def main():
    need(len(sys.argv)==2,'one packet path required')
    root=Path(sys.argv[1])
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    names=['CERTIFICATE.json','verify.py','independent_verify.py']
    source={n:(root/n).read_bytes() for n in names}
    base=parse(source['CERTIFICATE.json'])
    mutations = []
    def change(name, fun):
        c = copy.deepcopy(base); fun(c); mutations.append((name,json.dumps(c)))
    change('missing-generator',lambda c:c.pop('joint_generator'))
    change('extra-key',lambda c:c.update(unclaimed=0))
    change('schema-bool',lambda c:c.update(schema=True))
    change('schema-float',lambda c:c.update(schema=1.0))
    change('weight-bool',lambda c:c['weights'].__setitem__(0,True))
    change('weight-float',lambda c:c['weights'].__setitem__(0,1.0))
    change('weight-zero',lambda c:c['weights'].__setitem__(0,0))
    change('weight-repeat',lambda c:c['weights'].__setitem__(0,2))
    change('weight-overflow',lambda c:c['weights'].__setitem__(0,101))
    change('marginal-conservation',lambda c:c['marginal_generator'][0].__setitem__(0,-4))
    change('marginal-asymmetry',lambda c:c['marginal_generator'][1].__setitem__(0,2))
    change('joint-conservation',lambda c:c['joint_generator'][1].__setitem__(1,-7))
    change('joint-lumpability',lambda c:c['joint_generator'][0].__setitem__(1,4))
    change('joint-negative-rate',lambda c:c['joint_generator'][0].__setitem__(3,-1))
    change('joint-float',lambda c:c['joint_generator'][0].__setitem__(0,-6.0))
    change('joint-dimension',lambda c:c['joint_generator'].pop())
    change('state-bool',lambda c:c['states'][0].__setitem__(0,False))
    change('state-duplicate',lambda c:c['states'].__setitem__(1,[0,1]))
    change('false-automorphism',lambda c:c.update(automorphisms=[[1,2,0]]))
    change('automorphism-bool',lambda c:c['automorphisms'][0].__setitem__(0,False))
    change('product-nonrigid',lambda c:c['product_map'][0].__setitem__(0,-2))
    change('covariance-trace',lambda c:c['difference_covariance'][1].__setitem__(1,0))
    change('noise-identity',lambda c:c.update(perverse_J=[[1,0],[0,1]]))
    mutations += [('duplicate-json','{"schema":1,"schema":1}'),('nan','{"schema":NaN}'),
                  ('truncated','{'),('trailing',json.dumps(base)+'x'),('top-level-list','[]'),
                  ('oversize',' '*16385)]
    modes=[]
    with tempfile.TemporaryDirectory(prefix='public-shy-math-') as tmp:
        temp=Path(tmp);ro=temp/'readonly';ro.mkdir();hostile=temp/'hostile';hostile.mkdir()
        for n,b in source.items():(ro/n).write_bytes(b)
        marker=temp/'HOSTILE_EXECUTED'
        for name in ['json','itertools','fractions','pathlib','hashlib','sitecustomize','usercustomize']:
            (hostile/(name+'.py')).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\nraise RuntimeError("hostile import")\n')
        for d in [ro,hostile]:
            for f in d.iterdir():f.chmod(0o444)
            d.chmod(0o555)
        env=dict(PATH=os.defpath,HOME=str(temp),TMPDIR=str(temp),LC_ALL='C',PYTHONPATH=str(hostile),PYTHONHOME='/nonexistent-hostile-home',PYTHONSTARTUP=str(hostile/'sitecustomize.py'))
        def execute(script,path,flags):
            q=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(ro/script),str(path)],cwd=hostile,env=env,capture_output=True,timeout=20)
            return dict(exit_code=q.returncode,stdout=q.stdout.decode(),stderr=q.stderr.decode(),stdout_bytes=len(q.stdout),stdout_sha256=sha(q.stdout),stderr_bytes=len(q.stderr),stderr_sha256=sha(q.stderr))
        try:
            for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
                probes=[]
                for d in [ro,hostile]:
                    for f in [d,*sorted(d.iterdir())]:
                        directory=f.is_dir();need((f.stat().st_mode&0o777)==(0o555 if directory else 0o444) and not os.access(f,os.W_OK),'readonly mode')
                        try:fd=os.open(f/'FORBIDDEN' if directory else f,os.O_WRONLY|(os.O_CREAT|os.O_EXCL if directory else 0),0o600)
                        except PermissionError as e:
                            need(e.errno==13,'write-denial errno');probes.append(dict(path=f.relative_to(temp).as_posix(),operation='create' if directory else 'write_open',errno=e.errno,denied=True))
                        else:os.close(fd);raise ValueError('write-open succeeded')
                runs=[]
                for script in ['verify.py','independent_verify.py']:
                    positive=execute(script,ro/'CERTIFICATE.json',flags)
                    need(positive['exit_code']==0 and positive['stderr']=='','positive execution')
                    result=parse(positive['stdout']);need(result.get('verified') is True,'positive claim')
                    negatives=[]
                    for label,body in mutations:
                        bad=temp/'mutant.json';bad.write_text(body);r=execute(script,bad,flags)
                        need(r['exit_code']==2 and r['stderr']=='','clean rejection '+label)
                        answer=parse(r['stdout']);need(type(answer) is dict and set(answer)=={'verified','error'} and answer['verified'] is False and type(answer['error']) is str,'negative schema '+label)
                        r['case']=label;negatives.append(r)
                    runs.append(dict(checker=script,positive=positive,negative_count=len(negatives),negatives=negatives))
                modes.append(dict(mode=mode,uid=os.getuid(),euid=os.geteuid(),write_probes=probes,runs=runs))
            for i in [1,2]:
                need(same(modes[0]['runs'],modes[i]['runs']),'typed mode result difference')
            need(not marker.exists(),'hostile import executed')
            need(source=={n:(ro/n).read_bytes() for n in names},'math input changed')
        finally:
            for d in [ro,hostile]:
                d.chmod(0o755)
                for f in d.iterdir():f.chmod(0o644)
    need(source=={n:(root/n).read_bytes() for n in names},'public input changed')
    return dict(schema=1,problem_id=9500007,status='PASS',scope='Public derivative finite-algebra replay only; original complete bundle replay NOT_RUN.',uid=os.getuid(),euid=os.geteuid(),modes=modes,positive_acceptances=6,negative_rejections=174,hostile_import_executed=False,inputs_unchanged=True)

if __name__=='__main__':
    try:print(json.dumps(main(),sort_keys=True))
    except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
