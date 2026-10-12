"""Acquire one immutable source commit; no main/index/remote ref mutation."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;C=A.parents[2]
HEAD='d110ad761291aa6ac1d66d2a49e8b8212c18bed6';GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
D=A/'actual_original_object_acquisition_20261006';events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(args):
    start=now();child=subprocess.Popen([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
    events.append({'argv':[GIT,*args],'PID':child.pid,'UTC_start':start,'UTC_end':now(),'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf-8','replace')})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events});require(child.returncode==0,'Actual source-object acquisition failed');return out
require(not D.exists(),'Existing acquisition; inspect rather than repeat')
D.mkdir()
before=run(['rev-parse','HEAD']);refs=run(['show-ref']);index=run(['diff','--cached','--name-only','-z']);dirty=run(['diff','--name-only','--diff-filter=ACMRTUXB','-z'])
require(run(['branch','--show-current']).strip()==b'main','Not main')
run(['fetch','--no-tags','--no-write-fetch-head','origin',HEAD])
require(run(['cat-file','-t',HEAD]).strip()==b'commit','Exact requested immutable commit unavailable')
require(run(['rev-parse','HEAD'])==before and run(['show-ref'])==refs and run(['diff','--cached','--name-only','-z'])==index and run(['diff','--name-only','--diff-filter=ACMRTUXB','-z'])==dirty,'Main/ref/index/materialized invariance failed')
receipt={'schema':'pr124-actual-source-object-acquisition/v1','UTC':now(),'actual_operator_PID':os.getpid(),'immutable_head':HEAD,'main_unchanged':before.decode().strip(),'refs_index_and_materialized_tracked_changes_unchanged':True,'Git_object_database_write_only':True,'remote_ref_mutations':False,'primary_checkout_mutated':False,'initial_read_only_inventory_missing_object_probe_preserved_as_tool_exit128':True}
dump(D/'RECEIPT.json',receipt);print(json.dumps(receipt,sort_keys=True))
