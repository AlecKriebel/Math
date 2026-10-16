#!/usr/bin/env python3
"""Fresh review02; disposable extraction only; no canonical writes."""
import hashlib, io, json, os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[1]
PACKAGE=AUDIT/'NEWpreprint_v1_0'
WORKSPACE=AUDIT.parents[2]
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes(); return {'bytes':len(b),'sha256':sha(b)}
def tree(p):
    return {str(q.relative_to(p)):pin(q) for q in p.rglob('*') if q.is_file() and not q.is_symlink()}
def record_json(name,value): (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
COMMANDS=[]
def command(argv,cwd,want=True,label=''):
    p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True)
    row={'label':label,'argv':[str(x) for x in argv],'returncode':p.returncode,
         'expected_success':want,'stdout':p.stdout,'stderr':p.stderr}
    COMMANDS.append(row)
    need((p.returncode==0)==want,'Unexpected command: '+label+' '+p.stderr[-1500:])
    return p

def main():
    manifest=json.loads((PACKAGE/'PACKAGE_MANIFEST.json').read_text())
    archive=PACKAGE/'PR1071_preprint_v1_0_support.zip'
    names=sorted([x['path'] for x in manifest['members']]+['PACKAGE_MANIFEST.json'])
    with zipfile.ZipFile(archive) as z:
        need(z.namelist()==names and z.testzip() is None,'ZIP names/CRC')
        for info in z.infolist():
            need(z.read(info.filename)==(PACKAGE/info.filename).read_bytes(),'ZIP payload')
            need(info.compress_type==zipfile.ZIP_STORED and info.create_system==3 and info.date_time==(2026,10,14,0,0,0) and info.external_attr==(0o100644<<16),'ZIP attributes')
    memory=io.BytesIO()
    with zipfile.ZipFile(memory,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
        for name in names:
            info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED
            z.writestr(info,(PACKAGE/name).read_bytes())
    need(memory.getvalue()==archive.read_bytes(),'Independent CLOSED ZIP differs')
    metadata=json.loads((PACKAGE/'metadata.json').read_text())
    native=json.loads((AUDIT/'publication/zenodo-deposit.json').read_text())
    need(set(native)=={'metadata','files'} and native['metadata']==metadata,'Native metadata mismatch')
    need(metadata==json.loads((PACKAGE/'metadata_wrapped.json').read_text())['metadata']==json.loads((PACKAGE/'deposit.json').read_text())['metadata'],'Metadata mismatch')
    need([x['name'] for x in native['files']]==['paper.pdf',archive.name],'Upload names')
    for item in native['files']:
        need((AUDIT/'publication'/item['path']).resolve()==(PACKAGE/item['name']).resolve(),'Upload path')
    tool=WORKSPACE/'zenodo_deposit_tool/zenodo.py'
    need(tool.is_file(),'Repository uploader path')
    command([sys.executable,'-B',str(tool),'check',str(AUDIT/'publication/zenodo-deposit.json')],WORKSPACE,label='Repository LOCAL native manifest check')
    receipt={'zip':pin(archive),'pdf':pin(PACKAGE/'paper.pdf'),'tex':pin(PACKAGE/'paper.tex'),
             'archive_members':len(names),'independent_closed_zip_equal':True,
             'metadata_three_objects_and_native_equal':True,'native_assets_exact':True,
             'bootstrap_and_writer_cases':[]}
    with tempfile.TemporaryDirectory(prefix='scratch-review02-',dir=HERE) as temp:
        base=Path(temp); clean=base/'clean'
        with zipfile.ZipFile(archive) as z: z.extractall(clean)
        initial=tree(clean)
        def restore(rel,data):
            p=clean/rel
            if p.is_symlink() or p.exists():
                if p.is_dir() and not p.is_symlink(): shutil.rmtree(p)
                else:p.unlink()
            p.write_bytes(data)
        for optimized,flags in [(False,[]),(True,['-O'])]:
            mode='optimized' if optimized else 'normal'
            py=[sys.executable,'-B',*flags]
            command([*py,'scripts/verify_package.py'],clean,label=mode+' default clean absent binding')
            command([*py,'scripts/check.py','--out',str(base/('checks-'+mode))],clean,label=mode+' actual documented original checker replay')
            shutil.copyfile(base/('checks-'+mode)/'CHECK_RECEIPT.json',HERE/('DOCUMENTED_CHECK_'+mode+'.json'))
            command([*py,'scripts/build_archive.py','--out',str(base/('rebuilt-'+mode+'.zip'))],clean,label=mode+' documented archive build')
            need((base/('rebuilt-'+mode+'.zip')).read_bytes()==archive.read_bytes(),'Documented rebuild bytes')
            command([*py,'scripts/verify_package.py','--require-bindings','--bindings',str(PACKAGE/'UPLOAD_BINDINGS.json'),'--archive',str(base/('rebuilt-'+mode+'.zip'))],clean,label=mode+' strict external bindings')
            command([*py,'scripts/verify_package.py','--require-bindings'],clean,False,mode+' missing required binding')
            command([*py,'scripts/build_pdf.py','--out',str(base/('compiled-'+mode))],clean,label=mode+' REAL documented Tectonic compile')
            pdf=base/('compiled-'+mode)/'paper.pdf'
            need(pdf.read_bytes()==(PACKAGE/'paper.pdf').read_bytes(),'Clean PDF differs')
            for n in ['compile.stdout.txt','compile.stderr.txt']:
                shutil.copyfile(base/('compiled-'+mode)/n,HERE/(mode+'_'+n))
            need(tree(clean)==initial,'Clean documented commands mutated extraction')

            # New outputs only: every writer must reject BEFORE compiler or copy.
            for writer in ['build_archive.py','check.py','build_pdf.py']:
                target=clean/'paper.tex'; target_before=pin(target)
                hard=base/('hard-'+mode+'-'+writer);os.link(target,hard)
                sym=base/('sym-'+mode+'-'+writer);sym.symlink_to(target)
                dangling=base/('dangling-'+mode+'-'+writer);dangling.symlink_to(base/'missing-target')
                existing=base/('existing-'+mode+'-'+writer);existing.mkdir()
                extfile=base/('file-'+mode+'-'+writer);extfile.write_text('untouched')
                linkparent=base/('linkparent-'+mode+'-'+writer);linkparent.symlink_to(clean/'custody',target_is_directory=True)
                cases=[('nested protected descendant',clean/'custody'/'new-forbidden'),('hardlink',hard),('symlink',sym),('dangling symlink',dangling),('existing directory',existing),('existing file',extfile),('symlink ancestor',linkparent/'new-output'),('missing parent',base/'missing-parent'/'new-output')]
                for label,out in cases:
                    argv=[*py,'scripts/'+writer,'--out',str(out)]
                    if writer=='build_pdf.py':argv+=['--tectonic',str(base/'MUST_NOT_EXECUTE')]
                    p=command(argv,clean,False,mode+' '+writer+' '+label)
                    need('FileNotFoundError' not in p.stderr,'Compiler invoked before preflight')
                    need(pin(target)==target_before,'Writer mutated protected hardlink target')
                    receipt['bootstrap_and_writer_cases'].append({'mode':mode,'writer':writer,'case':label,'rejected':True,'protected_preserved':True})
                hard.unlink();sym.unlink();dangling.unlink();existing.rmdir();extfile.unlink();linkparent.unlink()
            # Test manifest leaf-kind before JSON load, plus ancestor-kind.
            original=(clean/'PACKAGE_MANIFEST.json').read_bytes()
            outside=base/('manifest-'+mode+'.json');outside.write_bytes(original)
            (clean/'PACKAGE_MANIFEST.json').unlink();(clean/'PACKAGE_MANIFEST.json').symlink_to(outside)
            for writer,more in [('verify_package.py',[]),('build_archive.py',['--out',str(base/('must-not-create-'+mode+'.zip'))])]:
                p=command([*py,'scripts/'+writer,*more],clean,False,mode+' manifest symlink '+writer)
                need('Symlink member/ancestor' in p.stderr,'Bootstrap did not reject before parse')
            restore('PACKAGE_MANIFEST.json',original)
            held=base/('held-custody-'+mode);(clean/'custody').rename(held);(clean/'custody').symlink_to(held,target_is_directory=True)
            command([*py,'scripts/verify_package.py'],clean,False,mode+' payload symlink ancestor')
            (clean/'custody').unlink();held.rename(clean/'custody')
            # Present strict binding faults, including a changed PDF, must fail.
            good=json.loads((PACKAGE/'UPLOAD_BINDINGS.json').read_text())
            binding=base/('binding-'+mode+'.json');binding.write_text(json.dumps(good))
            command([*py,'scripts/verify_package.py','--bindings',str(binding)],clean,False,mode+' present binding missing ZIP')
            good['pdf']['sha256']='0'*64;binding.write_text(json.dumps(good))
            command([*py,'scripts/verify_package.py','--bindings',str(binding),'--archive',str(archive)],clean,False,mode+' present corrupt PDF binding')
            # Exercise semantic plain-citation parser independently of member SHA.
            citation=(clean/'CITATION.txt').read_bytes()
            (clean/'CITATION.txt').write_bytes(citation.replace(b'Version: 1.0',b'Version: 9.9'))
            code="import sys;sys.dont_write_bytecode=True;sys.path.insert(0,'scripts');import verify_package,json;verify_package.validate_citation(verify_package.ROOT,json.loads((verify_package.ROOT/'metadata.json').read_text()))"
            command([*py,'-c',code],clean,False,mode+' plain citation semantic version mismatch')
            restore('CITATION.txt',citation)
            command([*py,'scripts/verify_package.py'],clean,label=mode+' restored clean verification')
            need(tree(clean)==initial,'Fault suite failed to restore exact extraction')
        receipt['clean_extraction_unchanged']=True
        receipt['real_pdf_byte_identical_both_modes']=True
    record_json('REPRODUCTION_AND_ATTACKS.json',{'summary':receipt,'commands':COMMANDS})
    print(json.dumps({'commands':len(COMMANDS),'writer_rejections':len(receipt['bootstrap_and_writer_cases']),'archive_members':len(names),'pdf_reproduced':True,'native_check':True,'all_outcomes_expected':True},indent=2))
if __name__=='__main__':main()
