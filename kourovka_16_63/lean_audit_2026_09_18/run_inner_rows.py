from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess,time,json
root=Path.cwd()
out=root.parent/'lean_audit_2026_09_18'/'inner_rows'
out.mkdir(exist_ok=True)
target=root/'.lake/build/lib/lean/Kourovka/Certificates/InnerChecks'
target.mkdir(parents=True,exist_ok=True)
def run(i):
    label=f'Row{i:02d}'
    start=time.time()
    cmd=['lake','env','lean','-j1','-s65536','-o',str(target/(label+'.olean')),f'Kourovka/Certificates/InnerChecks/{label}.lean']
    with (out/(label+'.log')).open('w') as f:
        result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
    record={'row':i,'returncode':result.returncode,'seconds':time.time()-start}
    (out/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record),flush=True)
    return record
with ThreadPoolExecutor(max_workers=2) as pool:
    records=list(pool.map(run,range(30)))
(out/'summary.json').write_text(json.dumps(records,indent=2)+'\n')
raise SystemExit(any(x['returncode'] for x in records))
