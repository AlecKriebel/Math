"""Fresh independent package audit. Writes only beneath this review folder."""
from pathlib import Path
import datetime, hashlib, io, json, os, shutil, subprocess, sys, zipfile
sys.dont_write_bytecode = True
OUT = Path(__file__).absolute().parent
AUDIT = OUT.parent.parent
PRE = AUDIT / 'preprint_v1_0'
TMP = OUT / 'tmp'
receipts = []
def need(ok, msg):
    if not ok: raise ValueError(msg)
def pin(p):
    d=p.read_bytes(); return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def inventory(base):
    return {p.relative_to(base).as_posix():pin(p) for p in sorted(base.rglob('*')) if p.is_file() and not p.is_symlink()}
def call(argv,cwd,success=True,reason=None):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    x=subprocess.run(argv,cwd=cwd,capture_output=True,text=True)
    r={'utc':started,'argv':list(map(str,argv)),'cwd':str(cwd),'expected_success':success,
       'exit_code':x.returncode,'stdout':x.stdout,'stderr':x.stderr}
    receipts.append(r); write('COMMAND_RECEIPTS.json',receipts)
    need((x.returncode==0)==success,'unexpected outcome '+repr(argv))
    if reason: need(reason in x.stderr,'wrong rejection reason: '+repr(argv))
    return x
def run():
    need(not TMP.exists(),'fresh scratch required'); TMP.mkdir()
    clean=TMP/'clean'; clean.mkdir(); kit=clean/'kit'; kit.mkdir()
    canonical=PRE/'pr1094_supportkit_v1.0.zip'
    # Closed read and independent ZIP reconstruction, before extraction.
    with zipfile.ZipFile(canonical) as z:
        names=z.namelist(); need(names==sorted(set(names)),'sorted unique ZIP names')
        need(z.testzip() is None,'CRC check')
        entries=[]; buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as rebuilt:
            for i in z.infolist():
                need(i.date_time==(1980,1,1,0,0,0) and i.compress_type==0 and i.create_system==3
                     and i.external_attr==0o100644<<16,'ZIP header')
                body=z.read(i.filename)
                need(body==(PRE/'kit'/i.filename).read_bytes(),'ZIP payload')
                need(not Path(i.filename).is_absolute() and '..' not in Path(i.filename).parts,'unsafe ZIP member')
                info=zipfile.ZipInfo(i.filename,(1980,1,1,0,0,0)); info.create_system=3
                info.external_attr=0o100644<<16; info.compress_type=zipfile.ZIP_STORED
                rebuilt.writestr(info,body)
                entries.append({'path':i.filename,**pin(PRE/'kit'/i.filename),'CRC32':i.CRC,
                                'timestamp':list(i.date_time),'external_attr':i.external_attr,'create_system':i.create_system,'compress_type':i.compress_type})
        need(buf.getvalue()==canonical.read_bytes(),'exact independent CLOSED ZIP rebuild')
        z.extractall(kit)
    write('ARCHIVE_REVIEW.json',{'status':'PASS','members':entries,'closed_rebuild_equal':True,'archive':pin(canonical)})
    baseline=inventory(clean)
    math_results=[]; pdf_results=[]
    for mode in [[],['-O']]:
        label='normal' if not mode else 'optimized'; py=[sys.executable,'-B']+mode
        call(py+['scripts/verify_kit.py'],kit)
        call(py+['scripts/verify_kit.py','--require-binding'],kit,False,'binding is absent')
        call(py+['scripts/verify_kit.py','--binding','../explicit-missing.json'],kit,False,'binding is absent')
        x=call(py+['scripts/run_checks.py','--out','../checks-'+label+'.json'],kit)
        observed=json.loads(x.stdout); math_results.append(observed)
        need(observed==json.loads((PRE/'kit/NEW_CONTROLS_RESULT.json').read_text()),'full mathematical JSON changed')
        call(py+['scripts/build_support.py','--out','../support-'+label+'.zip'],kit)
        need((clean/('support-'+label+'.zip')).read_bytes()==canonical.read_bytes(),'builder ZIP mismatch')
        # Real supported build, not mocked compilation.
        call(py+['scripts/build_pdf.py','--out-dir','../pdf-'+label,'--tectonic','/opt/homebrew/bin/tectonic'],kit)
        pdf=clean/('pdf-'+label)/'paper.pdf'
        need(pdf.read_bytes()==(PRE/'paper.pdf').read_bytes(),'recompiled PDF byte mismatch')
        pdf_results.append({'mode':label,**pin(pdf),'equal_delivered_pdf':True})
        call(py+[str(PRE/'kit/scripts/verify_kit.py'),'--require-binding'],OUT)
        call(py+[str(PRE/'kit/scripts/verify_kit.py'),'--binding',str(PRE/'DEPOSIT_BINDING.json'),'--require-binding'],OUT)
        # A corrupt present default cannot be treated as optional absence.
        binding=clean/'DEPOSIT_BINDING.json'; binding.write_text('{"bad":true}')
        call(py+['scripts/verify_kit.py'],kit,False,'binding keys'); binding.unlink()
        binding.write_text('{')
        call(py+['scripts/verify_kit.py','--binding',str(binding)],kit,False,'JSONDecodeError'); binding.unlink()
    need(math_results[0]==math_results[1],'mode mathematical JSON equality')
    write('PORTABLE_RESULTS.json',{'status':'PASS','full_json_equal':True,'result':math_results[0],'PDF_builds':pdf_results})
    # Every writer invoked, with a compiler witness which must never run on rejection.
    sent=TMP/'compiler-invoked'; fake=TMP/'compiler-witness'
    fake.write_text('#!/usr/bin/env python3\nfrom pathlib import Path\nPath('+repr(str(sent))+').write_text("CALLED")\nraise SystemExit(91)\n'); fake.chmod(0o755)
    alias=TMP/'lexical'; alias.symlink_to(clean,target_is_directory=True)
    dangling=TMP/'dangling'; dangling.symlink_to(TMP/'not-present',target_is_directory=True)
    hard=TMP/'hardlink.pdf'; os.link(PRE/'paper.pdf',hard)
    leaf=TMP/'leaf'; leaf.symlink_to(TMP/'leaf-target')
    parent_file=TMP/'regular-parent'; parent_file.write_text('SENTINEL')
    upper=clean/'KIT'; mixed=clean/'KiT'
    need(upper.samefile(kit) and mixed.samefile(kit),'actual case alias premise absent')
    guard_rows=[]
    for mode in [[],['-O']]:
        label='normal' if not mode else 'optimized'; py=[sys.executable,'-B']+mode
        for writer,option in [('run_checks.py','--out'),('build_support.py','--out'),('build_pdf.py','--out-dir')]:
            key=writer+label
            cases=[('existing-input',str(kit/'paper.tex')),
                   ('existing-external',str(PRE/'paper.pdf')),
                   ('hardlink-alias',str(hard)),('leaf-symlink',str(leaf)),
                   ('ancestor-symlink',str(alias/'new'/key)),
                   ('lexical-symlink-dotdot',str(alias/'..'/key)),
                   ('dangling-dotdot',str(dangling/'..'/key)),
                   ('kit-descendant',str(kit/'new'/'deep'/key)),
                   ('kit-ancestor',str(clean)),
                   ('case-upper',str(upper/key)),('case-mixed',str(mixed/'absent'/'deeper'/key)),
                   ('nondirectory-parent',str(parent_file/'child'/key))]
            for kind,target in cases:
                before=inventory(TMP); cmd=py+['scripts/'+writer,option,target]
                if writer=='build_pdf.py': cmd+=['--tectonic',str(fake)]
                call(cmd,kit,False)
                need(before==inventory(TMP),'rejected writer altered scratch '+kind)
                need(not sent.exists(),'compiler invoked on rejected output')
                guard_rows.append({'mode':label,'writer':writer,'case':kind,'target':target,'unchanged':True,'compiler_called':False})
            # Reverse canonical directions: script path itself uses an alias.
            for script_root in [upper,mixed]:
                target=kit/'missing'/'nested'/key
                before=inventory(TMP)
                cmd=py+[str(script_root/'scripts'/writer),option,str(target)]
                if writer=='build_pdf.py': cmd+=['--tectonic',str(fake)]
                call(cmd,kit,False)
                need(before==inventory(TMP) and not sent.exists(),'reverse case rejection wrote')
                guard_rows.append({'mode':label,'writer':writer,'case':'reverse-case-script-root','script_root':str(script_root),'target':str(target),'unchanged':True,'compiler_called':False})
    write('WRITER_GUARDS.json',{'status':'PASS','case_alias_samefile_checked':True,'commands':guard_rows})
    # The bootstrap manifest itself and every input are preflighted before use.
    manifest=kit/'MANIFEST.json'; original=manifest.read_bytes(); payload=kit/'CITATION.txt'; old=payload.read_bytes()
    malformed=[]
    for mode in [[],['-O']]:
        label='normal' if not mode else 'optimized'; py=[sys.executable,'-B']+mode
        for kind in ['manifest-symlink','manifest-duplicate','missing-payload','corrupt-payload','extra-payload','symlink-payload']:
            saved=TMP/'saved-input'
            if kind=='manifest-symlink':
                manifest.rename(saved); manifest.symlink_to(saved)
            elif kind=='manifest-duplicate':
                obj=json.loads(original);obj['records'].append(obj['records'][0]);manifest.write_text(json.dumps(obj))
            elif kind=='missing-payload': payload.rename(saved)
            elif kind=='corrupt-payload': payload.write_bytes(old+b'corrupt')
            elif kind=='extra-payload': (kit/'unexpected').write_text('extra')
            elif kind=='symlink-payload':
                payload.rename(saved); payload.symlink_to(saved)
            try:
                for script in ['verify_kit.py','build_support.py','run_checks.py','build_pdf.py']:
                    target=TMP/('invalid-input-output-'+label+'-'+kind+'-'+script)
                    argv=py+['scripts/'+script]
                    if script=='build_support.py': argv+=['--out',str(target)]
                    if script=='run_checks.py': argv+=['--out',str(target)]
                    if script=='build_pdf.py': argv+=['--out-dir',str(target),'--tectonic',str(fake)]
                    call(argv,kit,False)
                    need(not target.exists() and not sent.exists(),'invalid input created output')
                    malformed.append({'mode':label,'case':kind,'script':script,'rejected_before_output':True})
            finally:
                if kind=='manifest-symlink': manifest.unlink();saved.rename(manifest)
                elif kind=='manifest-duplicate': manifest.write_bytes(original)
                elif kind=='missing-payload': saved.rename(payload)
                elif kind=='corrupt-payload': payload.write_bytes(old)
                elif kind=='extra-payload': (kit/'unexpected').unlink()
                elif kind=='symlink-payload': payload.unlink();saved.rename(payload)
            need(inventory(kit)==inventory(PRE/'kit'),'mutated test input not restored')
    write('BOOTSTRAP_AND_INPUT_GUARDS.json',{'status':'PASS','commands':malformed,'self_excluded_manifest_regular_preflight':True})
    native=json.loads((PRE/'zenodo-deposit.json').read_text()); meta=json.loads((PRE/'kit/metadata.json').read_text())
    need(set(native)=={'metadata','files'} and native['metadata']==meta,'native exact schema')
    need(native['files']==[{'path':'paper.pdf','name':'paper.pdf'},{'path':'pr1094_supportkit_v1.0.zip','name':'pr1094_supportkit_v1.0.zip'}],'native assets')
    call([sys.executable,'-B',str(Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')),'check',str(PRE/'zenodo-deposit.json')],OUT)
    write('NATIVE_LOCAL_CHECK.json',{'status':'PASS','exact_top_keys':['metadata','files'],'metadata_equal':True,'selected_assets':native['files'],'service_actions':False})
    write('REPRODUCTION_COMPLETE.json',{'status':'PASS','actual_commands':len(receipts),'expected_rejections':sum(not r['expected_success'] for r in receipts),'extraction_initial_inventory_count':len(baseline),'canonical_inputs_untouched':inventory(kit)==inventory(PRE/'kit')})
if __name__=='__main__':
    try: run()
    except BaseException as e:
        write('HARNESS_FAILURE.json',{'type':type(e).__name__,'message':str(e),'completed_commands':len(receipts)})
        raise
