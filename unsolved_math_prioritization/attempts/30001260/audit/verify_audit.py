#!/usr/bin/env python3
"""Verify an externally pinned audit package and replay both independent checks.
This is an integrity/reproducibility utility, not a mathematical proof checker.
"""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import zipfile

AUTHOR_SHA = '80adc712a807f61e5b3daf948e356002d475cd44b5763408b05af1f70491aba0'
AUTHOR_MANIFEST_SHA = '3f689988d6844b90d70a1f3bbeb18dcbdecc769c8a98ed6c6f5f34053bc01757'

def need(ok, label):
    if not ok:
        raise ValueError(label)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def safe_name(name):
    return isinstance(name,str) and name not in ('','.','..') and '/' not in name and '\\' not in name

def check_inventory(root, manifest_name, pin):
    raw=(root/manifest_name).read_bytes()
    need(digest(raw)==pin,'manifest pin mismatch')
    manifest=json.loads(raw)
    need(manifest.get('schema')==1,'unknown manifest schema')
    records=manifest['files'];names=[r['path'] for r in records]
    need(all(safe_name(n) and n!=manifest_name for n in names),'unsafe inventory path')
    need(len(set(names))==len(names),'duplicate inventory path')
    found=[]
    for p in root.iterdir():
        need(not p.is_symlink() and p.is_file(),'nonregular or symlink entry')
        found.append(p.name)
    need(set(found)==set(names)|{manifest_name},'exact inventory mismatch')
    for r in records:
        raw=(root/r['path']).read_bytes()
        need(len(raw)==r['bytes'] and digest(raw)==r['sha256'],'file mismatch: '+r['path'])
    return len(records)

def main(root,pin):
    root=pathlib.Path(root).resolve()
    count=check_inventory(root,'AUDIT_MANIFEST.json',pin)
    expected=(root/'INDEPENDENT_CHECK_RESULTS.json').read_bytes()
    for flags in ([],['-O']):
        completed=subprocess.run([sys.executable,'-I',*flags,str(root/'independent_checks.py')],capture_output=True,check=True)
        need(completed.stdout==expected,'independent-check replay mismatch')
    archive=root/'AUTHOR_PACKET.zip'
    need(len(archive.read_bytes())==21349 and digest(archive.read_bytes())==AUTHOR_SHA,'original archive mismatch')
    with tempfile.TemporaryDirectory(prefix='s5-audit-replay-') as tmp:
        author=pathlib.Path(tmp)
        with zipfile.ZipFile(archive) as z:
            members=z.namelist()
            need(len(members)==14 and len(set(members))==14,'original ZIP inventory count')
            need(all(safe_name(n) for n in members),'unsafe original ZIP path')
            for info in z.infolist():
                need(not info.is_dir(),'original ZIP directory rejected')
                (author/info.filename).write_bytes(z.read(info))
        check_inventory(author,'MANIFEST.json',AUTHOR_MANIFEST_SHA)
        for flags in ([],['-O']):
            completed=subprocess.run([sys.executable,'-I',*flags,str(author/'verify_packet.py'),AUTHOR_MANIFEST_SHA],capture_output=True,check=True)
            need(json.loads(completed.stdout)['status']=='PASS','original packet replay failure')
    return {'status':'PASS','audit_manifest_sha256':pin,'audit_manifest_record_count':count,'independent_normal_and_optimized_replay':'PASS','original_normal_and_optimized_replay':'PASS','original_archive_sha256':AUTHOR_SHA,'scope':'Pinned inventory and exact replay; not a proof, source-authenticity signature, or smooth-realization certificate'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('manifest_sha256')
    parser.add_argument('--root',default=str(pathlib.Path(__file__).resolve().parent))
    args=parser.parse_args()
    print(json.dumps(main(args.root,args.manifest_sha256),indent=2,sort_keys=True))
