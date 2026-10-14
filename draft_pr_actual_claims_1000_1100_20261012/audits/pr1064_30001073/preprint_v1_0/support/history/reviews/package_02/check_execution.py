"""Whole-package black-box replay and static filesystem fault controls.
Mutations occur only in this review's fresh disposable extraction/fixture.
"""
from pathlib import Path
import subprocess, json, shutil, zipfile, hashlib, os, stat
W=Path(__file__).resolve().parent;R=W.parents[1];P=R/'preprint_v1_0'
TMP=W/'tmp';C=TMP/'clean';receipts=[]
def require(c,m):
    if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def execute(name,args,cwd=C,expected=0,env=None):
    p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,env=env)
    rec={'name':name,'argv':args,'cwd':str(cwd),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    receipts.append(rec)
    require((p.returncode==0)==(expected==0),'unexpected process '+name)
    return rec
def extract():
    if C.exists():shutil.rmtree(C)
    with zipfile.ZipFile(P/'support.zip') as z:z.extractall(C)
def cmd(script,*args,optimized=False):return ['python3','-I','-B',*(['-O'] if optimized else []),script,*map(str,args)]
def refresh():
    m=json.loads((C/'SUPPORT_MANIFEST.json').read_text())
    for x in m['entries']:
        b=(C/x['path']).read_bytes();x['bytes']=len(b);x['sha256']=sha(b)
    (C/'SUPPORT_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
try:
    extract()
    initial={p.relative_to(C).as_posix():sha(p.read_bytes()) for p in C.rglob('*') if p.is_file()}
    execute('README_verify',cmd('verify_package.py'))
    execute('README_run_checks',cmd('run_checks.py','--out-dir','tmp/recheck'))
    execute('README_build_archive',cmd('build_archive.py','--output','tmp/rebuilt.zip'))
    require((C/'tmp/rebuilt.zip').read_bytes()==(P/'support.zip').read_bytes(),'supplied ZIP rebuild differs')
    execute('README_verify_archive',cmd('verify_package.py','--archive','tmp/rebuilt.zip'))
    execute('README_compile',cmd('build_pdf.py','--out-dir','tmp/recompiled'))
    pdf=(C/'tmp/recompiled/paper.pdf').read_bytes()
    info=execute('recompiled_pdfinfo',['pdfinfo',str(C/'tmp/recompiled/paper.pdf')])
    require('Pages:           5' in info['stdout'],'recompiled page count')
    recompile={'bytes':len(pdf),'sha256':sha(pdf),'canonical_bytes_identical':pdf==(P/'paper.pdf').read_bytes(),'pages':5,'scope':'Standalone build in disposable extraction; no candidate mutation or cross-environment identity promise.'}
    baseline=json.loads((P/'support/history/root_reproduction/FINITE_CHECKS.json').read_text())
    replay=json.loads((C/'tmp/recheck/original_normal/FINITE_CHECKS.json').read_text())
    project=lambda j:{k:v for k,v in j.items() if k not in ['completed_utc','python','platform']}
    require(project(baseline)==project(replay),'unmodified normal replay differs')
    guard_normal=json.loads((C/'tmp/recheck/guard_normal/FINITE_CHECKS.json').read_text())
    guard_optimized=json.loads((C/'tmp/recheck/guard_optimized/FINITE_CHECKS.json').read_text())
    require(project(guard_normal)==project(guard_optimized),'guard mode mismatch')
    checks=json.loads((C/'tmp/recheck/CHECKS.json').read_text())
    (W/'SUPPLIED_REPLAY.json').write_text(json.dumps({'unmodified_original_normal_projection_equal':True,'no_original_optimized_validation_claim':True,'new_guard_normal_optimized_projection_equal':True,'checks':checks,'recompiled_pdf':recompile},indent=2)+'\n')
    require(all(sha((C/n).read_bytes())==s for n,s in initial.items()),'documented sequence mutated payload')
    for opt in [False,True]:
        suffix='optimized' if opt else 'normal'
        execute('default_absent_'+suffix,cmd('verify_package.py',optimized=opt))
        execute('required_absent_'+suffix,cmd('verify_package.py','--require-deposit-binding',optimized=opt),expected=1)
        execute('strict_external_binding_'+suffix,cmd('verify_package.py','--archive','tmp/rebuilt.zip','--deposit-binding',P/'publication/DEPOSIT_BINDING.json','--require-deposit-binding',optimized=opt))
        (C/'tmp/bad_binding.json').write_text('{"schema_version":1}')
        execute('malformed_explicit_binding_'+suffix,cmd('verify_package.py','--archive','tmp/rebuilt.zip','--deposit-binding','tmp/bad_binding.json',optimized=opt),expected=1)
        execute('missing_archive_'+suffix,cmd('verify_package.py','--archive','tmp/no_such_archive.zip',optimized=opt),expected=1)
        p=C/'paper.tex';old=p.read_bytes();p.write_bytes(old+b'\n% fault\n')
        execute('corrupt_member_'+suffix,cmd('verify_package.py',optimized=opt),expected=1);p.write_bytes(old)
        extra=C/'extra.json';extra.write_text('{}')
        execute('unmanifested_member_'+suffix,cmd('verify_package.py',optimized=opt),expected=1);extra.unlink()
        for label,name,changes in [('current_ready','CURRENT_STATUS.json',{'publication_ready':True}),('current_count','CURRENT_STATUS.json',{'whole_package_reviews_completed':2}),('current_hold','CURRENT_STATUS.json',{'ascending_publication_hold_after_pr':0}),('original_status','STATUS.json',{'publication_ready':True}),('metadata','metadata.json',{'title':'wrong title'})]:
            p=C/name;old=p.read_bytes();manifest=(C/'SUPPORT_MANIFEST.json').read_bytes();j=json.loads(old);j.update(changes);p.write_text(json.dumps(j,indent=2)+'\n');refresh()
            execute('coherent_'+label+'_'+suffix,cmd('verify_package.py',optimized=opt),expected=1);p.write_bytes(old);(C/'SUPPORT_MANIFEST.json').write_bytes(manifest)
        p=C/'COPY_MAP.json';old=p.read_bytes();manifest=(C/'SUPPORT_MANIFEST.json').read_bytes();j=json.loads(old);j['copies'][0]['sha256']='0'*64;p.write_text(json.dumps(j)+'\n');refresh()
        execute('coherent_copy_hash_'+suffix,cmd('verify_package.py',optimized=opt),expected=1);p.write_bytes(old);(C/'SUPPORT_MANIFEST.json').write_bytes(manifest)
        p=C/'SAFE_INPUT_PINS.json';old=p.read_bytes();manifest=(C/'SUPPORT_MANIFEST.json').read_bytes();j=json.loads(old);j['records']=j['records'][1:];p.write_text(json.dumps(j)+'\n');refresh()
        execute('coherent_selected_pins_'+suffix,cmd('verify_package.py',optimized=opt),expected=1);p.write_bytes(old);(C/'SUPPORT_MANIFEST.json').write_bytes(manifest)
        for label,name,bad in [('manifest_equal','SUPPORT_MANIFEST.json',False),('manifest_malformed','SUPPORT_MANIFEST.json',True),('allowlist_equal','SUPPORT_ALLOWLIST.json',False),('allowlist_malformed','SUPPORT_ALLOWLIST.json',True)]:
            p=C/name;old=p.read_bytes();target=C/'tmp'/('target_'+label);target.write_bytes(b'not JSON' if bad else old);p.unlink();p.symlink_to(target)
            x=execute('preflight_'+label+'_'+suffix,cmd('verify_package.py',optimized=opt),expected=1)
            require('missing/symlink member '+name in x['stderr'] and 'JSONDecodeError' not in x['stderr'],'preflight failed to precede JSON read')
            p.unlink();p.write_bytes(old);target.unlink()
        p=C/'support/history';target=C/'tmp/history_saved';p.rename(target);p.symlink_to(target,target_is_directory=True)
        x=execute('preflight_ancestor_'+suffix,cmd('verify_package.py',optimized=opt),expected=1)
        require('symlink in member ancestry' in x['stderr'],'ancestor preflight missing')
        p.unlink();target.rename(p)
        # Existing archive hardlinks: reveal source overwrite before final failure.
        for protected in ['paper.tex','paper.pdf']:
            p=C/protected;old=p.read_bytes();out=C/'tmp/hardlinked.zip';os.link(p,out)
            x=execute('archive_output_hardlink_'+protected+'_'+suffix,cmd('build_archive.py','--output',out,optimized=opt),expected=1)
            after=p.read_bytes();require(after!=old and after.startswith(b'PK'),'expected independently found defect was not reproduced')
            x.update({'canonical_overwritten':True,'protected_input':protected,'before_sha256':sha(old),'after_sha256':sha(after),'finding':'P3 archive output hardlink alias overwrite'})
            out.unlink();p.write_bytes(old)
    require(all(sha((C/n).read_bytes())==s for n,s in initial.items()),'fault suite restoration failed')
    (W/'REPRODUCTION_RECEIPTS.json').write_text(json.dumps({'pass':True,'command_count':len(receipts),'documented_sequence_payload_unchanged':True,'fault_suite_payload_restored':True,'receipts':receipts},indent=2)+'\n')
finally:
    if C.exists():shutil.rmtree(C)

# Use a separate tiny fixture for canonical PDF alias guards and compiler sentinel.
FOLDER=TMP/'pdf_guard';FOLDER.mkdir(exist_ok=True)
(FOLDER/'build_pdf.py').write_bytes((P/'build_pdf.py').read_bytes());(FOLDER/'paper.tex').write_text('fixture')
binfolder=FOLDER/'bin';binfolder.mkdir(exist_ok=True)
engine=binfolder/'tectonic';engine.write_text('#!/usr/bin/env python3\nfrom pathlib import Path\nimport sys\np=Path(sys.argv[sys.argv.index("--outdir")+1]);(p/"paper.pdf").write_bytes(b"compiler output");(Path(__file__).parent.parent/"compiler_called").write_text("called")\n');engine.chmod(0o755)
env=dict(os.environ);env['PATH']=str(binfolder)+os.pathsep+env['PATH'];pdf_receipts=[]
try:
    for opt in [False,True]:
        suffix='optimized' if opt else 'normal'
        for alias in ['dot','absolute','dotdot','directory_symlink','file_symlink','hardlink']:
            canonical=FOLDER/'paper.pdf';canonical.write_bytes(b'canonical sentinel');marker=FOLDER/'compiler_called'
            if marker.exists():marker.unlink()
            link=FOLDER/'directory_link';out=FOLDER/'out';newparent=FOLDER/'newparent'
            if link.exists() or link.is_symlink():link.unlink()
            if out.exists():shutil.rmtree(out)
            if alias=='dot':arg='.'
            elif alias=='absolute':arg=str(FOLDER)
            elif alias=='dotdot':arg=str(newparent/'..')
            elif alias=='directory_symlink':link.symlink_to(FOLDER,target_is_directory=True);arg=str(link)
            else:
                out.mkdir();arg=str(out)
                if alias=='file_symlink':(out/'paper.pdf').symlink_to(canonical)
                else:os.link(canonical,out/'paper.pdf')
            x=execute('pdf_alias_'+alias+'_'+suffix,cmd('build_pdf.py','--out-dir',arg,optimized=opt),cwd=FOLDER,expected=1,env=env)
            require('aliases canonical' in x['stderr'] and canonical.read_bytes()==b'canonical sentinel' and not marker.exists() and not newparent.exists(),'PDF alias rejection wrote or invoked compiler')
            pdf_receipts.append(x)
        safe=FOLDER/'safe';safe.mkdir(exist_ok=True)
        execute('pdf_safe_'+suffix,cmd('build_pdf.py','--out-dir',safe,optimized=opt),cwd=FOLDER,env=env)
        require(marker.exists() and canonical.read_bytes()==b'canonical sentinel','safe PDF control')
    (W/'PDF_GUARD_RECEIPTS.json').write_text(json.dumps({'pass':True,'aliases_rejected':12,'canonical_preserved':True,'compiler_not_called_on_aliases':True,'safe_controls':2,'receipts':pdf_receipts},indent=2)+'\n')
finally:shutil.rmtree(FOLDER)
(W/'ALL_EXECUTION_RECEIPTS.json').write_text(json.dumps({'pass':True,'actual_command_count':len(receipts),'receipts':receipts,'scope':'Documented reproduction, verifier faults, reproducible archive alias defect, and PDF destination guard controls. All mutations restricted to disposable scratch.'},indent=2)+'\n')
print(json.dumps({'pass':True,'actual_commands':len(receipts),'archive_alias_issue_confirmed':True,'pdf_alias_controls':12,'scratch_removed':True},indent=2))
