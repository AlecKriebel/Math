"""Actual unchanged package commands in one compact owned external fixture."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import uuid
import zipfile

sys.dont_write_bytecode = True
F = Path(__file__).resolve().parent
A = F.parents[1]
C = A/'preprint_v1_0'
T = Path('/private/tmp')/('pr1098-terminal-'+str(uuid.uuid4()))
commands = []
faults = []

def need(value, message):
    if not value:
        raise ValueError(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def rec(p):
    b = p.read_bytes()
    return {'bytes':len(b), 'sha256':digest(b)}

def save(name, obj):
    (F/name).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')

def run(argv, success=True, label=''):
    args = list(map(str,argv))
    result = subprocess.run(args,capture_output=True)
    commands.append({'argv':args,'label':label,'expected_success':success,
        'exit_code':result.returncode,'stdout':result.stdout.decode(errors='replace'),
        'stderr':result.stderr.decode(errors='replace'),
        'stdout_sha256':digest(result.stdout),'stderr_sha256':digest(result.stderr)})
    save('ACTUAL_COMMANDS.json',{'external_root':str(T),'commands':commands,
        'runtime_ROOT_or_ORIGINAL_modified':False})
    need((result.returncode==0)==success,'unexpected actual exit: '+label)
    return result

def closed_archive(kit, update=False):
    manifest=json.loads((kit/'MANIFEST.json').read_text())
    if update:
        for row in manifest['entries']:
            row.update(rec(kit/row['path']))
        (kit/'MANIFEST.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    names=[r['path'] for r in manifest['entries']]
    need(names==sorted(set(names)),'independent sorted unique names')
    payload={name:(kit/name).read_bytes() for name in names}
    payload['MANIFEST.json']=(kit/'MANIFEST.json').read_bytes()
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_STORED) as z:
        for name,raw in sorted(payload.items()):
            item=zipfile.ZipInfo(name,(2026,10,16,0,0,0))
            item.create_system=3
            item.external_attr=0o100644<<16
            z.writestr(item,raw)
    return stream.getvalue()

def main():
    T.mkdir()
    K=T/'kit';K.mkdir()
    with zipfile.ZipFile(C/'pr1098_support_v1_0.zip') as z:
        need(len(z.namelist())==len(set(z.namelist()))==124,'124 closed ZIP members')
        need(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist()),'safe ZIP names')
        z.extractall(K)
    for name in ('paper.pdf','pr1098_support_v1_0.zip'):
        shutil.copyfile(C/name,K/name)
    initial={str(p.relative_to(K)):rec(p) for p in K.rglob('*') if p.is_file()}
    independent=closed_archive(K)
    need(independent==(C/'pr1098_support_v1_0.zip').read_bytes(),'independent entire closed ZIP')
    (T/'independent-closed.zip').write_bytes(independent)
    with zipfile.ZipFile(io.BytesIO(independent)) as z:
        need(z.testzip() is None and not z.comment,'independent closed CRC/comment')
        need('paper.pdf' not in z.namelist() and 'ARTIFACT_BINDINGS.json' in z.namelist(),'external mandatory PDF binding')
        need(not any(n.endswith(('.pdf','.zip','.png')) for n in z.namelist()),'no body/pixel/old ZIP payload')
        for info in z.infolist():
            need(info.compress_type==zipfile.ZIP_STORED and info.date_time==(2026,10,16,0,0,0)
                 and info.external_attr==0o100644<<16 and info.create_system==3
                 and not info.extra and not info.comment,'fixed ZIP attributes')
    normal=[];verifications=[]
    for opt in (False,True):
        cmd=[sys.executable]+(['-O'] if opt else [])+['-B']
        v=run(cmd+[K/'code/verify_kit.py'],label='clean verifier '+str(opt));verifications.append(v.stdout)
        checks=run(cmd+[K/'code/run_checks.py'],label='complete finite diagnostics '+str(opt))
        obj=json.loads(checks.stdout);normal.append(checks.stdout)
        save('MATH_'+('optimized' if opt else 'normal')+'.json',obj)
        expected=json.loads((C/'validation'/('CLEAN_CHECKS_optimized.json' if opt else 'CLEAN_CHECKS_normal.json')).read_text())
        need(obj==expected,'full finite JSON equals preparation')
        bad=run(cmd+[K/'code/run_checks.py','--invalid'],False,'unconditional mathematical guard '+str(opt))
        need(b'deliberate unconditional diagnostic guard' in bad.stderr,'actual invalid exception')
        dest=T/('closed-rebuild-'+str(opt)+'.zip')
        run(cmd+[K/'code/rebuild_archive.py','--output',dest],label='actual unchanged archive writer '+str(opt))
        need(dest.read_bytes()==independent,'actual writer full closed ZIP equality')
    need(normal[0]==normal[1] and verifications[0]==verifications[1],'normal/optimized entire stdout equality')
    canonical={str(p.relative_to(K)):p.read_bytes() for p in K.rglob('*') if p.is_file()}
    def restore():
        for name,raw in canonical.items():
            path=K/name
            if path.is_symlink():path.unlink()
            path.write_bytes(raw)
    def coherent_fault(cmd,name,mutator):
        restore();mutator()
        (K/'pr1098_support_v1_0.zip').write_bytes(closed_archive(K,True))
        result=run(cmd+[K/'code/verify_kit.py'],False,'coherent '+name)
        faults.append({'fault':name,'optimized':'-O' in cmd,'repacked_all_manifest_bytes_and_entire_closed_ZIP':True,
                       'actual_exception':result.stderr.decode(errors='replace').splitlines()[-1]})
    def alter(name,key,value):
        path=K/name;obj=json.loads(path.read_text());obj[key]=value
        path.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
    for opt in (False,True):
        cmd=[sys.executable]+(['-O'] if opt else [])+['-B']
        for key,value in [
            ('new_complete_whole_reviews_completed',1),('minimum_new_complete_whole_reviews_required',3),
            ('latest_review_actionable_findings',{'P0':0,'P1':0,'P2':0,'P3':1}),
            ('latest_whole_review_ROOT_adopted',False),('further_whole_package_review_currently_required',True),
            ('ROOT_final_terminal_integrity_adopted',True),('publication_ready',True),
            ('issues_resolved',True),('published',True),('services_held_after_pr',1031),
            ('full_result_physical_simple_oriented_realization_remaining_method_priority_worldwide_openness','KNOWN')]:
            coherent_fault(cmd,'current '+key,lambda k=key,v=value:alter('TERMINAL_STATUS.json',k,v))
        evidence=[
            ('latest verdict findings','terminal/evidence/package_02/VERDICT.json','finding_counts',{'P0':0,'P1':0,'P2':1,'P3':0}),
            ('ROOT adopted count','terminal/evidence/ROOT_WHOLE_PACKAGE_REVIEW_02.json','whole_reviews_completed',1),
            ('ROOT pin identity','terminal/evidence/ROOT_WHOLE_PACKAGE_REVIEW_02.json','output_pins_sha256','0'*64),
            ('review seal verdict identity','terminal/evidence/package_02/OUTPUT_SEAL.json','verdict',{'bytes':1252,'sha256':'0'*64}),
            ('dated preparation count','STATUS.json','new_complete_whole_reviews_completed',2),
            ('native selections','publication/zenodo-deposit.json','files',[{'path':'../paper.pdf','name':'paper.pdf'}]),
            ('native metadata','metadata.json','creators',[])]
        for name,path,key,value in evidence:
            coherent_fault(cmd,name,lambda p=path,k=key,v=value:alter(p,k,v))
        coherent_fault(cmd,'review authored report',lambda:(K/'terminal/evidence/package_02/REPORT.md').write_bytes(canonical['terminal/evidence/package_02/REPORT.md']+b'changed'))
        def stage_fault():
            path=K/'terminal/REVIEW_STAGE_SELECTION.json';obj=json.loads(path.read_text())
            row=next(r for r in obj['entries'] if r['disposition']=='OMITTED');row['reason']=''
            path.write_text(json.dumps(obj))
        coherent_fault(cmd,'individual stage omission reason',stage_fault)
        def prep_fault():
            path=K/'terminal/PREPARATION_PIN_RESOLUTION.json';obj=json.loads(path.read_text());obj['entries'][0]['sha256']='0'*64
            path.write_text(json.dumps(obj))
        coherent_fault(cmd,'preparation original identity',prep_fault)
        restore()
        # Each bootstrap fault is applied independently and restored exactly.
        for name in ['MANIFEST.json','ARTIFACT_BINDINGS.json','metadata.json','TERMINAL_STATUS.json']:
            path=K/name;raw=path.read_bytes()
            for kind in ['missing','duplicate','symlink','hardlink']:
                ext=T/'bootstrap-saved';ext.write_bytes(raw)
                path.unlink()
                if kind=='duplicate':path.write_bytes(b'{"duplicate":1,"duplicate":2}')
                elif kind=='symlink':path.symlink_to(ext)
                elif kind=='hardlink':os.link(ext,path)
                result=run(cmd+[K/'code/verify_kit.py'],False,'bootstrap '+name+' '+kind+' '+str(opt))
                faults.append({'fault':name+' '+kind,'optimized':opt,'actual_exception':result.stderr.decode(errors='replace').splitlines()[-1]})
                if path.exists() or path.is_symlink():path.unlink()
                path.write_bytes(raw);ext.unlink()
        for name in ('paper.pdf','pr1098_support_v1_0.zip'):
            path=K/name;raw=path.read_bytes();path.unlink()
            run(cmd+[K/'code/verify_kit.py'],False,'missing download '+name+' '+str(opt));path.write_bytes(raw)
        existing=T/'existing';existing.write_bytes(b'keep existing bytes')
        directory=T/'existing-dir';directory.mkdir(exist_ok=True)
        link=T/'leaf-link';link.symlink_to(existing)
        broken=T/'broken-link';broken.symlink_to(T/'absent')
        ancestor=T/'kit-link';ancestor.symlink_to(K,target_is_directory=True)
        hard=T/'hard-existing';os.link(existing,hard)
        aliases=[Path(str(K).upper()),Path(str(A).upper())]
        need(all(p.exists() and os.path.samefile(p,q) for p,q in zip(aliases,[K,A])),'actual physical aliases of both protected roots')
        targets=[existing,directory,link,broken,ancestor/'new',hard,
            K/'forbidden-new',A/'terminal-admin-must-not-create',
            aliases[0]/'forbidden-new',aliases[1]/'terminal-admin-must-not-create',
            T/'missing-parent'/'new',T/'x'/'..'/'new',Path('relative-output')]
        for writer,flag in [('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')]:
            for dest in targets:
                run(cmd+[K/'code'/writer,flag,dest],False,'physical writer guard '+writer+' '+str(dest)+' '+str(opt))
            for name in ('MANIFEST.json','paper.tex'):
                source=K/name;linked=T/'input-hardlink';os.link(source,linked)
                dest=T/('new-bad-input-'+writer+name+str(opt))
                run(cmd+[K/'code'/writer,flag,dest],False,'good destination hardlinked '+name+' '+str(opt))
                need(not dest.exists(),'bad input created destination');linked.unlink()
            source=K/'publication';back=T/'publication-real';source.rename(back);source.symlink_to(back,target_is_directory=True)
            dest=T/('new-dirlink-'+writer+str(opt))
            run(cmd+[K/'code'/writer,flag,dest],False,'good destination symlinked publication '+str(opt))
            need(not dest.exists(),'symlinked input created destination');source.unlink();back.rename(source)
        need(existing.read_bytes()==b'keep existing bytes','existing leaf preserved')
        for path in [link,broken,ancestor,hard]:path.unlink()
        run(cmd+[K/'code/verify_kit.py'],label='clean after individual restoration '+str(opt))
    restore()
    final={str(p.relative_to(K)):rec(p) for p in K.rglob('*') if p.is_file()}
    need(initial==final,'all extracted bytes restored exactly')
    native=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
    source=native.read_text()
    start=source.index('if args.command == "check":')
    token=source.index('client = ZenodoClient(environment, token_for(environment))',start)
    need(source.index('return summary',start)<token,'native check returns before token/network client')
    local=run([sys.executable,'-B',native,'check',C/'publication/zenodo-deposit.json'],label='repository native LOCAL-ONLY check')
    save('NATIVE_LOCAL_CHECK.json',{'status':'PASS','tool':str(native),**rec(native),
        'check_returns_before_token_and_network_client':True,'network_action':False,
        'exit_code':local.returncode,'summary':json.loads(local.stdout)})
    save('VALIDATION.json',{'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS',
        'commands':len(commands),'coherent_semantic_and_evidence_faults':faults,
        'normal_optimized_complete_math_JSON_equal':True,'full_math_JSON_equals_preparation':True,
        'normal_optimized_complete_verifier_JSON_equal':True,'unconditional_math_fault_both_modes':True,
        'independent_closed_archive':{'bytes':len(independent),'sha256':digest(independent),'members':124,'entire_bytes_equal':True,'read_after_close':True},
        'actual_unmodified_archive_writers_both_modes_equal':True,
        'physical_alias_samefile_both_protected_roots':True,
        'runtime_ROOT_or_ORIGINAL_modified':False,'all_extracted_files_restored':len(final),
        'actual_real_PDF_rebuild_or_render_repeated':False,
        'PDF_reason':'Canonical PDF and TeX bytes unchanged; two completed whole reviews already performed actual normal/O builds and viewed all seven canonical pages.',
        'native_local_check':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032})

try:
    main()
finally:
    if T.exists():
        pins=[];links=[]
        for path in sorted(T.rglob('*')):
            info=path.lstat()
            if stat.S_ISREG(info.st_mode):pins.append({'path':str(path.relative_to(T)),**rec(path),'nlink':info.st_nlink})
            elif stat.S_ISLNK(info.st_mode):links.append({'path':str(path.relative_to(T)),'target':os.readlink(path)})
        cleanup={'absolute_path':str(T),'regular_files_before_cleanup':pins,'symlinks_before_cleanup':links,
            'only_new_owned_unsealed_derivatives':True,'durable_local_old_ZIP_is_outside_this_tree_and_retained':True,'removed':False}
        save('EXTERNAL_CLEANUP.json',cleanup)
        shutil.rmtree(T)
        cleanup['removed']=True;save('EXTERNAL_CLEANUP.json',cleanup)
