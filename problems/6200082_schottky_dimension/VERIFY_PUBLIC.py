from pathlib import Path
import json,hashlib,subprocess,sys
p=Path(__file__).resolve().parent
bindings=0
for base,m in [(p,'PACKET_MANIFEST.json'),(p/'review','REVIEW_MANIFEST.json'),(p,'CURRENT_PACKET_MANIFEST.json')]:
 for e in json.loads((base/m).read_text())['files']:
  b=(base/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'];bindings+=1
r=subprocess.check_output([sys.executable,str(p/'check.py')]);assert r==(p/'CHECKS.json').read_bytes()
s=json.loads(subprocess.check_output([sys.executable,str(p/'review/verify_review.py'),'--author',str(p)]));assert s['independent_algebra_assertions']==80000 and s['local_source_bindings']==0
print(json.dumps({'author_assertions':json.loads(r)['assertions'],'independent_assertions':s['independent_algebra_assertions'],'manifest_bindings':bindings,'raw_sources_required':False,'mandatory_clarification_bound':True,'analytic_review_required':True,'result':'PASS'},indent=2))
