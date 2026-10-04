#!/usr/bin/env python3
"""Read-only public/local evidence verifier; never writes or calls the network.

Default: exact public namespace, closure and recorded semantic evidence. Private
evidence must be collectively present or absent; absence is explicitly reported.
No arithmetic PASS is promoted into a proof or certification of inaccessible history.
"""
import argparse,base64,datetime,gzip,hashlib,json,os,pathlib,subprocess,sys
ap=argparse.ArgumentParser()
ap.add_argument('--preseal',action='store_true')
ap.add_argument('--require-private',action='store_true')
ap.add_argument('--replay',action='store_true',help='reexecute stable read-only programs; local private mode always replays those programs')
args=ap.parse_args()
ROOT=pathlib.Path(__file__).resolve().parent;A=ROOT.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def load(p):return json.loads((ROOT/p).read_bytes())
def checked(p):
    q=pathlib.PurePosixPath(p)
    assert not q.is_absolute() and '..' not in q.parts and q.as_posix()==p,p
    return ROOT/p
def verify(p,rec):
    b=checked(p).read_bytes();assert len(b)==rec['stored_bytes'] and sha(b)==rec['stored_sha256'],p
    logical=gzip.decompress(b) if rec['encoding']=='gzip' else b
    assert len(logical)==rec['logical_bytes'] and sha(logical)==rec['logical_sha256'],p
    return logical

m=load('PUBLIC_MANIFEST.json')
assert m['self_exclusions']==['PUBLIC_MANIFEST.json','FINAL_SEAL.json']
assert m['private_absence_policy']=='collectively all present or all absent; no partial private inventory'
pub=m['public_files'];private=m['private_files']
assert not set(pub)&set(private)
for p in list(pub)+list(private):checked(p)
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
private_present={p for p in private if checked(p).is_file()}
assert not (actual-set(pub)-set(private)-set(m['self_exclusions'])),('unlisted path',actual-set(pub)-set(private)-set(m['self_exclusions']))
assert set(pub)<=actual,('missing public file',set(pub)-actual)
assert private_present==set(private) or not private_present,('partial private evidence',set(private)-private_present)
if args.require_private:assert private_present==set(private),'private evidence required'
for p,r in pub.items():verify(p,r)
if private_present:
    for p,r in private.items():verify(p,r)

for seal in ['01_SOURCE_MECHANISM_SEAL.json','02_ANALYTIC_SEAL.json']:
    e=load(seal)
    fs=e.get('files',[dict(path=e.get('path'),sha256=e.get('sha256'))])
    for f in fs:
        p=f['path'];record=(pub|private)[p]
        assert record['logical_sha256']==f['sha256'],p
        if checked(p).exists():assert sha(checked(p).read_bytes())==f['sha256'],p
assert load('02_ANALYTIC_SEAL.json')['candidate_programs_executed'] is False
assert load('02_ANALYTIC_SEAL.json')['other_family_analyses_read'] is False
utc=lambda s:datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
assert utc(load('01_SOURCE_MECHANISM_SEAL.json')['sealed_utc'])<utc(load('02_ANALYTIC_SEAL.json')['sealed_utc'])

commands=load('COMMANDS.json')
assert len({r['name'] for r in commands})==len(commands)
streams={}
for r in commands:
    values={}
    for name,spec in r['streams'].items():
        p=spec['path'];assert (pub|private)[p]==spec['identity'],(r['name'],name)
        if p in pub or private_present:values[name]=verify(p,spec['identity'])
    streams[r['name']]=values
    assert r['exit_code'] in [0,1],r['name']
    if r['name'] not in ['cross_family_stream_audit','prepared_gate']:assert r['exit_code']==0,r['name']
    if values and r['name'] not in ['cross_family_stream_audit','prepared_gate']:assert values['stderr']==b'',r['name']
by_name={r['name']:r for r in commands}
assert utc(by_name['all_target_read']['finished_utc'])<utc(load('02_ANALYTIC_SEAL.json')['sealed_utc'])<utc(by_name['author_replay']['started_utc'])
if 'cross_family_stream_audit' in streams and streams['cross_family_stream_audit']:
    assert b"KeyError: 'name'" in streams['cross_family_stream_audit']['stderr']
assert by_name['cross_family_stream_audit_v2']['exit_code']==0
assert by_name['prepared_gate']['exit_code']==1
assert b"assert not obj['truncated']" in streams['prepared_gate']['stderr']
assert by_name['prepared_gate_v2']['exit_code']==0

original=load('03_reproduction_bindings.json')
assert original['frozen_head']=='4245f1af53840a07f43c05c928c4783bc6c3a467'
assert original['frozen_base']=='efd29c05204703acca9a0860812f54b94fae54b1'
assert original['source_checkpoint']=='a3ac55761d2301fbfe30e07a266da4a039cbfaba'
assert original['source_checkpoint_files']==10 and original['api_files_count']==19
bindings=original['original_bindings'];assert len(bindings)==19 and len({b['path'] for b in bindings})==19
prefix='unsolved_math_prioritization/attempts/2303002/'
assert sum(b['path'].startswith(prefix) for b in bindings)==18
assert {b['path'] for b in bindings if not b['path'].startswith(prefix)}=={'unsolved_math_prioritization/QUEUE.md'}
target=A/'snapshot'/prefix
for b in bindings:
    d=(A/'snapshot'/b['path']).read_bytes()
    assert b['mode']=='100644' and b['kind']=='blob' and len(d)==b['bytes'] and sha(d)==b['sha256'] and blob(d)==b['git_blob']
    checked_blob=streams['original_blob_'+str(bindings.index(b)).zfill(2)]['stdout']
    assert d==checked_blob
mf_counts={}
for f in original['nested_manifest_bindings']:
    d=(target/f['path']).read_bytes();assert len(d)==f['bytes'] and sha(d)==f['sha256']
    mf_counts[f['manifest']]=mf_counts.get(f['manifest'],0)+1
assert mf_counts=={'FINAL_FROZEN_MANIFEST.json':9,'final_review/REVIEW_MANIFEST.json':3,'PUBLICATION_MANIFEST.json':17}
publication=json.loads((target/'PUBLICATION_MANIFEST.json').read_bytes())
assert {f['path'] for f in publication['files']}|{'PUBLICATION_MANIFEST.json'}=={b['path'].removeprefix(prefix) for b in bindings if b['path'].startswith(prefix)}
assert publication['author_manifest_sha256']==sha((target/'FINAL_FROZEN_MANIFEST.json').read_bytes())
assert publication['review_manifest_sha256']==sha((target/'final_review/REVIEW_MANIFEST.json').read_bytes())
parents=lambda name:[x.split()[1] for x in streams[name]['stdout'].decode().splitlines() if x.startswith('parent ')]
assert parents('original_head')==[original['frozen_base'],original['source_checkpoint']]
assert parents('source_checkpoint')==[original['frozen_base']]
assert len(streams['checkpoint_tree']['stdout'].splitlines())==10
for i,line in enumerate(streams['checkpoint_tree']['stdout'].decode().splitlines()):
    left,p=line.split('\t');assert left.split()[0]=='100644'
    assert streams['checkpoint_blob_'+str(i).zfill(2)]['stdout']==(A/'snapshot'/p).read_bytes()
assert streams['author_replay']['stdout']==(target/'SOURCE_CHECKS.json').read_bytes()
review=(target/'final_review/INDEPENDENT_CHECKS.json').read_bytes()
assert streams['historical_review_replay']['stdout']==review
o=json.loads(review);o['independent_assertions']=1665
assert streams['math_only_review_replay']['stdout']==(json.dumps(o,indent=2)+'\n').encode()
assert json.loads(streams['independent_controls']['stdout'])['theorem_certified_by_finite_controls'] is False
assert json.loads(streams['geometry_symbolic_again']['stdout'])['identities']
assert json.loads(streams['poisson_controls_again']['stdout'])['exact_assertions']==735
if private_present:
    api=json.loads(streams['original_pr_api']['stdout']);assert api['head']['sha']==original['frozen_head'] and api['base']['sha']==original['frozen_base']
    files=json.loads(streams['original_pr_files_api']['stdout']);assert len(files)==19
    assert {r['filename']:r['sha'] for r in files}=={r['path']:r['git_blob'] for r in bindings}
    for i,b in enumerate(bindings):
        api=json.loads(streams['api_content_'+str(i).zfill(2)]['stdout'])
        d=base64.b64decode(api['content']);assert d==(A/'snapshot'/b['path']).read_bytes() and api['sha']==b['git_blob']

# Immutable family namespaces: exact inventories, explicit evidence absence.
# The original verifiers have differing public limitations; this wrapper does
# not edit them or claim private capture revalidation when they are absent.
family_modes={}
for f in m['family_closures']:
    directory=A/f['directory'];mf=directory/f['manifest']
    assert sha(mf.read_bytes())==f['manifest_sha256']
    assert sha((directory/'FINAL_SEAL.json').read_bytes())==f['seal_sha256']
    fm=json.loads(mf.read_bytes());fs=fm['files']
    fp={r['path']:r for r in fs} if isinstance(fs,list) else fs
    if f['directory']=='path_geometry_review':pr={r['path']:r for r in fm['private_inventory']}
    else:pr=json.loads((directory/f['private_inventory']).read_bytes())['files']
    real={p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file()}
    exclusions={f['manifest'],'FINAL_SEAL.json'}
    assert real-set(pr)-exclusions==set(fp),(f['directory'],'public namespace differs')
    present={p for p in pr if (directory/p).is_file()}
    assert present==set(pr) or not present,(f['directory'],'partial private inventory')
    if args.require_private:assert present==set(pr),(f['directory'],'private evidence required')
    for p,r in fp.items():
        d=(directory/p).read_bytes();assert len(d)==r['bytes'] and sha(d)==r['sha256']
    if present:
        for p,r in pr.items():
            d=(directory/p).read_bytes();assert len(d)==r['bytes'] and sha(d)==r['sha256']
            if 'logical_bytes' in r:
                decoded=gzip.decompress(d);assert len(decoded)==r['logical_bytes'] and sha(decoded)==r['logical_sha256']
        if f['directory']=='path_geometry_review':
            for source in json.loads((directory/'source_receipts.json').read_bytes())['sources']:
                for r in source['files']:
                    d=gzip.decompress((directory/r['path']).read_bytes());assert len(d)==r['bytes'] and sha(d)==r['sha256']
        family_modes[f['directory']]='complete private evidence verified'
    else:family_modes[f['directory']]='public integrity only; private streams absent and not reproduced'

replayed=[]
if private_present or args.replay:
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1')
    replay_specs=[('author_replay',[sys.executable,str(target/'verify_source_alignment.py')]),
                  ('math_only_review_replay',[sys.executable,str(target/'final_review/run_portable.py'),'--math-only'])]
    if private_present:
        replay_specs.append(('historical_review_replay',[sys.executable,str(target/'final_review/run_portable.py'),'--sources',str(ROOT/'private/portable_sources')]))
    for name,argv in replay_specs:
        result=subprocess.run(argv,env=env,capture_output=True)
        assert result.returncode==0 and result.stdout==streams[name]['stdout'] and result.stderr==streams[name]['stderr'],name
        replayed.append(name)
    for f in m['family_closures']:
        directory=A/f['directory']
        if family_modes[f['directory']].startswith('complete'):
            argv=[sys.executable,str(directory/f['verifier'])]+f.get('verifier_args',[])
            result=subprocess.run(argv,env=env,capture_output=True)
            assert result.returncode==0 and result.stderr==b'',f['directory']
            replayed.append(f['directory']+'/'+f['verifier'])

assert m['live_gate_required'] is True
live=load('05_prepared_gate.json')
assert live['complete'] is True and live['scope_files']==19 and live['unchanged_mathematical_files']==18
assert live['queue_changed_pipe_cells']==[8] and live['queue_turns_preserved']=='0/5'
assert live['branch_at_both_ends']=='main' and live['repository_head_at_both_ends']==live['prepared_base']
assert live['whole_api_git_body_main_merge_gate'] is True and live['all29_nested_bindings'] is True
assert live['private_git_index_unchanged'] is True
pins=m['prepared_pins']
assert pins=={k:live[k] for k in ['prepared_head','prepared_base','prepared_tree','testmerge','accepted_body_sha256']}
assert pins['prepared_head']=='47dbe2c144a77f590faf144b950f1e759db92e75'
assert pins['prepared_base']=='728b48109a11e83769b24ec5b30978c1c5ed7ec9'
assert pins['prepared_tree']=='c95a909fed27e9af7954f82ce216d34f305d91a2'
assert sha((ROOT/'accepted_body.md').read_bytes())==pins['accepted_body_sha256']
gs=lambda name:streams['prepared_v2_'+name]['stdout']
def captured_tree(name):
    rows={}
    for line in gs(name).split(b'\0'):
        if line:
            left,p=line.split(b'\t',1);rows[p.decode()]=left.decode().split()
    return rows
bt,ht=captured_tree('base_tree'),captured_tree('head_tree')
delta={p for p in set(bt)|set(ht) if bt.get(p)!=ht.get(p)}
assert delta=={b['path'] for b in bindings} and len(delta)==19
assert {p for p in ht if p.startswith(prefix)}==delta-{'unsolved_math_prioritization/QUEUE.md'}
assert gs('head_tree_oid').decode().strip()==pins['prepared_tree']
assert gs('head_parents').decode().split()==[original['frozen_head'],pins['prepared_base']]
assert gs('begin_branch')==gs('end_branch')==b'main\n'
assert gs('begin_main')==gs('end_main')==(pins['prepared_base']+'\n').encode()
assert gs('begin_index_path')==gs('end_index_path')
prepared_bindings=live['bindings'];assert len(prepared_bindings)==19
assert [b['path'] for b in prepared_bindings]==sorted(delta)
for i,b in enumerate(prepared_bindings):
    d=gs('blob_'+str(i).zfill(2));p=b['path']
    assert len(d)==b['bytes'] and sha(d)==b['sha256'] and blob(d)==b['git_blob']
    assert ht[p]==['100644','blob',b['git_blob']]
    if p.startswith(prefix):assert d==(A/'snapshot'/p).read_bytes() and p not in bt
    else:queue_head=d
queue_base=gs('base_queue');old=queue_base.splitlines(keepends=True);new=queue_head.splitlines(keepends=True)
assert len(old)==len(new)==1966
assert [i for i,(x,y) in enumerate(zip(old,new)) if x!=y]==[404]
bc,ac=old[404].split(b'|'),new[404].split(b'|')
assert b'2303002 / AMR-022-3002' in bc[2]
assert [i for i,(x,y) in enumerate(zip(bc,ac)) if x!=y]==[8]
assert bc[8].strip()==b'queued' and ac[8].strip()==b'already_solved'
assert bc[9].strip()==ac[9].strip()==b'0/5'
expected=old.copy();cells=bc.copy();cells[8]=b' already_solved ';expected[404]=b'|'.join(cells)
assert b''.join(expected)==queue_head
assert sha(queue_base)==live['queue_base_sha256'] and sha(queue_head)==live['queue_head_sha256']
for f in original['nested_manifest_bindings']:
    i=next(i for i,b in enumerate(prepared_bindings) if b['path']==prefix+f['path'])
    assert sha(gs('blob_'+str(i).zfill(2)))==f['sha256']
if private_present:
    ps=lambda name:json.loads(gs(name))
    for end in ['begin','end']:
        pr=ps(end+'_pr')
        assert pr['head']['sha']==pins['prepared_head'] and pr['base']['sha']==pins['prepared_base']
        assert pr['draft'] is True and pr['state']=='open' and pr['changed_files']==19
        assert pr['body'].encode()==(ROOT/'accepted_body.md').read_bytes()
        assert ps(end+'_main_ref')['object']['sha']==pins['prepared_base']
        hc,bc=ps(end+'_head_commit'),ps(end+'_base_commit')
        assert hc['sha']==pins['prepared_head'] and bc['sha']==pins['prepared_base']
        assert hc['tree']['sha']==pins['prepared_tree']
        assert [r['sha'] for r in hc['parents']]==[original['frozen_head'],pins['prepared_base']]
        merge=ps(end+'_testmerge')
        assert merge['sha']==pins['testmerge'] and merge['commit']['tree']['sha']==pins['prepared_tree']
        assert [r['sha'] for r in merge['parents']]==[pins['prepared_base'],pins['prepared_head']]
    for name,local in [('base_api_tree','base_root_tree'),('head_api_tree','head_root_tree'),('testmerge_api_tree','head_root_tree')]:
        obj=ps(name);assert obj['truncated'] is False
        assert {r['path']:[r['mode'],r['type'],r['sha']] for r in obj['tree']}==captured_tree(local)
    assert ps('head_api_tree')['sha']==ps('testmerge_api_tree')['sha']==pins['prepared_tree']
    assert ps('base_api_tree')['sha']==ps('begin_base_commit')['tree']['sha']
    files=ps('files');assert len(files)==19
    assert {f['filename']:f['sha'] for f in files}=={b['path']:b['git_blob'] for b in prepared_bindings}
    for i,b in enumerate(prepared_bindings):
        d=gs('blob_'+str(i).zfill(2))
        for kind in ['head','testmerge']:
            api=ps(kind+'_content_'+str(i).zfill(2))
            assert api['path']==b['path'] and api['type']=='file' and api['size']==len(d) and api['sha']==blob(d)
            assert base64.b64decode(api['content'])==d
    assert base64.b64decode(ps('base_queue_api')['content'])==queue_base
if not args.preseal:
    final=load('FINAL_SEAL.json')
    assert final['public_manifest_sha256']==sha((ROOT/'PUBLIC_MANIFEST.json').read_bytes())
    assert final['analytic_seal_sha256']==sha((ROOT/'02_ANALYTIC_SEAL.json').read_bytes())
    assert final['prepared_gate_sha256']==sha((ROOT/'05_prepared_gate.json').read_bytes())
    assert final['root_reviewed_verifier'] is True and final['live_gate_complete'] is True
    assert utc(final['sealed_utc'])>utc(live['completed_utc'])
print(json.dumps(dict(public_integrity='verified',private_evidence='complete and verified' if private_present else 'absent; private source/API captures not independently revalidated',
    original_scope=19,nested_bindings=29,author_receipt=3675,source_review_receipt=1667,math_only_receipt=1665,
    mathematical_verdict='credited entire harmonic/continuous case; analytic proof required',novel_theorems=0,
    family_evidence=family_modes,readonly_replayed=replayed,
    closure='preseal' if args.preseal else 'sealed',writes=0),indent=2))
