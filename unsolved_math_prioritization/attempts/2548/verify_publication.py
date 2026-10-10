#!/usr/bin/env python3
"""Strict, portable integrity and unoptimized replay of scoped KOU-21.39 partials."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

PINS = {'author': 'e618e640ee11d95fe411e007e34a3c851f31420e7e0ce33e37db6c4a4f5c0429',
        'audit': 'cc853e653dbaf5b5f2c57a9d9d46237e3e66bece4d96892ec570c3b2675c424e'}
OPTIONAL_COUNTS = {'source_pdf_signature': 4, 'source_pdf_hash_size': 4,
                   'dataset_hash_size': 3, 'dataset_exact_target_identity': 2,
                   'catalog_rank': 1, 'catalog_git_blob_hash': 1,
                   'research_exact_target_absent': 1}

def require(value, message):
    if not value:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root):
    require(root.is_dir() and not root.is_symlink(), 'Invalid directory')
    out = set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlink is forbidden: '+str(p))
        require(p.is_dir() or p.is_file(), 'Nonregular member')
        if p.is_file():
            out.add(p.relative_to(root).as_posix())
    return out

def check_manifest(root, name, pin=None):
    raw=(root/name).read_bytes()
    if pin:
        require(sha(raw)==pin, 'Frozen manifest pin mismatch')
    m=json.loads(raw); expected={name}
    for rec in m['files']:
        s=rec['path']; p=PurePosixPath(s)
        require(not p.is_absolute() and '..' not in p.parts and str(p)==s and s not in expected,
                'Unsafe or duplicate manifest entry')
        expected.add(s)
        f=root/s
        require(f.is_file() and not f.is_symlink(), 'Missing or nonregular file: '+s)
        b=f.read_bytes()
        require(len(b)==rec['bytes'] and sha(b)==rec['sha256'], 'Content mismatch: '+s)
    require(inventory(root)==expected, 'Unexpected file inventory')
    return m

def verify(root):
    m=check_manifest(root,'PUBLICATION_MANIFEST.json')
    require(m['problem_id']==2548 and m['status']=='unsolved' and m['turns']=='5/5','Publication scope')
    binding=json.loads((root/'BINDING.json').read_bytes())
    require(binding['original_problem_solved'] is False and binding['required_corrections']==[], 'Binding scope')
    for group,name in [('author','AUTHOR_MANIFEST.json'),('audit','AUDIT_MANIFEST.json')]:
        require(binding[group+'_manifest_sha256']==PINS[group],'Binding pin')
        check_manifest(root/group,name,PINS[group])
        with zipfile.ZipFile(root/(group+'_frozen.zip')) as z:
            names=z.namelist()
            require(len(names)==len(set(names)) and set(names)==inventory(root/group),'ZIP inventory')
            require(names==sorted(names),'ZIP ordering')
            for info in z.infolist():
                require(not info.is_dir() and info.compress_type==zipfile.ZIP_STORED,'ZIP regular storage')
                require(info.date_time==(1980,1,1,0,0,0),'ZIP fixed timestamp')
                require(info.create_system==3 and info.external_attr>>16==0o100644,'ZIP mode')
                require(z.read(info)==(root/group/info.filename).read_bytes(),'ZIP member bytes')
    return {'status':'PASS','publication_files':len(m['files'])+1,
            'author_frozen_files':10,'audit_frozen_files':8,'zip_archives_verified':2,
            'original_problem_solved':False,'turns':'5/5',
            'publication_manifest_sha256':sha((root/'PUBLICATION_MANIFEST.json').read_bytes())}

def run(script, *args):
    env=os.environ.copy()
    for name in list(env):
        if name.startswith('PYTHON'):
            del env[name]
    p=subprocess.run([sys.executable,'-I','-B',str(script),*map(str,args)],
                     cwd=script.parent,env=env,capture_output=True,timeout=600)
    require(p.returncode==0, 'Replay failed: '+script.name+' '+p.stderr.decode(errors='replace'))
    require(not p.stderr,'Unexpected replay stderr: '+script.name)
    return p.stdout

def replay(root):
    with tempfile.TemporaryDirectory(prefix='kourovka-2139-replay-') as td:
        dst=Path(td)/'relocated'; shutil.copytree(root,dst)
        verify(dst)
        author=run(dst/'author/verify_math.py')
        require(author==(dst/'author/CHECK_RESULTS.json').read_bytes(),'Author byte-exact replay')
        ar=json.loads(author)
        require(ar['total_assertions']==sum(ar['assertion_counts'].values())==116329,'Author count')
        run(dst/'author/verify_manifest.py'); run(dst/'audit/verify_audit_manifest.py')
        independent=run(dst/'audit/independent_verify.py','--author',dst/'author')
        actual=json.loads(independent)
        expected=json.loads((dst/'audit/INDEPENDENT_RESULTS.json').read_bytes())
        require(expected['total_independent_assertions']==2138878,'Historical full count')
        for key,count in OPTIONAL_COUNTS.items():
            require(expected['assertion_counts'].pop(key)==count,'Optional count: '+key)
        expected['total_independent_assertions']-=sum(OPTIONAL_COUNTS.values())
        expected['optional_source_checks']={}
        require(expected==actual,'Independent portable results mismatch')
        require(actual['total_independent_assertions']==sum(actual['assertion_counts'].values())==2138862,
                'Independent portable count')
        verify(dst)
        return {'status':'PASS','unoptimized_isolated_subprocesses':True,'relocated_temporary_copy':True,
                'author_assertions':116329,'author_byte_exact':True,
                'independent_portable_assertions':2138862,'all_non_source_results_match':True,
                'optional_source_metadata_assertions_not_replayed':16,
                'author_output_sha256':sha(author),'independent_portable_output_sha256':sha(independent),
                'frozen_inventory_unchanged_after_replay':True}

def main():
    require(sys.flags.optimize==0 and __debug__, 'Optimized execution is not accepted as verification')
    ap=argparse.ArgumentParser(); ap.add_argument('--replay',action='store_true'); args=ap.parse_args()
    root=Path(__file__).resolve().parent
    result=verify(root)
    if args.replay:
        result['replay']=replay(root)
        verify(root)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
