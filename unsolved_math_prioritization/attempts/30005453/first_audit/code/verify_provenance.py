#!/usr/bin/env python3
"""Hash full supplied corpora and source bytes; emit metadata, never source text."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

EXPECTED = {
 'problems.json':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'research_results.json':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
PDFS = {
 'owr.pdf':(407470,'320d7e903924249d1f57536cdf67491b3b5f89de8401c9a7c07800b09ee750c7'),
 'couzinie_hirsch.pdf':(193301,'49959f145120d52d101dabfd520b7d6b88da804ca2e36d3e0f5a3bcb31bfe983'),
 'couzinie_thesis.pdf':(499819,'bb7d2cabae092881d3bb4199038a38eb9ceee7b5dcb1ca6f6398258eb2fddc7a')}
STATEMENT='9b23f463c1979851e5c85e28336c68ac0b31c41d153334f25a92df39f3ac7733'
REVIEW='23a9b4f35fc3c8b7ae15e35434a656a6b8c9656a95dd6a150feeeb0a4028c0a3'
CATALOG_SHA='891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'
CATALOG_GIT='bd5c23e4e6c7e1901717a7e596477a7f6dc72425'

def digest(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,label):
    if not ok:raise ValueError(label)
def meta(raw):return {'bytes':len(raw),'sha256':digest(raw)}
def check(path,expected):
    raw=path.read_bytes()
    require((len(raw),digest(raw))==expected,'byte/hash mismatch: '+path.name)
    return raw
def review(p,r):return digest(json.dumps([p,r],sort_keys=True).encode('utf-8'))

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--corpus-dir',type=Path,required=True)
    p.add_argument('--catalog',type=Path,required=True)
    p.add_argument('--scholarly-dir',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    corp={name:check(a.corpus_dir/name,e) for name,e in EXPECTED.items()}
    problems=json.loads(corp['problems.json']);reports=json.loads(corp['research_results.json'])
    require(len(problems)==15458 and len(reports)==6701,'corpus cardinalities')
    ids=[i for i,x in enumerate(problems) if x.get('id')==30005453]
    keys=[i for i,x in enumerate(problems) if x.get('problem_number')=='OWR-12697708-006']
    require(ids==keys==[14237],'unique problem identity')
    target=problems[ids[0]]
    require('OWR-12697708-006' not in reports,'unexpected research key')
    require(b'30005453' not in corp['research_results.json'],'unexpected numeric ID in research corpus')
    require(digest(target['statement'].encode())==STATEMENT,'statement hash')
    require(review(target,{})==REVIEW,'review hash')
    cat=check(a.catalog,(21735099,CATALOG_SHA))
    blob=hashlib.sha1(b'blob '+str(len(cat)).encode()+b'\0'+cat).hexdigest()
    require(blob==CATALOG_GIT,'catalog Git blob')
    rows=[x for x in json.loads(cat) if x.get('id')=='30005453']
    require(len(rows)==1 and rows[0]['rank']==798,'catalog identity')
    require(rows[0]['statement_hash']==STATEMENT and rows[0]['review_hash']==REVIEW,'catalog hash match')
    pdfs={name:check(a.scholarly_dir/name,e) for name,e in PDFS.items()}
    require(all(raw.startswith(b'%PDF-') for raw in pdfs.values()),'PDF signature')
    altered=copy.deepcopy(target);altered['statement']+=' '
    require(review(altered,{})!=REVIEW,'review negative control')
    require(review(target,{'x':1})!=REVIEW,'research join negative control')
    out={'problem_id':30005453,'problem_number':'OWR-12697708-006','rank':798,
         'full_corpora':{name:{**meta(raw),'match':True} for name,raw in corp.items()},
         'corpus_records':len(problems),'research_entries':len(reports),
         'target_record_index':ids[0],'unique_id_and_code_match':True,
         'statement':{'bytes':len(target['statement'].encode()),'sha256':STATEMENT,'match':True},
         'research_record_present':False,'numeric_id_in_research_bytes':False,
         'review_sha256':REVIEW,'review_hash_match':True,
         'review_hash_rule':'SHA256 of UTF-8 json.dumps([problem_record, {}], sort_keys=True), using Python default JSON separators and ensure_ascii=True; empty object is the missing-report join.',
         'catalog':{**meta(cat),'git_blob_sha1':blob,'target_count':1,'descriptor_hashes_match':True},
         'scholarly_pdfs':{name:{**meta(raw),'match':True} for name,raw in pdfs.items()},
         'negative_controls':{'changed_statement':'REJECTED','changed_joined_report':'REJECTED'},
         'source_byte_scope':'Full cached corpora independently hashed against pinned public manifest; full cached catalog independently matched to a freshly observed Git tree blob; scholarly PDFs freshly retrieved independently.',
         'raw_source_material_in_safe_payload':False,'status':'PASS'}
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
