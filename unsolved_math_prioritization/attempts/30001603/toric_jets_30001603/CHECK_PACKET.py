#!/usr/bin/env python3
"""Verify a frozen packet without modifying it; Python standard library only."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

NAMES = {
    'README.md','PROOF.md','SOURCE_GATE.md','APPROACH_LOG.md','STATUS.json',
    'SOURCES.json','VERIFY.py','RESULTS.json','CHECK_PACKET.py','MANIFEST.json',
}

def unique_object(pairs):
    result = {}
    for k,v in pairs:
        if k in result:
            raise ValueError('duplicate JSON key')
        result[k] = v
    return result

def integrity(root):
    actual = {p.name for p in root.iterdir()}
    if actual != NAMES:
        raise ValueError('wrong file allowlist')
    if any((root/n).is_symlink() or not (root/n).is_file() for n in NAMES):
        raise ValueError('nonregular or linked packet member')
    raw = (root/'MANIFEST.json').read_bytes()
    manifest = json.loads(raw,object_pairs_hook=unique_object)
    if manifest['schema'] != 'toric-jets-frozen-manifest-v1':
        raise ValueError('wrong manifest schema')
    files = manifest['files']
    if {x['path'] for x in files} != NAMES-{'MANIFEST.json'} or len(files) != len(NAMES)-1:
        raise ValueError('wrong manifest membership')
    for entry in files:
        data = (root/entry['path']).read_bytes()
        if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError('content mismatch: '+entry['path'])
    return hashlib.sha256(raw).hexdigest()

def main():
    root = Path(__file__).resolve().parent
    digest = integrity(root)
    run = subprocess.run([sys.executable,'-B',str(root/'VERIFY.py')],check=True,capture_output=True)
    if run.stderr or run.stdout != (root/'RESULTS.json').read_bytes():
        raise ValueError('exact replay mismatch')
    negative = []
    for mode in ['modify','remove','add']:
        with tempfile.TemporaryDirectory(prefix='toric-jets-integrity-') as tmp:
            dest = Path(tmp)/'packet'
            shutil.copytree(root,dest)
            if mode == 'modify':
                with (dest/'PROOF.md').open('ab') as f:
                    f.write(b'\nunauthorized mutation\n')
            elif mode == 'remove':
                (dest/'SOURCES.json').unlink()
            else:
                (dest/'unlisted-payload.txt').write_text('unlisted')
            try:
                integrity(dest)
            except ValueError:
                negative.append(mode)
            else:
                raise ValueError('negative integrity control accepted: '+mode)
    print(json.dumps({
        'result':'PASS', 'manifest_sha256':digest,
        'verified_hashed_files':len(NAMES)-1,
        'exact_replay':'RESULTS.json reproduced byte-for-byte',
        'rejected_integrity_mutations':negative,
        'authentication_limit':'Compare this manifest SHA-256 with the separately recorded audit/handoff value; internal hashes alone do not authenticate origin.',
    },indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
