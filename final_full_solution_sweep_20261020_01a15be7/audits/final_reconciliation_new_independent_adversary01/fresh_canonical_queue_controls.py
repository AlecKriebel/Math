"""Fresh INERT in-memory adversarial controls for dated canonical QUEUE replay.
Never constructs root authority, fake actual receipts or service effects.
"""
from pathlib import Path
import hashlib,sys,base64,json,copy
W=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/final_reconciliation_new_independent_adversary01')
p=W/'check_dated_canonical_queue.py';b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=='03dc2f119a33a34a83ec2c7918f6b2e853677116c3fd3975c407c46066278339'
n={'__file__':str(p),'__name__':'_inert_canonical_controls'}
exec(compile(b,str(p),'exec'),n)
pin={'path':str(W.parent/'root_final_canonical_queue_live_reconciliation01/ROOT_CANONICAL_QUEUE_WITHDRAWAL_RECONCILIATION.json'),'bytes':33501,'sha256':'b1ec1d5aaa8c0acd5160b69aa88c6bbf7b39530e3ddc8f3e296bd15a2f6c4aba'}
r=n['objpin'](pin);es=[n['objpin'](p)for p in r['original_native_transports']]
body=n['objpin'](r['queue_body_and_blob_pin']);hist=n['objpin'](n['MAP'])
a=[r,es,body,hist];out=[]
def run(name,change):
 vals=copy.deepcopy(a);change(vals)
 try:n['check_data'](*vals)
 except Exception as e:out.append({'INERT_control':name,'expected':'REFUSE','actual':'REFUSE','reason':str(e)});return
 raise RuntimeError('Adverse control accepted: '+name)
def replace(v,i,fn):
 raw=base64.b64decode(v[1][i]['stdout_base64'])
 sep=b'\r\n\r\n'if b'\r\n\r\n'in raw else b'\n\n'
 head,b=raw.split(sep,1);o=n['strict'](b);fn(o)
 v[1][i]['stdout_base64']=base64.b64encode(head+sep+json.dumps(o).encode()).decode()
assert n['check_data'](*a)['final_clearance']is False
out.append({'INERT_control':'unmodified actual objects positive seam','expected':'PASS_DATED_ONLY','actual':'PASS_DATED_ONLY'})
run('native return bool is not zero int',lambda v:v[1][0].__setitem__('returncode',False))
run('extra projection argv refused',lambda v:v[1][0]['argv'].extend(['--jq','.object']))
run('non-GET native argv refused',lambda v:v[1][0]['argv'].__setitem__(3,'POST'))
run('missing sixth original refused',lambda v:v[1].pop())
run('backward native chronology',lambda v:v[1][1].__setitem__('before',v[1][0]['before']))
run('moved final main ref',lambda v:replace(v,5,lambda o:o['object'].__setitem__('sha','0'*40)))
run('truncated complete top tree',lambda v:replace(v,2,lambda o:o.__setitem__('truncated',True)))
run('full top tree unselected entry tampering',lambda v:replace(v,2,lambda o:o['tree'][0].__setitem__('sha','1'*40)))
run('full queue tree unselected entry tampering',lambda v:replace(v,3,lambda o:o['tree'][0].__setitem__('sha','1'*40)))
run('queue Git blob content tampering',lambda v:replace(v,4,lambda o:o.__setitem__('content',base64.b64encode(b'not the complete queue').decode())))
run('derived decoded carrier tampering',lambda v:v[2].__setitem__('decoded_bytes_base64',base64.b64encode(b'wrong carrier').decode()))
run('complete queue row count mismatch',lambda v:v[0].__setitem__('complete_queue_rows',1950))
run('withdrawal receipt title altered',lambda v:v[0]['checks'][0]['fresh_full_row'].__setitem__('problem_title','wrong title'))
run('withdrawal receipt alias altered',lambda v:v[0]['checks'][0]['fresh_full_row'].__setitem__('problem_alias','30002867 / WRONG'))
run('withdrawal receipt status restored to claimed',lambda v:v[0]['checks'][0]['fresh_full_row'].__setitem__('status','claimed_solved'))
run('receipt falsely says no unresolved',lambda v:v[0].__setitem__('unresolved',['unreconciled queue row']))
print(json.dumps({'status':'PASS_FRESH_INERT_CANONICAL_QUEUE_CONTROLS','control_count':len(out),'controls':out,'actual_services':0,'final_clearance':False},indent=2))
