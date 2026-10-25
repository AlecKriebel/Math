"""Unmodified mathematical replays on separate disposable copies; no review-body adoption."""
from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time,os,datetime,zipfile
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[1]
SRC=ROOT/'sources/published-source/aim_5_2_verification';CACHE=OWN/'replay-cache';E=OWN/'evidence'
if CACHE.exists():raise RuntimeError('fresh cache required')
CACHE.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
initial={p.relative_to(ROOT/'sources/published-source').as_posix():sha(p) for p in (ROOT/'sources/published-source').rglob('*') if p.is_file()}
programs=['packet/verify.py','packet/audit/independent_algebra.py','packet/audit/independent_audit.py'];results=[]
for mode in ['normal','O','OO']:
 kit=CACHE/mode;shutil.copytree(SRC,kit)
 for index,program in enumerate(programs):
  tag=f'{mode}-{index}';cmd=[sys.executable]+([] if mode=='normal' else ['-'+mode])+[program]
  start=time.monotonic();p=subprocess.run(cmd,cwd=kit,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=30)
  (E/f'replay-{tag}.stdout.txt').write_text(p.stdout);(E/f'replay-{tag}.stderr.txt').write_text(p.stderr)
  if p.returncode:raise RuntimeError(f'replay failed {tag}')
  data=json.loads(p.stdout)
  if not data['status'].startswith('PASS'):raise RuntimeError('nonpassing replay')
  outputs=[]
  if index:
   name='independent_algebra_results.json' if index==1 else 'independent_results.json'
   out=kit/'packet/audit'/name
   dest=E/f'replay-{tag}-{name}';shutil.copyfile(out,dest)
   outputs.append({'path':dest.relative_to(OWN).as_posix(),'sha256':sha(dest)})
  results.append({'mode':mode,'program':program,'source_sha256':sha(SRC/program),'command':cmd,'exit_code':p.returncode,'seconds':round(time.monotonic()-start,4),'result':data,'regenerated_outputs':outputs})
# Re-hash public assets and ALL archive-member source bytes after replays.
receipt=json.loads((ROOT/'sources/receipt.json').read_text())
for f in receipt['files']:
 p=ROOT/'sources'/f['name'];assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256']
for archive in receipt['archives']:
 with zipfile.ZipFile(ROOT/'sources'/archive['name']) as z:
  assert z.testzip() is None
  for m in archive['members']:
   b=z.read(m['member']);assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
   p=ROOT/'sources'/archive['extraction_root']/m['member'];assert p.read_bytes()==b
assert initial=={p.relative_to(ROOT/'sources/published-source').as_posix():sha(p) for p in (ROOT/'sources/published-source').rglob('*') if p.is_file()}
summary={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'pass','replays':results,'unmodified_programs':True,'all_originals_unchanged':True,'extracted_files':len(initial),'all_archive_crc_and_member_byte_checks':True,'limitations':'Only the three mathematical programs were replayed; historical review/status bodies and preexisting result JSONs were not read or adopted. Frozen ATTEMPT_1.md is read as opaque bytes by a helper to verify its hash. Private regenerated output files replace copies only.'}
(E/'replay-summary.json').write_text(json.dumps(summary,indent=2)+'\n');shutil.rmtree(CACHE)
print(json.dumps({'status':'pass','replays':len(results),'original_extracted_files':len(initial),'all_originals_unchanged':True}))
