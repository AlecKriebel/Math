#!/usr/bin/env python3
"""Actual static alias/bootstrap/citation controls on one disposable extraction."""
import datetime,hashlib,io,json,os,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
sys.dont_write_bytecode=True
EFFORT=Path(__file__).resolve().parent
ROOT=EFFORT.parents[1]
PACKAGE=ROOT/'NEWpreprint_v1_0'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(root):return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
records=[]
stream=EFFORT/('CONTROL_STREAM_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.jsonl')
with tempfile.TemporaryDirectory(prefix='control-',dir=EFFORT) as td:
    work=Path(td);clean=work/'clean';clean.mkdir()
    archive=PACKAGE/'PR1071_preprint_v1_0_support.zip'
    with zipfile.ZipFile(archive) as z:z.extractall(clean)
    original=snapshot(clean)
    def restore():
        # Deliberate mutations are confined to this disposable clean extraction.
        for q in sorted(clean.rglob('*'),key=lambda q:len(q.parts),reverse=True):
            if q.is_symlink() or q.is_file():q.unlink()
            elif q.is_dir():q.rmdir()
        for n,b in original.items():q=clean/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
    def refresh():
        m=json.loads((clean/'PACKAGE_MANIFEST.json').read_text())
        for x in m['members']:
            q=clean/x['path'];x['bytes']=q.stat().st_size;x['sha256']=sha(q)
        (clean/'PACKAGE_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
    def command(label,mode,script,args,success,contains=None):
        cmd=[sys.executable,*(['-O'] if mode=='optimized' else []),str(clean/'scripts'/script),*map(str,args)]
        proc=subprocess.run(cmd,cwd=clean,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        ok=(proc.returncode==0)==success
        if contains:ok=ok and contains in proc.stdout+proc.stderr
        records.append({'label':label,'mode':mode,'argv':cmd,'returncode':proc.returncode,'expected_success':success,'expected_text':contains,'stdout':proc.stdout,'stderr':proc.stderr,'expected_outcome':ok})
        with stream.open('a') as f:f.write(json.dumps(records[-1])+ '\n')
        need(ok,'Unexpected outcome '+label+' '+mode+' '+proc.stderr)
        return proc
    marker=work/'compiler-called'
    fake=work/'fake-tectonic.py'
    fake.write_text('#!'+sys.executable+'\nfrom pathlib import Path\nimport sys\nPath('+repr(str(marker))+').write_text("called")\nd=Path(sys.argv[sys.argv.index("--outdir")+1]);(d/"paper.pdf").write_bytes(b"fake-pdf; repair-interface only")\n(d/"paper.log").write_text("safe fake compiler log")\nprint("fake compile interface")\n')
    fake.chmod(0o755)
    for mode in ['normal','optimized']:
        command('clean_default_absent_bindings',mode,'verify_package.py',[],True)
        out=work/('check-'+mode);command('clean_finite_checker',mode,'check.py',['--out',out],True)
        receipt=json.loads((out/'CHECK_RECEIPT.json').read_text());need(all(x['full_mathematics_equal_utc_only_difference'] and all(c['rejected'] for c in x['negative_controls']) for x in receipt['modes']),'Finite checker control failure')
        shutil.rmtree(out)
        rebuilt=work/('rebuilt-'+mode+'.zip');command('clean_deterministic_archive',mode,'build_archive.py',['--out',rebuilt],True);need(rebuilt.read_bytes()==archive.read_bytes(),'Clean archive not byte-identical');rebuilt.unlink()
        command('clean_repeat_default_verification',mode,'verify_package.py',[],True)
        command('strict_external_bindings',mode,'verify_package.py',['--require-bindings','--bindings',PACKAGE/'UPLOAD_BINDINGS.json','--archive',archive],True)
        command('required_absent_bindings',mode,'verify_package.py',['--require-bindings'],False,'Required bindings are absent')
        # Exact binding corruption variants remain strict.
        bind=json.loads((PACKAGE/'UPLOAD_BINDINGS.json').read_text())
        for field in ['pdf','archive']:
            bad=json.loads(json.dumps(bind));bad[field]['sha256']='0'*64;bp=work/'bad-bindings.json';bp.write_text(json.dumps(bad))
            command('strict_corrupt_'+field,mode,'verify_package.py',['--require-bindings','--bindings',bp,'--archive',archive],False,'binding mismatch');bp.unlink()
        missing=work/'missing.zip';command('strict_missing_archive',mode,'verify_package.py',['--require-bindings','--bindings',PACKAGE/'UPLOAD_BINDINGS.json','--archive',missing],False,'regular nonsymlink archive')
        pd=work/('pdf-'+mode);command('safe_fresh_fake_compiler_interface',mode,'build_pdf.py',['--out',pd,'--tectonic',fake],True);need(marker.exists(),'Safe fake compiler was not called');marker.unlink();shutil.rmtree(pd)
        need(snapshot(clean)==original,'Positive command altered extraction')
        # Every protected content family: no existing direct/symlink/hardlink archive output.
        for member in ['paper.tex','paper.pdf','metadata.json','PACKAGE_MANIFEST.json','custody/submitted/PROOF.md']:
            target=clean/member;before=sha(target)
            for kind in ['direct','symlink','hardlink']:
                dest=target if kind=='direct' else work/('alias-'+kind)
                if kind=='symlink':dest.symlink_to(target)
                if kind=='hardlink':os.link(target,dest)
                command('archive_'+kind+'_'+member,mode,'build_archive.py',['--out',dest],False,'Output must be new')
                need(sha(target)==before,'Protected member mutated in alias rejection')
                records[-1]['protected_hash_unchanged']=True
                if kind!='direct':dest.unlink()
        for script in ['build_archive.py','check.py','build_pdf.py']:
            stem=script.replace('.py','');desc=clean/'custody'/('fresh-'+stem)
            args=['--out',desc]+(['--tectonic',fake] if script=='build_pdf.py' else [])
            command(stem+'_new_descendant',mode,script,args,False,'outside all frozen package descendants');need(not desc.exists() and not marker.exists(),'Rejected descendant produced output/compiler invocation')
            link=work/'ancestor-alias';link.symlink_to(clean/'custody',target_is_directory=True);dest=link/'new';args=['--out',dest]+(['--tectonic',fake] if script=='build_pdf.py' else [])
            command(stem+'_symlink_ancestor',mode,script,args,False,'Symlink output ancestor');need(not (clean/'custody/new').exists() and not marker.exists(),'Ancestor alias produced output');link.unlink()
            dang=work/'dangling';dang.symlink_to(work/'absent');args=['--out',dang]+(['--tectonic',fake] if script=='build_pdf.py' else [])
            command(stem+'_dangling_leaf',mode,script,args,False,'Output must be new');dang.unlink()
            no=work/'missing-parent/new';args=['--out',no]+(['--tectonic',fake] if script=='build_pdf.py' else [])
            command(stem+'_missing_parent',mode,script,args,False,'parent must already exist');need(not no.parent.exists(),'Missing parent was created')
        # Existing directories with aliases at ALL intended checker/PDF output names.
        groups={'check.py':['normal/original_finite_checks.py','normal/FINITE_CHECKS.json','normal/stdout.txt','normal/stderr.txt','optimized/original_finite_checks.py','optimized/FINITE_CHECKS.json','optimized/stdout.txt','optimized/stderr.txt','CHECK_RECEIPT.json'], 'build_pdf.py':['paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt']}
        for script,files in groups.items():
            for filename in files:
                for kind in ['symlink','hardlink']:
                    out=work/'existing-output';(out/filename).parent.mkdir(parents=True,exist_ok=True);leaf=out/filename;target=clean/'metadata.json';before=sha(target)
                    if kind=='symlink':leaf.symlink_to(target)
                    else:os.link(target,leaf)
                    args=['--out',out]+(['--tectonic',fake] if script=='build_pdf.py' else [])
                    command(script+'_existing_'+filename+'_'+kind,mode,script,args,False,'Output must be new')
                    need(sha(target)==before and not marker.exists(),'Existing directory alias mutation/compiler call')
                    records[-1]['protected_hash_unchanged']=True;records[-1]['compiler_not_called']=not marker.exists();shutil.rmtree(out)
        # Bootstrap rejection BEFORE parsing (invalid JSON deliberately behind the bad path).
        for kind in ['symlink','dangling','directory','missing']:
            for script in ['verify_package.py','build_archive.py']:
                restore();manifest=clean/'PACKAGE_MANIFEST.json';manifest.unlink();external=work/'manifest-target.json'
                if kind=='symlink':external.write_text('{invalid JSON');manifest.symlink_to(external)
                elif kind=='dangling':manifest.symlink_to(work/'absent-json')
                elif kind=='directory':manifest.mkdir()
                dest=work/'bootstrap-output.zip';args=[] if script=='verify_package.py' else ['--out',dest]
                expected='Symlink member/ancestor' if kind in ['symlink','dangling'] else ('Nonregular member' if kind=='directory' else 'Missing member/ancestor')
                proc=command('manifest_'+kind+'_before_parse_'+script,mode,script,args,False,expected);need('JSONDecodeError' not in proc.stderr and not dest.exists(),'Bootstrap parsed JSON or wrote archive')
                records[-1]['json_not_parsed']=True;records[-1]['archive_not_written']=True
                if external.exists():external.unlink()
        restore();parent=clean/'custody/submitted';saved=work/'saved-submitted';shutil.move(parent,saved);parent.symlink_to(saved,target_is_directory=True)
        command('member_directory_ancestor_symlink',mode,'verify_package.py',[],False,'Symlink member/ancestor');parent.unlink();shutil.move(saved,parent)
        # Semantic faults with coherent new outer manifest: checksum alone is insufficient.
        for label,old,new in [('citation_paper_type','Kind: Unrefereed research note (preprint)','Kind: software'),('citation_title','Title: A localized','Title: Incorrect localized'),('citation_duplicate','Author: Alec Kriebel','Author: Alec Kriebel\nAuthor: Alec Kriebel')]:
            restore();q=clean/'CITATION.txt';q.write_text(q.read_text().replace(old,new));refresh();command(label,mode,'verify_package.py',[],False,'Citation' if label=='citation_duplicate' else 'citation')
        for field,value in [('fresh_whole_package_reviews_completed',2),('publication_ready',True),('published',True),('services_held_at_pr',1033)]:
            restore();q=clean/'CURRENT_STATUS.json';d=json.loads(q.read_text());d[field]=value;q.write_text(json.dumps(d));refresh();command('coherent_current_stage_'+field,mode,'verify_package.py',[],False,'review state drift' if field=='fresh_whole_package_reviews_completed' else 'Premature current promotion')
        # Deleted-guard controls prove the rejected mechanisms, using ONLY this scratch tree.
        restore();q=clean/'scripts/package_paths.py';s=q.read_text();s=s.replace("require(not target.exists() and not target.is_symlink(),", "require(True,");q.write_text(s);refresh();target=clean/'metadata.json';before=sha(target);alias=work/'deleted-guard-hardlink';os.link(target,alias)
        command('DELETED_OUTPUT_GUARD_demonstrates_hardlink_overwrite',mode,'build_archive.py',['--out',alias],True);need(sha(target)!=before,'Deleted output guard did not demonstrate mutation');records[-1]['scratch_protected_input_mutated_as_expected']=True;alias.unlink()
        restore();q=clean/'scripts/package_paths.py';s=q.read_text();start=s.index('def safe_path(');end=s.index('\ndef fresh_output',start);s=s[:start]+"def safe_path(root,name):\n    return Path(root)/name\n"+s[end:];q.write_text(s);refresh();manifest=clean/'PACKAGE_MANIFEST.json';external=work/'deleted-bootstrap-target.json';external.write_bytes(manifest.read_bytes());manifest.unlink();manifest.symlink_to(external)
        command('DELETED_BOOTSTRAP_GUARD_accepts_manifest_symlink',mode,'verify_package.py',[],True);external.unlink()
        restore();q=clean/'scripts/verify_package.py';q.write_text(q.read_text().replace('    validate_citation(root,metadata)','    pass # deliberate citation-guard deletion'));q=clean/'CITATION.txt';q.write_text(q.read_text().replace('Kind: Unrefereed research note (preprint)','Kind: software'));refresh()
        command('DELETED_CITATION_GUARD_accepts_misclassification',mode,'verify_package.py',[],True)
        restore();need(snapshot(clean)==original,'Scratch baseline restoration failed')
    # Independent ZIP bytes, read only after closing.
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
        for name,data in sorted(original.items()):
            inf=zipfile.ZipInfo(name,date_time=(2026,10,14,0,0,0));inf.create_system=3;inf.external_attr=0o100644<<16;inf.compress_type=zipfile.ZIP_STORED;z.writestr(inf,data)
    need(b.getvalue()==archive.read_bytes(),'Independent CLOSED archive differs')
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_command_count':len(records),'normal_and_optimized':True,'all_expected_outcomes':all(z['expected_outcome'] for z in records),'records':records,'clean_extracted_files_unchanged':len(original),'independent_closed_archive_byte_identical':True,'archive_sha256':sha(archive),'paper_pdf_sha256':sha(PACKAGE/'paper.pdf'),'actual_candidate_compile_or_render':False,'fake_compiler_role':'Only bounded output interface testing; real compilation belongs to NEW whole02.','static_local_filesystem_only':True,'deliberately_deleted_guards_expose_all_three_defects':True,'only_disposable_extraction_mutated':True}
    (EFFORT/'CONTROL_RECEIPTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
