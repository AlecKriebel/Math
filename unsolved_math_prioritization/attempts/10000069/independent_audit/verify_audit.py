#!/usr/bin/env python3
"""Read-only replay and exact binding verification for this independent audit."""
from pathlib import Path
import hashlib,json,subprocess,sys
here=Path(__file__).resolve().parent
original=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else here.parent.parent/'safe_output'
def digest(data):return hashlib.sha256(data).hexdigest()
def must(value,message):
    if not value:raise AssertionError(message)
binding=json.loads((here/'EXACT_BINDING.json').read_text())
expected={item['name']:item for item in binding['input_files']}
must({p.name for p in original.iterdir()}==set(expected),'Original file set changed')
for name,item in expected.items():
    data=(original/name).read_bytes()
    must(len(data)==item['byte_count'] and digest(data)==item['sha256'],'Original binding mismatch: '+name)
for line in (original/'MANIFEST.sha256').read_text().splitlines():
    sha,name=line.split('  ',1)
    must(digest((original/name).read_bytes())==sha,'Original manifest mismatch: '+name)
entries=[]
for line in (here/'MANIFEST.sha256').read_text().splitlines():
    sha,name=line.split('  ',1);entries.append(name)
    must(digest((here/name).read_bytes())==sha,'Audit manifest mismatch: '+name)
must({p.name for p in here.iterdir()}==set(entries)|{'MANIFEST.sha256'},'Unmanifested audit payload')
author=subprocess.check_output([sys.executable,str(original/'verify_exact_controls.py')])
must(author==(original/'EXACT_CONTROLS.json').read_bytes(),'Author replay differs')
independent=subprocess.check_output([sys.executable,str(here/'independent_controls.py')])
must(independent==(here/'INDEPENDENT_CONTROLS.json').read_bytes(),'Independent replay differs')
report={'status':'PASS','original_files_verified':len(expected),'audit_payload_files_verified':len(entries),'original_manifest_sha256':digest((original/'MANIFEST.sha256').read_bytes()),'audit_manifest_sha256':digest((here/'MANIFEST.sha256').read_bytes()),'author_replay_assertions':json.loads(author)['assertions'],'independent_replay_assertions':json.loads(independent)['assertions'],'author_stdout_sha256':digest(author),'independent_stdout_sha256':digest(independent)}
print(json.dumps(report,indent=2,sort_keys=True))
