#!/usr/bin/env python3
"""Independent bounded filesystem/replay/custody controls; standard library."""
import hashlib, io, json, os, shutil, subprocess, sys, tempfile, zipfile
sys.dont_write_bytecode = True
from datetime import datetime, timezone
from pathlib import Path
D=Path(__file__).resolve().parent
A=D.parents[1]
P=A/'NEWpreprint_v1_0'
PROGRAM=A.parents[1]
REPO=A.parents[2]
ARCHIVE='PR1071_preprint_v1_0_support.zip'
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def write(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
def pin(p,n):
    b=p.read_bytes();return {'path':str(n),'bytes':len(b),'sha256':sha(b)}
def matches(p,r):
    return p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p.read_bytes())==r['sha256']
def check(p,r): need(matches(p,r),'Identity mismatch: '+str(p))
def log(message,percent):
    with (D/'RESEARCH_LOG.md').open('a') as f: f.write('\n'+datetime.now(timezone.utc).isoformat()+': '+message+' Bounded completion estimate '+str(percent)+'%.\n')

def custody():
    authorized=read(D/'AUTHORIZED_EXISTING_CHANGES.json')['records']
    before={r['path']:A/r['before_bytes_path_relative_to_audit'] for r in authorized}
    baseline=read(D/'BASELINE_INPUT_PINS.json')['records']
    unchanged=[];changed=[]
    for r in baseline:
        p=A/r['path']
        if r['path'] in before:
            check(before[r['path']],r); need(not matches(p,r),'Expected authorized mutation absent')
            changed.append({'path':r['path'],'before':r,'after':pin(p,r['path']),'before_bytes_path_relative_to_audit':str(before[r['path']].relative_to(A))})
        else: check(p,r);unchanged.append(r)
    need(len(changed)==9,'Mutation boundary drift')
    for r in read(D/'CORE_PROTECTED_IDENTITIES.json')['records']:check(A/r['path'],r)
    for r in read(D/'PROGRAM_SOURCE_PINS.json')['records']:check(PROGRAM/r['path'],r)
    old=read(A/'finalization/terminal_admin_20261015/HISTORICAL_STAGE_RESOLUTION.json')
    need(len(old['records'])==2788,'Historical row count drift')
    resolved=[]
    for index,r in enumerate(old['records']):
        actual=A/r['resolved_path']
        candidates=[actual]
        if r['resolved_path'] in before:candidates.append(before[r['resolved_path']])
        chosen=next((p for p in candidates if matches(p,r)),None)
        need(chosen is not None,'Unresolved old stage '+str(index)+' '+r['resolved_path'])
        resolved.append({**r,'prior_resolution_path':r['resolved_path'],'resolved_path':str(chosen.relative_to(A)) if chosen.is_relative_to(A) else str(chosen),'prior_row_index':index})
    # Recheck every later terminal capture as well as all 2,788 old rows.
    terminal=A/'finalization/terminal_admin_20261015'
    later=[]
    for name,key,base in [('OUTPUT_PINS.json','records',terminal),('CURRENT_CANDIDATE_PINS.json','records',P),('CURRENT_AUDIT_PINS.json','records',A),('PROTECTED_UNCHANGED.json','records',A)]:
        for r in read(terminal/name)[key]:
            actual=base/r['path'];candidates=[actual]
            rel=str(actual.relative_to(A))
            if rel in before:candidates.append(before[rel])
            chosen=next((p for p in candidates if matches(p,r)),None)
            need(chosen is not None,'Unresolved later terminal '+name+' '+rel)
            later.append({'stage':name,'captured_path':r['path'],'resolved_path':str(chosen.relative_to(A)),'bytes':r['bytes'],'sha256':r['sha256']})
    oldmap=read(D/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies']
    current=read(P/'INPUT_COPY_MAP.json')['copies']
    need(len(oldmap)==116 and current[:116]==oldmap,'Original 116 copy rows/order drift')
    pairs=[]
    for r in current:
        src=A/r.get('source_snapshot',r['original_path']);dst=P/r['package_copy']
        check(src,r);check(dst,r);need(src.read_bytes()==dst.read_bytes(),'Source copy inequality')
        pairs.append({'original_path':r['original_path'],'source_resolved':str(src.relative_to(A)),'package_copy':r['package_copy'],'bytes':r['bytes'],'sha256':r['sha256']})
    for name in ['WHOLE01_COPY_EXCLUSIONS.json','WHOLE02_COPY_EXCLUSIONS.json','CASE_ALIAS_COPY_EXCLUSIONS.json']:
        for r in read(P/name)['records']:check((PROGRAM if r.get('base')=='program_root' else A)/r['path'],r)
    workspace=read(P/'FROZEN_INPUTS.json')['workspace_AGENTS'];check(Path(workspace['path']),workspace)
    native=read(A/'publication/zenodo-deposit.json')
    need(set(native)=={'metadata','files'},'Native shape drift')
    metadata=read(P/'metadata.json')
    need(metadata==read(P/'metadata_wrapped.json')['metadata']==read(P/'deposit.json')['metadata']==native['metadata'],'Native bibliographic object drift')
    need(native['files']==[{'path':'../NEWpreprint_v1_0/paper.pdf','name':'paper.pdf'},{'path':'../NEWpreprint_v1_0/'+ARCHIVE,'name':ARCHIVE}],'Native asset selection drift')
    binding=read(P/'UPLOAD_BINDINGS.json');previous=read(D/'before/NEWpreprint_v1_0/UPLOAD_BINDINGS.json')
    adjusted=json.loads(json.dumps(binding));adjusted['archive']['bytes']=previous['archive']['bytes'];adjusted['archive']['sha256']=previous['archive']['sha256'];adjusted['manifest_sha256']=previous['manifest_sha256']
    need(adjusted==previous,'Unnecessary external binding change')
    check(P/ARCHIVE,{'bytes':binding['archive']['bytes'],'sha256':binding['archive']['sha256']})
    need((P/(ARCHIVE+'.sha256')).read_text()==binding['archive']['sha256']+'  '+ARCHIVE+'\n','Sidecar drift')
    write(D/'HISTORICAL_STAGE_RESOLUTION.json',{'status':'PASS','original_stage_counts':old['stage_counts'],'all_original_rows_preserved_in_order':True,'original_rows':len(resolved),'records':resolved,'additional_terminal_rows':later})
    write(D/'COPY_EQUALITY_RECHECK.json',{'status':'PASS','first_116_exact_rows_order_unchanged':True,'records':pairs})
    oldnames={r['path'] for r in baseline}
    write(D/'CHANGE_INVENTORY.json',{'authorized_existing_changes':changed,'all_new_paths_outside_effort':[pin(f,f.relative_to(A)) for f in sorted(A.rglob('*')) if f.is_file() and not f.is_symlink() and not f.is_relative_to(D) and str(f.relative_to(A)) not in oldnames]})
    write(D/'PROTECTED_UNCHANGED.json',{'status':'PASS','records':unchanged})
    return {'baseline_regular_files':len(baseline),'existing_changes':len(changed),'protected_unchanged':len(unchanged),'original_terminal_stage_rows':len(resolved),'additional_terminal_rows':len(later),'copy_pairs':len(pairs),'first_116_unchanged_ordered':True,'all_native_metadata_and_manifest_bytes_unchanged':True,'only_required_binding_scalars_changed':True,'workspace_AGENTS_unchanged':True}

def controls():
    scratch=D/'_scratch';scratch.mkdir(exist_ok=True)
    stream=D/'COMMAND_STREAM.jsonl'
    need(not stream.exists(),'Do not overwrite a previous actual-command stream')
    command_count=0;successes=0;case_records=[];api=[];semantics=[]
    with tempfile.TemporaryDirectory(prefix='one-kit-',dir=scratch) as temp:
        t=Path(temp).resolve();root=t/'kit';alias=t/'KIT';root.mkdir()
        with zipfile.ZipFile(P/ARCHIVE) as z:
            names=z.namelist()
            need(names==sorted(names) and len(names)==len(set(names)),'ZIP names/order')
            for i in z.infolist():
                need(not Path(i.filename).is_absolute() and all(x not in ('','.','..') for x in i.filename.split('/')),'Unsafe ZIP member')
                need(i.create_system==3 and i.compress_type==zipfile.ZIP_STORED and i.date_time==(2026,10,14,0,0,0) and i.external_attr==0o100644<<16 and not i.extra and not i.comment,'ZIP header drift')
                need(z.read(i.filename)==(P/i.filename).read_bytes(),'ZIP payload mismatch')
            need(z.testzip() is None,'ZIP CRC failure');z.extractall(root)
        original={str(f.relative_to(root)):f.read_bytes() for f in root.rglob('*') if f.is_file()}
        need(root.samefile(alias) and root.stat().st_dev==alias.stat().st_dev and root.stat().st_ino==alias.stat().st_ino and root.resolve()!=alias.resolve(),'Actual case-insensitive samefile precondition failed')
        need((root/'custody').samefile(alias/'CUSTODY'),'Nested case alias precondition failed')
        identity={'canonical':str(root),'case_alias':str(alias),'samefile':True,'canonical_resolve':str(root.resolve()),'alias_resolve':str(alias.resolve()),'device':root.stat().st_dev,'inode':root.stat().st_ino,'nested_custody_samefile':True}
        write(D/'ACTUAL_CASE_IDENTITY.json',identity)
        buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,'w',compression=0,allowZip64=False) as z:
            for name,data in sorted(original.items()):
                i=zipfile.ZipInfo(name,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=0;z.writestr(i,data)
        need(buffer.getvalue()==(P/ARCHIVE).read_bytes(),'Independent CLOSED archive differs')
        write(D/'INDEPENDENT_CLOSED_ZIP.json',{'status':'PASS','members':len(original),'headers_payloads_CRC_checked':True,'closed_before_byte_comparison':True,'byte_equal':True,'archive':pin(P/ARCHIVE,ARCHIVE)})
        def snapshot():return {str(f.relative_to(root)):sha(f.read_bytes()) for f in root.rglob('*') if f.is_file() and not f.is_symlink()}
        initial_snapshot={n:sha(b) for n,b in original.items()}
        def run(mode,label,args,success=True,expected_message=None,cwd=root):
            nonlocal command_count,successes
            argv=[sys.executable,'-B',*(['-O'] if mode else []),*map(str,args)]
            proc=subprocess.run(argv,cwd=cwd,capture_output=True,text=True)
            row={'index':command_count,'utc':datetime.now(timezone.utc).isoformat(),'mode':'optimized' if mode else 'normal','label':label,'argv':argv,'cwd':str(cwd),'returncode':proc.returncode,'expected_success':success,'stdout':proc.stdout,'stderr':proc.stderr}
            with stream.open('a') as f:f.write(json.dumps(row,sort_keys=True)+'\n')
            command_count+=1;successes+=int(success)
            need((proc.returncode==0)==success,'Unexpected command result '+label+': '+proc.stderr)
            if expected_message:need(expected_message in proc.stderr,'Wrong rejection '+label+': '+proc.stderr)
            return proc
        outside=t/'outside';outside.mkdir();outside_alias=t/'OUTSIDE'
        need(outside.samefile(outside_alias),'Safe outside case alias precondition failed')
        # Every writer: normal/-O, both script-root case spellings and both output spellings.
        for mode in [False,True]:
            tag='optimized' if mode else 'normal'
            for scriptbase,direction in [(root,'canonical_script'),(alias,'case_alias_script')]:
                for cli in ['build_archive.py','check.py','build_pdf.py']:
                    for target,label in [(root/'new-output','canonical_inside'),(alias/'new-output','alias_inside'),(root/'custody/new-output','canonical_nested'),(alias/'CUSTODY/new-output','alias_nested'),(root/'absent-one/absent-two/new-output','canonical_missing_intermediates'),(alias/'ABSENT-ONE/ABSENT-TWO/new-output','alias_missing_intermediates')]:
                        args=[scriptbase/'scripts'/cli,'--out',target]
                        if cli=='build_pdf.py':args+=['--tectonic','/nonexistent/pr1071-no-compiler-may-run']
                        before=snapshot();proc=run(mode,direction+'_'+cli+'_'+label,args,False,'Output must be outside all frozen package descendants.')
                        need(not target.exists() and not target.is_symlink() and snapshot()==before,'Rejected internal output wrote content')
                        need(not (root/'absent-one').exists(),'Missing intermediate directory was created')
                        case_records.append({'mode':tag,'script_case':direction,'writer':cli,'case':label,'physical_alias_test':True,'rejected_before_any_write':True,'compiler_not_invoked':cli=='build_pdf.py','stderr_sha256':sha(proc.stderr.encode())})
            # Actual external commands include safe case aliases; the physical identity rule must not overreject.
            run(mode,'documented_default_verify',[root/'scripts/verify_package.py'])
            run(mode,'documented_checker',[root/'scripts/check.py','--out',outside/('check-'+tag)])
            run(mode,'safe_outside_case_alias_checker',[alias/'scripts/check.py','--out',outside_alias/('check-case-'+tag)])
            run(mode,'default_temporary_checker',[root/'scripts/check.py'])
            for prefix,outparent,scriptbase in [('documented_archive',outside,root),('safe_outside_case_alias_archive',outside_alias,alias)]:
                dest=outparent/(prefix+'-'+tag+'.zip');run(mode,prefix,[scriptbase/'scripts/build_archive.py','--out',dest]);need(dest.read_bytes()==(P/ARCHIVE).read_bytes(),'External rebuild byte mismatch')
            run(mode,'strict_present_bindings',[root/'scripts/verify_package.py','--require-bindings','--bindings',P/'UPLOAD_BINDINGS.json','--archive',P/ARCHIVE])
            run(mode,'required_missing_bindings',[root/'scripts/verify_package.py','--require-bindings','--bindings',t/'missing-bindings.json'],False,'Required bindings are absent.')
            for fault in ['malformed','bad_pdf','bad_zip','bad_manifest','missing_archive']:
                b=read(P/'UPLOAD_BINDINGS.json');f=t/('binding-'+fault+'-'+tag+'.json')
                if fault=='malformed':f.write_text('{bad')
                else:
                    if fault in ['bad_pdf','bad_zip']:b['pdf' if fault=='bad_pdf' else 'archive']['sha256']='0'*64
                    if fault=='bad_manifest':b['manifest_sha256']='0'*64
                    write(f,b)
                run(mode,'binding_'+fault,[root/'scripts/verify_package.py','--require-bindings','--bindings',f,'--archive',t/'missing.zip' if fault=='missing_archive' else P/ARCHIVE],False)
                f.unlink()
            # Established existing-output, link, missing-parent and child-file boundaries.
            canary=outside/('canary-'+tag);canary.write_bytes(b'protected disposable canary\n');canary_before=canary.read_bytes()
            realparent=outside/('real-'+tag);realparent.mkdir()
            linked=outside/('linked-'+tag);linked.symlink_to(realparent,target_is_directory=True)
            parentfile=outside/('parentfile-'+tag);parentfile.write_bytes(b'not a directory')
            reused=outside/('reused-'+tag);reused.mkdir()
            child_names=['paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt','CHECK_RECEIPT.json','original_finite_checks.py','normal/FINITE_CHECKS.json','optimized/FINITE_CHECKS.json','normal/stdout.txt','normal/stderr.txt','optimized/stdout.txt','optimized/stderr.txt']
            for idx,name in enumerate(child_names):
                q=reused/name;q.parent.mkdir(parents=True,exist_ok=True)
                if idx%2:q.symlink_to(canary)
                else:os.link(canary,q)
            for cli in ['build_archive.py','check.py','build_pdf.py']:
                for fault in ['existing_file','existing_dir_with_child_aliases','hardlink','symlink','dangling','linked_parent','linked_above_missing','missing_outside_parent','nondirectory_parent','dotdot','symlink_dotdot']:
                    leaf=outside/(fault+'-'+cli+'-'+tag)
                    if fault=='existing_file':target=root/'paper.tex'
                    elif fault=='existing_dir_with_child_aliases':target=reused
                    elif fault=='hardlink':os.link(canary,leaf);target=leaf
                    elif fault=='symlink':leaf.symlink_to(canary);target=leaf
                    elif fault=='dangling':leaf.symlink_to(outside/'no-such-target');target=leaf
                    elif fault=='linked_parent':target=linked/'new-file'
                    elif fault=='linked_above_missing':target=linked/'absent-a/absent-b/new-file'
                    elif fault=='missing_outside_parent':target=outside/'absent-parent/new-file'
                    elif fault=='nondirectory_parent':target=parentfile/'new-file'
                    elif fault=='dotdot':target=realparent/'..'/'new-file'
                    else:target=linked/'..'/'new-file'
                    args=[root/'scripts'/cli,'--out',target]
                    if cli=='build_pdf.py':args+=['--tectonic','/nonexistent/pr1071-no-compiler-may-run']
                    proc=run(mode,'normal_fault_'+cli+'_'+fault,args,False)
                    need('FileNotFoundError' not in proc.stderr,'Compiler/process execution escaped rejection')
                    need(canary.read_bytes()==canary_before and snapshot()==initial_snapshot,'Protected bytes changed')
                    if fault in ['hardlink','symlink','dangling']:leaf.unlink()
            # Every distributed protected file, all protected core forms and native/binding interfaces.
            # Only disposable extraction/copies receive aliases; no canonical inode is linked.
            targets=[root/name for name in sorted(original)]
            copydir=t/('small-protected-copies-'+tag);copydir.mkdir()
            for idx,r in enumerate(read(D/'CORE_PROTECTED_IDENTITIES.json')['records']):
                q=copydir/str(idx);q.write_bytes((A/r['path']).read_bytes());check(q,r);targets.append(q)
            q=copydir/'binding';q.write_bytes((P/'UPLOAD_BINDINGS.json').read_bytes());targets.append(q)
            targetlist=t/('api-targets-'+tag+'.json');write(targetlist,[str(q) for q in targets])
            probe=t/'api_probe.py'
            probe.write_text('''import importlib.util,json,os,sys
from pathlib import Path
sys.dont_write_bytecode=True
root=Path(sys.argv[1]);outside=Path(sys.argv[2]);targets=json.loads(Path(sys.argv[3]).read_text())
s=importlib.util.spec_from_file_location('guard',root/'scripts/package_paths.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
count=0
for name in targets:
 p=Path(name)
 for kind in ['direct','hardlink','symlink']:
  q=p if kind=='direct' else outside/('alias-'+kind)
  if kind=='hardlink':os.link(p,q)
  if kind=='symlink':q.symlink_to(p)
  try:
   try:m.fresh_output(q,root)
   except RuntimeError:count+=1
   else:raise RuntimeError('Existing protected output accepted: '+str(q))
  finally:
   if kind!='direct':q.unlink()
# Physically external output directories, including case aliases, are allowed.
for frozen in [root,root.parent/'KIT']:
 for parent in [outside,outside.parent/'OUTSIDE']:
  q=parent/'new-absent-output';r=m.fresh_output(q,frozen)
  if r.exists():raise RuntimeError('Preflight created output')
print(json.dumps({'protected_targets':len(targets),'existing_output_rejections':count,'safe_outside_case_directions':4,'all_canonical_alias_targets_avoided':True},sort_keys=True))
''')
            proc=run(mode,'all_protected_output_alias_api',[probe,root,outside,targetlist]);api.append({'mode':tag,**json.loads(proc.stdout)})
            shutil.rmtree(copydir);targetlist.unlink();probe.unlink()
            # New current-state checks are challenged after coherent manifest refresh.
            def restore(name):(root/name).write_bytes(original[name])
            def refresh():
                m=json.loads(original['PACKAGE_MANIFEST.json'])
                for row in m['members']:row.update(pin(root/row['path'],row['path']))
                write(root/'PACKAGE_MANIFEST.json',m)
            alterations=[('state','OLD_READY'),('fresh_whole_package_reviews_completed',1),('minimum_fresh_reviews_required',1),('new_complete_whole_review_required',2),('new_complete_whole_review_completed',True),('bounded_repair_findings_fixed',[]),('root_repair_adoption_required',False),('root_terminal_adoption_required',False),('publication_ready',True),('issues_resolved',True),('published',True),('services_held_after_pr',0)]
            for field,value in alterations:
                v=json.loads(original['CASE_ALIAS_REPAIR_STATUS.json']);v[field]=value;write(root/'CASE_ALIAS_REPAIR_STATUS.json',v);refresh()
                proc=run(mode,'current_state_'+field,[root/'scripts/verify_package.py'],False)
                semantics.append({'mode':tag,'field':field,'coherent_manifest_rejection':True,'stderr_sha256':sha(proc.stderr.encode())})
                restore('CASE_ALIAS_REPAIR_STATUS.json');restore('PACKAGE_MANIFEST.json')
            for bad in [False,True]:
                external=t/'bootstrap-manifest.json';external.write_bytes(b'{bad' if bad else original['PACKAGE_MANIFEST.json'])
                (root/'PACKAGE_MANIFEST.json').unlink();(root/'PACKAGE_MANIFEST.json').symlink_to(external)
                for cli,args in [('verify_package.py',[]),('build_archive.py',['--out',outside/('bootstrap-'+tag+str(bad)+'.zip')])]:
                    run(mode,'bootstrap_symlink_'+cli+str(bad),[root/'scripts'/cli,*args],False,'Symlink member/ancestor')
                (root/'PACKAGE_MANIFEST.json').unlink();restore('PACKAGE_MANIFEST.json');external.unlink()
            run(mode,'repeat_default_verify',[root/'scripts/verify_package.py'])
        need(snapshot()==initial_snapshot and {str(f.relative_to(root)):f.read_bytes() for f in root.rglob('*') if f.is_file()}==original,'Extraction changed after suite')
        proc=run(False,'native_repository_LOCAL_check',[REPO/'zenodo_deposit_tool/zenodo.py','check',A/'publication/zenodo-deposit.json'],cwd=REPO)
        write(D/'NATIVE_REPOSITORY_LOCAL_CHECK.json',{'local_only':True,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'native_manifest':pin(A/'publication/zenodo-deposit.json','publication/zenodo-deposit.json')})
        write(D/'CASE_ALIAS_WRITER_CONTROLS.json',{'actual_case_identity':identity,'actual_writer_rejections':len(case_records),'records':case_records,'one_disposable_extraction':True,'canonical_tree_aliases_never_used':True})
        write(D/'ALL_PROTECTED_OUTPUT_CONTROLS.json',{'records':api,'canonical_inputs_never_used_as_destructive_alias_targets':True,'new_child_output_directory_alias_controls':True})
        write(D/'CURRENT_STATUS_SEMANTIC_CONTROLS.json',{'records':semantics})
        result={'actual_commands':command_count,'expected_successes':successes,'expected_rejections':command_count-successes,'actual_case_alias_writer_controls':len(case_records),'protected_api':api,'current_status_mutations_rejected':len(semantics),'clean_extracted_members_unchanged':len(original),'independent_CLOSED_archive_byte_equal':True,'real_PDF_compile':False,'new_render_or_PDF_marker':False,'paper_unchanged_whole02_prior_compile_and_seven_page_view_preserved':True,'native_repository_LOCAL_check':True}
    write(D/'CONTROL_SUMMARY.json',result)
    return result

def main():
    c=custody();log('All baseline, source/copy/native objects, original 2,788 rows and later terminal captures rechecked before controls.',60)
    try:s=controls()
    except Exception as e:
        log('Control attempt stopped: '+type(e).__name__+': '+str(e)+'. Only the actual streamed command prefix is retained; full completion is not claimed.',60)
        raise
    after=custody();need(c==after,'Custody changed during controls')
    write(D/'FINAL_VERIFICATION.json',{'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','custody':after,'controls':s,'new_complete_whole03_required':True,'root_repair_and_terminal_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032})
    log('Actual normal/optimized writer, identity, safe-outside, strict-binding, semantic, native LOCAL and deterministic CLOSED-ZIP controls passed. Protected baseline unchanged outside nine authorized edits.',95)
    print(json.dumps(read(D/'FINAL_VERIFICATION.json'),indent=2))
if __name__=='__main__':main()
