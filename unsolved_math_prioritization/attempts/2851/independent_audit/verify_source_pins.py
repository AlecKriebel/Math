#!/usr/bin/env python3
"""Recheck exact corpus and locally supplied source PDF pins without emitting source content.
Run with --catalog FILE --problems FILE --research FILE --pdf-dir DIRECTORY.
The PDF directory uses the five basenames below. This is a byte/record check, not proof inspection.
"""
import argparse
import hashlib
import json
from pathlib import Path
PINS={
 'catalog':(21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
 'problems':(68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
 'research':(80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')}
PDFS={
 'k3.pdf':(6578041,'ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f'),
 'greene_levine.pdf':(600681,'fc8e2618e82d24082b1d5ef086ab95c0661f278bad0497f1e8c6032815e41602'),
 'usui.pdf':(1177207,'4e88347bb17975127f2e59249123a58482680e5c5de957236fc570144ba55303'),
 'pfaffian_extended.pdf':(71913,'57d377b0bcc2df6b3a5cd9a55f925fe6bd50867a5fb2034db4cd6753b6eddb44'),
 'agol_chainmail.pdf':(3710927,'d2ba33c5e6b87a7f341ac972889cc757664d026127143b9305152f4484d8737c')}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def check(path,pin):
 b=path.read_bytes();need((len(b),hashlib.sha256(b).hexdigest())==pin,'byte pin mismatch')
 return b

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in PINS:p.add_argument('--'+n,type=Path,required=True)
 p.add_argument('--pdf-dir',type=Path,required=True);args=p.parse_args()
 data={n:json.loads(check(getattr(args,n),pin)) for n,pin in PINS.items()}
 c=[x for x in data['catalog'] if str(x.get('id'))=='2851']; r=[x for x in data['problems'] if x.get('id')==2851]
 need(len(c)==len(r)==1,'record uniqueness failed');record=r[0];report=data['research'].get('KP-3.53',{})
 pair=hashlib.sha256(json.dumps([record,report],sort_keys=True).encode()).hexdigest()
 statement=hashlib.sha256(record['statement'].encode()).hexdigest()
 need(pair=='7460a0bc185952a828d87e51464d3bd948cbc0f04c0bc240f02f8e3101009e4d','pair mismatch')
 need(statement=='25030a65a9e9bd04e0ddf7966ce6e3cd2a3d4563df3bc66756fe0d5bf94345b1','statement mismatch')
 need(c[0]['review_hash']==pair and c[0]['statement_hash']==statement and c[0]['rank']==914,'catalog linkage mismatch')
 need(record['problem_number']==c[0]['problem_number']=='KP-3.53' and report=={},'record/report linkage mismatch')
 for name,pin in PDFS.items():need(check(args.pdf_dir/name,pin).startswith(b'%PDF-'),'source is not a PDF')
 print(json.dumps({'problem_id':2851,'rank':914,'status':'PASS_EXACT_SOURCE_AND_CORPUS_PINS',
  'complete_corpora_checked':{n:{'bytes':pin[0],'sha256':pin[1]} for n,pin in PINS.items()},
  'source_pdf_pins_checked':{n:{'bytes':pin[0],'sha256':pin[1]} for n,pin in PDFS.items()},
  'complete_record_count':1,'catalog_record_count':1,'complete_report_empty':True,
  'record_report_pair_sha256':pair,'statement_sha256':statement,
  'pair_serialization':'default json.dumps([complete_record, reports.get(problem_number,{})], sort_keys=True), UTF-8',
  'scope':'Exact local bytes and full parsed records checked; intellectual/source inspection is reported separately.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
