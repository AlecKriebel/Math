"""Run unchanged published mathematical controls on a disposable exact copy."""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time, zipfile
ROOT=Path(__file__).resolve().parents[2]
OWN=Path(__file__).resolve().parent
SRC=ROOT/'sources/published-source'
CACHE=OWN/'replay-cache'
if CACHE.exists(): raise RuntimeError('fresh cache required')
CACHE.mkdir()
kit=CACHE/'kit';shutil.copytree(SRC,kit)
evidence=OWN/'evidence'; results=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
initial={p.relative_to(SRC).as_posix():sha(p) for p in SRC.rglob('*') if p.is_file()}
for mode in ('normal','O','OO'):
 cmd=[sys.executable]+([] if mode=='normal' else ['-'+mode])+['scripts/run_checks.py','--out',str(CACHE/f'{mode}.json')]
 start=time.monotonic();run=subprocess.run(cmd,cwd=kit,env=env,capture_output=True,text=True,timeout=180)
 (evidence/f'replay-{mode}.stdout.txt').write_text(run.stdout)
 (evidence/f'replay-{mode}.stderr.txt').write_text(run.stderr)
 if run.returncode:raise RuntimeError(f'math replay failed {mode}')
 result=json.loads(run.stdout)
 if result['status']!='PASS':raise RuntimeError('nonpassing result')
 results.append({'mode':mode,'command':cmd,'exit_code':run.returncode,'seconds':round(time.monotonic()-start,3),'result':result})
 shutil.copyfile(CACHE/f'{mode}.json',evidence/f'replay-{mode}.json')
# Source bytes, zip CRC/inventory, and deterministic package replay; no historical verdict semantics adopted.
ziprun=subprocess.run([sys.executable,'scripts/build_support.py','--out',str(CACHE/'rebuilt.zip')],cwd=kit,env=env,capture_output=True,text=True,timeout=60)
(evidence/'rebuild.stdout.txt').write_text(ziprun.stdout)
(evidence/'rebuild.stderr.txt').write_text(ziprun.stderr)
if ziprun.returncode:raise RuntimeError('archive rebuild failed')
archive=ROOT/'sources/pr1094_supportkit_v1.0.zip'
if (CACHE/'rebuilt.zip').read_bytes()!=archive.read_bytes():raise RuntimeError('rebuilt ZIP differs')
# Input-integrity and existing-output guards checked independently of removable assertions.
protected=CACHE/'exists.json';protected.write_text('sentinel\n')
guard=subprocess.run([sys.executable,'-OO','scripts/run_checks.py','--out',str(protected)],cwd=kit,env=env,capture_output=True,text=True,timeout=20)
if guard.returncode==0 or protected.read_text()!='sentinel\n':raise RuntimeError('existing output guard failed')
(evidence/'existing-output-guard.stderr.txt').write_text(guard.stderr)
# Change only the disposable copy. Mathematical entry must reject payload tampering.
f=kit/'paper.tex';f.write_bytes(f.read_bytes()+b'\n% independent disposable corruption probe\n')
bad=subprocess.run([sys.executable,'-OO','scripts/run_checks.py'],cwd=kit,env=env,capture_output=True,text=True,timeout=20)
if bad.returncode==0 or 'payload mismatch' not in bad.stderr:raise RuntimeError('tamper guard failed')
(evidence/'tamper-guard.stderr.txt').write_text(bad.stderr)
if initial!={p.relative_to(SRC).as_posix():sha(p) for p in SRC.rglob('*') if p.is_file()}:raise RuntimeError('original changed')
with zipfile.ZipFile(archive) as z:
 if z.testzip() is not None:raise RuntimeError('CRC failure')
 for info in z.infolist():
  if info.is_dir():continue
  if hashlib.sha256(z.read(info)).hexdigest()!=initial[info.filename]:raise RuntimeError('ZIP/extraction mismatch')
result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'pass','mathematical_replays':results,'recreated_zip_sha256':sha(CACHE/'rebuilt.zip'),'recreated_zip_matches_public':True,'original_extracted_file_count':len(initial),'all_originals_unchanged':True,'existing_output_guard':{'mode':'OO','returncode':guard.returncode,'preserved_sentinel':True},'payload_tamper_guard':{'mode':'OO','returncode':bad.returncode,'rejected':True},'not_run':'verify_kit.py terminal-accounting historical review semantics and PDF regeneration; neither is evidence for the current theorem','incidental_exposure':'Current verify_kit.py contains hard-coded historical whole-review no-finding counts/status flags. Read only as executable package support, after independent proof/controls; historical assessment bodies and sibling reviews not opened or adopted.'}
(evidence/'replay-summary.json').write_text(json.dumps(result,indent=2)+'\n')
shutil.rmtree(CACHE)
print(json.dumps({'status':'pass','replays':len(results),'unchanged_original_files':len(initial),'deterministic_archive':True,'guards_rejected':2}))
