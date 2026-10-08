#!/usr/bin/env python3
"""Authenticate this wrapper externally before execution; separately pin its manifest.
Checks identity and exact finite diagnostics, not arbitrary mathematical proofs.
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
    'public': '63f3be3527b07b3cef5b5bc509f3bcd93e78fec442a62f1f59bab0ca9ab3e554',
    'audit': '7b2f6b7d36716b7044c0e41a98d4fd21a86ef114c5a5374ab420c46117c4286c',
}
TOP = {'README.md', 'PUBLICATION_ACCEPTANCE.md', 'RESEARCH_LOG.md',
       'VERIFY_PUBLICATION.py', 'TEST_MUTATIONS.py', 'MUTATION_RESULTS.json',
       'PUBLICATION_MANIFEST.json'}
HEX = re.compile(r'[0-9a-f]{64}')

def need(value, message):
    if not value: raise RuntimeError(message)


def sha(data): return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(raw):
    def bad(value): raise ValueError('Nonfinite JSON: ' + value)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad)


def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'Nonregular file: ' + str(path))
    return path.read_bytes()


def inventory(root, manifest_name, entries, profile, flat=False):
    need(type(entries) is list and bool(entries), 'Invalid inventory')
    names, directories = {manifest_name}, set()
    for item in entries:
        need(type(item) is dict and set(item) == {'path','bytes','sha256','mode'}, 'Invalid member schema')
        name = item['path']
        need(type(name) is str and name and '\\' not in name, 'Unsafe path')
        parts = name.split('/')
        need(all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) and p not in ('.','..') for p in parts), 'Unsafe path')
        need(PurePosixPath(name).suffix in {'.md','.json','.py','.patch'}, 'Invalid member extension')
        need(not flat or len(parts) == 1, 'Nonflat frozen slice')
        need(name not in names, 'Duplicate inventory path'); names.add(name)
        for parent in PurePosixPath(name).parents:
            if str(parent) != '.': directories.add(str(parent))
        need(type(item['bytes']) is int and item['bytes'] >= 0, 'Invalid byte count')
        need(type(item['sha256']) is str and HEX.fullmatch(item['sha256']) is not None, 'Invalid digest')
        need(type(item['mode']) is str and item['mode'] == '0644', 'Baseline file mode must be 0644')
    actual_files, actual_dirs = set(), set()
    expected_file_mode, expected_dir_mode = (0o644,0o755) if profile == 'baseline' else (0o444,0o555)
    need(stat.S_IMODE(root.lstat().st_mode) == expected_dir_mode, 'Root mode mismatch')
    for directory, subdirs, files in os.walk(root, followlinks=False):
        for name in subdirs + files:
            path = Path(directory)/name; mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            need(not stat.S_ISLNK(mode), 'Symlink forbidden: ' + relative)
            if stat.S_ISDIR(mode):
                need(stat.S_IMODE(mode) == expected_dir_mode, 'Directory mode mismatch: ' + relative)
                actual_dirs.add(relative)
            else:
                need(stat.S_ISREG(mode), 'Special file forbidden: ' + relative)
                need(stat.S_IMODE(mode) == expected_file_mode, 'File mode mismatch: ' + relative)
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
    m = load_json(raw)
    need(type(m) is dict and set(m) == {'schema','problem_id','rank','status','turns','source_files_redistributed','frozen_manifest_anchors','baseline_file_mode','files'}, 'Invalid publication schema')
    need(m['schema'] == 'mapping-class-cohomology-publication-v1', 'Wrong schema')
    need(type(m['problem_id']) is int and m['problem_id'] == 30003298 and type(m['rank']) is int and m['rank'] == 997, 'Wrong target')
    need(m['status'] == 'unsolved' and m['turns'] == '5/5', 'Wrong disposition')
    need(m['source_files_redistributed'] is False and m['baseline_file_mode'] == '0644', 'Wrong publication scope/mode')
    need(type(m['frozen_manifest_anchors']) is dict and m['frozen_manifest_anchors'] == FROZEN, 'Wrong frozen anchors')
    need({p.name for p in root.iterdir()} == TOP | set(FROZEN), 'Top-level inventory mismatch')
    count = inventory(root,'PUBLICATION_MANIFEST.json',m['files'],profile)
    for name,pin in FROZEN.items():
        filename = 'MANIFEST.json' if name == 'public' else 'AUDIT_MANIFEST.json'
        raw = regular(root/name/filename); need(sha(raw) == pin, 'Frozen anchor mismatch: '+name)
        inner = load_json(raw)
        fields = {'schema','files'} if name == 'public' else {'schema','problem_id','author_manifest_sha256','files'}
        need(type(inner) is dict and set(inner) == fields, 'Invalid inner schema')
        need(type(inner['schema']) is int and inner['schema'] == 1, 'Invalid inner version')
        if name == 'audit':
            need(type(inner['problem_id']) is int and inner['problem_id'] == 30003298, 'Wrong audit target')
            need(inner['author_manifest_sha256'] == FROZEN['public'], 'Wrong audited freeze')
        need(type(inner['files']) is list and len(inner['files']) == (9 if name == 'public' else 6), 'Invalid inner inventory')
        items = []
        for item in inner['files']:
            need(type(item) is dict and set(item) == {'name','bytes','sha256'}, 'Invalid inner record')
            items.append({'path':item['name'],'bytes':item['bytes'],'sha256':item['sha256'],'mode':'0644'})
        inventory(root/name,filename,items,profile,flat=True)
    for path in root.rglob('*.json'): load_json(regular(path))
    for path in root.rglob('*.py'):
        need(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(regular(path)))), 'Optimization-removable check: '+path.name)
    return count


def snapshot(root):
    return {p.relative_to(root).as_posix():(stat.S_IMODE(p.lstat().st_mode),sha(regular(p)) if p.is_file() else None) for p in [root,*root.rglob('*')]}


def stage(source,destination):
    shutil.copytree(source,destination)
    destination.chmod(0o755)
    for p in destination.rglob('*'): p.chmod(0o755 if p.is_dir() else 0o644)


def readonly_stage(source,destination):
    stage(source,destination)
    for p in destination.rglob('*'): p.chmod(0o555 if p.is_dir() else 0o444)
    destination.chmod(0o555)


def writable(root):
    root.chmod(0o755)
    for p in root.rglob('*'): p.chmod(0o755 if p.is_dir() else 0o644)


def replay(root,selected):
    before = snapshot(root); receipts = []
    env = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for label,flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        if selected != 'all' and label != selected: continue
        with tempfile.TemporaryDirectory(prefix='mapping-class-publication-') as temporary:
            work = Path(temporary); packet = work/'readonly-packet'
            readonly_stage(root,packet); ro_before = snapshot(packet)
            blocked = []
            for path,mode in [(packet/'probe','wb'),(packet/'public/PROOF.md','ab')]:
                try:
                    with path.open(mode): pass
                except PermissionError: blocked.append(True)
                else: blocked.append(False)
            need(blocked == [True,True], 'Read-only probes unexpectedly writable')
            def invoke(script):
                cp = subprocess.run([sys.executable,'-I','-B',*flags,str(script)],cwd=work,env=env,capture_output=True,timeout=300)
                need(cp.returncode == 0, 'Replay failed: '+script.name+': '+cp.stdout.decode(errors='replace')[-1000:]+cp.stderr.decode(errors='replace')[-1000:])
                obj = load_json(cp.stdout); need(obj['status'] == 'PASS', 'Replay status mismatch')
                return obj,cp.stdout
            try:
                for name,script,total in [('public','verify.py',13830),('audit','independent_verify.py',4398)]:
                    obj,out = invoke(packet/name/script)
                    need(type(obj['checks']) is int and obj['checks'] == total, 'Replay count mismatch')
                    receipts.append({'mode':label,'slice':name,'checks':total,'stdout_sha256':sha(out)})
                # Historical mutation harness copies permissions before editing fixtures.
                # Run it from separate writable copies; its own readonly probes remain active.
                harness = work/'harness'; harness.mkdir()
                for name in FROZEN: stage(root/name,harness/name)
                harness_before = snapshot(harness)
                obj,out = invoke(harness/'audit/test_independent.py')
                need(snapshot(harness) == harness_before, 'Historical harness changed its source fixture')
                need(obj == load_json(regular(root/'audit/CONTROL_RESULTS.json')), 'Historical control output mismatch')
                receipts.append({'mode':label,'suite':'independent_and_author_controls','child_modes':3,'independent_rejections_per_child_mode':40,'author_rejections_per_child_mode':20,'stdout_sha256':sha(out)})
                need(snapshot(packet) == ro_before, 'Read-only replay changed packet')
                receipts.append({'mode':label,'profile':'readonly_0444_0555','original_manifest_anchors_preserved':True,'write_probes_rejected':2,'unchanged':True})
            finally: writable(packet)
    need(snapshot(root) == before, 'Publication packet changed during replay')
    return receipts


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',type=Path,default=Path(__file__).absolute().parent)
    p.add_argument('--expected-manifest',required=True)
    p.add_argument('--filesystem-profile',choices=['baseline','readonly'],default='baseline')
    p.add_argument('--check-only',action='store_true')
    p.add_argument('--mode',choices=['all','normal','-O','-OO'],default='all')
    args = p.parse_args(); root = args.packet.absolute()
    try:
        count = verify(root,args.expected_manifest,args.filesystem_profile)
        results = [] if args.check_only else replay(root,args.mode)
        verify(root,args.expected_manifest,args.filesystem_profile)
        print(json.dumps({'status':'PASS','problem_id':30003298,'publication_manifest_sha256':args.expected_manifest,'bound_files':count,'filesystem_profile':args.filesystem_profile,'check_only':args.check_only,'replays':results,'limits':'Source-free identity and finite diagnostics; not formal proof, human peer review, novelty, or global openness certification.'},indent=2,sort_keys=True))
    except (RuntimeError,ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: '+str(error),file=sys.stderr); return 1
    return 0

if __name__ == '__main__': sys.exit(main())
