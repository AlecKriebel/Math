#!/usr/bin/env python3
"""Replay reviewed fixed inputs and patch bindings; no network or source downloads."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,shutil,stat,subprocess,sys,tempfile,zipfile

def need(ok,message):
    if not ok:raise RuntimeError(message)
def info(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def regular(p):
    need(p.is_file() and all(not q.is_symlink() for q in [p,*p.parents]),'regular nonsymlink file required')
    return p.read_bytes()
def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,'use python -I -S -B')
    need(len(sys.argv)==2,'pass package directory')
    root=Path(sys.argv[1]).absolute();frozen=json.loads(regular(root/'FROZEN_INPUTS.json'))
    for name,binding in frozen['files'].items():need(info(regular(root/name))==binding,'frozen file mismatch '+name)
    payloads={};records=[]
    for a in frozen['archives']:
        manifest=json.loads(regular(root/a['manifest']));archive=root/a['archive']
        need(info(regular(archive))=={k:manifest['archive'][k] for k in ['bytes','sha256']},'archive binding')
        payload={}
        with zipfile.ZipFile(archive) as z:
            names=z.namelist();need(len(names)==len(set(names)) and set(names)==set(manifest['members']),'ZIP inventory')
            for i in z.infolist():
                p=PurePosixPath(i.filename);need(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and stat.S_ISREG(i.external_attr>>16),'ZIP path/type')
                data=z.read(i);need(info(data)==manifest['members'][i.filename],'ZIP member binding');payload[i.filename]=data
        payloads[a['archive']]=payload
    prefix='HIGHER_KOSZUL_30003060_'
    original=payloads[prefix+'AUTHOR_SAFE_FREEZE.zip'];corrected=payloads[prefix+'CORRECTED_SAFE.zip'];audit=payloads[prefix+'INDEPENDENT_AUDIT_SAFE.zip'];second=payloads[prefix+'SECOND_REVIEW_SAFE.zip']
    for dirname,payload in [('author',corrected),('independent_audit',audit),('second_review',second)]:
        for name,data in payload.items():need(regular(root/dirname/name)==data,'published extracted member differs')
    acceptance=json.loads(audit['CORRECTED_ACCEPTANCE.json'])
    for key,suffix in [('archive','CORRECTED_SAFE.zip'),('manifest','CORRECTED_EXTERNAL_MANIFEST.json'),('bootstrap','CORRECTED_BOOTSTRAP.py')]:
        need(info(regular(root/(prefix+suffix)))=={k:acceptance[key][k] for k in ['bytes','sha256']},'corrected acceptance binding')
    for field,name in [('actual_bootstrap_patch_sha256','BOOTSTRAP_HARDENING.patch'),('actual_combined_patch_sha256','COMBINED_AUTHOR_CHANGES.patch'),('source_scope_patch_sha256','SOURCE_SCOPE.patch'),('math_audit_sha256','MATHEMATICAL_AUDIT.md'),('source_scope_audit_sha256','SOURCE_SCOPE_AUDIT.md')]:
        need(info(audit[name])['sha256']==acceptance[field],'acceptance report binding')
    need(audit['SOURCE_SCOPE.patch']==second['SOURCE_SCOPE.patch'],'two scope patches differ')
    with tempfile.TemporaryDirectory(prefix='koszul-publication-') as temp:
        t=Path(temp);hostile=t/'hostile';hostile.mkdir();marker=t/'unexpected_import'
        for n in ['sitecustomize','usercustomize','hashlib','json','fractions','subprocess','zipfile']:
            (hostile/(n+'.py')).write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\nraise RuntimeError("unexpected import")\n')
        env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONHOME=str(hostile),PYTHONOPTIMIZE='2')
        def run(label,script,args=(),optimized=False,expect=None,error=None):
            r=subprocess.run([sys.executable,'-I','-S','-B',*(['-O'] if optimized else []),str(script),*map(str,args)],cwd=hostile,env=env,capture_output=True,timeout=180)
            if error:
                need(r.returncode!=0 and error.encode() in r.stderr,label+' did not fail closed')
            else:
                need(r.returncode==0,label+' failed: '+r.stderr.decode())
                if expect is not None:need(r.stdout==expect,label+' output mismatch')
            need(not marker.exists(),label+' imported hostile module')
            records.append({'test':label,'optimized':optimized,'expected_outcome':'fail_closed' if error else 'computational_pass','returncode':r.returncode,'stdout':info(r.stdout),'passed':True})
            return r.stdout
        def extract(payload,d):
            d.mkdir()
            for n,b in payload.items():
                p=d/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        scope=t/'scope';combined=t/'combined';extract(original,scope);extract(original,combined)
        patch_results=[]
        for label,d,patch in [('source_scope',scope,audit['SOURCE_SCOPE.patch']),('combined',combined,audit['COMBINED_AUTHOR_CHANGES.patch'])]:
            r=subprocess.run(['patch','--batch','--fuzz=0','-p1'],input=patch,cwd=d,capture_output=True)
            need(r.returncode==0 and b'fuzz' not in r.stdout and b'offset' not in r.stdout,'patch replay failed '+label)
            patch_results.append({'patch':label,'passed':True,'fuzz':0})
        bindings=json.loads(second['SOURCE_SCOPE_PATCH_BINDINGS.json'])['files']
        for n,v in bindings.items():
            need(info(original[n])=={'bytes':v['before_bytes'],'sha256':v['before_sha256']},'scope before binding')
            need(info((scope/n).read_bytes())=={'bytes':v['after_bytes'],'sha256':v['after_sha256']},'scope after binding')
            need((scope/n).read_bytes()==second['scope_corrected/'+n],'scope corrected exact bytes')
        need({p.relative_to(combined).as_posix():p.read_bytes() for p in combined.rglob('*') if p.is_file()}==corrected,'combined patch not exact derivative')
        boot=t/'bootstrap';boot.mkdir();(boot/'AUTHOR_BOOTSTRAP.py').write_bytes(regular(root/(prefix+'AUTHOR_BOOTSTRAP.py')))
        r=subprocess.run(['patch','--batch','--fuzz=0','-p1'],input=audit['BOOTSTRAP_HARDENING.patch'],cwd=boot,capture_output=True)
        need(r.returncode==0 and b'fuzz' not in r.stdout and b'offset' not in r.stdout,'bootstrap patch replay')
        need((boot/'AUTHOR_BOOTSTRAP.py').read_bytes()==regular(root/(prefix+'CORRECTED_BOOTSTRAP.py')) or ((boot/'CORRECTED_BOOTSTRAP.py').is_file() and (boot/'CORRECTED_BOOTSTRAP.py').read_bytes()==regular(root/(prefix+'CORRECTED_BOOTSTRAP.py'))),'bootstrap patch byte mismatch')
        patch_results.append({'patch':'bootstrap_hardening','passed':True,'fuzz':0})
        run('original author direct',scope/'verify_free_algebra.py',expect=original['RESULTS.json'])
        run('original author optimized rejection',scope/'verify_free_algebra.py',optimized=True,error='optimized Python is unsupported')
        for kind in ['CORRECTED','INDEPENDENT_AUDIT','SECOND_REVIEW']:
            run(kind+' bootstrap',root/(prefix+kind+'_BOOTSTRAP.py'),[root/(prefix+kind+'_SAFE.zip'),root/(prefix+kind+'_EXTERNAL_MANIFEST.json')])
        run('corrected bootstrap optimized rejection',root/(prefix+'CORRECTED_BOOTSTRAP.py'),[root/(prefix+'CORRECTED_SAFE.zip'),root/(prefix+'CORRECTED_EXTERNAL_MANIFEST.json')],optimized=True,error='optimized execution rejected')
        run('first audit optimized bootstrap',root/(prefix+'INDEPENDENT_AUDIT_BOOTSTRAP.py'),[root/(prefix+'INDEPENDENT_AUDIT_SAFE.zip'),root/(prefix+'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json')],optimized=True)
        run('second review optimized bootstrap rejection',root/(prefix+'SECOND_REVIEW_BOOTSTRAP.py'),[root/(prefix+'SECOND_REVIEW_SAFE.zip'),root/(prefix+'SECOND_REVIEW_EXTERNAL_MANIFEST.json')],optimized=True,error='optimized execution rejected')
        for optimized in [False,True]:
            run('first independent mathematical checker',root/'independent_audit/independent_math.py',optimized=optimized,expect=audit['INDEPENDENT_MATH_RESULTS.json'])
            run('eighteen replay controls',root/'independent_audit/test_replay_controls.py',[root],optimized=optimized,expect=audit['REPLAY_CONTROL_RESULTS.json'])
        run('second independent mathematical checker',root/'second_review/independent_check.py',expect=second['INDEPENDENT_RESULTS.json'])
        run('second independent optimized rejection',root/'second_review/independent_check.py',optimized=True,error='optimization rejected')
        need(not list(t.rglob('*.pyc')) and not marker.exists(),'startup isolation failed')
    result={'schema':'higher-koszul-publication-replay-v1','problem_id':30003060,'status':'PASS','archives_verified':4,'members_verified':sum(map(len,payloads.values())),'patches':patch_results,'corrected_acceptance_bindings_verified':True,'original_preserved':True,'runs':records,'hostile_import_marker_absent':True,'bytecode_absent':True,'source_retrieval_and_inspection_repeated':False,'provenance_rehash_repeated':False,'mathematical_proof_certified_by_execution':False,'limitation':'Replay and bounded controls supplement the algebraic proof and separately recorded source reviews. No formal or human-referee certification and no novelty claim.'}
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
