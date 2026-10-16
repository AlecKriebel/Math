#!/usr/bin/env python3
"""Read-only authentication of the exact assigned 29 original Git files."""
import hashlib, json, pathlib, subprocess, sys
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
AUDIT = HERE.parent.parent
REPO = pathlib.Path('/Users/alec/Documents/Math')
PIN = 'c09ef9df8b1f4642be0396ba6343344be8fa25b0'

def run(output):
    known = json.loads((AUDIT/'ROOT_PACKET_AUTHENTICATION.json').read_text())
    records = []
    for relative, expected in sorted(known['records'].items()):
        path = AUDIT/'original'/relative
        disk = path.read_bytes()
        git = subprocess.run(['git','cat-file','blob',f'{PIN}:{relative}'], cwd=REPO,
                             check=True, capture_output=True).stdout
        digest = hashlib.sha256(disk).hexdigest()
        records.append(dict(path=relative, bytes=len(disk), sha256=digest,
                            disk_regular=path.is_file() and not path.is_symlink(),
                            git_equal_disk=git==disk, expected_equal_disk=
                            expected==dict(bytes=len(disk),sha256=digest)))
    receipt = dict(utc=datetime.now(timezone.utc).isoformat(), original_head=PIN,
                   actual_current_head=subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,
                       check=True,capture_output=True,text=True).stdout.strip(),
                   exact_original_files=len(records), all_authenticated=all(
                       r['disk_regular'] and r['git_equal_disk'] and r['expected_equal_disk']
                       for r in records), records=records)
    (HERE/output).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='records'},sort_keys=True))
    if not receipt['all_authenticated']: raise SystemExit(1)

if __name__=='__main__': run(sys.argv[1] if len(sys.argv)>1 else 'AUTH_START.json')
