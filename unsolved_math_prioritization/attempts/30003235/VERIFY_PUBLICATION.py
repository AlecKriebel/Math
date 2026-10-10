#!/usr/bin/env python3
"""Source-free integrity and finite replay only. Authenticate this file before execution.
An independently trusted outer-manifest SHA-256 is also required.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile

FROZEN = {
    'original/MANIFEST.json': 'b499c40203ef2203d86d3dd6fd6e612944d7cbad92edb801170626965bc07b90',
    'independent_audit/AUDIT_MANIFEST.json': 'ee06ce6399f65b6775d4f7e892dc91efd133e47e236197a00b84fba33f268eca',
}
TOP_FILES = {'README.md', 'PUBLICATION_ACCEPTANCE.md', 'RESEARCH_LOG.md',
             'VERIFY_PUBLICATION.py', 'TEST_MUTATIONS.py', 'MUTATION_RESULTS.json',
             'PUBLICATION_MANIFEST.json'}
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
    def finite_float(value):
        result = float(value)
        need(math.isfinite(result), 'Nonfinite JSON number')
        return result
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad_constant, parse_float=finite_float)


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


def verify(root, expected):
    need(type(expected) is str and HEX.fullmatch(expected) is not None, 'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode), 'Packet root must be a real directory')
    raw = regular(root / 'PUBLICATION_MANIFEST.json')
    need(sha(raw) == expected, 'Publication manifest anchor mismatch')
    manifest = load_json(raw)
    need(type(manifest) is dict and set(manifest) == {'schema', 'problem_id', 'status', 'turns', 'source_files_redistributed', 'frozen_manifest_anchors', 'files'}, 'Invalid publication schema')
    need(manifest['schema'] == 'weighted-affine-endpoint-publication-v1', 'Wrong publication schema')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30003235, 'Wrong problem')
    need(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Wrong disposition')
    need(manifest['source_files_redistributed'] is False, 'Source redistribution not permitted')
    need(manifest['frozen_manifest_anchors'] == FROZEN, 'Frozen anchor mapping mismatch')
    need({p.name for p in root.iterdir()} == TOP_FILES | {'original', 'independent_audit'}, 'Top-level inventory mismatch')
    count = validate_members(root, 'PUBLICATION_MANIFEST.json', manifest['files'])
    for relative, anchor in FROZEN.items():
        path = root / relative
        raw = regular(path)
        need(sha(raw) == anchor, 'Frozen manifest anchor mismatch: ' + relative)
        inner = load_json(raw)
        need(type(inner) is dict and set(inner) == {'schema', 'files'}, 'Frozen schema fields')
        need(type(inner['schema']) is int and inner['schema'] == 1, 'Wrong frozen schema')
        validate_members(path.parent, path.name, inner['files'])
    for path in root.rglob('*.json'): load_json(regular(path))
    for path in root.rglob('*.py'):
        need(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(regular(path)))), 'Optimization-removable guard: ' + str(path.relative_to(root)))
    return count


def replay(root, mode):
    modes = [('ordinary', []), ('optimized', ['-O']), ('double_optimized', ['-OO'])]
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    receipts = []
    for name, flags in modes:
        if mode != 'all' and mode != name: continue
        with tempfile.TemporaryDirectory(prefix='weighted-affine-publication-replay-') as temporary:
            cwd = Path(temporary)
            def run(script, args=()):
                result = subprocess.run([sys.executable, '-I', '-B', *flags, str(script), *map(str,args)],
                                        cwd=cwd, env=env, capture_output=True, timeout=180)
                need(result.returncode == 0, 'Replay failed: ' + script.name + ': ' + result.stdout.decode(errors='replace') + result.stderr.decode(errors='replace'))
                obj = load_json(result.stdout)
                need(obj['status'] == 'PASS', 'Replay status mismatch')
                return obj, result.stdout
            obj, output = run(root/'original/check.py')
            expected = load_json(regular(root/'original/VERIFICATION_RESULTS.json'))
            need(obj == expected['checker_output'] and obj['total_checks'] == 9485, 'Author replay mismatch')
            receipts.append({'script':'original/check.py','mode':name,'status':'PASS','total_checks':9485,'stdout_sha256':sha(output)})
            obj, output = run(root/'independent_audit/independent_check.py', ['--root', root/'original', '--probe', root/'independent_audit/probe.json'])
            independent = load_json(regular(root/'independent_audit/INDEPENDENT_CONTROLS.json'))
            need(obj == independent['baseline'] and obj['total'] == 9638, 'Independent replay mismatch')
            receipts.append({'script':'independent_audit/independent_check.py','mode':name,'status':'PASS','total_checks':9638,'stdout_sha256':sha(output)})
            # Historical controls mutate disposable copies. Supply a byte-exact,
            # writable temporary copy when the publication input is read-only.
            staged = cwd/'author_controls_input'
            shutil.copytree(root/'original', staged)
            for path in [staged, *staged.rglob('*')]: path.chmod(0o700 if path.is_dir() else 0o600)
            obj, output = run(staged/'run_controls.py')
            need(obj == expected, 'Author control receipt mismatch')
            need(output == regular(root/'independent_audit/AUTHOR_REPLAY.json'), 'Author control bytes mismatch')
            receipts.append({'script':'original/run_controls.py','mode':name,'all_child_modes':True,'negative_controls':len(obj['negative_controls']),'stdout_sha256':sha(output)})
            obj, output = run(root/'independent_audit/run_independent_controls.py', ['--root', staged])
            need(obj == independent and output == regular(root/'independent_audit/INDEPENDENT_CONTROLS.json'), 'Independent control receipt mismatch')
            receipts.append({'script':'independent_audit/run_independent_controls.py','mode':name,'all_child_modes':True,'negative_controls':24,'stdout_sha256':sha(output)})
            # Record the original optional probe interface exactly as accepted:
            # it validates individual entries but permits repeated kinds.
            probes = load_json(regular(root/'original/probes.json'))
            repeated = cwd/'repeated_kinds.json'; repeated.write_text(json.dumps([probes[0]]*3))
            obj, _ = run(root/'original/check.py', ['--probes', repeated])
            need(obj['status'] == 'PASS', 'Historical probe qualification changed')
            receipts.append({'mode':name,'optional_author_probe_interface':'Repeated kinds accepted; no strict collection-schema claim'})
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
        print(json.dumps({'status':'PASS','problem_id':30003235,'publication_manifest_sha256':args.expected_manifest,
                          'bound_files':count,'check_only':args.check_only,'replays':receipts,
                          'limits':'Integrity and bounded exact diagnostics only. Source bytes are absent; no universal proof, novelty, exhaustive literature, formal verification or human peer review is certified.'},indent=2,sort_keys=True))
    except (RuntimeError,ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: '+str(error),file=sys.stderr); return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
