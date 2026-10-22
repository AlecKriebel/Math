#!/usr/bin/env python3
"""Verify the frozen release allowlist, then run the exact mathematical checks."""
import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={v['path']:v for v in manifest['files']}
actual={p.name for p in root.iterdir()}
assert actual==set(expected)|{'MANIFEST.json'}, (actual,set(expected))
for name,item in expected.items():
    p=root/name
    assert p.is_file() and not p.is_symlink(),name
    data=p.read_bytes()
    assert len(data)==item['bytes'],name
    assert hashlib.sha256(data).hexdigest()==item['sha256'],name
result=subprocess.run([sys.executable,'-B',str(root/'verify_clasp_bridge.py')],check=True,capture_output=True,text=True)
assert json.loads(result.stdout)==json.loads((root/'EXACT_CHECKS.json').read_text())
print(json.dumps({'status':'PASS','manifest_files_verified':len(expected),'mathematical_replay_matches':True,'manifest_self_hashed':False},indent=2))
