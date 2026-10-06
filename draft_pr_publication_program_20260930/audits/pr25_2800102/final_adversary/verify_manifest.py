from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent;sha=lambda b:hashlib.sha256(b).hexdigest();m=json.loads((H/'MANIFEST.json').read_text());s=json.loads((H/'FINAL_SEAL.json').read_text());assert sha((H/'MANIFEST.json').read_bytes())==s['first_party_manifest_sha256'];assert len(m['files'])==s['first_party_entry_count']
for f in m['files']:
 b=(H/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['path']
for file,key in [('REPORT.md','report_sha256'),('VERDICT.json','verdict_sha256'),('EARLY_SEAL.json','early_seal_sha256'),('EARLY_CRITERION_AND_RECONSTRUCTION.md','early_criterion_sha256')]:assert sha((H/file).read_bytes())==s[key],file
print(json.dumps({'pass':True,'first_party_files':len(m['files']),'manifest_sha256':s['first_party_manifest_sha256'],'final_seal_sha256':sha((H/'FINAL_SEAL.json').read_bytes())},indent=2))
