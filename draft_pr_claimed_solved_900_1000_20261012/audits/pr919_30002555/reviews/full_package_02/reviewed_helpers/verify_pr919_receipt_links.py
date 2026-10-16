#!/usr/bin/env python3
"""Synthetic local receipt-substitution checks; never contact any service."""
import argparse,ast,copy,hashlib,json,tempfile
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parent
HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();rows=[];sources={}
 for name in ['append_pr919_tracker.py','update_pr919_publication_ledger.py','finalize_pr919_and_gate_next.py']:
  raw=(P/name).read_text();tree=ast.parse(raw);node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='verify_receipt_links');source=ast.get_source_segment(raw,node);sources[name]=source
 if len(set(sources.values()))!=1:raise RuntimeError('Downstream guards differ')
 ns={'json':json,'hashlib':hashlib};exec(next(iter(sources.values())),ns);verify=ns['verify_receipt_links']
 with tempfile.TemporaryDirectory(dir=P/'audits/pr919_30002555/publication/tmp',prefix='lineage-fixtures-') as td:
  root=Path(td);(root/'publication/output/pdf').mkdir(parents=True)
  def write(name,value):
   q=root/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(value,sort_keys=True)+'\n');return q.read_bytes()
  (root/'publication/output/pdf/note.pdf').write_bytes(b'SYNTHETIC_PDF_FIXTURE_NOT_A_PAPER');(root/'publication/package.zip').write_bytes(b'SYNTHETIC_ARCHIVE_FIXTURE')
  desc={'files':[{'path':'output/pdf/note.pdf','name':'paper.pdf'},{'path':'package.zip','name':'package.zip'}]};d=write('publication/zenodo-deposit.json',desc)
  files={n:{'bytes':len((root/'publication'/n).read_bytes()),'sha256':sha((root/'publication'/n).read_bytes())} for n in ['zenodo-deposit.json','output/pdf/note.pdf','package.zip']}
  freeze={'pr':919,'problem_id':'30002555','original_pr_head':HEAD,'files':files};pin=sha(write('publication/PREPUBLICATION_FREEZE.json',freeze))
  accepted={'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{},{}],'freeze_sha256':pin,'files':files}
  merged='a'*40;merge={'number':919,'state':'MERGED','headRefOid':HEAD,'mergeCommit':{'oid':merged}}
  expected=[{'name':x['name'],'size':files[x['path']]['bytes'],'sha256':files[x['path']]['sha256']} for x in desc['files']]
  doi='10.5281/zenodo.101';pub={'id':101,'state':'published','doi':doi,'record_url':'https://zenodo.org/records/101','files':expected}
  intent={'action':'publish','pr':919,'accepted_freeze_sha256':pin,'merged_commit':merged,'descriptor_sha256':sha(d)}
  stage={'id':101,'files':expected};inspect=copy.deepcopy(pub)
  tracker={'confirmed':True,'readback_matches':True,'pr':919,'problem_id':'30002555','original_pr_head':HEAD,'merged_head':HEAD,'merge_commit':merged,'accepted_freeze_sha256':pin,'doi':doi,'zenodo_record_id':101,'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','gid':1254632077,'tab_title':'Math Puzzles','row':['problem','','https://doi.org/'+doi,'notes'],'updated_range':"'Math Puzzles'!A2:D2"}
  native={'push_confirmed':True,'published_event':{'id':'30002555','pr':919,'doi':doi,'original_pr_head':HEAD,'accepted_freeze_sha256':pin,'merged_commit':merged,'zenodo_record_id':101,'evidence':{'tracker_range':tracker['updated_range']}}}
  baseline=[pub,merge,accepted,tracker,native,intent,stage,inspect,{'values':[tracker['row']]}]
  cases=[('wrong_merge_PR',1,['number'],920),('wrong_merge_head',1,['headRefOid'],'0'*40),('wrong_acceptance_head',2,['original_pr_head'],'0'*40),('wrong_acceptance_freeze',2,['freeze_sha256'],'0'*64),('wrong_published_DOI',0,['doi'],'10.5281/zenodo.102'),('wrong_published_file',0,['files',0,'sha256'],'0'*64),('wrong_intent_PR',5,['pr'],920),('wrong_intent_freeze',5,['accepted_freeze_sha256'],'0'*64),('wrong_intent_merge',5,['merged_commit'],'0'*40),('wrong_intent_descriptor',5,['descriptor_sha256'],'0'*64),('wrong_stage_ID',6,['id'],102),('wrong_inspect_DOI',7,['doi'],'10.5281/zenodo.102'),('wrong_tracker_PR',3,['pr'],920),('wrong_tracker_problem',3,['problem_id'],'other'),('wrong_tracker_head',3,['original_pr_head'],'0'*40),('wrong_tracker_freeze',3,['accepted_freeze_sha256'],'0'*64),('wrong_tracker_DOI',3,['doi'],'10.5281/zenodo.102'),('wrong_tracker_gid',3,['gid'],0),('wrong_tracker_readback',8,['values'],[['different']]),('wrong_native_PR',4,['published_event','pr'],920),('wrong_native_problem',4,['published_event','id'],'other'),('wrong_native_head',4,['published_event','original_pr_head'],'0'*40),('wrong_native_freeze',4,['published_event','accepted_freeze_sha256'],'0'*64),('wrong_native_DOI',4,['published_event','doi'],'10.5281/zenodo.102'),('wrong_native_merge',4,['published_event','merged_commit'],'0'*40),('wrong_native_record_ID',4,['published_event','zenodo_record_id'],102),('wrong_native_tracker',4,['published_event','evidence','tracker_range'],'wrong')]
  for label,index,path,value in [('unchanged',None,None,None),*cases]:
   data=copy.deepcopy(baseline)
   if index is not None:
    target=data[index]
    for key in path[:-1]:target=target[key]
    target[path[-1]]=value
   for name,item in zip(['publication/ZENODO_PUBLISH_INTENT.json','publication/ZENODO_STAGE.json','publication/ZENODO_INSPECT.json','TRACKER_READBACK.json'],data[5:]):write(name,item)
   rejected=False
   try:verify(root,*data[:5])
   except RuntimeError as error:
    if not str(error).startswith('PR919 receipt linkage:'):raise
    rejected=True
   if rejected!=(index is not None):raise RuntimeError('Unexpected lineage outcome '+label)
   rows.append({'case':label,'rejected':rejected,'passed':True})
 result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','identical_guards_in_three_helpers':True,'positive_fixtures':1,'stale_or_cross_target_rejections':len(cases),'fixtures_are_synthetic_not_publication_receipts':True,'no_network_or_external_actions':True,'guard_source_sha256':sha(next(iter(sources.values())).encode()),'rows':rows};args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
