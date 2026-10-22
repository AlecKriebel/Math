#!/usr/bin/env python3
"""Externally authenticate these bytes before execution and separately pin the manifest.

Identity and bounded arithmetic checks only; no global modularity certification.
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
    'original': '7162a7e1927ccaaf5454fde977da28f50d910ed695931e08431eb77d9a878991',
    'independent_audit': 'c9c827f589c5ad30678dcdc7abd1ef780a3379e93363a78b372afc7d2d72bd32',
}
TOP = {'README.md', 'PUBLICATION_ACCEPTANCE.md', 'RESEARCH_LOG.md',
       'VERIFY_PUBLICATION.py', 'TEST_MUTATIONS.py', 'MUTATION_RESULTS.json',
       'PUBLICATION_MANIFEST.json'}
HEX = re.compile(r'[0-9a-f]{64}')


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'Duplicate JSON key: ' + key)
        out[key] = value
    return out


def strict_json(raw):
    def bad(value):
        raise ValueError('Nonintegral or nonfinite JSON number: ' + value)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad, parse_float=bad)


def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'Nonregular file: ' + str(path))
    return path.read_bytes()


def inventory(root, manifest_name, entries, profile, flat=False):
    need(type(entries) is list and bool(entries), 'Invalid inventory list')
    names, directories = {manifest_name}, set()
    for item in entries:
        need(type(item) is dict and set(item) == {'path','bytes','sha256','mode'}, 'Invalid member schema')
        name = item['path']
        need(type(name) is str and name and '\\' not in name, 'Unsafe path')
        parts = name.split('/')
        need(all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) and p not in ('.','..') for p in parts), 'Unsafe path')
        need(PurePosixPath(name).suffix in {'.md','.json','.py'}, 'Forbidden member extension')
        need(not flat or len(parts) == 1, 'Nonflat frozen inventory')
        need(name not in names, 'Duplicate inventory path')
        names.add(name)
        for parent in PurePosixPath(name).parents:
            if str(parent) != '.':
                directories.add(str(parent))
        need(type(item['bytes']) is int and item['bytes'] >= 0, 'Invalid byte count')
        need(type(item['sha256']) is str and HEX.fullmatch(item['sha256']) is not None, 'Invalid digest')
        need(type(item['mode']) is str and item['mode'] == '0644', 'Invalid baseline mode')
    file_mode, dir_mode = (0o644,0o755) if profile == 'baseline' else (0o444,0o555)
    need(stat.S_ISDIR(root.lstat().st_mode), 'Root is not a real directory')
    need(stat.S_IMODE(root.lstat().st_mode) == dir_mode, 'Root mode mismatch')
    actual_files, actual_dirs = set(), set()
    for directory, subdirs, files in os.walk(root, followlinks=False):
        for name in subdirs + files:
            path = Path(directory)/name
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            need(not stat.S_ISLNK(mode), 'Symlink forbidden: ' + relative)
            if stat.S_ISDIR(mode):
                need(stat.S_IMODE(mode) == dir_mode, 'Directory mode mismatch: ' + relative)
                actual_dirs.add(relative)
            else:
                need(stat.S_ISREG(mode), 'Special file forbidden: ' + relative)
                need(stat.S_IMODE(mode) == file_mode, 'File mode mismatch: ' + relative)
                actual_files.add(relative)
    need(actual_files == names and actual_dirs == directories, 'Exact files/directories inventory mismatch')
    for item in entries:
        raw = regular(root/item['path'])
        need(len(raw) == item['bytes'] and sha(raw) == item['sha256'], 'Payload mismatch: ' + item['path'])
    return len(entries)


def verify(root, expected, profile='baseline'):
    need(type(expected) is str and HEX.fullmatch(expected) is not None, 'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode), 'Packet root must be a real directory')
    raw = regular(root/'PUBLICATION_MANIFEST.json')
    need(sha(raw) == expected, 'Publication manifest anchor mismatch')
    m = strict_json(raw)
    need(type(m) is dict and set(m) == {'schema','problem_id','rank','status','turns',
         'source_files_redistributed','frozen_manifest_anchors','baseline_file_mode','files'}, 'Invalid publication schema')
    need(m['schema'] == 'antisymmetric-borcherds-publication-v1', 'Wrong schema')
    need(type(m['problem_id']) is int and m['problem_id'] == 30003140, 'Wrong problem')
    need(type(m['rank']) is int and m['rank'] == 994, 'Wrong rank')
    need(m['status'] == 'unsolved' and m['turns'] == '5/5', 'Wrong disposition')
    need(m['source_files_redistributed'] is False and m['baseline_file_mode'] == '0644', 'Wrong scope/mode')
    need(m['frozen_manifest_anchors'] == FROZEN, 'Wrong frozen anchors')
    need({p.name for p in root.iterdir()} == TOP | set(FROZEN), 'Top-level inventory mismatch')
    count = inventory(root,'PUBLICATION_MANIFEST.json',m['files'],profile)
    for name,pin in FROZEN.items():
        raw = regular(root/name/'MANIFEST.json')
        need(sha(raw) == pin, 'Frozen anchor mismatch: ' + name)
        inner = strict_json(raw)
        need(type(inner) is dict and set(inner) == {'exceptions','files'}, 'Invalid frozen schema')
        need(inner['exceptions'] == ['MANIFEST.json is externally pinned and excludes itself'], 'Wrong manifest exception')
        need(type(inner['files']) is dict and len(inner['files']) == (8 if name == 'original' else 6), 'Invalid frozen inventory')
        entries = []
        for filename,item in inner['files'].items():
            need(type(item) is dict and set(item) == {'bytes','sha256'}, 'Invalid frozen member')
            entries.append(dict(path=filename,mode='0644',**item))
        inventory(root/name,'MANIFEST.json',entries,profile,flat=True)
    for path in root.rglob('*.json'):
        strict_json(regular(path))
    for path in root.rglob('*.py'):
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(regular(path)))), 'Optimization-removable check: ' + path.name)
    return count


def snapshot(root):
    return {p.relative_to(root).as_posix(): (stat.S_IMODE(p.lstat().st_mode),
            sha(regular(p)) if p.is_file() else None) for p in [root,*root.rglob('*')]}


def replay(root, selected):
    before = snapshot(root)
    receipts = []
    env = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for label,flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        if selected != 'all' and label != selected:
            continue
        with tempfile.TemporaryDirectory(prefix='borcherds-publication-') as temporary:
            work = Path(temporary)
            for name in FROZEN:
                shutil.copytree(root/name,work/name)
                for p in [work/name,*(work/name).rglob('*')]:
                    p.chmod(0o755 if p.is_dir() else 0o644)
            def invoke(script, arguments=()):
                # The author's control suite imports its pinned sibling verify.py.
                # Other entry points support isolated mode directly.
                isolation = [] if script.name == 'test_negative_controls.py' else ['-I']
                cp = subprocess.run([sys.executable,*isolation,'-B',*flags,str(script),*map(str,arguments)],
                     cwd=work,env=env,capture_output=True,timeout=240)
                need(cp.returncode == 0, 'Replay failed: ' + script.name + ': ' + cp.stderr.decode(errors='replace')[-2000:])
                return strict_json(cp.stdout), cp.stdout
            def arithmetic(profile):
                obj,out = invoke(work/'original/verify.py',['--manifest-sha',FROZEN['original']])
                need(obj['status'] == 'PASS_BOUNDED_ARITHMETIC_ONLY' and obj['global_modularity'] == 'NOT_PROVED', 'Author status mismatch')
                need(obj['good_prime_factors'] == 20 and obj['bad_prime_factors'] == 4, 'Author count mismatch')
                receipts.append(dict(mode=label,slice='original',profile=profile,stdout_sha256=sha(out)))
                obj,out = invoke(work/'independent_audit/independent_exact.py',[work/'original'])
                need(obj['status'] == 'PASS_INDEPENDENT_BOUNDED_ARITHMETIC' and obj['global_modularity'] == 'NOT_PROVED', 'Audit status mismatch')
                need(obj['good_factors'] == 20 and obj['bad_factors'] == 4 and obj['exact_theta_identities'] == 3, 'Audit count mismatch')
                receipts.append(dict(mode=label,slice='independent_audit',profile=profile,stdout_sha256=sha(out)))
            arithmetic('baseline_0644')
            # Both frozen control programs already iterate over all three modes.
            # Run them once, rather than imply nine independent suites.
            if label == 'normal' or selected != 'all':
                obj,out = invoke(work/'original/test_negative_controls.py',['--manifest-sha',FROZEN['original']])
                need(obj == {'modes':['normal','-O','-OO'],'positive_relocated_runs':3,
                     'rejected_integrity_mutations':15,'rejected_mathematical_mutations':21,
                     'status':'PASS_NEGATIVE_CONTROLS_ONLY'}, 'Author control mismatch')
                receipts.append(dict(suite='author_controls',all_child_modes=True,positives=3,
                                     mathematical_rejections=21,integrity_rejections=15,stdout_sha256=sha(out)))
                obj,out = invoke(work/'independent_audit/test_independent_controls.py',[work/'original'])
                need(obj['status'] == 'PASS_INDEPENDENT_NEGATIVE_CONTROLS' and obj['positive'] == 3
                     and obj['rejected'] == 87 and len(obj['cases']) == 29, 'Independent control mismatch')
                receipts.append(dict(suite='independent_controls',all_child_modes=True,positives=3,
                                     rejections=87,cases_per_mode=29,stdout_sha256=sha(out)))
            for name in FROZEN:
                for p in (work/name).rglob('*'):
                    p.chmod(0o555 if p.is_dir() else 0o444)
                (work/name).chmod(0o555)
            ro_before = snapshot(work)
            blocked = False
            try:
                with (work/'original/README.md').open('ab'):
                    pass
            except PermissionError:
                blocked = True
            need(blocked, 'Read-only fixture writable; do not run as a privileged user')
            try:
                arithmetic('readonly_0444_same_frozen_bytes')
                need(snapshot(work) == ro_before, 'Read-only fixture changed')
            finally:
                for name in FROZEN:
                    for p in [work/name,*(work/name).rglob('*')]:
                        p.chmod(0o755 if p.is_dir() else 0o644)
    need(snapshot(root) == before, 'Publication packet changed during replay')
    return receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path,default=Path(__file__).absolute().parent)
    parser.add_argument('--expected-manifest',required=True)
    parser.add_argument('--filesystem-profile',choices=['baseline','readonly'],default='baseline')
    parser.add_argument('--check-only',action='store_true')
    parser.add_argument('--mode',choices=['all','normal','-O','-OO'],default='all')
    args = parser.parse_args()
    root = args.packet.absolute()
    try:
        count = verify(root,args.expected_manifest,args.filesystem_profile)
        results = [] if args.check_only else replay(root,args.mode)
        verify(root,args.expected_manifest,args.filesystem_profile)
        print(json.dumps(dict(status='PASS_BOUNDED_PUBLICATION',problem_id=30003140,
              publication_manifest_sha256=args.expected_manifest,bound_files=count,
              filesystem_profile=args.filesystem_profile,check_only=args.check_only,replays=results,
              global_modularity='NOT_PROVED',external_sources='NOT_REPLAYED_METADATA_ONLY'),indent=2,sort_keys=True))
    except (ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: ' + str(error),file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
