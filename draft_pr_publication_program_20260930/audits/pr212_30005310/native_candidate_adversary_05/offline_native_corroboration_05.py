#!/usr/bin/env python3
"""Offline corroboration of the separately authorized actual PR212 concurrent extension verify main/eight-worker journals.
No imports of production modules, executor, network, Git, lock or ref actions.
"""
from pathlib import Path
import base64, collections, datetime, hashlib, json, stat
Q=Path(__file__).resolve().parent
B=Q.parent/'native_administrative_preparation_01'
J=B/'ROOT_ADMIN212_FAST_READ_INDEPENDENT_VERIFY_05'
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pairs(rows):
    out={}
    for k,v in rows:
        assert k not in out,('duplicate JSON key',k)
        out[k]=v
    return out
def parse(raw):
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(AssertionError(v)))
def checked(r):
    p=Path(r['path'])
    assert p.parent in JOURNALS and p.is_file() and not p.is_symlink(),r
    actual=pin(p)
    assert type(r['bytes'])is int and actual['bytes']==r['bytes'] and actual['sha256']==r['sha256'],r
    return p.read_bytes()
def native(kind,body):
    return hashlib.sha1(kind.encode()+b' '+str(len(body)).encode()+b'\0'+body).hexdigest()
def output(name,obj):
    p=Q/name
    assert not p.exists(),p
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    p.chmod(0o444)
    return pin(p)
proof=parse((J/'VERIFIED.json').read_bytes())
transport=proof['transport_extension']
assert transport['worker_count']==8 and transport['operation']=='verify'and transport['joined_before_original_proof']is True
assert transport['extension_pin']=={'bytes':24985,'sha256':'ef746eb08622c919dffe08b037fc2ce18dfcc6629d44182aacb9d8b2e156f5f0'}
expected_digest=hashlib.sha256((J.name+'verify').encode()).hexdigest()[:20]
workers=[B/('ROOT_ADMIN212_FAST_WORK_'+expected_digest+'_'+str(i))for i in range(8)]
assert transport['worker_journals']==[str(p)for p in workers]
JOURNALS=[J]+workers
assert len(set(JOURNALS))==9 and all(p.is_dir()and not p.is_symlink()and p.resolve()==p for p in JOURNALS)
assert proof==parse((Q/'ACTUAL_VERIFY_05.stdout.json').read_bytes())
assert pin(J/'VERIFIED.json')['sha256']=='6cdc3aa7027da1e2a8817bba01ea2d2c5810bf1d092b7dfa3979c83480331a12'
assert proof['candidate']=='abe1a84f2f767a8b2524e4f29ded4515f9770fdd'
assert proof['tree']=='50f2790c04c6ae847e6886bfc2cca61ee3c32818'
assert proof['parent']=='6e756e88d5e33a4124c26ed18dc2c95085d426c0'
assert proof['parents']==[proof['parent']] and proof['parent_tree']=='41e3ade0420b9f8c785d2c4bfc72c97c1a5c4f6f'
assert proof['selected_count']==len(proof['selected_files'])==271
assert len(proof['changed_leaves'])==271 and len(proof['new_directories'])==25 and proof['deleted_directories']==[]
assert proof['mutable_Main_observed_or_spoofed']is False and proof['actual_CAS_or_completion_inferred']is False and proof['this_action_native_POSTs']==0
for key in ['full_scope_verified','all_selected_native_bodies_verified','foreign_native_tuples_preserved',
            'deterministic_canonical_commit_oid_verified','fixed_author_and_committer_metadata_verified']:
    assert proof[key]is True,key
receipts={}
blobs={}
trees={}
routes=collections.Counter()
pr_observations=[]
candidate_metadata=[]
for p in sorted(p for d in JOURNALS for p in d.glob('*.API_RECEIPT.json')):
    r=parse(p.read_bytes())
    assert r['method']=='GET' and type(r['exit'])is int and r['exit']==0 and r['request_pin']is None,r
    stdout=checked(r['raw_stdout']);stderr=checked(r['raw_stderr'])
    assert not stderr
    assert r['stdout_pin']=={k:r['raw_stdout'][k]for k in ['bytes','sha256']}
    assert r['stderr_pin']=={k:r['raw_stderr'][k]for k in ['bytes','sha256']}
    x=parse(stdout);route=r['path'];receipts[str(p)]=(r,x);routes['/'.join(route.split('/')[:2])]+=1
    assert 'ref/heads/main'not in route and not route.startswith('git/refs/')
    if route.startswith('git/blobs/'):
        oid=route.removeprefix('git/blobs/')
        assert x['sha']==oid and x['encoding']=='base64' and type(x['size'])is int
        body=base64.b64decode(''.join(x['content'].split()),validate=True)
        assert len(body)==x['size'] and native('blob',body)==oid
        if oid in blobs:assert blobs[oid]==body
        blobs[oid]=body
    elif route.startswith('git/trees/'):
        oid=route.removeprefix('git/trees/')
        assert x['sha']==oid and x['truncated']is False
        rows=x['tree'];assert len({r['path']for r in rows})==len(rows)
        raw=b''
        for r in sorted(rows,key=lambda r:r['path'].encode()+(b'/'if r['type']=='tree'else b'')):
            name=r['path'].encode();assert name and b'/'not in name and b'\0'not in name
            mode=r['mode'].lstrip('0')
            assert (mode,r['type'])in {('40000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')}
            raw+=mode.encode()+b' '+name+b'\0'+bytes.fromhex(r['sha'])
        assert native('tree',raw)==oid
        trees[oid]=rows
    elif route.startswith('git/commits/'):
        assert x['sha']==route.removeprefix('git/commits/')
        if x['sha']==proof['candidate']:candidate_metadata.append(x)
    elif route=='pulls/212':
        assert x['number']==212 and x['state']=='open' and x['draft']is True and x['merged']is False
        assert x['head']['sha']=='99af7a27a711271bcd0b9e7ce90e374e4100ea6d'
        pr_observations.append({'state':x['state'],'draft':x['draft'],'merged':x['merged'],'HEAD':x['head']['sha']})
    else:
        assert route=='compare/ad3af31e26c29115d222142ae6b033115e195808...'+proof['parent']
        assert x['status']=='ahead' and x['merge_base_commit']['sha']=='ad3af31e26c29115d222142ae6b033115e195808'
assert len(receipts)==303 and len(pr_observations)==2
origins={}
def origin_body(o,oid,wanted):
    assert o['hostname']=='github.com' and o['repository']=='AlecKriebel/Math' and o['method']=='GET'
    assert o['route']=='git/blobs/'+oid and o['receipt']in receipts
    rr={'path':o['receipt'],**o['receipt_pin']};checked(rr)
    r,x=receipts[o['receipt']]
    assert r['path']==o['route'] and r['raw_stdout']==o['raw_response'] and r['raw_stderr']==o['raw_stderr']
    checked(o['raw_response']);checked(o['raw_stderr'])
    body=blobs[oid]
    assert len(body)==wanted['bytes'] and hashlib.sha256(body).hexdigest()==wanted['sha256']
    if oid in origins:assert origins[oid]==o
    origins[oid]=o
    return body
selected_bytes=0
for path,r in proof['selected_files'].items():
    assert r['mode']=='100644' and r['type']=='blob'
    selected_bytes+=len(origin_body(r['actual_native_GET_origin'],r['git_blob'],r))
assert selected_bytes==2310514 and len(origins)==253
queue=proof['Main_QUEUE_observation']
assert queue['foreign_rows_may_differ']is False
assert queue['candidate_QUEUE_oid']==queue['parent_QUEUE_oid']==queue['observed_QUEUE_oid']=='d2ed87c338c2904e234e484e5775c93cfca1318c'
body=origin_body(queue['actual_native_body_origin'],queue['observed_QUEUE_oid'],queue['whole_body_pin'])
row=[r+b'\n'for r in body.splitlines()if r.startswith(b'|') and len(r.split(b'|'))>2 and r.split(b'|')[2].strip().split()[:1]==[b'30005310']]
assert len(row)==1 and len(row[0])==166
assert hashlib.sha256(row[0]).hexdigest()=='b192db8bf68c86e83dd5be05cd38bfd0f65ccad7b29c63a9c54f00bd66258ff3'
assert b'| queued | 0/5 |'in row[0]
admission=parse((B/'ROOT_ADMIN212_READ_ADMISSION_05/ADMISSION.json').read_bytes())
def identity(r):
    t=datetime.datetime.fromisoformat(r['date'].replace('Z','+00:00'))
    assert t.utcoffset()==datetime.timedelta(0)
    return (r['name']+' <'+r['email']+'> '+str(int(t.timestamp()))+' +0000').encode()
commit=(b'tree '+proof['tree'].encode()+b'\nparent '+proof['parent'].encode()+b'\nauthor '+
        identity(admission['commit_author'])+b'\ncommitter '+identity(admission['commit_committer'])+
        b'\n\n'+admission['commit_message'].encode())
assert native('commit',commit)==proof['candidate']
assert len(candidate_metadata)==1
meta=candidate_metadata[0]
assert meta['tree']['sha']==proof['tree'] and [p['sha']for p in meta['parents']]==[proof['parent']]
assert meta['message']==admission['commit_message'][:-1] and admission['commit_message'].endswith('\n')
for field in ['author','committer']:
    assert {k:meta[field][k]for k in ['name','email','date']}==admission['commit_'+field]
inventory=[]
for p in sorted(p for d in JOURNALS for p in d.iterdir()):
    st=p.lstat();assert stat.S_ISREG(st.st_mode) and stat.S_IMODE(st.st_mode)==0o444
    inventory.append(pin(p))
assert len(inventory)==303*3+sum(len(list(d.glob('*.IMMUTABLE_GET_CACHE_HIT.json')))for d in JOURNALS)+3
cache_hits=sum(len(list(d.glob('*.IMMUTABLE_GET_CACHE_HIT.json')))for d in JOURNALS)
assert parse((J/'EXTENSION_ACTION_RESULT.json').read_bytes())==proof
assert parse((J/'FAST_GET_EXTENSION_BINDING.json').read_bytes())==transport
exit_record=parse((Q/'ACTUAL_PROCESS_EXIT_05.json').read_bytes())
assert exit_record['actual_process_exit_code']==0 and exit_record['stderr']['bytes']==0
journal_manifest=output('READ_JOURNALS_FINITE_MANIFEST_05.json',{'schema':'pr212-independent-actual-read-journal-finite-manifest-v1',
    'files':inventory,'file_count':len(inventory),'total_bytes':sum(r['bytes']for r in inventory),
    'all_files_regular0444':True,'journals':[str(p)for p in JOURNALS],'manifest_is_readonly_observation_not_Root_acceptance':True})
report={'schema':'pr212-independent-actual-GETonly-candidate-corroboration-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'PASS','verified':pin(J/'VERIFIED.json'),'actual_process_exit':pin(Q/'ACTUAL_PROCESS_EXIT_05.json'),
    'journal_manifest':journal_manifest,'candidate':proof['candidate'],'tree':proof['tree'],'parent':proof['parent'],
    'parent_tree':proof['parent_tree'],'selected_paths':271,'unique_selected_native_bodies':253,'selected_bytes':selected_bytes,
    'changed_leaves':271,'new_directories':25,'deleted_directories':0,'actual_API_receipts':303,'actual_method_counts':{'GET':303},
    'actual_route_family_counts':dict(routes),'all_raw_response_and_stderr_and_receipt_pins_independently_rehashed':True,
    'every_native_blob_GET_independently_base64_size_nativeSHA1_checked':True,'distinct_blob_GETs':len(blobs),
    'every_native_tree_GET_independently_canonical_nativeSHA1_checked':True,'distinct_tree_GETs':len(trees),
    'all_selected_origin_chains_in_this_new_journal_checked':True,'canonical_commit_independently_recomputed':True,
    'open_draft_unmerged_current_PR_observations':pr_observations,'candidate_and_parent_whole_QUEUE_preserved':True,
    'immutable_same_instance_cache_hit_record_count':cache_hits,'worker_count':8,'complete_journal_count':9,'prefetched_unique_bodies':transport['unique_native_bodies'],'prefetched_decoded_bytes':transport['decoded_bytes'],'original_driver_CLI_claimed':False,'mutable_Main_GET_count':0,'this_action_POST_count':0,
    'source_audit_frozen_closure_not_modified':True,'extension_source_pin':transport['extension_pin'],'extension_source_manifest_pin':transport['extension_source_manifest_pin'],'actual_extension_acceptance':transport['extension_acceptance'],'Root_acceptance_or_admission_CAS_sync_terminal_PR_publication_numeric_authority':False,
    'no_other_effects_evidence_basis':'Exact approved verify branch, mutate=False API source, all303 retained process API receipts GET with no request bodies, complete journal inventory and actual exit0/empty stderr. No other action was invoked; this is bounded execution evidence, not a global OS activity proof.',
    'limits':'Production approved code performs full path/tree/foreign-scope proof. This offline corroboration independently rehashes all raw origins/native blobs/native trees, selected associations, queued own row, canonical candidate and PR metadata. It does not infer mutable Main status, live CAS, actual original-lock custody, synchronization, completion or future lease.'}
print(json.dumps({'corroboration':output('INDEPENDENT_NATIVE_CORROBORATION_05.json',report),'journal_manifest':journal_manifest},indent=2))

