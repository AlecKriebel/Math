from pathlib import Path
import hashlib,json,datetime
home=Path(__file__).resolve().parent
manifest=home/'OUTPUT_MANIFEST.json';checksum=home/'OUTPUT_MANIFEST.sha256'
if manifest.exists() or checksum.exists():raise RuntimeError('Review is already sealed; do not rewrite sealed evidence silently')
files=[]
for p in sorted(home.rglob('*')):
 if p.is_symlink():raise RuntimeError('Unexpected symlink in review evidence')
 if p.is_file() and p not in {manifest,checksum}:
  b=p.read_bytes();files.append({'path':p.relative_to(home).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
value={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'algorithm':'sha256','scope':'Every retained review-directory file, including bound inputs, authored analyses/code, copied/rebuilt author artifacts, synthetic fixture records and failed-harness notes; only OUTPUT_MANIFEST.json and OUTPUT_MANIFEST.sha256 self-excluded. Third-party primary bodies/renderings are outside this directory in ignored private storage and are not included.','files':files}
manifest.write_text(json.dumps(value,indent=2)+'\n');digest=hashlib.sha256(manifest.read_bytes()).hexdigest();checksum.write_text(digest+'  OUTPUT_MANIFEST.json\n')
for item in files:
 b=(home/item['path']).read_bytes();assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
assert json.loads((home/'VERDICT.json').read_text())['review_completion_percent']==100
print(json.dumps({'review_complete':True,'verdict':'PASS_NO_REMAINING_SUBSTANTIVE_CONCERNS','sealed_files':len(files),'manifest_sha256':digest,'report_sha256':hashlib.sha256((home/'REPORT.md').read_bytes()).hexdigest(),'verdict_sha256':hashlib.sha256((home/'VERDICT.json').read_bytes()).hexdigest()}))
