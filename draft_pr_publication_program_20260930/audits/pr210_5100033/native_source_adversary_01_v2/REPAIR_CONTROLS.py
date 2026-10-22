"""Independent, focused V2 repair checks; never dispatch gh or touch live views.

Exact copied executor candidate() runs only against an owned synthetic loader
and stopping logical API. No source/function/module/transport is monkeypatched.
The fixture lock identity is intentionally synthetic; no Root gate is created.
"""
from pathlib import Path
import ast
import base64
import copy
import datetime
import difflib
import hashlib
import json
import os
import select
import stat
import subprocess
import sys
import tempfile
import types

OWN = Path(__file__).absolute().parent
V1 = OWN.parent/'native_adoption_preparation_01'
V2 = OWN.parent/'native_adoption_preparation_02'
V2_PIN = {'bytes':4397,'sha256':'6e1df1fd6fbc21a4819d2fc69e319f538feb65ad4c58514d8dffd61692459520'}


def pin(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def load(path):
    value = types.ModuleType('independent_V2_'+path.stem)
    value.__file__ = str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),value.__dict__)
    return value


def run():
    checks,scenarios = [],[]
    def yes(ok,label):
        if ok is not True:raise RuntimeError(label)
        checks.append(label)
    def named(tree):
        return {n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    frozen = (V2/'SOURCE_MANIFEST.json').read_bytes()
    yes(pin(frozen) == V2_PIN,'exact_frozen_V2_manifest')
    manifest = json.loads(frozen)
    yes(manifest['total_files'] == 19 and manifest['total_bytes'] == 156579,'exact_nineteen_payload_scope')
    for row in manifest['source_files']:
        path = V2/row['path']
        yes(pin(path.read_bytes()) == {k:row[k] for k in ('bytes','sha256')} and stat.S_IMODE(path.stat().st_mode) == 0o444,'V2_frozen_'+row['path'])
    fixed_content = {'native210_model.py':{'bytes':34675,'sha256':'ff8d79fc245fcf55ac1d109ece1d3c5cd9c5f28bd51060e7efbc750ec41d2c4d'},'native_trees_readonly.py':{'bytes':4719,'sha256':'c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce'}}
    for name,expected in fixed_content.items():
        yes(pin((V2/name).read_bytes()) == expected,'unchanged_V1_content_pin_'+name)
    oldraw,newraw = (V1/'native210_future_executor.py').read_bytes(),(V2/'native210_future_executor.py').read_bytes()
    delta = ''.join(difflib.unified_diff(oldraw.decode().splitlines(keepends=True),newraw.decode().splitlines(keepends=True),fromfile='preserved_V1/native210_future_executor.py',tofile='current_V2/native210_future_executor.py')).encode()
    yes(delta == (V2/'V1_EXECUTOR_REPAIR_DELTA.patch').read_bytes(),'exact_full_repair_delta')
    oldtree,newtree = ast.parse(oldraw),ast.parse(newraw)
    oldnodes,newnodes = named(oldtree),named(newtree)
    yes(set(newnodes)-set(oldnodes) == {'api_argv'} and set(oldnodes)-set(newnodes) == set(),'only_new_code_node_is_pure_api_argv')
    changed = {name for name in oldnodes if ast.dump(oldnodes[name]) != ast.dump(newnodes[name])}
    yes(changed == {'API','candidate'},'only_API_and_candidate_changed')
    yes([ast.dump(n) for n in oldtree.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))] == [ast.dump(n) for n in newtree.body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))],'all_imports_globals_and_metadata_unchanged')
    for name in sorted(set(oldnodes)-changed):
        yes(ast.dump(oldnodes[name]) == ast.dump(newnodes[name]),'unchanged_V1_AST_'+name)
    candidate = copy.deepcopy(newnodes['candidate'])
    yes(len(candidate.body) == 2 and isinstance(candidate.body[1],ast.With) and ast.unparse(candidate.body[1].items[0].context_expr) == "WriterLock(m['writer_lock'])",'candidate_entire_effect_and_verifier_scope_held')
    candidate.body = candidate.body[:1]+candidate.body[1].body
    guard = next(n for n in ast.walk(candidate) if isinstance(n,ast.FunctionDef) and n.name == 'effect_guard')
    yes(ast.unparse(guard.body[0]) == 'lock.check()' and ast.unparse(guard.body[-1]) == 'lock.check()','guard_first_and_last_actions_check_lock')
    class StripChecks(ast.NodeTransformer):
        def visit_Expr(self,node):
            if isinstance(node.value,ast.Call) and ast.unparse(node.value.func) == 'lock.check':return None
            return self.generic_visit(node)
    candidate = StripChecks().visit(candidate)
    yes(ast.dump(candidate) == ast.dump(oldnodes['candidate']),'candidate_has_no_other_semantic_delta')
    oldcall = next(n for n in oldnodes['API'].body if isinstance(n,ast.FunctionDef) and n.name == '__call__')
    argv_assign = next(n for n in oldcall.body if isinstance(n,ast.Assign) and ast.unparse(n.targets[0]) == 'argv')
    argv_if = next(n for n in oldcall.body if isinstance(n,ast.If) and ast.unparse(n.test) == 'body is not None')
    class RestoreArgv(ast.NodeTransformer):
        def visit_Assign(self,node):
            if isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name) and node.value.func.id == 'api_argv':return [copy.deepcopy(argv_assign),copy.deepcopy(argv_if)]
            return self.generic_visit(node)
    repaired_api = RestoreArgv().visit(copy.deepcopy(newnodes['API']))
    yes(ast.dump(repaired_api) == ast.dump(oldnodes['API']),'API_has_no_other_semantic_delta')
    h = load(V2/'native210_model.py');c = h.core();e = load(V2/'native210_future_executor.py')
    previous_host = os.environ.get('GH_HOST')
    try:
        os.environ['GH_HOST'] = 'hostile-independent-fixture.invalid'
        routes = [('GET','git/ref/heads/main',False),('GET','pulls/210',False),('GET','git/trees/'+'a'*40,False),('POST','git/blobs',True),('POST','git/trees',True),('POST','git/commits',True)]
        for method,path,has_body in routes:
            expected = [e.GH,'api','--hostname','github.com','--method',method,'repos/AlecKriebel/Math/'+path]+(['--input','-'] if has_body else [])
            yes(e.api_argv(method,path,has_body) == expected,'hostile_env_canonical_argv_'+method+'_'+path)
    finally:
        if previous_host is None:os.environ.pop('GH_HOST',None)
        else:os.environ['GH_HOST'] = previous_host
    yes(pin((V2/'history/V1_SOURCE_AUDIT.md').read_bytes()) == {'bytes':8510,'sha256':'c1684544b62abc8d6f9bad9467f81e5ff5d845c5cfffd97f759a7349e19c005a'},'exact_preserved_V1_report_body')

    # This independently built native fixture exercises actual candidate(), not a surrogate.
    enc = lambda value:(json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
    baseline = json.loads((V2/'BASELINE_MEMBERSHIP.json').read_bytes())
    prior = {**h.baseline_facts(),**{k:baseline[k] for k in ('fully_completed_eligible_PRs','published_PRs','dated_eligible_total')}}
    marker = h.phase_marker('adoption100')
    oldviews = {h.VIEWS[0]:b'{"synthetic":true}\n',h.VIEWS[1]:b'synthetic case history\n',h.VIEWS[2]:enc(prior),h.VIEWS[3]:b'synthetic old markdown\n',h.VIEWS[4]:b'synthetic program history\n'}
    terminal = {**h.phase_facts('adoption100'),'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs']+[210],'published_PRs':baseline['published_PRs']+[210],'dated_eligible_total':99}
    overlay = {h.VIEWS[0]:enc(h.phase_facts('adoption100')),h.VIEWS[1]:oldviews[h.VIEWS[1]]+marker+b'\n',h.VIEWS[2]:enc(terminal),h.VIEWS[3]:marker+b'\n',h.VIEWS[4]:oldviews[h.VIEWS[4]]+marker+b'\n',h.CASE+'SYNTHETIC_BINARY.txt':b'owned fixture\0binary'}
    objects,blobs = {},{}
    def blob(raw):
        oid = h.native('blob',raw);blobs[oid] = raw;return oid
    def tree(rows):
        rows = sorted(rows,key=lambda r:r[0].encode()+(b'/' if r[1] == '040000' else b''))
        oid = c.tree_hash(rows)
        objects[oid] = {'sha':oid,'truncated':False,'tree':[{'path':n,'mode':mo,'type':k,'sha':s} for n,mo,k,s in rows]}
        return oid
    def root_tree(leaves):
        trie = {}
        for path,value in leaves.items():
            node = trie
            for part in path.split('/')[:-1]:node = node.setdefault(part,{})
            node[path.split('/')[-1]] = value
        def descend(node):return tree([(k,'040000','tree',descend(v)) if type(v) is dict else (k,*v) for k,v in node.items()])
        return descend(trie)
    queue = ('100644','blob',blob(b'opaque synthetic queue\n'))
    leaves = {**{p:('100644','blob',blob(raw)) for p,raw in oldviews.items()},h.QUEUE:queue,h.ATTEMPT[:-1]:('040000','tree',h.ATTEMPT_TREE),h.SHARED:('040000','tree',h.SHARED_TREE)}
    parent_tree = root_tree(leaves);pre = {p:leaves.get(p) for p in overlay}
    commits = {h.ANCHOR:{'sha':h.ANCHOR,'tree':{'sha':parent_tree},'parents':[{'sha':'7'*40}]},h.ORIGINAL:{'sha':h.ORIGINAL,'tree':{'sha':h.ORIGINAL_TREE},'parents':[{'sha':'462ac1846ea0abc36cb0e617d05c120351d943a0'}]},h.PREPARED:{'sha':h.PREPARED,'tree':{'sha':h.PREPARED_TREE},'parents':[{'sha':h.ORIGINAL},{'sha':h.MERGE_FIRST_PARENT}]},h.MERGED:{'sha':h.MERGED,'tree':{'sha':h.PREPARED_TREE},'parents':[{'sha':h.MERGE_FIRST_PARENT},{'sha':h.PREPARED}]}}
    pr = {'number':210,'head':{'sha':h.PREPARED},'base':{'ref':'main'},'draft':False,'state':'closed','merged':True,'merge_commit_sha':h.MERGED,'merged_at':h.MERGED_AT}
    def observer(method,path,body=None):
        if method != 'GET' or body is not None:raise RuntimeError('Synthetic observer GET only')
        if path == 'git/ref/heads/main':return {'object':{'sha':h.ANCHOR}}
        if path == 'pulls/210':return copy.deepcopy(pr)
        if path.startswith('compare/'):return {'status':'ahead','merge_base_commit':{'sha':path.split('/')[1].split('...')[0]}}
        oid = path.rsplit('/',1)[-1]
        if path.startswith('git/commits/'):return copy.deepcopy(commits[oid])
        if path.startswith('git/trees/'):return copy.deepcopy(objects[oid])
        if path.startswith('git/blobs/'):
            raw = blobs[oid];return {'sha':oid,'encoding':'base64','size':len(raw),'content':base64.b64encode(raw).decode()}
        raise RuntimeError('Unexpected synthetic route')
    identity = {'name':'Independent synthetic fixture','email':'fixture@example.invalid','date':'2026-10-17T04:00:00Z'}
    base_m = {'phase':'adoption100','facts':h.phase_facts('adoption100'),'expected_parent':h.ANCHOR,'expected_parent_tree':parent_tree,'protected_queue':dict(zip(('mode','type','sha'),queue)),'commit_message':'Independent V2 fixture only\n','commit_author':identity,'commit_committer':identity,'local_views':[{'path':p,'preimage':pin(raw)} for p,raw in oldviews.items()]}
    probe_code = 'import os,sys,fcntl; fd=os.open(sys.argv[1],os.O_RDONLY)\ntry: fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)\nexcept BlockingIOError: sys.exit(7)\nelse: sys.exit(0)'
    def probe(path):
        return subprocess.run([sys.executable,'-E','-S','-B','-P','-c',probe_code,str(path)],capture_output=True,check=False,timeout=3).returncode
    class LogicalPostStop(RuntimeError):pass
    modes = ['held_all_three','absent','wrong_device','wrong_inode','wrong_mode','wrong_payload','symlink','replaced_in_first_guard','payload_at_first_guard_end','replaced_after_blob','payload_after_tree','contention']
    for mode in modes:
        with tempfile.TemporaryDirectory(prefix='repair_'+mode+'_',dir=OWN/'_private') as temp:
            root = Path(temp)/'checkout';program = root/'draft_pr_publication_program_20260930';case = program/'audits/pr210_5100033';copied = case/'native_adoption_preparation_02';copied.mkdir(parents=True)
            target = copied/'native210_future_executor.py';target.write_bytes(newraw);target.chmod(0o444)
            ex = load(target)
            for path,raw in oldviews.items():
                target = root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);target.chmod(0o444)
            lockpath = program/'ROOT_GLOBAL_FIVE_WRITER.lock';lockpath.write_bytes(ex.LOCK_BYTES);lockpath.chmod(0o444)
            st = lockpath.stat();lock = {'path':h.WRITER_LOCK_REFERENCE['path'],'device':st.st_dev,'inode':st.st_ino,**pin(ex.LOCK_BYTES)}
            m = {**base_m,'writer_lock':lock,'candidate_journal':'INDEPENDENT_'+mode.upper()}
            journal = ex.journal_new(m['candidate_journal']);posts = [];loads = [0];main_reads = [0];retired = lockpath.with_name('retired_original.lock');holder = None
            def replace_lock():
                lockpath.rename(retired);lockpath.write_bytes(ex.LOCK_BYTES);lockpath.chmod(0o444)
            def change_payload():
                lockpath.chmod(0o644);lockpath.write_bytes(b'corrupt owned synthetic lock\n');lockpath.chmod(0o444)
            def fixture_load():
                loads[0] += 1
                return c,m,overlay,pre,{}
            def stopping_api(method,path,body=None,expected_oid=None):
                if method == 'POST':
                    posts.append(path)
                    yes(probe(retired if retired.exists() else lockpath) == 7,mode+'_held_at_'+path)
                    yes((journal/'CANDIDATE_DISPATCH_RESERVATION.json').exists() and loads[0] >= 3,mode+'_reserved_and_refreshed_at_'+path)
                    if mode == 'replaced_after_blob' and path == 'git/blobs':replace_lock()
                    if mode == 'payload_after_tree' and path == 'git/trees':change_payload()
                    if path == 'git/commits':raise LogicalPostStop('Stop before real API or independent readback transport')
                    return {'sha':expected_oid}
                answer = observer(method,path,body)
                if path == 'git/ref/heads/main':
                    main_reads[0] += 1
                    if mode == 'replaced_in_first_guard' and main_reads[0] == 3:replace_lock()
                    if mode == 'payload_at_first_guard_end' and main_reads[0] == 4:change_payload()
                return answer
            if mode == 'absent':lockpath.unlink()
            elif mode == 'wrong_device':m['writer_lock'] = {**lock,'device':lock['device']+1}
            elif mode == 'wrong_inode':m['writer_lock'] = {**lock,'inode':lock['inode']+1}
            elif mode == 'wrong_mode':lockpath.chmod(0o644)
            elif mode == 'wrong_payload':change_payload()
            elif mode == 'symlink':lockpath.rename(retired);lockpath.symlink_to(retired.name)
            elif mode == 'contention':
                code = 'import os,sys,fcntl; fd=os.open(sys.argv[1],os.O_RDONLY); fcntl.flock(fd,fcntl.LOCK_EX); print("HELD",flush=True); sys.stdin.buffer.read(1)'
                holder = subprocess.Popen([sys.executable,'-E','-S','-B','-P','-c',code,str(lockpath)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                yes(bool(select.select([holder.stdout],[],[],3)[0]) and holder.stdout.readline() == b'HELD\n','owned_other_process_lock_holder_ready')
            outcome = None
            try:
                ex.candidate(h,fixture_load,stopping_api,journal)
            except LogicalPostStop as error:
                outcome = type(error).__name__
                yes(mode == 'held_all_three' and posts == ['git/blobs','git/trees','git/commits'],'all_three_immutable_routes_hold_lock')
            except (RuntimeError,OSError) as error:
                outcome = type(error).__name__+': '+str(error)
                expected_posts = 1 if mode == 'replaced_after_blob' else 2 if mode == 'payload_after_tree' else 0
                yes(mode != 'held_all_three' and len(posts) == expected_posts,mode+'_stops_before_next_POST')
            else:
                raise RuntimeError('Stopping fixture unexpectedly completed')
            finally:
                if holder is not None:
                    try:holder.communicate(input=b'x',timeout=3)
                    except subprocess.TimeoutExpired:
                        holder.kill();holder.communicate(timeout=3)
            if mode != 'absent':
                yes(probe(retired if retired.exists() else lockpath) == 0,mode+'_original_inode_released_after_stop')
            scenarios.append({'mode':mode,'logical_POST_paths':posts,'loader_calls':loads[0],'MAIN_reads':main_reads[0],'outcome':outcome})
    yes((V2/'SOURCE_MANIFEST.json').read_bytes() == frozen,'V2_manifest_unchanged_after_controls')
    for row in manifest['source_files']:
        yes(pin((V2/row['path']).read_bytes()) == {k:row[k] for k in ('bytes','sha256')},'V2_payload_unchanged_after_'+row['path'])
    yes(list((OWN/'_private').iterdir()) == [],'owned_fixtures_cleaned')
    return {'schema':'pr210-independent-V2-repair-controls-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS_BOUNDED_SOURCE_REPAIRS_NO_OPERATIONAL_CLEARANCE','source_manifest_pin':V2_PIN,'check_count':len(checks),'checks':checks,'lock_scenarios':scenarios,'provider_API_calls':0,'local_Git_calls':0,'real_lock_or_current_five_touched':False,'actual_manifests_gates_native_objects_or_pointers_created':False,'target_sources_modified':False,'model_core_byte_unchanged':True,'no_source_function_module_or_transport_monkeypatch':True,'synthetic_fixtures_cleaned':True}


if __name__ == '__main__':
    if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Use python3 -E -S -B -P without -O')
    print(json.dumps(run(),sort_keys=True,indent=2))
