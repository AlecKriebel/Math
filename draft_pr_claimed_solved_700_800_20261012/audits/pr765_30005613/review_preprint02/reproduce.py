"""Run only in a disposable copy of this review; receipts are authored outputs."""
from pathlib import Path
import datetime, hashlib, importlib.util, io, json, os, shutil, stat, subprocess, sys, zipfile

HERE=Path(__file__).resolve().parent
PRE=HERE.parent/'preprint'
TMP=HERE/'tmp'
SRC=TMP/'source'
PDF=PRE/'output/pdf/paper.pdf'
PY312='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def require(v,m):
    if not v: raise RuntimeError(m)
def ident(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(n,v): (HERE/n).write_text(json.dumps(v,indent=2)+'\n')
def tree(p):
    if not p.exists() and not p.is_symlink(): return {}
    result={}
    paths=[p]+list(p.rglob('*')) if p.is_dir() and not p.is_symlink() else [p]
    for f in paths:
        s=f.lstat(); t=stat.S_IFMT(s.st_mode)
        result[str(f.relative_to(p))]=(t,os.readlink(f) if stat.S_ISLNK(s.st_mode) else ident(f.read_bytes()) if stat.S_ISREG(s.st_mode) else None)
    return result
def call(args,env=None):
    e=os.environ.copy();e.pop('PYTHONOPTIMIZE',None);e['PYTHONDONTWRITEBYTECODE']='1'
    if env:e.update(env)
    return subprocess.run(args,cwd='/',env=e,text=True,capture_output=True,timeout=180)
def extract():
    TMP.mkdir(exist_ok=True)
    if SRC.exists():shutil.rmtree(SRC)
    with zipfile.ZipFile(PRE/'source-and-verification.zip') as z:
        names=z.namelist();require(len(names)==len(set(names)),'duplicate zip')
        for i in z.infolist():
            require(not i.is_dir() and stat.S_ISREG(i.external_attr>>16),'zip not regular')
            require(not i.filename.startswith('/') and all(x not in ('','.','..') for x in i.filename.split('/')),'unsafe zip')
        z.extractall(SRC)
    return tree(SRC)
def main():
    
    for row in json.loads((HERE/'CHECKED_INPUTS.json').read_text())['files']:
        require(ident((PRE/row['path']).read_bytes())=={k:row[k] for k in ('bytes','sha256')},'Frozen publication input differs')
    before=extract(); rows=[]
    for label,py,flags,env in [('normal',sys.executable,[],{}),('outer_O',sys.executable,['-O'],{}),('env_OPT2',sys.executable,[],{'PYTHONOPTIMIZE':'2'}),('bundled312',PY312,[],{})]:
        r=call([py,*flags,'-B',str(SRC/'verify_bundle.py'),'--pdf',str(PDF)],env)
        require(r.returncode==0,label+r.stderr);data=json.loads(r.stdout)
        require(tree(SRC)==before,'changed source '+label)
        rows.append({'mode':label,'python':call([py,'--version']).stdout.strip(),'exit':r.returncode,'result':data,'source_unchanged':True})
    save('REPLAY_RECEIPT.json',{'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'modes':rows})
    rows=[]
    inv=json.loads((PRE/'PACKAGE_INVENTORY.json').read_text())
    for label,py,flags in [('normal',sys.executable,[]),('outer_O',sys.executable,['-O']),('bundled312',PY312,[])]:
        out=TMP/'rebuild'
        if out.exists():shutil.rmtree(out)
        r=call([py,*flags,'-B',str(SRC/'build_package.py'),'--output-dir',str(out),'--pdf',str(PDF)])
        require(r.returncode==0,r.stderr)
        comparisons=[]
        for row in inv['files']:
            b=(out/row['path']).read_bytes(); require(ident(b)=={k:row[k] for k in ('bytes','sha256')},'rebuild '+row['path'])
            comparisons.append({'path':row['path'],'byte_identical':True})
        z=zipfile.ZipFile(out/'zenodo-upload-kit.zip');require(set(z.namelist())=={'paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json','README.md'},'kit set')
        dep=json.loads(z.read('zenodo-deposit.json'));meta=json.loads(z.read('zenodo-metadata.json'))
        require(dep['metadata']==meta['metadata']==json.loads((out/'zenodo-deposit.json').read_bytes())['metadata'],'metadata mismatch')
        require(dep['files']==[{'path':'paper.pdf'},{'path':'source-and-verification.zip'}],'not 2 files')
        for f in ('paper.pdf','source-and-verification.zip'):
            require(z.read(f)==(PDF.read_bytes() if f=='paper.pdf' else (out/f).read_bytes()),'kit content')
        require(tree(SRC)==before,'source mutation')
        rows.append({'mode':label,'six_files':comparisons,'closed_source_unchanged':True,'kit_exact':True})
        shutil.rmtree(out)
    save('REBUILD_RECEIPT.json',{'runs':rows,'receipt_timestamp_excluded':True})
    snap=json.loads((SRC/'audit/SNAPSHOT.json').read_text()); comparisons=[]
    for row in snap['files']:
        actual=HERE.parent/'original'/row['path']
        relative=row['path'].split('attempts/30005613/',1)[1]
        b=(SRC/'historical_candidate'/relative).read_bytes()
        require(actual.read_bytes()==b,'actual original mismatch '+relative)
        require(ident(b)=={k:row[k] for k in ('bytes','sha256')},'snapshot mismatch')
        comparisons.append(relative)
    archives=[]
    for zp in sorted((SRC/'historical_candidate/archives').glob('*.zip')):
        with zipfile.ZipFile(zp) as z:
            members=[]
            for i in z.infolist():
                if i.is_dir():continue
                raw=z.read(i); matches=[p.relative_to(SRC/'historical_candidate').as_posix() for p in (SRC/'historical_candidate').rglob('*') if p.is_file() and p.suffix!='.zip' and p.read_bytes()==raw]
                require(matches,'unmatched ZIP payload '+i.filename);members.append({'member':i.filename,'identical_extracted_paths':matches})
            archives.append({'archive':zp.name,'members':members})
    require(len(archives)==3,'archive count');save('PRESERVATION_RECEIPT.json',{'original_count':len(comparisons),'actual_originals_compared':comparisons,'archives':archives})
    # Reuse the repaired root harness only after own first derivation; rebind every write path.
    spec=importlib.util.spec_from_file_location('root_guard',HERE/'root47_harness.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    attackroot=TMP/'root_harness';attackroot.mkdir();shutil.copy(PDF,attackroot/'paper.pdf');(attackroot/'output/pdf').mkdir(parents=True);shutil.copy(PDF,attackroot/'output/pdf/paper.pdf');shutil.copy(PRE/'source-and-verification.zip',attackroot/'source-and-verification.zip');(attackroot/'tmp').mkdir()
    mod.ROOT=attackroot;mod.SOURCE=SRC;mod.FIXTURE=TMP/'fixture';mod.OUTPUT=TMP/'attack-output'
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):mod.main()
    rootreceipt=json.loads((attackroot/'ROOT_GUARD_ATTACKS.json').read_text());save('ROOT47_INDEPENDENT_REPLAY.json',rootreceipt)
    # Extend beyond root47: all seven targets reject dirs/FIFOs, dangling links,
    # foreign hardlinks, plus parent FIFO/dangling/ordinary-file and root ancestors.
    extra=[]
    for name in ('paper.tex','output/pdf/paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json','zenodo-upload-kit.zip','PACKAGE_INVENTORY.json'):
        for kind in ('directory','fifo','dangling','foreign_hardlink'):
            def setup(src,out,n=name,k=kind):
                out.mkdir(); dest=out/n;dest.parent.mkdir(parents=True,exist_ok=True)
                if k=='directory':dest.mkdir()
                elif k=='fifo':os.mkfifo(dest)
                elif k=='dangling':dest.symlink_to(TMP/'does-not-exist')
                else:
                    (TMP/'foreign').write_bytes(b'foreign');os.link(TMP/'foreign',dest)
            extra.append(mod.run_case('extra_'+kind+'_'+name,lambda r:None,build=True,setup_output=setup))
            if (TMP/'foreign').exists():(TMP/'foreign').unlink()
    for kind in ('fifo','dangling','file','symlink_other'):
        def setup(src,out,k=kind):
            out.mkdir();dest=out/'output'
            if k=='fifo':os.mkfifo(dest)
            elif k=='dangling':dest.symlink_to(TMP/'absent-parent')
            elif k=='file':dest.write_bytes(b'sentinel')
            else:dest.symlink_to(TMP,target_is_directory=True)
        extra.append(mod.run_case('extra_parent_'+kind,lambda r:None,build=True,setup_output=setup))
    # Hidden file, invalid slash grammar, and independently repinned historical archive.
    extra.append(mod.run_case('extra_hidden',lambda r:(r/'.hidden').write_text('x')))
    for bad in ('a//b','./paper.tex','a/./b','a\\b',''):
        extra.append(mod.run_case('grammar_'+repr(bad),lambda r,b=bad:mod.edit_json(r,'MANIFEST.json',lambda m:m['files'][0].update(path=b))))
    extra.append(mod.run_case('repinned_original_archive',lambda r:mod.append(r,'historical_candidate/archives/QUASICONICAL_30005613_AUTHOR_SAFE_FREEZE.zip',True)))
    save('EXTRA_ATTACKS.json',{'count':len(extra),'cases':extra,'scope':'Every rejection checked before any source/output bytes changed; isolated copies only.'})
    if mod.FIXTURE.exists():shutil.rmtree(mod.FIXTURE)
    mod.remove_owned_output();shutil.rmtree(attackroot)
    # Comparator exact-type and near-zero boundaries independently exercised.
    sys.path.insert(0,str(SRC));spec=importlib.util.spec_from_file_location('vb',SRC/'verify_bundle.py');vb=importlib.util.module_from_spec(spec);spec.loader.exec_module(vb)
    cases=[('equal',1.0,1.0,True),('within_relative',1.,1.+5e-13,True),('beyond_relative',1.,1.+2e-12,False),('tiny_nonzero',0.,1e-300,False),('nan',float('nan'),float('nan'),False),('infinity',float('inf'),float('inf'),False),('int_float',1,1.,False),('bool_int',True,1,False),('keys',{'a':1},{'b':1},False),('length',[1],[1,2],False),('exact_count',4187,4188,False),('negative_near',-1.,-1.-5e-13,True)]
    cr=[]
    for label,a,b,want in cases:
        ok=True
        try:vb.compare_diagnostics(a,b)
        except ValueError:ok=False
        require(ok==want,'comparator '+label);cr.append({'case':label,'accepted':ok,'expected':want})
    save('COMPARATOR_RECEIPT.json',{'relative':1e-12,'absolute':0,'cases':cr})
    require(tree(SRC)==before,'final extracted mutation')
    print('PASS: four replays, three six-byte rebuilds, 39 originals, 3 archives, 47+39 rejections, comparator')
if __name__=='__main__':main()
