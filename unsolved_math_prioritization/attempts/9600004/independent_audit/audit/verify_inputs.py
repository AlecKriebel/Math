#!/usr/bin/env python3
"""Recheck optional external corpus and PDF bytes without copying their contents.

Usage: python verify_inputs.py --corpus-dir DIR --pdf-dir DIR
Inputs are not part of the public audit payload.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise ValueError(message)

def pin(path):
    raw=path.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--corpus-dir',type=Path)
    p.add_argument('--pdf-dir',type=Path)
    a=p.parse_args()
    require(a.corpus_dir is not None or a.pdf_dir is not None,'supply at least one input directory')
    sources=json.loads((HERE.parent/'original/asymmetric_exclusion_9600004/SOURCES.json').read_text())
    result={}
    if a.corpus_dir:
        result['corpus']=[]
        for source in sources['public_corpus_verification']:
            actual=pin(a.corpus_dir/source['name'])
            require(all(actual[k]==source[k] for k in actual),'corpus pin mismatch: '+source['name'])
            result['corpus'].append({'name':source['name'],**actual,'match':True})
        problems=json.loads((a.corpus_dir/'problems.json').read_text())
        catalog=json.loads((a.corpus_dir/'catalog.json').read_text())
        reports=json.loads((a.corpus_dir/'research_results.json').read_text())
        target=[x for x in problems if str(x['id'])=='9600004']
        row=[x for x in catalog if str(x['id'])=='9600004']
        require(len(target)==len(row)==1,'target ID not unique')
        raw=json.dumps([target[0],reports.get(target[0]['problem_number'],{})],sort_keys=True).encode('utf-8')
        actual={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
        require(all(actual[k]==sources['canonical_pair'][k] for k in actual),'canonical pair mismatch')
        require(actual['sha256']==row[0]['review_hash'],'catalog review hash mismatch')
        require(row[0]['rank']==933 and row[0]['turns_used']==0,'gate metadata changed')
        result['canonical_pair']={**actual,'match':True}
    if a.pdf_dir:
        names=['liggett_archive','bbl_arxiv','conroy_sethuraman','conroy2025_k','conroy2025_d']
        result['pdfs']=[]
        for source,name in zip(sources['sources'],names):
            actual=pin(a.pdf_dir/(name+'.pdf'))
            require(all(actual[k]==source[k] for k in actual),'source PDF pin mismatch: '+name)
            result['pdfs'].append({'title':source['title'],'url':source['url'],**actual,'match':True})
    print(json.dumps({'ok':True,**result},indent=2))

if __name__=='__main__':main()
