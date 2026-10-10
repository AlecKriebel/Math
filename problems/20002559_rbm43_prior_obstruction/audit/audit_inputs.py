#!/usr/bin/env python3
"""Audit the untouched author ZIP, public source identities and dataset metadata.

Only hashes, sizes and match results are emitted. No imported records are copied.
"""
import argparse
from hashlib import sha256,sha1
import json
from pathlib import Path
import zipfile


def need(ok,message):
    if not ok:
        raise ValueError(message)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('freeze',type=Path)
    p.add_argument('author_directory',type=Path)
    p.add_argument('source_directory',type=Path)
    p.add_argument('corpus_directory',type=Path)
    p.add_argument('positive_controls',type=Path)
    a=p.parse_args()
    freeze=a.freeze.read_bytes()
    need(len(freeze) == 19315 and sha256(freeze).hexdigest() == '023751c3c9d7d97dbd860ba42e260e35b3de8563c8ba257baf98b00b22991d06','author ZIP identity')
    with zipfile.ZipFile(a.freeze) as z:
        names=z.namelist()
        need(len(names) == len(set(names)) == 15,'ZIP inventory count or duplicates')
        manifest=json.loads(z.read('MANIFEST.json'))
        need(set(names) == {r['path'] for r in manifest['files']}|{'MANIFEST.json'},'ZIP manifest inventory')
        files=[]
        for name in names:
            need('/' not in name and name not in ('.','..'),'ZIP unsafe path')
            data=z.read(name)
            need(data == (a.author_directory/name).read_bytes(),'author file changed from ZIP')
            files.append({'path':name,'bytes':len(data),'sha256':sha256(data).hexdigest(),'unchanged':True})
        for r in manifest['files']:
            data=z.read(r['path'])
            need(r['bytes'] == len(data) and r['sha256'] == sha256(data).hexdigest(),'author manifest mismatch')
    fresh=json.loads(Path(__file__).with_name('source_tree_metadata.json').read_text())
    authored=json.loads((a.author_directory/'source_verification.json').read_text())
    metadata={r['path']:r for r in fresh['files']}
    sources=[]
    for r in authored['files']:
        data=(a.source_directory/r['path']).read_bytes()
        blob=sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        need(len(data) == r['bytes'] == metadata[r['path']]['size'],'source byte count')
        need(sha256(data).hexdigest() == r['sha256'],'source hash mismatch')
        need(blob == r['git_blob_sha1'] == metadata[r['path']]['sha'],'fresh Git tree mismatch')
        sources.append({'path':r['path'],'bytes':len(data),'sha256':r['sha256'],'fresh_public_git_blob_match':True})
    pc=a.positive_controls.read_bytes()
    need(len(pc) == 4292 and sha1(b'blob 4292\0'+pc).hexdigest() == '513aa4aaecde04e9b4c353a482bbc026c7951ce9','positive controls public blob')
    pins={'problems.json':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),'research_results.json':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
    parsed={};corpus=[]
    for name,(length,digest) in pins.items():
        data=(a.corpus_directory/name).read_bytes()
        need(len(data) == length and sha256(data).hexdigest() == digest,'public corpus hash/size')
        corpus.append({'name':name,'bytes':length,'sha256':digest,'match':True})
        parsed[name]=json.loads(data)
    targets=[r for r in parsed['problems.json'] if r['id'] == 20002559]
    need(len(targets) == 1 and targets[0]['problem_number'] == 'AIM-PROBABILITY-0001','target identity')
    target=targets[0]
    report=parsed['research_results.json'][target['problem_number']]
    need(target['statement'] == target['original_statement'] == target['clean_statement'],'problem statement variants')
    need(report['problem_original'] == report['problem_clean'] == target['statement'],'paired statement agreement')
    prior=(a.source_directory/'upstream_report.txt').read_text()
    for value in report.values():
        if isinstance(value,str):
            need(value in prior,'prior report missing field content')
    out={'status':'PASS','freeze':{'bytes':len(freeze),'sha256':sha256(freeze).hexdigest(),'authored_file_count':len(files),'all_files_unchanged':True,'manifest_verified':True,'files':files},'public_sources':sources,'additional_controls_public_blob_match':True,'public_corpus_metadata':corpus,'problem_id':20002559,'problem_number':'AIM-PROBABILITY-0001','statement_variants_and_paired_report_match':True,'full_paired_report_in_inspected_local_copy':True,'source_text_or_dataset_records_emitted':False}
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
