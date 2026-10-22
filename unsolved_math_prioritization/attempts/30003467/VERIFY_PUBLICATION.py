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
    'public': '1f2b1644d763a9c3b87bb391ab135e2501b86458fa36e9d050da544b0e111dbf',
    'audit': '41ed2194464fba3a4945b67fa7fc6314022aa9620b773d81d589ec538e546e33',
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
    need(m['schema'] == 'pseudodisk-prior-negative-publication-v1', 'Wrong schema')
    need(type(m['problem_id']) is int and m['problem_id'] == 30003467 and type(m['rank']) is int and m['rank'] == 998, 'Wrong target')
    need(m['status'] == 'already_solved' and m['turns'] == '0/5', 'Wrong disposition')
    need(m['source_files_redistributed'] is False and m['baseline_file_mode'] == '0644', 'Wrong publication scope/mode')
    need(type(m['frozen_manifest_anchors']) is dict and m['frozen_manifest_anchors'] == FROZEN, 'Wrong frozen anchors')
    need({p.name for p in root.iterdir()} == TOP | set(FROZEN), 'Top-level inventory mismatch')
    count = inventory(root,'PUBLICATION_MANIFEST.json',m['files'],profile)
    for name,pin in FROZEN.items():
        filename = 'MANIFEST.json' if name == 'public' else 'AUDIT_MANIFEST.json'
        raw = regular(root/name/filename); need(sha(raw) == pin, 'Frozen anchor mismatch: '+name)
        inner = load_json(raw)
        fields = {'schema','files'}
        need(type(inner) is dict and set(inner) == fields, 'Invalid inner schema')
        need(type(inner['schema']) is int and inner['schema'] == 1, 'Invalid inner version')
        need(type(inner['files']) is list and len(inner['files']) == (12 if name == 'public' else 4), 'Invalid inner inventory')
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


def replay(root,selected,sources=None):
    before = snapshot(root); receipts = []
    env = {k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    source_state = 'NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES' if sources is None else 'PASS_EXTERNAL_BYTE_PINS_AND_SELECTED_RECORD'
    for label,flags in [('normal',[]),('-O',['-O']),('-OO',['-OO'])]:
        if selected != 'all' and label != selected: continue
        with tempfile.TemporaryDirectory(prefix='pseudodisk-publication-') as temporary:
            work=Path(temporary); packet=work/'readonly-packet'
            readonly_stage(root,packet); ro_before=snapshot(packet)
            blocked=[]
            for path,mode in [(packet/'probe','wb'),(packet/'public/PROOF.md','ab')]:
                try:
                    with path.open(mode): pass
                except PermissionError: blocked.append(True)
                else: blocked.append(False)
            need(blocked == [True,True], 'Read-only probes unexpectedly writable')
            def invoke(script,arguments=()):
                cp=subprocess.run([sys.executable,'-I','-B',*flags,str(script),*map(str,arguments)],cwd=work,env=env,capture_output=True,timeout=300)
                need(cp.returncode == 0, 'Replay failed: '+script.name+': '+cp.stdout.decode(errors='replace')[-1000:]+cp.stderr.decode(errors='replace')[-1000:])
                return load_json(cp.stdout),cp.stdout
            try:
                args=['--expected-manifest',FROZEN['public']]
                if sources is not None: args+=['--source-root',sources]
                obj,out=invoke(packet/'public/verify_packet.py',args)
                need(obj == {'packet':'PASS','bound_files':12,'scope':'credited_prior_negative_resolution','source_verification':source_state,'geometry':'EXTERNAL_PUBLISHED_THEOREM_NOT_RECOMPUTED'}, 'Author verifier receipt differs')
                receipts.append({'mode':label,'suite':'author_verifier','source_verification':source_state,'stdout_sha256':sha(out)})
                # Mutation harnesses edit disposable copies. Stage their input writable;
                # each harness also enforces its own internal read-only relocation.
                harness=work/'harness'; harness.mkdir()
                for name in FROZEN: stage(root/name,harness/name)
                harness_before=snapshot(harness)
                obj,out=invoke(harness/'public/test_packet.py')
                need(obj == load_json(regular(root/'public/TEST_RESULTS.json')), 'Author mutation receipt differs')
                receipts.append({'mode':label,'suite':'author_adverse_controls','rejections':63,'positive_and_readonly_runs':6,'stdout_sha256':sha(out)})
                args=[harness/'public']
                if sources is not None: args+=['--sources',sources]
                obj,out=invoke(harness/'audit/independent_controls.py',args)
                historical=load_json(regular(root/'audit/INDEPENDENT_RESULTS.json'))
                # The historical audit used separately supplied sources. Portable replay
                # omits them honestly rather than reproducing its three source passes.
                expected=dict(historical); expected['source_replay_runs']=0 if sources is None else 3
                need(obj == expected, 'Independent audit receipt differs beyond disclosed source-stage selection')
                receipts.append({'mode':label,'suite':'independent_audit_controls','rejections':81,'positive_runs':3,'enforced_readonly_runs':3,'source_replay_runs':obj['source_replay_runs'],'source_verification':source_state,'math':obj['math'],'stdout_sha256':sha(out)})
                need(snapshot(harness) == harness_before, 'Historical harness changed its input')
                need(snapshot(packet) == ro_before, 'Read-only replay changed packet')
                receipts.append({'mode':label,'profile':'readonly_0444_0555','write_probes_rejected':2,'unchanged':True})
            finally: writable(packet)
    need(snapshot(root) == before, 'Publication packet changed during replay')
    return receipts


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet',type=Path,default=Path(__file__).absolute().parent)
    p.add_argument('--expected-manifest',required=True)
    p.add_argument('--filesystem-profile',choices=['baseline','readonly'],default='baseline')
    p.add_argument('--check-only',action='store_true')
    p.add_argument('--source-root',type=Path,help='Optional separately supplied external source files; never distributed in this packet')
    p.add_argument('--mode',choices=['all','normal','-O','-OO'],default='all')
    args = p.parse_args(); root = args.packet.absolute()
    try:
        count = verify(root,args.expected_manifest,args.filesystem_profile)
        results = [] if args.check_only else replay(root,args.mode,args.source_root.absolute() if args.source_root is not None else None)
        verify(root,args.expected_manifest,args.filesystem_profile)
        print(json.dumps({'status':'PASS','problem_id':30003467,'publication_manifest_sha256':args.expected_manifest,'bound_files':count,'filesystem_profile':args.filesystem_profile,'check_only':args.check_only,'source_verification':'NOT_RUN_CHECK_ONLY' if args.check_only else ('NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES' if args.source_root is None else 'PASS_EXTERNAL_BYTE_PINS_AND_SELECTED_RECORD'),'replays':results,'limits':'Source-free identity and finite diagnostics; not formal proof, human peer review, novelty, or global openness certification.'},indent=2,sort_keys=True))
    except (RuntimeError,ValueError,TypeError,KeyError,OSError,SyntaxError,subprocess.SubprocessError) as error:
        print('REJECT: '+str(error),file=sys.stderr); return 1
    return 0

if __name__ == '__main__': sys.exit(main())
