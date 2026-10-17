"""Actual metadata fixture and synthetic verifier controls; no transport/effects."""
import base64
import hashlib
import json
from pathlib import Path
import types

BASE = Path(__file__).absolute().parent
FIXTURE_PIN = {'bytes':3386,'sha256':'3e934f79fab95ee4555c4e03100a72e5916a8e57d150ec21de1a7b485d4f4ff8'}


def module(name):
    result = types.ModuleType(name)
    result.__file__ = str(BASE/(name+'.py'))
    exec(compile(Path(result.__file__).read_bytes(),result.__file__,'exec'),result.__dict__)
    return result


def run():
    h,c = module('native209_model'),module('native_trees_readonly')
    checks = []
    def yes(condition,label):
        if not condition:
            raise RuntimeError(label)
        checks.append(label)
    def refused(call,label):
        try:
            call()
        except (RuntimeError,ValueError,TypeError,KeyError):
            checks.append(label)
        else:
            raise RuntimeError('Expected refusal: '+label)
    fixture_raw = (BASE/'COMMIT_MESSAGE_READBACK_ACTUAL_FIXTURE.json').read_bytes()
    yes(h.pin(fixture_raw) == FIXTURE_PIN,'actual_diagnostic_fixture_pin')
    fixture = h.decode(fixture_raw)
    request,api = fixture['canonical_commit_request'],fixture['api_response']
    actual_m = {'commit_message':request['message'],'commit_author':request['author'],
                'commit_committer':request['committer']}
    body,oid = h.commit_request(actual_m,request['tree'],request['parents'])
    yes(oid == api['sha'] == fixture['deterministic_canonical_oid'],
        'actual45d_canonical_message_and_fixed_identities_reconstruct_oid')
    yes(api['message'] != request['message'] and api['message'] == request['message'][:-1],
        'actual45d_old_exact_message_guard_failure_reproduced')
    normalization = h.commit_message_readback(request['message'],api['message'])
    yes(normalization['representation'] == 'omits_exactly_one_terminal_LF'
        and normalization['terminal_LFs_omitted'] == 1,'actual45d_oneLF_metadata_representation_accepted')
    yes(h.commit_message_readback(request['message'],request['message'])['terminal_LFs_omitted'] == 0,
        'exact_metadata_representation_accepted')
    for observed,label in ((api['message']+' ','trailing_space'),(api['message']+'\r\n','CRLF'),
                           (request['message']+'\n','added_LF'),(api['message']+'\n\n','added_two_LFs'),
                           (api['message'][:-1],'text_character_removed'),
                           (api['message'].replace('\n\n','\n',1),'internal_blank_line_removed')):
        refused(lambda observed=observed:h.commit_message_readback(request['message'],observed),
                'message_other_change_refused_'+label)
    refused(lambda:h.commit_message_readback(request['message']+'\n',api['message']),
            'two_terminal_LFs_omitted_refused')
    refused(lambda:h.commit_message_readback(request['message'],None),'nonstring_metadata_refused')

    objects = {}
    def tree(rows):
        rows = sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''))
        oid = c.tree_hash(rows)
        objects[oid] = {'sha':oid,'truncated':False,'tree':[
            {'path':n,'mode':mode,'type':kind,'sha':sha} for n,mode,kind,sha in rows]}
        return oid
    # Known own/shared subtree edges stay opaque; one selected synthetic body
    # exercises the real verifier's complete native diff/body path. This is not
    # an actual full input manifest or Root authority envelope.
    attempts = tree([('5100015','040000','tree',h.ATTEMPT_TREE)])
    unsolved = tree([('attempts','040000','tree',attempts)])
    audits = tree([('pr209_5100015','040000','tree',h.SHARED_TREE)])
    descending = tree([('audits','040000','tree',audits)])
    before_body,after_body = b'synthetic before\n',b'synthetic after\n'
    oldblob,newblob = h.native('blob',before_body),h.native('blob',after_body)
    common = [('unsolved_math_prioritization','040000','tree',unsolved),
              ('draft_pr_descending_audit_20261002','040000','tree',descending)]
    before = tree(common+[('synthetic_selected.txt','100644','blob',oldblob)])
    after = tree(common+[('synthetic_selected.txt','100644','blob',newblob)])
    identity = {'name':'Synthetic Fixture','email':'synthetic@example.invalid','date':'2026-01-01T00:00:00Z'}
    m = {'phase':'merge95','facts':h.phase_facts('merge95'),'commit_message':'Synthetic full verify fixture\n\nData only.\n',
         'commit_author':identity,'commit_committer':identity}
    parent,parents = '9'*40,['9'*40,h.PREPARED]
    payload,expected_oid = h.commit_request(m,after,parents)
    baseline_commit = {'sha':expected_oid,'tree':{'sha':after},'parents':[{'sha':p} for p in parents],
                       'message':m['commit_message'],'author':identity,'committer':identity}
    baseline_blob = {'sha':newblob,'size':len(after_body),'encoding':'base64',
                     'content':base64.b64encode(after_body).decode()}
    selected = {'synthetic_selected.txt':after_body}
    native_commit,native_blob = baseline_commit,baseline_blob
    requested = []
    def observer(method,path,body=None):
        if method != 'GET' or body is not None:
            raise RuntimeError('Synthetic provider forbids effects')
        requested.append(path)
        if path.startswith('git/trees/'):
            value = objects[path.removeprefix('git/trees/')]
        elif path == 'git/commits/'+expected_oid:
            value = native_commit
        elif path == 'git/blobs/'+newblob:
            value = native_blob
        elif path == 'git/ref/heads/main':
            value = {'object':{'sha':parent}}
        else:
            raise RuntimeError('Unknown synthetic GET route')
        return h.decode(json.dumps(value).encode())
    real_state = h.state
    def synthetic_state(c0,m0,overlay0,pre0,reused0,observer0,after_ref=False):
        return {'api':h.GetOnly(observer0),'parent':parent,'parent_tree':before,'wanted':after,
                'changed':set(selected),'dirs':set(),'parents':parents}
    h.state = synthetic_state
    def verify(candidate=expected_oid):
        return h.verify(c,m,selected,{'synthetic_selected.txt':('100644','blob',oldblob)},
                        {},observer,candidate)
    try:
        evidence = verify()
        yes(evidence['full_scope_verified'] and evidence['all_selected_native_bodies_verified']
            and evidence['deterministic_canonical_commit_oid_verified']
            and evidence['fixed_author_and_committer_metadata_verified']
            and evidence['commit_message_readback']['representation'] == 'exact',
            'full_real_verifier_exact_readback_and_native_body_pass')
        native_commit = {**baseline_commit,'message':m['commit_message'][:-1]}
        evidence = verify()
        yes(evidence['commit_message_readback']['terminal_LFs_omitted'] == 1,
            'full_real_verifier_oneLF_normalization_evidence_pass')
        for changed,label in (({'message':m['commit_message']+'\n'},'extra_LF'),
                              ({'message':m['commit_message'][:-1]+' '},'trailing_space'),
                              ({'message':m['commit_message'][:-1]+'\r\n'},'CRLF'),
                              ({'message':'changed text'},'different_text'),
                              ({'sha':'e'*40},'response_SHA'),
                              ({'tree':{'sha':before}},'tree'),
                              ({'parents':[{'sha':p} for p in reversed(parents)]},'ordered_parents'),
                              ({'author':{**identity,'email':'changed@example.invalid'}},'author_email'),
                              ({'committer':{**identity,'date':'2026-01-01T00:00:01Z'}},'committer_date')):
            native_commit = {**baseline_commit,**changed}
            refused(verify,'full_real_verifier_refuses_'+label)
        native_commit = baseline_commit
        before_calls = len(requested)
        refused(lambda:verify('e'*40),'full_real_verifier_requires_deterministic_canonical_oid')
        yes(len(requested) == before_calls,'wrong_canonical_oid_refused_before_candidate_GET')
        native_blob = {**baseline_blob,'content':base64.b64encode(b'corrupted selected body').decode()}
        refused(verify,'full_real_verifier_selected_body_corruption_refused')
    finally:
        h.state = real_state
    return {'schema':'pr209-commit-message-readback-targeted-controls-v1','status':'PASS',
            'checks':checks,'check_count':len(checks),'actual_metadata_fixture_replayed_offline':True,
            'full_verify_uses_synthetic_state_only_no_authority_envelope':True,
            'actual_provider_calls':0,'native_objects_or_refs_or_local_views_modified':False}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
