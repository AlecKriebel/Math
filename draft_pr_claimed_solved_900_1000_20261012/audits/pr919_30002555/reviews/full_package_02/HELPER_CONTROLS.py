#!/usr/bin/env python3
"""Safe synthetic helper tests. Every external action is replaced by a sentinel."""
import ast,copy,hashlib,importlib.util,json,sys,tempfile,types
from pathlib import Path
D=Path(__file__).resolve().parent;H=D/'reviewed_helpers';HEAD='704685791ec0053dc0a52590fdef49ed4aae61d9'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,s):
 if not x:raise RuntimeError(s)
def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path);args=ap.parse_args();R=(args.output_dir or D).resolve();R.mkdir(parents=True,exist_ok=True)
 rows=[]
 # Extend the actual root's downstream receipt harness through AST without rewriting helpers.
 tree=ast.parse((H/'verify_pr919_receipt_links.py').read_text())
 for node in ast.walk(tree):
  if isinstance(node,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='cases' for x in node.targets):
   node.value.elts += [ast.parse(repr(x),mode='eval').body for x in [('wrong_record_URL',0,['record_url'],'https://zenodo.org/records/102'),('wrong_stage_file',6,['files',0,'sha256'],'0'*64),('wrong_inspection_ID',7,['id'],102),('wrong_inspection_file',7,['files',1,'size'],0),('wrong_tracker_merge',3,['merge_commit'],'0'*40),('wrong_tracker_record',3,['zenodo_record_id'],102),('unconfirmed_native_push',4,['push_confirmed'],False),('unconfirmed_acceptance',2,['accepted'],False)]]
 ns={'__file__':str(H/'verify_pr919_receipt_links.py'),'__name__':'synthetic_extended'};exec(compile(ast.fix_missing_locations(tree),'extended_root_fixture','exec'),ns);old=sys.argv;sys.argv=[str(H/'verify_pr919_receipt_links.py'),'--output',str(R/'RECEIPT_LINK_EXTENDED_TEST.json')]
 try:ns['main']()
 finally:sys.argv=old
 # A forged/stale merge-head receipt should stop the Zenodo launcher before its kit call.
 spec=importlib.util.spec_from_file_location('zenodo_launcher_under_test',H/'run_pr919_zenodo.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 with tempfile.TemporaryDirectory(dir=D/'tmp',prefix='synthetic-helper-') as td:
  a=Path(td);pub=a/'publication';pub.mkdir();repo=a/'repo';(repo/'zenodo_deposit_tool').mkdir(parents=True);(repo/'zenodo_deposit_tool/zenodo.py').write_text('# synthetic kit sentinel, never executed\n')
  (pub/'paper.pdf').write_bytes(b'SYNTHETIC_NOT_A_PAPER');(pub/'package.zip').write_bytes(b'SYNTHETIC_NOT_AN_ARCHIVE')
  desc={'files':[{'path':'paper.pdf','name':'paper.pdf'},{'path':'package.zip','name':'package.zip'}]};(pub/'zenodo-deposit.json').write_text(json.dumps(desc))
  files={n:{'bytes':len((pub/n).read_bytes()),'sha256':sha((pub/n).read_bytes())} for n in ['paper.pdf','package.zip','zenodo-deposit.json']};freeze={'pr':919,'problem_id':'30002555','original_pr_head':HEAD,'files':files};(pub/'PREPUBLICATION_FREEZE.json').write_text(json.dumps(freeze));pin=sha((pub/'PREPUBLICATION_FREEZE.json').read_bytes());(a/'ACCEPTANCE.json').write_text(json.dumps({'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{},{}],'freeze_sha256':pin,'files':files}));(a/'PUBLICATION_DISPOSITION.json').write_text(json.dumps({'decision':'PREPARE_EXPLICITLY_ATTRIBUTED_APPLICATION_NOTE'}))
  expected=[{'name':x['name'],'size':files[x['path']]['bytes'],'sha256':files[x['path']]['sha256']} for x in desc['files']];(pub/'ZENODO_STAGE.json').write_text(json.dumps({'id':101,'files':expected}));m.A=a;m.D=pub;m.ROOT=repo
  for label,number,head in [('correct_head_baseline',919,HEAD),('stale_wrong_PR919_head',919,'0'*40),('wrong_PR_negative',920,HEAD)]:
   merge={'state':'MERGED','number':number,'headRefOid':head,'mergeCommit':{'oid':'a'*40}};(a/'PR_MERGE_RECEIPT.json').write_text(json.dumps(merge))
   calls=[]
   def sentinel(command,**kw):
    calls.append(command);return types.SimpleNamespace(returncode=0,stdout=json.dumps({'id':101,'state':'published','doi':'10.5281/zenodo.101','record_url':'https://zenodo.org/records/101','files':expected}),stderr='')
   m.subprocess=types.SimpleNamespace(run=sentinel);old=sys.argv;sys.argv=['run_pr919_zenodo.py','publish'];caught=None
   try:m.main()
   except RuntimeError as e:caught=str(e)
   finally:sys.argv=old
   need((len(calls)==1)==(number==919),label)
   rows.append({'case':label,'kit_publish_invocation_reached':bool(calls),'actual_external_action':False,'guard':caught})
 out={'status':'PASS_REPRODUCED_OPTIONAL_SEQUENCING_GAP','all_fixtures_synthetic':True,'no_service_contact_or_real_publication_receipt':True,'rows':rows,'finding':'run_pr919_zenodo.py validates merged PR number/state but not headRefOid against the accepted original/integration head before invoking publish. Its downstream guards detect this only after publication. Under the intended trusted sequence the merge helper creates the correct receipt; this is optional stale-receipt hardening, not a mathematical gap or evidence of actual wrong publication.'};(R/'HELPER_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
