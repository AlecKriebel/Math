#!/usr/bin/env python3
"""Synthetic launcher tests; no real acceptance, upload, or service action."""
import argparse,contextlib,copy,hashlib,importlib.util,io,json,sys,tempfile,types
from datetime import datetime,timezone
from pathlib import Path
HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'
def need(x,s):
 if not x:raise RuntimeError(s)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--launcher',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--expect-pre-fix',action='store_true');args=ap.parse_args()
 spec=importlib.util.spec_from_file_location('synthetic_pr919_upload_launcher',args.launcher);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);rows=[]
 with tempfile.TemporaryDirectory(prefix='pr919-head-guard-') as td:
  a=Path(td);pub=a/'publication';pub.mkdir();repo=a/'repo';(repo/'zenodo_deposit_tool').mkdir(parents=True);(repo/'zenodo_deposit_tool/zenodo.py').write_text('# synthetic sentinel; never executed\n')
  (pub/'paper.pdf').write_bytes(b'SYNTHETIC_NOT_A_PAPER');(pub/'package.zip').write_bytes(b'SYNTHETIC_NOT_AN_ARCHIVE');desc={'files':[{'path':'paper.pdf','name':'paper.pdf'},{'path':'package.zip','name':'package.zip'}]};(pub/'zenodo-deposit.json').write_text(json.dumps(desc));files={n:{'bytes':(pub/n).stat().st_size,'sha256':digest(pub/n)} for n in ['paper.pdf','package.zip','zenodo-deposit.json']};freeze={'pr':919,'problem_id':'30002555','original_pr_head':HEAD,'files':files};(pub/'PREPUBLICATION_FREEZE.json').write_text(json.dumps(freeze));pin=digest(pub/'PREPUBLICATION_FREEZE.json');base={'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{}, {}, {}],'freeze_sha256':pin,'files':files};expected=[{'name':x['name'],'size':files[x['path']]['bytes'],'sha256':files[x['path']]['sha256']} for x in desc['files']];(a/'PUBLICATION_DISPOSITION.json').write_text(json.dumps({'decision':'PREPARE_EXPLICITLY_ATTRIBUTED_APPLICATION_NOTE'}));m.A=a;m.D=pub;m.ROOT=repo
  valid={'accepted':True,'original_audited_head':HEAD,'integrated_head':'b'*40}
  cases=[('original_head_positive',True,HEAD,None,{},{}),('stale_wrong_PR919_head',False,'0'*40,None,{},{}),('accepted_integration_positive',True,'b'*40,valid,{},{}),('wrong_PR',False,HEAD,None,{}, {'number':920}),('unaccepted_integration',False,'b'*40,{**valid,'accepted':False},{},{}),('wrong_original_integration',False,'b'*40,{**valid,'original_audited_head':'0'*40},{},{}),('malformed_integration_head',False,'not_a_commit',{**valid,'integrated_head':'not_a_commit'},{},{}),('stale_original_after_integration',False,HEAD,valid,{},{}),('unaccepted_candidate',False,HEAD,None,{'accepted':False},{}),('wrong_accepted_original',False,HEAD,None,{'original_pr_head':'0'*40},{}),('unmerged_PR',False,HEAD,None,{}, {'state':'OPEN'})]
  if args.expect_pre_fix:cases=cases[:2]
  for action in ['stage','publish','inspect']:
   for label,positive,head,add,achange,mchange in cases:
    addpath=a/'ACCEPTANCE_INTEGRATION_ADDENDUM.json'
    if addpath.exists():addpath.unlink()
    if add is not None:addpath.write_text(json.dumps(add))
    (a/'ACCEPTANCE.json').write_text(json.dumps({**base,**achange}));(a/'PR_MERGE_RECEIPT.json').write_text(json.dumps({'state':'MERGED','number':919,'headRefOid':head,'mergeCommit':{'oid':'a'*40},**mchange}));(pub/'ZENODO_STAGE.json').write_text(json.dumps({'id':101,'files':expected}));intent=pub/('ZENODO_'+action.upper()+'_INTENT.json')
    if intent.exists():intent.unlink()
    calls=[]
    def sentinel(command,**kwargs):
     calls.append(command);need(command[2]==action,'Wrong mocked kit action')
     if action=='publish':need(command[-2:]==['--confirm-id','101'],'Lost exact staged ID guard')
     return types.SimpleNamespace(returncode=0,stdout=json.dumps({'id':101,'state':'ready_to_publish' if action=='stage' else 'published','doi':'10.5281/zenodo.101','record_url':'https://zenodo.org/records/101','files':expected}),stderr='')
    m.subprocess=types.SimpleNamespace(run=sentinel);old=sys.argv;sys.argv=[str(args.launcher),action];error=None
    try:
     with contextlib.redirect_stdout(io.StringIO()):m.main()
    except RuntimeError as e:error=str(e)
    finally:sys.argv=old
    expected_reach=positive or (args.expect_pre_fix and label=='stale_wrong_PR919_head');need(bool(calls)==expected_reach,action+':'+label);need(len(calls)<=1,'Repeated mocked action');need(intent.exists()==expected_reach,'Rejected case wrote a kit intent');rows.append({'action':action,'case':label,'expected_kit_reached':expected_reach,'mocked_kit_reached':bool(calls),'guard':error,'actual_external_action':False})
 out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_REPRODUCED_PRE_FIX_GAP' if args.expect_pre_fix else 'PASS_REPAIRED_PUBLICATION_HEAD_GUARD','launcher_sha256':digest(args.launcher),'positive_cases':sum(r['mocked_kit_reached'] for r in rows),'negative_rejections':sum(not r['mocked_kit_reached'] for r in rows),'all_fixtures_synthetic':True,'no_service_contact_or_real_acceptance_merge_publication_receipt':True,'rows':rows};args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
