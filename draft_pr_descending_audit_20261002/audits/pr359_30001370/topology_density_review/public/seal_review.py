#!/usr/bin/env python3
"""One-shot package closure; run only after parent authorizes final sealing.

This creates only PUBLIC_MANIFEST.json, PRIVATE_MANIFEST.json and
FINAL_CLOSURE.json. Existing closure causes an error. It does not run Git,
use network, install anything, or modify candidate/source/report bytes.
After creation it invokes the read-only verifier without saving new files.
"""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent


def main():
    if sys.argv[1:] != ['--parent-approved']:
        raise SystemExit('Parent approval required before one-shot sealing.')
    destinations=[ROOT/'public/PUBLIC_MANIFEST.json',ROOT/'private/PRIVATE_MANIFEST.json',ROOT/'FINAL_CLOSURE.json']
    if any(p.exists() for p in destinations):
        raise SystemExit('Closure already exists; no subsequent writes are permitted.')
    data={}
    for scope in ['public','private']:
        entries=[]
        for p in sorted((ROOT/scope).rglob('*')):
            if p.is_symlink():
                raise SystemExit('Symlinks are not permitted: '+str(p))
            if p.is_file():
                b=p.read_bytes()
                entries.append({'path':str(p.relative_to(ROOT)),'bytes':len(b),
                                'sha256':hashlib.sha256(b).hexdigest(),
                                'mode':'100755' if p.stat().st_mode&0o111 else '100644'})
        obj={'scope':scope,'closure_policy':'Exact recursive regular-file set; this manifest is the sole self-exclusion and FINAL_CLOSURE.json at root binds both manifest bytes. No post-seal writes.',
             'files':entries}
        data[scope]=(json.dumps(obj,indent=2)+'\n').encode()
    destinations[0].write_bytes(data['public'])
    destinations[1].write_bytes(data['private'])
    closure={'sealed_utc':datetime.now(timezone.utc).isoformat(),'parent_approved':True,
             'public_manifest_sha256':hashlib.sha256(data['public']).hexdigest(),
             'private_manifest_sha256':hashlib.sha256(data['private']).hexdigest(),
             'root_set':['public','private','FINAL_CLOSURE.json'],
             'policy':'No subsequent writes anywhere in this review folder. Final closure is the only root seal self-exclusion.'}
    destinations[2].write_text(json.dumps(closure,indent=2)+'\n')
    result=subprocess.run([sys.executable,str(ROOT/'public/verify_review.py'),'--with-private'],capture_output=True)
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    print(json.dumps(closure,indent=2))
    raise SystemExit(result.returncode)


if __name__=='__main__':
    main()
