#!/usr/bin/env python3
"""Recheck complete externally supplied corpora and public-source byte pins.
Inputs remain private; output contains verification metadata only.
"""
import argparse
import hashlib
import json
from pathlib import Path

CORPORA={
 'catalog.json':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566',15458),
 'problems.json':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf',15458),
 'research_results.json':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b',6701)}
SOURCES={
 'junkyard.html':(10581,'08d988d3470105d8177627180cf24c0c31b3ae3d7e073f0cfc9f003e95d96a99','https://ics.uci.edu/~eppstein/junkyard/open.html'),
 'jiang.pdf':(567362,'7911796db6dad3216b395622a24aea81ec0425e5c94b2496094a8df0b663c9e8','https://arxiv.org/pdf/2609.28791v1'),
 'zhu_joos.pdf':(395486,'dae8c84090190cf13834e3fef6dbafba17064342cd7f9dd57c85e0138a047662','https://arxiv.org/pdf/2211.10356v1'),
 'slack_pack.pdf':(1510276,'d14bf80dfb7905e3f471c745cb87b7f8d46f1bfefe770a9a31b784bb2c62cd44','https://arxiv.org/pdf/2412.17151v3'),
 'martin.pdf':(131229,'37152fea1a1abc34f5a658b6abe123a99d901dbab118adf50a53733032db627b','https://personal.math.ubc.ca/~gerg/papers/downloads/CTGP.pdf')}
PAIR_HASH='24e97cc97da5043fe972e9bfecb2ceb7ffcd8879316a9fea453065c61b6c573f'

def require(ok,message):
 if not ok:raise ValueError(message)

def pinned(path,size,digest):
 b=path.read_bytes();require(len(b)==size,'size mismatch: '+path.name)
 require(hashlib.sha256(b).hexdigest()==digest,'hash mismatch: '+path.name)
 return b

def verify(corpus,source):
 objects={};corp=[]
 for name,(size,digest,count) in CORPORA.items():
  b=pinned(corpus/name,size,digest);objects[name]=json.loads(b)
  require(len(objects[name])==count,'record count mismatch: '+name)
  corp.append({'dataset':name,'bytes':size,'sha256':digest,'record_count':count,'complete_file_verified':True})
 matches=[p for p in objects['problems.json'] if str(p.get('id'))=='3900015']
 catalogs=[p for p in objects['catalog.json'] if str(p.get('id'))=='3900015']
 require(len(matches)==len(catalogs)==1,'exact ID not unique')
 problem=matches[0];require(problem['problem_number']=='AMR-038-0015','problem number mismatch')
 require(catalogs[0]['rank']==928,'rank mismatch')
 report=objects['research_results.json'].get(problem['problem_number'],{})
 pair=json.dumps({'problem':problem,'report':report},sort_keys=True).encode('utf-8')
 require(len(pair)==4960 and hashlib.sha256(pair).hexdigest()==PAIR_HASH,'complete pair pin mismatch')
 src=[]
 for name,(size,digest,url) in SOURCES.items():
  pinned(source/name,size,digest)
  src.append({'filename':name,'bytes':size,'sha256':digest,'public_url':url,'complete_file_verified':True})
 return {'schema':'independent-source-corpus-byte-audit-v1','problem_id':'3900015','problem_number':'AMR-038-0015',
         'rank':928,'complete_corpora':corp,'exact_problem_matches':1,'exact_catalog_matches':1,
         'record_pair_bytes':4960,'record_pair_sha256':PAIR_HASH,'pair_includes_complete_problem_and_report':True,
         'pair_serialization':'json.dumps({"problem": complete_exact_id_record, "report": reports.get(problem_number,{})}, sort_keys=True).encode("utf-8") using Python defaults',
         'public_sources':src,'raw_data_or_source_text_included':False,
         'limitation':'Byte identity and full-record selection do not establish theorem validity; mathematical and source-reading conclusions are in AUDIT.md.'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--corpus-dir',type=Path,required=True);p.add_argument('--source-dir',type=Path,required=True)
 a=p.parse_args();print(json.dumps(verify(a.corpus_dir,a.source_dir),sort_keys=True,indent=2))
