"""Commit only the readback tool's repository-size repair to the prepared PR."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
PRE=Path(__file__).resolve().parent
ROOT=Path('/Users/alec/Documents/Math')
PUB=PRE.parent/'publication'
OUT=PUB/('native-readback-tool-repair-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
OUT.mkdir(exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
seq=0
def api(method,path,payload=None):
    global seq
    seq+=1;args=[GH,'api','--method',method,'repos/AlecKriebel/Math/'+path]
    if payload is not None:
        f=OUT/f'{seq:02d}-request.json';f.write_text(json.dumps(payload));args+=['--input',str(f)]
    r=subprocess.run(args,capture_output=True)
    (OUT/f'{seq:02d}-stdout.json').write_bytes(r.stdout)
    (OUT/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
    assert r.returncode==0,'Reconcile any uncertain native action before retry'
    return json.loads(r.stdout)
ready=json.loads((PUB/'PR_PREPARED.json').read_text())
head=ready['prepared_head']
pr=api('GET','pulls/248')
assert pr['state']=='open' and pr['draft'] and pr['head']['sha']==head
clear=json.loads((PRE/'FINAL_CLEARANCE.json').read_text())
for name,p in clear['candidate_files'].items():
    data=(PRE/name).read_bytes();assert len(data)==p['bytes'] and hashlib.sha256(data).hexdigest()==p['sha256']
helper=PRE/'verify_and_merge.py'
path=helper.relative_to(ROOT).as_posix()
data=helper.read_bytes()
oldpin=next(p for p in ready['included_owned_pins'] if p['path']==path)
assert hashlib.sha256(data).hexdigest()!=oldpin['sha256']
tree=api('POST','git/trees',{'base_tree':ready['tree'],'tree':[{'path':path,'mode':'100644','type':'blob','content':data.decode()}]})['sha']
commit=api('POST','git/commits',{'message':'Scope exact native readback to PR248 subtree after full-repository listing truncation','tree':tree,'parents':[head]})['sha']
assert api('GET','pulls/248')['head']['sha']==head
attempt={'utc':datetime.now(timezone.utc).isoformat(),'previous_head':head,'new_head':commit,'new_tree':tree,'only_changed_path':path,'old_pin':oldpin.copy(),'new_pin':{'path':path,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()},'scientific_candidate5_unchanged':True,'source_packet20_unchanged':True,'earlier_failed_readbacks_only_GET_calls':True,'branch_mutation':'about to be attempted'}
(PUB/'NATIVE_READBACK_SCOPE_REPAIR_ATTEMPT.json').write_text(json.dumps(attempt,indent=2)+'\n')
result=api('PATCH','git/refs/heads/'+pr['head']['ref'],{'sha':commit,'force':False})
assert result['object']['sha']==commit
oldpin.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
ready.update(previous_prepared_head=head,prepared_head=commit,tree=tree,readback_tool_scope_repair=attempt['new_pin'])
(PUB/'PR_PREPARED.json').write_text(json.dumps(ready,indent=2)+'\n')
attempt.update(branch_mutation='verified nonforce fast-forward',native_merge_pending=True)
(PUB/'NATIVE_READBACK_SCOPE_REPAIR.json').write_text(json.dumps(attempt,indent=2)+'\n')
print(json.dumps(attempt,indent=2))
