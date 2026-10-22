#!/usr/bin/env python3
"""Validate portable audit and frozen packet inventories. No external access."""
import hashlib
import json
from pathlib import Path
import sys
EXPECTED='767185ee51afce74a4227eb090aa4e896503ddbf186cc236e5deedadb4b51ab2'

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def hashentry(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def inventory(root,excluded):
    out={}
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symlink not permitted: '+str(p))
        if p.is_file():
            rel=p.relative_to(root).as_posix()
            if rel not in excluded: out[rel]=hashentry(p)
    return out

def main():
    audit=Path(__file__).resolve().parent
    packet=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else audit.parent/'packet'
    binding=json.loads((audit/'BINDING.json').read_text())
    require(binding['author_packet_manifest']['sha256']==EXPECTED,'binding targets wrong packet')
    require(hashentry(packet/'SHA256SUMS.json')==binding['author_packet_manifest'],'packet manifest mismatch')
    pm=json.loads((packet/'SHA256SUMS.json').read_text())
    require(inventory(packet,{'SHA256SUMS.json'})==pm['files'],'packet inventory mismatch')
    require(inventory(audit,{'BINDING.json'})==binding['audit_files'],'audit inventory mismatch')
    require(binding['verdict']=='pass_unsolved_partial_results','unexpected verdict')
    require(binding['full_target_verified'] is False,'full-target claim unexpectedly enabled')
    print(json.dumps({'passed':True,'packet_files_verified':len(pm['files']),
                      'audit_files_verified':len(binding['audit_files']),
                      'packet_manifest_sha256':EXPECTED,
                      'binding_manifest_sha256':hashentry(audit/'BINDING.json')['sha256']},indent=2))
if __name__=='__main__':main()
