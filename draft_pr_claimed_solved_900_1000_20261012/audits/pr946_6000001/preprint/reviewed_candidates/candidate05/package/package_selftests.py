#!/usr/bin/env python3
"""Transport rejection controls; externally authenticate before running.
Run with nonoptimized Python -I -B. Writes only temporary fixtures and stdout.
"""
import sys
if sys.flags.optimize != 0 or not __debug__ or not sys.flags.isolated or not sys.dont_write_bytecode:
    raise SystemExit('REJECTED: selftests require python -I -B, optimization 0')
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import stat
import tempfile
import zipfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def trusted_bytes(path, expected):
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NONBLOCK)
    try:
        for part in path.absolute().parts[1:-1]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            os.close(fd)
            fd = nxt
        child = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
    finally:
        os.close(fd)
    try:
        info = os.fstat(child)
        require(stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644 and
                0 <= info.st_size <= 8 * 1024 * 1024, 'Untrusted source type/mode/size')
        raw = b''
        while len(raw) <= info.st_size:
            block = os.read(child, min(65536, info.st_size + 1 - len(raw)))
            if not block:
                break
            raw += block
        require(len(raw) == info.st_size and hashlib.sha256(raw).hexdigest() == expected,
                'External source pin mismatch')
        return raw
    finally:
        os.close(child)


BOOT = "import base64,sys; raw=base64.b64decode(sys.argv[1],validate=True); p=sys.argv[2];sys.argv=sys.argv[2:];exec(compile(raw,p,'exec'),dict(__name__='__main__',__file__=p))"


def command(raw, path, args, no_site=False):
    return [sys.executable, '-I', '-B'] + (['-S'] if no_site else []) + [
        '-c', BOOT, base64.b64encode(raw).decode(), str(path), *map(str, args)]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package', type=Path, required=True)
    p.add_argument('--manifest-sha256', required=True)
    a = p.parse_args()
    script = a.package / 'verify_package.py'
    manifest = json.loads(trusted_bytes(a.package / 'PACKAGE_MANIFEST.json', a.manifest_sha256))
    script_raw = trusted_bytes(script, manifest['files']['verify_package.py']['sha256'])
    names = sorted(manifest['files']) + ['PACKAGE_MANIFEST.json']
    records = []
    def check(label, root=None, archive=None):
        args = ['--manifest-sha256', a.manifest_sha256, '--integrity-only']
        if archive:
            args += ['--archive', str(archive), '--archive-sha256', hashlib.sha256(archive.read_bytes()).hexdigest()]
        else:
            args += ['--package', str(root)]
        cmd = command(script_raw, script, args)
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        require(r.returncode != 0 and 'REJECTED:' in r.stderr, 'Malformed fixture accepted: ' + label)
        records.append(dict(case=label, rejected=True))
    with tempfile.TemporaryDirectory(prefix='pr946-package-controls-',
                                     dir=Path(tempfile.gettempdir()).resolve(strict=True)) as td:
        top = Path(td)
        clean = subprocess.run(command(script_raw, script, ['--package', a.package,
                   '--manifest-sha256', a.manifest_sha256, '--integrity-only']),
                   capture_output=True, text=True, timeout=10)
        require(clean.returncode == 0 and json.loads(clean.stdout)['status'] == 'PASS', 'Initial package integrity failed')
        copy = top / 'copy'
        shutil.copytree(a.package, copy)
        # A controlled extra module must not execute before inventory authentication.
        marker = top / 'unsafe-shadow-executed'
        shadow = copy / 'argparse.py'
        shadow.write_text('open(' + repr(str(marker)) + ', "w").write("executed")\n')
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith('PYTHON')}
        unsafe = subprocess.run([sys.executable, '-B', str(copy / 'verify_package.py'),
                 '--package', str(copy), '--manifest-sha256', a.manifest_sha256],
                 capture_output=True, text=True, timeout=5, env=env)
        require(unsafe.returncode != 0 and 'safe-path startup required' in unsafe.stderr and
                not marker.exists(), 'Unsafe stdlib-shadow bootstrap was not rejected before import')
        records.append(dict(case='unsafe_stdlib_shadow_bootstrap', rejected=True, injected_module_executed=False))
        shadow.unlink()
        victim = copy / 'original/unsolved_math_prioritization/attempts/6000001/public/PROOF.md'
        original = victim.read_bytes()
        victim.write_bytes(original + b'\n')
        check('changed_original_proof', root=copy)
        victim.write_bytes(original)
        extra = copy / 'unexpected.txt'
        extra.write_text('not in the closed inventory\n')
        check('extra_file', root=copy)
        extra.unlink()
        victim.unlink()
        victim.symlink_to(a.package / 'original/unsolved_math_prioritization/attempts/6000001/public/PROOF.md')
        check('symlink_payload', root=copy)
        victim.unlink()
        os.mkfifo(victim, 0o644)
        check('FIFO_payload_prompt_rejection', root=copy)
        victim.unlink()
        victim.write_bytes(original)
        victim.chmod(0o644)
        def archive(path, bad):
            with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
                for name in names:
                    info = zipfile.ZipInfo(name)
                    info.create_system = 3
                    info.external_attr = 0o100644 << 16
                    z.writestr(info, (a.package / name).read_bytes())
                info = zipfile.ZipInfo('../escape.txt' if bad == 'traversal' else names[0] if bad == 'duplicate'
                                       else 'bad\nname.txt' if bad == 'control_character' else 'extra.txt')
                info.create_system = 3
                info.external_attr = (0o120777 if bad == 'symlink' else 0o100644) << 16
                z.writestr(info, b'rejected fixture')
        for label in ['traversal', 'duplicate', 'symlink', 'control_character']:
            path = top / (label + '.zip')
            archive(path, label)
            check('archive_' + label, archive=path)
        # The trusted v2 launcher has an intentional false-assertion transport control.
        # Its worker must fail with assertions enabled, rather than return a false PASS.
        tool = a.package / 'tools'
        pins = {
            'portable_gate.py': '65f2d6b7f96f9994d073d7bf3741af5dcfc92ac6fe9f9aaadf224d25016e5b57',
            'portable_worker.py': 'fe5a88a4e5c5a8a6e95ad4b729a0427366f33eabbb512017a06ce362e2739fa2',
            'compare_results.py': '85c7a936c3333a6dc283bb46525589f21ab11584f0cde88c745286fb364bbd4b'}
        args = [str(a.package / 'original/unsolved_math_prioritization/attempts/6000001'),
               '--gate', str(tool / 'portable_gate.py'), '--gate-sha256', pins['portable_gate.py'],
               '--worker', str(tool / 'portable_worker.py'), '--worker-sha256', pins['portable_worker.py'],
               '--comparator', str(tool / 'compare_results.py'), '--comparator-sha256', pins['compare_results.py'],
               '--scratch', str(top), '--test-false-assert']
        launcher = tool / 'launch_portable_gate.py'
        launcher_raw = trusted_bytes(launcher, '0199b8c7c481527121813c6d3c57a5acd2e598e8a5223acba69eb2161235d3b8')
        cmd = command(launcher_raw, launcher, args, no_site=True)
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        require(r.returncode != 0 and 'Intentional worker assertion control' in r.stderr,
                'False assertion failed to reject in worker')
        records.append(dict(case='v2_false_assertion', rejected=True, worker_optimization=0))
    print(json.dumps(dict(status='PASS', pr=946, problem_id='6000001', controls=records,
                         limit='Selected transport controls; full historical typed/numerical tests remain separate sealed evidence.'), indent=2))


if __name__ == '__main__':
    main()
