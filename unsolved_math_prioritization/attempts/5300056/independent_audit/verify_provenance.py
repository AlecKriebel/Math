#!/usr/bin/env python3
"""Opt-in verification of omitted corpora and public source/repository files.

No file is downloaded or modified. Inputs must be supplied explicitly.
Only hashes, byte counts, matching flags, and record counts are emitted.
"""
from pathlib import Path
import argparse
import hashlib
import json

PINS={
 'catalog':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 'problems':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'research_results':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'),
 'queue_python':(25994,'f72aee023f837bad092da58531c2cc069ce2cf094e835d090221107d20f07ab2'),
 'dataset_manifest':(486,'3e025cee22128443584ddc22e095e44600a006699d0d62488793d881e62be208'),
 'primary_pdf':(1151433,'e0dbfa6ad56d14971d4f901dc8568731e22359feeb1efb429b240f156b88d29e'),
 'dobbs_pdf':(284132,'343682595b235d2f158fd1fe6876574a842a97b86f9e6f479f9ed8a1bdcd465e'),
 'fine_inducing_pdf':(413187,'dfceb248b8db3433bf37fb791260a8783e006f34d5f3616c399db8a5d483ee0f')
}
def require(test,message):
    if not test:raise AssertionError(message)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in PINS:p.add_argument('--'+name.replace('_','-'),type=Path,required=True)
    a=p.parse_args()
    blobs={}; matches={}
    for name,(size,sha) in PINS.items():
        blob=getattr(a,name).read_bytes()
        found=hashlib.sha256(blob).hexdigest()
        require((len(blob),found)==(size,sha),'Full input does not match pin: '+name)
        blobs[name]=blob
        matches[name]={'bytes':len(blob),'sha256':found,'matches_pin':True}
    catalog=json.loads(blobs['catalog']); records=json.loads(blobs['problems'])
    reports=json.loads(blobs['research_results']); manifest=json.loads(blobs['dataset_manifest'])
    require(len(catalog)==len(records)==15458 and len(reports)==6701,'Unexpected corpus counts')
    target=[r for r in records if str(r['id'])=='5300056']
    cats=[r for r in catalog if str(r['id'])=='5300056']
    require(len(target)==len(cats)==1,'Ambiguous numeric target identity')
    record=target[0]; cat=cats[0]; number=record['problem_number']
    require(number=='AMR-052-0056','Target code mismatch')
    require(sum(r['problem_number']==number for r in records)==1,'Ambiguous report join')
    report=reports.get(number,{})
    statement_hash=hashlib.sha256(record['statement'].encode()).hexdigest()
    review_hash=hashlib.sha256(json.dumps([record,report],sort_keys=True).encode()).hexdigest()
    require(statement_hash==cat['statement_hash']=='a614504e062997e753cc062b35f1d72bf7c9b69525b5d1bdb8b2b2fa6702e469','Statement mismatch')
    require(review_hash==cat['review_hash']=='d699f57822f44019eccaa623b4da5ef95efde4be68233c08d5229e8ed5fa938c','Full-record review mismatch')
    require(cat['rank']==795,'Catalog rank mismatch')
    for name in ['problems','research_results']:
        require(manifest['files'][name+'.json']=={'bytes':PINS[name][0],'sha256':PINS[name][1]},'Repository manifest mismatch')
    # The exact fetched queue.py is pinned above. This signature check records
    # the inspected serialization; it does not execute the repository script.
    require('review_hash=digest(json.dumps([p,r],sort_keys=True))' in blobs['queue_python'].decode(),'Review serialization mismatch')
    result={
        'status':'PASS', 'problem_id':5300056,
        'full_input_matches':matches,
        'record_counts':{'catalog':len(catalog),'problems':len(records),'research_results':len(reports)},
        'target_id_unique':True,'report_join_unambiguous':True,
        'statement_utf8_sha256':statement_hash,'review_hash':review_hash,
        'statement_matches_catalog':True,'review_matches_catalog':True,
        'review_formula':'SHA256(json.dumps([full_problem_record, research_results.get(problem_number,{})], sort_keys=True).encode())',
        'dataset_revision':manifest['revision'],
        'raw_corpus_contents_included':False,
        'scope':'Full supplied bytes and target identity verified. This is provenance, not evidence of mathematical validity or current open status.'
    }
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
