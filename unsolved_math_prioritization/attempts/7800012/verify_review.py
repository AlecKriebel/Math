"""Additive portable wrapper; independent checker additionally requires SymPy."""
from pathlib import Path
import hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent;R=D/'final_review'
assert hashlib.sha256((R/'REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='d8566da423fcc51c272a47030db5217ba35df7dbe65362c2abd497747b6c77a5'
assert hashlib.sha256((D/'FINAL_FROZEN_MANIFEST.json').read_bytes()).hexdigest()=='a4b41064c8571a65e32bed10b4a630fc5e12d5a5601aacbf0bdbdb655efc463f'
for base,name in [(D,'FINAL_FROZEN_MANIFEST.json'),(R,'REVIEW_MANIFEST.json')]:
 for item in json.loads((base/name).read_text())['files']:
  b=(base/item['path']).read_bytes();assert len(b)==item['bytes'];assert hashlib.sha256(b).hexdigest()==item['sha256']
assert subprocess.check_output([sys.executable,str(R/'independent_check.py')],cwd=R)==(R/'INDEPENDENT_CHECKS.json').read_bytes()
print('PASS: frozen author/review hashes and 984 independent SymPy controls')
