#!/usr/bin/env python3
"""Adversarial packaging checks; no producer code or source data needed."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('publication',Path(__file__).with_name('verify_publication.py'))
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('expected_manifest');p.add_argument('--queue',type=Path)
    a=p.parse_args();v.verify(a.root,a.expected_manifest,a.queue);checks=[]
    def reject(name,fn):
        try: fn()
        except (ValueError,OSError,KeyError): checks.append(name);return
        raise RuntimeError('Accepted negative control: '+name)
    reject('wrong_external_pin',lambda:v.verify(a.root,'0'*64))
    cases=[('missing_author_manifest','author/MANIFEST.json','missing'),('missing_audit_manifest','audit/MANIFEST.json','missing'),
           ('changed_author_proof','author/REPORT.md','change'),('changed_audit_proof','audit/AUDIT_REPORT.md','change'),
           ('changed_author_code','author/verify_reconstruction.py','change'),('changed_audit_code','audit/audit_certificate.py','change'),
           ('changed_publication_code','verify_publication.py','change'),('changed_status','PUBLICATION_STATUS.json','change'),
           ('changed_receipt','audit/fresh_audit_receipt.json','change'),('changed_manifest','PUBLICATION_MANIFEST.json','change'),
           ('unexpected_certificate','certificate.json','extra'),('unexpected_directory','empty-source-directory','directory'),
           ('payload_symlink','author/REPORT.md','symlink')]
    with tempfile.TemporaryDirectory(prefix='rbm publication negative controls ') as td:
        td=Path(td)
        for name,file,kind in cases:
            root=td/name;shutil.copytree(a.root,root);f=root/file
            if kind=='missing': f.unlink()
            elif kind=='change': f.write_bytes(f.read_bytes()+b'\n')
            elif kind=='extra': f.write_text('{}')
            elif kind=='directory': f.mkdir()
            elif kind=='symlink': f.unlink();f.symlink_to((a.root/file).resolve())
            reject(name,lambda root=root:v.verify(root,a.expected_manifest))
        missing=v.full(a.root,None)
        v.need(missing['status']=='NOT_RUN','missing inputs must not pass');checks.append('missing_sources_not_run')
        source=td/'external';source.mkdir();(source/'appendix.md').write_text('bad');(source/'certificate.json').write_text('{}')
        reject('tampered_external_input',lambda:v.source_check(source))
        (source/'appendix.md').unlink();(source/'appendix.md').symlink_to(source/'certificate.json')
        reject('symlink_external_input',lambda:v.source_check(source))
        if a.queue:
            raw=a.queue.read_bytes();q=td/'QUEUE.md'
            for name,changed in [('queue_other_bytes_changed',b'changed header\n'+raw),('queue_wrong_status',raw.replace(b'| 763 | 20002559 /',b'| 764 | 20002559 /',1)),('queue_stale',raw.replace(b' already_solved | 1/5 |',b' queued | 0/5 |',1))]:
                q.write_bytes(changed);reject(name,lambda:v.check_queue(a.root,q))
    v.verify(a.root,a.expected_manifest,a.queue)
    print(json.dumps({'status':'PASS','python_optimized':sys.flags.optimize,'negative_controls':len(checks),'checks':checks,'queue_controls':'RUN' if a.queue else 'NOT_RUN: optional queue absent'},sort_keys=True,indent=2))

if __name__=='__main__': main()
