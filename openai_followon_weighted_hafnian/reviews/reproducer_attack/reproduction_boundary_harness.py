"""Review a repaired v3 archive, using the exact README command in its extraction.

This intentionally refuses v2 and any reproducer that still invokes copytree.
Collision runs intercept attempted writes to original extracted payload files:
an interception is a FAILED test, never evidence of native collision rejection.
All created files stay beside this harness. The source ZIP is never modified.
"""
import argparse
import ast
import hashlib
import json
import re
import shlex
import stat
import subprocess
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
V2_SHA256 = "cd63ad9d2a1ee591f49721d5b97150ee2bda9a116e8250a93ebc82bd0bafdd2c"
README_COMMAND = "python3 reproduce.py --output reproduction-receipt.json"
GUARD_MARKER = "HARNESS_PROTECTED_PAYLOAD_WRITE"

# Path.write_text uses io.open. Also guard common lower-level and atomic writes.
# This is an accidental-write guard for the authored reproducer, not a sandbox
# against hostile code. Child finite-check processes write only their clean copy.
COLLISION_LAUNCHER = r'''
import builtins, io, json, os, pathlib, runpy, sys
protected = [pathlib.Path(p) for p in json.loads(sys.argv[1])]
def protect(p):
    if isinstance(p, int): return
    p = pathlib.Path(os.fsdecode(p))
    for q in protected:
        if p.resolve() == q.resolve() or (p.exists() and p.samefile(q)):
            print("HARNESS_PROTECTED_PAYLOAD_WRITE: " + str(p), file=sys.stderr)
            raise PermissionError("Harness prevented original payload mutation")
def wrap_open(original):
    def checked(p, mode='r', *a, **kw):
        if any(c in mode for c in 'wax+'): protect(p)
        return original(p, mode, *a, **kw)
    return checked
builtins.open = wrap_open(builtins.open)
io.open = wrap_open(io.open)
original_os_open = os.open
def checked_os_open(p, flags, *a, **kw):
    if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND): protect(p)
    return original_os_open(p, flags, *a, **kw)
os.open = checked_os_open
for name in ('replace', 'rename'):
    original = getattr(os, name)
    def checked(src, dst, *a, _original=original, **kw):
        protect(src); protect(dst)
        return _original(src, dst, *a, **kw)
    setattr(os, name, checked)
for name in ('unlink', 'remove'):
    original = getattr(os, name)
    def checked(p, *a, _original=original, **kw):
        protect(p)
        return _original(p, *a, **kw)
    setattr(os, name, checked)
script, output = sys.argv[2:4]
sys.argv = [script, '--output', output]
runpy.run_path(script, run_name='__main__')
'''

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def valid_name(name):
    p = PurePosixPath(name)
    return (isinstance(name, str) and bool(name) and not p.is_absolute()
            and '\\' not in name and str(p) == name
            and all(part not in ('', '.', '..') for part in p.parts))

def snapshot(root, names):
    return {name: digest(root / name) for name in names}

def checked_run(command, root):
    return subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=120)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    archive = args.archive.resolve()
    archive_digest = digest(archive)
    if archive_digest == V2_SHA256 or 'candidate_v2' in archive.parts:
        raise RuntimeError('Refusing to execute the preserved faulty v2 archive')
    run_root = HERE / ('v3-run-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    root = run_root / 'extracted'
    root.mkdir(parents=True)
    with ZipFile(archive) as zip_file:
        infos = zip_file.infolist()
        names = [info.filename for info in infos if not info.is_dir()]
        if len(names) != len(set(names)) or not all(valid_name(name) for name in names):
            raise RuntimeError('Archive has duplicate or unsafe member paths')
        for info in infos:
            if stat.S_ISLNK(info.external_attr >> 16):
                raise RuntimeError('Archive contains symlink: ' + info.filename)
        zip_file.extractall(root)
    source = (root / 'reproduce.py').read_text()
    for node in ast.walk(ast.parse(source)):
        if (isinstance(node, ast.Call) and
            ((isinstance(node.func, ast.Attribute) and node.func.attr == 'copytree') or
             (isinstance(node.func, ast.Name) and node.func.id == 'copytree'))):
            raise RuntimeError('Refusing a reproducer that still calls copytree')
    manifest = json.loads((root / 'PAYLOAD_SHA256.json').read_text())
    if not isinstance(manifest, dict) or not all(valid_name(name) for name in manifest):
        raise RuntimeError('Unsafe payload manifest')
    if not all(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) for value in manifest.values()):
        raise RuntimeError('Malformed payload digest')
    protected_names = sorted(set(manifest) | {'PAYLOAD_SHA256.json'})
    baseline = snapshot(root, protected_names)
    if any(baseline[name] != expected for name, expected in manifest.items()):
        raise RuntimeError('Archive payload does not match its manifest')
    readme = (root / 'README.md').read_text()
    if README_COMMAND not in re.findall(r'^python3 reproduce\.py --output [^\n]+$', readme, re.MULTILINE):
        raise RuntimeError('Exact expected README command not found')
    report = run_root / 'boundary-harness-report.json'
    evidence = {'status': 'running', 'archive': str(archive), 'archive_sha256': archive_digest,
                'extracted': str(root), 'readme_command': README_COMMAND,
                'protected_original_hashes': baseline, 'cases': []}
    def record(case):
        case['original_payload_unchanged'] = snapshot(root, protected_names) == baseline
        evidence['cases'].append(case)
        report.write_text(json.dumps(evidence, indent=2) + '\n')
    # This is exactly the README invocation, including its relative receipt path.
    for attempt in (1, 2):
        run = checked_run(shlex.split(README_COMMAND), root)
        record({'case': 'exact README command, run ' + str(attempt),
                'returncode': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr})
        if run.returncode or snapshot(root, protected_names) != baseline:
            raise RuntimeError('README invocation failed or changed original payload: ' + run.stderr)
        receipt = json.loads((root / 'reproduction-receipt.json').read_text())
        if receipt.get('status') != 'passed' or receipt.get('payload_hashes_verified') != len(manifest):
            raise RuntimeError('Incomplete success receipt')
        expected_checks = {'test_gadget.py', 'test_sampling.py', 'upstream_cell_checks.py'}
        if {item['check'] for item in receipt['runs']} != expected_checks:
            raise RuntimeError('Receipt does not cover all three finite checks')
        for item in receipt['runs']:
            if item['returncode'] or hashlib.sha256(item['stdout'].encode()).hexdigest() != item['stdout_sha256']:
                raise RuntimeError('Incorrect run status or stdout digest in receipt')
    # Unlisted files should not affect reproduction or become recursively copied.
    (root / 'unlisted-extra.txt').write_text('Unlisted reproduction-boundary canary\n')
    (root / 'nested-receipts').mkdir()
    for output in ('nested-receipts/receipt.json', str(run_root / 'absolute-receipt.json')):
        run = checked_run(['python3', 'reproduce.py', '--output', output], root)
        record({'case': 'valid output ' + output, 'returncode': run.returncode,
                'stdout': run.stdout, 'stderr': run.stderr})
        if run.returncode or snapshot(root, protected_names) != baseline:
            raise RuntimeError('Valid output failed or changed original payload: ' + run.stderr)
    aliases = [('payload-symlink-alias', 'README.md', 'symlink'),
               ('manifest-symlink-alias', 'PAYLOAD_SHA256.json', 'symlink'),
               ('payload-hardlink-alias', 'README.md', 'hardlink'),
               ('manifest-hardlink-alias', 'PAYLOAD_SHA256.json', 'hardlink')]
    for alias, target, kind in aliases:
        if kind == 'symlink': (root / alias).symlink_to(target)
        else: (root / alias).hardlink_to(root / target)
    collision_outputs = protected_names + [alias for alias, _, _ in aliases]
    collision_outputs += [str(root / 'README.md'), 'code/../README.md']
    protected_paths = json.dumps([str(root / name) for name in protected_names])
    for output in collision_outputs:
        run = checked_run(['python3', '-I', '-B', '-c', COLLISION_LAUNCHER,
                           protected_paths, str(root / 'reproduce.py'), output], root)
        record({'case': 'reject collision ' + output, 'returncode': run.returncode,
                'stdout': run.stdout, 'stderr': run.stderr})
        if snapshot(root, protected_names) != baseline:
            raise RuntimeError('Collision attempt changed original payload: ' + output)
        if not run.returncode or GUARD_MARKER in run.stderr:
            raise RuntimeError('Reproducer lacks native collision rejection: ' + output + '\n' + run.stderr)
    evidence.update(status='passed', original_payload_unchanged=True,
                    payload_members=len(manifest), collision_cases=len(collision_outputs),
                    receipt_sha256=digest(root / 'reproduction-receipt.json'),
                    completed_at=datetime.now(timezone.utc).isoformat())
    if digest(archive) != archive_digest:
        raise RuntimeError('Source archive changed during the boundary audit')
    evidence['archive_unchanged'] = True
    report.write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'report': str(report),
                      'collision_cases': len(collision_outputs), 'original_payload_unchanged': True}))

if __name__ == '__main__':
    main()
