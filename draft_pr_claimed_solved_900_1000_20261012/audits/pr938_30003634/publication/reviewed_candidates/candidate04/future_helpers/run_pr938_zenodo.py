#!/usr/bin/env python3
"""Use the repository kit only for an accepted, merged, unchanged PR938 package."""
import argparse
from datetime import datetime,timezone
import hashlib,json,re
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
ROOT=P.parent
A=P/'audits/pr938_30003634'
D=A/'publication'
HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
def require(x,label):
 if not x:raise RuntimeError(label)
def sha(path):
 require(path.is_file() and not path.is_symlink(),'Nonregular accepted file')
 return hashlib.sha256(path.read_bytes()).hexdigest()
def require_main_merged_record(record,expected_head,expected_commit=None):
 require(type(record.get('number')) is int and record['number']==938 and record.get('state')=='MERGED' and record.get('baseRefName')=='main','Merged PR destination must be exactly main')
 require(record.get('headRefOid')==expected_head,'Merged head differs from accepted head')
 commit=record.get('mergeCommit',{}).get('oid')
 require(type(commit) is str and re.fullmatch('[0-9a-f]{40}',commit) is not None,'Merged commit identity missing')
 if expected_commit is not None:require(commit==expected_commit,'Fresh destination readback has different merge commit')
 return commit
def confirm_main_destination(merge,expected_head):
 commit=require_main_merged_record(merge,expected_head)
 def read(command):return subprocess.run(command,cwd=ROOT,check=True,capture_output=True,text=True).stdout
 live=json.loads(read(['gh','pr','view','938','--repo','AlecKriebel/Math','--json','number,state,headRefOid,baseRefName,mergeCommit']))
 require_main_merged_record(live,expected_head,commit)
 remote_main=read(['git','ls-remote','origin','refs/heads/main']).split()[0]
 read(['git','fetch','--no-write-fetch-head','origin',remote_main])
 read(['git','merge-base','--is-ancestor',commit,remote_main])
 return {'utc':datetime.now(timezone.utc).isoformat(),'baseRefName':'main','actual_PR_readback':live,'merge_commit':commit,'observed_remote_main':remote_main,'merge_commit_is_ancestor_of_observed_main':True}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=['stage','publish','inspect']);args=ap.parse_args()
 accepted=json.loads((A/'ACCEPTANCE.json').read_text())
 require(accepted.get('accepted') is True and accepted['original_pr_head']==HEAD,'Final exact acceptance absent')
 require(len(accepted['full_package_reviews'])>=2,'Sequential fresh reviews absent')
 require(sha(D/'PREPUBLICATION_FREEZE.json')==accepted['freeze_sha256'],'Accepted freeze changed')
 freeze=json.loads((D/'PREPUBLICATION_FREEZE.json').read_text())
 require(freeze['future_helpers']==accepted['future_helpers'],'Accepted operational helper inventory changed')
 for name,pin in freeze['future_helpers'].items():require(sha(P/name)==pin['sha256'] and (P/name).stat().st_size==pin['bytes'],'Reviewed operational helper changed: '+name)
 for name,pin in freeze['files'].items():
  require(sha(D/name)==pin['sha256'] and (D/name).stat().st_size==pin['bytes'],'Accepted release changed: '+name)
 merge=json.loads((A/'PR_MERGE_RECEIPT.json').read_text())
 require(merge['state']=='MERGED' and merge['number']==938,'Merge not confirmed')
 expected_head=HEAD
 integration=A/'ACCEPTANCE_INTEGRATION_ADDENDUM.json'
 if integration.exists():
  addendum=json.loads(integration.read_text())
  require(addendum.get('accepted') is True and addendum['original_audited_head']==HEAD,'Integration review not accepted')
  expected_head=addendum['integrated_head']
 require(type(expected_head) is str and re.fullmatch('[0-9a-f]{40}',expected_head) is not None,'Malformed accepted merged head')
 require(merge.get('headRefOid')==expected_head,'Merged head differs from accepted original/integration head')
 destination=confirm_main_destination(merge,expected_head)
 decision=json.loads((A/'PUBLICATION_DISPOSITION.json').read_text())
 require(decision['decision']=='PREPARE_ALL_FINITE_DERIVED_DEPTH_RESEARCH_NOTE','Outcome disposition changed')
 descriptor=D/'zenodo-deposit.json'
 command=['python3',str(ROOT/'zenodo_deposit_tool/zenodo.py'),args.action,str(descriptor)]
 if args.action=='publish':
  stage=json.loads((D/'ZENODO_STAGE.json').read_text());ident=stage['id']
  require(type(ident) is int and ident>0,'Exact staged record ID absent')
  command += ['--confirm-id',str(ident)]
 elif args.action=='inspect':command+=['--check-doi']
 intent={'utc':datetime.now(timezone.utc).isoformat(),'action':args.action,'pr':938,'original_pr_head':HEAD,'accepted_merged_head':expected_head,'accepted_freeze_sha256':accepted['freeze_sha256'],'descriptor_sha256':sha(descriptor),'repository_kit_sha256':sha(ROOT/'zenodo_deposit_tool/zenodo.py'),'merged_commit':merge['mergeCommit']['oid'],'merged_base':'main','destination_readback':destination,'blind_retry_permitted':False}
 (D/('ZENODO_'+args.action.upper()+'_INTENT.json')).write_text(json.dumps(intent,indent=2)+'\n')
 result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
 if result.returncode!=0:
  # The kit already redacts credentials/HTML. Preserve uncertainty; never repeat
  # a publication request automatically to work around a failed receipt.
  failure={**intent,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'instruction':'Read back using the repository kit and reconcile before another write.'}
  (D/('ZENODO_'+args.action.upper()+'_FAILURE.json')).write_text(json.dumps(failure,indent=2)+'\n')
  raise RuntimeError('Kit action did not report success; inspect saved failure before proceeding')
 receipt=json.loads(result.stdout)
 if args.action=='publish':
  require(receipt['state']=='published','Published state not confirmed')
  require(type(receipt['id']) is int and receipt['doi']==f"10.5281/zenodo.{receipt['id']}",'Unexpected DOI/ID')
 if args.action=='publish':
  require(receipt['id']==ident,'Published record differs from staged exact ID')
 if args.action in ('stage','publish'):
  require(len(receipt['files'])==2,'Unexpected published file count')
 (D/('ZENODO_'+args.action.upper()+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'action':args.action,'id':receipt.get('id'),'state':receipt.get('state'),'doi':receipt.get('doi'),'record_url':receipt.get('record_url'),'receipt_saved_in_own_audit':True},indent=2))
if __name__=='__main__':main()
