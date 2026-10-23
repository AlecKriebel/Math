"""Fresh INERT full native inventory ingress counterexamples; no fake actual receipts."""
from pathlib import Path
import hashlib,copy,base64,json
W=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/final_reconciliation_new_independent_adversary01')
p=W/'strict_inventory_native_ingress.py';b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=='f68e9b43367bc35302ccf8d1f069890fa3195bdbfa1ec49279b7fb0a14497aba'
n={'__name__':'_inert_inventory_ingress','__file__':str(p)};exec(compile(b,str(p),'exec'),n)
pin={'path':str(W.parent/'ROOT_HIGHEST_PR_READ_20261023_0019.json.gz'),'bytes':10567,'sha256':'2e13d4a41cbcf234df998cc0aa6dda3239d581b1ab369c2059c61a337dbc2996'}
e=n['objpin'](pin);a,_,_=n['native'](e,n['NEW']);x=a[0]
out=[{'INERT_control':'dated original positive','result':'PASS_DATED_ONLY','highest':n['node'](x)}]
def test(name,original,change,fn):
 v=copy.deepcopy(original);change(v)
 try:fn(v)
 except Exception as exc:out.append({'INERT_control':name,'result':'EXPECTED_REFUSAL','reason':str(exc)});return
 raise RuntimeError('Accepted adverse control '+name)
nat=lambda e:n['native'](e,n['NEW'])
test('outer labeled method diverges',e,lambda v:v.__setitem__('method','POST'),nat)
test('boolean HTTP status',e,lambda v:v.__setitem__('status',True),nat)
test('actual argv route diverges from label',e,lambda v:v['original_cli']['argv'].__setitem__(-1,n['NEW']+'&page=2'),nat)
test('original projection flag',e,lambda v:v['original_cli']['argv'].extend(['--jq','.[].number']),nat)
test('original CLI absent',e,lambda v:v.pop('original_cli'),nat)
test('native CLI boolean return',e,lambda v:v['original_cli'].__setitem__('returncode',False),nat)
test('raw body relabeled',e,lambda v:v.__setitem__('raw_body_base64',base64.b64encode(b'[]').decode()),nat)
test('original headers relabeled',e,lambda v:v.__setitem__('raw_headers_base64',base64.b64encode(b'HTTP/2.0 200 OK\n\n').decode()),nat)
test('body hash relabeled',e,lambda v:v.__setitem__('raw_body_sha256','0'*64),nat)
test('naive native time',e,lambda v:v.__setitem__('at','2026-10-23T00:21:11'),nat)
test('native time reversed',e,lambda v:v.__setitem__('completed_at','2026-10-23T00:00:00+00:00'),nat)
test('number boolean',x,lambda v:v.__setitem__('number',True),n['node'])
test('missing complete branch field',x,lambda v:v.pop('base'),n['node'])
test('wrong base repository',x,lambda v:v['base']['repo'].__setitem__('full_name','Different/Math'),n['node'])
test('draft numeric zero',x,lambda v:v.__setitem__('draft',0),n['node'])
test('body boolean',x,lambda v:v.__setitem__('body',False),n['node'])
test('wrong PR URL',x,lambda v:v.__setitem__('url',n['API']+'/pulls/1'),n['node'])
test('nonhex head identity',x,lambda v:v['head'].__setitem__('sha','Z'*40),n['node'])
test('naive creation timestamp',x,lambda v:v.__setitem__('created_at','2026-10-20T00:00:00'),n['node'])
print(json.dumps({'status':'PASS_FRESH_INERT_STRICT_INVENTORY_INGRESS_CONTROLS','count':len(out),'controls':out,'actual_final_inputs_tested':False,'services':0,'final_clearance':False},indent=2))
