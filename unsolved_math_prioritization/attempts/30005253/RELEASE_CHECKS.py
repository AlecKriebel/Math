#!/usr/bin/env python3
"""Strict portable release verification. Write optional outputs outside this tree."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

AUTHOR_MANIFEST='0b6c020816320cf325c05981ba16699ecfc4e6a5a596cb46752494827c9534f4'
AUDIT_MANIFEST='10c9dae2d19a5e6724ade288996c7af323ed6c895cbd7c848ea84850727336e9'

class Invalid(ValueError):
    pass

def need(condition,message):
    if not condition:
        raise Invalid(message)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(root):
    files=[]
    for p in root.rglob('*'):
        need(not p.is_symlink(),'symlink')
        if p.is_file(): files.append(p.relative_to(root).as_posix())
        else: need(p.is_dir(),'unexpected file type')
    return sorted(files)

def strict_manifest(root):
    raw=(root/'SHA256SUMS').read_bytes()
    need(raw.endswith(b'\n'),'unterminated manifest')
    rows=raw.decode('utf-8').splitlines()
    names=[]
    for line in rows:
        m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        need(m is not None,'malformed manifest')
        digest,name=m.groups()
        path=PurePosixPath(name)
        need(not path.is_absolute() and name==path.as_posix() and
             all(x not in ('','.','..') for x in name.split('/')) and
             '\\' not in name and name!='SHA256SUMS','unsafe manifest path')
        need(name not in names,'duplicate manifest path')
        names.append(name)
        f=root/name
        need(f.is_file() and not f.is_symlink(),'missing file or symlink')
        need(sha(f)==digest,'file digest mismatch: '+name)
    need(names==sorted(names),'unsorted manifest')
    need(names==[n for n in inventory(root) if n!='SHA256SUMS'],'manifest inventory mismatch')
    return len(names)

def verify(root):
    count=strict_manifest(root)
    need(sha(root/'author/SHA256SUMS')==AUTHOR_MANIFEST,'author binding')
    need(sha(root/'audit/SHA256SUMS')==AUDIT_MANIFEST,'audit binding')
    strict_manifest(root/'author')
    strict_manifest(root/'audit')
    strict_manifest(root/'audit/audited_packet')
    for name in inventory(root/'author'):
        need((root/'author'/name).read_bytes()==(root/'audit/audited_packet'/name).read_bytes(),
             'frozen copies differ')
    return count

def regenerate_manifest(root):
    (root/'SHA256SUMS').write_text(''.join(sha(root/n)+'  '+n+'\n' for n in inventory(root) if n!='SHA256SUMS'))

def negatives(root):
    cases=('tampered_file','missing_file','unexpected_file','duplicate_entry','malformed_digest',
           'parent_path','absolute_path','symlink','forged_top_manifest_author','forged_top_manifest_audit')
    for case in cases:
        with tempfile.TemporaryDirectory() as td:
            q=Path(td)/'release';shutil.copytree(root,q)
            f=q/'author/README.md';manifest=q/'SHA256SUMS'
            if case=='tampered_file': f.write_bytes(f.read_bytes()+b'\nchanged\n')
            elif case=='missing_file': f.unlink()
            elif case=='unexpected_file': (q/'unlisted.txt').write_text('unexpected')
            elif case=='duplicate_entry': manifest.write_bytes(manifest.read_bytes()+manifest.read_bytes().splitlines(keepends=True)[0])
            elif case=='malformed_digest': manifest.write_text('z'+manifest.read_text()[1:])
            elif case=='parent_path': manifest.write_text('0'*64+'  ../outside\n'+manifest.read_text())
            elif case=='absolute_path': manifest.write_text('0'*64+'  /outside\n'+manifest.read_text())
            elif case=='symlink': f.unlink();f.symlink_to(q/'author/PROOF.md')
            elif case=='forged_top_manifest_author':
                f.write_bytes(f.read_bytes()+b'changed');regenerate_manifest(q)
            elif case=='forged_top_manifest_audit':
                f=q/'audit/AUDIT.md';f.write_bytes(f.read_bytes()+b'changed');regenerate_manifest(q)
            try: verify(q)
            except (Invalid,FileNotFoundError): pass
            else: raise Invalid('negative control accepted: '+case)
    return len(cases)

def run(root):
    count=verify(root)
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'original.json'
        subprocess.run([sys.executable,'-B',str(root/'author/compute_controls.py'),'--output',str(out)],check=True,capture_output=True)
        need(out.read_bytes()==(root/'author/control_results.json').read_bytes(),'original replay differs')
        out=Path(td)/'independent.json'
        subprocess.run([sys.executable,'-B',str(root/'audit/verify_audit.py'),'--output',str(out)],check=True,capture_output=True)
        need(out.read_bytes()==(root/'audit/audit_results.json').read_bytes(),'independent replay differs')
    return {'passed':True,'manifest_entries':count,'original_replay_byte_identical':True,
            'independent_replay_byte_identical':True,'frozen_author_copies_identical':True,
            'strict_negative_controls_rejected':negatives(root),'full_target_status':'unsolved',
            'substantive_routes':5,'full_resolution':False,'novelty_claim':False,
            'gaussian_1800_fit_scope':'numerical sanity only, not a proof'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=run(Path(__file__).resolve().parent)
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output: args.output.write_text(text)
    print(text,end='')
