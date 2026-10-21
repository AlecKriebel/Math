"""Actual clean standard-library and bounded administrative negative controls."""
from pathlib import Path
import datetime, hashlib, io, json, os, shutil, subprocess, sys, tempfile, zipfile
F=Path(__file__).resolve().parent
A=F.parents[1]
K=A/'preprint_v1_0'
REPO=A.parents[2]
ARCHIVE='pr1085_support_v1_0.zip'
records=[]
def sha(data): return hashlib.sha256(data).hexdigest()
def need(ok,message):
    if not ok: raise ValueError(message)
def dump(path,obj): path.write_text(json.dumps(obj,indent=2)+'\n')
def run(cwd,argv,label,good=True,expect_text=None,env=None):
    p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,env=env)
    records.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'label':label,'cwd':str(cwd),'argv':argv,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    need((p.returncode==0)==good,label+' exit: '+p.stdout+p.stderr)
    if expect_text is not None: need(expect_text in p.stderr,label+' did not reach intended guard: '+p.stderr)
    return p
def main():
    body=(K/ARCHIVE).read_bytes()
    with zipfile.ZipFile(io.BytesIO(body)) as z: payload={i.filename:z.read(i) for i in z.infolist()}
    data_stream=io.BytesIO()
    with zipfile.ZipFile(data_stream,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(payload):
            info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.create_system=3
            info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,payload[name],compresslevel=9)
    need(data_stream.getvalue()==body,'independent CLOSED deterministic ZIP differs')
    baseline={str(p.relative_to(K)):(len(p.read_bytes()),sha(p.read_bytes())) for p in K.rglob('*') if p.is_file()}
    mode_results=[]; alias_rows=[]; semantic_rows=[]
    with tempfile.TemporaryDirectory(prefix='pr1085-terminal-',dir='/private/tmp') as td:
        temp=Path(td); root=temp/'kit'
        root.mkdir()
        def fresh(full=False):
            for p in sorted(root.rglob('*'),key=lambda p:len(p.parts),reverse=True):
                if p.is_symlink() or p.is_file():p.unlink()
                elif p.is_dir():p.rmdir()
            for name,data in payload.items():
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
            if full:
                (root/ARCHIVE).write_bytes(body)
                for name in ['zenodo-deposit.json','UPLOAD_BINDINGS.json']:(root/name).write_bytes((K/name).read_bytes())
        def repin():
            p=root/'SUPPORT_MANIFEST.json'; obj=json.loads(p.read_text())
            for row in obj['files']:
                data=(root/row['path']).read_bytes();row['bytes']=len(data);row['sha256']=sha(data)
            dump(p,obj)
        def change(name,fn,coherent_source=False):
            p=root/name; obj=json.loads(p.read_text());fn(obj);dump(p,obj)
            if coherent_source:
                b=p.read_bytes();mapping=json.loads((root/'TERMINAL_COPY_MAP.json').read_text())
                row=next(r for r in mapping['files'] if r['copy']==name)
                row['bytes']=len(b);row['sha256']=sha(b);dump(root/'TERMINAL_COPY_MAP.json',mapping)
                pins=json.loads((root/'TERMINAL_INPUT_PINS.json').read_text())
                row2=next(r for r in pins['files'] if r['path']==row['source_relative_audit'])
                row2['bytes']=len(b);row2['sha256']=sha(b);dump(root/'TERMINAL_INPUT_PINS.json',pins)
            repin()
        for mode in [[],['-O']]:
            label='optimized' if mode else 'normal'; prefix=[sys.executable,*mode,'-B']
            fresh(); start={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
            default=json.loads(run(root,prefix+['verify_package.py'],label+' clean default verifier').stdout)
            math=json.loads(run(root,prefix+['check_math.py'],label+' clean mathematical checker').stdout)
            rebuilt=temp/('rebuilt_'+label+'.zip')
            run(root,prefix+['build_archive.py','--output',str(rebuilt)],label+' documented archive rebuild')
            need(rebuilt.read_bytes()==body,label+' documented ZIP differs')
            run(root,prefix+['verify_package.py'],label+' clean verifier after rebuild')
            need(start=={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()},'documented commands changed clean inputs')
            need(default['new_whole_reviews']==2 and not default['external_deposit_binding_verified'],'terminal/default semantics')
            run(root,prefix+['verify_package.py','--require-deposit'],label+' strict missing descriptor',False,'regular input required')
            fresh(full=True)
            strict=json.loads(run(root,prefix+['verify_package.py','--require-deposit'],label+' strict actual native binding').stdout)
            need(strict['external_deposit_binding_verified'] and strict['archive_verified'],'full actual binding not checked')
            (root/'UPLOAD_BINDINGS.json').unlink()
            run(root,prefix+['verify_package.py','--require-deposit'],label+' strict missing attachment binding',False,'regular input required')
            terminal_faults=[('whole_reviews_completed',1,'terminal two reviews'),('minimum_whole_reviews',0,'terminal two reviews'),
                ('latest_actionable_P0_P1_P2_P3',1,'latest review zero findings'),
                ('root_terminal_integrity_adoption_required',False,'root adoption and historical stage'),
                ('historical_STATUS_preserved',False,'root adoption and historical stage'),
                ('publication_ready',True,'terminal forbidden promotion'),('all_actionable_issues_resolved',True,'terminal forbidden promotion'),
                ('published',True,'terminal forbidden promotion'),('human_peer_review',True,'terminal forbidden promotion'),
                ('formal_proof_certificate',True,'terminal forbidden promotion'),('services_hold','none','terminal ordered hold'),
                ('novelty','VERIFIED','terminal historical scope'),('priority','CLEARED','terminal historical scope'),
                ('paper_pdf_sha256','0'*64,'unchanged paper identity'),('review_evidence',[],'exact two review interfaces')]
            for key,value,message in terminal_faults:
                fresh();change('TERMINAL_ACCOUNTING.json',lambda o,k=key,v=value:o.__setitem__(k,v))
                p=run(root,prefix+['verify_package.py'],label+' coherent terminal fault '+key,False,message)
                semantic_rows.append({'mode':label,'case':key,'reached_guard':message,'exit':p.returncode})
            evidence_faults=[('evidence/terminal/ROOT_WHOLE_PACKAGE_REVIEW_02.json',lambda o:o.__setitem__('publication_ready',True),'root review adoption semantics'),
                ('evidence/terminal/ROOT_WHOLE_PACKAGE_REVIEW_02.json',lambda o:o.__setitem__('status','ADOPTED'),'captured root review stage'),
                ('evidence/terminal/reviews/package_02/VERDICT.json',lambda o:o['severity_counts'].__setitem__('P0',1),'whole02 zero finding semantics'),
                ('evidence/terminal/reviews/package_01/VERDICT.json',lambda o:o.__setitem__('P3',1),'whole01 zero finding semantics')]
            for i,(name,fn,message) in enumerate(evidence_faults):
                fresh();change(name,fn,True)
                p=run(root,prefix+['verify_package.py'],label+' coherently forged review semantic '+str(i),False,message)
                semantic_rows.append({'mode':label,'case':name+'#'+str(i),'reached_guard':message,'exit':p.returncode})
            fresh();change('TERMINAL_COPY_MAP.json',lambda o:o['files'].pop())
            run(root,prefix+['verify_package.py'],label+' incomplete terminal copy partition',False,'terminal complete custody partition')
            fresh();change('TERMINAL_EXCLUSIONS.json',lambda o:o['files'][0].__setitem__('reason',''))
            run(root,prefix+['verify_package.py'],label+' absent individual exclusion reason',False,'terminal individual exclusion')
            fresh();(root/'evidence/terminal/ROOT_WHOLE_PACKAGE_REVIEW_02.json').unlink()
            run(root,prefix+['verify_package.py'],label+' missing root adoption evidence',False,'regular input required')
            for name in ['SUPPORT_MANIFEST.json','PAYLOAD_MEMBERS.txt']:
                fresh(); target=temp/(label+'_'+name);target.write_bytes((root/name).read_bytes())
                (root/name).unlink();(root/name).symlink_to(target)
                run(root,prefix+['verify_package.py'],label+' identical bootstrap symlink '+name,False,'symlink input or ancestor')
            fresh();p=root/'TERMINAL_ACCOUNTING.json';p.write_text('{"schema":1,"schema":1}\n');repin()
            run(root,prefix+['verify_package.py'],label+' duplicate JSON bootstrap',False,'duplicate JSON key')
            fresh(full=True);change('UPLOAD_BINDINGS.json',lambda o:o['files'][1].__setitem__('sha256','0'*64))
            run(root,prefix+['verify_package.py','--require-deposit'],label+' stale actual ZIP binding',False,'exact attachment binding')
            fresh()
            for script,targetname in [('verify_package.py','TERMINAL_ACCOUNTING.json'),('check_math.py','paper.tex'),('build_archive.py','TERMINAL_COPY_MAP.json')]:
                target=root/targetname; before=target.read_bytes()
                for kind in ['direct','hardlink','symlink','symlink_ancestor']:
                    if kind=='direct':out=target
                    elif kind=='hardlink':
                        out=temp/(label+'_'+script+'.hard');os.link(target,out)
                    elif kind=='symlink':
                        out=temp/(label+'_'+script+'.sym');out.symlink_to(target)
                    else:
                        parent=temp/(label+'_'+script+'.linked_parent');parent.symlink_to(root,target_is_directory=True);out=parent/targetname
                    p=run(root,prefix+[script,'--output',str(out)],label+' '+kind+' writer alias '+script,False,'output ')
                    need(target.read_bytes()==before,'alias changed target')
                    if kind in ['hardlink','symlink']:out.unlink()
                    if kind=='symlink_ancestor':parent.unlink()
                    alias_rows.append({'mode':label,'script':script,'alias':kind,'target':targetname,'exit':p.returncode,'target_unchanged':True})
            external=temp/('external_'+label+'.json');external.write_text('{}\n');out=temp/('external_'+label+'.hard');os.link(external,out)
            before=external.read_bytes()
            run(root,prefix+['verify_package.py','--deposit',str(external),'--output',str(out)],label+' external supplied descriptor hardlink',False,'output hardlinks protected input')
            need(external.read_bytes()==before,'external alias changed target');out.unlink()
            for name in ['paper.tex','paper.pdf','paper.log','COMPILE_RECEIPT.json']:
                outdir=temp/('pdf_'+label+'_'+name);outdir.mkdir();target=root/'paper.tex';os.link(target,outdir/name)
                before=target.read_bytes();env=dict(os.environ,PATH='/definitely/no/compiler')
                run(root,prefix+['build_pdf.py','--out-dir',str(outdir)],label+' PDF child protected hardlink '+name,False,'output hardlinks protected input',env)
                need(target.read_bytes()==before and sorted(p.name for p in outdir.iterdir())==[name],'PDF preflight failed before compiler or write')
                shutil.rmtree(outdir)
            fresh()
            for mutation in ['normal_sign','lost_jacobian','preprint_theta','fourier_boundary_sign']:
                run(root,prefix+['check_math.py','--mutation',mutation],label+' unchanged mathematical fault control '+mutation,False)
            run(root,prefix+['verify_package.py'],label+' final restored clean verification')
            need(start=={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()},'final restored extraction changed')
            mode_results.append({'mode':label,'default':default,'math':math,'strict':strict,'clean_payload_unchanged':True})
    need(mode_results[0]['default']==mode_results[1]['default'] and mode_results[0]['math']==mode_results[1]['math'] and mode_results[0]['strict']==mode_results[1]['strict'],'full ordinary/optimized JSON differs')
    local=run(REPO,[sys.executable,'-B',str(REPO/'zenodo_deposit_tool/zenodo.py'),'check',str(K/'zenodo-deposit.json')],'repository actual LOCAL native check')
    local_obj=json.loads(local.stdout)
    need(local_obj['files'][0]['sha256']==sha((K/'paper.pdf').read_bytes()) and local_obj['files'][1]['sha256']==sha(body),'local uploader actual identities')
    need(baseline=={str(p.relative_to(K)):(len(p.read_bytes()),sha(p.read_bytes())) for p in K.rglob('*') if p.is_file()},'candidate changed by controls')
    dump(F/'CONTROL_RECEIPTS.json',{'scope':'Actual argv/cwd/full process outputs; no actual PDF compile or service operation. All mutations were one disposable extraction.','commands':records})
    dump(F/'TERMINAL_SEMANTIC_CONTROLS.json',{'passed':True,'cases':semantic_rows,'coherent_outer_hashes':True,'review_semantic_cases_also_refresh_copied_source_maps':True})
    dump(F/'OUTPUT_ALIAS_CONTROLS.json',{'passed':True,'cases':alias_rows,'additional_per_mode':['supplied external descriptor hardlink','four PDF child hardlinks; nonexistent compiler could not be invoked'],'no_canonical_inodes_used_as_mutation_targets':True})
    dump(F/'REPOSITORY_TOOL_LOCAL_CHECK.json',{'passed':True,'argv':records[-1]['argv'],'stdout':local_obj,'services':'None; repository check only.'})
    dump(F/'CONTROL_SUMMARY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'passed':True,'commands':len(records),'successes':sum(r['returncode']==0 for r in records),'expected_rejections':sum(r['returncode']!=0 for r in records),'mode_results':mode_results,'full_normal_optimized_JSON_equal':True,'independent_closed_ZIP_exact':True,'candidate_unchanged':True,'scratch_removed':True,'no_actual_compile_render_or_marker':True})
    print(json.dumps({'passed':True,'commands':len(records),'expected_rejections':sum(r['returncode']!=0 for r in records)},indent=2))
if __name__=='__main__':main()
