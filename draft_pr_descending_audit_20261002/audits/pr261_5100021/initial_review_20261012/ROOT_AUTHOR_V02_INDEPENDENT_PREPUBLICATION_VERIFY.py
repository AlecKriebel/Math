"""Root independent, local-only reconstruction; imports no publisher/reviewer code."""
from pathlib import Path
import datetime as dt
import hashlib
import json

N=Path(__file__).resolve().parent
D=N/'pr261_publication_preparation/author_v02'
P=json.loads((D/'PLAN.json').read_bytes())
I=json.loads((D/'INPUT.json').read_bytes())
def oid(kind,b):
    return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def tree_raw(es):
    assert len({e['path'] for e in es})==len(es)
    return b''.join(e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha'])
      for e in sorted(es,key=lambda e:e['path'].encode()+(b'/' if e['type']=='tree' else b'')))
captures=D/'prepare_captures'
for name,v in P['preparation_captures'].items():assert pin(captures/name)==v
for p in captures.glob('*.exit.json'):
    x=json.loads(p.read_bytes());assert x['exit_code']==0 and x['timed_out'] is False
    assert p.with_name(p.name.replace('.exit.json','.stderr')).read_bytes()==b''
for p in captures.glob('*.STARTED.json'):assert json.loads(p.read_bytes())['method']=='GET'
objects={}
for p in captures.glob('TREE_*.stdout.json'):
    x=json.loads(p.read_bytes());assert not x['truncated']
    es=[{k:e[k] for k in ['mode','type','path','sha']} for e in x['tree']]
    assert oid('tree',tree_raw(es))==x['sha'];objects[x['sha']]=es
base=json.loads((captures/'BASE_COMMIT.stdout.json').read_bytes())
assert base['sha']==P['before']==I['expected_old']=='7b7fcd63d5ea83df3a4c29853c4ba34b93d16f07'
assert base['tree']['sha']==P['before_root']
ref=json.loads((captures/'REF.stdout.json').read_bytes())
assert ref['ref']==P['ref']=='refs/heads/dot/math-5100021' and ref['object']['sha']==P['before']
pr=json.loads((captures/'PR.stdout.json').read_bytes())
assert pr['number']==261 and pr['state']=='open' and pr['draft'] is True and pr['merged'] is False
assert pr['head']['sha']==P['before'] and pr['head']['ref']=='dot/math-5100021'
for f in P['files']:
    if f['action']=='delete':continue
    b=(D/f['body_file']).read_bytes();assert pin(D/f['body_file'])==f['frozen_pin'] and oid('blob',b)==f['blob']
    if f.get('queue_generated'):continue
    assert Path(f['body_path']).read_bytes()==b
files={f['path']:f for f in P['files']}
trees={t['path']:t for t in P['trees']}
assert len(trees)==len(P['trees'])==7 and len(files)==53
unchanged=0;untouched_subtrees=0
for path,t in trees.items():
    old=t['before_entries'];new=t['after_entries']
    if t['before'] is not None:assert objects[t['before']]==old
    else:assert old==[]
    if t['after'] is None:
        assert path.endswith('/independent_review') and new==[] and t['omitted_empty'] is True
        assert oid('tree',b'')==t['empty_tree_oid'];continue
    assert oid('tree',tree_raw(new))==t['after'];objects[t['after']]=new
    expected={e['path']:dict(e) for e in old};changed=set()
    prefix=path+'/' if path else ''
    for full,f in files.items():
        if full.rpartition('/')[0]!=path:continue
        name=full.rpartition('/')[2];changed.add(name)
        prior=expected.get(name);assert (prior['sha'] if prior else None)==f['before_blob']
        if f['action']=='delete':del expected[name]
        else:expected[name]={'path':name,'mode':f['mode'],'type':'blob','sha':f['blob']}
    for child,c in trees.items():
        if child=='' or child.rpartition('/')[0]!=path:continue
        name=child.rpartition('/')[2];changed.add(name)
        prior=expected.get(name);assert (prior['sha'] if prior else None)==c['before']
        if c['after'] is None:expected.pop(name,None)
        else:expected[name]={'path':name,'mode':'040000','type':'tree','sha':c['after']}
    assert sorted(expected.values(),key=lambda e:e['path'])==new
    for e in old:
        if e['path'] not in changed:
            assert e in new;unchanged+=1;untouched_subtrees+=e['type']=='tree'
payload=P['commit_payload'];lines=['tree '+payload['tree'],'parent '+payload['parents'][0]]
for role in ['author','committer']:
    a=payload[role];epoch=int(dt.datetime.fromisoformat(a['date'].replace('Z','+00:00')).timestamp())
    lines.append(f"{role} {a['name']} <{a['email']}> {epoch} +0000")
raw=('\n'.join(lines)+'\n\n'+payload['message']).encode()
assert raw==(D/'COMMIT.raw').read_bytes() and not raw.endswith(b'\n') and oid('commit',raw)==P['after']
before=(D/'QUEUE_BEFORE.body').read_bytes();after=(D/'bodies/queue.body').read_bytes();q=I['queue']
assert oid('blob',before)==q['before_blob'] and before.count(q['before_line'].encode())==1
assert before.replace(q['before_line'].encode(),q['after_line'].encode(),1)==after
oldcols=q['before_line'].split('|');newcols=q['after_line'].split('|')
assert [i for i in range(len(oldcols)) if oldcols[i]!=newcols[i]]==[8,11]
assert oldcols[9].strip()==newcols[9].strip()=='1/5'
result={'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'decision':'PASS_ROOT_INDEPENDENT_AUTHOR_V02_RECONSTRUCTION',
 'plan':pin(D/'PLAN.json'),'input':pin(D/'INPUT.json'),'source':pin(N/'pr261_publication_preparation/publish_pr261.py'),
 'before':P['before'],'after':P['after'],'tree':P['after_root'],'selected_paths':53,'trees':7,'omitted_empty_tree':1,
 'unselected_entries_preserved':unchanged,'untouched_subtree_entries_preserved':untouched_subtrees,
 'all_GET_captures':True,'whole_QUEUE_one_row_only':True,'no_source_imports':True,'provider_writes':0,'primary_Git_writes':0,
 'publication_authority':False}
(N/'ROOT_AUTHOR_V02_INDEPENDENT_PREPUBLICATION_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2))
