#!/usr/bin/env python3
"""Three-mode hostile-input, integrity, and read-only checks of a pinned bundle.

Temporary copies are removed at exit. The original bundle is never edited.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

MODES = [('normal', []), ('optimized', ['-O']), ('double_optimized', ['-OO'])]


def check(ok,message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script, extra, mode, expected=0, cwd=None):
    cp = subprocess.run([sys.executable,*mode,'-B',str(script),*map(str,extra)],
                        capture_output=True,text=True,cwd=cwd,timeout=90)
    check(cp.returncode == expected, 'unexpected exit status for '+Path(script).name+': '+str(cp.returncode))
    return cp.stdout


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('bundle',type=Path)
    ap.add_argument('--manifest-sha256',required=True)
    ap.add_argument('--verifier-sha256',required=True)
    args=ap.parse_args()
    bundle=args.bundle.absolute()
    check(not bundle.is_symlink(),'linked original root')
    check(digest(bundle/'MANIFEST.json') == args.manifest_sha256,'external manifest pin mismatch')
    check(digest(bundle/'verify.py') == args.verifier_sha256,'external verifier pin mismatch')
    before={p.name:digest(p) for p in bundle.iterdir()}
    for _,mode in MODES:
        run(bundle/'verify.py',[bundle,'--manifest-sha256',args.manifest_sha256],mode)
    authors=[run(bundle/'audit.py',[],mode) for _,mode in MODES]
    check(len(set(authors)) == 1,'original three-mode output mismatch')
    independent=Path(__file__).absolute().with_name('independent_audit.py')
    more=[run(independent,[bundle,'--manifest-sha256',args.manifest_sha256,
            '--verifier-sha256',args.verifier_sha256],mode) for _,mode in MODES]
    check(len(set(more)) == 1,'independent three-mode output mismatch')
    hostile=[]
    for field in ('p','q'):
        for value in (True,False,None,1.0,0.0,'1',[],{},[1],{'n':1}):
            obj={'p':1,'q':1};obj[field]=value
            hostile.append(json.dumps(obj))
    hostile.extend([
        '{"p":0,"q":1}', '{"p":1,"q":0}', '{"p":1,"q":-1}',
        '{"p":6,"q":2}', '{"p":-6,"q":2}', '{"p":100001,"q":1}',
        '{"p":-100001,"q":1}', '{"p":1,"q":100001}',
        '{"p":1,"q":1,"extra":false}', '{"p":1,"q":1,"q":1}',
        '{"p":1,"p":1,"q":1}', '{"p":1}', '{"q":1}', '{}', '[]',
        'null','true','1','"1"','{','',
        '{"p":NaN,"q":1}', '{"p":Infinity,"q":1}', '{"p":-Infinity,"q":1}',
        '{"p":1e309,"q":1}', '{"p":1,"q":1e309}',
        '{"p":'+('9'*5000)+',"q":1}',
        '{"p":1,"q":'+('9'*5000)+'}',
        '{"p":1,"q":1} trailing', '{"p":1,"q":1}\n{}',
        '{"p":'+('['*100)+'1'+(']'*100)+',"q":1}',
    ])
    for item in hostile:
        for _,mode in MODES:
            run(bundle/'audit.py',['--slope-json',item],mode,expected=2)
    cases=[]
    # Original pins for byte alterations; locally recomputed pins only to enter schema branches.
    with tempfile.TemporaryDirectory(prefix='su2-independent-controls-') as td:
        td=Path(td)
        for case in ['content_bitflip','deleted_payload','extra_file','extra_directory',
                     'payload_symlink','manifest_symlink','root_symlink','zero_pin','uppercase_pin',
                     'short_pin','nonhex_pin','empty_pin','invalid_json','duplicate_json_key',
                     'wrong_top_type','extra_manifest_key','wrong_format','files_not_list',
                     'empty_files','too_many_files','entry_not_object','entry_extra_key',
                     'entry_missing_key','name_parent','name_absolute','name_separator',
                     'name_dot','name_empty','name_reserved','duplicate_entry',
                     'bytes_bool','bytes_float','bytes_negative','bytes_over_limit',
                     'bytes_infinity','sha_not_string','sha_uppercase','sha_short',
                     'bad_payload_size','bad_payload_hash','oversized_manifest']:
            root=td/case;shutil.copytree(bundle,root)
            pin=args.manifest_sha256
            actual=root
            m=json.loads((root/'MANIFEST.json').read_text())
            change=False
            if case == 'content_bitflip': (root/'REPORT.md').write_bytes((root/'REPORT.md').read_bytes()+b'x')
            elif case == 'deleted_payload': (root/'README.md').unlink()
            elif case == 'extra_file': (root/'extra.txt').write_text('extra')
            elif case == 'extra_directory': (root/'extra').mkdir()
            elif case == 'payload_symlink':
                (root/'README.md').unlink();(root/'README.md').symlink_to(bundle/'README.md')
            elif case == 'manifest_symlink':
                (root/'MANIFEST.json').unlink();(root/'MANIFEST.json').symlink_to(bundle/'MANIFEST.json')
            elif case == 'root_symlink':
                actual=td/'linked_root';actual.symlink_to(root,target_is_directory=True)
            elif case == 'zero_pin': pin='0'*64
            elif case == 'uppercase_pin': pin=pin.upper()
            elif case == 'short_pin': pin=pin[:-1]
            elif case == 'nonhex_pin': pin='g'*64
            elif case == 'empty_pin': pin=''
            elif case == 'invalid_json':
                (root/'MANIFEST.json').write_text('{');pin=digest(root/'MANIFEST.json')
            elif case == 'duplicate_json_key':
                (root/'MANIFEST.json').write_text('{"format":"su2-surgery-audit-v1","format":"su2-surgery-audit-v1","files":[]}');pin=digest(root/'MANIFEST.json')
            elif case == 'oversized_manifest':
                (root/'MANIFEST.json').write_text(' '*65537);pin=digest(root/'MANIFEST.json')
            else:
                change=True
                if case == 'wrong_top_type': m=[]
                elif case == 'extra_manifest_key': m['extra']=1
                elif case == 'wrong_format': m['format']='su2-surgery-audit-v2'
                elif case == 'files_not_list': m['files']={}
                elif case == 'empty_files': m['files']=[]
                elif case == 'too_many_files': m['files']=m['files']*3
                elif case == 'entry_not_object': m['files'][0]=[]
                elif case == 'entry_extra_key': m['files'][0]['extra']=1
                elif case == 'entry_missing_key': del m['files'][0]['sha256']
                elif case.startswith('name_'):
                    m['files'][0]['name']={'name_parent':'../REPORT.md','name_absolute':'/tmp/x',
                        'name_separator':'sub/x','name_dot':'.','name_empty':'','name_reserved':'MANIFEST.json'}[case]
                elif case == 'duplicate_entry': m['files'].append(m['files'][0])
                elif case.startswith('bytes_'):
                    m['files'][0]['bytes']={'bytes_bool':True,'bytes_float':1897.0,
                        'bytes_negative':-1,'bytes_over_limit':2000001,'bytes_infinity':float('inf')}[case]
                elif case.startswith('sha_'):
                    m['files'][0]['sha256']={'sha_not_string':1,'sha_uppercase':m['files'][0]['sha256'].upper(),'sha_short':'a'*63}[case]
                elif case == 'bad_payload_size': m['files'][0]['bytes']+=1
                elif case == 'bad_payload_hash': m['files'][0]['sha256']='0'*64
                else: raise ValueError('unknown mutation')
            if change:
                (root/'MANIFEST.json').write_text(json.dumps(m));pin=digest(root/'MANIFEST.json')
            for _,mode in MODES:
                run(bundle/'verify.py',[actual,'--manifest-sha256',pin],mode,expected=2)
            cases.append(case)
        ro=td/'readonly';shutil.copytree(bundle,ro)
        for p in ro.iterdir():p.chmod(0o444)
        ro.chmod(0o555)
        check(os.geteuid()!=0,'read-only test requires nonroot')
        blocked=False
        try:
            try:(ro/'forbidden-write').write_text('x')
            except PermissionError:blocked=True
            check(blocked,'read-only permission challenge failed')
            ro_before={p.name:digest(p) for p in ro.iterdir()}
            for _,mode in MODES:
                run(ro/'audit.py',[],mode,cwd=ro)
                run(ro/'verify.py',['.','--manifest-sha256',args.manifest_sha256],mode,cwd=ro)
                run(independent,[ro,'--manifest-sha256',args.manifest_sha256,
                    '--verifier-sha256',args.verifier_sha256],mode,cwd=ro)
            check(ro_before == {p.name:digest(p) for p in ro.iterdir()},'read-only snapshot changed')
        finally:
            ro.chmod(0o755)
            for p in ro.iterdir():p.chmod(0o644)
    check(before == {p.name:digest(p) for p in bundle.iterdir()},'original bundle changed')
    print(json.dumps({'status':'passed','modes':[name for name,_ in MODES],
        'author_outputs_identical':True,'independent_outputs_identical':True,
        'author_math':json.loads(authors[0]),'independent_math':json.loads(more[0]),
        'hostile_slope_cases_per_mode':len(hostile),'integrity_cases_per_mode':len(cases),
        'integrity_cases':cases,'read_only_nonroot':{'uid':os.geteuid(),
        'directory_mode':'0555','file_mode':'0444','write_denial_verified':True,
        'author_math_author_verifier_independent_math_all_three_modes':True},
        'original_unchanged':True,'scope':'static fixed-bundle parser, arithmetic, hash, and permission controls; no hostile-filesystem race safety or theorem certification'},indent=2,sort_keys=True))

if __name__ == '__main__':main()
