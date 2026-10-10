#!/usr/bin/env python3
"""External literal pins for the six-file author packet. No file writes."""
import hashlib
import json
from pathlib import Path
import sys

EXPECTED = {
    'MANIFEST.json': (735, '17801144470cef33242e5e0dde6fef457945642182644767adcefbdee502aad3'),
    'MATHEMATICAL_AUDIT.md': (13317, '27572974eae9d9a1a5f65c3762ebbacaf8f8ad7cf53caf6e22646c6ff12247bc'),
    'README.md': (1288, '7c0f2a2399bf94aa6edc694f140a02e0c27fc9f35bf951fdf1b78d66b38607a9'),
    'SOURCE_METADATA.json': (3556, '3d9d08b5520a30bc43e2c45fffbf30287bc32aa1194fb6550a1b0e0c87aa1faf'),
    'VERIFICATION.json': (1807, 'db909dc39919fcceed8b6bc1851bcd01c3989c2daa4207fa70d6961fdc6eb32a'),
    'check_examples.py': (9079, '3cb18eae17a6d27feeaa2d5405c049dc155c9debf958b5dd13c3eddd8bbdc0ef'),
}


def verify(directory):
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('packet must be a real directory')
    if {p.name for p in directory.iterdir()} != set(EXPECTED):
        raise ValueError('packet file set differs from external pins')
    result = {}
    for name, (size, digest) in EXPECTED.items():
        path = directory / name
        if path.is_symlink() or not path.is_file():
            raise ValueError('not an ordinary file: ' + name)
        data = path.read_bytes()
        actual = (len(data), hashlib.sha256(data).hexdigest())
        if actual != (size, digest):
            raise ValueError('external pin mismatch: ' + name)
        result[name] = {'bytes': size, 'sha256': digest}
    return result


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('usage: verify_frozen.py PACKET_DIRECTORY')
        print(json.dumps({'status': 'PASS', 'files': verify(sys.argv[1])}, sort_keys=True))
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'FAIL', 'reason': str(exc)}, sort_keys=True))
        sys.exit(1)
