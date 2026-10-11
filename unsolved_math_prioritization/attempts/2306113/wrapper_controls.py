#!/usr/bin/env python3
"""Adversarial controls for the externally pinned publication wrapper.

Run under -I -B as UID/EUID 1000. Independently authenticate this script too.
All mutation fixtures are disposable copies; the publication stays read-only.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def modes(root, writable):
    for parent, dirs, files in os.walk(root, followlinks=False):
        Path(parent).chmod(0o755 if writable else 0o555)
        for name in files:
            path = Path(parent) / name
            if not path.is_symlink():
                path.chmod(0o644 if writable else 0o444)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--wrapper-sha256', required=True)
    args = parser.parse_args()
    need(os.getuid() == os.geteuid() == 1000, 'requires genuine UID/EUID 1000')
    need(sys.flags.isolated and sys.dont_write_bytecode, 'invoke with -I -B')
    root = args.root.resolve()
    wrapper = root / 'verify_publication.py'
    need(sha(wrapper.read_bytes()) == args.wrapper_sha256, 'external wrapper pin')
    need(sha((root / 'PUBLIC_MANIFEST.json').read_bytes()) == args.manifest_sha256, 'external manifest pin')
    initial = {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    manifest = json.loads((root / 'PUBLIC_MANIFEST.json').read_bytes())
    cases = [
        'wrong_pin', 'bad_pin_syntax', 'missing_manifest', 'missing_file',
        'extra_file', 'extra_directory', 'symlink_file', 'symlink_directory',
        'symlink_root', 'writable_root', 'writable_file', 'nonregular_file',
        'witness_mutation', 'checker_mutation', 'manifest_malformed',
        'duplicate_json_key', 'schema', 'file_count_bool', 'file_count_float',
        'file_count_wrong', 'files_object', 'bytes_bool', 'bytes_float',
        'bytes_negative', 'digest_type', 'digest_syntax', 'duplicate_path',
        'absolute_path', 'traversal_path', 'backslash_path', 'noncanonical_path',
        'extra_manifest_key', 'invalid_utf8', 'overflow_float',
        'oversized_integer', 'repinned_checker', 'repinned_original_checker',
    ]
    results, positive_modes = [], []
    with tempfile.TemporaryDirectory(prefix='sigma-wrapper-controls-') as td:
        temp = Path(td)
        (temp / 'fractions.py').write_text('raise RuntimeError("HOSTILE fractions")\n')
        (temp / 'sitecustomize.py').write_text('raise RuntimeError("HOSTILE sitecustomize")\n')
        env = dict(os.environ, PYTHONPATH=td, PYTHONHOME='/nonexistent/hostile-home',
                   PYTHONOPTIMIZE='99', PYTHONDONTWRITEBYTECODE='0')
        def execute(packet, pin, flags):
            return subprocess.run([sys.executable, '-I', '-B', *flags, str(wrapper),
                                   '--root', str(packet), '--manifest-sha256', pin,
                                   '--integrity-only'], cwd=temp, env=env,
                                  capture_output=True, timeout=20)
        for label, flags in [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]:
            proc = execute(root, args.manifest_sha256, flags)
            need(proc.returncode == 0 and not proc.stderr and
                 json.loads(proc.stdout) == {'status': 'PASS', 'stage': 'integrity-only', 'write_probes_rejected': 2},
                 'positive wrapper control: ' + label)
            positive_modes.append(label)
            for case in cases:
                fixture = temp / 'fixture'
                shutil.copytree(root, fixture, copy_function=shutil.copyfile)
                modes(fixture, True)
                mf = copy.deepcopy(manifest)
                pin, target, reseal = args.manifest_sha256, fixture, False
                mp = fixture / 'PUBLIC_MANIFEST.json'
                if case == 'wrong_pin': pin = '0' * 64
                elif case == 'bad_pin_syntax': pin = 'not-a-digest'
                elif case == 'missing_manifest': mp.unlink()
                elif case == 'missing_file': (fixture / 'candidate/COUNTEREXAMPLE.json').unlink()
                elif case == 'extra_file': (fixture / 'extra.txt').write_text('extra')
                elif case == 'extra_directory': (fixture / 'extra').mkdir()
                elif case == 'symlink_file':
                    p = fixture / 'candidate/COUNTEREXAMPLE.json'; p.unlink(); p.symlink_to(root / 'candidate/COUNTEREXAMPLE.json')
                elif case == 'symlink_directory':
                    shutil.rmtree(fixture / 'scope_audit'); (fixture / 'scope_audit').symlink_to(root / 'scope_audit', target_is_directory=True)
                elif case == 'symlink_root':
                    target = temp / 'root_link'; target.symlink_to(fixture, target_is_directory=True)
                elif case == 'writable_root': pass
                elif case == 'writable_file': pass
                elif case == 'nonregular_file':
                    p = fixture / 'candidate/COUNTEREXAMPLE.json'; p.unlink(); os.mkfifo(p)
                elif case == 'witness_mutation':
                    p = fixture / 'candidate/COUNTEREXAMPLE.json'; p.write_bytes(p.read_bytes() + b' ')
                elif case == 'checker_mutation':
                    p = fixture / 'candidate/verify_counterexample.py'; p.write_bytes(p.read_bytes() + b'\n')
                elif case == 'manifest_malformed': mp.write_bytes(b'{'); reseal = True
                elif case == 'duplicate_json_key': mp.write_text('{"schema":1,"schema":1}'); reseal = True
                elif case == 'invalid_utf8': mp.write_bytes(b'\xff'); reseal = True
                elif case == 'overflow_float': mp.write_text('{"file_count":1e1000000}'); reseal = True
                elif case == 'oversized_integer': mp.write_text('{"file_count":' + '9' * 5000 + '}'); reseal = True
                else:
                    if case == 'schema': mf['schema'] = 'wrong'
                    elif case == 'file_count_bool': mf['file_count'] = True
                    elif case == 'file_count_float': mf['file_count'] = float(mf['file_count'])
                    elif case == 'file_count_wrong': mf['file_count'] += 1
                    elif case == 'files_object': mf['files'] = {}
                    elif case == 'bytes_bool': mf['files'][0]['bytes'] = True
                    elif case == 'bytes_float': mf['files'][0]['bytes'] = float(mf['files'][0]['bytes'])
                    elif case == 'bytes_negative': mf['files'][0]['bytes'] = -1
                    elif case == 'digest_type': mf['files'][0]['sha256'] = 1
                    elif case == 'digest_syntax': mf['files'][0]['sha256'] = 'g' * 64
                    elif case == 'duplicate_path': mf['files'][1] = copy.deepcopy(mf['files'][0])
                    elif case == 'absolute_path': mf['files'][0]['path'] = '/etc/passwd'
                    elif case == 'traversal_path': mf['files'][0]['path'] = '../outside'
                    elif case == 'backslash_path': mf['files'][0]['path'] = 'candidate\\PROOF.md'
                    elif case == 'noncanonical_path': mf['files'][0]['path'] = './README.md'
                    elif case == 'extra_manifest_key': mf['ignored'] = 1
                    elif case in {'repinned_checker', 'repinned_original_checker'}:
                        n = ('candidate' if case == 'repinned_checker' else 'original_v2') + '/verify_counterexample.py'
                        p = fixture / n; p.write_bytes(p.read_bytes() + b'\n')
                        for entry in mf['files']:
                            if entry['path'] == n:
                                entry.update(bytes=p.stat().st_size, sha256=sha(p.read_bytes()))
                    else: raise ValueError('unimplemented control: ' + case)
                    mp.write_text(json.dumps(mf, indent=2) + '\n'); reseal = True
                if reseal: pin = sha(mp.read_bytes())
                modes(fixture, False)
                if case == 'writable_root': fixture.chmod(0o755)
                if case == 'writable_file': (fixture / 'candidate/COUNTEREXAMPLE.json').chmod(0o644)
                proc = execute(target, pin, flags)
                try: answer = json.loads(proc.stdout)
                except (ValueError, UnicodeError): answer = {}
                need(proc.returncode == 2 and not proc.stderr and answer.get('status') == 'REJECT',
                     'wrapper control failed: ' + label + '/' + case)
                results.append({'mode': label, 'case': case, 'status': 'REJECT', 'reason': answer['reason']})
                if case == 'symlink_root': target.unlink()
                modes(fixture, True)
                shutil.rmtree(fixture)
    current = {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    need(current == initial, 'original packet changed')
    print(json.dumps({'status': 'PASS', 'uid': os.getuid(), 'euid': os.geteuid(),
                      'positive_modes': positive_modes, 'negative_cases_per_mode': len(cases),
                      'negative_executions': len(results), 'post_run_hashes_unchanged': True,
                      'controls': results}, indent=2))


if __name__ == '__main__':
    main()
