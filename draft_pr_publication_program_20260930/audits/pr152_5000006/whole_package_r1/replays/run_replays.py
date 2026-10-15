"""R1 original harness: frozen inventory, full archive, fresh success/failure runs."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, zipfile
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
CASE = OUT.parent.parent
PKG = CASE / 'publication_package_v1'
sha = lambda b: hashlib.sha256(b).hexdigest()
frozen = json.loads((CASE / 'PACKAGE_REVIEW_INPUT.json').read_text())
checks = {}
def ck(name, condition):
    checks[name] = bool(condition)
    if not condition:
        raise RuntimeError(name)

actual = {str(p.relative_to(PKG)): {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
          for p in sorted(PKG.rglob('*')) if p.is_file()}
ck('frozen_inventory_exact', actual == frozen['package_files'])
with zipfile.ZipFile(PKG / 'labelled_length_ratio_support.zip') as z:
    ck('zip_no_crc_errors', z.testzip() is None)
    ck('zip_members_exact', sorted(z.namelist()) == sorted(frozen['zip_members']))
    ck('zip_no_duplicates', len(z.namelist()) == len(set(z.namelist())))
    ck('zip_safe_paths', all(not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist()))
    for n in z.namelist():
        ck('zip_bytes:' + n, z.read(n) == (PKG / n).read_bytes())
lines = (PKG / 'SHA256SUMS.txt').read_text().splitlines()
summed = {}
for line in lines:
    digest, name = line.split('  ', 1)
    ck('checksum:' + name, sha((PKG / name).read_bytes()) == digest)
    summed[name] = digest
ck('checksum_scope_exact', set(summed) == set(actual) - {'SHA256SUMS.txt', 'labelled_length_ratio_support.zip'})
meta = json.loads((PKG / 'metadata.json').read_text())
deposit = json.loads((PKG / 'zenodo-deposit.json').read_text())
ck('deposit_metadata_identical', deposit['metadata'] == meta)
ck('deposit_files_exist', all((PKG / x['path']).is_file() for x in deposit['files']))
ck('deposit_exact_deliverables', [x['path'] for x in deposit['files']] == ['labelled_length_ratio.pdf','labelled_length_ratio_support.zip'])

runs = []
scripts = ['verify_exact.py', 'exact_reversal_counterexample.py']
receipt_names = ['verification.json','exact_reversal_counterexample.json']
for mode in ['normal','optimized']:
    scratch = OUT / mode
    shutil.copytree(PKG, scratch, dirs_exist_ok=True)
    for name in receipt_names:
        (scratch / 'verification' / name).unlink()
    for script, receipt in zip(scripts, receipt_names):
        cmd = [sys.executable] + (['-O'] if mode == 'optimized' else []) + [str(scratch / 'verification' / script)]
        proc = subprocess.run(cmd, cwd=scratch, text=True, capture_output=True)
        (OUT / (mode+'-'+script+'.stdout')).write_text(proc.stdout)
        (OUT / (mode+'-'+script+'.stderr')).write_text(proc.stderr)
        ck('success_exit:' + mode + ':' + script, proc.returncode == 0)
        data = json.loads((scratch / 'verification' / receipt).read_text())
        ck('receipt_status:' + mode + ':' + script, data['status'] == 'PASS')
        ck('receipt_matches_frozen:' + mode + ':' + script, data == json.loads((PKG / 'verification' / receipt).read_text()))
        runs.append({'mode':mode,'script':script,'exit':proc.returncode,'receipt':data})

# False predicates and a wrong Q-corner dictionary are inserted only into fresh copies.
mutations = [
    ('verify_exact.py', "ck('vertex_class_count',len(classes)==expected)", "ck('vertex_class_count',False)", 'vertex_class_count'),
    ('verify_exact.py', 'beta=diff-t*delta+alpha+F(2,n)', 'beta=diff-t*delta+alpha', 'all_corner_index_congruences'),
    ('exact_reversal_counterexample.py', "ck('regular_pentagon_cosine_relation',", "ck('regular_pentagon_cosine_relation',False and ", 'regular_pentagon_cosine_relation'),
]
failures=[]
for index,(script,old,new,label) in enumerate(mutations):
    for mode in ['normal','optimized']:
        scratch=OUT/('failure-'+str(index)+'-'+mode)
        shutil.copytree(PKG,scratch,dirs_exist_ok=True)
        for name in receipt_names:
            (scratch/'verification'/name).unlink()
        p=scratch/'verification'/script
        code=p.read_text()
        ck('unique_mutation:'+str(index)+':'+mode,code.count(old)==1)
        p.write_text(code.replace(old,new))
        cmd=[sys.executable]+(['-O'] if mode=='optimized' else [])+[str(p)]
        proc=subprocess.run(cmd,cwd=scratch,text=True,capture_output=True)
        (OUT/('failure-'+str(index)+'-'+mode+'.stderr')).write_text(proc.stderr)
        ck('failure_exit:'+str(index)+':'+mode,proc.returncode!=0)
        ck('failure_named_condition:'+str(index)+':'+mode,label in proc.stderr.splitlines()[-1])
        ck('failure_no_success_receipt:'+str(index)+':'+mode,all(not (scratch/'verification'/name).exists() for name in receipt_names))
        failures.append({'index':index,'mode':mode,'script':script,'exit':proc.returncode,'expected_first_condition':label,'stderr':proc.stderr})

result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','checks':checks,'runs':runs,'failures':failures,
        'python':sys.version,'input_inventory':actual,'scope':'Reproduction and packaging; not universal proof or imported theorem verification.'}
(OUT/'replay_results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','inventory':len(actual),'checks':len(checks),'success_runs':len(runs),'failure_runs':len(failures)},indent=2))
