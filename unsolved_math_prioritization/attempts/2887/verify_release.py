#!/usr/bin/env python3
"""Verify the corrected publication layout and exact correction provenance."""
from pathlib import Path
import difflib,hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
m=json.loads((p/'RELEASE_SHA256SUMS.json').read_text());errors=[]
actual={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and f.name!='RELEASE_SHA256SUMS.json' and '__pycache__' not in f.parts}
if actual!=set(m['files']): errors.append('inventory')
for name,r in m['files'].items():
 f=p/name
 if not f.is_file() or f.stat().st_size!=r['bytes'] or h(f)!=r['sha256']: errors.append(name)
c=json.loads((p/'audit'/'CORRECTIONS.json').read_text());s=(p/'submission'/'FULL_PROOF.md').read_text()
for r in c['replacements']:
 if s.count(r['old'])!=1:errors.append(r['id'])
 s=s.replace(r['old'],r['new'])
if s!=(p/'corrected_release'/'FULL_PROOF.md').read_text():errors.append('corrected narrative')
if h(p/'corrected_release'/'FULL_PROOF.md')!=c['corrected_full_proof_sha256']:errors.append('corrected hash')
if h(p/'submission'/'SHA256SUMS.json')!=c['input_manifest_sha256']:errors.append('original freeze')
if h(p/'audit'/'AUDIT_SHA256SUMS.json')!=m['audit_manifest_sha256']:errors.append('audit freeze')
changed=[];diff=[]
for f in sorted((p/'submission').iterdir()):
 if not f.is_file() or f.name=='SHA256SUMS.json':continue
 a=f.read_text();b=(p/'corrected_release'/f.name).read_text()
 if a!=b:
  changed.append(f.name)
  diff.extend(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='submission/'+f.name,tofile='corrected_release/'+f.name))
if changed!=['FULL_PROOF.md','README.md','STATUS.json']:errors.append('unexpected corrected-file set')
if ''.join(diff)!=(p/'RELEASE_DIFF.patch').read_text():errors.append('release diff')
for script in ['submission/verify_manifest.py','corrected_release/verify_manifest.py','audit/verify_audit.py']:
 r=subprocess.run([sys.executable,str(p/script)],capture_output=True,text=True)
 if r.returncode:errors.append(script+': '+r.stdout+r.stderr)
for folder in ['submission','corrected_release']:
 r=subprocess.run([sys.executable,str(p/folder/'verify.py')],capture_output=True)
 if r.returncode or r.stdout!=(p/folder/'CONTROL_RESULTS.json').read_bytes():errors.append(folder+' controls')
print(json.dumps({'problem_id':2887,'result':'PASS_CORRECTED_SCOPED_PARTIAL_RELEASE' if not errors else 'FAIL','errors':errors,'files':len(actual),'mathematical_corrections':len(c['replacements']),'status':'unsolved','turns':'5/5','complete_candidate':False,'original_target_restricted_to_compact':False,'noncompact_extensions_certified':False,'limit':'Integrity and replay checks; mathematical review is in audit/AUDIT.md and accepts only the corrected partial scope.'},indent=2))
sys.exit(bool(errors))
