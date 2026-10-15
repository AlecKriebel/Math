#!/usr/bin/env python3
"""Review driver: execute only inspected tools in disposable relocated layouts."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os, shutil, stat, subprocess, sys, time, zipfile

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ASSEMBLY=AUDIT.parents[1]/'work/pr822_revision_r2'
INDEX='b3ac480b710b4a2a6ac8fb438b09697357e0796fe879d614afb54429c10aa374'
OUTER='ab68f85b25ce12369da8eb0d818d10edb55b2d835d23ba098b99583a9ef83e9c'
ZIP='06cb9c3018eff4ab2e2654e56cee8f302672a8f05ffe4dce0b2d7c78c4fa1d0a'

def need(ok,label):
    if not ok: raise RuntimeError(label)

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(root):
    out=[]
    for p in sorted(root.rglob('*')):
        mode=p.lstat().st_mode
        need(stat.S_ISDIR(mode) or stat.S_ISREG(mode),'nonregular replay inventory')
        out.append({'path':p.relative_to(root).as_posix(),'kind':'dir' if p.is_dir() else 'file',
                    **({} if p.is_dir() else {'bytes':p.stat().st_size,'sha256':digest(p)})})
    return out

def main():
    raw=HERE/'private_sources'
    scratch=raw/'relocated published review with spaces'
    need(not scratch.exists(),'fresh review scratch required')
    scratch.mkdir()
    tmp=raw/'disposable tool temporary directories'; tmp.mkdir(exist_ok=True)
    env=dict(os.environ,TMPDIR=str(tmp))
    copied=scratch/'intact published assembly with spaces'
    shutil.copytree(ASSEMBLY,copied)
    outer_before=inventory(copied)
    pre=copied/'publication_20261013/preprint'
    arc=pre/'verification.zip'
    need(digest(arc)==ZIP,'current ZIP pin')
    extracted=scratch/'standalone verification extracted with spaces'; extracted.mkdir()
    with zipfile.ZipFile(arc) as z:
        infos=z.infolist(); names=[i.filename for i in infos]
        need(len(names)==len(set(names))==110,'current ZIP inventory')
        for i in infos:
            n=PurePosixPath(i.filename)
            need(not n.is_absolute() and '..' not in n.parts and str(n)==i.filename and stat.S_ISREG(i.external_attr>>16),'safe ZIP member')
            dest=extracted/n; dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(i))
    inner_before=inventory(extracted)
    records=[]
    def run(label,argv,cwd):
        t=time.monotonic()
        p=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True,timeout=900)
        (raw/(label+'.stdout')).write_text(p.stdout)
        (raw/(label+'.stderr')).write_text(p.stderr)
        row={'label':label,'command':argv,'cwd':str(cwd),'returncode':p.returncode,
             'seconds':round(time.monotonic()-t,3),'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),
             'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest(),
             'stdout_path':'private_sources/'+label+'.stdout','stderr_path':'private_sources/'+label+'.stderr'}
        if p.returncode==0:
            row['result']=json.loads(p.stdout)
        records.append(row)
        (HERE/'REPLAY_RECEIPTS.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':records},indent=2)+'\n')
        print(label,p.returncode,round(time.monotonic()-t,2),flush=True)
        need(p.returncode==0 and not p.stderr,'replay failure: '+label+' '+p.stderr[-3000:])
    for optimized in (False,True):
        flags=['-I','-B']+(['-O'] if optimized else [])
        suffix='optimized' if optimized else 'normal'
        run('portable_full_'+suffix,[sys.executable,*flags,str(extracted/'verify_package.py'),INDEX,'--full'],Path('/'))
        run('outer_full_'+suffix,[sys.executable,*flags,str(copied/'verify_publication.py'),OUTER,'--full'],Path('/'))
        run('published_builder_'+suffix,[sys.executable,*flags,'build_verification.py','--from-package','../verification_package','--trusted-index-sha256',INDEX,'--output-root',str(scratch/('fresh rebuilt '+suffix+' with spaces'))],pre)
        built=scratch/('fresh rebuilt '+suffix+' with spaces')
        need(digest(built/'package_index.json')==INDEX and digest(built/'verification.zip')==ZIP,'deterministic rebuilt identity')
    run('current_outer_controls',[sys.executable,'-I','-B',str(copied/'package_controls.py'),OUTER],Path('/'))
    run('independent_arithmetic_normal',[sys.executable,'-I','-B',str(HERE/'independent_arithmetic.py')],Path('/'))
    run('independent_arithmetic_optimized',[sys.executable,'-I','-B','-O',str(HERE/'independent_arithmetic.py')],Path('/'))
    need(outer_before==inventory(copied),'outer before/after changed')
    need(inner_before==inventory(extracted),'inner before/after changed')
    (HERE/'REPLAY_INVENTORY_RECEIPT.json').write_text(json.dumps({'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'outer_before':outer_before,'outer_after':inventory(copied),'portable_before':inner_before,'portable_after':inventory(extracted),
        'outer_before_after_equal':True,'portable_before_after_equal':True,'retained_relocated_layout':str(scratch)},indent=2)+'\n')

if __name__=='__main__':main()
