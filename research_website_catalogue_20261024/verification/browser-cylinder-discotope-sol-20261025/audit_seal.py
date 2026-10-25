#!/usr/bin/env python3
"""Read-only check of this bounded browser handoff; no network, UI or writes."""
from pathlib import Path
import hashlib,json,subprocess,sys
E=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(p,r):return p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
def main():
    issues=[];seal=read(E/'FINAL_SEAL.json');manifest=read(E/'FINAL_MANIFEST.json')
    for name,r in seal['bindings'].items():
        if not bound(E/name,r):issues.append('seal:'+name)
    for r in manifest['files']:
        if not bound(E/r['path'],r):issues.append('owned:'+r['path'])
    actual={str(p.relative_to(E)) for p in E.rglob('*') if p.is_file() and 'private' not in p.relative_to(E).parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']}
    if actual!={r['path'] for r in manifest['files']}:issues.append('owned_file_set')
    baseline=read(E/'preservation-before.json')
    if '--owned-only' not in sys.argv:
        for r in baseline['files']:
            if not bound(Path(r['path']),r):issues.append('original:'+r['path'])
    tabs=read(E/'tab-preservation.json')
    for r in tabs['private_inventory_bindings']:
        if not bound(E/r['path'],r):issues.append('private_inventory:'+r['path'])
    before=read(E/'private/user-tabs-before.json');after=read(E/'private/user-tabs-after.json')
    if len(before)!=11 or len(after)!=11 or not all(any(x['id']==y['id'] and x.get('url')==y.get('url') for y in after) for x in before):issues.append('original_tabs')
    if '--owned-only' not in sys.argv:
        child=subprocess.run([sys.executable,str(E/'verify_browser_records.py')],text=True,capture_output=True)
        if child.returncode or read(E/'verification-result.json')['status']!='RECORDED_BROWSER_CUSTODY_PASS':issues.append('browser_records')
    print(json.dumps({'status':'PASS' if not issues else 'FAIL','owned_bindings':len(manifest['files']),'original_bindings':len(baseline['files']),'original_scope_checked':'snapshot only' if '--owned-only' in sys.argv else 'current exact inputs','original_tabs':len(before),'issues':issues},indent=2))
    return bool(issues)
if __name__=='__main__':raise SystemExit(main())
