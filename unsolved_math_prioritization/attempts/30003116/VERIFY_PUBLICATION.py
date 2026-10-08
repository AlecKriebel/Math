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
    'original': 'f0e11096444ac0a676a9e4a8cd267e51bb4600512574eebf961ce5789a03c115',
    'independent_audit': 'c31e73a1f91d61795313bd602583881ef06dbbf03491aa5c995b286bfe6929ee',
    'corrected': '5bad065fa3e8cdce7dc68a7772b66075a124f112648176bb9da417a0b21762b4',
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
    m = load_json(regular(root/'original/MANIFEST.json'))
    patches = {'04_average_collision.md':'MATHEMATICAL_CLARIFICATION.patch',
               'verify_public.py':'OPTIONAL_VALIDATOR_HARDENING.patch'}
    for name in m['files']:
        expected = regular(root/'original'/name)
        if name in patches:
            expected = exact_patch(expected,regular(root/'independent_audit'/patches[name]),name)
            m['files'][name].update(bytes=len(expected),sha256=sha(expected))
        need(regular(root/'corrected'/name) == expected, 'Unexpected corrected bytes: '+name)
    need(regular(root/'corrected/verify_public.py') == regular(root/'independent_audit/verify_public_hardened.py'), 'Hardening candidate mismatch')
    derived = (json.dumps(m,indent=2,sort_keys=True)+'\n').encode()
    need(derived == regular(root/'corrected/MANIFEST.json'), 'Corrected manifest derivation mismatch')


def verify(root, expected, profile='baseline'):
    need(type(expected) is str and HEX.fullmatch(expected) is not None, 'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode), 'Packet root must be real directory')
    raw = regular(root/'PUBLICATION_MANIFEST.json')
    need(sha(raw) == expected, 'Publication manifest anchor mismatch')
    m = load_json(raw)
    need(type(m) is dict and set(m) == {'schema','problem_id','rank','status','turns','source_files_redistributed','frozen_manifest_anchors','baseline_file_mode','files'}, 'Invalid publication schema')
    need(m['schema'] == 'rational-orbit-entropy-publication-v1', 'Wrong publication schema')
    need(type(m['problem_id']) is int and m['problem_id'] == 30003116 and type(m['rank']) is int and m['rank'] == 993, 'Wrong target')
    need(m['status'] == 'unsolved' and m['turns'] == '5/5', 'Wrong disposition')
    need(m['source_files_redistributed'] is False and m['baseline_file_mode'] == '0644', 'Wrong publication scope/mode')
    need(m['frozen_manifest_anchors'] == FROZEN, 'Wrong frozen anchors')
    need({p.name for p in root.iterdir()} == TOP | set(FROZEN), 'Top-level inventory mismatch')
    count = inventory(root,'PUBLICATION_MANIFEST.json',m['files'],profile)
    for name,pin in FROZEN.items():
        raw = regular(root/name/'MANIFEST.json'); need(sha(raw) == pin, 'Frozen anchor mismatch: '+name)
        inner = load_json(raw)
        fields = {'format','problem_id','exceptions','files'}
        if name == 'independent_audit': fields.add('original_manifest_sha256')
        need(type(inner) is dict and set(inner) == fields, 'Invalid inner schema')
        fmt = 'rational-orbit-independent-audit-v1' if name == 'independent_audit' else 'rational-orbit-entropy-v1'
        need(inner['format'] == fmt and type(inner['problem_id']) is int and inner['problem_id'] == 30003116, 'Wrong inner target/schema')
        need(inner['exceptions'] == ['MANIFEST.json'], 'Wrong inner exceptions')
        if name == 'independent_audit': need(inner['original_manifest_sha256'] == FROZEN['original'], 'Wrong original anchor in audit')
        need(type(inner['files']) is dict and len(inner['files']) == 12, 'Invalid inner inventory')
        items = []
        for filename,item in inner['files'].items():
            need(type(item) is dict and set(item) == {'bytes','sha256','mode'}, 'Invalid inner record')
            items.append(dict(path=filename,**item))
        inventory(root/name,'MANIFEST.json',items,profile,flat=True)
    for path in root.rglob('*.json'): load_json(regular(path))
    for path in root.rglob('*.py'):
        need(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(regular(path)))), 'Optimization-removable check: '+path.name)
    correction(root)
    return count


def snapshot(root):
    return {p.relative_to(root).as_posix():(stat.S_IMODE(p.lstat().st_mode),sha(regular(p)) if p.is_file() else None) for p in [root,*root.rglob('*')]}


def stage(source,destination):
    shutil.copytree(source,destination)
    destination.chmod(0o755)
    for p in destination.rglob('*'): p.chmod(0o755 if p.is_dir() else 0o644)


def replay(root,selected):
    before = snapshot(root); receipts = []
    env = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for label,flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        if selected != 'all' and label != selected: continue
        with tempfile.TemporaryDirectory(prefix='rational-orbit-publication-') as temporary:
            work = Path(temporary)
            for name in FROZEN: stage(root/name,work/name)
            def invoke(script,extra=()):
                cp = subprocess.run([sys.executable,'-I','-B',*flags,str(script),*map(str,extra)],cwd=work,env=env,capture_output=True,timeout=240)
                need(cp.returncode == 0,'Replay failed: '+script.name+': '+cp.stdout.decode(errors='replace')[-2000:]+cp.stderr.decode(errors='replace')[-1000:])
                obj = load_json(cp.stdout); need(obj['status'] == 'PASS','Replay status mismatch')
                return obj,cp.stdout
            for name,pin in FROZEN.items():
                script = 'verify_audit.py' if name == 'independent_audit' else 'verify_public.py'
                obj,out = invoke(work/name/script,['--expected-manifest',pin])
                key,total = ('independent_checks',38715) if name == 'independent_audit' else ('checks',86778)
                need(obj[key] == total,'Replay count mismatch')
                receipts.append({'mode':label,'slice':name,'profile':'baseline_0644','manifest_sha256':pin,'checks':total,'stdout_sha256':sha(out)})
            obj,out = invoke(work/'original/test_negative_controls.py',['--expected-manifest',FROZEN['original']])
            need(obj == load_json(regular(root/'independent_audit/original_controls_replayed.json')),'Historical author control output mismatch')
            receipts.append({'mode':label,'suite':'original_negative_controls','all_child_modes':True,'math_rejections':21,'packet_rejections':30,'stdout_sha256':sha(out)})
            obj,out = invoke(work/'independent_audit/independent_packet_controls.py',['--packet',work/'original','--expected-manifest',FROZEN['original'],'--hardened',work/'independent_audit/verify_public_hardened.py'])
            need(obj == load_json(regular(root/'independent_audit/independent_packet_results.json')),'Historical independent packet control output mismatch')
            receipts.append({'mode':label,'suite':'independent_packet_controls','all_child_modes':True,'cases':obj['cases'],'stdout_sha256':sha(out)})
            # Native verifiers bind modes. A read-only fixture has a DIFFERENT manifest
            # and external pin. This never changes the frozen original or its anchor.
            for name in FROZEN:
                ro = work/(name+'_readonly'); stage(root/name,ro)
                m = load_json(regular(ro/'MANIFEST.json'))
                for item in m['files'].values(): item['mode'] = '0444'
                raw = (json.dumps(m,sort_keys=True,indent=2)+'\n').encode(); (ro/'MANIFEST.json').write_bytes(raw)
                pin = sha(raw); need(pin != FROZEN[name],'Read-only fixture incorrectly reused baseline pin')
                for p in ro.iterdir(): p.chmod(0o444)
                ro.chmod(0o555); ro_before = snapshot(ro); blocked = False
                try:
                    with (ro/'README.md').open('ab'): pass
                except PermissionError: blocked = True
                need(blocked,'Read-only fixture writable')
                try:
                    script = 'verify_audit.py' if name == 'independent_audit' else 'verify_public.py'
                    obj,out = invoke(ro/script,['--expected-manifest',pin])
                    need(snapshot(ro) == ro_before,'Read-only fixture changed')
                    receipts.append({'mode':label,'slice':name,'profile':'readonly_0444_re_pinned_fixture','baseline_manifest_sha256':FROZEN[name],'fixture_manifest_sha256':pin,'write_blocked':True,'unchanged':True,'stdout_sha256':sha(out)})
                finally:
                    ro.chmod(0o755)
                    for p in ro.iterdir(): p.chmod(0o644)
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
        print(json.dumps({'status':'PASS','problem_id':30003116,'publication_manifest_sha256':args.expected_manifest,'bound_files':count,'filesystem_profile':args.filesystem_profile,'check_only':args.check_only,'replays':results,'limits':'Source-free identity and finite diagnostics; not formal proof, human peer review, novelty, or global openness certification.'},indent=2,sort_keys=True))
    except (RuntimeError,ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: '+str(error),file=sys.stderr); return 1
    return 0

if __name__ == '__main__': sys.exit(main())
