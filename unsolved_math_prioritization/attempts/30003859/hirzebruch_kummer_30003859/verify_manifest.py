#!/usr/bin/env python3
"""Strict portable author-packet integrity and optional exact replay."""
import argparse, hashlib, json, pathlib, shutil, subprocess, sys, tempfile

MANIFEST='manifest.json'

def verify(root):
    root=pathlib.Path(root)
    if not root.is_dir() or root.is_symlink():
        raise ValueError('root must be a real directory')
    manifest=root/MANIFEST
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError('manifest must be a regular file')
    data=json.loads(manifest.read_text())
    entries=data['files']
    if not isinstance(entries,list):
        raise ValueError('malformed file list')
    names=[x['path'] for x in entries]
    if len(set(names))!=len(names):
        raise ValueError('duplicate file path')
    if any('/' in n or '\\' in n or n.startswith('.') or n==MANIFEST for n in names):
        raise ValueError('invalid flat packet path')
    actual={p.name for p in root.iterdir()}
    if actual!=set(names)|{MANIFEST}:
        raise ValueError('unexpected or omitted path')
    for entry in entries:
        p=root/entry['path']
        if p.is_symlink() or not p.is_file():
            raise ValueError('nonregular packet member')
        b=p.read_bytes()
        if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
            raise ValueError('digest or size mismatch: '+p.name)
    return len(entries)


def replay(root):
    expected=(root/'expected_results.json').read_bytes()
    for flags in ([],['-O']):
        result=subprocess.run([sys.executable]+flags+[str(root/'verify.py')],cwd=tempfile.gettempdir(),capture_output=True,check=True)
        if result.stdout!=expected:
            raise ValueError('exact replay mismatch: '+str(flags))


def negative_tests(root):
    cases=['changed_bytes','missing_file','extra_file','symlink','duplicate_manifest_entry','traversal_path']
    for case in cases:
        with tempfile.TemporaryDirectory() as t:
            target=pathlib.Path(t)/'packet'
            shutil.copytree(root,target)
            if case=='changed_bytes':
                with (target/'REPORT.md').open('ab') as f:f.write(b'\nchanged\n')
            elif case=='missing_file':(target/'REPORT.md').unlink()
            elif case=='extra_file':(target/'extra.txt').write_text('unexpected')
            elif case=='symlink':
                p=target/'REPORT.md';p.unlink();p.symlink_to(root/'REPORT.md')
            else:
                p=target/MANIFEST;m=json.loads(p.read_text())
                if case=='duplicate_manifest_entry':m['files'].append(m['files'][0])
                else:m['files'][0]['path']='../escape'
                p.write_text(json.dumps(m))
            try:verify(target)
            except (ValueError,KeyError,TypeError):pass
            else:raise ValueError('negative integrity control accepted: '+case)
    return len(cases)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    parser.add_argument('--selftest',action='store_true')
    args=parser.parse_args()
    root=pathlib.Path(__file__).resolve().parent
    n=verify(root)
    report={'status':'PASS_AUTHOR_INTEGRITY','bound_files':n}
    if args.replay:
        replay(root);report['normal_and_optimized_replay']='byte_identical'
    if args.selftest:report['rejected_integrity_mutations']=negative_tests(root)
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()
