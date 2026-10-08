#!/usr/bin/env python3
"""Externally authenticate this wrapper and independently pin the manifest.
Source-free artifact identity, exact patch replay and finite diagnostics only.
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
    'original': '2ed09ec9ba1d31bb913b84c6e63f3256394744c7635817ec2a1467cbcb124ec0',
    'independent_audit': '6f6310bc3c592f76f1b42edcc3239123cf5620af14cd0c9f53e69e13a31b98ab',
    'corrected': '10e904a94ffabba520bd60ebbfb27f0dd41eb0d248f49eb7680ed0dd7e6aaf94',
}
TOP = {'README.md', 'PUBLICATION_ACCEPTANCE.md', 'RESEARCH_LOG.md',
       'VERIFY_PUBLICATION.py', 'BOOTSTRAP.py', 'TEST_MUTATIONS.py',
       'MUTATION_RESULTS.json', 'PUBLICATION_MANIFEST.json'}

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


def exact_patch(old, patch, filename):
    lines = patch.decode().splitlines(keepends=True)
    need(lines[:2] == ['--- a/'+filename+'\n','+++ b/'+filename+'\n'], 'Patch path mismatch')
    original = old.decode().splitlines(keepends=True)
    output, cursor, i, hunks = [], 0, 2, 0
    while i < len(lines):
        match = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[i])
        need(match is not None, 'Invalid hunk header')
        old_start, old_count, new_start, new_count = map(int,match.groups())
        need(old_start >= 1 and old_start - 1 >= cursor and old_start - 1 <= len(original), 'Invalid hunk offset')
        output.extend(original[cursor:old_start-1]); cursor = old_start-1
        need(len(output) == new_start-1, 'New hunk offset mismatch')
        used, made = 0,0; i += 1
        while i < len(lines) and not lines[i].startswith('@@ '):
            line = lines[i]; need(line and line[0] in ' +-', 'Invalid patch line')
            if line[0] in ' -':
                need(cursor < len(original) and original[cursor] == line[1:], 'Exact patch context mismatch')
                cursor += 1; used += 1
            if line[0] in ' +': output.append(line[1:]); made += 1
            i += 1
        need(used == old_count and made == new_count, 'Hunk count mismatch'); hunks += 1
    need(hunks >= 1, 'No patch hunks'); output.extend(original[cursor:])
    return ''.join(output).encode()

def correction(root):
    raw = regular(root/'independent_audit/CORRECTIONS.patch')
    sections = re.split(rb'(?m)(?=^--- a/)',raw)
    need(sections[0] == b'', 'Unexpected patch prefix')
    patches = {}
    for block in sections[1:]:
        first = block.splitlines()[0].decode()
        name = first.removeprefix('--- a/')
        need(re.fullmatch(r'[A-Za-z0-9_.-]+',name) is not None and name not in patches, 'Unsafe or duplicate patch path')
        patches[name] = block
    need(set(patches) == {'MANIFEST.json','PROOFS.md','VALIDATION.md','selftest.py','verify.py'}, 'Unexpected patch scope')
    original = root/'original'; hardened = root/'corrected'
    need({p.name for p in original.iterdir()} == {p.name for p in hardened.iterdir()}, 'Hardening inventory mismatch')
    for p in original.iterdir():
        expected = regular(p)
        if p.name in patches: expected = exact_patch(expected,patches[p.name],p.name)
        need(regular(hardened/p.name) == expected,'Unexpected hardened bytes: '+p.name)


def verify(root, expected, profile='baseline'):
    need(type(expected) is str and HEX.fullmatch(expected) is not None,'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode),'Packet root must be real directory')
    raw = regular(root/'PUBLICATION_MANIFEST.json')
    need(sha(raw) == expected,'Publication manifest anchor mismatch')
    m = load_json(raw)
    need(type(m) is dict and set(m) == {'schema','problem_id','rank','status','turns','source_files_redistributed','frozen_manifest_anchors','baseline_file_mode','files'},'Invalid publication schema')
    need(type(m['schema']) is str and m['schema'] == 'high-frequency-coercivity-publication-v1','Wrong publication schema')
    need(type(m['problem_id']) is int and m['problem_id'] == 30003533 and type(m['rank']) is int and m['rank'] == 1000,'Wrong target')
    need(type(m['status']) is str and m['status'] == 'unsolved' and type(m['turns']) is str and m['turns'] == '5/5','Wrong disposition')
    need(m['source_files_redistributed'] is False and type(m['baseline_file_mode']) is str and m['baseline_file_mode'] == '0644','Wrong scope or mode')
    need(m['frozen_manifest_anchors'] == FROZEN,'Wrong frozen anchors')
    need({p.name for p in root.iterdir()} == TOP | set(FROZEN),'Top-level inventory mismatch')
    count = inventory(root,'PUBLICATION_MANIFEST.json',m['files'],profile)
    bootstrap = regular(root/'BOOTSTRAP.py')
    line = ("WRAPPER_SHA256 = '"+sha(regular(root/'VERIFY_PUBLICATION.py'))+"'").encode()
    need(bootstrap.count(line) == 1,'Bootstrap wrapper pin mismatch')
    template = bootstrap.replace(line,b"WRAPPER_SHA256 = 'WRAPPER_HASH_PLACEHOLDER'")
    need(sha(template) == '6ac9a241619a16296ab5dcb962d8b9e45e38c406bd38049f17933545071f4980','Bootstrap template mismatch')
    for name,pin in FROZEN.items():
        manifest_name = 'AUDIT_MANIFEST.json' if name == 'independent_audit' else 'MANIFEST.json'
        raw = regular(root/name/manifest_name); need(sha(raw) == pin,'Frozen anchor mismatch: '+name)
        inner = load_json(raw)
        keys = {'schema_version','files'}
        if name == 'independent_audit': keys |= {'original_manifest_sha256','problem_id'}
        need(type(inner) is dict and set(inner) == keys,'Invalid inner schema')
        need(type(inner['schema_version']) is int and inner['schema_version'] == 1 and type(inner['files']) is dict,'Invalid inner types')
        need(len(inner['files']) == (9 if name == 'independent_audit' else 12),'Invalid inner count')
        if name == 'independent_audit':
            need(type(inner['problem_id']) is int and inner['problem_id'] == 30003533 and inner['original_manifest_sha256'] == FROZEN['original'],'Audit identity')
        items = []
        for member,item in inner['files'].items():
            need(type(item) is dict and set(item) == {'bytes','sha256'},'Invalid inner record')
            items.append(dict(item,path=member,mode='0644'))
        inventory(root/name,manifest_name,items,profile,flat=True)
    need(regular(root/'corrected/MANIFEST.json') == regular(root/'independent_audit/CORRECTED_MANIFEST.json'),'Corrected manifest disagreement')
    for path in root.rglob('*.json'): load_json(regular(path))
    for path in root.rglob('*.py'):
        need(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(regular(path)))),'Optimization-removable check: '+path.name)
    correction(root)
    return count


def snapshot(root):
    return {p.relative_to(root).as_posix():(stat.S_IMODE(p.lstat().st_mode),sha(regular(p)) if p.is_file() else None) for p in [root,*root.rglob('*')]}


def stage(source,destination,readonly=False):
    shutil.copytree(source,destination)
    for p in destination.rglob('*'): p.chmod(0o555 if p.is_dir() and readonly else 0o755 if p.is_dir() else 0o444 if readonly else 0o644)
    destination.chmod(0o555 if readonly else 0o755)


def replay(root,selected):
    before = snapshot(root); receipts = []
    env = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}; env['PYTHONDONTWRITEBYTECODE'] = '1'
    expected_author = load_json(regular(root/'corrected/REPLAY.json'))
    historical = load_json(regular(root/'independent_audit/VALIDATION_RECEIPT.json'))
    for label,flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        if selected != 'all' and label != selected: continue
        with tempfile.TemporaryDirectory(prefix='coercivity-publication-') as temporary:
            work = Path(temporary); cwd = work/'unrelated'; cwd.mkdir()
            def invoke(script,extra=()):
                # Authenticated author scripts import a sibling module; omit -I here.
                # Sanitized environment, unrelated cwd, and -B prevent ambient PYTHON* injection and bytecode writes.
                cp = subprocess.run([sys.executable,'-B',*flags,str(script),*map(str,extra)],cwd=cwd,env=env,capture_output=True,timeout=300)
                need(cp.returncode == 0,'Replay failed: '+script.name+': '+cp.stdout.decode(errors='replace')[-2000:]+cp.stderr.decode(errors='replace')[-1000:])
                return load_json(cp.stdout),cp.stdout
            for name in ['original','corrected']:
                stage(root/name,work/name)
                obj,out = invoke(work/name/'verify.py')
                need(obj == expected_author,'Author finite control output mismatch')
                receipts.append({'mode':label,'suite':name+'_author_controls','exact_checks':4455,'stdout_sha256':sha(out)})
                obj,out = invoke(root/'independent_audit/independent_controls.py',['--packet',work/name,'--manifest',FROZEN[name]])
                need(obj == historical['independent_controls'],'Independent output mismatch')
                receipts.append({'mode':label,'suite':name+'_independent_controls','exact_checks':4658,'numerical_checks':2144,'integrity_checks':69,'stdout_sha256':sha(out)})
                ro = work/(name+'_readonly'); stage(root/name,ro,True); rb = snapshot(ro); blocked = False
                try:
                    with (ro/'PROOFS.md').open('ab'): pass
                except PermissionError: blocked = True
                need(blocked,'Read-only fixture writable; run unprivileged')
                try:
                    obj,out = invoke(ro/'verify.py'); need(obj == expected_author,'Read-only author output mismatch')
                    obj,out = invoke(root/'independent_audit/independent_controls.py',['--packet',ro,'--manifest',FROZEN[name]])
                    need(obj == historical['independent_controls'],'Read-only independent output mismatch')
                    if name == 'corrected':
                        obj,out = invoke(ro/'selftest.py')
                        need(obj == historical['corrected_selftest_modes'][0],'Corrected hostile controls changed')
                        receipts.append({'mode':label,'suite':'corrected_readonly_selftest','successful_replays':6,'mutation_cases':13,'rejections':39,'stdout_sha256':sha(out)})
                    need(snapshot(ro) == rb,'Read-only bytes/modes changed')
                    receipts.append({'mode':label,'suite':name+'_readonly_relocated','write_blocked':True,'unchanged':True})
                finally:
                    ro.chmod(0o755)
                    for path in ro.iterdir(): path.chmod(0o644)
            # Preserve the runner's historical sibling layout only in a disposable fixture.
            stage(root/'original',work/'public',True)
            stage(root/'independent_audit',work/'independent_audit')
            obj,out = invoke(work/'independent_audit/run_audit.py')
            need(obj == historical,'Historical independent audit output changed')
            for member in ['CORRECTIONS.patch','CORRECTED_MANIFEST.json','VALIDATION_RECEIPT.json']:
                need(regular(work/'independent_audit'/member) == regular(root/'independent_audit'/member),'Historical replay differs: '+member)
            receipts.append({'mode':label,'suite':'historical_independent_audit','all_child_modes':True,'independent_malformed_cases':23,'independent_rejections':69,'original_defects_reproduced':True,'exact_patch_reproduced':True,'stdout_sha256':sha(out)})
            (work/'public').chmod(0o755)
            for path in (work/'public').iterdir(): path.chmod(0o644)
    need(snapshot(root) == before,'Publication packet changed during replay')
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
        print(json.dumps({'status':'PASS','problem_id':30003533,'publication_manifest_sha256':args.expected_manifest,'bound_files':count,'filesystem_profile':args.filesystem_profile,'check_only':args.check_only,'replays':results,'limits':'Identity and finite diagnostics; not a PDE solution, smooth counterexample, formal proof, human peer review, novelty, or exhaustive literature certification.'},indent=2,sort_keys=True))
    except (RuntimeError,ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: '+str(error),file=sys.stderr); return 1
    return 0

if __name__ == '__main__': sys.exit(main())
