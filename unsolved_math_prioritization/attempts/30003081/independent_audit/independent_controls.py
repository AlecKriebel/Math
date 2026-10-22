#!/usr/bin/env python3
"""Adversarial checks of the pinned author's verifier; no changes to author originals."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PIN = '7cec8ef8716ab0e930d6c03f2cd4d8559214d9329ccde8ef258cd9a8d3c7ae55'
VERIFIER = '629cc9238c6c8ec49257c8f42fcdc0946f9561978a4ebbe2c9b9a3149b651884'

def require(value, message):
    if not value:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def snapshot(root):
    return {p.name: {'bytes':p.stat().st_size,'sha256':digest(p)} for p in root.iterdir()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author-root', required=True, type=Path)
    args = parser.parse_args()
    original = args.author_root.resolve()
    trusted = original / 'verify_packet.py'
    require(digest(original/'MANIFEST.json') == PIN, 'unrecognized author manifest')
    require(digest(trusted) == VERIFIER, 'unrecognized author verifier')
    before = snapshot(original)
    names = ['null_manifest','array_manifest','number_manifest','missing_schema','extra_top_field','bad_schema',
             'files_null','files_string','entry_null','entry_array','entry_extra_field','missing_entry_field',
             'duplicate_entry','boolean_size','negative_size','float_size','string_size','bad_digest_length',
             'uppercase_digest','nonstring_path','absolute_path','parent_path','backslash_path','dot_path',
             'empty_path','unicode_path','duplicate_json_key','invalid_json','invalid_utf8',
             'manifest_symlink','member_symlink','broken_symlink','member_directory','fifo_member',
             'unexpected_directory','unexpected_file','missing_math','root_symlink','root_file','injected_assert',
             'syntax_error','replay_output_mismatch']
    reports = []
    with tempfile.TemporaryDirectory(prefix='independent-logarithmic-audit-') as td:
        base = Path(td)
        for mode in range(3):
            flags = [] if mode == 0 else ['-O' if mode == 1 else '-OO']
            def invoke(root, pin):
                return subprocess.run([sys.executable,*flags,'-I','-B',str(trusted),'--root',str(root),
                    '--manifest-sha256',pin],cwd=base,capture_output=True,timeout=60)
            clean = base / ('clean'+str(mode))
            shutil.copytree(original, clean)
            result = invoke(clean,PIN)
            require(result.returncode == 0, 'clean relocation failed')
            require(json.loads(result.stdout)['optimization'] == mode, 'wrong optimization mode')
            failures = []
            for name in names:
                root = base / (str(mode)+'-'+name)
                shutil.copytree(original,root)
                path = root/'MANIFEST.json'
                manifest = json.loads(path.read_text())
                entry = manifest['files'][0]
                repin = True
                if name == 'null_manifest': manifest = None
                elif name == 'array_manifest': manifest = []
                elif name == 'number_manifest': manifest = 7
                elif name == 'missing_schema': del manifest['schema']
                elif name == 'extra_top_field': manifest['extra'] = True
                elif name == 'bad_schema': manifest['schema'] = 'unknown'
                elif name == 'files_null': manifest['files'] = None
                elif name == 'files_string': manifest['files'] = 'files'
                elif name == 'entry_null': manifest['files'][0] = None
                elif name == 'entry_array': manifest['files'][0] = []
                elif name == 'entry_extra_field': entry['extra'] = 1
                elif name == 'missing_entry_field': del entry['bytes']
                elif name == 'duplicate_entry': manifest['files'].append(dict(entry))
                elif name == 'boolean_size': entry['bytes'] = True
                elif name == 'negative_size': entry['bytes'] = -1
                elif name == 'float_size': entry['bytes'] = float(entry['bytes'])
                elif name == 'string_size': entry['bytes'] = str(entry['bytes'])
                elif name == 'bad_digest_length': entry['sha256'] = '0'*63
                elif name == 'uppercase_digest': entry['sha256'] = entry['sha256'].upper()
                elif name == 'nonstring_path': entry['path'] = 4
                elif name == 'absolute_path': entry['path'] = '/tmp/payload'
                elif name == 'parent_path': entry['path'] = '../payload'
                elif name == 'backslash_path': entry['path'] = '..\\payload'
                elif name == 'dot_path': entry['path'] = '.'
                elif name == 'empty_path': entry['path'] = ''
                elif name == 'unicode_path': entry['path'] = '\u2603.md'
                elif name == 'duplicate_json_key':
                    path.write_text('{"schema":"source-free-flat-v1",'+path.read_text()[1:]);repin=False
                elif name == 'invalid_json': path.write_text('{');repin=False
                elif name == 'invalid_utf8': path.write_bytes(b'\xff');repin=False
                elif name == 'manifest_symlink': path.unlink();path.symlink_to(original/'MANIFEST.json');repin=False
                elif name in ('member_symlink','broken_symlink','member_directory','fifo_member'):
                    item=root/entry['path'];item.unlink()
                    if name == 'member_symlink': item.symlink_to(original/entry['path'])
                    elif name == 'broken_symlink': item.symlink_to(root/'absent')
                    elif name == 'member_directory': item.mkdir()
                    else: os.mkfifo(item)
                elif name == 'unexpected_directory': (root/'extra').mkdir()
                elif name == 'unexpected_file': (root/'extra').write_text('x')
                elif name == 'missing_math': (root/'check_math.py').unlink()
                elif name == 'root_symlink':
                    alternate=base/(str(mode)+'-root-link');alternate.symlink_to(root,target_is_directory=True);root=alternate
                elif name == 'root_file':
                    alternate=base/(str(mode)+'-root-plain');alternate.write_text('x');root=alternate
                elif name in ('injected_assert','syntax_error','replay_output_mismatch'):
                    item=root/('MATH_RESULTS.json' if name=='replay_output_mismatch' else 'check_math.py')
                    addition = b'\n' if name=='replay_output_mismatch' else b'\nassert True\n' if name=='injected_assert' else b'\ndef invalid syntax\n'
                    item.write_bytes(item.read_bytes()+addition)
                    for row in manifest['files']:
                        if row['path'] == item.name:
                            row['bytes']=item.stat().st_size;row['sha256']=digest(item)
                if repin: path.write_text(json.dumps(manifest))
                pin=digest(path)
                result=invoke(root,pin)
                require(result.returncode != 0, 'accepted malformed case '+name+' at '+str(mode))
                failures.append({'case':name,'returncode':result.returncode,'explicit_reject':result.stderr.startswith(b'REJECT:')})
            math=Path(__file__).resolve().parent/'independent_math.py'
            result=subprocess.run([sys.executable,*flags,'-I','-B',str(math)],cwd=base,capture_output=True,timeout=60)
            require(result.returncode == 0,'independent math failed')
            math_controls=[]
            for control in ['surjection','codimension','chern','torsion']:
                result=subprocess.run([sys.executable,*flags,'-I','-B',str(math),'--false-control',control],
                    cwd=base,capture_output=True,timeout=60)
                require(result.returncode != 0 and b'AuditFailure' in result.stderr,'false control not rejected correctly: '+control)
                math_controls.append(control)
            reports.append({'optimization':mode,'clean_relocation':'PASS','integrity_cases':failures,
                            'mathematical_false_controls_rejected':math_controls,'independent_math':'PASS'})
    require(before == snapshot(original),'author original changed')
    print(json.dumps({'status':'PASS','author_original_unchanged':True,'tested_manifest_sha256':PIN,
        'runs':reports,'limits':'Targeted fail-closed checks, not a general hostile-code, filesystem-race or resource-exhaustion guarantee.'},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
