#!/usr/bin/env python3
"""Verify this curated map only after authenticating an externally supplied map digest.
This is an integrity check, never a mathematical proof or publication approval.
"""
import argparse
import hashlib
import importlib.util
import json
import pathlib
import re
import sys

ALLOWLIST = (
    'AUDIT.md', 'CONTROL_RESULTS.json', 'INITIAL_RECONSTRUCTION.md',
    'ORIGINAL_END.json', 'ORIGINAL_START.json', 'RESEARCH_LOG.md',
    'RESULT.json', 'VERIFY.py', 'VERIFY_ORIGINAL.py', 'geometry_controls.py',
)

def digest(data): return hashlib.sha256(data).hexdigest()

def verify(external_digest):
    if not re.fullmatch('[0-9a-f]{64}', external_digest):
        raise ValueError('external manifest SHA256 must be 64 lowercase hex characters')
    root=pathlib.Path(__file__).resolve().parent
    manifest_path=root/'MANIFEST.json'
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError('manifest is not a regular non-symlink file')
    raw=manifest_path.read_bytes()
    if digest(raw)!=external_digest:
        raise ValueError('manifest does not match externally supplied digest')
    manifest=json.loads(raw)
    if manifest.get('schema')!='geometry-family-public-map-v1': raise ValueError('manifest schema')
    if manifest.get('self_excluded')!='MANIFEST.json': raise ValueError('self exclusion')
    if manifest.get('allowlist')!=list(ALLOWLIST): raise ValueError('curated allowlist changed')
    if set(manifest.get('files',{}))!=set(ALLOWLIST): raise ValueError('file map differs from allowlist')
    for name in ALLOWLIST:
        path=root/name
        if path.is_symlink() or not path.is_file(): raise ValueError('nonregular mapped file: '+name)
        raw=path.read_bytes()
        actual={'bytes':len(raw),'sha256':digest(raw)}
        if actual!=manifest['files'][name]: raise ValueError('mapped bytes differ: '+name)
    # Execute this known exact helper only after all mapped executable bytes are authenticated.
    spec=importlib.util.spec_from_file_location('geometry_verify_original',root/'VERIFY_ORIGINAL.py')
    helper=importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
    current=helper.authenticate()
    start=json.loads((root/'ORIGINAL_START.json').read_text())
    end=json.loads((root/'ORIGINAL_END.json').read_text())
    for key in ['original_head','proof_sha256','outer_manifest_sha256','original_count',
                'all_originals_match_actual_Git','shared_head','shared_branch','shared_index_sha256','selected_records']:
        if start[key]!=end[key] or end[key]!=current[key]:
            raise ValueError('original/head/index authentication mismatch: '+key)
    return {'authenticated_manifest_sha256':external_digest,'mapped_file_count':len(ALLOWLIST),
            'all_originals_match_actual_Git':True,'shared_head_index_match_start_and_end':True,
            'scope':'Integrity only; mathematical conclusions require reading AUDIT.md; no publication approval.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256',required=True,help='Digest supplied independently of this folder')
    args=parser.parse_args()
    try:
        print(json.dumps(verify(args.manifest_sha256),indent=2,sort_keys=True))
    except Exception as exc:
        print('INTEGRITY FAILURE: '+str(exc),file=sys.stderr)
        sys.exit(1)
