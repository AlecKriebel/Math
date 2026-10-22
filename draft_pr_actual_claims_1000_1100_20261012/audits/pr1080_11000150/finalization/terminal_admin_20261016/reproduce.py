#!/usr/bin/env python3
"""One clean scratch; actual stdout/stderr receipts, no compilation or service writes."""
import datetime, hashlib, io, json, os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent; A=W.parents[1]; D=A/'preprint_v1_0'; K=D/'verification_kit'; REPO=A.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def dump(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def require(test,msg):
    if not test:raise RuntimeError(msg)
def snapshot():return {p.relative_to(A).as_posix():(p.stat().st_size,sha(p)) for p in A.rglob('*') if p.is_file() and not p.is_relative_to(W)}

def main():
    require(not (W/'SEAL.json').exists(),'Do not rewrite sealed stage')
    baseline=snapshot(); receipts=[]; env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    def run(argv,cwd,expected=0,label=None,contains=None):
        p=subprocess.run([str(x) for x in argv],cwd=cwd,env=env,capture_output=True,text=True)
        r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':[str(x) for x in argv],'cwd':str(cwd),'expected':expected,'returncode':p.returncode,'label':label,'stdout':p.stdout,'stderr':p.stderr}; receipts.append(r)
        (W/'REPRODUCTION_RECEIPTS.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in receipts))
        require((p.returncode==0) if expected==0 else (p.returncode!=0),'Unexpected return: '+str(argv)+'\n'+p.stderr)
        if contains:require(contains in p.stderr,'Fault did not hit intended semantic guard: '+str(argv))
        return p.stdout
    with tempfile.TemporaryDirectory(prefix='scratch-',dir=W) as temp:
        S=Path(temp)
        env['TMPDIR']=str(S)
        with zipfile.ZipFile(D/'verification_kit.zip') as z:z.extractall(S/'clean')
        C=S/'clean/verification_kit'
        positives=[]; guardresults=[]
        for optimized in [False,True]:
            py=[sys.executable,'-I']+(['-O'] if optimized else [])
            run(py+['verify.py'],C,label='clean default')
            positives.append(json.loads(run(py+['run_checks.py'],C,label='full finite adapters')))
            run(py+['fault_checks.py'],C,label='all built-in mathematical and custody faults')
            guardresults.append(json.loads(run(py+['output_guard_checks.py'],C,label='complete existing output-alias suite')))
            rebuilt=S/('rebuilt-O.zip' if optimized else 'rebuilt.zip')
            run(py+['build_archive.py','--output',rebuilt],C,label='clean deterministic rebuild')
            require(rebuilt.read_bytes()==(D/'verification_kit.zip').read_bytes(),'Actual rebuilt archive differs')
            run(py+['verify.py','--require-binding','--binding',D/'EXTERNAL_BINDING.json','--pdf',D/'preprint.pdf','--archive',D/'verification_kit.zip'],C,label='strict current external binding')
            run(py+['verify.py','--require-binding'],C,expected=1,label='required missing binding',contains='external binding required')
            run(py+['verify.py','--binding',S/'missing.json'],C,expected=1,label='explicit missing binding',contains='input missing or nonregular')
        require(positives[0]==positives[1],'Complete normal/-O finite JSON differs')
        # Same-byte bootstrap alias, normal and optimized; identical file bytes do not excuse the alias.
        allow=C/'ALLOWLIST.json'; original=allow.read_bytes(); saved=S/'identical-allowlist.json'; saved.write_bytes(original);allow.unlink();allow.symlink_to(saved)
        for optimized in [False,True]:
            run([sys.executable,'-I']+(['-O'] if optimized else [])+['verify.py'],C,expected=1,label='identical bootstrap symlink',contains='input symlink rejected')
        allow.unlink();allow.write_bytes(original)
        # Rehash the altered status so each failure comes from the new semantic guard rather than byte mismatch.
        status=C/'TERMINAL_ADMIN_STAGE.json'; manifest=C/'MANIFEST.json'; original_status=status.read_bytes(); original_manifest=manifest.read_bytes()
        faults=[('whole_reviews_completed',1,'terminal complete review count'),('minimum_whole_reviews',1,'terminal complete review count'),('latest_review_actionable_P0_P1_P2_P3',1,'terminal latest review findings'),('root_integrity_adoption_required',False,'terminal root adoption boundary'),('publication_ready',True,'terminal publication/service boundary'),('services_held_at',1033,'terminal publication/service boundary'),('full_original_maximum_classification_bundle','SOLVED','terminal scope boundary')]
        for key,value,message in faults:
            altered=json.loads(original_status);altered[key]=value;dump(status,altered)
            m=json.loads(original_manifest)
            for r in m['files']:
                if r['path']=='TERMINAL_ADMIN_STAGE.json':r.update(bytes=status.stat().st_size,sha256=sha(status))
            dump(manifest,m)
            for optimized in [False,True]:
                run([sys.executable,'-I']+(['-O'] if optimized else [])+['verify.py'],C,expected=1,label='terminal semantic '+key,contains=message)
            status.write_bytes(original_status);manifest.write_bytes(original_manifest)
        run([sys.executable,'-B',REPO/'zenodo_deposit_tool/zenodo.py','check',D/'deposit_metadata.json'],REPO,label='actual repository native LOCAL check')
        # An independent CLOSED archive construction, not the delivered builder.
        names=obj(K/'ALLOWLIST.json')['members']; buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
            for n in names:
                info=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED
                z.writestr(info,(K/n).read_bytes())
        require(buf.getvalue()==(D/'verification_kit.zip').read_bytes(),'Independent CLOSED ZIP differs')
        payload=[]
        with zipfile.ZipFile(D/'verification_kit.zip') as z:
            require(z.namelist()==['verification_kit/'+n for n in names] and not z.comment and z.testzip() is None,'Archive order/comment/CRC')
            for i in z.infolist():
                require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==zipfile.ZIP_STORED and not i.extra and not i.comment and not i.is_dir(),'Archive header')
                body=z.read(i);require(body==(K/i.filename.removeprefix('verification_kit/')).read_bytes(),'Archive payload')
                payload.append({'path':i.filename,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
        dump(W/'ARCHIVE_PAYLOAD_CHECKS.json',{'closed_independent_byte_equal':True,'headers_and_payloads':payload})
    require(snapshot()==baseline,'Canonical audit changed during reproduction')
    dump(W/'REPRODUCTION_SUMMARY.json',{'status':'PASS','actual_commands':len(receipts),'normal_optimized_complete_finite_json_equal':True,'guard_invocations':guardresults,'terminal_semantic_cases_each_mode':len(faults),'independent_closed_zip_byte_equal':True,'canonical_inputs_unchanged_during_reproduction':len(baseline),'archive_sha256':sha(D/'verification_kit.zip'),'no_compile_render_or_page_view':True,'actual_repository_local_native_check':True,'published':False,'services_held_at':1032})
    print(json.dumps(obj(W/'REPRODUCTION_SUMMARY.json'),indent=2))
if __name__=='__main__':main()
