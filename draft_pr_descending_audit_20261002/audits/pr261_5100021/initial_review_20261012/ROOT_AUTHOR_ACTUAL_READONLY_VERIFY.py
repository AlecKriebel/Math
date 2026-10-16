"""Verify one consumed AUTHOR execution and later GET-only postreads, locally."""
from pathlib import Path
import base64, datetime as dt, hashlib, json
N=Path(__file__).resolve().parent
D=N/'pr261_publication_preparation/author_v02'
A=D/'actual'
V=N/'author_post_CAS_readonly_verification_20261012'
P=json.loads((D/'PLAN.json').read_bytes())
def read(d,n):return json.loads((d/n).read_bytes())
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def oid(k,b):return hashlib.sha1(k.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def entries(x):return [{k:e[k] for k in ('path','mode','type','sha')} for e in x['tree']]
def tree(es):
    return b''.join(e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in sorted(es,key=lambda e:e['path'].encode()+(b'/' if e['type']=='tree' else b'')))
def raw(c):
    lines=['tree '+c['tree']['sha']]+['parent '+p['sha'] for p in c['parents']]
    for role in ['author','committer']:
        x=c[role];epoch=int(dt.datetime.fromisoformat(x['date'].replace('Z','+00:00')).timestamp())
        lines.append(f"{role} {x['name']} <{x['email']}> {epoch} +0000")
    return ('\n'.join(lines)+'\n\n'+c['message']).encode()
for d in [A,V]:
    for p in d.glob('*.exit.json'):
        x=read(d,p.name);assert x['exit_code']==0 and x['timed_out'] is False
        assert p.with_name(p.name.replace('.exit.json','.stderr')).read_bytes()==b''
assert not (A/'COMPLETE.json').exists()
assert b'PR branch mismatch' in (N/'ROOT_AUTHOR_V02_PUBLISH.stderr').read_bytes()
starts=[read(A,p.name) for p in A.glob('*.STARTED.json')]
assert sum(x['endpoint']=='graphql' for x in starts)==1
assert sum(x['method']=='POST' for x in starts)==46
assert not any(x['method']=='PATCH' for x in starts)
for p in V.glob('*.STARTED.json'):assert read(V,p.name)['method']=='GET'
for label in ['REF_before','REF_before_CAS']:
    assert read(A,label+'.stdout.json')['object']['sha']==P['before']
for label in ['REF_after_CAS']:
    assert read(A,label+'.stdout.json')['object']['sha']==P['after']
assert read(V,'REF.stdout.json')['object']['sha']==P['after']
cas=read(A,'REF_CAS.payload.json')['variables']['input']
assert cas['refUpdates']==[{'name':P['ref'],'beforeOid':P['before'],'afterOid':P['after'],'force':False}]
assert read(A,'REF_CAS.stdout.json')=={'data':{'updateRefs':{'clientMutationId':cas['clientMutationId']}}}
for label in ['PR_before','PR_before_CAS','PR_after_CAS']:
    q=read(A,label+'.stdout.json')
    assert q['head']['sha']==P['before']
    for k in ['number','title','body','state','draft','merged','closed_at','merged_at']:assert q[k]==P['PR_guard'][k]
q=read(V,'PR.stdout.json')
assert q['head']['sha']==P['after'] and q['head']['ref']=='dot/math-5100021' and q['base']['ref']=='main'
for k in ['number','title','body','state','draft','merged','closed_at','merged_at']:assert q[k]==P['PR_guard'][k]
for side in ['head','base']:assert q[side]['repo']['full_name']=='AlecKriebel/Math' and q[side]['repo']['node_id']=='R_kgDOTfIvPw'
for i,f in enumerate(P['files']):
    if f['action']=='delete':continue
    label=f'BLOB_{i:03d}';body=(D/f['body_file']).read_bytes()
    assert base64.b64decode(read(A,label+'.payload.json')['content'])==body
    assert read(A,label+'.stdout.json')['sha']==f['blob']==oid('blob',body)
    rb=read(A,f'BLOB_READ_{i:03d}.stdout.json');assert rb['sha']==f['blob'] and base64.b64decode(rb['content'])==body
ts=sorted((t for t in P['trees'] if t['after'] is not None),key=lambda t:len(t['path'].split('/')) if t['path'] else 0,reverse=True)
for i,t in enumerate(ts):
    label=f'TREE_{i:03d}';assert read(A,label+'.payload.json')['tree']==t['after_entries']
    assert read(A,label+'.stdout.json')['sha']==t['after']==oid('tree',tree(t['after_entries']))
    rb=read(A,f'TREE_READ_{i:03d}.stdout.json');assert rb['sha']==t['after'] and not rb['truncated']
    assert sorted(entries(rb),key=lambda e:e['path'])==t['after_entries']
root=read(V,'ROOT.stdout.json');assert root['sha']==P['after_root']==oid('tree',tree(entries(root)))
assert sorted(entries(root),key=lambda e:e['path'])==next(t['after_entries'] for t in ts if t['path']=='')
assert read(A,'COMMIT_CREATE.payload.json')==P['commit_payload']
assert read(A,'COMMIT_CREATE.stdout.json')['sha']==P['after']
for d,label in [(A,'COMMIT_READ'),(V,'COMMIT')]:
    c=read(d,label+'.stdout.json');b=raw(c)
    assert c['sha']==P['after']==oid('commit',b) and b==(D/'COMMIT.raw').read_bytes()==(A/'PROVIDER_COMMIT.raw').read_bytes()
    assert not b.endswith(b'\n') and c['tree']['sha']==P['after_root'] and [p['sha'] for p in c['parents']]==[P['before']]
result={'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'decision':'ROOT_INDEPENDENT_ACTUAL_AUTHOR_GRAPH_AND_GET_POSTREADS_PASS','before':P['before'],'after':P['after'],'tree':P['after_root'],'selected_paths':53,'created_blobs':38,'created_nonempty_trees':6,'single_expected_old_nonforce_CAS':True,'publisher_exit_code':1,'publisher_failure':'Immediate PR postread returned the old head after successful CAS; no replay. Later separate GET-only complete ref/PR/root/commit observations agree with exact corrected head.','original_actual_captures':{p.name:pin(p) for p in sorted(A.iterdir())},'later_GET_captures':{p.name:pin(p) for p in sorted(V.iterdir())},'primary_Git_writes':0,'metadata_writes':0,'native_merge_close_ready_writes':0,'paper_DOI_tracker_writes':0,'mathematics_percent':100,'bounded_priority_percent':100,'workflow_percent':70,'publication_authority':False}
(N/'ROOT_AUTHOR_ACTUAL_READONLY_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print('Root independently verified exact actual AUTHOR graph, all captures and later complete GET-only postreads.')
