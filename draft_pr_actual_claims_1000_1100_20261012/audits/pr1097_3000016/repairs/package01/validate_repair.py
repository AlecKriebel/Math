#!/usr/bin/env python3
"""Actual bounded repair tests in one owned extraction; no real PDF recompilation."""
import sys
sys.dont_write_bytecode = True
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

F=Path(__file__).resolve().parent
A=F.parent.parent
P=A/'preprint_v1_0'
K=P/'kit'
REPO=A.parents[2]
commands=[]

def need(q,m):
    if not q:raise ValueError(m)

def pin(p):
    b=Path(p).read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def load(p):return json.loads(Path(p).read_text())

def write(p,value):Path(p).write_text(json.dumps(value,indent=2)+'\n')

def run(argv,cwd,success=True,env=None,label=''):
    result=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,env=env)
    commands.append({'label':label,'argv':list(map(str,argv)),'cwd':str(cwd),
        'exit_code':result.returncode,'expected_success':success,
        'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr),
        'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
        'stderr_sha256':hashlib.sha256(result.stderr).hexdigest()})
    need((result.returncode==0)==success,'unexpected result '+repr(argv)+' '+result.stderr.decode(errors='replace')[:1400])
    return result.stdout

def tree(root):
    return {str(q.relative_to(root)):pin(q) for q in root.rglob('*') if q.is_file() and not q.is_symlink()}

def main():
    baseline=load(F/'INPUT_PINS.json')['entries']
    before={r['path']:r for r in load(F/'BEFORE_BYTES.json')['entries']}
    changed=[]
    for r in baseline:
        want={'bytes':r['bytes'],'sha256':r['sha256']}
        if pin(A/r['path'])!=want:
            need(r['path'] in before,'unpermitted baseline mutation '+r['path'])
            need(pin(A/before[r['path']]['before_path'])==want,'before bytes missing')
            changed.append(r['path'])
    need(len(changed)==7,'bounded edits count')
    old_pins=(P/'INPUT_PINS.json').read_bytes()
    need(old_pins==(K/'provenance/INPUT_PINS.json').read_bytes(),'old input capture changed')
    old_custody=load(K/'provenance/CUSTODY.json')['entries']
    old_counts={'copies':0,'exclusions':0}
    for r in old_custody:
        if r['decision']=='EXACT_AUTHORED_COPY':
            need((K/r['copy_path']).read_bytes()==(A/r['original_path']).read_bytes(),'old copy changed')
            old_counts['copies']+=1
        else:
            need(r['decision']=='EXCLUDED' and r['reason'],'old omission')
            old_counts['exclusions']+=1
    need(old_counts=={'copies':83,'exclusions':82},'old custody count')
    new_copies=load(K/'provenance/repair01/COPIES.json')['entries']
    for r in new_copies:
        need((A/r['source_path']).read_bytes()==(K/r['copy_path']).read_bytes(),'new exact copy mismatch')
        need(pin(K/r['copy_path'])=={'bytes':r['bytes'],'sha256':r['sha256']},'new copy pin')
    captures=load(K/'provenance/repair01/CUSTODY.json')['entries']
    need(len(captures)==len(baseline) and {r['captured_path'] for r in captures}=={r['path'] for r in baseline},'repair partition')
    captured={r['path']:r for r in baseline}
    distribution_counts={'exact':0,'omitted':0}
    for r in captures:
        need(all(r[k]==captured[r['captured_path']][k] for k in ['bytes','sha256']),'repair captured identity')
        if r['decision']=='EXACT_DISTRIBUTED_BYTES':
            need(pin(K/r['copy_path'])=={'bytes':r['bytes'],'sha256':r['sha256']},'repair distribution mismatch')
            distribution_counts['exact']+=1
        else:
            need(r['decision']=='EXCLUDED' and r['reason'],'repair individual omission')
            distribution_counts['omitted']+=1
    stages=load(K/'provenance/repair01/STAGE_RESOLUTION.json')['entries']
    stage_counts={'audit_exact':0,'audit_omitted':0,'portable_exact':0,'portable_omitted':0}
    for r in stages:
        for field,root,prefix in [('original_audit_resolution',A,'audit'),('portable_resolution',K,'portable')]:
            resolution=r[field]
            if resolution['state'].startswith('EXACT_'):
                need(pin(root/resolution['path'])=={'bytes':r['bytes'],'sha256':r['sha256']},'prior stage resolution mismatch')
                stage_counts[prefix+'_exact']+=1
            else:
                need(resolution['state']=='INDIVIDUAL_OMISSION' and resolution['reason'],'prior omission missing')
                stage_counts[prefix+'_omitted']+=1
    metadata=load(K/'metadata.json')
    need(load(P/'.zenodo.json')==metadata,'bare metadata')
    need(load(P/'zenodo-metadata.json')==load(K/'zenodo-metadata.json')=={'metadata':metadata},'wrapper metadata')
    need(load(P/'zenodo-deposit.json')=={'metadata':metadata,'files':[{'path':n,'name':n} for n in ['paper.pdf','pr1097_support_v1_0.zip']]},'native manifest')
    need(load(F/'before/DEPOSIT_BINDING.json')['metadata']==metadata,'bibliographic metadata changed')
    need(pin(P/'paper.pdf')['sha256']=='6ae840e0b2e1df73b204c2c293c3fbcfa39206654e775a75261515c693a6187d','paper changed')
    names=sorted(q.relative_to(K).as_posix() for q in K.rglob('*') if q.is_file())
    source=(P/'pr1097_support_v1_0.zip').read_bytes()
    with zipfile.ZipFile(io.BytesIO(source)) as z:
        need(z.namelist()==names and not z.comment and z.testzip() is None,'ZIP inventory/CRC')
        for info in z.infolist():
            need(z.read(info.filename)==(K/info.filename).read_bytes(),'ZIP payload')
            need(info.date_time==(1980,1,1,0,0,0) and info.compress_type==zipfile.ZIP_STORED and info.create_system==3 and info.external_attr==0o100644<<16 and not info.extra and not info.comment,'ZIP metadata')
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_STORED) as z:
        for name in names:
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16
            z.writestr(info,(K/name).read_bytes())
    need(buffer.getvalue()==source,'independent CLOSED ZIP mismatch')
    scratch=Path(tempfile.mkdtemp(prefix='repair1097-package01-',dir='/private/tmp'))
    cleanup=[];case_rows=[];original_rows=[];normalization_rows=[]
    results=[];status='RUNNING';failure=None
    try:
        clean=scratch/'clean';clean.mkdir()
        with zipfile.ZipFile(io.BytesIO(source)) as z:z.extractall(clean)
        clean_before=tree(clean)
        original=scratch/'OriginalRoot';original.mkdir();(original/'nested').mkdir()
        (original/'unchanged.txt').write_bytes(b'original root sentinel\n')
        original_before=tree(original)
        accented=scratch/'Caf\u00e9Root';accented.mkdir()
        (accented/'unchanged.txt').write_bytes(b'unicode root sentinel\n')
        accented_before=tree(accented)
        absent=scratch/'AbsentOriginalRoot'
        bindir=scratch/'bin';bindir.mkdir()
        fake=bindir/'tectonic'
        fake.write_text('#!/bin/sh\nprintf invoked > "$REPAIR1097_SENTINEL"\nexit 97\n')
        fake.chmod(0o700)
        sentinel=scratch/'compiler-was-invoked'
        env=dict(os.environ);env['PATH']=str(bindir)+os.pathsep+env.get('PATH','');env['REPAIR1097_SENTINEL']=str(sentinel)
        config=clean/'PROTECTED_PATHS.json';manifest=clean/'MANIFEST.json'
        saved_config=config.read_bytes();saved_manifest=manifest.read_bytes()
        def set_config(roots):
            value=json.loads(saved_config);value['original_protected_roots']=list(map(str,roots))
            config.write_text(json.dumps(value,indent=2)+'\n')
            m=json.loads(saved_manifest)
            for row in m['entries']:
                if row['path']=='PROTECTED_PATHS.json':row.update(pin(config))
            manifest.write_text(json.dumps(m,indent=2)+'\n')
        def reject_writer(base,script,option,dest,label):
            before_files=tree(clean)
            run(base+['scripts/'+script,option,dest],clean,False,env,label)
            need(not os.path.lexists(dest),'rejected fresh output appeared: '+str(dest))
            need(tree(clean)==before_files,'rejected writer changed kit')
            need(not sentinel.exists(),'rejected PDF writer invoked compiler')
        for tag,flags in [('normal',['-B']),('optimized',['-O','-B'])]:
            base=[sys.executable]+flags
            need(json.loads(run(base+['scripts/verify.py'],clean,label='README optional '+tag))['binding']['state']=='ABSENT_OPTIONAL','optional missing state')
            check=json.loads(run(base+['scripts/run_checks.py'],clean,label='README exact math '+tag))
            need(check==load(clean/'EXPECTED_RESULTS.json'),'complete expected math JSON');results.append(check)
            run(base+['scripts/run_checks.py','--inject-failure'],clean,False,label='unconditional guard '+tag)
            run(base+['scripts/verify.py','--require-binding'],clean,False,label='strict absent default '+tag)
            run(base+['scripts/verify.py','--binding',scratch/'missing-binding.json'],clean,False,label='explicit absent '+tag)
            run(base+['scripts/verify.py','--binding',P/'DEPOSIT_BINDING.json','--require-binding'],clean,label='strict actual binding '+tag)
            output=scratch/(tag+'.zip')
            run(base+['scripts/build_support.py','--out',output],clean,label='README clean archive '+tag)
            need(output.read_bytes()==source,'supported clean ZIP byte mismatch')
            # Actual physical aliases are asserted before using them as controls.
            alias=scratch/'CLEAN'
            case_available=alias.exists() and os.path.samefile(alias,clean)
            if case_available:
                for script,opt,suffix in [('build_support.py','--out','.zip'),('rebuild_pdf.py','--out-dir','-pdf')]:
                    for parent,kind in [(alias,'root'),(alias/'provenance','existing-nested'),(alias/'new-missing'/'deeper','missing-deeper')]:
                        need(os.path.samefile(alias,clean),'case alias identity lost')
                        dest=parent/(tag+'-'+kind+suffix)
                        reject_writer(base,script,opt,dest,'physical kit case alias '+kind+' '+tag)
                        case_rows.append({'mode':tag,'writer':script,'kind':kind,'samefile_asserted':True,'exit_nonzero':True,'new_output_absent':True})
            else:
                case_rows.append({'mode':tag,'status':'QUALIFIED_SKIP_CASE_ALIAS_NOT_AVAILABLE_ON_THIS_FILESYSTEM','samefile_asserted':False})
            # Both writers retain existing-leaf, hardlink/symlink, traversal and ancestry guards.
            hard=scratch/(tag+'-hardlink');os.link(clean/'paper.pdf',hard)
            link=scratch/(tag+'-leaflink');link.symlink_to(clean/'paper.pdf')
            ancestor=scratch/(tag+'-ancestor');ancestor.symlink_to(scratch,target_is_directory=True)
            occupied=scratch/(tag+'-occupied');occupied.mkdir()
            for name in ['paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt']:
                os.link(clean/'paper.pdf',occupied/name)
            protected_pins={str(p):pin(p) for p in [hard,clean/'paper.pdf']+[occupied/n for n in ['paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt']]}
            for script,opt in [('build_support.py','--out'),('rebuild_pdf.py','--out-dir')]:
                for dest,label in [(hard,'hardlink leaf'),(link,'symlink leaf'),(ancestor/'new-output','symlink ancestor'),(occupied,'occupied directory')]:
                    run(base+['scripts/'+script,opt,dest],clean,False,env,label+' '+tag)
                for dest,label in [(clean/('new-output-'+tag),'lexical protected root'),(clean/'provenance'/('new-output-'+tag),'lexical protected nested'),(scratch/'..'/('bad-output-'+tag),'parent traversal'),(scratch/'missing-parent'/('new-output-'+tag),'missing parent')]:
                    reject_writer(base,script,opt,dest,label+' '+tag)
            need({p:pin(Path(p)) for p in protected_pins}==protected_pins,'existing target bytes modified')
            # Bootstrap checks must reject a symlink before attempting invalid JSON parsing.
            invalid=scratch/(tag+'-invalid-manifest.json');invalid.write_bytes(b'NOT JSON')
            manifest.unlink();manifest.symlink_to(invalid)
            try:
                for script,extra in [('verify.py',[]),('build_support.py',['--out',scratch/(tag+'-bootstrap.zip')]),('rebuild_pdf.py',['--out-dir',scratch/(tag+'-bootstrap-pdf')])]:
                    run(base+['scripts/'+script]+extra,clean,False,env,'bootstrap preparse '+script+' '+tag)
            finally:
                manifest.unlink();manifest.write_bytes(saved_manifest)
            sibling=scratch/'DEPOSIT_BINDING.json'
            for bad in [{'bad':'binding'},dict(load(P/'DEPOSIT_BINDING.json'),metadata=dict(metadata,title='WRONG'))]:
                sibling.write_text(json.dumps(bad))
                run(base+['scripts/verify.py'],clean,False,label='present malformed binding '+tag);sibling.unlink()
            sibling.symlink_to(scratch/'broken-binding-target')
            run(base+['scripts/verify.py'],clean,False,label='present broken binding symlink '+tag);sibling.unlink()
            for script in ['verify.py','run_checks.py']:
                run(base+['scripts/'+script,'--output',scratch/(tag+'-unsupported')],clean,False,label='unsupported output '+script+' '+tag)
            # Change only disposable guard config and its inventory pin. Never address a canonical original-root alias.
            set_config([original,absent,accented])
            run(base+['scripts/verify.py'],clean,label='disposable original-root guard configuration '+tag)
            original_alias=scratch/'ORIGINALROOT'
            original_case=original_alias.exists() and os.path.samefile(original_alias,original)
            if original_case:
                for script,opt,suffix in [('build_support.py','--out','.zip'),('rebuild_pdf.py','--out-dir','-pdf')]:
                    for parent,kind in [(original_alias,'root'),(original_alias/'nested','existing-nested'),(original_alias/'new-missing'/'deeper','missing-deeper')]:
                        need(os.path.samefile(original_alias,original),'original alias identity lost')
                        reject_writer(base,script,opt,parent/(tag+'-'+kind+suffix),'physical ORIGINAL case alias '+kind+' '+tag)
                        original_rows.append({'mode':tag,'writer':script,'kind':kind,'samefile_asserted':True,'new_output_absent':True})
            else:
                original_rows.append({'mode':tag,'status':'QUALIFIED_SKIP_CASE_ALIAS_NOT_AVAILABLE_ON_THIS_FILESYSTEM'})
            normalized_alias=scratch/'Cafe\u0301Root'
            normalization_available=normalized_alias.exists() and os.path.samefile(normalized_alias,accented)
            if normalization_available:
                for script,opt,suffix in [('build_support.py','--out','.zip'),('rebuild_pdf.py','--out-dir','-pdf')]:
                    need(os.path.samefile(normalized_alias,accented),'normalization alias identity lost')
                    reject_writer(base,script,opt,normalized_alias/(tag+suffix),'physical normalization ORIGINAL alias '+tag)
                    normalization_rows.append({'mode':tag,'writer':script,'samefile_asserted':True,'new_output_absent':True})
            else:
                normalization_rows.append({'mode':tag,'status':'QUALIFIED_SKIP_NORMALIZATION_ALIAS_NOT_AVAILABLE'})
            need(tree(original)==original_before and tree(accented)==accented_before,'disposable protected original changed')
            # An absent original root remains optional, as before this repair.
            set_config([absent])
            run(base+['scripts/verify.py'],clean,label='absent original root verification '+tag)
            absent_output=scratch/(tag+'-absent-original.zip')
            run(base+['scripts/build_support.py','--out',absent_output],clean,label='absent original root allowed archive '+tag)
            with zipfile.ZipFile(absent_output) as z:need(z.testzip() is None and z.read('PROTECTED_PATHS.json')==config.read_bytes(),'absent-root ZIP')
            config.write_bytes(saved_config);manifest.write_bytes(saved_manifest)
            run(base+['scripts/verify.py','--binding',P/'DEPOSIT_BINDING.json','--require-binding'],clean,label='final restored strict '+tag)
            need(tree(clean)==clean_before,'disposable kit failed exact restoration')
        need(results[0]==results[1],'complete normal/optimized checker results differ')
        need(not sentinel.exists(),'ANY rejection invoked compiler')
        local=json.loads(run([sys.executable,'-B',REPO/'zenodo_deposit_tool/zenodo.py','check',P/'zenodo-deposit.json'],REPO,label='actual repository native LOCAL check'))
        for r in baseline:
            target=A/r['path']
            if r['path'] in before:target=A/before[r['path']]['before_path']
            need(pin(target)=={'bytes':r['bytes'],'sha256':r['sha256']},'final baseline preservation')
        result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
            'baseline_regular_files':len(baseline),'changed_existing_files':changed,'unchanged_existing_files':len(baseline)-len(changed),
            'all_changed_before_bytes_exact':True,'old165_capture_and83_82_custody_unchanged':True,
            'supplementary_exact_source_copies':len(new_copies),'repair_custody':distribution_counts,
            'prior_pin_rows':len(stages),'prior_pin_resolution':stage_counts,
            'native_bibliographic_metadata_unchanged':True,'all_native_metadata_objects_equal':True,
            'closed_ZIP_members':len(names),'independent_closed_ZIP_byte_identity':True,
            'ordinary_optimized_complete_math_JSON_equal_EXPECTED':True,
            'kit_case_alias_controls':case_rows,'disposable_original_case_alias_controls':original_rows,
            'normalization_alias_controls':normalization_rows,
            'compiler_invoked_by_rejections':False,'new_real_compilation_or_rendering_performed':False,
            'unchanged_PDF_prior_real_compile_and_all6_actual_views':'INHERITED_CAPTURED_STAGE_NOT_REPEATED',
            'command_count':len(commands),'expected_nonzero_rejections':sum(not r['expected_success'] for r in commands),
            'paper':pin(P/'paper.pdf'),'archive':pin(P/'pr1097_support_v1_0.zip'),
            'native_repository_local_check':local,'publication_ready':False,'published':False,
            'new_complete_whole02_required':True,'ordered_service_hold_pr':1032,
            'Git_or_service_or_outreach_action':False}
        write(F/'VALIDATION.json',result);status='PASS'
        print(json.dumps({k:result[k] for k in ['status','baseline_regular_files','unchanged_existing_files','supplementary_exact_source_copies','prior_pin_rows','closed_ZIP_members','command_count','expected_nonzero_rejections','archive']},indent=2))
    except BaseException as exc:
        status='FAIL';failure={'type':type(exc).__name__,'message':str(exc)}
        raise
    finally:
        for q in sorted(scratch.rglob('*')):
            if q.is_file() and not q.is_symlink():cleanup.append({'path':str(q.relative_to(scratch)),**pin(q)})
        write(F/'COMMAND_RECEIPTS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'failure':failure,'entries':commands})
        write(F/'SCRATCH_CLEANUP.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scratch':str(scratch),'removed_only_own_scratch':True,'files':cleanup})
        shutil.rmtree(scratch)

if __name__=='__main__':main()
