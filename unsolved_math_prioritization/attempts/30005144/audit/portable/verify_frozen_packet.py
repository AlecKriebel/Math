#!/usr/bin/env python3
"""Read-only verification of the six frozen candidate files; standard library only."""
import hashlib
import json
from pathlib import Path
import sys

def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python verify_frozen_packet.py CANDIDATE_DIRECTORY')
    manifest = json.loads(Path(__file__).with_name('candidate_manifest.json').read_text())
    directory = Path(sys.argv[1])
    checked = []
    for name, expected in sorted(manifest['public_files'].items()):
        payload = (directory/name).read_bytes()
        actual = {'sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload)}
        if actual != expected:
            raise RuntimeError('Frozen candidate mismatch: '+name)
        checked.append(name)
    print(json.dumps({'status':'PASS','files_checked':checked},indent=2))

if __name__ == '__main__':
    main()
