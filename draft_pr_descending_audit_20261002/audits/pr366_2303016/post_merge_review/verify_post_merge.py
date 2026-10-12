"""Read-only verifier of all closed post-merge public evidence and saved semantics."""
from pathlib import Path,PurePosixPath
import base64,gzip,hashlib,json
R=Path(__file__).resolve().parent;A=R.parent
EXCLUDED={'PUBLIC_MANIFEST.json','FINAL_SEAL.json'}
BASE='04c40062219cc9fa20834d98db2b270fdad1a848';HEAD='7821af7ddd84a4b3bb3168a11246f4b49ab0c5e8';MERGE='a7931795d85cd86c414200c5828d175046f707d5';ORIGINAL='f4039c9c093b10e651ee7fd2e6379073b84238c7'
TREE='194ef7dbd1f1a0d050400e68a61c6d166a54ef6e';BODY='90a8ee71e425f5b1c8f0873102ae6d3d6cb904fb5509d4a2b75b0fc4056a1626';MERGED_AT='2026-10-03T18:10:21Z'
PREFIX='unsolved_math_prioritization/attempts/2303016/';QUEUE='unsolved_math_prioritization/QUEUE.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def path(name):
    q=PurePosixPath(name);assert not q.is_absolute() and '..' not in q.parts and q.as_posix()==name
    p=R/name;assert not p.is_symlink();return p

def public_inventory():return {p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file() and not set(p.relative_to(R).parts)&{'private','__pycache__'} and p.relative_to(R).as_posix() not in EXCLUDED}
raw_manifest=(R/'PUBLIC_MANIFEST.json').read_bytes();manifest=json.loads(raw_manifest)
assert manifest['excluded']==sorted(EXCLUDED)
assert len(manifest['files'])==len({e['path'] for e in manifest['files']})
assert {e['path'] for e in manifest['files']}==public_inventory()
for e in manifest['files']:
    p=path(e['path']);b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
r=json.loads((R/'ACTUAL_POST_MERGE_RECEIPT.json').read_text())
assert r['actual_merge']==MERGE and r['actual_parents']==[BASE,HEAD] and r['actual_tree']==TREE
assert r['prepared_head']==HEAD and r['literal_base']==BASE and r['original_head']==ORIGINAL
assert r['merged_at']==MERGED_AT and r['body_sha256']==BODY and r['remote_state']=='CLOSED and merged'
assert r['local_remote_main_at_both_ends']==MERGE and r['assertions']==635
assert len(r['commands'])==88 and len({e['label'] for e in r['commands']})==88
private_paths=[path(e[s+'_path']) for e in r['commands'] if e['private'] for s in ['stdout','stderr']]
private_count=sum(p.is_file() for p in private_paths);assert private_count in {0,len(private_paths)}
def capture(e,s):
    p=path(e[s+'_path'])
    if e['private'] and private_count==0:return None
    stored=p.read_bytes();assert sha(stored)==e[s+'_stored_sha256']
    logical=gzip.decompress(stored) if e['compressed'] else stored
    assert len(logical)==e[s+'_bytes'] and sha(logical)==e[s+'_sha256']
    return logical
captures={}
for e in r['commands']:
    assert e['exit']==0
    assert e['stdout_path'].startswith('private/' if e['private'] else 'streams/')
    captures[e['label']]=capture(e,'stdout');assert capture(e,'stderr') in {None,b''}
for label in ['main_start','checkout_start','local_main_end']:assert captures[label].decode().strip()==MERGE
assert captures['branch_start'].decode().strip()=='main'
for label in ['remote_main_start','remote_main_end']:assert captures[label].decode().split()==[MERGE,'refs/heads/main']
assert captures['actual_local_merge_parents'].decode().split()==[BASE,HEAD]
for label in ['actual_local_merge_tree','prepared_local_tree']:assert captures[label].decode().strip()==TREE
for label in ['main_ancestry_base','main_ancestry_prepared','main_ancestry_actual_merge']:assert captures[label]==b''
def tree(b):
    out={}
    for entry in b.split(b'\0'):
        if not entry:continue
        meta,name=entry.split(b'\t',1);mode,kind,oid=meta.decode().split();out[name.decode()]={'mode':mode,'type':kind,'blob':oid}
    return out
bt=tree(captures['whole_base_tree']);ht=tree(captures['whole_prepared_tree']);mt=tree(captures['whole_actual_merge_tree']);ot=tree(captures['whole_original_tree'])
assert ht==mt
expected={e['path'] for e in r['whole_file_receipts']};assert len(expected)==22 and QUEUE in expected
assert all(p==QUEUE or p.startswith(PREFIX) for p in expected)
changed={p for p in bt.keys()|mt.keys() if bt.get(p)!=mt.get(p)};assert changed==expected
assert {p for p in mt if p.startswith(PREFIX)}==expected-{QUEUE}
assert len(r['all_root_changed_entries'])==22 and {e['path'] for e in r['all_root_changed_entries']}==expected
for e in r['all_root_changed_entries']:assert e['before']==bt.get(e['path']) and e['after']==mt[e['path']]
contents={}
for i,e in enumerate(r['whole_file_receipts']):
    name=e['path'];b=captures['actual_blob_'+str(i)];contents[name]=b
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
    blob=hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest();assert blob==e['git_blob']
    assert mt[name]=={'mode':'100644','type':'blob','blob':blob}
    assert e['mode']=='100644' and e['type']=='blob' and e['actual_worktree_equal'] and e['whole_actual_merge_remote_equal']
    if name!=QUEUE:
        assert e['original_target_equal'] and e['whole_prepared_remote_equal'] and ot[name]==mt[name]
    if private_count:
        api=json.loads(captures['remote_merge_content_'+str(i)])
        assert api['path']==name and api['type']=='file' and api['sha']==blob and api['size']==len(b)
        assert api['encoding']=='base64' and base64.b64decode(api['content'])==b
        if name!=QUEUE:
            api=json.loads(captures['remote_head_content_'+str(i)])
            assert api['path']==name and api['type']=='file' and api['sha']==blob and api['size']==len(b)
            assert api['encoding']=='base64' and base64.b64decode(api['content'])==b
assert r['original_target_files_unchanged']==21 and r['remote_contents_fetched']==43
baseq=captures['entire_literal_base_queue'];actualq=contents[QUEUE]
old=baseq.splitlines(keepends=True);new=actualq.splitlines(keepends=True)
assert len(old)==len(new)==1966
changes=[(i+1,a,b) for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert len(changes)==1
line,before,after=changes[0];assert line==406 and b'2303016 / AMR-022-3016' in before
assert [i for i,(a,b) in enumerate(zip(before.split(b'|'),after.split(b'|'))) if a!=b]==[8,9]
assert after==before.replace(b'| queued | 0/5 |',b'| already_solved | 1/5 |')
assert baseq.count(before)==1 and baseq.replace(before,after,1)==actualq
q=r['queue'];assert q['line']==406 and q['lines']==1966 and q['changed_cells']==[8,9]
assert q['base_bytes']==len(baseq) and q['merged_bytes']==len(actualq) and q['all_other_bytes_equal']
assert q['status']=='already_solved' and q['turns']=='1/5'
# Every nested binding is independently rechecked from whole actual merge captures.
assert r['nested_binding_count']==48 and len(r['nested_bindings'])==48
for e in r['nested_bindings']:
    directory=PREFIX+('final_review/' if e['manifest'].startswith('final_review/') else '')
    b=contents[directory+e['path']];assert len(b)==e['bytes'] and sha(b)==e['sha256']
pub=json.loads(contents[PREFIX+'PUBLICATION_MANIFEST.json'])
assert pub['author_manifest_sha256']==sha(contents[PREFIX+'FINAL_FROZEN_MANIFEST.json'])
assert pub['review_manifest_sha256']==sha(contents[PREFIX+'final_review/REVIEW_MANIFEST.json'])
# The proof packet and its finite-control evidence are unchanged; no new theorem is inferred.
assert json.loads(contents[PREFIX+'TURN_1_CHECKS.json'])['assertions']==2690
assert json.loads(contents[PREFIX+'final_review/CHECKS.json'])['independent_assertions']==1909
assert r['completion']['post_merge_review_percent']==100 and r['completion']['credited_method_percent']==100 and r['completion']['new_theorem_percent']==0
expected_prior={'priority_method_review':('REVIEW_MANIFEST.json','c37d071fcafdb11d26332a185676a381b2af8746e9855669075c98ec1e0d646d',8),'variational_capacity_review':('IMMUTABLE_MANIFEST.json','aa86e6f71ddeb7ea73ac13729035cbe0bb846a5aac7d12a9b6200e4ed97d2358',26),'clean_final_adversary':('IMMUTABLE_MANIFEST.json','aa40b05b683b74d4d24e34bb9eb3c76bacc8fb6f9c37f4da183faad29e320636',194)}
assert len(r['earlier_closed_manifests'])==3
prior_ignored={'priority_method_review':{'private_replays','private_sources','replays','__pycache__'},'variational_capacity_review':{'private'},'clean_final_adversary':{'private_sources','private_replay','__pycache__'}}
for e in r['earlier_closed_manifests']:
    assert (e['manifest'],e['sha256'],e['public_files'])==expected_prior[e['family']] and e['all_closed_files_unchanged']
    p=A/e['family']/e['manifest']
    if p.exists():
        raw=p.read_bytes();assert sha(raw)==e['sha256']
        entries=json.loads(raw)['files'];assert len(entries)==e['public_files']
        actual_inventory={q.relative_to(p.parent).as_posix() for q in p.parent.rglob('*') if q.is_file() and not set(q.relative_to(p.parent).parts)&prior_ignored[e['family']] and q.name not in {e['manifest'],'FINAL_SEAL.json'}}
        assert actual_inventory=={entry['path'] for entry in entries}
        for entry in entries:
            data=(p.parent/entry['path']).read_bytes();assert len(data)==entry['bytes'] and sha(data)==entry['sha256']
prior_seal=A/'clean_final_adversary/FINAL_SEAL.json'
assert r['clean_final_194_file_seal_sha256']=='326455cb355e429c8e397776326a38d1f8b7d1f403f8e8b5d2fde6887eedc634'
if prior_seal.exists():assert sha(prior_seal.read_bytes())==r['clean_final_194_file_seal_sha256']
assert r['primary_pdf_pins']=={'hayman_lingham_2018':[1706228,'8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0'],'hedberg_wolff_1983':[1782353,'f351a967ae723f590d85da9a886ca4f6d8a1a21f7de8315f83180d9dcf3b5006']}
body=(R/'ACTUAL_MERGED_PR_BODY.md').read_bytes();assert sha(body)==BODY
if private_count:
    for label in ['raw_api_main_start','raw_api_main_end']:assert json.loads(captures[label])['object']['sha']==MERGE
    for label in ['raw_merged_pr_start','raw_merged_pr_end']:
        api=json.loads(captures[label]);assert api['state']=='closed' and api['merged'] is True and api['merged_at']==MERGED_AT
        assert api['merge_commit_sha']==MERGE and api['head']['sha']==HEAD and api['base']['sha']==BASE and api['body'].encode()==body
    api=json.loads(captures['raw_actual_merge_commit']);assert [e['sha'] for e in api['parents']]==[BASE,HEAD] and api['tree']['sha']==TREE
assert len(r['negative_controls'])==4 and all(e['rejected'] for e in r['negative_controls'])
clarification=json.loads((R/'QUEUE_NEGATIVE_CLARIFICATION.json').read_text())
assert clarification['changed_physical_line']==406 and clarification['changed_pipe_cell']==9 and clarification['rejected_wrong_target_turn']
assert (R/'queue_negative.stdout').read_bytes()==(R/'QUEUE_NEGATIVE_CLARIFICATION.json').read_bytes()
for name in ['post_merge.stderr','queue_negative.stderr']:assert (R/name).read_bytes()==b''
if (R/'FINAL_SEAL.json').exists():
    f=json.loads((R/'FINAL_SEAL.json').read_text());assert f['status']=='PASS'
    assert f['manifest_sha256']==sha(raw_manifest) and f['verifier_code_sha256']==sha(Path(__file__).read_bytes())
    assert f['verifier_exit']==0 and f['verifier_stdout_sha256']==sha((R/'closure.stdout').read_bytes()) and f['verifier_stderr_sha256']==sha((R/'closure.stderr').read_bytes())
    assert f['public_files']==len(manifest['files']) and f['explicit_self_exclusions']==sorted(EXCLUDED)
print('PASS: closed actual post-merge audit; literal merge/parents/tree/body/refs; all22 entries and21 preserved proofs; wholequeue;48 bindings; prior194-file seal; negative controls.')
