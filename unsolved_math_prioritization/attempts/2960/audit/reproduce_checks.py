#!/usr/bin/env python3
"""Reproduce checker hardening without editing the audited packet.

Usage: python reproduce_checks.py PATH_TO_ORIGINAL_PUBLIC PATH_TO_WORK_DIRECTORY
The work directory must not already exist. Run as UID 1000, not root.
"""
import ast
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    require(os.getuid() == 1000 and os.geteuid() == 1000, 'Must genuinely run as UID/EUID 1000')
    original = Path(sys.argv[1]).resolve()
    work = Path(sys.argv[2]).resolve()
    work.mkdir()
    baseline = (original / 'exact_checks.py').read_text()
    patched = Path(__file__).with_name('exact_checks_hardened.py').read_text()
    expected = (original / 'EXACT_CHECKS.json').read_bytes()
    require(sum(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(baseline))) == 17, 'Wrong baseline assertion count')
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(patched))), 'Patched checker contains removable assertions')
    jobs = []
    modes = [('normal', []), ('O', ['-O']), ('OO', ['-OO'])]
    probes = []
    mutations = {
        'wrong_torus_generator': ('(0,0,1,-1)); powers=', '(0,0,1,0)); powers='),
        'remove_countermodel_twist': ('(z+w+e*m)%2', '(z+w)%2'),
        'wrong_wreath_conjugator': ('c=wi[(e,a,0)]', 'c=wi[(a,e,0)]'),
        'orientation_reversing_sign_coset': ('if sum(v)%2==0', 'if sum(v)%2==1'),
    }
    for kind, source in [('original', baseline), ('hardened', patched)]:
        cases = [('pristine', source)]
        for name, (before, after) in mutations.items():
            require(source.count(before) == 1, 'Mutation anchor must be unique: ' + name)
            cases.append((name, source.replace(before, after)))
        for case, text in cases:
            for mode, flags in modes:
                label = kind + '_' + case + '_' + mode
                folder = work / label
                folder.mkdir()
                script = folder / 'exact_checks.py'
                script.write_text(text)
                jobs.append((label, kind, case, mode, flags, script, False))
        for mode, flags in modes:
            label = kind + '_readonly_' + mode
            folder = work / label
            folder.mkdir()
            script = folder / 'exact_checks.py'
            script.write_text(source)
            (folder / 'EXACT_CHECKS.json').write_bytes(expected)
            for item in folder.iterdir():
                item.chmod(0o444)
            folder.chmod(0o555)
            denied = 0
            for target in [folder / 'probe', folder / 'EXACT_CHECKS.json']:
                try:
                    with target.open('a'):
                        pass
                except PermissionError:
                    denied += 1
            require(denied == 2, 'Read-only proof failed')
            probes.append({'case': label, 'directory_mode': oct(folder.stat().st_mode & 0o777),
                           'file_mode': oct(script.stat().st_mode & 0o777),
                           'creation_and_modification_denied': True})
            jobs.append((label, kind, 'readonly', mode, flags, script, True))

    def run(job):
        label, kind, case, mode, flags, script, readonly = job
        result = subprocess.run([sys.executable, '-B', *flags, str(script)], cwd=script.parent,
                                capture_output=True, timeout=180)
        try:
            parsed = json.loads(result.stdout)
        except (ValueError, UnicodeError):
            parsed = None
        last_error = result.stderr.decode(errors='replace').strip().splitlines()[-1:] or ['']
        record = {'case': label, 'kind': kind, 'mutation': case, 'optimization': mode,
                  'returncode': result.returncode, 'emitted_PASS': isinstance(parsed, dict) and parsed.get('status') == 'PASS',
                  'matches_frozen_JSON_bytes': result.stdout == expected,
                  'stdout_sha256': digest(result.stdout), 'stderr_final_line': last_error[0]}
        record['stderr_final_line'] = record['stderr_final_line'].replace(str(work), '<work>')
        if case == 'readonly' and kind == 'original':
            require(result.returncode != 0 and b'PermissionError' in result.stderr, label)
        elif case in ('pristine', 'readonly'):
            require(result.returncode == 0 and result.stdout == expected, label)
        elif kind == 'original' and mode != 'normal':
            require(result.returncode == 0 and record['emitted_PASS'], label)
        else:
            require(result.returncode != 0 and not record['emitted_PASS'] and b'AssertionError' in result.stderr, label)
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(run, jobs))
    explicit = work / 'explicit_output.json'
    out = subprocess.run([sys.executable, '-B', '-OO', str(work / 'hardened_readonly_OO' / 'exact_checks.py'),
                          '--output', str(explicit)], capture_output=True, timeout=180)
    require(out.returncode == 0 and out.stdout == expected and explicit.read_bytes() == expected, 'Explicit external output failed')
    require((original / 'exact_checks.py').read_text() == baseline, 'Original changed')
    result = {'status': 'PASS', 'uid': os.getuid(), 'euid': os.geteuid(), 'python': sys.version.split()[0],
              'original_checker_sha256': digest(baseline.encode()), 'hardened_checker_sha256': digest(patched.encode()),
              'original_removable_assertions': 17, 'hardened_removable_assertions': 0,
              'readonly_permission_probes': probes, 'runs': records,
              'hardened_explicit_output_from_readonly_OO': 'PASS', 'original_unchanged': True,
              'interpretation': 'Original optimization modes falsely pass all four corruptions; hardened checker rejects all twelve mutation/mode combinations.'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
