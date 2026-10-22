#!/usr/bin/env python3
"""Integrity negative controls using isolated temporary copies, with no source inputs."""
import hashlib, importlib.util, json, os, shutil, sys, tempfile
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('packet_verify',ROOT/'verify_publication.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def rehash(p,n):
    m=json.loads((p/'PUBLICATION_MANIFEST.json').read_bytes());m['files'][n]=v.pin((p/n).read_bytes());(p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
def byte_mutation(p):
    n='author/RESULT.md';(p/n).write_bytes((p/n).read_bytes()+b'\nchanged\n')
def frozen_rehash(p):byte_mutation(p);rehash(p,'author/RESULT.md')
def zip_mutation(p):
    n=v.ARCHIVES[0][0];(p/n).write_bytes((p/n).read_bytes()+b'x');rehash(p,n)
def scope_mutation(p):
    n='PUBLICATION.json';m=json.loads((p/n).read_bytes());m['general_problem_solved']=True;(p/n).write_text(json.dumps(m));rehash(p,n)
def extra_file(p):(p/'unlisted').write_text('test')
def extra_directory(p):(p/'empty_unlisted').mkdir()
def symlink(p):(p/'link').symlink_to('author/RESULT.md')
def omission(p):(p/'author/RESULT.md').unlink()
def manifest_path(p):
    n='PUBLICATION_MANIFEST.json';m=json.loads((p/n).read_bytes());m['files']['../outside']={'bytes':0,'sha256':hashlib.sha256(b'').hexdigest()};(p/n).write_text(json.dumps(m))
def frozen_manifest(p):
    n='author/AUTHOR_MANIFEST.json';m=json.loads((p/n).read_bytes());m['status']='solved';(p/n).write_text(json.dumps(m));rehash(p,n)
def expected_output(p):(p/'VERIFICATION_RESULTS.json').write_text('{}\n')
def main():
    v.integrity();results={}
    for mutation in [byte_mutation,frozen_rehash,zip_mutation,scope_mutation,extra_file,extra_directory,symlink,omission,manifest_path,frozen_manifest,expected_output]:
        with tempfile.TemporaryDirectory(prefix='abelian-cone-negative-') as d:
            p=Path(d)/'packet';shutil.copytree(ROOT,p);mutation(p)
            try:v.integrity(p)
            except (RuntimeError,FileNotFoundError,ValueError):results[mutation.__name__]='REJECTED'
            else:raise RuntimeError('Mutation accepted: '+mutation.__name__)
    print(json.dumps({'status':'PASS','negative_controls':len(results),'results':results},indent=2,sort_keys=True))
if __name__=='__main__':main()
