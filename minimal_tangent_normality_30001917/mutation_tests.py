#!/usr/bin/env python3
"""Run source-free corruption controls on disposable copies, leaving the packet untouched."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def sha(data):
    return hashlib.sha256(data).hexdigest()

def change(path):
    path.write_bytes(path.read_bytes() + b'\ncorruption control\n')

def reseal(root, name):
    path = root / name
    obj = json.loads(path.read_bytes())
    for rel in obj['files']:
        b = (root / rel).read_bytes()
        obj['files'][rel] = {'bytes': len(b), 'sha256': sha(b)}
    path.write_text(json.dumps(obj, indent=2) + '\n')

def mutate(root, case):
    if case in ('baseline', 'wrong_external_pin', 'missing_external_pin'):
        return
    if case == 'changed_report':
        change(root / 'original/REPORT.md')
    elif case == 'missing_file':
        (root / 'independent_audit/SOURCE_CHECKS.json').unlink()
    elif case == 'extra_file':
        (root / 'extra.txt').write_text('extra')
    elif case == 'extra_directory':
        (root / 'extra').mkdir()
    elif case == 'symlink_file':
        p = root / 'original/REPORT.md'
        p.unlink()
        p.symlink_to('../README.md')
    elif case == 'symlink_directory':
        (root / 'linked').symlink_to('original', target_is_directory=True)
    elif case == 'changed_archive':
        change(root / 'archives/original_frozen_v1.zip')
    elif case == 'changed_audit':
        change(root / 'independent_audit/INDEPENDENT_AUDIT.md')
    elif case == 'coordinated_original_rewrite':
        change(root / 'original/REPORT.md')
        reseal(root / 'original', 'FROZEN_MANIFEST.json')
        reseal(root, 'PUBLIC_MANIFEST.json')
    elif case == 'coordinated_audit_rewrite':
        change(root / 'independent_audit/INDEPENDENT_AUDIT.md')
        reseal(root / 'independent_audit', 'AUDIT_MANIFEST.json')
        reseal(root, 'PUBLIC_MANIFEST.json')
    elif case == 'coordinated_wrapper_rewrite':
        change(root / 'README.md')
        reseal(root, 'PUBLIC_MANIFEST.json')
    elif case == 'nonlocal_manifest_entry':
        p = root / 'PUBLIC_MANIFEST.json'
        o = json.loads(p.read_bytes())
        o['files']['../outside'] = next(iter(o['files'].values()))
        p.write_text(json.dumps(o))
    elif case == 'duplicate_json_key':
        p = root / 'PUBLIC_MANIFEST.json'
        s = p.read_text()
        p.write_text(s.replace('{', '{"files": {},', 1))
    else:
        raise ValueError(case)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-manifest-sha256', required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    cases = ['baseline', 'wrong_external_pin', 'missing_external_pin', 'changed_report',
             'missing_file', 'extra_file', 'extra_directory', 'symlink_file', 'symlink_directory',
             'changed_archive', 'changed_audit', 'coordinated_original_rewrite',
             'coordinated_audit_rewrite', 'coordinated_wrapper_rewrite',
             'nonlocal_manifest_entry', 'duplicate_json_key']
    results = []
    for flags in ([], ['-O'], ['-OO']):
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='vmrt-control-') as temp:
                root = Path(temp) / 'relocated package with spaces'
                shutil.copytree(source, root)
                mutate(root, case)
                pin = '0' * 64 if case == 'wrong_external_pin' else args.expected_manifest_sha256
                cmd = [sys.executable, '-I', '-B', *flags, str(source / 'verify_publication.py'), '--root', str(root)]
                if case != 'missing_external_pin':
                    cmd += ['--expected-manifest-sha256', pin]
                cp = subprocess.run(cmd, cwd=temp, capture_output=True, text=True, timeout=30)
                expected = case == 'baseline'
                passed = (cp.returncode == 0) == expected
                if not passed:
                    raise RuntimeError((flags, case, cp.returncode, cp.stdout, cp.stderr))
                results.append({'mode': flags or ['normal'], 'case': case,
                                'expected_acceptance': expected, 'returncode': cp.returncode,
                                'behaved_as_expected': passed})
    print(json.dumps({'passed': True, 'controlled_runs': len(results), 'results': results}, indent=2))

if __name__ == '__main__':
    main()
