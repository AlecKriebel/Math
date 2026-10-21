from pathlib import Path
import concurrent.futures, subprocess, json, hashlib, sys, time
root=Path(__file__).resolve().parent
py='/opt/homebrew/opt/python@3.14/bin/python3.14'
package=root.parent/'publication_package_v1'
def run(job):
    name,opt,script,fail=job
    out=root/('replay_'+name)
    cmd=[py,'-E','-S','-B','-P']+(['-O'] if opt else [])+[str(root/'run_portable.py'),str(package/'materials/verification'/script),'--output-dir',str(out)]+(['--self-test-failure'] if fail else [])
    before=time.monotonic(); p=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
    (root/(name+'.stdout')).write_text(p.stdout)
    (root/(name+'.stderr')).write_text(p.stderr)
    row={'job':name,'command':cmd,'returncode':p.returncode,'seconds':round(time.monotonic()-before,3),'expected_failure':fail}
    if fail:
        row['passed']=p.returncode!=0 and 'deliberate explicit-guard failure' in p.stderr
    else:
        filename='exact_certificates.json' if script.startswith('exact') else 'parity_controls_results.json'
        actual=(out/filename).read_bytes() if (out/filename).exists() else b''
        expected=(package/'materials/expected'/filename).read_bytes()
        row.update(sha256=hashlib.sha256(actual).hexdigest(),byte_identity=actual==expected,json_identity=json.loads(actual)==json.loads(expected) if actual else False)
        row['passed']=p.returncode==0 and row['byte_identity']
    return row
jobs=[]
for opt in [False,True]:
    for script in ['exact_certificates.py','parity_controls.py']:
        for fail in [False,True]:
            jobs.append((script.removesuffix('.py')+('_O' if opt else '_normal')+('_failure' if fail else ''),opt,script,fail))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,jobs))
(root/'REPLAY_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
if not all(r['passed'] for r in results):raise RuntimeError('replay failure')
