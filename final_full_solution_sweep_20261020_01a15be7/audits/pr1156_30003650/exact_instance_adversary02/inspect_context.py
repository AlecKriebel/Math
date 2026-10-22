#!/usr/bin/env python3
"""Read-only independent corpus/pin inspection; no project imports or service calls."""
from pathlib import Path
import ast,collections,datetime,hashlib,json,re
from urllib.parse import unquote
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[]
def pin(path,expected=None,length=None):
    b=path.read_bytes();digest=sha(b)
    if expected is not None and digest!=expected:raise RuntimeError('Pin mismatch '+str(path))
    if length is not None and len(b)!=length:raise RuntimeError('Length mismatch '+str(path))
    checks.append({'path':str(path.relative_to(R)) if path.is_relative_to(R) else str(path),'bytes':len(b),'sha256':digest})
    return b
pin(A/'reconcile_exact_instance_v2.py','d0fe59f4967facfd64db7332aad0f9663b4771f7a116c463c89bf4c30b88eacb',19390)
pin(A/'LEDGER_RECONCILIATION_PLAN.json','83df78463704c63ea3969a87325f18ab21c21893d6e1b8b49c5b16a6b4e3b2e1',4337)
acceptance=json.loads(pin(A/'ROOT_LEDGER_REVIEW06_ACCEPTANCE.json'))
for p,s in acceptance['dependency_pins'].items():pin(R/p,s)
for name,expected in [('ACTUAL_INSTANCE_MANIFEST.json','26628c01fc5c8cf793f420eb00c4a9f75d5dbefdebe79e9569b93993321d804a'),('FRESH_INSTANCE_MANIFEST.json','89d564562e4bfd1ec6b4c881b3fe82cb56e32b53840570a5803492882341cc9e')]:
    manifest=json.loads(pin(A/'ledger_adversary08'/name,expected))
    for e in manifest['files']:pin(A/'ledger_adversary08'/e['path'],e['sha256'],e['bytes'])
root=json.loads(pin(A/'root/ROOT_ACTUAL_INSTANCE08_ACCEPTANCE.json','515a230a271e286acd195f997982dfd9c8b9f5e1549e5963cb27cd44fde5153d'))
source=json.loads((H/'SOURCE_PINS.json').read_bytes())['files'];byname={Path(e['original']).name:e for e in source}
def private(e):
    b=pin(H/e['snapshot'],e['sha256'],e['bytes'])
    if Path(e['original']).read_bytes()!=b:raise RuntimeError('Original changed')
    return json.loads(b)
a=private(byname['source_14_account.json']);ledger=private(byname['source_10_ledger_live.json'])['response']['values'];fresh=private(byname['account.json'])
assert type(a['total']) is int and a['total']==197 and len(a['records'])==197 and len(ledger)==181
old={r['id']:r for r in a['records']};new={r['id']:r for r in fresh['records']}
if old.keys()!=new.keys() or len(old)!=197:raise RuntimeError('Inventory differs')
stats={'downloads','unique_downloads','version_downloads','version_unique_downloads','views','unique_views','version_views','version_unique_views'}
deltas=[];leafs=0;nodes=collections.Counter();shape={};texts=[]
def compare(x,y,p):
    global leafs
    nodes[type(x).__name__]+=1
    if type(x) is not type(y):raise RuntimeError('Different type at '+str(p))
    if isinstance(x,dict):
        if x.keys()!=y.keys():raise RuntimeError('Different keyset')
        for k in x:compare(x[k],y[k],p+(k,))
    elif isinstance(x,list):
        if len(x)!=len(y):raise RuntimeError('Different length')
        for i in range(len(x)):compare(x[i],y[i],p+(i,))
    else:
        leafs+=1
        if x!=y:
            if not(len(p)==3 and p[1]=='stats' and p[2] in stats and type(x) is int and min(x,y)>=0):raise RuntimeError('Forbidden changed leaf '+str(p))
            deltas.append({'path':p,'old':x,'new':y})
for i in old:compare(old[i],new[i],(i,))
if len(deltas)!=152:raise RuntimeError('Wrong fresh delta count')
def visit(v,path):
    if isinstance(v,str):texts.append((path,v))
    elif isinstance(v,list):
        for i,x in enumerate(v):visit(x,path+(i,))
    elif isinstance(v,dict):
        for k,x in v.items():texts.append((path+('KEY',),k));visit(x,path+(k,))
for n,r in enumerate(a['records']):visit(r,('account',n))
visit(ledger,('ledger',))
if len(texts)!=43495:raise RuntimeError('Wrong string inventory')
pattern=re.compile('2335036[34]|30003650|OWR.?15957.?003|CP[ _^+–-]*plus|positive[ -]?factor[ -]?rank|/pull/1156(?![0-9])',re.I)
leads=[]
for p,v in texts:
    for _ in range(8):
        nxt=unquote(v)
        if nxt==v:break
        v=nxt
    if pattern.search(v):leads.append({'path':p,'value':v})
if leads:raise RuntimeError('Unexpected target semantic lead')
result={'schema':1,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Exact parsed JSON identity data and pinned dependencies only; independent evidence sources read, original input bytes unchanged.','pins':checks,'account_records':len(old),'ledger_rows':len(ledger),'all_record_nodes_compared':dict(nodes),'compared_leaf_values':leafs,'fresh_allowed_stat_changes':deltas,'fresh_changed_leaves':len(deltas),'raw_string_keys_and_values':len(texts),'independent_semantic_leads':leads,'v2_operational_acceptance_present':(A/'ROOT_EXACT_INSTANCE_V2_ACCEPTANCE.json').exists(),'new_mutations_or_live_reads':False}
(H/'CONTEXT_AND_PIN_INSPECTION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['pins','fresh_allowed_stat_changes']},indent=2))
