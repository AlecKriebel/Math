"""Independent package replay in disposable copies. No candidate mutations."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, tempfile, zipfile

A = Path(__file__).resolve().parent.parent
O = Path(__file__).resolve().parent
PY = '/opt/homebrew/opt/python@3.14/bin/python3.14'

def check(ok, label):
    if not ok:
        raise RuntimeError(label)

def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    receipts = []
    pkg = A/'publication_package_v1'
    archive = pkg/'gram_locus_support.zip'
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        check(len(names)==len(set(names)), 'duplicate ZIP names')
        check(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names), 'unsafe archive member')
        check(len(names)==15, 'unexpected ZIP membership')
        manifest = json.loads(z.read('MANIFEST.json'))
        check(set(names)==set(manifest['files'])|{'MANIFEST.json'}, 'manifest exact membership')
        member_rows=[]
        for name in names:
            body=z.read(name)
            check(body==(pkg/name).read_bytes(), 'archive/directory bytes mismatch: '+name)
            if name!='MANIFEST.json':
                check({'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}==manifest['files'][name], 'manifest hash: '+name)
            member_rows.append({'path':name,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
    check(all(pin(p)==pin(A/'native_proposal_v1/publication_package'/p.relative_to(pkg)) for p in pkg.rglob('*') if p.is_file()), 'native active package differs')
    history=json.loads((A/'ORIGINAL_FILE_MANIFEST.json').read_text())
    historical=[]
    prefix='unsolved_math_prioritization/attempts/30003480/'
    for row in history['files']:
        p=A/'native_proposal_v1/historical_original_submission'/row['repo_path'].removeprefix(prefix)
        check(pin(p)=={'bytes':row['bytes'],'sha256':row['sha256']}, 'historical bytes changed: '+str(p))
        historical.append({'path':str(p.relative_to(A)),'bytes':row['bytes'],'sha256':row['sha256']})
    check(len(historical)==17, 'historical file count')
    for kind in ['archive','native']:
        with tempfile.TemporaryDirectory(prefix=kind+'-',dir=O/'scratch') as td:
            d=Path(td)
            if kind=='archive':
                with zipfile.ZipFile(archive) as z:z.extractall(d)
                script=d/'verify_exact.py';driver=d/'verify_controls.py';reports=d
            else:
                shutil.copytree(A/'native_proposal_v1',d,dirs_exist_ok=True)
                script=d/'verify.py';driver=d/'publication_package/verify_controls.py';reports=d/'publication_package'
            for p in d.rglob('*'):
                if p.is_file():p.chmod(0o644)
                else:p.chmod(0o755)
            outputs=[]
            for mode in ['normal','optimized']:
                args=[PY,'-E','-S','-B','-P']+(['-O'] if mode=='optimized' else [])
                for mutation in ['none','weights','reflection','normalization','Q2']:
                    cp=subprocess.run(args+[str(script),'--mutate',mutation],cwd=d,capture_output=True,timeout=60)
                    name=kind+'_'+mode+'_'+mutation
                    stdout=O/'scratch'/(name+'.stdout');stderr=O/'scratch'/(name+'.stderr')
                    stdout.write_bytes(cp.stdout);stderr.write_bytes(cp.stderr)
                    expected={'weights':'exact real parity marginals','reflection':'polynomial-coordinate involution identity','normalization':'normalized integer-tensor determinant bound','Q2':'printed full-sign Q2 exact value'}
                    if mutation=='none':
                        check(cp.returncode==0 and not cp.stderr, 'baseline failure: '+name)
                        j=json.loads(cp.stdout)
                        check(j['total_checks']==46274 and not j['all_polynomial_nonexistence_proved_by_finite_checks'], 'baseline semantics')
                        check(cp.stdout==(pkg/'verification.normal.json').read_bytes(), 'baseline deposit mismatch')
                        outputs.append(cp.stdout)
                    else:
                        check(cp.returncode!=0 and not cp.stdout and ('RuntimeError: '+expected[mutation]).encode() in cp.stderr, 'false variant escaped: '+name)
                    receipts.append({'kind':kind,'mode':mode,'mutation':mutation,'exit':cp.returncode,'stdout':pin(stdout),'stderr':pin(stderr),'expected_semantic_outcome_verified':True})
                cp=subprocess.run(args+[str(driver)],cwd=d,capture_output=True,timeout=60)
                check(cp.returncode==0 and not cp.stderr,'driver failure: '+kind+'/'+mode)
                report=json.loads((reports/'negative_controls.json').read_text())
                check(report['status']=='PASS_IDENTICAL_BASELINES_AND_ALL_FALSE_VARIANTS_REJECTED' and len(report['rejections'])==8, 'driver outcome')
                receipts.append({'kind':kind,'driver_outer_mode':mode,'exit':cp.returncode,'stdout':cp.stdout.decode().strip(),'inner_rejections':len(report['rejections'])})
            check(outputs[0]==outputs[1], 'mode byte mismatch')
    result={'status':'PASS','universal_theorem_verified_by_finite_controls':False,'archive':pin(archive),'archive_members':member_rows,'native_package_identical':True,'historical_17_preserved':historical,'runtime':pin(Path(PY)),'runs':receipts}
    (O/'PACKAGE_REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','semantic_runs':20,'drivers':4,'historical_files':len(historical),'archive_members':len(member_rows)}))

if __name__=='__main__':main()
