#!/usr/bin/env python3
"""Externally authenticate this wrapper and independently pin the manifest.
Source-free artifact identity and finite diagnostics; topology requires mathematical review.
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
    'original': 'd1e1467c6d36b6c62283af2ec50ddff8864020ad8a7c9e0ba9a6704dacb4246a',
    'audit1': '599456c9e8acb599c226aa7175aede3e72fb50241a83d1937cbc09c1a227f009',
    'audit2': '0347538b88fcc15d20816d96bc901b492938492084174749e6e8463905c1ff2a',
}
TOP = {'README.md','PUBLICATION_ACCEPTANCE.md','RESEARCH_LOG.md','VERIFY_PUBLICATION.py',
       'BOOTSTRAP.py','TEST_MUTATIONS.py','MUTATION_RESULTS.json','PUBLICATION_MANIFEST.json','AUDIT2_FREEZE_RECEIPT.json'}

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
    need(type(expected) is str and HEX.fullmatch(expected) is not None,'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode),'Packet root must be real directory')
    raw = regular(root/'PUBLICATION_MANIFEST.json')
    need(sha(raw) == expected,'Publication manifest anchor mismatch')
    m = load_json(raw)
    need(type(m) is dict and set(m) == {'schema','problem_id','rank','status','turns','source_files_redistributed','frozen_manifest_anchors','baseline_file_mode','files'},'Invalid publication schema')
    need(type(m['schema']) is str and m['schema'] == 'derived-pure-braid-publication-v1','Wrong publication schema')
    need(type(m['problem_id']) is int and m['problem_id'] == 30003634 and type(m['rank']) is int and m['rank'] == 1002,'Wrong target')
    need(type(m['status']) is str and m['status'] == 'claimed_solved' and type(m['turns']) is str and m['turns'] == '1/5','Wrong disposition')
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
        manifest_name = 'AUDIT_MANIFEST.json' if name == 'audit1' else 'MANIFEST.json'
        raw = regular(root/name/manifest_name); need(sha(raw) == pin,'Frozen anchor mismatch: '+name)
        inner = load_json(raw)
        need(type(inner) is dict and type(inner['files']) is list,'Invalid inner manifest')
        need(type(inner['problem_id']) is int and inner['problem_id'] == 30003634,'Inner target')
        need(len(inner['files']) == {'original':11,'audit1':8,'audit2':13}[name],'Inner file count')
        if name != 'original': need(inner['author_manifest_sha256'] == FROZEN['original'],'Audit author identity')
        items = []
        for item in inner['files']:
            need(type(item) is dict and set(item) == {'path','bytes','sha256'},'Invalid inner member')
            items.append(dict(item,mode='0644'))
        inventory(root/name,manifest_name,items,profile,flat=True)
    a1=load_json(regular(root/'audit1/ACCEPTANCE.json')); a2=load_json(regular(root/'audit2/ACCEPTANCE.json'))
    need(a1['status']=='ACCEPTED_NO_REQUIRED_MATHEMATICAL_CORRECTION' and a1['required_corrections']==[],'First audit verdict')
    need(a2['decision']=='ACCEPT' and a2['required_proof_corrections']==[] and a2['mathematical_blockers']==[],'Second audit verdict')
    receipt=load_json(regular(root/'AUDIT2_FREEZE_RECEIPT.json'))
    need(receipt['audit_manifest_sha256']==FROZEN['audit2'] and receipt['archive_sha256']=='55ddfe94d05eef7e04a7d20e84d9ddfa7e8e22cf341d4038610e1d8023c3bd44','Freeze receipt mismatch')
    need(sha(regular(root/'AUDIT2_FREEZE_RECEIPT.json')) == 'cf226445fa2dd3788e5881f0d9fb8d6f7a4636abd674f59fe311daa48bb312d7','Freeze receipt anchor')
    for path in root.rglob('*.json'): load_json(regular(path))
    for path in root.rglob('*.py'):
        need(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse(regular(path)))),'Optimization-removable check: '+path.name)
    return count


def snapshot(root):
    return {p.relative_to(root).as_posix():(stat.S_IMODE(p.lstat().st_mode),sha(regular(p)) if p.is_file() else None) for p in [root,*root.rglob('*')]}


def stage(source,destination,readonly=False):
    shutil.copytree(source,destination)
    for p in destination.rglob('*'): p.chmod(0o555 if p.is_dir() and readonly else 0o755 if p.is_dir() else 0o444 if readonly else 0o644)
    destination.chmod(0o555 if readonly else 0o755)


def replay(root,selected):
    before=snapshot(root); receipts=[]
    env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')};env['PYTHONDONTWRITEBYTECODE']='1'
    for label,flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        if selected != 'all' and label != selected: continue
        with tempfile.TemporaryDirectory(prefix='pure-braid-publication-') as temporary:
            work=Path(temporary);cwd=work/'unrelated';cwd.mkdir()
            for name in FROZEN:stage(root/name,work/name,True)
            rb={name:snapshot(work/name) for name in FROZEN}
            blocked=False
            try:
                with (work/'original/PROOF.md').open('ab'):pass
            except PermissionError:blocked=True
            need(blocked,'Read-only fixture writable; run unprivileged')
            def invoke(script,extra,expected,version_metadata=False):
                cp=subprocess.run([sys.executable,'-I','-B',*flags,str(script),*map(str,extra)],cwd=cwd,env=env,capture_output=True,timeout=300)
                need(cp.returncode==0 and not cp.stderr,'Replay failed: '+script.name+': '+cp.stderr.decode(errors='replace')[-2000:])
                got=load_json(cp.stdout);want=load_json(regular(expected))
                if version_metadata:
                    # Python version is descriptive environment metadata only.
                    got.pop('python_version',None);want.pop('python_version',None)
                need(got==want,'Saved exact output mismatch: '+script.name)
                receipts.append({'mode':label,'suite':str(script.relative_to(work)),'stdout_sha256':sha(cp.stdout),'saved_result_matched':True})
            try:
                invoke(work/'original/verify.py',[],root/'original/VERIFY_OUTPUT.json')
                invoke(work/'audit1/recovery_controls.py',['--packet',work/'original'],root/'audit1/RECOVERY_CONTROLS.json',True)
                invoke(work/'audit2/recovery_controls.py',['--author-packet',work/'original'],root/'audit2/RECOVERY_CONTROLS.json')
                if label=='normal':
                    invoke(work/'original/test_replay.py',[],root/'original/TEST_REPORT.json')
                    invoke(work/'audit2/test_second_audit_replay.py',['--author-packet',work/'original'],root/'audit2/PORTABLE_REPLAY.json')
                need(all(snapshot(work/name)==rb[name] for name in FROZEN),'Read-only bytes/modes changed')
                receipts.append({'mode':label,'suite':'genuine_readonly_relocation','write_blocked':True,'all_bytes_modes_unchanged':True})
            finally:
                for name in FROZEN:
                    (work/name).chmod(0o755)
                    for path in (work/name).rglob('*'):path.chmod(0o755 if path.is_dir() else 0o644)
    need(snapshot(root)==before,'Publication packet changed')
    return receipts


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',type=Path,default=Path(__file__).absolute().parent)
    p.add_argument('--expected-manifest',required=True)
    p.add_argument('--filesystem-profile',choices=['baseline','readonly'],default='baseline')
    p.add_argument('--check-only',action='store_true')
    p.add_argument('--mode',choices=['all','normal','-O','-OO'],default='all')
    a=p.parse_args();root=a.packet.absolute()
    try:
        count=verify(root,a.expected_manifest,a.filesystem_profile)
        results=[] if a.check_only else replay(root,a.mode)
        verify(root,a.expected_manifest,a.filesystem_profile)
        print(json.dumps({'status':'PASS','problem_id':30003634,'publication_manifest_sha256':a.expected_manifest,'bound_files':count,'filesystem_profile':a.filesystem_profile,'check_only':a.check_only,'replays':results,'limits':'Identity and finite diagnostics; not formal topology verification, human peer review, novelty, exhaustive literature certification or a separate failure claim at every higher n.'},indent=2,sort_keys=True))
    except (RuntimeError,ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: '+str(error),file=sys.stderr);return 1
    return 0
if __name__=='__main__':sys.exit(main())
