#!/usr/bin/env python3
"""Verify pinned publication inventory and replay exact diagnostics."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys, tempfile

FILES={'README.md','RESULTS.md','RESEARCH_LOG.md','PRIOR_ATTEMPT_CHECK.md','SOURCE_VERIFICATION.json','STATUS.json','EXACT_RESULTS.json','verify_math.py','verify_package.py'}

def sha(b):return hashlib.sha256(b).hexdigest()

def integrity(root, expected):
    p=root/'MANIFEST.json'
    if p.is_symlink() or not p.is_file():raise ValueError('missing or linked manifest')
    if sha(p.read_bytes())!=expected:raise ValueError('manifest pin mismatch')
    obj=json.loads(p.read_text())
    if set(obj)!= {'schema','files'} or obj['schema']!='cyclic-lifts-author-freeze-v1':raise ValueError('manifest schema mismatch')
    if set(obj['files'])!=FILES:raise ValueError('manifest inventory mismatch')
    actual={x.name for x in root.iterdir()}
    if actual!=FILES|{'MANIFEST.json'}:raise ValueError('directory inventory mismatch')
    for name,entry in obj['files'].items():
        p=root/name
        if p.is_symlink() or not p.is_file():raise ValueError('missing or linked file: '+name)
        b=p.read_bytes()
        if set(entry)!={'bytes','sha256'} or len(b)!=entry['bytes'] or sha(b)!=entry['sha256']:
            raise ValueError('file mismatch: '+name)
    return obj

def replay(root):
    golden=(root/'EXACT_RESULTS.json').read_bytes()
    for flags in ([],['-O']):
        p=subprocess.run([sys.executable,'-B',*flags,str(root/'verify_math.py')],cwd=root.parent,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
        if p.returncode or p.stdout!=golden:raise ValueError('mathematical replay mismatch: '+repr(flags))
    return json.loads(golden)['total_checks']

def self_test(root,pin):
    count=0
    def rejected(mutator):
        nonlocal count
        with tempfile.TemporaryDirectory(prefix='cyclic-lifts-negative-') as td:
            dest=pathlib.Path(td)/'packet';shutil.copytree(root,dest)
            badpin=mutator(dest) or pin
            try:integrity(dest,badpin)
            except (ValueError,OSError,json.JSONDecodeError):count+=1;return
            raise ValueError('negative control was accepted')
    def change(p):
        f=p/'RESULTS.md';f.write_bytes(f.read_bytes()+b'corruption\n')
    def delete(p):(p/'STATUS.json').unlink()
    def extra(p):(p/'unexpected.txt').write_text('unexpected')
    def manifest(p):
        f=p/'MANIFEST.json';f.write_bytes(f.read_bytes()+b' ')
    def link(p):
        f=p/'README.md';f.unlink();f.symlink_to(p/'STATUS.json')
    rejected(change);rejected(delete);rejected(extra);rejected(manifest);rejected(link);rejected(lambda p:'0'*64)
    return count

def main():
    a=argparse.ArgumentParser();a.add_argument('--expected-manifest',required=True);a.add_argument('--self-test',action='store_true');args=a.parse_args()
    if len(args.expected_manifest)!=64 or any(c not in '0123456789abcdef' for c in args.expected_manifest):raise ValueError('invalid external manifest pin')
    root=pathlib.Path(__file__).resolve().parent
    obj=integrity(root,args.expected_manifest);checks=replay(root)
    nc=self_test(root,args.expected_manifest) if args.self_test else 0
    print(json.dumps({'manifest_sha256':args.expected_manifest,'payload_files':len(obj['files']),'mathematical_checks_per_replay':checks,'normal_and_optimized_replay':'PASS','integrity_negative_controls':nc,'scope':'author packet verified; independent mathematical audit still required'},sort_keys=True,indent=2))
if __name__=='__main__':main()
