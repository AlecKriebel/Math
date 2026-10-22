#!/usr/bin/env python3
"""Verify frozen author input and the narrowly corrected replacement."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent.parent
audit=root/'audit';source=root/'submission'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]
am=json.loads((audit/'AUDIT_SHA256SUMS.json').read_text())
for name,item in am['files'].items():
 p=audit/name
 if not p.is_file() or len(p.read_bytes())!=item['bytes'] or h(p)!=item['sha256']:errors.append('audit file changed: '+name)
actual={p.name for p in audit.iterdir() if p.is_file() and p.name!='AUDIT_SHA256SUMS.json'}
if actual!=set(am['files']):errors.append('audit inventory differs')
c=json.loads((audit/'CORRECTIONS.json').read_text())
if h(source/'SHA256SUMS.json')!=c['input_manifest_sha256']:errors.append('frozen manifest changed')
if h(source/'FULL_PROOF.md')!=c['input_full_proof_sha256']:errors.append('frozen proof changed')
new=(source/'FULL_PROOF.md').read_text()
for item in c['replacements']:
 if new.count(item['old'])!=1:errors.append(item['id']+' old text count is not one')
 else:new=new.replace(item['old'],item['new'])
if new!=(audit/'CORRECTED_FULL_PROOF.md').read_text():errors.append('corrected replacement differs')
if h(audit/'CORRECTED_FULL_PROOF.md')!=c['corrected_full_proof_sha256']:errors.append('corrected hash differs')
r=subprocess.run([sys.executable,str(source/'verify_manifest.py')],capture_output=True,text=True)
if r.returncode:errors.append('source manifest replay failed')
r=subprocess.run([sys.executable,str(source/'verify.py')],capture_output=True)
if r.returncode or r.stdout!=(source/'CONTROL_RESULTS.json').read_bytes():errors.append('source control replay differs')
r=subprocess.run([sys.executable,str(audit/'independent_checks.py')],capture_output=True)
if r.returncode or r.stdout!=(audit/'independent_results.json').read_bytes():errors.append('independent replay differs')
print(json.dumps({'problem_id':2887,'result':'PASS_CORRECTED_SCOPED_PARTIAL_BUNDLE' if not errors else 'FAIL','errors':errors,
 'frozen_author_unchanged':not errors,'source_mathematical_verdict':'requires explicit compactness scoping corrections',
 'corrected_mathematical_verdict':'pass as unsolved partial progress only','status':'unsolved','turns':'5/5','complete_resolution_verified':False,
 'limit':'This verifies correction provenance and controls; AUDIT.md supplies the mathematical review, with external theorem inputs.'},indent=2))
sys.exit(bool(errors))
