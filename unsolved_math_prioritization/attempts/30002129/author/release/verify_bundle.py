#!/usr/bin/env python3
"""Strict flat inventory verifier; external manifest digest is the trust anchor."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys, tempfile

def sha(data):return hashlib.sha256(data).hexdigest()
def verify(root, expected):
    mp=root/'MANIFEST.json'
    if mp.is_symlink() or not mp.is_file():raise ValueError('manifest missing or symlink')
    raw=mp.read_bytes()
    if sha(raw)!=expected:raise ValueError('manifest binding mismatch')
    obj=json.loads(raw)
    files=obj['files']
    paths=[x['path'] for x in files]
    if len(paths)!=len(set(paths)) or any(pathlib.PurePosixPath(p).name!=p or p=='MANIFEST.json' for p in paths):raise ValueError('invalid inventory')
    actual={p.name for p in root.iterdir()}
    if actual!=set(paths)|{'MANIFEST.json'}:raise ValueError('unexpected or missing path')
    for entry in files:
        p=root/entry['path']
        if p.is_symlink() or not p.is_file():raise ValueError('nonregular file')
        data=p.read_bytes()
        if len(data)!=entry['bytes'] or sha(data)!=entry['sha256']:raise ValueError('file mismatch: '+p.name)
    return len(files)

def self_test(root, expected):
    names=['changed_file','missing_file','extra_file','extra_directory','symlink','changed_manifest']
    for name in names:
        with tempfile.TemporaryDirectory(prefix='slippery-integrity-') as td:
            dst=pathlib.Path(td)/'release';shutil.copytree(root,dst)
            target=dst/'RESULT.md'
            if name=='changed_file':target.write_bytes(target.read_bytes()+b'\nmutation\n')
            elif name=='missing_file':target.unlink()
            elif name=='extra_file':(dst/'extra.txt').write_text('extra')
            elif name=='extra_directory':(dst/'unlisted').mkdir()
            elif name=='symlink':target.unlink();target.symlink_to(dst/'README.md')
            elif name=='changed_manifest':(dst/'MANIFEST.json').write_bytes((dst/'MANIFEST.json').read_bytes()+b' ')
            try:verify(dst,expected)
            except (ValueError,KeyError,TypeError,json.JSONDecodeError):continue
            raise RuntimeError('mutation accepted: '+name)
    return names

def main():
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);p.add_argument('--replay',action='store_true');p.add_argument('--self-test',action='store_true');args=p.parse_args()
    root=pathlib.Path(__file__).resolve().parent
    count=verify(root,args.expected_manifest)
    result={'status':'PASS_INVENTORY','files_verified':count,'manifest_sha256':args.expected_manifest}
    if args.replay:
        output=subprocess.check_output([sys.executable,'-B',str(root/'verify_math.py')],cwd=root)
        if output!=(root/'MATH_CHECKS.json').read_bytes():raise RuntimeError('mathematical replay byte mismatch')
        result['mathematical_replay']='BYTE_EXACT'
    if args.self_test:result['rejected_mutations']=self_test(root,args.expected_manifest)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
