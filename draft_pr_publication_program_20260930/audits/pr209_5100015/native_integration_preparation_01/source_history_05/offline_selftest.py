"""Synthetic offline controls only. No actual gate, service, view, or lock touched."""
import base64
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import types

BASE = Path(__file__).absolute().parent


def load(name):
    module = types.ModuleType(name)
    module.__file__ = str(BASE/(name+'.py'))
    exec(compile(Path(module.__file__).read_bytes(),module.__file__,'exec'),module.__dict__)
    return module


def run():
    h = load('native209_model')
    c = load('native_trees_readonly')
    checks = []
    def yes(condition,name):
        if not condition:
            raise RuntimeError(name)
        checks.append(name)
    def refused(call,name):
        try:
            call()
        except (RuntimeError,ValueError,TypeError,KeyError,OSError):
            checks.append(name)
        else:
            raise RuntimeError('Expected refusal: '+name)
    objects = {}
    def tree(rows):
        rows = sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1]=='040000' else b''))
        oid = c.tree_hash(rows)
        objects[oid] = {'sha':oid,'truncated':False,'tree':[
            {'path':name,'mode':mode,'type':kind,'sha':sha} for name,mode,kind,sha in rows]}
        return oid
    def observe(method,path,body=None):
        if method != 'GET' or body is not None or not path.startswith('git/trees/'):
            raise RuntimeError('Synthetic fixture is GET-only')
        return objects[path.removeprefix('git/trees/')]
    empty = tree([])
    oldbody,newbody = b'old synthetic\n',b'new synthetic\n'
    foreignblob = c.native('blob',b'opaque foreign bytes\n')
    ownold = tree([('selected.txt','100644','blob',c.native('blob',oldbody))])
    ownnew = tree([('selected.txt','100644','blob',c.native('blob',newbody))])
    foreign = tree([('empty','040000','tree',empty),('executable','100755','blob',foreignblob),
                    ('link','120000','blob',foreignblob),('submodule','160000','commit','b'*40)])
    before = tree([('own','040000','tree',ownold),('foreign','040000','tree',foreign)])
    after = tree([('own','040000','tree',ownnew),('foreign','040000','tree',foreign)])
    overlay = {'own/selected.txt':newbody}
    pre = {'own/selected.txt':('100644','blob',c.native('blob',oldbody))}
    wanted,changed,dirs = h.expected(c,c.NativeTrees(observe),before,overlay,pre)
    yes(wanted == after and changed == {'own/selected.txt'} and dirs == set(),'exact_preimage_native_rebuild')
    leaves,added,deleted = c.NativeTrees(observe).changes(before,after)
    yes(leaves == changed and not added and not deleted,'full_scope_exact_changed_leaf')
    reader = c.NativeTrees(observe)
    yes(reader.lookup(after,'foreign') == ('040000','tree',foreign),'opaque_foreign_tree_native_SHA_preserved')
    yes(reader.lookup(after,'foreign/empty') == ('040000','tree',empty),'foreign_empty_directory_preserved')
    yes(reader.lookup(after,'foreign/executable')[:2] == ('100755','blob'),'foreign_executable_mode_preserved')
    yes(reader.lookup(after,'foreign/link')[:2] == ('120000','blob'),'foreign_symlink_mode_preserved')
    yes(reader.lookup(after,'foreign/submodule') == ('160000','commit','b'*40),'foreign_gitlink_preserved')
    refused(lambda:h.expected(c,c.NativeTrees(observe),before,overlay,{'own/selected.txt':None}),'stale_native_preimage_refused')
    refused(lambda:h.expected(c,c.NativeTrees(observe),before,{'foreign/executable/new':newbody},
                             {'foreign/executable/new':None}),'native_leaf_ancestor_collision_refused')
    refused(lambda:h.expected(c,c.NativeTrees(observe),before,{'x':b'a','x/y':b'b'},
                             {'x':None,'x/y':None}),'overlay_leaf_ancestor_collision_refused')
    evilforeign = tree([('empty','040000','tree',empty),('executable','100644','blob',foreignblob),
                        ('link','120000','blob',foreignblob),('submodule','160000','commit','b'*40)])
    evil = tree([('own','040000','tree',ownnew),('foreign','040000','tree',evilforeign)])
    yes(c.NativeTrees(observe).changes(before,evil)[0] == {'own/selected.txt','foreign/executable'},
        'hidden_foreign_mode_change_detected')
    noemptyforeign = tree([('executable','100755','blob',foreignblob),('link','120000','blob',foreignblob),
                          ('submodule','160000','commit','b'*40)])
    noempty = tree([('own','040000','tree',ownnew),('foreign','040000','tree',noemptyforeign)])
    yes(c.NativeTrees(observe).changes(before,noempty)[2] == {'foreign/empty'},'foreign_empty_directory_deletion_detected')
    tampered = dict(objects[before]);tampered['tree'] = list(reversed(tampered['tree']))
    refused(lambda:c.NativeTrees(lambda *_:tampered).get(before,0),'noncanonical_native_tree_order_refused')
    badsha = dict(objects[before]);badsha['sha'] = '0'*40
    refused(lambda:c.NativeTrees(lambda *_:badsha).get(before,0),'wrong_native_tree_SHA_refused')
    truncated = dict(objects[before]);truncated['truncated'] = True
    refused(lambda:c.NativeTrees(lambda *_:truncated).get(before,0),'truncated_native_tree_refused')
    called = []
    safe = h.GetOnly(lambda *args: called.append(args) or {})
    refused(lambda:safe('POST','git/trees',{}),'GET_firewall_POST_refused')
    refused(lambda:safe('GET','git/refs/heads/main'),'GET_firewall_unlisted_ref_route_refused')
    refused(lambda:safe('GET','pulls/208'),'GET_firewall_other_PR_refused')
    refused(lambda:safe('GET','git/ref/heads/main',{}),'GET_firewall_request_body_refused')
    yes(not called,'forbidden_routes_never_dispatch')
    calls = []
    def unavailable(*args):
        calls.append(args)
        raise RuntimeError('synthetic uncertainty')
    stopped = h.GetOnly(unavailable)
    refused(lambda:stopped('GET','git/ref/heads/main'),'GET_uncertainty_stops')
    refused(lambda:stopped('GET','git/ref/heads/main'),'GET_uncertainty_no_automatic_retry')
    yes(len(calls) == 1,'exactly_one_GET_dispatch_after_failure')
    refused(lambda:h.decode(b'{"x":1,"x":2}'),'duplicate_JSON_key_refused')
    refused(lambda:h.decode(b'{"x":NaN}'),'nonfinite_JSON_constant_refused')
    refused(lambda:h.decode(b'{"x":1e999}'),'overflow_JSON_float_refused')
    for value in ('../escape','a/../b','/absolute','a\\b','a//b','a\nb'):
        refused(lambda value=value:h.rel(value),'unsafe_path_refused_'+repr(value))
    queued = (b'| 222 | 5100015 / AMR-050-0015 | Elliptic-billiard invariant k_{303,b} | 0.1905 | 5.0 | 3 | 2021 | queued | 0/5 |  |  |  |\n')
    revised = h.decode((BASE/'QUEUE_REFERENCE.json').read_bytes())['snapshots'][1]['own_row'].encode()
    old = b'foreign prefix\n'+queued+b'foreign suffix\n'
    new = b'foreign prefix\n'+revised+b'foreign suffix\n'
    h.queue_change(old,new,'merge95');checks.append('exact_own_QUEUE_row_transplant')
    h.queue_change(new,new,'completion100');checks.append('completion_QUEUE_byteexact_noop')
    refused(lambda:h.queue_change(old,new.replace(b'foreign suffix',b'changed foreign suffix'),'merge95'),
            'foreign_QUEUE_byte_change_refused')
    refused(lambda:h.queue_change(old,new.replace(b'claimed_solved',b'already_solved'),'merge95'),
            'historical_claimed_solved_status_change_refused')
    refused(lambda:h.queue_change(new,new.replace(b'1/5',b'2/5'),'completion100'),'historical_effort_change_refused')
    yes(h.phase_facts('merge95')['fully_completed_count'] == 50
        and h.phase_facts('merge95')['published_count'] == 35
        and h.phase_facts('completion100')['fully_completed_count'] == 51
        and h.phase_facts('completion100')['next_numeric_intake_cursor'] == 210,'phase_counter_contract')
    refused(lambda:h.phase_facts('findings45'),'unapproved_phase_refused')
    real_log_preimages = []
    for path in (BASE.parent/'RESEARCH_LOG.md',BASE.parents[2]/'RESEARCH_LOG.md'):
        original_log = path.read_bytes()
        merge95_log = original_log+b'\nSYNTHETIC OFFLINE95 FIXTURE; no actual gate or acceptance.\n'+h.phase_marker('merge95')+b'\n'
        completion_log = merge95_log+b'\nSYNTHETIC OFFLINE100 FIXTURE; no actual gate or acceptance.\n'+h.phase_marker('completion100')+b'\n'
        yes(completion_log.startswith(merge95_log) and merge95_log.startswith(original_log)
            and completion_log.count(b'<!-- PR209_NATIVE_PHASE_FACTS ') == 2,
            'old_exactly_one_policy_conflict_reproduced_'+path.parent.name)
        h.markdown_current(merge95_log,'merge95',True)
        h.markdown_current(completion_log,'completion100',True)
        checks.append('real_log_prefix_two_phase_transition_pass_'+path.parent.name)
        real_log_preimages.append({'path':str(path),'pin':h.pin(original_log)})
    current100 = b'Synthetic current document\n'+h.phase_marker('completion100')+b'\n'
    h.markdown_current(current100,'completion100',False);checks.append('replaceable_current_markdown_single100_pass')
    h.markdown_current(completion_log+b'\n','completion100',True);checks.append('terminal_marker_trailing_empty_line_pass')
    refused(lambda:h.markdown_current(current100,'completion100',True),'append_log_cannot_discard95_history')
    refused(lambda:h.markdown_current(merge95_log,'completion100',True),'stale95_current_refused')
    refused(lambda:h.markdown_current(completion_log+b'after current marker\n','completion100',True),
            'content_after_current_terminal_marker_refused')
    refused(lambda:h.markdown_current(completion_log+h.phase_marker('completion100')+b'\n','completion100',True),
            'duplicate_current100_marker_refused')
    refused(lambda:h.markdown_current(completion_log+h.phase_marker('merge95')+b'\n','completion100',True),
            'stale_latest95_after100_refused')
    refused(lambda:h.markdown_current(completion_log.replace(h.phase_marker('merge95'),
            h.phase_marker('merge95').replace(b'"published_count":35',b'"published_count":34')),'completion100',True),
            'malformed_historical_phase_facts_refused')
    refused(lambda:h.markdown_current(completion_log.replace(h.phase_marker('completion100'),
            b'embedded '+h.phase_marker('completion100')),'completion100',True),
            'midline_current_marker_refused')
    for tag,label in ((b'<!-- PR209_NATIVE_PHASE_FACTS{} -->','missing_separator'),
                      (b'<!-- PR209_NATIVE_PHASE_FACTS\t{} -->','tab_separator'),
                      (b'<!-- PR209_NATIVE_PHASE_FACTSX {} -->','extra_namespace_suffix')):
        refused(lambda tag=tag:h.markdown_current(completion_log.replace(h.phase_marker('completion100'),
                tag+b'\n'+h.phase_marker('completion100')),'completion100',True),
                'malformed_namespace_'+label+'_refused')
    refused(lambda:h.markdown_current(h.phase_marker('merge95')+b'\n'+h.phase_marker('merge95')+b'\n'+current100,
            'completion100',False),'duplicate95_history_in_replaceable_current_document_refused')
    content = b'synthetic blob bytes'
    oid = h.native('blob',content)
    blob = {'sha':oid,'encoding':'base64','size':len(content),'content':base64.b64encode(content).decode()}
    yes(h.read_blob(lambda *_:blob,oid) == content,'full_native_blob_body_positive')
    bad = {**blob,'content':base64.b64encode(b'x'*len(content)).decode()}
    refused(lambda:h.read_blob(lambda *_:bad,oid),'full_native_blob_tamper_refused')
    refused(lambda:h.load_inputs('ABSENT_ACTUAL_MANIFEST.json',{'bytes':0,'sha256':'0'*64},
                                 'ABSENT_ROOT_ACCEPTANCE.json',{'bytes':0,'sha256':'0'*64}),
            'absent_actual_manifest_and_Root_gate_fail_closed')
    yes(h.exact({'x':[9,True]}, {'x':[9,True]})
        and not h.exact({'x':[9,True]}, {'x':[9.0,True]})
        and not h.exact({'x':[9,True]}, {'x':[9,1]}),'deep_exact_JSON_types')
    identity = {'name':'Synthetic Fixture','email':'synthetic@example.invalid','date':'2026-01-01T00:00:00Z'}
    frozen = {'commit_message':'Synthetic fixture only\n','commit_author':identity,'commit_committer':identity}
    request,oid = h.commit_request(frozen,'a'*40,['b'*40])
    raw = ('tree '+'a'*40+'\nparent '+'b'*40+'\nauthor Synthetic Fixture <synthetic@example.invalid> 1767225600 +0000\n'
           'committer Synthetic Fixture <synthetic@example.invalid> 1767225600 +0000\n\nSynthetic fixture only\n').encode()
    yes(oid == hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        and request['author'] == identity,'deterministic_exact_commit_request_identity')
    refused(lambda:h.commit_request({**frozen,'commit_message':'missing newline'},'a'*40,['b'*40]),
            'noncanonical_commit_message_refused')
    e = load('native209_future_executor')
    with tempfile.TemporaryDirectory(prefix='_offline_controls_',dir=BASE) as temporary:
        fixture = Path(temporary).resolve()
        e.CHECKOUT,e.BASE,e.PROGRAM = fixture,fixture,fixture/'program'
        e.PROGRAM.mkdir()
        view = e.PROGRAM/'synthetic.json'
        view.write_bytes(b'synthetic fixture bytes\n')
        yes(e.local_pin(h,view) == h.pin(view.read_bytes()),'descriptor_local_view_positive')
        link = e.PROGRAM/'synthetic_link.json'
        link.symlink_to(view)
        refused(lambda:e.local_pin(h,link),'descriptor_local_view_symlink_refused')
        lock = e.PROGRAM/'ROOT_GLOBAL_FIVE_WRITER.lock'
        lock.write_bytes(e.LOCK_BYTES);lock.chmod(0o444);s=lock.stat()
        expected = {'path':'synthetic/program/ROOT_GLOBAL_FIVE_WRITER.lock','device':s.st_dev,
                    'inode':s.st_ino,**h.pin(e.LOCK_BYTES)}
        with e.WriterLock(expected):
            checks.append('pinned_fixture_lock_positive')
        replacement = e.PROGRAM/'replacement.lock'
        replacement.write_bytes(e.LOCK_BYTES);replacement.chmod(0o444);replacement.replace(lock)
        refused(lambda:e.WriterLock(expected).__enter__(),'same_payload_different_inode_lock_refused')
        refused(lambda:e.WriterLock({**expected,'inode':float(expected['inode'])}),
                'floating_lock_inode_refused')
        journal = e.journal_new('synthetic_one_use')
        e.put(journal,'INTENT.json',{'synthetic':True})
        refused(lambda:e.journal_new('synthetic_one_use'),'fresh_journal_reuse_refused')
        refused(lambda:e.put(journal,'INTENT.json',{'synthetic':True}),'durable_intent_overwrite_refused')
        runner = e.run_bounded
        dispatches = []
        fixturebody = b'synthetic cached blob'
        fixtureoid = h.native('blob',fixturebody)
        def synthetic_response(argv,body):
            dispatches.append(argv[-1])
            if '/git/blobs/' in argv[-1]:
                value = {'sha':fixtureoid,'size':len(fixturebody),'encoding':'base64',
                         'content':base64.b64encode(fixturebody).decode()}
            else:
                value = {'synthetic':True,'uncached':True}
            return types.SimpleNamespace(returncode=0,stdout=json.dumps(value).encode(),stderr=b'')
        e.run_bounded = synthetic_response
        cachejournal = e.journal_new('synthetic_cache')
        api = e.API(h,cachejournal)
        first = api('GET','git/blobs/'+fixtureoid)
        first['size'] = 0
        second = api('GET','git/blobs/'+fixtureoid)
        yes(len(dispatches) == 1 and second['size'] == len(fixturebody),'immutable_GET_cache_fresh_copy')
        second['content'] = 'changed caller object'
        yes(h.read_blob(api,fixtureoid) == fixturebody and len(dispatches) == 1,
            'cached_blob_still_native_authenticated')
        before = len(dispatches)
        for route in ('git/ref/heads/main','pulls/209','compare/'+'a'*40+'...'+'b'*40):
            api('GET',route);api('GET',route)
        yes(len(dispatches) == before+6,'mutable_ref_PR_compare_never_cached')
        fresh = e.API(h,cachejournal);fresh.number = api.number
        fresh('GET','git/blobs/'+fixtureoid)
        yes(len(dispatches) == before+7,'new_API_has_empty_independent_cache')
        raw,pinned,origin = fresh._immutable_cache['git/blobs/'+fixtureoid]
        fresh._immutable_cache['git/blobs/'+fixtureoid] = (raw+b' ',pinned,origin)
        refused(lambda:fresh('GET','git/blobs/'+fixtureoid),'cached_raw_bytes_tamper_refused')
        bad = e.API(h,cachejournal);bad.number = fresh.number
        refused(lambda:bad('GET','git/blobs/'+'d'*40),'GET_response_sha_must_match_immutable_route')
        yes(not bad._immutable_cache,'wrong_route_response_never_cached')
        e.run_bounded = runner
    result = e.run_bounded([sys.executable,'-E','-S','-B','-P','-c',
        'import sys; x=sys.stdin.buffer.read(); sys.stdout.buffer.write(x); sys.stderr.write("ok")'],b'synthetic stdin')
    yes(result.returncode == 0 and result.stdout == b'synthetic stdin' and result.stderr == b'ok',
        'bounded_concurrent_local_transport_positive')
    refused(lambda:e.run_bounded([sys.executable,'-E','-S','-B','-P','-c',
        'import os; os.write(2,b"x"*100000)'],None),'streaming_stderr_cap_kills_and_reaps')
    return {'schema':'pr209-native-preparation-synthetic-selftest-v1','status':'PASS',
            'checks':checks,'check_count':len(checks),'synthetic_only':True,'independent_audit':False,
            'phase_transition_real_log_preimage_pins':real_log_preimages,
            'service_calls':0,'native_objects_created':False,'global_views_modified':False,
            'actual_gate_or_acceptance_or_checkpoint_created':False}


if __name__ == '__main__':
    need_flags = sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path
    if not need_flags:
        raise RuntimeError('Use python3 -E -S -B -P')
    print(json.dumps(run(),sort_keys=True,indent=2))
