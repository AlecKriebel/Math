#!/usr/bin/env python3
"""Strict self-excluding inventory for this audit packet; no foreign scratch."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parent
NAME='authored_manifest.json'


def inventory():
    out=[]
    for file in sorted(ROOT.rglob('*')):
        if not file.is_file():
            continue
        rel=file.relative_to(ROOT)
        if rel.as_posix()==NAME or any(part in ('tmp','__pycache__') for part in rel.parts):
            continue
        data=file.read_bytes()
        origin='audit_authored'
        if rel.parts[0]=='original_replay':
            origin='unchanged_original_git_input_copy'
        elif rel.parts[0]=='mutations':
            origin='audit_authored_corrupted_variant_or_exact_patch'
        elif rel.parts[0]=='results':
            origin='audit_generated_execution_receipt'
        out.append({'path':rel.as_posix(),'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'origin':origin})
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seal',action='store_true')
    args=parser.parse_args()
    manifest=ROOT/NAME
    if args.seal:
        manifest.write_text(json.dumps({'created_at':datetime.now(timezone.utc).isoformat(),
                          'schema':'strict_self_excluding_audit_inventory_v1',
                          'head':'35be7fe58a2832c4d7012cf69c973810fb4c42f8',
                          'base':'01358d66fc67d1c462bddf31c0d4ee5b120e6737',
                          'self_excluded':NAME,'excluded_directory_parts':['tmp','__pycache__'],
                          'foreign_source_downloads':'Only ignored tmp; no downloaded source bytes in deliverable inventory.',
                          'files':inventory()},indent=2)+'\n')
    sealed=json.loads(manifest.read_text())
    actual=inventory()
    if sealed['files']!=actual:
        raise AssertionError('Strict authored manifest inventory/hash/size/origin mismatch')
    if any(x['path']==NAME for x in sealed['files']):
        raise AssertionError('Manifest must exclude itself')
    print(json.dumps({'pass':True,'files':len(actual),'strict_no_missing_or_extra_files':True,
                      'self_excluding':True,'foreign_downloads_excluded':True}))


if __name__=='__main__':
    main()
