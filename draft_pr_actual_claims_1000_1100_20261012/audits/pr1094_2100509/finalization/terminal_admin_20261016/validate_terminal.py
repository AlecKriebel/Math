"""Actual standard commands and coherent terminal faults in one own extraction."""
from pathlib import Path
import copy, datetime, hashlib, io, json, os, shutil, subprocess, sys, zipfile, zlib
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; A=R.parent.parent; P=A/'preprint_v1_0'; K=P/'kit'; T=R/'scratch'
commands=[]; cleanup_rows=[]; semantic=[]; guards=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def wj(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def rec(p,n):
    b=p.read_bytes();return {'path':n,'bytes':len(b),'sha256':sha(b)}
def pins(root):return {p.relative_to(root).as_posix():rec(p,p.relative_to(root).as_posix()) for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()}
def clean(p,label):
    if not p.exists() and not p.is_symlink():return
    if p.is_symlink():cleanup_rows.append({'path':str(p.relative_to(R)),'symlink_target':os.readlink(p),'label':label});p.unlink();return
    paths=[p] if p.is_file() else sorted(p.rglob('*'))
    for q in paths:
        if q.is_symlink():cleanup_rows.append({'path':str(q.relative_to(R)),'symlink_target':os.readlink(q),'label':label})
        elif q.is_file():cleanup_rows.append({**rec(q,str(q.relative_to(R))),'label':label})
    if p.is_file():p.unlink()
    else:shutil.rmtree(p)
def run(cwd,args,ok=True,label='',error=None):
    d=subprocess.run([str(x) for x in args],cwd=cwd,capture_output=True)
    row={'label':label,'cwd':str(cwd),'argv':[str(x) for x in args],'exit_code':d.returncode,
         'stdout':d.stdout.decode(errors='replace'),'stderr':d.stderr.decode(errors='replace'),
         'stdout_sha256':sha(d.stdout),'stderr_sha256':sha(d.stderr)}
    commands.append(row)
    wj(R/'COMMAND_RECEIPTS.json',{'utc':now(),'status':'IN_PROGRESS','commands':commands})
    need((d.returncode==0)==ok,'unexpected outcome '+label)
    if error:need(error in row['stderr'],'unexpected rejection '+label)
    return d
def refresh_manifest(root):
    m=json.loads((root/'MANIFEST.json').read_text())
    m['records']=[rec(p,p.relative_to(root).as_posix()) for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink() and p!=root/'MANIFEST.json']
    wj(root/'MANIFEST.json',m)
def refresh_evidence(root,role,mutate):
    t=json.loads((root/'TERMINAL_ACCOUNTING_20261016.json').read_text())
    e=t['evidence'];p=root/e[role]['copy_path'];x=json.loads(p.read_text());mutate(x);wj(p,x)
    # Keep all documentary hashes coherent so faults reach semantic checks.
    if role in ('verdict','report','derivation','source_ledger'):
        pp=root/e['output_pins']['copy_path'];op=json.loads(pp.read_text())
        name=e[role]['original_path'].split('/')[-1]
        for row in op['records']:
            if row['path']==name:row.update(rec(p,name))
        wj(pp,op)
    if role in ('verdict','report','derivation','source_ledger','output_pins'):
        pp=root/e['output_pins']['copy_path'];sp=root/e['seal']['copy_path'];s=json.loads(sp.read_text())
        s['output_pins']=rec(pp,'OUTPUT_PINS.json');wj(sp,s)
        rp=root/e['root_adoption']['copy_path'];r=json.loads(rp.read_text());r['output_pins_sha256']=sha(pp.read_bytes());wj(rp,r)
    ledger=json.loads((root/'TERMINAL_SOURCE_COPY_LEDGER.json').read_text())
    for row in ledger['copies']:
        q=rec(root/row['copy_path'],row['original_path']);row.update({k:q[k] for k in ('bytes','sha256')})
    wj(root/'TERMINAL_SOURCE_COPY_LEDGER.json',ledger)
    by={r['original_path']:r for r in ledger['copies']}
    for role,row in t['evidence'].items():t['evidence'][role]=by[row['original_path']]
    wj(root/'TERMINAL_ACCOUNTING_20261016.json',t);refresh_manifest(root)

def main():
    need(not T.exists(),'own scratch already exists')
    T.mkdir(); root=T/'kit'; root.mkdir()
    archive=P/'pr1094_supportkit_v1.0.zip'
    original=pins(K)
    with zipfile.ZipFile(archive) as z:z.extractall(root)
    originals={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
    def restore():
        for n,b in originals.items():
            p=root/n
            if p.is_symlink():p.unlink()
            if not p.exists() or p.read_bytes()!=b:p.write_bytes(b)
        need(pins(root)==original,'extraction not restored exactly')
    names=sorted(original)
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w') as z:
        for n in names:
            i=zipfile.ZipInfo(n,(1980,1,1,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED
            z.writestr(i,(K/n).read_bytes())
    need(buffer.getvalue()==archive.read_bytes(),'independent CLOSED ZIP differs')
    archive_rows=[]
    with zipfile.ZipFile(archive) as z:
        need(z.namelist()==names and len(names)==len(set(names)) and z.testzip() is None,'archive inventory/CRC')
        for i in z.infolist():
            b=z.read(i.filename);need(b==(K/i.filename).read_bytes(),'archive payload')
            need(i.date_time==(1980,1,1,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==zipfile.ZIP_STORED,'archive header')
            need(i.CRC==zlib.crc32(b),'individual CRC')
            archive_rows.append({**rec(K/i.filename,i.filename),'crc32':i.CRC,'date_time':list(i.date_time),'create_system':i.create_system,'external_attr':i.external_attr,'compression':i.compress_type,'compressed_bytes':i.compress_size})
    wj(R/'CLOSED_ARCHIVE_REVIEW.json',{'utc':now(),'status':'PASS','independently_built_only_read_after_close':True,'byte_exact':True,'archive':rec(archive,archive.name),'member_count':len(names),'records':archive_rows})
    all_math=[]
    witness=T/'compiler-witness';marker=T/'COMPILER_WAS_INVOKED'
    witness.write_text('#!/bin/sh\necho invoked > "'+str(marker)+'"\nexit 97\n');witness.chmod(0o755)
    for optimized in (False,True):
        mode='optimized' if optimized else 'normal';py=[sys.executable,'-B']+(['-O'] if optimized else [])
        run(root,py+['scripts/verify_kit.py'],label=mode+' documented verifier/default absent')
        d=run(root,py+['scripts/run_checks.py','--out','../checks-'+mode+'.json'],label=mode+' documented math full JSON/safe sibling')
        actual=json.loads(d.stdout);need(actual==json.loads((T/('checks-'+mode+'.json')).read_text())==json.loads((K/'NEW_CONTROLS_RESULT.json').read_text()),'math full JSON differs');all_math.append(actual)
        out=T/('support-'+mode+'.zip');run(root,py+['scripts/build_support.py','--out','../'+out.name],label=mode+' documented CLOSED archive writer/safe sibling');need(out.read_bytes()==archive.read_bytes(),'actual archive builder differs');clean(out,'completed exact archive build')
        run(K,py+['scripts/verify_kit.py','--require-binding'],label=mode+' canonical present strict default')
        run(K,py+['scripts/verify_kit.py','--binding','../DEPOSIT_BINDING.json','--require-binding'],label=mode+' canonical explicit strict binding')
        for args,label in ((['--require-binding'],'required default missing'),(['--binding',str(T/'missing.json')],'explicit missing')):
            run(root,py+['scripts/verify_kit.py']+args,ok=False,label=mode+' '+label,error='required or explicit binding is absent')
        bad=T/'DEPOSIT_BINDING.json';bad.write_text('{}\n')
        for args,label in (([],'corrupt present default'),(['--binding',str(bad)],'corrupt explicit binding')):
            run(root,py+['scripts/verify_kit.py']+args,ok=False,label=mode+' '+label,error='binding keys')
        clean(bad,'corrupt binding fault')
        # Semantically coherent faults refresh root manifest and every copied
        # evidence locator/hash that depends on the changed documentary bytes.
        cases=[
          ('count',lambda t:t.update(completed_new_whole_package_reviews=1),'terminal whole-review counts'),
          ('minimum',lambda t:t.update(minimum_new_whole_package_reviews=1),'terminal whole-review counts'),
          ('boolean_count',lambda t:t.update(completed_new_whole_package_reviews=True),'terminal whole-review counts'),
          ('new_review_required',lambda t:t.update(new_complete_whole_review_required=True),'terminal whole-review counts'),
          ('publication_ready',lambda t:t.update(publication_ready=True),'terminal false flag'),
          ('issues_resolved',lambda t:t.update(issues_resolved=True),'terminal false flag'),
          ('published',lambda t:t.update(published=True),'terminal false flag'),
          ('root_adopted',lambda t:t.update(root_terminal_integrity_adopted=True),'terminal false flag'),
          ('root_not_required',lambda t:t.update(root_terminal_integrity_required=False),'terminal true flag'),
          ('priority',lambda t:t.update(full_result_priority='ESTABLISHED'),'terminal priority'),
          ('human_review',lambda t:t.update(external_human_peer_review=True),'terminal false flag'),
          ('unrefereed',lambda t:t.update(unrefereed=False),'terminal true flag'),
          ('hold',lambda t:t.update(ordered_services_hold_pr=1094),'terminal service hold'),
          ('services',lambda t:t.update(service_actions_permitted=True),'terminal service hold'),
          ('scope',lambda t:t.update(mathematical_scope='Fixed Cartesian matrix everywhere'),'terminal mathematical scope'),
          ('latest_findings',lambda t:t['latest_whole_review'].update(P3=1),'terminal latest whole review'),
        ]
        for name,mutate,error in cases:
            restore();p=root/'TERMINAL_ACCOUNTING_20261016.json';t=json.loads(p.read_text());mutate(t);wj(p,t);refresh_manifest(root)
            run(root,py+['scripts/verify_kit.py'],ok=False,label=mode+' coherent terminal '+name,error=error)
            semantic.append({'mode':mode,'case':name,'manifest_refreshed':True,'expected_semantic_error':error})
        ecases=[('verdict_findings','verdict',lambda x:x.update(P3=1),'terminal verdict semantics'),
                ('verdict_priority','verdict',lambda x:x.update(novelty='NEW'),'terminal verdict priority'),
                ('verdict_readiness','verdict',lambda x:x.update(publication_ready=True),'terminal evidence readiness'),
                ('root_count','root_adoption',lambda x:x.update(whole_reviews_completed=1),'terminal root adoption semantics'),
                ('root_hold','root_adoption',lambda x:x.update(services_held_after_pr=1094),'terminal evidence service hold'),
                ('root_priority','root_adoption',lambda x:x.update(full_result_and_method_priority_novelty_worldwide_openness='NEW'),'terminal root priority'),
                ('seal_findings','seal',lambda x:x.update(P2=1),'terminal seal semantics')]
        for name,role,mutate,error in ecases:
            restore();refresh_evidence(root,role,mutate)
            run(root,py+['scripts/verify_kit.py'],ok=False,label=mode+' coherent copied evidence '+name,error=error)
            semantic.append({'mode':mode,'case':name,'manifest_and_all_dependent_evidence_hashes_refreshed':True,'expected_semantic_error':error})
        restore()
        # Original static writer contracts, ordinary and optimized, with an
        # executable compiler witness that MUST never be invoked.
        for script,flag in (('run_checks.py','--out'),('build_support.py','--out'),('build_pdf.py','--out-dir')):
            for kind in ('existing_input','external_PDF','hardlink','leaf_symlink','ancestor_symlink','symlink_dotdot','PDF_child','case_forward_upper','case_forward_mixed','case_reverse_upper','case_reverse_mixed'):
                case=T/'writer_case';case.mkdir();external=case/'paper.pdf';external.write_bytes((P/'paper.pdf').read_bytes());invoke=root
                if kind=='existing_input':target=root/'paper.tex';error='output must be absent'
                elif kind=='external_PDF':target=external;error='output must be absent'
                elif kind=='hardlink':target=case/'alias';os.link(external,target);error='output must be absent'
                elif kind=='leaf_symlink':target=case/'link';target.symlink_to(external);error='symlink component'
                elif kind=='ancestor_symlink':q=case/'link';q.symlink_to(root,target_is_directory=True);target=q/'fresh';error='symlink component'
                elif kind=='symlink_dotdot':q=case/'link';q.symlink_to(root,target_is_directory=True);target=q/'..'/'fresh';error='symlink component'
                elif kind=='PDF_child':target=external/'absent'/'child';error='ancestor is not a directory'
                else:
                    alias=root.with_name('KIT' if kind.endswith('upper') else 'KiT');need(alias.samefile(root),'actual case alias premise failed')
                    if 'reverse' in kind:invoke=alias;target=root/'absent1'/'absent2'/'fresh';error='overlaps protected kit'
                    else:target=alias/'absent1'/'absent2'/'fresh';error='output physically overlaps protected kit'
                before=pins(root);outside=external.read_bytes();args=py+[str(invoke/'scripts'/script),flag,str(target)]
                if script=='build_pdf.py':args+=['--tectonic',str(witness)]
                run(T,args,ok=False,label=mode+' actual writer '+script+' '+kind,error=error)
                need(pins(root)==before and external.read_bytes()==outside and not marker.exists(),'writer changed input or invoked compiler')
                need(not (root/'absent1').exists() and not (case/'fresh').exists(),'writer created output')
                guards.append({'mode':mode,'writer':script,'case':kind,'rejected_before_write_or_compiler':True,'samefile_confirmed':kind.startswith('case_')})
                clean(case,'completed writer rejection')
        # Bootstrap is self-excluded, so regular-file preparse must independently
        # reject its symlink even though no manifest record can hash it.
        mp=root/'MANIFEST.json';saved=T/'saved-manifest.json';saved.write_bytes(mp.read_bytes());mp.unlink();mp.symlink_to(saved)
        for script,args in (('verify_kit.py',[]),('run_checks.py',[]),('build_support.py',['--out',str(T/'no.zip')]),('build_pdf.py',['--out-dir',str(T/'no-pdf'),'--tectonic',str(witness)])):
            run(root,py+['scripts/'+script]+args,ok=False,label=mode+' self-excluded manifest symlink '+script,error='symlink component')
            need(not marker.exists() and not (T/'no.zip').exists() and not (T/'no-pdf').exists(),'bootstrap rejection wrote output')
        mp.unlink();mp.write_bytes(saved.read_bytes());clean(saved,'bootstrap original saved bytes');restore()
    need(all_math[0]==all_math[1],'normal/optimized full JSON differs')
    repo=Path('/Users/alec/Documents/Math');native=run(repo,[sys.executable,'-B',str(repo/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'zenodo-deposit.json')],label='actual repository uploader LOCAL-ONLY check')
    (R/'REPOSITORY_UPLOADER_LOCAL_CHECK.json').write_bytes(native.stdout)
    need(pins(K)==original,'canonical inputs changed during validation')
    wj(R/'SEMANTIC_CONTROLS.json',{'utc':now(),'status':'PASS','actual_rejections':semantic,'count':len(semantic),'coherent_faults_not_just_manifest_mismatch':True})
    wj(R/'WRITER_BOOTSTRAP_CONTROLS.json',{'utc':now(),'status':'PASS','writer_cases':guards,'writer_rejections':len(guards),'bootstrap_actual_rejections':8,'executable_compiler_witness_never_invoked':True,'no_compile_or_render':True})
    summary={'utc':now(),'status':'PASS','actual_commands':len(commands),'expected_rejections':sum(c['exit_code']!=0 for c in commands),'semantic_rejections':len(semantic),'writer_rejections':len(guards),'bootstrap_rejections':8,'normal_optimized_full_math_JSON_equals_NEW_CONTROLS_RESULT':True,'independent_CLOSED_ZIP_byte_exact':True,'native_repository_check_LOCAL_ONLY':True,'no_compile_or_render':True,'canonical_inputs_unchanged':True}
    wj(R/'VALIDATION.json',summary)
    wj(R/'COMMAND_RECEIPTS.json',{'utc':now(),'status':'PASS','commands':commands})
    clean(T,'completed own single compact extraction and derivatives')
    wj(R/'OWN_SCRATCH_CLEANUP.json',{'utc':now(),'only_own_derivatives_removed_after_hashing':True,'records':cleanup_rows})
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
