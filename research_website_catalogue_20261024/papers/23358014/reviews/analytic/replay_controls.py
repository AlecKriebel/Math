"""Run only four inspected mathematical helpers, unmodified, in isolated copies."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,shutil,subprocess
O=Path(__file__).resolve().parent
P=O.parents[1]
S=P/'sources/published-source/critical_wave_verification/checks'
PY=O/'cache/venv/bin/python'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(rel):
    src=S/rel;dest=O/'cache/replay'/rel;dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dest)
    assert sha(src)==sha(dest)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result=subprocess.run([str(PY),str(dest)],cwd=dest.parent,capture_output=True,text=True,timeout=120)
    (dest.parent/'stdout.txt').write_text(result.stdout)
    (dest.parent/'stderr.txt').write_text(result.stderr)
    payload=json.loads(result.stdout) if result.returncode==0 else None
    assert result.returncode==0 and payload['status']=='PASS',(rel,result.stderr)
    assert sha(src)==sha(dest)
    return {'source_path':str(src.relative_to(P)),'source_sha256':sha(src),'started_utc':start,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'returncode':result.returncode,'exact_unmodified_copy':True,'result':payload,'stdout_sha256':sha(dest.parent/'stdout.txt'),'stderr_sha256':sha(dest.parent/'stderr.txt')}
paths=['author3937/verify_algebra.py','source17/controls.py','addendum21/checks.py','variational215/independent_variational_checks.py']
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,paths))
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','programs':results,'all_original_sources_unchanged':True,'fresh_controls_preceded_helper_reading':True,'historical_expected_or_verdict_files_read':False,'full_archive_wrapper_run':False,'limits':'Four relevant scalar/symbolic/rational helper controls only; original variational helper includes explicitly non-certified high-precision diagnostics. No nonlinear PDE simulation or mathematical theorem established by finite testing alone.'}
(O/'replay-results.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({x['source_path']:x['result'].get('assertions') for x in results},indent=2))
