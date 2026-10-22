#!/usr/bin/env python3
"""Synthetic third-round helper tests. External subprocesses are sentinels."""
import argparse,ast,contextlib,copy,hashlib,importlib.util,io,json,pathlib,shutil,sys,tempfile,types
R=pathlib.Path(__file__).resolve().parent;HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'
def need(x,s):
 if not x:raise RuntimeError(s)
def module(n):
 s=importlib.util.spec_from_file_location('review03_'+n,R/'reviewed_helpers'/n);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def perform():
 rows=[];S=R/'private/helper_controls';S.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(dir=S) as td:
  a=pathlib.Path(td);pub=a/'publication';pub.mkdir();repo=a/'repo';(repo/'zenodo_deposit_tool').mkdir(parents=True);(repo/'zenodo_deposit_tool/zenodo.py').write_text('# test sentinel only')
  def write(n,v):
   q=a/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(v));return q.read_bytes()
  data=b'SYNTHETIC_ONLY';(pub/'paper').write_bytes(data);(pub/'archive').write_bytes(data)
  desc={'files':[{'path':'paper','name':'paper'},{'path':'archive','name':'archive'}]};write('publication/zenodo-deposit.json',desc)
  files={n:{'bytes':len((pub/n).read_bytes()),'sha256':hashlib.sha256((pub/n).read_bytes()).hexdigest()} for n in ['paper','archive','zenodo-deposit.json']}
  f={'pr':919,'problem_id':'30002555','original_pr_head':HEAD,'files':files};fraw=write('publication/PREPUBLICATION_FREEZE.json',f);pin=hashlib.sha256(fraw).hexdigest()
  accepted={'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{}, {}, {}],'freeze_sha256':pin,'files':files}
  expected=[{'name':n,'size':len(data),'sha256':hashlib.sha256(data).hexdigest()} for n in ['paper','archive']]
  doi='10.5281/zenodo.217';p={'id':217,'state':'published','doi':doi,'record_url':'https://zenodo.org/records/217','files':expected}
  merge={'number':919,'state':'MERGED','headRefOid':HEAD,'mergeCommit':{'oid':'a'*40}}
  intent={'action':'publish','pr':919,'accepted_freeze_sha256':pin,'merged_commit':'a'*40,'descriptor_sha256':files['zenodo-deposit.json']['sha256']}
  tracker={'confirmed':True,'readback_matches':True,'pr':919,'problem_id':'30002555','original_pr_head':HEAD,'merged_head':HEAD,'merge_commit':'a'*40,'accepted_freeze_sha256':pin,'doi':doi,'zenodo_record_id':217,'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','gid':1254632077,'tab_title':'Math Puzzles','row':['p','','https://doi.org/'+doi,'n'],'updated_range':"'Math Puzzles'!A8:D8"}
  native={'push_confirmed':True,'published_event':{'id':'30002555','pr':919,'doi':doi,'original_pr_head':HEAD,'accepted_freeze_sha256':pin,'merged_commit':'a'*40,'zenodo_record_id':217,'evidence':{'tracker_range':tracker['updated_range']}}}
  base=[p,merge,accepted,tracker,native,intent,{'id':217,'files':expected},copy.deepcopy(p),{'values':[tracker['row']]}]
  downstream=[module(n) for n in ['append_pr919_tracker.py','update_pr919_publication_ledger.py','finalize_pr919_and_gate_next.py']]
  def reset(v):
   for n,x in zip(['publication/ZENODO_PUBLISH_INTENT.json','publication/ZENODO_STAGE.json','publication/ZENODO_INSPECT.json','TRACKER_READBACK.json'],v[5:]):write(n,x)
  cases=[('native_push_false',4,['push_confirmed'],False),('tracker_confirmation_false',3,['confirmed'],False),('tracker_readback_false',3,['readback_matches'],False),('wrong_record_URL',0,['record_url'],'https://zenodo.org/records/218'),('publish_ID_boolean',0,['id'],True),('tracker_recordID',3,['zenodo_record_id'],218),('tracker_merged_head',3,['merged_head'],'b'*40),('tracker_merge_commit',3,['merge_commit'],'b'*40),('tracker_spreadsheet',3,['spreadsheet_id'],'other'),('tracker_title',3,['tab_title'],'other'),('tracker_DOIcell',3,['row',2],'https://doi.org/other'),('native_merge',4,['published_event','merged_commit'],'b'*40),('inspect_state',7,['state'],'draft'),('stage_fingerprint',6,['files',1,'sha256'],'0'*64),('inspect_recordID',7,['id'],218),('intent_action',5,['action'],'stage')]
  for m in downstream:
   reset(base);m.verify_receipt_links(a,*base[:5]);rows.append({'helper':m.__file__.split('/')[-1],'case':'positive_chain','passed':True})
   for name,index,path,value in cases:
    v=copy.deepcopy(base);x=v[index]
    for k in path[:-1]:x=x[k]
    x[path[-1]]=value;reset(v);caught=None
    try:m.verify_receipt_links(a,*v[:5])
    except RuntimeError as e:caught=str(e)
    need(caught and caught.startswith('PR919 receipt linkage:'),name);rows.append({'helper':pathlib.Path(m.__file__).name,'case':name,'rejected':True})
   # Integration must update every dependent head, not just the merge receipt.
   write('ACCEPTANCE_INTEGRATION_ADDENDUM.json',{'accepted':True,'original_audited_head':HEAD,'integrated_head':'b'*40});v=copy.deepcopy(base);v[1]['headRefOid']='b'*40;v[3]['merged_head']='b'*40;reset(v);m.verify_receipt_links(a,*v[:5]);rows.append({'helper':pathlib.Path(m.__file__).name,'case':'integrated_positive_chain','passed':True});(a/'ACCEPTANCE_INTEGRATION_ADDENDUM.json').unlink()
  launcher=module('run_pr919_zenodo.py');launcher.A=a;launcher.D=pub;launcher.ROOT=repo;write('PUBLICATION_DISPOSITION.json',{'decision':'PREPARE_EXPLICITLY_ATTRIBUTED_APPLICATION_NOTE'})
  for action in ['stage','publish','inspect']:
   for case,head,add,positive in [('original_positive',HEAD,None,True),('integrated_positive','c'*40,{'accepted':True,'original_audited_head':HEAD,'integrated_head':'c'*40},True),('stale_integration_receipt','b'*40,{'accepted':True,'original_audited_head':HEAD,'integrated_head':'c'*40},False),('wrong_no_addendum_head','0'*40,None,False),('malformed_integrated_head','c'*39,{'accepted':True,'original_audited_head':HEAD,'integrated_head':'c'*39},False)]:
    q=a/'ACCEPTANCE_INTEGRATION_ADDENDUM.json'
    if q.exists():q.unlink()
    if add:write('ACCEPTANCE_INTEGRATION_ADDENDUM.json',add)
    write('ACCEPTANCE.json',accepted);write('PR_MERGE_RECEIPT.json',{**merge,'headRefOid':head});write('publication/ZENODO_STAGE.json',{'id':217,'files':expected})
    ip=pub/('ZENODO_'+action.upper()+'_INTENT.json')
    if ip.exists():ip.unlink()
    calls=[]
    def sentinel(cmd,**kw):
     calls.append(cmd)
     if action=='publish':need(cmd[-2:]==['--confirm-id','217'],'exact staged ID')
     return types.SimpleNamespace(returncode=0,stdout=json.dumps(p),stderr='')
    launcher.subprocess=types.SimpleNamespace(run=sentinel);old=sys.argv;sys.argv=['launcher',action];error=None
    try:
     with contextlib.redirect_stdout(io.StringIO()):launcher.main()
    except RuntimeError as e:error=str(e)
    finally:sys.argv=old
    need(bool(calls)==positive and ip.exists()==positive,'launcher '+action+':'+case)
    if positive:need(json.loads(ip.read_text())['accepted_merged_head']==head,'intent linked head')
    rows.append({'helper':'run_pr919_zenodo.py','action':action,'case':case,'mocked_kit_reached':bool(calls),'intent_created_in_synthetic_fixture':ip.exists(),'guard':error,'passed':True})
 return {'status':'PASS','rows':rows,'downstream_negative_rejections':len(cases)*3,'downstream_positive_chains':6,'launcher_positive_mocked_actions':6,'launcher_negative_preintent_rejections':9,'all_fixtures_synthetic':True,'actual_external_actions':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path);a=p.parse_args();r=perform()
 if a.output:a.output.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k!='rows'},indent=2))
