#!/usr/bin/env python3
"""Independent terminal administrative integrity/replay controls, stdlib only."""
import hashlib, importlib.util, io, json, os, shutil, subprocess, sys, tempfile, zipfile
sys.dont_write_bytecode = True
from pathlib import Path

D=Path(__file__).resolve().parent
A=D.parents[1]
P=A/'NEWpreprint_v1_0'
REPO=A.parents[2]
ARCHIVE='PR1071_preprint_v1_0_support.zip'

def need(ok,msg):
    if not ok: raise RuntimeError(msg)

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def rows(o): return o.get('records',o.get('files'))
def pin(p,name):
    b=p.read_bytes();return {'path':str(name),'bytes':len(b),'sha256':sha(b)}
def check(p,r):
    need(p.is_file() and not p.is_symlink(),'Absent/nonregular '+str(p))
    b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'Identity '+str(p))
def write(p,v): p.write_text(json.dumps(v,indent=2)+'\n')

def stages():
    changes=read(D/'AUTHORIZED_EXISTING_CHANGES.json')['records']
    latest={r['path']:A/r['before_bytes_path_relative_to_audit'] for r in changes}
    previous={r['path']:A/r['before_bytes_path_relative_to_audit'] for r in read(A/'repairs/package01/CHANGE_INVENTORY.json')['authorized_existing_changes']}
    resolutions=[]
    def resolve(stage,row,path):
        name=str(path.relative_to(A)) if path.is_relative_to(A) else str(path)
        candidates=[path]
        if name in latest:candidates.append(latest[name])
        if name in previous:candidates.append(previous[name])
        for actual in candidates:
            if actual.is_file() and not actual.is_symlink():
                b=actual.read_bytes()
                if len(b)==row['bytes'] and sha(b)==row['sha256']:
                    resolutions.append({'stage':stage,'captured_path':row['path'],'resolved_path':str(actual.relative_to(A)) if actual.is_relative_to(A) else str(actual),'bytes':row['bytes'],'sha256':row['sha256']})
                    return
        raise RuntimeError('Unresolved '+stage+' '+name)
    sets=[('terminal_immediate_inputs',D/'BASELINE_INPUT_PINS.json',A,'records'),
          ('preparation_204',P/'FROZEN_INPUTS.json',A,'records'),
          ('preparation_92',P/'INPUT_OUTPUT_PINS.json',P,'records'),
          ('repair_492_before',A/'repairs/package01/BASELINE_INPUT_PINS.json',A,'records'),
          ('repair_34_outputs',A/'repairs/package01/OUTPUT_PINS.json',A/'repairs/package01','records'),
          ('repair_270_current',A/'repairs/package01/CURRENT_OUTPUT_PINS.json',P,'records'),
          ('repair_480_unchanged',A/'repairs/package01/PROTECTED_UNCHANGED.json',A,'unchanged_records'),
          ('whole01_25_outputs',A/'reviews/package_01/OUTPUT_PINS.json',A/'reviews/package_01','files'),
          ('whole02_25_outputs',A/'reviews/package_02/OUTPUT_PINS.json',A/'reviews/package_02','files'),
          ('whole02_569_inputs',A/'reviews/package_02/INPUT_PINS.json',A,'files')]
    counts={}
    for stage,file,base,key in sets:
        rr=read(file)[key]
        for r in rr:resolve(stage,r,base/r['path'])
        counts[stage]=len(rr)
    workspace=read(P/'FROZEN_INPUTS.json')['workspace_AGENTS'];check(Path(workspace['path']),workspace)
    original83=read(D/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies']
    current=read(P/'INPUT_COPY_MAP.json')['copies']
    need(len(original83)==83 and current[:83]==original83,'Original map rows or order changed')
    copies=[]
    for r in current:
        src=A/r.get('source_snapshot',r['original_path']);dest=P/r['package_copy']
        check(src,r);check(dest,r);need(src.read_bytes()==dest.read_bytes(),'Copy source equality')
        copies.append({'original_path':r['original_path'],'source_resolved':str(src.relative_to(A)),'package_copy':r['package_copy'],'bytes':r['bytes'],'sha256':r['sha256']})
    for name in ['WHOLE01_COPY_EXCLUSIONS.json','WHOLE02_COPY_EXCLUSIONS.json']:
        for r in read(P/name)['records']:check(A/r['path'],r)
    for r in read(D/'CORE_PROTECTED_IDENTITIES.json')['records']:check(A/r['path'],r)
    native=read(A/'publication/zenodo-deposit.json')
    need(set(native)=={'metadata','files'},'Native upload manifest shape')
    metadata=read(P/'metadata.json')
    need(metadata==read(P/'metadata_wrapped.json')['metadata']==read(P/'deposit.json')['metadata']==native['metadata'],'Native metadata object drift')
    need(native['files']==[{'path':'../NEWpreprint_v1_0/paper.pdf','name':'paper.pdf'},{'path':'../NEWpreprint_v1_0/'+ARCHIVE,'name':ARCHIVE}],'Native exact assets drift')
    baseline=read(D/'BASELINE_INPUT_PINS.json')['records'];authorized={r['path'] for r in changes}
    changed=[];unchanged=[]
    for r in baseline:
        actual=A/r['path']
        if r['path'] in authorized:
            check(latest[r['path']],r)
            need(pin(actual,r['path'])!=r,'Authorized path unexpectedly unchanged')
            changed.append({'path':r['path'],'before':r,'after':pin(actual,r['path']),'before_bytes_path_relative_to_audit':str(latest[r['path']].relative_to(A))})
        else:check(actual,r);unchanged.append(r)
    need(len(changed)==8,'Unexpected mutation count')
    write(D/'HISTORICAL_STAGE_RESOLUTION.json',{'status':'PASS','stage_counts':counts,'workspace_AGENTS_unchanged':True,'records':resolutions})
    write(D/'COPY_EQUALITY_RECHECK.json',{'status':'PASS','original_83_rows_and_order_unchanged':True,'records':copies})
    write(D/'CHANGE_INVENTORY.json',{'authorized_existing_changes':changed,'all_new_paths_outside_effort':[pin(f,f.relative_to(A)) for f in sorted(A.rglob('*')) if f.is_file() and not f.is_symlink() and not f.is_relative_to(D) and str(f.relative_to(A)) not in {r['path'] for r in baseline}]})
    write(D/'PROTECTED_UNCHANGED.json',{'records':unchanged})
    return {'stage_counts':counts,'all_stage_rows':len(resolutions),'source_equal_copies':len(copies),'authorized_existing_changes':len(changed),'unchanged_immediate_inputs':len(unchanged),'exact_native_metadata_and_assets':True,'protected_core_records':len(read(D/'CORE_PROTECTED_IDENTITIES.json')['records'])}

def controls():
    command_log=[];api_log=[];semantics=[]
    with tempfile.TemporaryDirectory(prefix='pr1071-terminal-',dir=D/'_scratch') as temp:
        t=Path(temp);root=t/'kit';root.mkdir()
        with zipfile.ZipFile(P/ARCHIVE) as z:z.extractall(root)
        original={str(f.relative_to(root)):f.read_bytes() for f in root.rglob('*') if f.is_file()}
        with zipfile.ZipFile(P/ARCHIVE) as z:
            need(z.testzip() is None,'ZIP CRC')
            need(z.namelist()==sorted(original),'ZIP order')
            for i in z.infolist():
                need(i.compress_type==zipfile.ZIP_STORED and i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16,'ZIP header')
                need(z.read(i.filename)==(P/i.filename).read_bytes(),'ZIP current payload')
        # Separately implemented deterministic reconstruction; inspect buffer only after close.
        buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,mode='w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
            for name,data in sorted(original.items()):
                entry=zipfile.ZipInfo(filename=name,date_time=(2026,10,14,0,0,0));entry.create_system=3;entry.compress_type=0;entry.external_attr=0o100644<<16
                z.writestr(entry,data)
        need(buffer.getvalue()==(P/ARCHIVE).read_bytes(),'Independent CLOSED ZIP differs')
        def restore(name):
            f=root/name
            if f.is_symlink() or f.is_file():f.unlink()
            elif f.is_dir():shutil.rmtree(f)
            f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(original[name])
        def manifest_refresh():
            m=json.loads(original['PACKAGE_MANIFEST.json'])
            for r in m['members']:
                p=root/r['path'];r['bytes']=p.stat().st_size;r['sha256']=sha(p.read_bytes())
            (root/'PACKAGE_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
        def run(mode,label,args,success=True,cwd=root):
            cmd=[sys.executable,'-B',*(['-O'] if mode else []),*map(str,args)]
            proc=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
            command_log.append({'mode':'optimized' if mode else 'normal','label':label,'argv':[str(x) for x in cmd],'returncode':proc.returncode,'expected_success':success,'stdout':proc.stdout,'stderr':proc.stderr})
            need((proc.returncode==0)==success,'Unexpected outcome '+label+': '+proc.stderr)
            return proc
        for mode in [False,True]:
            tag='optimized' if mode else 'normal'
            run(mode,'default_verify',['scripts/verify_package.py'])
            run(mode,'documented_checker',['scripts/check.py','--out',t/('check-'+tag)])
            run(mode,'default_checker',['scripts/check.py'])
            rebuilt=t/('rebuilt-'+tag+'.zip')
            run(mode,'documented_archive',['scripts/build_archive.py','--out',rebuilt])
            need(rebuilt.read_bytes()==(P/ARCHIVE).read_bytes(),'Documented archive mismatch')
            strict=['scripts/verify_package.py','--require-bindings','--bindings',P/'UPLOAD_BINDINGS.json','--archive',P/ARCHIVE]
            run(mode,'strict_present_binding',strict)
            run(mode,'required_absent_binding',['scripts/verify_package.py','--require-bindings','--bindings',t/'missing.json'],False)
            for case in ['malformed','bad_pdf','bad_zip','bad_manifest','missing_archive']:
                binding=read(P/'UPLOAD_BINDINGS.json')
                f=t/('binding-'+tag+'-'+case+'.json')
                if case=='malformed':f.write_text('{bad')
                else:
                    if case in ['bad_pdf','bad_zip']:binding['pdf' if case=='bad_pdf' else 'archive']['sha256']='0'*64
                    if case=='bad_manifest':binding['manifest_sha256']='0'*64
                    write(f,binding)
                ap=t/'missing.zip' if case=='missing_archive' else P/ARCHIVE
                run(mode,'binding_'+case,['scripts/verify_package.py','--require-bindings','--bindings',f,'--archive',ap],False)
            # Terminal-accounting semantics are challenged with coherent outer checksums.
            for case in ['review_count','premature_readiness','bypass_hold','latest_finding','root_adoption']:
                if case in ['review_count','premature_readiness','bypass_hold']:
                    name='TERMINAL_STATUS.json';v=json.loads(original[name]);v[{'review_count':'fresh_whole_package_reviews_completed','premature_readiness':'publication_ready','bypass_hold':'services_held_after_pr'}[case]]={'review_count':1,'premature_readiness':True,'bypass_hold':0}[case]
                elif case=='latest_finding':
                    name='custody/reviews/package_02/VERDICT.json';v=json.loads(original[name]);v['finding_counts']['P3']=1
                else:
                    name='custody/ROOT_WHOLE_PACKAGE_REVIEW_02.json';v=json.loads(original[name]);v['status']='PENDING'
                write(root/name,v);manifest_refresh()
                result=run(mode,'semantic_'+case,['scripts/verify_package.py'],False)
                semantics.append({'mode':tag,'case':case,'rejected_with_coherent_outer_manifest':True,'stderr_sha256':sha(result.stderr.encode())})
                restore(name);restore('PACKAGE_MANIFEST.json')
            # Citation semantic parser, independently of file checksums.
            for case in ['title','duplicate','classification']:
                text=original['CITATION.txt'].decode()
                if case=='title':text=text.replace('Title: A localized','Title: Wrong localized')
                elif case=='duplicate':text=text.replace('Kind: Unrefereed research note (preprint)','Author: Alec Kriebel')
                else:text=text.replace('Kind: Unrefereed research note (preprint)','Kind: Software')
                (root/'CITATION.txt').write_text(text);manifest_refresh()
                run(mode,'citation_'+case,['scripts/verify_package.py'],False)
                restore('CITATION.txt');restore('PACKAGE_MANIFEST.json')
            # Identical and malformed bootstrap symlinks must fail before JSON parsing and writes.
            for bad in [False,True]:
                external=t/('manifest-'+tag+str(bad)+'.json');external.write_bytes(b'{bad' if bad else original['PACKAGE_MANIFEST.json'])
                (root/'PACKAGE_MANIFEST.json').unlink();(root/'PACKAGE_MANIFEST.json').symlink_to(external)
                for cli in [['scripts/verify_package.py'],['scripts/build_archive.py','--out',t/('bootstrap-'+tag+str(bad)+'.zip')]]:
                    result=run(mode,'bootstrap_symlink_malformed' if bad else 'bootstrap_symlink_identical',cli,False)
                    need('Symlink member/ancestor' in result.stderr,'Bootstrap JSON parsed before structural preflight')
                restore('PACKAGE_MANIFEST.json')
            # Every archived protected record and both external binding interfaces receive direct, hardlink and symlink API checks.
            # Fresh output policy rejects every existing inode independently of contents and before any writer action.
            probe_source="""import importlib.util,json,os,sys
from pathlib import Path
sys.dont_write_bytecode=True
root=Path(sys.argv[1]);outside=Path(sys.argv[2]);targets=json.loads(Path(sys.argv[3]).read_text())
spec=importlib.util.spec_from_file_location('reviewed_paths',root/'scripts/package_paths.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
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
print(json.dumps({'protected_targets':len(targets),'output_rejections':count,'all_preflight_before_writes':True},sort_keys=True))
"""
            probe=t/('probe-'+tag+'.py');probe.write_text(probe_source)
            # Include all 597 immediate protected record types one at a time via byte-exact disposable copies,
            # never place a destructive output alias on any canonical audit inode.
            protected_dir=t/('protected-records-'+tag);protected_dir.mkdir()
            targets=[str(root/name) for name in sorted(original)]
            for idx,row in enumerate(read(D/'BASELINE_INPUT_PINS.json')['records']):
                path=A/row['path']
                if row['path'] in {r['path'] for r in read(D/'AUTHORIZED_EXISTING_CHANGES.json')['records']}:
                    path=D/'before'/row['path']
                check(path,row)
                dest=protected_dir/str(idx);shutil.copyfile(path,dest);targets.append(str(dest))
            for idx,f in enumerate([P/'UPLOAD_BINDINGS.json',A/'publication/zenodo-deposit.json']):
                dest=protected_dir/('external'+str(idx));shutil.copyfile(f,dest);targets.append(str(dest))
            target_file=t/('targets-'+tag+'.json');write(target_file,targets)
            proc=run(mode,'all_protected_output_alias_api',[probe,root,t,target_file]);api_log.append({'mode':tag,**json.loads(proc.stdout)})
            shutil.rmtree(protected_dir)
            # Actual CLI rejection at all writer entry points; compiler never runs on rejection.
            for cli in ['build_archive.py','check.py','build_pdf.py']:
                for target_name in ['TERMINAL_STATUS.json','custody/ROOT_WHOLE_PACKAGE_REVIEW_02.json','PACKAGE_MANIFEST.json','CITATION.txt']:
                    target=root/target_name
                    args=['scripts/'+cli,'--out',target]
                    if cli=='build_pdf.py':args+=['--tectonic','/nonexistent/no-compiler-may-run']
                    result=run(mode,'writer_existing_'+cli+'_'+target_name,args,False)
                    need('Output must be new' in result.stderr,'Writer did not reject before processing')
                for kind in ['descendant','missing_parent','linked_parent','dangling']:
                    target={'descendant':root/'custody'/'never-create', 'missing_parent':t/'absent-parent'/'file', 'linked_parent':t/('parent-link-'+tag+'-'+cli)/'file', 'dangling':t/('dangling-'+tag+'-'+cli)}[kind]
                    if kind=='linked_parent':target.parent.symlink_to(root/'custody',target_is_directory=True)
                    if kind=='dangling':target.symlink_to(t/'does-not-exist')
                    args=['scripts/'+cli,'--out',target]
                    if cli=='build_pdf.py':args+=['--tectonic','/nonexistent/no-compiler-may-run']
                    run(mode,'writer_'+kind+'_'+cli,args,False)
                    need(not target.exists(),'Rejected output materialized')
                    if kind=='linked_parent':target.parent.unlink()
                    if kind=='dangling':target.unlink()
            run(mode,'repeat_default_verify',['scripts/verify_package.py'])
        need({str(f.relative_to(root)):f.read_bytes() for f in root.rglob('*') if f.is_file()}==original,'Clean extracted bytes changed after controls')
        # Actual repository uploader, entirely local check; no secret or remote operation.
        local=run(False,'repository_uploader_check',[REPO/'zenodo_deposit_tool/zenodo.py','check',A/'publication/zenodo-deposit.json'],cwd=REPO)
        write(D/'REPOSITORY_TOOL_LOCAL_CHECK.json',{'returncode':local.returncode,'stdout':local.stdout,'stderr':local.stderr,'local_only':True})
    write(D/'CONTROL_RECEIPTS.json',{'actual_commands':len(command_log),'records':command_log})
    write(D/'OUTPUT_ALIAS_ALL_PROTECTED.json',{'records':api_log,'canonical_inputs_never_used_as_destructive_alias_targets':True})
    write(D/'TERMINAL_SEMANTIC_CONTROLS.json',{'records':semantics})
    return {'actual_commands':len(command_log),'expected_successes':sum(r['expected_success'] for r in command_log),'expected_rejections':sum(not r['expected_success'] for r in command_log),'all_protected_api':api_log,'semantic_terminal_mutations_rejected':len(semantics),'clean_extracted_members_unchanged':len(original),'independent_closed_zip_exact':True,'real_pdf_compile_performed':False,'paper_unchanged_no_new_render_required':True,'native_repository_local_check':True}

def main():
    (D/'_scratch').mkdir(exist_ok=True)
    s=stages();c=controls();s2=stages();need(s==s2,'Custody changed during controls')
    write(D/'FINAL_VERIFICATION.json',{'status':'PASS','custody':s,'controls':c,'root_terminal_adoption_required':True,'publication_ready':False,'published':False,'service_hold_after_pr':1032})
    print(json.dumps(read(D/'FINAL_VERIFICATION.json'),indent=2))

if __name__=='__main__':main()
