#!/usr/bin/env python3
"""Pure offline read-only custody. No network, subprocesses, supplied code or own science execution."""
from pathlib import Path,PurePosixPath
import hashlib,json,struct,sys
R=Path(__file__).resolve().parent
S=R.parents[1]/'sources'
EXCLUDED={'FINAL_MANIFEST.json','FINAL_CLOSURE.json','FINAL_SEAL.json'}
N=0
def req(ok,message):
 global N
 N+=1
 if not ok:raise RuntimeError(message)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,item):
 name=PurePosixPath(item['path']);req(not name.is_absolute() and '..'not in name.parts and str(name)==item['path'],'Safe manifest name')
 p=root/name;req(p.resolve().is_relative_to(root)and not p.is_symlink(),'Owned regular path')
 req(p.is_file()and p.stat().st_size==item['bytes']and sha(p)==item['SHA256'],'Whole-byte binding '+str(p));return p
def main(preseal):
 manifest=load(R/'FINAL_MANIFEST.json');names=[]
 req(set(manifest['excluded_terminal_files'])==EXCLUDED,'Terminal exclusions')
 for item in manifest['files']:bind(R,item);names.append(item['path'])
 req(len(names)==len(set(names))and set(names)=={p.relative_to(R).as_posix()for p in R.rglob('*')if p.is_file()}-EXCLUDED,'Complete review namespace')
 initial=load(R/'INITIAL_SEAL.json')
 for item in initial['files']:bind(R,item)
 req(initial['materially_distinct_claims']>=8 and initial['stage']=='INITIAL_INDEPENDENT_RECONSTRUCTION','Early reconstruction extent')
 sourcebinding=load(R/'SOURCE_BINDING.json')
 for item in sourcebinding['terminal_source_files']:bind(S,item)
 source_manifest=load(S/'SOURCE_READY_MANIFEST.json');source_names=[]
 for item in source_manifest['files']:bind(S,item);source_names.append(item['path'])
 req(set(source_names)=={p.relative_to(S).as_posix()for p in S.rglob('*')if p.is_file()}-set(source_manifest['excluded_terminal_files']),'Complete immutable source namespace')
 req(sha(S/'SOURCE_READY.json')=='daf4295ead3b1f6c626bef12d6bb1f6796688aee7a56f04b5abd4f80c5d073f9','Original READY hash')
 req(sha(S/'SOURCE_READY_SEAL.json')=='47b3874516ef61b804e27e8980c013a6cae36edc9934c273938c73dcdff3ce24','Original source seal hash')
 ready=load(S/'SOURCE_READY.json');arc=load(S/'ARCHIVE_CUSTODY.json')
 req(ready['record_id']==23418581 and ready['sheet_row']==132,'Native row identity')
 req(len(arc['containers'])==4 and arc['nested_archive_count']==3 and arc['whole_regular_payload_occurrences']==243,'Complete four-container source extent')
 ledger=load(R/'PRIMARY_READ_LEDGER.json');req(ledger['foreign_sources_read_only_after_initial_seal']is True,'Primary chronology declaration')
 req(len(ledger['sources'])==4 and [x['key']for x in ledger['sources']]==['DD','MFO','CP','EL'],'Exact critical source extent')
 for source in ledger['sources']:bind(R,source['whole_object'])
 for role in ['DD','CP','MFO','EL']:
  receipts=load(R/'primary_raw'/(role+'.transports.json'));req(len(receipts)>=1,'Actual primary transport receipt')
  for receipt in receipts:
   req(receipt['method']=='GET'and receipt['transport_error']is None,'Ordinary successful primary GET')
   req(isinstance(receipt['request_headers_ordered'],list)and isinstance(receipt['response_headers_ordered'],list),'Ordered whole primary headers')
   p=Path(receipt['whole_body_path']);req(p.resolve().is_relative_to(R/'primary_raw')and p.stat().st_size==receipt['bytes']and sha(p)==receipt['SHA256'],'Complete primary response body')
  req(receipts[-1]['HTTP_status']==200,'Actual primary PDF HTTP200')
 text=load(R/'INITIAL_READ_LEDGER.json');req(text['actual_PDF_all_pages_read']==text['fresh_individual_rasters_all_read']==[1,2,3,4]and text['controlling_TeX_all_lines_read']==279,'Complete target read declaration')
 for i in [1,2,3,4]:
  b=(R/('page-'+str(i)+'.png')).read_bytes();req(b[:8]==b'\x89PNG\r\n\x1a\n'and all(struct.unpack('>II',b[16:24])),'Actual fresh individual PNG')
 result=load(R/'OWN_EXACT_RESULTS.json');req(result['status']=='OWN_EXACT_CHECKS_PASS'and result['checks']==7292 and len(result['rows'])==10,'Bounded own exact result extent')
 req(result['implementation_SHA256']==sha(R/'own_exact_checks.py'),'Own exact code/result binding')
 req(result['supplied_scientific_code_imports_or_execution']==[],'No supplied code execution')
 verdict=load(R/'CUSTOM_VERDICT.json');req(verdict['record_id']==23418581 and verdict['completion_percent']==100,'Review verdict identity')
 req(verdict['target_supplied_scientific_programmes_imported_or_executed']==[]and verdict['archived_or_peer_target_scientific_opinions_read']is False,'Declared exposure boundary')
 req(verdict['publication_authority']is False and verdict['substantive_findings_shared_before_OPEN']is False,'Family authority and CLOSED gate')
 if not preseal:
  seal=load(R/'FINAL_SEAL.json')
  for file,key in [('FINAL_MANIFEST.json','MANIFEST_SHA256'),('FINAL_CLOSURE.json','CLOSURE_SHA256'),('CUSTOM_VERDICT.json','CUSTOM_VERDICT_SHA256'),('REPORT.md','REPORT_SHA256'),('INITIAL_SEAL.json','INITIAL_SEAL_SHA256')]:req(sha(R/file)==seal[key],'Final seal')
  req(seal['owned_payload_count']==len(names),'Final owned extent')
 print(json.dumps({'status':'REVIEW_CUSTODY_PASS','record_id':23418581,'family':'scope_and_primary','mode':'preseal'if preseal else'sealed','checks':N,'owned_payload_count':len(names),'original_source_payload_count':len(source_names),'source_regular_ZIP_occurrences':243,'source_archive_containers':4,'primary_whole_PDF_objects':4,'network_requests':0,'writes':0,'scientific_programmes_executed':0},sort_keys=True))
if __name__=='__main__':
 req(sys.argv[1:]in[[],['--preseal']],'Usage: verify_custody.py [--preseal]')
 main(sys.argv[1:]==['--preseal'])
