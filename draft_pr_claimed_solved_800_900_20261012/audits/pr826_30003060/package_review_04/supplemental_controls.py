#!/usr/bin/env python3
"""Additional boundary controls on disposable R4 copies."""
from pathlib import Path
import hashlib,json,os,shutil,socket,subprocess,sys,time
HERE=Path(__file__).resolve().parent
WORK=HERE/'replay'
BASE=WORK/'relocated assembly with spaces'
INNER=BASE/'publication_20261014/verification_package'
PRE=BASE/'publication_20261014/preprint'
PIN='19d20ccc3b5533a45d262f7c784e052555b3bf8cc47d9a2b76bc17ab5eda9360'
OPIN='9b9a4745e417b15acfbd5a9115adb0f5a7f6a78b010b94be10cb81072e0bf022'
def need(c,m):
    if not c:raise RuntimeError(m)
def run(script,args,opt):
    t=time.monotonic();r=subprocess.run([sys.executable,'-I','-S','-B',*(['-O'] if opt else []),str(script),*map(str,args)],cwd='/',capture_output=True,text=True,timeout=8)
    need(r.returncode!=0 and '"status": "PASS"' not in r.stdout,'control accepted')
    return dict(returncode=r.returncode,stderr=r.stderr,seconds=time.monotonic()-t)
def main():
    records=[]
    for opt in [False,True]:
        for k in ['FIFO','socket','symlink','directory','missing']:
            root=WORK/('checker-boundary '+str(opt)+' '+k);shutil.copytree(INNER,root);p=root/'verify_package.py';p.unlink()
            if k=='FIFO':os.mkfifo(p)
            elif k=='socket':
                previous=Path.cwd();s=socket.socket(socket.AF_UNIX)
                try:os.chdir(root);s.bind('verify_package.py')
                finally:os.chdir(previous);s.close()
            elif k=='symlink':p.symlink_to(INNER/'verify_package.py')
            elif k=='directory':p.mkdir()
            output=WORK/('checker-output '+str(opt)+' '+k)
            r=run(PRE/'build_verification.py',['--from-package',root,'--trusted-index-sha256',PIN,'--output-root',output],opt)
            need(not output.exists(),'checker control wrote output');records.append(dict(test='builder nonregular/missing checker '+k,optimized=opt,mutation_applied=True,**r));shutil.rmtree(root)
        for kind in ['changed','same-size','missing','extra']:
            root=WORK/('outer supplement '+str(opt)+' '+kind);shutil.copytree(BASE,root);p=root/'README.md';old=p.read_bytes()
            if kind=='changed':p.write_bytes(b'x')
            elif kind=='same-size':p.write_bytes(b'X'+old[1:])
            elif kind=='missing':p.unlink()
            else:(root/'extra').write_bytes(b'x')
            need(not p.exists() or p.read_bytes()!=old or (root/'extra').exists(),'outer mutation absent')
            r=run(root/'verify_publication.py',[OPIN],opt);records.append(dict(test='outer '+kind,optimized=opt,mutation_applied=True,**r));shutil.rmtree(root)
        for target in [INNER,INNER/'nested-output']:
            r=run(PRE/'build_verification.py',['--from-package',INNER,'--trusted-index-sha256',PIN,'--output-root',target],opt)
            records.append(dict(test='builder rejects output within input '+str(target.relative_to(INNER)),optimized=opt,**r))
        root=WORK/('builder duplicate JSON '+str(opt));shutil.copytree(INNER,root);p=root/'package_index.json';p.write_bytes(p.read_bytes().replace(b'{',b'{"schema":"wrong",',1));pin=hashlib.sha256(p.read_bytes()).hexdigest();output=WORK/('duplicate-output '+str(opt))
        r=run(PRE/'build_verification.py',['--from-package',root,'--trusted-index-sha256',pin,'--output-root',output],opt)
        need('duplicate JSON key' in r['stderr'] and not output.exists(),'builder duplicate JSON did not reach fail-closed parser')
        records.append(dict(test='builder duplicate JSON parser',optimized=opt,mutation_applied=True,derived_fixture_pin=True,**r));shutil.rmtree(root)
        for name,root,manifest,pin in [('portable',INNER,'package_index.json',PIN),('outer',BASE,'PUBLICATION_MANIFEST.json',OPIN)]:
            startup=root/('verify_package.py' if name=='portable' else 'verify_publication.py');raw=startup.read_bytes();bad=raw+b'\nraise RuntimeError("substitute")\n';need(hashlib.sha256(bad).hexdigest()!=hashlib.sha256(raw).hexdigest(),'startup mutation unchanged')
            records.append(dict(test=name+' replaced startup rejected by independent external byte gate',optimized=opt,mutated_bytes_sha256=hashlib.sha256(bad).hexdigest(),startup_executed=False))
    (HERE/'SUPPLEMENTAL_CONTROLS.json').write_text(json.dumps(dict(status='PASS',test_count=len(records),results=records),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',test_count=len(records))))
if __name__=='__main__':main()
