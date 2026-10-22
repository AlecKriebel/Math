#!/usr/bin/env python3
"""Bounded actual normal/-O verification in one owned compact scratch; no compiler."""
import sys
sys.dont_write_bytecode=True
import datetime, hashlib, io, json, os, shutil, struct, subprocess, tempfile, zlib, zipfile
from pathlib import Path
import prepare_terminal as p
F,A,P,K=p.F,p.A,p.P,p.K
commands=[]
def need(q,m):
    if not q:raise ValueError(m)
def pin(q):return p.pin(Path(q))
def load(q):return p.load(Path(q))
def write(q,v):p.write(Path(q),v)
def run(argv,cwd,label,success=True,env=None,expect_text=None):
    r=subprocess.run(list(map(str,argv)),cwd=cwd,env=env,capture_output=True)
    entry={'label':label,'argv':list(map(str,argv)),'cwd':str(cwd),'exit_code':r.returncode,'expected_success':success,
           'stdout':r.stdout.decode(errors='replace'),'stderr':r.stderr.decode(errors='replace'),
           'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),
           'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()}
    commands.append(entry)
    need((r.returncode==0)==success,'unexpected actual return code '+label+' '+entry['stderr'][:1500])
    if expect_text:need(expect_text in entry['stderr'],'failure did not reach intended guard '+label+' '+entry['stderr'][:1500])
    return r.stdout
def tree(root):
    return {q.relative_to(root).as_posix():pin(q) for q in root.rglob('*') if q.is_file() and not q.is_symlink()}
def closed_zip():
    source=(P/'pr1097_support_v1_0.zip').read_bytes();names=sorted(q.relative_to(K).as_posix() for q in K.rglob('*') if q.is_file());rows=[]
    with zipfile.ZipFile(io.BytesIO(source)) as z:
        need(z.namelist()==names and len(names)==len(set(names)) and not z.comment and z.testzip() is None,'CLOSED ZIP names/CRC')
        for info in z.infolist():
            data=z.read(info.filename);need(data==(K/info.filename).read_bytes(),'CLOSED ZIP payload')
            need(info.date_time==(1980,1,1,0,0,0) and info.compress_type==0 and info.create_system==3 and info.external_attr==0o100644<<16
                 and info.flag_bits==0 and not info.extra and not info.comment and info.CRC==zlib.crc32(data),'CLOSED ZIP central metadata')
            fields=struct.unpack_from('<IHHHHHIIIHH',source,info.header_offset)
            signature,version,flags,method,mtime,mdate,crc,csize,usize,nlen,xlen=fields
            start=info.header_offset+30;raw_name=source[start:start+nlen];payload=source[start+nlen+xlen:start+nlen+xlen+csize]
            need(signature==0x04034b50 and version==20 and flags==0 and method==0 and mtime==0 and mdate==33
                 and crc==info.CRC and csize==usize==len(data) and xlen==0 and raw_name==info.filename.encode('utf-8') and payload==data,'CLOSED ZIP local header/payload')
            rows.append({'path':info.filename,**pin(K/info.filename),'CRC':info.CRC,'header_offset':info.header_offset,'local_header_fields':list(fields)})
    independent=io.BytesIO()
    with zipfile.ZipFile(independent,'w',compression=zipfile.ZIP_STORED) as z:
        for name in names:
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;z.writestr(info,(K/name).read_bytes())
    need(independent.getvalue()==source,'independent CLOSED deterministic ZIP bytes')
    write(F/'CLOSED_ZIP.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','members':len(names),'archive':pin(P/'pr1097_support_v1_0.zip'),'all_local_and_central_headers_payloads_CRC_checked':True,'independent_closed_archive_byte_equal':True,'entries':rows})
    return source
def custody():
    freeze=load(F/'INPUT_FREEZE.json')['entries'];before={r['path']:r for r in load(F/'BEFORE_BYTES.json')['entries']};changed=[]
    actual={};distributed={};rebindings=[]
    for r in freeze:
        actual[(r['bytes'],r['sha256'])]=A/(before[r['path']]['before_path'] if r['path'] in before else r['path'])
    for q in K.rglob('*'):
        if q.is_file():
            identity=pin(q);distributed[(identity['bytes'],identity['sha256'])]=q
    def historical_exact(target,row,portable,label):
        want={k:row[k] for k in ['bytes','sha256']}
        if target.is_file() and pin(target)==want:return
        replacement=(distributed if portable else actual).get((row['bytes'],row['sha256']))
        need(replacement is not None and pin(replacement)==want,'unresolved historical exact identity '+label)
        rebindings.append({'historical_locator':str(target),'current_exact_old_byte_locator':str(replacement),'record':label,**want})
    for r in freeze:
        want={k:r[k] for k in ['bytes','sha256']};now=pin(A/r['path'])
        if now!=want:
            need(r['path'] in before,'unpermitted baseline edit '+r['path']);need(pin(A/before[r['path']]['before_path'])==want,'before bytes');changed.append(r['path'])
    need(len(changed)==7,'seven minimal changes')
    old=load(K/'provenance/CUSTODY.json')['entries'];repair=load(K/'provenance/repair01/CUSTODY.json')['entries']
    need(len(old)==165 and sum(r['decision']=='EXACT_AUTHORED_COPY' for r in old)==83 and sum(r['decision']=='EXCLUDED' for r in old)==82,'original165 partition')
    need(len(repair)==332 and sum(r['decision']=='EXACT_DISTRIBUTED_BYTES' for r in repair)==233 and sum(r['decision']=='EXCLUDED' for r in repair)==99,'repair332 partition')
    for group in [old,repair]:
        for r in group:
            if r['decision']!='EXCLUDED':historical_exact(K/r['copy_path'],r,True,'old custody '+r.get('captured_path',r.get('original_path','')))
            else:need(r['reason'],'old omission reason')
    for layer in ['repair01','terminal_admin_20261016']:
        for r in load(K/'provenance'/layer/'COPIES.json')['entries']:
            need((A/r['source_path']).read_bytes()==(K/r['copy_path']).read_bytes(),'source-copy exact '+r['source_path'])
            need(pin(K/r['copy_path'])=={k:r[k] for k in ['bytes','sha256']},'copy pin')
    terminal=load(K/'provenance/terminal_admin_20261016/CUSTODY.json')['entries'];freeze_by={r['path']:r for r in freeze}
    need(len(terminal)==683 and {r['captured_path'] for r in terminal}==set(freeze_by),'terminal capture partition')
    for r in terminal:
        need(all(r[k]==freeze_by[r['captured_path']][k] for k in ['bytes','sha256']),'terminal capture pin')
        if r['decision']=='EXACT_DISTRIBUTED_BYTES':need(pin(K/r['copy_path'])=={k:r[k] for k in ['bytes','sha256']},'terminal custody copy')
        else:need(r['decision']=='EXCLUDED' and r['reason'],'terminal omission')
    stage_counts={};history=load(K/'provenance/repair01/STAGE_RESOLUTION.json')['entries']
    need(len(history)==1127 and sum(r['original_audit_resolution']['state']=='INDIVIDUAL_OMISSION' for r in history)==18,'old1127 history')
    for rows in [history,load(K/'provenance/terminal_admin_20261016/STAGE_RESOLUTION.json')['entries']]:
        coverage=[]
        for r in rows:
            for field,root in [('original_audit_resolution',A),('portable_resolution',K)]:
                resolution=r[field];state=resolution['state'];stage_counts[field+':'+state]=stage_counts.get(field+':'+state,0)+1
                if state.startswith('EXACT_'):
                    target=Path(resolution['path']) if state=='EXACT_EXTERNAL_READ_ONLY_INPUT' else root/resolution['path']
                    historical_exact(target,r,field=='portable_resolution','stage '+r['inventory']+':'+str(r['row_zero_based']))
                else:need(state=='INDIVIDUAL_OMISSION' and resolution['reason'],'individual historical omission')
            inv=A/r['inventory']
            if r['inventory'] in before:inv=A/before[r['inventory']]['before_path']
            value=load(inv);field=r.get('array')
            source=value[field] if field else next(value[k] for k in ['entries','files','records','renders'] if isinstance(value.get(k),list))
            row=source[r['row_zero_based']]
            need(row.get('bytes',row.get('size'))==r['bytes'] and row['sha256']==r['sha256'],'original inventory indexed row')
            coverage.append((r['inventory'],r['row_zero_based']))
        need(len(coverage)==len(set(coverage)),'duplicate stage rows')
    meta=load(K/'metadata.json');native=load(P/'zenodo-deposit.json')
    need(native=={'metadata':meta,'files':[{'path':n,'name':n} for n in ['paper.pdf','pr1097_support_v1_0.zip']]},'native exact schema')
    need(load(P/'.zenodo.json')==meta and load(P/'zenodo-metadata.json')==load(K/'zenodo-metadata.json')=={'metadata':meta},'native metadata agreement')
    need(load(F/'before/DEPOSIT_BINDING.json')['metadata']==meta,'metadata unchanged')
    need((P/'TERMINAL_ADMIN.json').read_bytes()==(K/'TERMINAL_ADMIN.json').read_bytes(),'terminal dual interface')
    write(F/'HISTORICAL_LOCATOR_REBINDINGS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Exact old records stay unchanged; terminal before copies resolve these five stale active verifier locators. No old history is rewritten.','entries':rebindings})
    need(len(rebindings)==5,'exact five verifier-history locator rebindings')
    return {'frozen':683,'unchanged':676,'changed':changed,'source_copy_pairs':37,'old_stage_rows':1127,'terminal_prior_rows':4025,'old_locator_rebindings':len(rebindings),'resolution_counts_both_layers':stage_counts,
            'original165_partition':[83,82],'repair332_partition':[233,99],'native_metadata_and_manifest_unchanged':True}
def main():
    result=custody();source=closed_zip();scratch=Path(tempfile.mkdtemp(prefix='pr1097-terminal-',dir='/private/tmp'))
    status='RUNNING';failure=None;guard_rows=[];semantic_rows=[]
    try:
        clean=scratch/'CleanKit';clean.mkdir()
        with zipfile.ZipFile(io.BytesIO(source)) as z:z.extractall(clean)
        clean_before=tree(clean);manifest=clean/'MANIFEST.json';saved_manifest=manifest.read_bytes()
        saved={q.relative_to(clean).as_posix():q.read_bytes() for q in [clean/'TERMINAL_ADMIN.json',clean/'PROTECTED_PATHS.json',clean/'provenance/terminal_admin_20261016/COPIES.json',clean/'provenance/terminal_admin_20261016/selected/ROOT_WHOLE_PACKAGE_REVIEW_02.json',clean/'provenance/terminal_admin_20261016/selected/reviews/package_02/VERDICT.json']}
        def refresh():
            value=json.loads(saved_manifest)
            for row in value['entries']:row.update(pin(clean/row['path']))
            write(manifest,value)
        def restore():
            for n,b in saved.items():(clean/n).write_bytes(b)
            manifest.write_bytes(saved_manifest)
        def update_copy(name):
            q=clean/'provenance/terminal_admin_20261016/COPIES.json';v=load(q)
            for row in v['entries']:
                if row['copy_path']==name:row.update(pin(clean/name))
            write(q,v);refresh()
        bindir=scratch/'bin';bindir.mkdir();marker=scratch/'compiler-marker';fake=bindir/'tectonic'
        fake.write_text('#!/bin/sh\nprintf invoked > "$TERMINAL1097_MARKER"\nexit 97\n');fake.chmod(0o700)
        env=dict(os.environ);env['PATH']=str(bindir)+os.pathsep+env.get('PATH','');env['TERMINAL1097_MARKER']=str(marker)
        original=scratch/'OriginalRoot';original.mkdir();(original/'nested').mkdir();(original/'sentinel').write_bytes(b'original sentinel\n')
        accented=scratch/'Caf\u00e9Root';accented.mkdir();(accented/'sentinel').write_bytes(b'unicode sentinel\n');absent=scratch/'AbsentOriginal'
        original_before=tree(original);accented_before=tree(accented)
        for tag,flags in [('normal',['-B']),('optimized',['-O','-B'])]:
            base=[sys.executable]+flags
            need(json.loads(run(base+['scripts/verify.py'],clean,'clean optional '+tag))['binding']['state']=='ABSENT_OPTIONAL','optional absent')
            math=json.loads(run(base+['scripts/run_checks.py'],clean,'clean math '+tag));need(math==load(clean/'EXPECTED_RESULTS.json'),'complete math JSON expected');write(F/('MATH_'+tag.upper()+'.json'),math)
            run(base+['scripts/run_checks.py','--inject-failure'],clean,'unconditional math failure '+tag,False)
            run(base+['scripts/verify.py','--require-binding'],clean,'required absent '+tag,False)
            run(base+['scripts/verify.py','--binding',scratch/'missing.json'],clean,'explicit missing '+tag,False)
            run(base+['scripts/verify.py','--binding',P/'DEPOSIT_BINDING.json','--require-binding'],clean,'explicit present required '+tag)
            out=scratch/(tag+'.zip');run(base+['scripts/build_support.py','--out',out],clean,'actual clean archive '+tag);need(out.read_bytes()==source,'supported archive exact');out.unlink()
            # Build a complete disposable delivery once per mode; default binding may never silently skip.
            for name in ['paper.pdf','pr1097_support_v1_0.zip','.zenodo.json','zenodo-metadata.json','zenodo-deposit.json','DEPOSIT_BINDING.json']:shutil.copyfile(P/name,scratch/name)
            run(base+['scripts/verify.py'],clean,'default present '+tag);run(base+['scripts/verify.py','--require-binding'],clean,'default required present '+tag)
            binding=scratch/'DEPOSIT_BINDING.json';binding_saved=binding.read_bytes()
            for kind in ['asset-hash','manifest-hash','metadata','file-order']:
                v=json.loads(binding_saved)
                if kind=='asset-hash':v['files'][1]['sha256']='0'*64
                if kind=='manifest-hash':v['kit_manifest_sha256']='0'*64
                if kind=='metadata':v['metadata']['title']='corrupt title'
                if kind=='file-order':v['files'].reverse()
                write(binding,v);run(base+['scripts/verify.py'],clean,'default corrupt '+kind+' '+tag,False);binding.write_bytes(binding_saved)
            # Native wrapper corruption with a valid binding reaches native semantic checks.
            native=scratch/'zenodo-deposit.json';b=native.read_bytes();v=json.loads(b);v['files'].reverse();write(native,v)
            run(base+['scripts/verify.py','--require-binding'],clean,'native file order '+tag,False);native.write_bytes(b)
            wrapper=scratch/'zenodo-metadata.json';b=wrapper.read_bytes();v=json.loads(b);v['metadata']['notes']='corrupt';write(wrapper,v)
            run(base+['scripts/verify.py'],clean,'wrapper mismatch '+tag,False);wrapper.write_bytes(b)
            binding.unlink();binding.symlink_to(scratch/'nonexistent-binding')
            run(base+['scripts/verify.py'],clean,'broken present binding '+tag,False,expect_text='symlink component');binding.unlink()
            for name in ['paper.pdf','pr1097_support_v1_0.zip','.zenodo.json','zenodo-metadata.json','zenodo-deposit.json']:(scratch/name).unlink()
            # Coherent terminal faults: inventory and copy hashes refreshed to reach semantic checks.
            faults=[('complete_whole_package_reviews_completed',1),('minimum_complete_whole_package_reviews_required',1),('latest_whole_review_root_adopted',False),('repair01_root_adopted',False),('further_complete_whole_review_currently_required',True),('external_ROOT_final_integrity_required',False),('external_ROOT_final_integrity_adopted',True),('publication_ready',True),('issues_resolved',True),('published',True),('ordered_service_hold_pr',1033),('historical_omitted_program_replayed',True)]
            for key,bad in faults:
                value=json.loads(saved['TERMINAL_ADMIN.json']);value[key]=bad;write(clean/'TERMINAL_ADMIN.json',value);refresh()
                run(base+['scripts/verify.py'],clean,'coherent terminal '+key+' '+tag,False,expect_text='terminal semantic mismatch: '+key);semantic_rows.append({'mode':tag,'field':key,'manifest_refreshed':True,'semantic_guard_reached':True});restore()
            root_name='provenance/terminal_admin_20261016/selected/ROOT_WHOLE_PACKAGE_REVIEW_02.json';v=json.loads(saved[root_name]);v['whole_reviews_completed']=1;write(clean/root_name,v);update_copy(root_name)
            run(base+['scripts/verify.py'],clean,'coherent ROOT adoption '+tag,False,expect_text='terminal ROOT adoption mismatch');semantic_rows.append({'mode':tag,'field':'ROOT adopted review count','copy_and_manifest_refreshed':True,'semantic_guard_reached':True});restore()
            verdict_name='provenance/terminal_admin_20261016/selected/reviews/package_02/VERDICT.json';v=json.loads(saved[verdict_name]);v['finding_counts']['P3']=1;write(clean/verdict_name,v);update_copy(verdict_name)
            run(base+['scripts/verify.py'],clean,'coherent latest verdict '+tag,False,expect_text='terminal whole02 verdict mismatch');semantic_rows.append({'mode':tag,'field':'latest verdict P3','copy_and_manifest_refreshed':True,'semantic_guard_reached':True});restore()
            # Bootstrap regularity is checked before parsing malformed linked content.
            malformed=scratch/(tag+'-malformed');malformed.write_bytes(b'not JSON')
            manifest.unlink();manifest.symlink_to(malformed)
            for script,extra in [('verify.py',[]),('build_support.py',['--out',scratch/(tag+'-bootstrap.zip')]),('rebuild_pdf.py',['--out-dir',scratch/(tag+'-bootstrap-pdf')])]:
                run(base+['scripts/'+script]+extra,clean,'manifest symlink preparse '+script+' '+tag,False,env,expect_text='symlink component')
            manifest.unlink();manifest.mkdir();run(base+['scripts/verify.py'],clean,'directory manifest '+tag,False,expect_text='input must be regular');manifest.rmdir();manifest.write_bytes(saved_manifest)
            link_ancestor=scratch/(tag+'-linked-kit');link_ancestor.symlink_to(clean,target_is_directory=True)
            code='import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import common;common.KIT=Path(sys.argv[2]);common.inventory()'
            run(base+['-c',code,clean/'scripts',link_ancestor],clean,'direct linked kit ancestry '+tag,False,expect_text='symlink component')
            # Every rejected writer uses disposable targets; no canonical inode alias is a target.
            sentinel=scratch/(tag+'-sentinel');sentinel.write_bytes(b'untouched disposable target\n')
            hard=scratch/(tag+'-hard');os.link(sentinel,hard)
            leaf=scratch/(tag+'-symlink');leaf.symlink_to(sentinel)
            ancestor=scratch/(tag+'-ancestor');ancestor.symlink_to(scratch,target_is_directory=True)
            occupied=scratch/(tag+'-occupied');occupied.mkdir()
            for n in ['paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt']:os.link(sentinel,occupied/n)
            target_before=pin(sentinel)
            for script,opt in [('build_support.py','--out'),('rebuild_pdf.py','--out-dir')]:
                for target,kind in [(hard,'hardlink leaf'),(leaf,'symlink leaf'),(ancestor/'new','linked ancestor'),(occupied,'occupied PDF child directory'),(clean/'new','protected root'),(clean/'provenance/new','protected nested'),(scratch/'..'/('traversal-'+tag),'traversal'),(scratch/'missing-parent/new','missing parent')]:
                    run(base+['scripts/'+script,opt,target],clean,'writer '+kind+' '+script+' '+tag,False,env);guard_rows.append({'mode':tag,'writer':script,'kind':kind,'exit_nonzero':True,'compiler_marker_absent':not marker.exists()})
                alias=scratch/'CLEANKIT';need(alias.exists() and os.path.samefile(alias,clean),'actual physical kit case alias unavailable')
                run(base+['scripts/'+script,opt,alias/('physical-'+tag)],clean,'physical kit case '+script+' '+tag,False,env,expect_text='aliases a protected root');guard_rows.append({'mode':tag,'writer':script,'kind':'physical kit case','samefile_asserted':True,'compiler_marker_absent':not marker.exists()})
            need(pin(sentinel)==target_before and all(pin(occupied/n)==target_before for n in ['paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt']),'disposable leaf or PDF child modified')
            config=clean/'PROTECTED_PATHS.json';v=json.loads(saved['PROTECTED_PATHS.json']);v['original_protected_roots']=list(map(str,[original,accented,absent]));write(config,v);refresh()
            for root,alias,kind in [(original,scratch/'ORIGINALROOT','original case'),(accented,scratch/'Cafe\u0301Root','normalization')]:
                need(alias.exists() and os.path.samefile(alias,root),'physical alias unavailable '+kind)
                for script,opt in [('build_support.py','--out'),('rebuild_pdf.py','--out-dir')]:
                    run(base+['scripts/'+script,opt,alias/('new-'+tag)],clean,'physical '+kind+' '+script+' '+tag,False,env,expect_text='aliases a protected root');guard_rows.append({'mode':tag,'writer':script,'kind':kind,'samefile_asserted':True,'compiler_marker_absent':not marker.exists()})
            # Reverse spelling: alias in configuration, ordinary spelling in requested output.
            v['original_protected_roots']=[str(scratch/'ORIGINALROOT'),str(scratch/'Cafe\u0301Root')];write(config,v);refresh()
            for root in [original,accented]:
                for script,opt in [('build_support.py','--out'),('rebuild_pdf.py','--out-dir')]:
                    run(base+['scripts/'+script,opt,root/('reverse-'+tag)],clean,'reverse physical alias '+script+' '+tag,False,env,expect_text='aliases a protected root')
            v['original_protected_roots']=[str(absent)];write(config,v);refresh();run(base+['scripts/verify.py'],clean,'absent original verification '+tag)
            out=scratch/(tag+'-absent.zip');run(base+['scripts/build_support.py','--out',out],clean,'absent original actual archive '+tag);out.unlink()
            # Test common preflight permits a fresh directory with the original root absent; no PDF/authoring operation.
            code='import sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from common import fresh_output;fresh_output(sys.argv[2],is_directory=True)'
            allowed=scratch/(tag+'-allowed-directory');run(base+['-c',code,clean/'scripts',allowed],clean,'absent original directory preflight only '+tag);allowed.rmdir()
            need(tree(original)==original_before and tree(accented)==accented_before,'disposable original changed');restore()
            run(base+['scripts/verify.py','--binding',P/'DEPOSIT_BINDING.json','--require-binding'],clean,'restored explicit required '+tag)
            need(tree(clean)==clean_before,'clean extraction exact restoration')
            need(not marker.exists(),'rejected PDF request invoked compiler')
        need(load(F/'MATH_NORMAL.json')==load(F/'MATH_OPTIMIZED.json')==load(K/'EXPECTED_RESULTS.json'),'complete math equality both modes')
        repo=Path('/Users/alec/Documents/Math')
        native=json.loads(run([sys.executable,'-B',repo/'zenodo_deposit_tool/zenodo.py','check',P/'zenodo-deposit.json'],repo,'actual native repository LOCAL check'))
        result.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',complete_math_JSON_equals_EXPECTED_both_modes=True,
           unconditional_failures_both_modes=True,semantic_faults=semantic_rows,writer_guards=guard_rows,command_count=len(commands),expected_failures=sum(not r['expected_success'] for r in commands),
           closed_ZIP_members=198,actual_native_repository_local_check=native,no_compiler_or_render_or_PDF_authoring_operation=True,compiler_marker_absent=True,
           canonical_paper=pin(P/'paper.pdf'),archive=pin(P/'pr1097_support_v1_0.zip'),publication_ready=False,issues_resolved=False,published=False,services_held_after_pr=1032)
        custody();write(F/'VALIDATION.json',result);status='PASS'
        print(json.dumps({k:result[k] for k in ['status','command_count','expected_failures','closed_ZIP_members','archive']},indent=2))
    except BaseException as exc:
        status='FAIL';failure={'type':type(exc).__name__,'message':str(exc)};raise
    finally:
        receipt_name='COMMAND_RECEIPTS.json' if status=='PASS' else 'FAILED_COMMAND_RECEIPTS_'+datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')+'.json'
        write(F/receipt_name,{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'failure':failure,'entries':commands})
        rows=[{'path':q.relative_to(scratch).as_posix(),**pin(q)} for q in sorted(scratch.rglob('*')) if q.is_file() and not q.is_symlink()]
        write(F/('SCRATCH_CLEANUP.json' if status=='PASS' else 'FAILED_SCRATCH_CLEANUP_'+datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')+'.json'),{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scratch':str(scratch),'files':rows,'all_individually_pinned_before_removing_only_owned_scratch':True})
        shutil.rmtree(scratch)
if __name__=='__main__':main()
