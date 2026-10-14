#!/usr/bin/env python3
"""Source-free integrity and finite replay only. Authenticate this file before execution.
An independently trusted outer-manifest SHA-256 is also required.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile

FROZEN = {
    'original/MANIFEST.json': '7cec8ef8716ab0e930d6c03f2cd4d8559214d9329ccde8ef258cd9a8d3c7ae55',
    'corrected/MANIFEST.json': '178ee6e7b46973dae0286b07184f1ca2c3456f8270c812302869c7d31ebba3a9',
    'independent_audit/MANIFEST.json': '4f5950d90f5b2db1d69ed83760bec88dbeeb28005340e325c688567277f470de',
}
TOP_FILES = {'README.md', 'PUBLICATION_ACCEPTANCE.md', 'RESEARCH_LOG.md',
             'VERIFY_PUBLICATION.py', 'TEST_MUTATIONS.py', 'MUTATION_RESULTS.json',
             'PUBLICATION_MANIFEST.json', 'HARDENING_REPLAY.patch'}
HEX = re.compile(r'[0-9a-f]{64}')


def need(value, message):
    if not value:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(raw):
    def bad_constant(value):
        raise RuntimeError('Nonfinite JSON constant: ' + value)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad_constant)


def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'Nonregular file: ' + str(path))
    return path.read_bytes()


def validate_members(root, manifest_name, entries, flat=False):
    need(type(entries) is list and bool(entries), 'Invalid inventory')
    names = {manifest_name}
    directories = set()
    for item in entries:
        need(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'}, 'Invalid member schema')
        name = item['path']
        need(type(name) is str and name and '\\' not in name, 'Unsafe path')
        need(PurePosixPath(name).suffix in {'.md', '.json', '.py', '.patch'}, 'Disallowed file type')
        parts = name.split('/')
        need(all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) and p not in ('.', '..') for p in parts), 'Unsafe path')
        need(not flat or len(parts) == 1, 'Nonflat frozen inventory')
        need(name not in names, 'Duplicate inventory path')
        names.add(name)
        for parent in PurePosixPath(name).parents:
            if str(parent) != '.': directories.add(str(parent))
        need(type(item['bytes']) is int and item['bytes'] >= 0, 'Invalid byte count')
        need(type(item['sha256']) is str and HEX.fullmatch(item['sha256']) is not None, 'Invalid digest')
    actual_files, actual_dirs = set(), set()
    for directory, subdirs, files in os.walk(root, followlinks=False):
        for name in subdirs + files:
            path = Path(directory) / name
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            need(not stat.S_ISLNK(mode), 'Symlink forbidden: ' + relative)
            if stat.S_ISDIR(mode): actual_dirs.add(relative)
            else:
                need(stat.S_ISREG(mode), 'Special file forbidden: ' + relative)
                actual_files.add(relative)
    need(actual_files == names and actual_dirs == directories, 'Exact inventory mismatch')
    for item in entries:
        data = regular(root / item['path'])
        need(len(data) == item['bytes'] and sha(data) == item['sha256'], 'Payload mismatch: ' + item['path'])
    return len(entries)


def apply_exact_patch(old, patch):
    """Apply the preserved single-file unified diff with exact offsets and context."""
    lines = patch.decode('utf-8').splitlines(keepends=True)
    need(lines[:2] == ['--- verify_packet.py\n', '+++ verify_packet.py\n'], 'Wrong patch headers')
    original = old.decode('utf-8').splitlines(keepends=True)
    output, cursor, i, hunks = [], 0, 2, 0
    while i < len(lines):
        match = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n', lines[i])
        need(match is not None, 'Malformed patch hunk')
        old_start, old_count, new_start, new_count = map(int, match.groups())
        need(old_start - 1 >= cursor, 'Overlapping patch hunk')
        output.extend(original[cursor:old_start-1]); cursor = old_start - 1
        need(len(output) == new_start - 1, 'New hunk offset mismatch')
        used, made = 0, 0
        i += 1
        while i < len(lines) and not lines[i].startswith('@@ '):
            line = lines[i]
            need(line and line[0] in ' +-', 'Invalid patch line')
            if line[0] in ' -':
                need(cursor < len(original) and original[cursor] == line[1:], 'Exact patch context mismatch')
                cursor += 1; used += 1
            if line[0] in ' +': output.append(line[1:]); made += 1
            i += 1
        need(used == old_count and made == new_count, 'Patch hunk count mismatch')
        hunks += 1
    need(hunks == 1, 'Unexpected hunk count')
    output.extend(original[cursor:])
    return ''.join(output).encode('utf-8')


def exact_correction(root):
    preserved = regular(root / 'independent_audit/HARDENING.patch')
    old_header, new_header = b'@@ -77,7 +77,7 @@\n', b'@@ -76,7 +76,7 @@\n'
    need(preserved.count(old_header) == 1, 'Unexpected preserved patch header')
    canonical = regular(root / 'HARDENING_REPLAY.patch')
    need(canonical == preserved.replace(old_header, new_header), 'Canonical patch changes more than hunk offsets')
    replayed = apply_exact_patch(regular(root / 'original/verify_packet.py'), canonical)
    need(replayed == regular(root / 'corrected/verify_packet.py'), 'Patch replay mismatch')
    original_manifest = load_json(regular(root / 'original/MANIFEST.json'))
    changed = 0
    for item in original_manifest['files']:
        if item['path'] == 'verify_packet.py':
            item.update(bytes=len(replayed), sha256=sha(replayed)); changed += 1
    need(changed == 1, 'Missing or repeated verifier entry')
    derived_manifest = (json.dumps(original_manifest, indent=2) + '\n').encode('utf-8')
    need(derived_manifest == regular(root / 'corrected/MANIFEST.json'), 'Derived manifest mismatch')
    for path in (root / 'original').iterdir():
        if path.name not in {'verify_packet.py', 'MANIFEST.json'}:
            need(regular(path) == regular(root / 'corrected' / path.name), 'Unexpected derived change: ' + path.name)


def verify(root, expected):
    need(type(expected) is str and HEX.fullmatch(expected) is not None, 'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode), 'Packet root must be a real directory')
    raw = regular(root / 'PUBLICATION_MANIFEST.json')
    need(sha(raw) == expected, 'Publication manifest anchor mismatch')
    manifest = load_json(raw)
    need(type(manifest) is dict and set(manifest) == {'schema', 'problem_id', 'status', 'turns', 'source_files_redistributed', 'frozen_manifest_anchors', 'files'}, 'Invalid publication schema')
    need(manifest['schema'] == 'logarithmic-deletion-publication-v1', 'Wrong publication schema')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30003081, 'Wrong problem')
    need(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Wrong disposition')
    need(manifest['source_files_redistributed'] is False, 'Source redistribution not permitted')
    need(manifest['frozen_manifest_anchors'] == FROZEN, 'Frozen anchor mapping mismatch')
    need({p.name for p in root.iterdir()} == TOP_FILES | {'original', 'corrected', 'independent_audit'}, 'Top-level inventory mismatch')
    count = validate_members(root, 'PUBLICATION_MANIFEST.json', manifest['files'])
    for relative, anchor in FROZEN.items():
        path = root / relative
        raw = regular(path)
        need(sha(raw) == anchor, 'Frozen manifest anchor mismatch: ' + relative)
        inner = load_json(raw)
        need(type(inner) is dict and set(inner) == {'schema', 'files'}, 'Frozen schema fields')
        expected_schema = 'source-free-independent-audit-v1' if relative.startswith('independent_audit/') else 'source-free-flat-v1'
        need(inner['schema'] == expected_schema, 'Wrong frozen schema')
        validate_members(path.parent, 'MANIFEST.json', inner['files'], flat=True)
    for path in root.rglob('*.json'): load_json(regular(path))
    for path in root.rglob('*.py'):
        need(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(regular(path)))), 'Optimization-removable guard: ' + str(path.relative_to(root)))
    exact_correction(root)
    return count


def replay(root, selected):
    env = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    modes = [('ordinary', []), ('optimized', ['-O']), ('double_optimized', ['-OO'])]
    receipts = []
    for mode, flags in modes:
        if selected != 'all' and selected != mode: continue
        with tempfile.TemporaryDirectory(prefix='log-deletion-replay-') as temporary:
            cwd = Path(temporary)
            def run(script, extra=(), expected_status='PASS'):
                r = subprocess.run([sys.executable, '-I', '-B', *flags, str(script), *map(str,extra)], env=env, cwd=cwd, capture_output=True, timeout=180)
                need(r.returncode == 0, 'Replay failed: ' + script.name + ': ' + r.stderr.decode(errors='replace'))
                obj = load_json(r.stdout)
                need(obj['status'] == expected_status, 'Replay status mismatch: ' + script.name)
                return obj, r.stdout
            for directory, script in [('original','verify_packet.py'), ('corrected','verify_packet.py'), ('independent_audit','verify_audit.py')]:
                obj, output = run(root / directory / script, ['--root', root / directory, '--manifest-sha256', FROZEN[directory+'/MANIFEST.json']])
                need(obj['optimization'] == len(flags) + (1 if flags == ['-OO'] else 0) and obj['payload_files'] == 15, 'Replay count/mode mismatch')
                receipts.append({'script':directory+'/'+script, 'mode':mode, 'status':'PASS', 'stdout_sha256':sha(output)})
            # Historical control scripts mutate temporary copies without making copied
            # read-only files writable. Stage an exact disposable writable input first.
            staged = cwd / 'author_controls_input'
            shutil.copytree(root / 'original', staged)
            staged.chmod(0o700)
            for path in staged.iterdir(): path.chmod(0o600)
            _, output = run(staged / 'mutation_tests.py', ['--root', staged, '--manifest-sha256', FROZEN['original/MANIFEST.json']])
            need(output == regular(root / 'independent_audit/AUTHOR_CONTROLS_RERUN.json'), 'Author control output mismatch')
            receipts.append({'script':'original/mutation_tests.py', 'mode':mode, 'all_child_modes':True, 'stdout_sha256':sha(output)})
            _, output = run(root / 'independent_audit/independent_controls.py', ['--author-root', staged])
            need(output == regular(root / 'independent_audit/EXPANDED_CONTROLS.json'), 'Independent control output mismatch')
            receipts.append({'script':'independent_audit/independent_controls.py', 'mode':mode, 'all_child_modes':True, 'stdout_sha256':sha(output)})
            obj, output = run(root / 'independent_audit/verify_sources.py', expected_status='NOT_RUN')
            need(all(x['status'].startswith('NOT_RUN') for x in obj['checks']), 'Source-free run claimed source verification')
            receipts.append({'script':'independent_audit/verify_sources.py', 'mode':mode, 'status':'NOT_RUN', 'reason':'No original source bytes supplied'})
            for kind in ('--pdf-dir', '--corpus-dir'):
                missing = cwd / ('missing_' + kind[2:]); missing.mkdir()
                r = subprocess.run([sys.executable, '-I', '-B', *flags, str(root/'independent_audit/verify_sources.py'),kind,str(missing)], env=env, cwd=cwd, capture_output=True, timeout=30)
                need(r.returncode == 1 and r.stderr.startswith(b'REJECT:'), 'Missing requested sources not rejected')
            # Patch is optional diagnostic hardening, tested on an externally re-pinned
            # malformed disposable fixture; the immutable original already fails closed.
            bad = cwd / 'syntax_fixture'; shutil.copytree(staged,bad)
            script = bad / 'check_math.py'; script.write_bytes(script.read_bytes()+b'\ndef invalid syntax\n')
            mf = bad / 'MANIFEST.json'; m = load_json(mf.read_bytes())
            for item in m['files']:
                if item['path'] == script.name: item.update(bytes=script.stat().st_size,sha256=sha(script.read_bytes()))
            mf.write_text(json.dumps(m))
            for directory in ('original','corrected'):
                r = subprocess.run([sys.executable,'-I','-B',*flags,str(root/directory/'verify_packet.py'),'--root',str(bad),'--manifest-sha256',sha(mf.read_bytes())],env=env,cwd=cwd,capture_output=True,timeout=30)
                need(r.returncode != 0, 'Malformed Python accepted')
                if directory == 'corrected': need(r.returncode == 1 and r.stderr.startswith(b'REJECT:'), 'Hardening diagnostic failed')
            receipts.append({'mode':mode, 'optional_hardening':'Original and corrected reject malformed Python; corrected uses REJECT diagnostic', 'missing_requested_sources':'Both rejected'})
    return receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path,default=Path(__file__).absolute().parent)
    parser.add_argument('--expected-manifest',required=True)
    parser.add_argument('--check-only',action='store_true')
    parser.add_argument('--mode',choices=['all','ordinary','optimized','double_optimized'],default='all')
    args = parser.parse_args(); root = args.packet.absolute()
    try:
        count = verify(root,args.expected_manifest)
        receipts = [] if args.check_only else replay(root,args.mode)
        verify(root,args.expected_manifest)
        print(json.dumps({'status':'PASS','problem_id':30003081,'publication_manifest_sha256':args.expected_manifest,
                          'bound_files':count,'check_only':args.check_only,'replays':receipts,
                          'limits':'Integrity and bounded exact diagnostics only. Source bytes are absent; no universal proof, novelty, exhaustive literature, formal verification or human peer review is certified.'},indent=2,sort_keys=True))
    except (RuntimeError,ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: '+str(error),file=sys.stderr); return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
