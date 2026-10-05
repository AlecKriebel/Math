#!/usr/bin/env python3
"""Read-only offline delivery replay; checks survive Python optimization."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def snapshot():
    return {p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
            for p in ROOT.rglob('*') if p.is_file()}

def verify_inventory():
    manifest = json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_text())
    actual = snapshot()
    expected = {e['path'] for e in manifest['files']} | {'PUBLICATION_MANIFEST.json'}
    require(set(actual) == expected, 'delivery inventory differs')
    require(not any(p.is_symlink() for p in ROOT.rglob('*')), 'symlink in delivery')
    for entry in manifest['files']:
        p = PurePosixPath(entry['path'])
        require(not p.is_absolute() and '..' not in p.parts, 'unsafe manifest path')
        data = (ROOT/entry['path']).read_bytes()
        require(len(data) == entry['bytes'] and digest(data) == entry['sha256'],
                'delivery integrity: '+entry['path'])
    for folder, archive in [
        ('author_freeze', 'RANDOM_LABELING_PEAKS_9500009_AUTHOR_SAFE_FREEZE.zip'),
        ('independent_audit', 'RANDOM_LABELING_PEAKS_9500009_INDEPENDENT_AUDIT.zip')]:
        expanded = ROOT/folder
        original = json.loads((expanded/'MANIFEST.json').read_text())
        names = {e['path'] for e in original['files']} | {'MANIFEST.json'}
        require({p.relative_to(expanded).as_posix() for p in expanded.rglob('*') if p.is_file()} == names,
                'original inventory differs: '+folder)
        for entry in original['files']:
            data = (expanded/entry['path']).read_bytes()
            require(len(data) == entry['bytes'] and digest(data) == entry['sha256'],
                    'original manifest mismatch: '+entry['path'])
        with zipfile.ZipFile(ROOT/'archives'/archive) as z:
            require(len(z.namelist()) == len(names) and set(z.namelist()) == names,
                    'ZIP inventory differs: '+archive)
            for name in names:
                require(z.read(name) == (expanded/name).read_bytes(), 'ZIP member differs: '+name)
    return actual

def run(label, args, expected, env):
    process = subprocess.run(args, env=env, cwd=ROOT, capture_output=True, text=True)
    require(process.returncode == expected,
            label+' unexpected exit '+str(process.returncode)+'\n'+process.stderr)
    if expected == 0:
        require(json.loads(process.stdout)['status'] == 'PASS', label+' missing PASS')
    else:
        require('mismatch in pair_counts' in process.stderr, label+' wrong failure')
    return {'check': label, 'exit_code': process.returncode,
            'stdout_sha256': digest(process.stdout.encode()),
            'stderr_sha256': digest(process.stderr.encode())}

def main():
    before = verify_inventory()
    compiler = shutil.which('g++')
    require(compiler is not None, 'C++17 compiler g++ is required and was not found')
    version = subprocess.check_output([compiler, '--version'], text=True).splitlines()[0]
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    # No -O flag is passed to this new interpreter. Check that assert executes
    # before running the unchanged author verifier in that same process.
    guard = '''import runpy, sys
if sys.flags.optimize != 0 or not __debug__:
    raise RuntimeError("author assertions disabled")
try:
    assert False, "assertion sentinel"
except AssertionError:
    pass
else:
    raise RuntimeError("assertion sentinel removed")
target = sys.argv[1]
sys.argv = [target]
runpy.run_path(target, run_name="__main__")
'''
    checks = [run('author_normal_assertion_sentinel',
                  [sys.executable, '-c', guard, str(ROOT/'author_freeze/code/verify.py')], 0, env)]
    for flags in ([], ['-O']):
        command = [sys.executable, *flags, str(ROOT/'independent_audit/code/verify.py')]
        mode = 'optimized' if flags else 'normal'
        checks.append(run('audit_'+mode, command, 0, env))
        checks.append(run('audit_'+mode+'_negative_control', command+['--negative-control'], 1, env))
    require(snapshot() == before, 'replay changed delivery files')
    print(json.dumps({'status': 'PASS', 'full_target_resolved': False,
                      'disposition': 'UNSOLVED, 5/5', 'files_verified': len(before),
                      'compiler': version, 'author_assertions_enabled': True,
                      'replay_nonmutating': True, 'checks': checks}, indent=2))

if __name__ == '__main__':
    main()
