"""Externally pin this file and MANIFEST.json before execution.

Usage: python -I -S -B verify_bundle.py ROOT MANIFEST_SHA256 LAUNCHER_SHA256
Checks a closed bundle, then runs its authenticated finite checker.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('Require -I -S -B')
from pathlib import Path
import hashlib
import json
import subprocess


def need(ok, why):
    if not ok:
        raise SystemExit('REJECT: '+why)


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def no_link(p):
    p = p.absolute()
    need(all(not q.is_symlink() for q in [p, *p.parents]), 'symlink path')


need(len(sys.argv) == 4, 'arguments')
root = Path(sys.argv[1]).absolute()
manifest_pin, launcher_pin = sys.argv[2:]
for pin in (manifest_pin, launcher_pin):
    need(len(pin) == 64 and all(c in '0123456789abcdef' for c in pin), 'pin format')
me = Path(__file__).absolute()
no_link(me)
no_link(root)
need(me.parent == root, 'launcher location')
need(digest(me) == launcher_pin, 'launcher bytes')
manifest = root/'MANIFEST.json'
no_link(manifest)
need(manifest.is_file() and digest(manifest) == manifest_pin, 'manifest bytes')
data = json.loads(manifest.read_text())
need(set(data) == {'schema', 'files'}, 'manifest schema')
need(data['schema'] == 'cm-hodge-audit-closed-v1', 'manifest version')
expected = data['files']
need(isinstance(expected, dict) and 'verify_bundle.py' in expected and 'finite_check.py' in expected,
     'required members')
actual = set()
for p in root.iterdir():
    need(not p.is_symlink() and p.is_file(), 'nonregular member')
    actual.add(p.name)
need(actual == set(expected)|{'MANIFEST.json'}, 'closed inventory')
for name, record in expected.items():
    need(name == Path(name).name and name not in {'.','..','MANIFEST.json'}, 'member name')
    p = root/name
    need(set(record) == {'bytes','sha256'}, 'record schema')
    need(p.stat().st_size == record['bytes'] and digest(p) == record['sha256'], 'member bytes '+name)
need(expected['verify_bundle.py']['sha256'] == launcher_pin, 'launcher consistency')
args = [sys.executable, '-I', '-S', '-B']
if sys.flags.optimize:
    args.append('-O')
args.append(str(root/'finite_check.py'))
result = subprocess.run(args, cwd=root, text=True, capture_output=True)
need(result.returncode == 0, 'finite checker failed: '+result.stderr)
answer = json.loads(result.stdout)
need(answer['result'] == 'PASS', 'finite checker result')
print(json.dumps({'integrity':'PASS','finite':answer}, sort_keys=True))
