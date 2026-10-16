"""Package 03 independent complete replay and adversarial interface checks.

Only this review folder is written. Every candidate mutation below is confined
to our disposable extraction, restored after the check. No network/service calls.
"""
import sys
sys.dont_write_bytecode = True
import os, json, hashlib, zipfile, subprocess, shutil, datetime, stat, zlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[1]
KIT=AUDIT/'NEWpreprint_v1_0'
WORK=HERE/'scratch'
WORK.mkdir(exist_ok=True)
RECEIPTS=[]
def require(ok, msg):
    if not ok: raise RuntimeError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def run(label,args,success=True,cwd=None,contains=None):
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    p=subprocess.run([str(x) for x in args],cwd=cwd or WORK,env=env,capture_output=True,text=True)
    row={'label':label,'args':[str(x) for x in args],'cwd':str(cwd or WORK),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expected_success':success}
    RECEIPTS.append(row);save('COMMAND_RECEIPTS.json',RECEIPTS)
    require((p.returncode==0)==success,label+' exit mismatch')
    if contains:require(contains in p.stdout+p.stderr,label+' diagnostic mismatch')
    return p
def main():
    clean=WORK/'CleanPackage'
    require(not clean.exists(),'scratch must be fresh')
    archive=KIT/'PR1071_preprint_v1_0_support.zip'
    run('stdlib-clean-extraction',[sys.executable,'-m','zipfile','-e',archive,clean])
    bindings=WORK/'bindings.json';shutil.copyfile(KIT/'UPLOAD_BINDINGS.json',bindings)
    for flags,label in [([], 'normal'),(['-O'],'optimized')]:
        py=[sys.executable,*flags]
        run('clean-optional-absent-'+label,[*py,clean/'scripts/verify_package.py'])
        run('current-strict-present-'+label,[*py,KIT/'scripts/verify_package.py'])
        run('clean-explicit-valid-binding-'+label,[*py,clean/'scripts/verify_package.py','--require-bindings','--bindings',bindings,'--archive',archive])
        run('clean-required-absent-'+label,[*py,clean/'scripts/verify_package.py','--require-bindings'],False,contains='Required bindings are absent')
        run('clean-explicit-missing-optional-'+label,[*py,clean/'scripts/verify_package.py','--bindings',WORK/'missing-bindings.json'])
        run('clean-explicit-missing-required-'+label,[*py,clean/'scripts/verify_package.py','--require-bindings','--bindings',WORK/'missing-bindings.json'],False)
        run('binding-valid-but-missing-archive-'+label,[*py,clean/'scripts/verify_package.py','--bindings',bindings,'--archive',WORK/'missing.zip'],False)
        malformed=WORK/'malformed-binding.json';malformed.write_text('{broken')
        run('malformed-binding-'+label,[*py,clean/'scripts/verify_package.py','--bindings',malformed],False)
        corrupt=json.loads(bindings.read_text());corrupt['pdf']['sha256']='0'*64
        bad=WORK/'corrupt-binding.json';bad.write_text(json.dumps(corrupt))
        run('corrupt-pdf-binding-'+label,[*py,clean/'scripts/verify_package.py','--bindings',bad,'--archive',archive],False)
        corrupt=json.loads(bindings.read_text());corrupt['manifest_sha256']='0'*64;bad.write_text(json.dumps(corrupt))
        run('corrupt-manifest-binding-'+label,[*py,clean/'scripts/verify_package.py','--bindings',bad,'--archive',archive],False)
        corrupt=json.loads(bindings.read_text());corrupt['archive']['sha256']='0'*64;bad.write_text(json.dumps(corrupt))
        run('corrupt-archive-binding-'+label,[*py,clean/'scripts/verify_package.py','--bindings',bad,'--archive',archive],False)
        link=WORK/'binding-link.json';link.symlink_to(bindings)
        run('binding-symlink-'+label,[*py,clean/'scripts/verify_package.py','--bindings',link],False)
        link.unlink()
        run('checker-full-wrapper-'+label,[*py,clean/'scripts/check.py','--out',WORK/('checker-'+label)])
        run('archive-supported-'+label,[*py,clean/'scripts/build_archive.py','--out',WORK/('rebuilt-'+label+'.zip')])
        require((WORK/('rebuilt-'+label+'.zip')).read_bytes()==archive.read_bytes(),'Rebuilt zip unequal')
    # Independent closed ZIP reconstruction, including CRC/header attributes.
    manifest=json.loads((clean/'PACKAGE_MANIFEST.json').read_text())
    names=sorted([r['path'] for r in manifest['members']]+['PACKAGE_MANIFEST.json'])
    closed=WORK/'closed-independent.zip'
    with zipfile.ZipFile(closed,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
        for name in names:
            i=zipfile.ZipInfo(name,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED
            z.writestr(i,(clean/name).read_bytes())
    require(closed.read_bytes()==archive.read_bytes(),'Independent CLOSED zip differs')
    ziprows=[]
    with zipfile.ZipFile(archive) as z:
        require(z.namelist()==names and z.testzip() is None,'closed ZIP member/CRC issue')
        for i in z.infolist():
            data=(clean/i.filename).read_bytes()
            require(z.read(i)==data and i.CRC==zlib.crc32(data),'ZIP payload/CRC mismatch')
            require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.compress_type==0 and i.external_attr==0o100644<<16,'ZIP headers mismatch')
            ziprows.append({'path':i.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'crc32':f'{i.CRC:08x}','fixed_headers_checked':True})
    save('CLOSED_ZIP.json',{'members':ziprows,'independent_rebuild':pin(closed),'byte_equal':True})
    # Bootstrap member preflight before JSON parsing: invalid link body is deliberate.
    mp=clean/'PACKAGE_MANIFEST.json';mb=mp.read_bytes()
    malformed=WORK/'not-json';malformed.write_text('not json')
    for flags,label in [([], 'normal'),(['-O'],'optimized')]:
        mp.unlink();mp.symlink_to(malformed)
        run('bootstrap-manifest-symlink-before-parse-'+label,[sys.executable,*flags,clean/'scripts/verify_package.py'],False,contains='Symlink member/ancestor')
        mp.unlink();mp.mkdir()
        run('bootstrap-manifest-directory-before-parse-'+label,[sys.executable,*flags,clean/'scripts/verify_package.py'],False,contains='Nonregular member')
        mp.rmdir();mp.write_bytes(mb)
        member=clean/'checks/original_expected.json';body=member.read_bytes();member.unlink();member.symlink_to(malformed)
        run('member-symlink-'+label,[sys.executable,*flags,clean/'scripts/verify_package.py'],False,contains='Symlink member/ancestor')
        member.unlink();member.write_bytes(body)
        folder=clean/'checks';saved=clean/'checks-saved';folder.rename(saved);folder.symlink_to(saved,target_is_directory=True)
        run('member-ancestor-symlink-'+label,[sys.executable,*flags,clean/'scripts/verify_package.py'],False,contains='Symlink member/ancestor')
        folder.unlink();saved.rename(folder)
    # Real physical case-alias premises; no canonical candidate alias requested.
    alias=clean.with_name(clean.name.swapcase())
    require(alias.exists() and alias.samefile(clean),'physical case-alias premise unavailable')
    nested=clean/'ExistingNested';nested.mkdir()
    aliasnested=alias/'existingnested'
    require(aliasnested.samefile(nested),'nested case premise failed')
    external=WORK/'ExternalCase';external.mkdir();externalalias=WORK/'eXTERNALcASE'
    require(externalalias.samefile(external),'normal external case premise failed')
    compiler=WORK/'compiler-sentinel.py';sentinel=WORK/'COMPILER_WAS_RUN'
    compiler.write_text('#!'+sys.executable+'\nfrom pathlib import Path\nPath('+repr(str(sentinel))+').write_text("ran")\nraise SystemExit(97)\n');compiler.chmod(0o755)
    symlinkparent=WORK/'link-parent';symlinkparent.symlink_to(external,target_is_directory=True)
    ancestorlink=WORK/'ancestor-link';ancestorlink.symlink_to(WORK,target_is_directory=True)
    pathcases=[
        ('root-canonical-target-alias',clean,alias/'NeverWrite'),
        ('root-alias-target-canonical',alias,clean/'NeverWrite'),
        ('nested-existing-case',clean,aliasnested/'NeverWrite'),
        ('absent-multilevel-case',clean,alias/'MissingA'/'MissingB'/'NeverWrite'),
        ('reverse-absent-multilevel-case',alias,clean/'MissingA'/'MissingB'/'NeverWrite'),
        ('lexical-internal',clean,clean/'NoWrite'),
        ('traversal-collapse-external',clean,external/'..'/'NeverWrite'),
        ('symlink-parent',clean,symlinkparent/'NeverWrite'),
        ('symlink-ancestor',clean,ancestorlink/external.name/'NeverWrite'),
        ('absent-external-parent',clean,WORK/'AbsentA'/'AbsentB'/'NeverWrite'),
    ]
    existing=WORK/'existing-file';existing.write_text('unchanged')
    existingdir=WORK/'existing-dir';existingdir.mkdir()
    hard=WORK/'hardlink-paper';os.link(clean/'paper.pdf',hard)
    link=WORK/'leaf-link';link.symlink_to(existing)
    dangling=WORK/'dangling-leaf';dangling.symlink_to(WORK/'missing-target')
    for name,p in [('existing-file',existing),('existing-dir',existingdir),('hardlink-leaf',hard),('symlink-leaf',link),('dangling-leaf',dangling)]:pathcases.append((name,clean,p))
    probes=[]
    for flags,label in [([], 'normal'),(['-O'],'optimized')]:
        for script in ['build_archive.py','check.py','build_pdf.py']:
            for name,scriptroot,target in pathcases:
                args=[sys.executable,*flags,scriptroot/'scripts'/script,'--out',target]
                if script=='build_pdf.py':args+=['--tectonic',compiler]
                was=target.exists() or target.is_symlink();before=sha(target) if target.is_file() and not target.is_symlink() else None
                run(script+'-'+name+'-'+label,args,False)
                require(not sentinel.exists(),'compiler ran on rejected output')
                require((target.exists() or target.is_symlink())==was,'rejected writer created output')
                if before:require(sha(target)==before,'existing leaf mutated')
                probes.append({'script':script,'mode':label,'case':name,'output':str(target),'rejected_before_output_and_compiler':True})
            # Positive external alias output really executes each writer.
            dest=externalalias/(script.replace('.py','')+'-'+label)
            args=[sys.executable,*flags,clean/'scripts'/script,'--out',dest]
            if script=='build_pdf.py':
                args+=['--tectonic',compiler];run(script+'-external-case-positive-'+label,args,False)
                require(sentinel.exists() and dest.is_dir(),'external compiler positive did not reach sentinel')
                sentinel.unlink()
            else:run(script+'-external-case-positive-'+label,args)
            probes.append({'script':script,'mode':label,'case':'external-case-positive','output':str(dest),'reached_writer':True})
    save('FILESYSTEM_PROBES.json',{'static_local_only':True,'physical_clean_alias_samefile':True,'physical_nested_alias_samefile':True,'physical_external_alias_samefile':True,'probes':probes})
    run('clean-readonly-verification-after-controls',[sys.executable,clean/'scripts/verify_package.py'])
    run('actual-native-local-check',[sys.executable,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',AUDIT/'publication/zenodo-deposit.json'])
    # Actual standalone compile is reproduction of unchanged source, read-only review.
    run('actual-pdf-compile',[sys.executable,clean/'scripts/build_pdf.py','--out',WORK/'pdf-rebuild'],cwd=WORK)
    require((WORK/'pdf-rebuild/paper.pdf').read_bytes()==(KIT/'paper.pdf').read_bytes(),'PDF reproduction differs')
    run('all-seven-pages-render',['pdftoppm','-scale-to','1600','-png',KIT/'paper.pdf',WORK/'paper-page'])
    pages=sorted(WORK.glob('paper-page-*.png'));require(len(pages)==7,'seven page render failed')
    save('PDF_REPRODUCTION.json',{'original':pin(KIT/'paper.pdf'),'recompiled':pin(WORK/'pdf-rebuild/paper.pdf'),'byte_equal':True,'pages':[pin(x) for x in pages],'visual_review_pending':True,'marker_not_run':'Read-only reproduction of unchanged paper; no create/edit authoring marker.'})
    save('EXECUTION_SUMMARY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command_count':len(RECEIPTS),'all_expected_outcomes':True,'source_archive':pin(archive),'clean_manifest':pin(mp),'generated_file_pins':[pin(x) for x in sorted(WORK.rglob('*')) if x.is_file() and not x.is_symlink()],'meaning':'Finite and static local tests only; not a universal theorem proof or race guarantee.'})
    print(json.dumps({'commands':len(RECEIPTS),'all_expected_outcomes':True,'rendered_pages':[str(x) for x in pages]},indent=2))

if __name__=='__main__':main()
