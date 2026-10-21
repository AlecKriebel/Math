"""Fail-closed integrity controls on disposable package copies."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def run(root, optimized):
    return subprocess.run([sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + ['verify_manifest.py'], cwd=root, capture_output=True, text=True, timeout=60)

def refresh_entry(root, name):
    path = root/'MANIFEST.json'
    obj = json.loads(path.read_text())
    data = (root/name).read_bytes()
    for entry in obj['files']:
        if entry['path'] == name:
            entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    obj['total_bytes_excluding_manifest'] = sum(e['bytes'] for e in obj['files'])
    path.write_text(json.dumps(obj))

def main():
    root = pathlib.Path(__file__).resolve().parent
    results = []
    for optimized in (False, True):
        baseline = run(root, optimized)
        require(baseline.returncode == 0 and not baseline.stderr, 'Baseline invalid: ' + baseline.stderr)
        for mutation in ('same_size_manuscript', 'missing_file', 'extra_file', 'symlink', 'frozen_version', 'provenance'):
            with tempfile.TemporaryDirectory(prefix='arakelov-controls-') as tmp:
                work = pathlib.Path(tmp)/'package'
                shutil.copytree(root, work)
                if mutation == 'same_size_manuscript':
                    target = work/'vertical_euler_classes.md'
                    data = target.read_bytes()
                    target.write_bytes(bytes([data[0]^1])+data[1:])
                    diagnostic = 'SHA-256 mismatch'
                elif mutation == 'missing_file':
                    (work/'CLAIM_LEDGER.json').unlink()
                    diagnostic = 'Inventory mismatch'
                elif mutation == 'extra_file':
                    (work/'EXTRA.txt').write_text('unexpected')
                    diagnostic = 'Inventory mismatch'
                elif mutation == 'symlink':
                    (work/'EXTRA_LINK').symlink_to('README.md')
                    diagnostic = 'Symlink forbidden'
                elif mutation == 'frozen_version':
                    target = work/'AUDIT_ACCEPTANCE.json'
                    obj = json.loads(target.read_text())
                    obj['frozen_authored_reports'][0]['sha256'] = '0'*64
                    target.write_text(json.dumps(obj))
                    refresh_entry(work, target.name)
                    diagnostic = 'Frozen version mismatch'
                else:
                    target = work/'PROVENANCE.json'
                    obj = json.loads(target.read_text())
                    obj['modified'][0]['packaged_sha256'] = '0'*64
                    target.write_text(json.dumps(obj))
                    refresh_entry(work, target.name)
                    diagnostic = 'Modified provenance mismatch'
                done = run(work, optimized)
                require(done.returncode != 0 and diagnostic in done.stderr, 'Corruption not rejected: '+mutation+' '+done.stderr)
                results.append({'mutation': mutation, 'optimized': optimized, 'rejected': True, 'diagnostic': diagnostic})
    print(json.dumps({'status': 'PASS', 'controls': results, 'scope': 'Selected accidental tampering; not adversarial authentication or theorem verification.'}, indent=2))

if __name__ == '__main__':
    main()
