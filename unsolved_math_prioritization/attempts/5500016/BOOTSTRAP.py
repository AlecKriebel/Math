#!/usr/bin/env python3
"""Use an independently obtained, SHA-256-verified copy of this file outside ROOT.
The external copy binds all ROOT files, including acceptance and receipts, and QUEUE.
Usage: python -I -S -B TRUSTED_BOOTSTRAP.py ROOT QUEUE [--inventory-only]
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import types

MANIFEST_SHA256 = '14444b1de5cf2609db591e15063242e8f732ac11a1bf175e73d9d518142527eb'
VERIFIER_SHA256 = 'ad3fc5d253c3b90978192cce71ac7236d64a26107b021217a1b3042607d045af'
VERIFIER_BYTES = 16555
QUEUE_SHA256 = '9eef625462e2dff44c306c9eb515a5c2446179539bb6887eb2183a1549838393'
QUEUE_BYTES = 397815


def need(ok,message):
    if not ok:raise ValueError(message)


def read_regular(path):
    s=path.lstat()
    need(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'ordinary single-link file required')
    return path.read_bytes()


def main():
    need(len(sys.argv) in (3,4),'usage: TRUSTED_BOOTSTRAP.py ROOT QUEUE [--inventory-only]')
    inventory_only=len(sys.argv)==4
    need(not inventory_only or sys.argv[3]=='--inventory-only','unknown option')
    need(os.getuid()==1000 and os.geteuid()==1000,'actual UID=EUID=1000')
    root=Path(sys.argv[1]);queue=Path(sys.argv[2])
    need(stat.S_ISDIR(root.lstat().st_mode),'ordinary root directory')
    trusted=read_regular(Path(__file__))
    need(read_regular(root/'BOOTSTRAP.py')==trusted,'candidate bootstrap differs from external anchor')
    manifest=read_regular(root/'PUBLICATION_MANIFEST.json')
    need(hashlib.sha256(manifest).hexdigest()==MANIFEST_SHA256,'fixed manifest anchor')
    verifier=read_regular(root/'verify_publication.py')
    need(len(verifier)==VERIFIER_BYTES and hashlib.sha256(verifier).hexdigest()==VERIFIER_SHA256,'fixed verifier anchor')
    qb=read_regular(queue)
    need(len(qb)==QUEUE_BYTES and hashlib.sha256(qb).hexdigest()==QUEUE_SHA256,'fixed entire queue anchor')
    module=types.ModuleType('anchored_publication_verifier')
    exec(compile(verifier,'anchored_publication_verifier.py','exec'),module.__dict__)
    result=module.verify(root,queue,inventory_only)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except Exception as e:
        print('REJECT: '+type(e).__name__,file=sys.stderr)
        sys.exit(1)
