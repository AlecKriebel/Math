"""Three focused schema/core-anchor controls after the main harness."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
SOURCE=BASE.parents[1]/'original/unsolved_math_prioritization/attempts/30001345'
ROOT=BASE/'tmp'/'supplemental fixture'
ENV=os.environ.copy();ENV['TMPDIR']=str(BASE/'tmp');ENV['PYTHONDONTWRITEBYTECODE']='1'
def sha(b):return hashlib.sha256(b).hexdigest()
def fresh():
    if ROOT.exists():shutil.rmtree(ROOT)
    shutil.copytree(SOURCE,ROOT)
def outer():
    p=ROOT/'PACKAGE_MANIFEST.json';d=json.loads(p.read_bytes())
    for item in d['files']:
        b=(ROOT/item['file']).read_bytes();item.update(bytes=len(b),sha256=sha(b))
    p.write_text(json.dumps(d,indent=2)+'\n');checksum()
def checksum():
    b=(ROOT/'PACKAGE_MANIFEST.json').read_bytes();(ROOT/'PACKAGE_MANIFEST.sha256').write_text(sha(b)+'  PACKAGE_MANIFEST.json\n')
def invoke(name):
    p=subprocess.run([sys.executable,'-I','-B',ROOT/'verify_publication.py','--integrity-only'],env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=3)
    if p.returncode==0:raise RuntimeError(name+' unexpectedly passed')
    return {'returncode':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),'timeout':False}
results={}
fresh();(ROOT/'PACKAGE_MANIFEST.json').write_bytes(b'{malformed');checksum();results['malformed_JSON_with_matching_checksum']=invoke('malformed')
fresh();p=ROOT/'PACKAGE_MANIFEST.json';d=json.loads(p.read_bytes());d['schema']='1';p.write_text(json.dumps(d));checksum();results['string_schema_version']=invoke('string schema')
fresh();p=ROOT/'frozen_v2/PROOF.md';p.write_bytes(b'modified proof\n');m=ROOT/'frozen_v2/FROZEN_MANIFEST.json';d=json.loads(m.read_bytes())
for item in d['files']:
    if item['file']=='PROOF.md':item.update(bytes=len(p.read_bytes()),sha256=sha(p.read_bytes()))
m.write_text(json.dumps(d,indent=2)+'\n');outer();results['proof_child_manifest_and_outer_rewritten_anchor_rejects']=invoke('fixed child anchor')
(BASE/'supplemental_guard_results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','controls':len(results)},indent=2))
