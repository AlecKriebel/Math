import hashlib,json,os,subprocess,sys,zipfile
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent;D=R.parents[1]/'publication';W=R/'private/cold';W.mkdir(exist_ok=True);E=W/'extracted';E.mkdir(exist_ok=True)
MAN='5f86b1126a90ffa4a7d9725a039b89e5ab1653f8a6c3fcd1f96a4b11e4553fa4';PIN='7f661daf498cd151ddd5fd44eb0d7d763b8bdfdbf7c12262dc5255a0133a4bc6'
with zipfile.ZipFile(D/'deep-derived-pure-braids-source-verification-v1.0.zip') as z:
 assert hashlib.sha256(z.read('PACKAGE_MANIFEST.json')).hexdigest()==MAN
 assert hashlib.sha256(z.read('verify_package.py')).hexdigest()==PIN
 for n in z.namelist():
  p=Path(n);assert not p.is_absolute() and '..' not in p.parts
 z.extractall(E)
assert hashlib.sha256((E/'verify_package.py').read_bytes()).hexdigest()==PIN
print('Authenticated external verifier before execution',flush=True)
(R/'private/extraction.json').write_text(json.dumps({'root':str(E),'externally_pinned_verifier_sha256':PIN}))
