#!/usr/bin/env python3
"""Use the repository kit only for an accepted, merged, unchanged PR909 package."""
import argparse
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
ROOT=P.parent
A=P/'audits/pr909_30001345'
D=A/'publication'
HEAD='d186dea31791cd3e8acf6829e0b65d01849623b8'
def require(x,label):
 if not x:raise RuntimeError(label)
def sha(path):
 require(path.is_file() and not path.is_symlink(),'Nonregular accepted file')
 return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=['stage','publish','inspect']);args=ap.parse_args()
 accepted=json.loads((A/'ACCEPTANCE.json').read_text())
 require(accepted.get('accepted') is True and accepted['original_pr_head']==HEAD,'Final exact acceptance absent')
 require(len(accepted['full_package_reviews'])>=2,'Sequential fresh reviews absent')
 require(sha(D/'PREPUBLICATION_FREEZE.json')==accepted['freeze_sha256'],'Accepted freeze changed')
 freeze=json.loads((D/'PREPUBLICATION_FREEZE.json').read_text())
 for name,pin in freeze['files'].items():
  require(sha(D/name)==pin['sha256'] and (D/name).stat().st_size==pin['bytes'],'Accepted release changed: '+name)
 merge=json.loads((A/'PR_MERGE_RECEIPT.json').read_text())
 require(merge['state']=='MERGED' and merge['number']==909,'Merge not confirmed')
 decision=json.loads((A/'PUBLICATION_DISPOSITION.json').read_text())
 require(decision['decision']=='EVALUATE_AND_IF_ALL_FINAL_GATES_PASS_ACCEPT_EXPLICITLY_ATTRIBUTED_CLASSICAL_COROLLARY','Outcome disposition changed')
 descriptor=D/'zenodo-deposit.json'
 command=['python3',str(ROOT/'zenodo_deposit_tool/zenodo.py'),args.action,str(descriptor)]
 if args.action=='publish':
  stage=json.loads((D/'ZENODO_STAGE.json').read_text());ident=stage['id']
  require(type(ident) is int and ident>0,'Exact staged record ID absent')
  command += ['--confirm-id',str(ident)]
 elif args.action=='inspect':command+=['--check-doi']
 intent={'utc':datetime.now(timezone.utc).isoformat(),'action':args.action,'pr':909,'accepted_freeze_sha256':accepted['freeze_sha256'],'descriptor_sha256':sha(descriptor),'repository_kit_sha256':sha(ROOT/'zenodo_deposit_tool/zenodo.py'),'merged_commit':merge['mergeCommit']['oid'],'blind_retry_permitted':False}
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
