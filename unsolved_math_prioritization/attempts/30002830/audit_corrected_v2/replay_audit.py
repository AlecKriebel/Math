#!/usr/bin/env python3
"""Fail-closed replay with immutable externally recorded author bindings."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

AUTHOR_MANIFEST_SHA256='d9e4ec28d3ccab08918a952bc6e448366f451d8abebaca72f292aa9e2a4e8494'
AUTHOR_ZIP_SHA256='8d3c73ef5321e5722260ee27e69ec465926cedcbff0965b52b3523b91fcd3fbf'


def require(value,message):
    if not value:raise RuntimeError(message)


def verify_tree(root,pinned_manifest=None):
    root=Path(root)
    for name in ('MANIFEST.json','MANIFEST.sha256'):
        require((root/name).is_file() and not (root/name).is_symlink(),'invalid manifest file')
    raw=(root/'MANIFEST.json').read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if pinned_manifest:require(digest==pinned_manifest,'pinned manifest mismatch')
    require((root/'MANIFEST.sha256').read_text().split()==[digest,'MANIFEST.json'],'manifest checksum mismatch')
    data=json.loads(raw)
    require(data['target_id']=='30002830','wrong target')
    names=[]
    for item in data['allowlisted_files']:
        name=item['path']
        require(isinstance(name,str) and Path(name).name==name and name not in names,'invalid or duplicate path')
        names.append(name);p=root/name
        require(p.is_file() and not p.is_symlink(),'invalid payload file')
        b=p.read_bytes()
        require(len(b)==item['bytes'],'payload length mismatch')
        require(hashlib.sha256(b).hexdigest()==item['sha256'],'payload hash mismatch')
    require(set(p.name for p in root.iterdir())==set(names)|{'MANIFEST.json','MANIFEST.sha256'},'unmanifested file')
    return len(names)


def verify_zip(path,author):
    raw=Path(path).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==AUTHOR_ZIP_SHA256,'pinned archive mismatch')
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        expected={'safe/'+p.name for p in Path(author).iterdir()}
        require(len(names)==len(set(names)) and set(names)==expected,'archive member mismatch')
        for name in names:
            require(z.read(name)==(Path(author)/Path(name).name).read_bytes(),'archive payload mismatch')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-safe',required=True)
    parser.add_argument('--author-zip')
    parser.add_argument('--integrity-only',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    audit_files=verify_tree(root)
    author_files=verify_tree(args.author_safe,AUTHOR_MANIFEST_SHA256)
    if args.author_zip:verify_zip(args.author_zip,args.author_safe)
    if not args.integrity_only:
        result=subprocess.run([sys.executable,str(root/'independent_verifier.py')],capture_output=True,text=True,check=True)
        require(json.loads(result.stdout)==json.loads((root/'independent_results.json').read_text()),'independent replay mismatch')
        aroot=Path(args.author_safe)
        author_result=subprocess.run([sys.executable,str(aroot/'verify_exact.py')],capture_output=True,text=True,check=True)
        require(json.loads(author_result.stdout)==json.loads((aroot/'verification_results.json').read_text()),'author replay mismatch')
    print(json.dumps(dict(target_id='30002830',integrity_passed=True,author_files=author_files,audit_files=audit_files,
                          symbolic_replay_passed=not args.integrity_only,archive_verified=bool(args.author_zip),
                          mathematical_scope='Five retained partial routes; no rationality resolution.')))


if __name__=='__main__':main()
