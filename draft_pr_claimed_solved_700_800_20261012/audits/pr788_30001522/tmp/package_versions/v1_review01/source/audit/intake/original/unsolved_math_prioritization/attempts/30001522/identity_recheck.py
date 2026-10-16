#!/usr/bin/env python3
"""Recheck full supplied corpora; emit only hashes/counts/match metadata."""
import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
 'catalog':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566',15458),
 'problems':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf',15458),
 'research_results':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b',6701)}
REVIEW='ca5ea39f6f40b6344a17adf507993b7a3aa628f194669943f2b6acb99876e306'
STATEMENT='c368a8d0a2095496760c49e9393ba1825274ccad544d6cf16acbca830d7ef0a0'
def require(value,message):
 if not value:raise RuntimeError(message)
def h(b):return hashlib.sha256(b).hexdigest()
def run(paths):
 loaded={};metadata=[]
 for role,path in paths.items():
  raw=path.read_bytes();expected_bytes,expected_sha,expected_count=EXPECTED[role]
  require(len(raw)==expected_bytes and h(raw)==expected_sha,'corpus pin mismatch: '+role)
  value=json.loads(raw);require(len(value)==expected_count,'record-count mismatch: '+role)
  loaded[role]=value
  metadata.append({'role':role,'bytes':len(raw),'sha256':h(raw),'top_level_records':len(value),'pin_match':True})
 records=[r for r in loaded['problems'] if str(r.get('id'))=='30001522']
 catalog=[r for r in loaded['catalog'] if str(r.get('id'))=='30001522']
 require(len(records)==len(catalog)==1,'target identifier not unique')
 record=records[0];entry=catalog[0];reports=loaded['research_results']
 require(record['problem_number']==entry['problem_number']=='OWR-4413-005','problem number mismatch')
 require(entry['rank']==828,'rank mismatch')
 report=reports.get(record['problem_number'],{})
 blob=json.dumps([record,report],sort_keys=True).encode('utf-8')
 statement=record['statement'].encode('utf-8')
 require(h(blob)==REVIEW==entry['review_hash'],'review hash mismatch')
 require(h(statement)==STATEMENT==entry['statement_hash'],'statement hash mismatch')
 return {'schema':1,'problem_id':30001522,'problem_number':'OWR-4413-005','rank':828,
         'corpora':metadata,'review_serialized_bytes':len(blob),'review_sha256':h(blob),
         'review_match':True,'serialization':'UTF-8 Python json.dumps([full problem record, reports.get(problem_number,{})], sort_keys=True), default separators and ensure_ascii',
         'report_entry_present':record['problem_number'] in reports,'report_fallback':'empty JSON object',
         'statement_utf8_bytes':len(statement),'statement_sha256':h(statement),'statement_match':True,
         'dataset_or_record_text_emitted':False}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for role in EXPECTED:p.add_argument('--'+role.replace('_','-'),type=Path,required=True)
 args=p.parse_args();print(json.dumps(run(vars(args)),indent=2,sort_keys=True))
