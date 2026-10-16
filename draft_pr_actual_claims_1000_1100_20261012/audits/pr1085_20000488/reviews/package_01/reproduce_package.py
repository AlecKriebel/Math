from pathlib import Path
import hashlib,io,json,os,shutil,subprocess,sys,tempfile,zipfile,datetime
R=Path(__file__).resolve().parent; A=R.parents[1]; P=A/'preprint_v1_0'
ARCHIVE='pr1085_support_v1_0.zip'; calls=[]; checks={}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def dump(n,o):(R/n).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def pins(base,rows):
    for row in rows:
        b=(base/row['path']).read_bytes()
        need(len(b)==row['bytes'] and sha(b)==row['sha256'],'pin '+row['path'])
    return len(rows)
checks['all_frozen_inputs']=pins(A,json.loads((R/'INPUT_PINS.json').read_text())['files'])
checks['preparation_outputs']=pins(P,json.loads((P/'OUTPUT_PINS.json').read_text())['files'])
frozen=json.loads((P/'PREPARATION_INPUT_PINS.json').read_text())['files']
checks['all_preparation_inputs']=pins(A,frozen)
copies=json.loads((P/'COPY_MAP.json').read_text())['files'];exclusions=json.loads((P/'EXCLUSIONS.json').read_text())['files']
need(len(copies)==66 and len(exclusions)==126,'partition counts')
need({r['source_relative_audit'] for r in copies}.isdisjoint(r['path'] for r in exclusions),'partition disjoint')
need({r['source_relative_audit'] for r in copies}|{r['path'] for r in exclusions}=={r['path'] for r in frozen},'partition complete')
for row in copies:need((P/row['copy']).read_bytes()==(A/row['source_relative_audit']).read_bytes(),'source exact copy')
checks['source_equal_copies']=len(copies);checks['individual_exclusions']=len(exclusions)
meta=json.loads((P/'.zenodo.json').read_text());need(meta==json.loads((P/'metadata.json').read_text())['metadata']==json.loads((P/'zenodo-deposit.json').read_text())['metadata']==json.loads((P/'UPLOAD_BINDINGS.json').read_text())['metadata'],'all metadata equal')
data=(P/ARCHIVE).read_bytes();names=(P/'PAYLOAD_MEMBERS.txt').read_text().splitlines();expected=sorted(names+['SUPPORT_MANIFEST.json'])
out=io.BytesIO()
with zipfile.ZipFile(io.BytesIO(data)) as z,zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as w:
    need(z.namelist()==expected and z.testzip() is None,'archive members/CRC')
    need(not z.comment,'archive comment')
    for info in z.infolist():
        body=(P/info.filename).read_bytes();need(z.read(info.filename)==body,'archive bytes')
        need(info.date_time==(2026,10,14,0,0,0) and info.create_system==3 and info.external_attr==(0o100644<<16) and info.compress_type==8 and info.flag_bits==0 and not info.extra and not info.comment,'headers')
        i=zipfile.ZipInfo(info.filename,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=8;w.writestr(i,body,compresslevel=9)
need(out.getvalue()==data,'independently CLOSED ZIP bytes')
checks['archive']={'members':len(expected),'bytes':len(data),'sha256':sha(data),'independent_closed_rebuild_identical':True}

def command(argv,cwd,expect=0,env=None,label=''):
    proc=subprocess.run([str(x) for x in argv],cwd=cwd,env=env,capture_output=True,text=True)
    calls.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,'argv':[str(x) for x in argv],'cwd':str(cwd),'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'expected':'success' if expect==0 else 'nonzero'})
    dump('COMMANDS.json',calls)
    need(proc.returncode==0 if expect==0 else proc.returncode!=0,'unexpected command: '+label)
    return proc
def fresh(root):
    kit=root/'kit'
    if kit.exists():shutil.rmtree(kit)
    kit.mkdir()
    with zipfile.ZipFile(io.BytesIO(data)) as z:z.extractall(kit)
    return kit
def refresh(kit,name):
    path=kit/'SUPPORT_MANIFEST.json';m=json.loads(path.read_text());b=(kit/name).read_bytes()
    for row in m['files']:
        if row['path']==name:row.update(bytes=len(b),sha256=sha(b))
    path.write_text(json.dumps(m,indent=2)+'\n')
def change_json(kit,name,fn):
    p=kit/name;o=json.loads(p.read_text());fn(o);p.write_text(json.dumps(o,indent=2)+'\n');refresh(kit,name)
def native(kit):
    for n in ['zenodo-deposit.json','UPLOAD_BINDINGS.json',ARCHIVE]:shutil.copyfile(P/n,kit/n)
def treepins(root):return {p.relative_to(root).as_posix():sha(p.read_bytes()) for p in root.rglob('*') if p.is_file() and not p.is_symlink()}
math_results=[];public_results=[]
(R/'tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(dir=R/'tmp',prefix='whole-review-') as temp:
    root=Path(temp)
    for optimized in [False,True]:
        py=[sys.executable]+(['-O'] if optimized else [])+['-B']
        mode='optimized' if optimized else 'normal'
        for exe,args in [('verify_package.py',[]),('check_math.py',[]),('verify_package.py',['--require-deposit'])]:
            p=command(py+[P/exe]+args,P,label=mode+' canonical '+exe+' '+' '.join(args))
            public_results.append(json.loads(p.stdout))
        m=command(py+[R/'check_independent_math.py'],R,label=mode+' independent math');math_results.append(json.loads(m.stdout))
        dump('INDEPENDENT_MATH_'+mode.upper()+'.json',math_results[-1])
        for fault in ['drop_fiber_endpoint','wrong_mass_power','reverse_normal']:
            command(py+[R/'check_independent_math.py','--fault',fault],R,1,label=mode+' independent '+fault)
        kit=fresh(root);before=treepins(kit)
        p=command(py+[kit/'verify_package.py'],kit,label=mode+' clean default');need(json.loads(p.stdout)['external_deposit_binding_verified'] is False,'optional binding status')
        command(py+[kit/'check_math.py'],kit,label=mode+' clean math')
        output=root/('rebuilt_'+mode+'.zip')
        command(py+[kit/'build_archive.py','--output',output],kit,label=mode+' documented archive rebuild')
        need(output.read_bytes()==data,'actual clean archive identity')
        command(py+[kit/'verify_package.py'],kit,label=mode+' documented post-build verification')
        pdfout=root/('compiled_'+mode)
        command(py+[kit/'build_pdf.py','--out-dir',pdfout],kit,label=mode+' REAL documented clean compilation')
        need((pdfout/'paper.pdf').read_bytes()==(P/'paper.pdf').read_bytes(),'actual compiled PDF identity')
        need(treepins(kit)==before,'clean documented commands preserve all extracted payload')
        receipt=json.loads((pdfout/'COMPILE_RECEIPT.json').read_text());dump('REAL_COMPILE_'+mode.upper()+'.json',receipt)
        shutil.rmtree(pdfout);output.unlink()
        # Every mutation below is confined to one disposable extraction.
        for mutation in ['normal_sign','lost_jacobian','preprint_theta','fourier_boundary_sign']:
            kit=fresh(root);command(py+[kit/'check_math.py','--mutation',mutation],kit,1,label=mode+' package math mutation '+mutation)
        for key,value in [('publication_ready',True),('all_actionable_issues_resolved',True),('published',True),('embedded_eigenvalues_excluded',True),('all_coupling_absence_for_one_fixed_nonzero_graph',True),('general_n_ge_4_nongraph_classification',True),('human_peer_review',True),('formal_proof_certificate',True),('new_whole_package_reviews',2),('minimum_new_whole_package_reviews',1),('novelty','TRUE'),('audited_head','0'*40)]:
            kit=fresh(root);change_json(kit,'STATUS.json',lambda o,k=key,v=value:o.__setitem__(k,v));command(py+[kit/'verify_package.py'],kit,1,label=mode+' refreshed-manifest status '+key)
        for name in ['SUPPORT_MANIFEST.json','PAYLOAD_MEMBERS.txt','paper.tex']:
            kit=fresh(root);target=root/'same_bytes';shutil.copyfile(kit/name,target);(kit/name).unlink();(kit/name).symlink_to(target)
            command(py+[kit/'verify_package.py'],kit,1,label=mode+' same-byte symlink '+name)
            target.unlink()
        kit=fresh(root);shutil.move(kit/'evidence',root/'evidence_moved');(kit/'evidence').symlink_to(root/'evidence_moved',target_is_directory=True)
        command(py+[kit/'verify_package.py'],kit,1,label=mode+' same-byte symlink ancestor');(kit/'evidence').unlink();shutil.rmtree(root/'evidence_moved')
        kit=fresh(root);change_json(kit,'COPY_MAP.json',lambda o:o['files'][0].__setitem__('sha256','0'*64));command(py+[kit/'verify_package.py'],kit,1,label=mode+' refreshed copy-map forgery')
        kit=fresh(root);change_json(kit,'EXCLUSIONS.json',lambda o:o['files'][0].__setitem__('reason',''));command(py+[kit/'verify_package.py'],kit,1,label=mode+' refreshed empty exclusion')
        kit=fresh(root);change_json(kit,'EXCLUSIONS.json',lambda o:o['files'].pop());command(py+[kit/'verify_package.py'],kit,1,label=mode+' refreshed omitted exclusion')
        kit=fresh(root)
        for name in ['.zenodo.json','metadata.json']:
            change_json(kit,name,lambda o:o.get('metadata',o).__setitem__('description','first novel human peer reviewed solution'))
        command(py+[kit/'verify_package.py'],kit,1,label=mode+' coherent bibliographic overclaim')
        kit=fresh(root);command(py+[kit/'verify_package.py','--require-deposit'],kit,1,label=mode+' required missing descriptor')
        for kind in ['dangling','ordinary']:
            kit=fresh(root);target=root/'descriptor';target.write_text((P/'zenodo-deposit.json').read_text())
            if kind=='dangling':target.unlink()
            (kit/'zenodo-deposit.json').symlink_to(target)
            command(py+[kit/'verify_package.py'],kit,1,label=mode+' '+kind+' descriptor symlink')
            if target.exists():target.unlink()
        kit=fresh(root);native(kit);p=command(py+[kit/'verify_package.py','--require-deposit'],kit,label=mode+' actual descriptor binding');need(json.loads(p.stdout)['external_deposit_binding_verified'] is True,'true binding')
        for field,val in [('sha256','0'*64),('bytes',0),('filename','wrong.pdf')]:
            kit=fresh(root);native(kit);p=kit/'UPLOAD_BINDINGS.json';o=json.loads(p.read_text());o['files'][0][field]=val;p.write_text(json.dumps(o));command(py+[kit/'verify_package.py','--require-deposit'],kit,1,label=mode+' external binding '+field)
        kit=fresh(root);native(kit);p=kit/'zenodo-deposit.json';o=json.loads(p.read_text());o['files'][0]['path']='other.pdf';p.write_text(json.dumps(o));command(py+[kit/'verify_package.py','--require-deposit'],kit,1,label=mode+' wrong native attachment path')
        kit=fresh(root);(kit/'SUPPORT_MANIFEST.json').write_text('{"schema":1,"schema":1}');command(py+[kit/'verify_package.py'],kit,1,label=mode+' duplicate bootstrap JSON key')
        # All public output writers, including each compiler child, reject
        # direct input, hardlink, symlink, and symlink-ancestor aliases.
        for writer,flag in [('check_math.py','--output'),('verify_package.py','--output'),('build_archive.py','--output')]:
            for kind in ['direct','hardlink','symlink','ancestor']:
                kit=fresh(root);alias=root/'alias';source=kit/'paper.tex';saved=source.read_bytes()
                if kind=='direct':target=source
                elif kind=='hardlink':os.link(source,alias);target=alias
                elif kind=='symlink':alias.symlink_to(source);target=alias
                else:alias.symlink_to(kit,target_is_directory=True);target=alias/'paper.tex'
                command(py+[kit/writer,flag,target],kit,1,label=mode+' '+writer+' '+kind+' output alias')
                need(source.read_bytes()==saved,'writer preserved protected bytes')
                if alias.is_symlink() or alias.exists():alias.unlink()
        for child in ['paper.tex','paper.pdf','paper.log','COMPILE_RECEIPT.json']:
            kit=fresh(root);outdir=root/'pdf_alias';outdir.mkdir();source=kit/'paper.tex';saved=source.read_bytes();os.link(source,outdir/child)
            command(py+[kit/'build_pdf.py','--out-dir',outdir],kit,1,label=mode+' PDF child hardlink '+child)
            need(source.read_bytes()==saved,'PDF child preserved input');shutil.rmtree(outdir)
        kit=fresh(root);descriptor=root/'external_descriptor.json';descriptor.write_text((P/'zenodo-deposit.json').read_text());alias=root/'alias';os.link(descriptor,alias);saved=descriptor.read_bytes()
        command(py+[kit/'verify_package.py','--deposit',descriptor,'--output',alias],kit,1,label=mode+' explicit external descriptor hardlink output')
        need(descriptor.read_bytes()==saved,'external descriptor preserved');alias.unlink();descriptor.unlink()
        # The old frozen-source list is protected when it exists in the local
        # audit layout. Simulate that layout without touching canonical inputs.
        kit=fresh(root);old=root/'submitted/MATHEMATICAL_REPORT.md';old.parent.mkdir(exist_ok=True);old.write_bytes((A/'submitted/MATHEMATICAL_REPORT.md').read_bytes());alias=root/'alias';os.link(old,alias);saved=old.read_bytes()
        command(py+[kit/'build_archive.py','--output',alias],kit,1,label=mode+' frozen original source hardlink')
        need(old.read_bytes()==saved,'old original source preserved');alias.unlink();shutil.rmtree(old.parent)
    need(math_results[0]==math_results[1],'independent math ordinary/optimized equality')
    need(public_results[:3]==public_results[3:],'canonical results ordinary/optimized equality')
    # Real repository interface, entirely local: no credentials/state/network.
    repo=Path('/Users/alec/Documents/Math')
    command([sys.executable,'-B',repo/'zenodo_deposit_tool/zenodo.py','check',P/'zenodo-deposit.json'],repo,label='actual repository LOCAL native manifest check')
checks['all_frozen_inputs_terminal']=pins(A,json.loads((R/'INPUT_PINS.json').read_text())['files'])
checks['actual_commands']=len(calls);checks['expected_rejections']=sum(c['expected']=='nonzero' for c in calls)
checks['normal_optimized_equal']=True;checks['all_tests_passed']=True;checks['real_clean_pdf_compilations']=2
dump('REPRODUCTION_RESULTS.json',checks)
print(json.dumps(checks,indent=2,sort_keys=True))
