"""Execute the frozen checksets without changing the distributed files."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,shutil,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'MANIFEST.json').read_text())
for row in manifest['files']:
 assert hashlib.sha256((HERE/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
jobs=json.loads((HERE/'CHECKSETS.json').read_text())
def run(job):
 with tempfile.TemporaryDirectory(prefix='k403a-'+job['name']+'-') as tmp:
  d=Path(tmp);p=d/Path(job['script']).name;shutil.copyfile(HERE/job['script'],p)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==job['source_script_sha256']
  r=subprocess.run([sys.executable,str(p)],capture_output=True)
  if r.returncode:raise RuntimeError(job['name']+': '+r.stderr.decode())
  actual=json.loads((d/job['result_file']).read_text()) if job['result_file'] else json.loads(r.stdout)
  expected=json.loads((HERE/job['expected']).read_text())
  for obj in [actual,expected]:
   for key in ['utc','elapsed_seconds']:obj.pop(key,None)
  if actual!=expected:raise AssertionError(job['name']+' differs from its complete reference receipt')
  return {'checkset':job['name'],'status':'PASS','complete_receipt_match':True}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,jobs))
print(json.dumps({'status':'PASS','results':results,'scope':'Finite algebra/constructions and diagnostics; universal proof is in the manuscript. No interval or proof-assistant certification.'},indent=2))
