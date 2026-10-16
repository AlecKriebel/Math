from pathlib import Path
import subprocess, os, sys, json, datetime, hashlib, time
HERE=Path(__file__).resolve().parent
PKG=HERE/'extracted/outer-pedal-centroid-verification'
TMP=HERE/'replay-temp'
TMP.mkdir(exist_ok=True)
env=os.environ.copy()
env['TMPDIR']=str(TMP)
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
tick=time.monotonic()
with (HERE/'portable-full.stdout.txt').open('w') as out,(HERE/'portable-full.stderr.txt').open('w') as err:
 p=subprocess.run([sys.executable,str(PKG/'run_verification.py'),'--full'],cwd=PKG,env=env,stdout=out,stderr=err)
manifest=json.loads((PKG/'MANIFEST.json').read_text())
unchanged=all(hashlib.sha256((PKG/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in manifest['files'])
receipt={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-tick,'returncode':p.returncode,'all_archived_evidence_unchanged':unchanged,'interpreter':sys.executable,'command':['run_verification.py','--full'],'temporary_work_root':str(TMP)}
(HERE/'PORTABLE_FULL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
assert p.returncode==0 and unchanged
