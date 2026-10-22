#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,sys,os,shutil,io,tarfile,gzip,hashlib,datetime
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent;CAND=BASE/'preprint_v1_0';work=HERE/'private/layered_fault';shutil.copytree(HERE/'private/full',work)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');rows=[]
def run(tag,pass_expected=False):
 for opt in [False,True]:
  for dep in [False,True]:
   args=[sys.executable]+(['-O'] if opt else [])+['verify_package.py']+(['--require-deposit'] if dep else []);p=subprocess.run(args,cwd=work,env=env,capture_output=True,text=True);name=tag+('_optimized' if opt else '_normal')+('_required' if dep else '_default');(HERE/(name+'_STDOUT.txt')).write_text(p.stdout);(HERE/(name+'_STDERR.txt')).write_text(p.stderr)
   if (p.returncode==0)!=pass_expected:raise RuntimeError('Unexpected layered '+name+p.stderr)
   rows.append({'name':name,'args':args,'returncode':p.returncode,'expected_pass':pass_expected,'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest(),'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()})
archive=work/'supportkit-v1.0.tar.gz';side=work/'ARCHIVE_SHA256.json';a0=archive.read_bytes();s0=side.read_bytes()
with tarfile.open(fileobj=io.BytesIO(a0),mode='r:gz') as t:items=[(m,t.extractfile(m).read()) for m in t.getmembers()]
for tag in ['tar_payload','tar_mode','tar_missing','tar_duplicate']:
 buffer=io.BytesIO()
 with tarfile.open(fileobj=buffer,mode='w',format=tarfile.PAX_FORMAT) as t:
  for i,(m,b) in enumerate(items):
   m=__import__('copy').copy(m)
   if i==0 and tag=='tar_missing':continue
   if i==0 and tag=='tar_payload':b=b'X'+b[1:]
   if i==0 and tag=='tar_mode':m.mode=0o755
   t.addfile(m,io.BytesIO(b))
   if i==0 and tag=='tar_duplicate':t.addfile(m,io.BytesIO(b))
 mutated=gzip.compress(buffer.getvalue(),compresslevel=9,mtime=0);archive.write_bytes(mutated);o=json.loads(s0);o.update(bytes=len(mutated),sha256=hashlib.sha256(mutated).hexdigest());side.write_text(json.dumps(o,indent=2)+'\n')
 run('LAYERED_'+tag);archive.write_bytes(a0);side.write_bytes(s0)
# Change an old authored verdict and its copy-map identity, then rehash current
# content/archive. Historical OUTPUT_PINS must remain a separate guard.
p=work/'evidence/reviews/package_01/VERDICT.json';o=json.loads(p.read_text());o['adversary_injected_field']='historical substitution';p.write_text(json.dumps(o,indent=2)+'\n');copyp=work/'EVIDENCE_COPY_MANIFEST.json';o=json.loads(copyp.read_text());b=p.read_bytes()
for r in o['files']:
 if r['package_path']=='evidence/reviews/package_01/VERDICT.json':r.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
copyp.write_text(json.dumps(o,indent=2)+'\n');build=subprocess.run([sys.executable,'build_archive.py'],cwd=work,env=env,capture_output=True,text=True);(HERE/'PREPARE_LAYERED_HISTORIC_STDOUT.txt').write_text(build.stdout);(HERE/'PREPARE_LAYERED_HISTORIC_STDERR.txt').write_text(build.stderr)
if build.returncode:raise RuntimeError('Layered prepare failed')
run('LAYERED_historic_after_copymap_rehash')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','controls':rows,'faults':5,'mode_combinations_per_fault':4,'failures':len(rows),'outer_hashes_refreshed':True,'historic_copy_map_and_content_rehashed':True,'all_rejected':True};(HERE/'LAYERED_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='controls'},indent=2))
