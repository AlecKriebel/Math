"""Read-only standalone verifier of the closed original + prepared public audit.

Raw primary PDFs and API captures are private. When archived API captures are
available, their complete bytes and semantics are also checked. A public-only
copy still verifies every public Git capture, proof/control output, literal pin,
receipt, chronology seal and inventory; live retrieval is reproduced separately
with a private copy of audit_prepared_head.py, never by mutating this closure.
"""
from pathlib import Path,PurePosixPath
import base64,datetime,gzip,hashlib,json
R=Path(__file__).resolve().parent
EXCLUDED={'IMMUTABLE_MANIFEST.json','FINAL_SEAL.json'}
HEAD='7821af7ddd84a4b3bb3168a11246f4b49ab0c5e8';BASE='04c40062219cc9fa20834d98db2b270fdad1a848';ORIGINAL='f4039c9c093b10e651ee7fd2e6379073b84238c7'
BODY='90a8ee71e425f5b1c8f0873102ae6d3d6cb904fb5509d4a2b75b0fc4056a1626'
QUEUE='unsolved_math_prioritization/QUEUE.md';PREFIX='unsolved_math_prioritization/attempts/2303016/'
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(p):return sha(p.read_bytes())
def path(name):
    q=PurePosixPath(name);assert not q.is_absolute() and '..' not in q.parts and q.as_posix()==name
    p=R/name;assert not p.is_symlink();return p

def public_files():
    return {str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and not any(part in {'private_sources','private_replay','__pycache__'} for part in p.relative_to(R).parts) and str(p.relative_to(R)) not in EXCLUDED}
def bind(e):
    p=path(e['path']);assert p.is_file() and p.stat().st_size==e['bytes'] and digest(p)==e['sha256'],e['path']
    return p.read_bytes()
def dt(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
manifest_raw=(R/'IMMUTABLE_MANIFEST.json').read_bytes();m=json.loads(manifest_raw)
assert m['excluded']==sorted(EXCLUDED)
assert len({e['path'] for e in m['files']})==len(m['files'])
assert {e['path'] for e in m['files']}==public_files()
for e in m['files']:bind(e)
for n in ['INDEPENDENT_BASELINE_SEAL.json','ORIGINAL_ASSESSMENT_SEAL.json']:
    z=json.loads((R/n).read_text())
    for name,e in z['files'].items():
        p=path(name);assert p.stat().st_size==e.get('bytes',e.get('size')) and digest(p)==e['sha256'],(n,name)
source=json.loads((R/'PRIMARY_SOURCE_RECEIPTS.json').read_text());baseline=json.loads((R/'INDEPENDENT_BASELINE_SEAL.json').read_text());assessment=json.loads((R/'ORIGINAL_ASSESSMENT_SEAL.json').read_text())
assert dt(source['utc'])<dt(baseline['utc'])<dt(assessment['utc'])
assert assessment['original_head']==ORIGINAL
expected_sources={'hayman_lingham_2018':(1706228,'8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0'),'hedberg_wolff_1983':(1782353,'f351a967ae723f590d85da9a886ca4f6d8a1a21f7de8315f83180d9dcf3b5006')}
assert len(source['receipts'])==2
for e in source['receipts']:
    assert (e['size'],e['sha256'])==expected_sources[e['name']]
    assert e['extraction_exit']==0 and e['extraction_stdout']==e['extraction_stderr']==''
# Every original command capture is complete and hash-bound.
z=json.loads((R/'FROZEN_PACKET_RECEIPT.json').read_text())
assert z['original_head']==ORIGINAL and z['base']=='efd29c05204703acca9a0860812f54b94fae54b1'
assert z['author_checkpoint']=='2a14016d7e62d1b044bb63cad51a25e5747e7cd1'
assert z['nested_binding_count']==48 and len(z['nested_bindings'])==48
assert z['author_checkpoint_files']==14 and z['author_checkpoint_byte_preservation']
assert z['queue_only_status_and_turn_cells'] and z['queue_changed_line']==406
assert len(z['commands'])==43
for command in z['commands']:
    assert command['exit']==0
    for stream in ['stdout','stderr']:
        p=R/'streams'/(command['label']+'.'+stream)
        assert p.stat().st_size==command[stream+'_bytes'] and digest(p)==command[stream+'_sha256']
original_bytes={}
assert len(z['snapshot_file_bindings'])==22
for i,e in enumerate(z['snapshot_file_bindings']):
    b=(R/'streams'/('original_blob_'+str(i)+'.stdout')).read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
    assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==e['git_blob_sha']
    original_bytes[e['path']]=b
assert len(original_bytes)==22 and QUEUE in original_bytes
assert all(p==QUEUE or p.startswith(PREFIX) for p in original_bytes)
for e in z['nested_bindings']:
    directory=PREFIX+('final_review/' if e['manifest'].startswith('final_review/') else '')
    b=original_bytes[directory+e['path']]
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
assert (R/'streams/author_checks.stdout').read_bytes()==original_bytes[PREFIX+'TURN_1_CHECKS.json']
assert (R/'streams/historical_review.stdout').read_bytes()==original_bytes[PREFIX+'final_review/CHECKS.json']
assert json.loads(original_bytes[PREFIX+'TURN_1_CHECKS.json'])['assertions']==2690
assert json.loads(original_bytes[PREFIX+'final_review/CHECKS.json'])['independent_assertions']==1909
for prefix in ['frozen_packet','adversarial_controls','assessment_seal','prepared_head','root_evidence_inspection']:
    assert (R/(prefix+'.stderr')).read_bytes()==b''
a=json.loads((R/'ADVERSARIAL_CONTROLS.json').read_text())
assert a['assertions']==2590 and a['status']=='PASS' and all(e['rejected'] for e in a['negative_controls'])
assert (R/'adversarial_controls.stdout').read_bytes()==(R/'ADVERSARIAL_CONTROLS.json').read_bytes()
# Prepared semantics are derived again from complete saved Git streams.
p=json.loads((R/'PREPARED_HEAD_RECEIPT.json').read_text())
assert p['prepared_head']==HEAD and p['literal_base_local_remote_main']==BASE and p['original_head']==ORIGINAL
assert p['status']=='PASS' and dt(assessment['utc'])<dt(p['utc'])
assert p['body_sha256']==BODY and digest(R/'LIVE_ACCEPTED_PR_BODY.md')==BODY
assert p['refresh_parents']==[ORIGINAL,BASE]
assert p['original_target_files_preserved']==21 and p['live_scoped_remote_files']==22
assert p['remote_state']=='OPEN ready mergeable clean'
assert len(p['commands'])==64 and len({e['label'] for e in p['commands']})==64
private_paths=[path(e[name+'_path']) for e in p['commands'] if e['private'] for name in ['stdout','stderr']]
private_present=sum(q.is_file() for q in private_paths)
assert private_present in {0,len(private_paths)},'partially missing private captures'
def capture(e,stream):
    q=path(e[stream+'_path'])
    if e['private'] and private_present==0:return None
    stored=q.read_bytes();assert sha(stored)==e[stream+'_stored_sha256']
    logical=gzip.decompress(stored) if e['compressed'] else stored
    assert len(logical)==e[stream+'_bytes'] and sha(logical)==e[stream+'_sha256']
    return logical
captures={}
for e in p['commands']:
    assert e['exit']==0
    assert ('private_replay/' if e['private'] else 'prepared_streams/') in e['stdout_path']
    captures[e['label']]=capture(e,'stdout')
    error=capture(e,'stderr');assert error in {None,b''}
assert captures['local_branch'].decode().strip()=='main'
for name in ['local_main','local_main_end']:assert captures[name].decode().strip()==BASE
for name in ['remote_main','remote_main_end']:assert captures[name].decode().split()==[BASE,'refs/heads/main']
assert captures['local_head_parents'].decode().split()==[ORIGINAL,BASE]
def tree(b):
    result={}
    for entry in b.split(b'\0'):
        if not entry:continue
        meta,name=entry.split(b'\t',1);mode,kind,oid=meta.decode().split()
        result[name.decode()]={'mode':mode,'type':kind,'blob':oid}
    return result
bt=tree(captures['entire_base_tree']);ht=tree(captures['entire_head_tree']);ot=tree(captures['entire_original_tree'])
expected=set(original_bytes)
changed={name for name in bt.keys()|ht.keys() if bt.get(name)!=ht.get(name)}
assert changed==expected and len(changed)==22
assert {e['path'] for e in p['full_root_changed_entries']}==expected
for e in p['full_root_changed_entries']:assert e['before']==bt.get(e['path']) and e['after']==ht[e['path']]
prepared_bytes={}
assert len(p['remote_whole_file_receipts'])==22
for i,e in enumerate(p['remote_whole_file_receipts']):
    name=e['path'];b=captures['prepared_blob_'+str(i)];prepared_bytes[name]=b
    assert len(b)==e['bytes'] and sha(b)==e['sha256'] and e['remote_whole_bytes_equal']
    assert hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()==e['blob']
    assert ht[name]=={'mode':'100644','type':'blob','blob':e['blob']}
    if name!=QUEUE:assert ot[name]==ht[name] and b==original_bytes[name]
    if private_present:
        content=json.loads(captures['remote_content_'+str(i)])
        assert content['path']==name and content['size']==len(b) and content['sha']==e['blob'] and content['type']=='file'
        assert content['encoding']=='base64' and base64.b64decode(content['content'])==b
assert set(prepared_bytes)==expected
assert len(p['target_preservation'])==21 and {e['path'] for e in p['target_preservation']}==expected-{QUEUE}
assert all(e['mode_type_blob_unchanged'] and e['bytes_sha256_unchanged'] for e in p['target_preservation'])
baseq=captures['literal_base_queue'];headq=prepared_bytes[QUEUE]
old=baseq.decode().splitlines(keepends=True);new=headq.decode().splitlines(keepends=True)
assert len(old)==len(new)==p['queue']['lines']==1966
changes=[(i+1,a,b) for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert len(changes)==1
line,before,after=changes[0];assert line==p['queue']['line']==406 and '2303016 / AMR-022-3016' in before
assert [i for i,(a,b) in enumerate(zip(before.split('|'),after.split('|'))) if a!=b]==[8,9]==p['queue']['changed_cells']
assert after==before.replace('| queued | 0/5 |','| already_solved | 1/5 |')
assert baseq.replace(before.encode(),after.encode(),1)==headq and baseq.count(before.encode())==1
assert p['queue']['base_bytes']==len(baseq) and p['queue']['head_bytes']==len(headq) and p['queue']['whole_non_target_bytes_preserved']
assert len(p['nested_bindings'])==48
for e in p['nested_bindings']:
    directory=PREFIX+('final_review/' if e['manifest'].startswith('final_review/') else '')
    b=prepared_bytes[directory+e['path']];assert len(b)==e['bytes'] and sha(b)==e['sha256']
merge=p['test_merge'];assert merge['parents']==[BASE,HEAD] and merge['equal_to_prepared_head_tree']
assert merge['sha']=='f86ef1149ccc845c6297285718f50f6f93601fee'
assert captures['actual_test_merge_ref'].decode().split()==[merge['sha'],'refs/pull/366/merge']
assert captures['local_head_tree_oid'].decode().strip()==merge['tree']
family_expected={'priority_method_review':('REVIEW_MANIFEST.json','c37d071fcafdb11d26332a185676a381b2af8746e9855669075c98ec1e0d646d',8),'variational_capacity_review':('IMMUTABLE_MANIFEST.json','aa86e6f71ddeb7ea73ac13729035cbe0bb846a5aac7d12a9b6200e4ed97d2358',26)}
assert len(p['family_manifests'])==2
for e in p['family_manifests']:
    assert (e['manifest'],e['sha256'],e['public_files'])==family_expected[e['family']] and e['all_public_hashes_equal']
if private_present:
    assert json.loads(captures['api_main_ref'])['object']['sha']==BASE
    assert json.loads(captures['api_pr_branch_ref'])['object']['sha']==HEAD
    hc=json.loads(captures['api_head_commit']);mc=json.loads(captures['actual_test_merge_commit'])
    assert [e['sha'] for e in hc['parents']]==[ORIGINAL,BASE] and hc['tree']['sha']==merge['tree']
    assert [e['sha'] for e in mc['parents']]==[BASE,HEAD] and mc['tree']['sha']==merge['tree']
    for name in ['live_pr_start','live_pr_end']:
        live=json.loads(captures[name]);assert live['state']=='open' and not live['draft']
        assert live['head']['sha']==HEAD and live['base']['sha']==BASE and live['base']['ref']=='main'
        assert live['mergeable'] is True and live['mergeable_state']=='clean' and live['merge_commit_sha']==merge['sha']
        assert live['body'].encode()==(R/'LIVE_ACCEPTED_PR_BODY.md').read_bytes()
    remote_files=json.loads(captures['remote_pr_files']);assert len(remote_files)==22 and {e['filename'] for e in remote_files}==expected
    for e in remote_files:assert e['sha']==ht[e['filename']]['blob'] and e['status']==('modified' if e['filename']==QUEUE else 'added')
if (R/'FINAL_SEAL.json').exists():
    final=json.loads((R/'FINAL_SEAL.json').read_text())
    assert final['status']=='PASS' and final['manifest_sha256']==sha(manifest_raw)
    assert final['verifier_code_sha256']==digest(Path(__file__)) and final['verifier_exit']==0
    assert final['verifier_stdout_sha256']==digest(R/'closure.stdout') and final['verifier_stderr_sha256']==digest(R/'closure.stderr')
    assert final['public_files']==len(m['files']) and final['explicit_manifest_self_and_final_seal_exclusion']
print('PASS: closed public inventory; source/math chronology; original 22 files and 48 bindings; 2590 controls; exact prepared head/base/body/test merge; whole queue and 22 remote receipts.')
