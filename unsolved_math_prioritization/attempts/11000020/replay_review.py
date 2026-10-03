#!/usr/bin/env python3
"""Portable staging wrapper for the unchanged author and review freezes."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
AUTHOR_SEAL = '441c21fe437955edfaedf0a13f32c25115d1ce1cc0f849c2e4a5b8c1b3941794'
REVIEW_SEAL = 'a65c535c7cdc26fb9e3e1ed2ff6c90f1691a41a42e41778243d35c0df432e870'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def validate(directory, name, seal, key):
    raw = (directory/name).read_bytes()
    if sha(raw) != seal:
        raise ValueError('Wrong freeze: '+name)
    manifest = json.loads(raw)
    names = [name]
    for entry in manifest['files']:
        name = entry[key]
        data = (directory/name).read_bytes()
        if sha(data) != entry['sha256'] or len(data) != entry['bytes']:
            raise ValueError('Binding mismatch: '+name)
        names.append(name)
    return names

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path)
    args = parser.parse_args()
    authors = validate(ROOT, 'manifest.json', AUTHOR_SEAL, 'file')
    reviews = validate(ROOT/'review', 'REVIEW_MANIFEST.json', REVIEW_SEAL, 'path')
    result = subprocess.run(['python3',str(ROOT/'verify.py')],check=True,capture_output=True).stdout
    if result != (ROOT/'verifier_output.json').read_bytes():
        raise ValueError('Author replay differs')
    report = {'status':'PASS','author_files_verified':len(authors),
              'review_files_verified':len(reviews),'author_assertions':json.loads(result)['assertions'],
              'independent_suite':'NOT_RUN: requires --source-dir', 'classification_reproduced':False}
    if args.source_dir is not None:
        sources = json.loads((ROOT/'source_manifest.json').read_text())['sources']
        with tempfile.TemporaryDirectory(prefix='canonical-basepoints-review-') as tmp:
            stage = Path(tmp)
            for dirname in ['packet','review','source']:
                (stage/dirname).mkdir()
            for name in authors:
                shutil.copyfile(ROOT/name,stage/'packet'/name)
            for name in reviews:
                shutil.copyfile(ROOT/'review'/name,stage/'review'/name)
            for entry in sources:
                src=args.source_dir/entry['file']
                data=src.read_bytes()
                if len(data)!=entry['bytes'] or sha(data)!=entry['sha256']:
                    raise ValueError('Source binding mismatch: '+entry['file'])
                shutil.copyfile(src,stage/'source'/entry['file'])
            independent = subprocess.run(['python3',str(stage/'review'/'reviewer_checks.py')],
                                         check=True,capture_output=True).stdout
            if independent!=(ROOT/'review'/'REVIEWER_CHECKS.json').read_bytes():
                raise ValueError('Independent replay differs')
            report['independent_suite']='PASS'
            report['independent_assertions']=json.loads(independent)['assertions']
            report['source_files_verified']=len(sources)
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
