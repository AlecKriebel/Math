#!/usr/bin/env python3
"""Publish only this shard's explicit paths atop current remote main.
The shared checkout, local main ref and shared index are never rewritten.
A failed non-fast-forward push is retained and retried on a fresh parent.
"""
import argparse,datetime,json,os,pathlib,subprocess,tempfile
ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parent

def run(args,*,env=None,input=None):
 return subprocess.check_output(args,cwd=REPO,env=env,input=input,text=True).strip()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('message');ap.add_argument('--paths',nargs='+',required=True);a=ap.parse_args()
 for p in a.paths:
  if pathlib.PurePosixPath(p).parts[0]!=ROOT.name:raise SystemExit('Refuse paths outside this shard')
 work=ROOT/'local_tools';work.mkdir(exist_ok=True)
 history=[]
 for attempt in range(5):
  run(['git','fetch','--no-tags','origin','main']);base=run(['git','rev-parse','origin/main'])
  with tempfile.TemporaryDirectory(dir=work) as td:
   env=dict(os.environ,GIT_INDEX_FILE=str(pathlib.Path(td)/'index'))
   run(['git','read-tree',base],env=env)
   run(['git','add','--',*a.paths],env=env)
   changed=run(['git','diff','--cached','--name-only',base],env=env).splitlines()
   if any(pathlib.PurePosixPath(p).parts[0]!=ROOT.name for p in changed):raise SystemExit('Unexpected staged path')
   if not changed:print(json.dumps({'result':'no_changes','base':base}));return
   tree=run(['git','write-tree'],env=env)
   commit=run(['git','commit-tree',tree,'-p',base],input=a.message+'\n')
  pr=subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=REPO,capture_output=True,text=True)
  history.append({'base':base,'commit':commit,'changed_paths':changed,'push_exit':pr.returncode})
  if pr.returncode==0:
   receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'pushed','commit':commit,'base':base,'attempts':history,'scope':'remote main; shared local branch/index/working files unchanged'}
   (ROOT/'LATEST_CHECKPOINT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt));return
  if 'non-fast-forward' not in pr.stderr and 'fetch first' not in pr.stderr and 'failed to update ref' not in pr.stderr:raise SystemExit(pr.stderr)
 raise SystemExit('Five concurrent main advances prevented publication; commits retained in objects')
if __name__=='__main__':main()
