#!/usr/bin/env python3
"""Recheck optional external source bytes. Never emit source content."""
import argparse
import hashlib
import json
from pathlib import Path


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def fingerprint(path, expected):
    data=path.read_bytes()
    actual={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    require(actual==expected,'Source fingerprint mismatch: '+path.name)
    return data,actual


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--corpus-dir',required=True)
    p.add_argument('--pdf-dir',required=True)
    a=p.parse_args()
    here=Path(__file__).resolve().parent
    metadata=json.loads((here/'SOURCE_AUDIT.json').read_text())
    out={'status':'PASS','corpus':{},'pdfs':{},'record_ids':[],'join_absent':[]}
    objects={}
    for name,expected in metadata['corpus_fingerprints'].items():
        data,actual=fingerprint(Path(a.corpus_dir)/name,expected)
        objects[name]=json.loads(data)
        out['corpus'][name]=actual
    problems=objects['problems.json'];reports=objects['research_results.json']
    for id,code in ((30006622,'OWR-14299911-024'),(30006623,'OWR-14299911-025'),
                    (30006624,'OWR-14299911-026')):
        matches=[row for row in problems if row['id']==id]
        require(len(matches)==1,'Numeric source identity is not unique')
        require(matches[0]['problem_number']==code,'Numeric identity/code mismatch')
        require(code not in reports,'Unexpected exact joined research report')
        out['record_ids'].append(id);out['join_absent'].append(code)
    for source in metadata['pdf_sources']:
        _,actual=fingerprint(Path(a.pdf_dir)/source['local_basename'],
                              {'bytes':source['bytes'],'sha256':source['sha256']})
        out['pdfs'][source['title']]=actual
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
