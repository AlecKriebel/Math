#!/usr/bin/env python3
"""Validate this frozen package; --self-test checks damaged-package rejection."""
import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

ALLOWED = {'README.md','PROOF.md','RESEARCH_LOG.md','SOURCE_METADATA.json','verify.py',
           'requirements.txt','verification.json','selftest.json','audit_manifest.py','audit_checks.json'}

def require(ok,msg):
    if not ok:raise ValueError(msg)

def check(root):
    root=Path(root)
    manifest=json.loads((root/'MANIFEST.json').read_text())
    require(manifest['problem_id']=='30003442','problem ID')
    require(manifest['status']=='partial; unrestricted target unresolved','scope')
    entries=manifest['files'];require(set(entries)==ALLOWED,'manifest allowlist')
    require({p.name for p in root.iterdir()}==ALLOWED|{'MANIFEST.json'},'directory allowlist')
    for name,meta in entries.items():
        p=root/name;require(p.is_file() and not p.is_symlink(),'regular file required')
        data=p.read_bytes();require(len(data)==meta['bytes'],'byte count mismatch: '+name)
        require(hashlib.sha256(data).hexdigest()==meta['sha256'],'SHA mismatch: '+name)
    source=json.loads((root/'SOURCE_METADATA.json').read_text())
    require(source['dataset_verification']['byte_match'] is True,'dataset bytes not verified')
    require(source['prior_reports_verification']['byte_match'] is True,'reports bytes not verified')
    verification=json.loads((root/'verification.json').read_text())
    require(verification['exact_example_count']==58,'example count')
    require(verification['unrestricted_target']=='unresolved','mathematical scope')
    return {'status':'pass','files_checked':len(entries),'source_bytes_required':False}

def selftest(root):
    root=Path(root);check(root);tests=[]
    def rejects(label,action):
        with tempfile.TemporaryDirectory(prefix='stable-roots-audit-') as tmp:
            dst=Path(tmp)/'packet';shutil.copytree(root,dst);action(dst)
            try:check(dst)
            except (ValueError,KeyError,FileNotFoundError,json.JSONDecodeError):tests.append(label);return
            raise RuntimeError('corruption accepted: '+label)
    for name in sorted(ALLOWED):
        rejects('modified '+name,lambda p,n=name:(p/n).write_bytes((p/n).read_bytes()+b'\n'))
    rejects('missing proof',lambda p:(p/'PROOF.md').unlink())
    rejects('unexpected file',lambda p:(p/'unexpected.pdf').write_bytes(b'forbidden extra file'))
    def unsafe_manifest(p):
        m=json.loads((p/'MANIFEST.json').read_text());m['files']['../escape']={};(p/'MANIFEST.json').write_text(json.dumps(m))
    rejects('path traversal manifest',unsafe_manifest)
    def symlink(p):
        f=p/'PROOF.md';f.unlink();f.symlink_to(p/'README.md')
    rejects('symlink input',symlink)
    return {'status':'pass','corruptions_rejected':len(tests),'tests':tests,'scope':'integrity relative to the frozen manifest; not an authenticity signature'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',default=str(Path(__file__).resolve().parent));ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    print(json.dumps(selftest(args.root) if args.self_test else check(args.root),indent=2,sort_keys=True))

if __name__=='__main__':main()
