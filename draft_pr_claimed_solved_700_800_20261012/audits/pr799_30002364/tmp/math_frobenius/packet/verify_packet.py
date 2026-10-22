"""Authenticate this file externally before invocation; pass independent SHA256 pins.

python3 -I -S -B verify_packet.py ROOT MANIFEST_SHA256 CHECKER_SHA256
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def need(p, message):
    if not p:
        raise RuntimeError(message)


def plain_path(p):
    need(p.is_absolute(), 'absolute path required')
    for q in [p] + list(p.parents):
        need(not q.is_symlink(), 'symlink path rejected')


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,
     'use -I -S -B')
need(len(sys.argv) == 4, 'ROOT MANIFEST_SHA256 CHECKER_SHA256 required')
root = Path(sys.argv[1])
plain_path(root)
need(root.is_dir(), 'packet root missing')
for pin in sys.argv[2:]:
    need(re.fullmatch('[0-9a-f]{64}', pin) is not None, 'invalid pin')
self_file = Path(__file__).absolute()
plain_path(self_file)
need(self_file == root / 'verify_packet.py', 'checker must be in packet root')
need(digest(self_file) == sys.argv[3], 'checker pin mismatch')
manifest = root / 'MANIFEST.json'
plain_path(manifest)
need(digest(manifest) == sys.argv[2], 'manifest pin mismatch')
data = json.loads(manifest.read_text())
need(data['schema'] == 'frobenius-audit-packet-v1', 'manifest schema')
records = data['files']
need(isinstance(records, dict), 'manifest records')
need(all(re.fullmatch('[A-Za-z0-9_.-]+', n) is not None for n in records), 'flat safe names')
need(set(records).isdisjoint({'MANIFEST.json', 'verify_packet.py'}), 'external pins are separate')
allowed = set(records) | {'MANIFEST.json', 'verify_packet.py'}
need({p.name for p in root.iterdir()} == allowed, 'closed inventory mismatch')
for name, record in records.items():
    p = root / name
    plain_path(p)
    need(p.is_file(), 'regular payload files required')
    need(p.stat().st_size == record['bytes'] and digest(p) == record['sha256'],
         'payload mismatch: '+name)
need(not any(p.is_dir() for p in root.iterdir()), 'no directories/caches allowed')
flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
r = subprocess.run([sys.executable]+flags+[str(root/'exact_checker.py')],
                   capture_output=True, text=True, check=False)
need(r.returncode == 0, 'arithmetic failed: '+r.stderr)
need(json.loads(r.stdout) == json.loads((root/'EXPECTED.json').read_text()),
     'arithmetic output differs from expected')
print(json.dumps({'authenticated_inventory': len(allowed), 'arithmetic': 'PASS',
                  'optimized': bool(sys.flags.optimize)}, sort_keys=True))
