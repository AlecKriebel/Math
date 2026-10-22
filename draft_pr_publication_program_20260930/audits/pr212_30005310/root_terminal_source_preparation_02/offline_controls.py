"""Owned synthetic controls only; never calls production context/main/transport.

Copies unchanged inspector and primitives into a disposable synthetic checkout.
The inspector's dependency-explicit inspect core uses explicit synthetic driver,
runtime, pool and observations. Real descriptor/WriterLock/exclusive-write code
operates only on the new owned fixture inode. No real API/Root receipt is made.
"""
from pathlib import Path
import ast,copy,hashlib,json,os,re,tempfile,types

HERE=Path(__file__).resolve().parent;CASE=HERE.parent
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(name,path):
    m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
def write(p,b):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o444)

def run():
    checks=[]
    def ok(name,value):
        if type(value) is not bool or not value:raise AssertionError(name)
        checks.append({'name':name,'kind':'positive','passed':True})
    def refuse(name,fn):
        try:fn()
        except (RuntimeError,ValueError,KeyError,TypeError,FileExistsError,FileNotFoundError):
            checks.append({'name':name,'kind':'expected refusal','passed':True});return
        raise AssertionError('Accepted invalid '+name)
    src=(HERE/'ROOT_TERMINAL_INSPECTION.py').read_bytes()
    primitive=(CASE/'native_administrative_preparation_01/native212_primitives.py').read_bytes()
    baseline_raw=(CASE/'native_administrative_preparation_01/BASELINE_MEMBERSHIP.json').read_bytes()
    parser_path=CASE.parents[1]/'ordered_intakes_after_PR212_20261017/preparation_01/status_only_intake_after_pr212.py'
    parser_source=parser_path.read_bytes()
    parser_pin={'bytes':24760,'sha256':'0292388c3722d04cb2c11108d409c14759b61a370b0478fbbef41c92e19349eb'}
    ok('unchanged actual after212 parser pin',pin(parser_source)==parser_pin)
    queue_source=(CASE/'root_packet_preparation_01/_private_parent_capture_01/PARENT_QUEUE_BODY.txt').read_bytes()
    ownrow=[line for line in queue_source.splitlines(keepends=True) if b'30005310 / OWR-11695865-009' in line]
    ok('one recorded Main own-row fixture',len(ownrow)==1)
    # Use exact original source definition for the canonical unique-row grammar.
    model_source=(CASE/'native_administrative_preparation_01/native212_model.py').read_text()
    model_ast=ast.parse(model_source)
    row_node=next(n for n in model_ast.body if isinstance(n,ast.FunctionDef) and n.name=='own_queue_row')
    row_source=ast.get_source_segment(model_source,row_node)
    with tempfile.TemporaryDirectory(prefix='_synthetic_terminal_',dir=HERE) as temp:
        checkout=Path(temp)/'checkout';program=checkout/'program';a=program/'audits/pr212_30005310'
        b=a/'native_administrative_preparation_01';out=a/'root_terminal_source_preparation_01'
        out.mkdir(parents=True);b.mkdir(parents=True)
        write(out/'ROOT_TERMINAL_INSPECTION.py',src);write(b/'native212_primitives.py',primitive)
        t=load('synthetic_terminal212',out/'ROOT_TERMINAL_INSPECTION.py');e=load('synthetic_primitives212',b/'native212_primitives.py')
        ok('import inspector produces no operational output',list(out.iterdir())==[out/'ROOT_TERMINAL_INSPECTION.py'])
        ok('baseline exact853-byte pin',pin(baseline_raw)==t.BASELINE_PIN)
        ok('Main own queued-row pin exact',pin(ownrow[0])==t.MAIN_ROW_PIN)
        for left,right in [(True,1),(False,0),([1],[True]),({'a':[1]},{'a':[True]}),(({'a':1},),({'a':True},))]:
            ok('recursive typed inequality '+repr(left),not t.exact(left,right))
        for raw in (b'{"a":1,"a":1}',b'{"n":NaN}',b'{"n":Infinity}',b'{"n":1e999}'):
            refuse('duplicate/nonfinite JSON '+raw.decode(),lambda raw=raw:t.decode(raw))
        source_pin=pin(src);manifest_pin={'bytes':1,'sha256':'1'*64};policy={'operation':'terminal','mode':'approved-driver-api','extension_source':None,'extension_acceptance':None}
        accept={'schema':t.SOURCE_SCHEMA,'evidence_scope':'ACTUAL_ROOT_RECEIPT_SOURCE_ONLY','PR':212,'accepted':True,
            'terminal_source_pin':source_pin,'terminal_source_manifest_pin':manifest_pin,'approved_driver_pin':t.DRIVER_PIN,
            'receipt_schema':t.RECEIPT_SCHEMA,'Root_full_source_read':True,'independent_source_review_accepted':True,
            'transport_policy':policy,'source_acceptance_is_not_actual_terminal_or_numeric_authority':True}
        t.check_source_acceptance(accept,source_pin,manifest_pin,policy);ok('strict synthetic source acceptance accepted',True)
        for field in ('PR','accepted','Root_full_source_read','independent_source_review_accepted','source_acceptance_is_not_actual_terminal_or_numeric_authority'):
            bad=copy.deepcopy(accept);bad[field]=1 if type(bad[field]) is bool else True
            refuse('source gate typed field '+field,lambda bad=bad:t.check_source_acceptance(bad,source_pin,manifest_pin,policy))
        for field in ('schema','evidence_scope','terminal_source_pin','terminal_source_manifest_pin','approved_driver_pin','receipt_schema','transport_policy'):
            bad=copy.deepcopy(accept);bad.pop(field)
            refuse('source gate missing '+field,lambda bad=bad:t.check_source_acceptance(bad,source_pin,manifest_pin,policy))
        bad=copy.deepcopy(accept);bad['transport_policy']['mode']='implicit-fast-cache'
        refuse('implicit extension selection',lambda:t.check_source_acceptance(bad,source_pin,manifest_pin,policy))
        path=a/'fixture.json';write(path,b'{}\n');row={'path':str(path),**pin(b'{}\n')}
        refuse('extension source without separate gate',lambda:t.transport_policy({'extension_source':row,'extension_acceptance':None}))
        refuse('extension gate without source pin',lambda:t.transport_policy({'extension_source':None,'extension_acceptance':row}))
        ok('canonical0444 exact input',t.raw_ref(row)==b'{}\n')
        for changed in ({**row,'bytes':True},{**row,'sha256':'x'*64},{**row,'path':str(b/'..'/'fixture.json')}, {**row,'path':'relative.json'}):
            refuse('invalid input reference '+repr(changed),lambda changed=changed:t.raw_ref(changed))
        sym=a/'symlink.json';sym.symlink_to(path)
        refuse('symlink input',lambda:t.raw_ref({**row,'path':str(sym)}))
        path.chmod(0o644);refuse('writable input',lambda:t.raw_ref(row));path.chmod(0o444)
        calls=[]
        observer=types.SimpleNamespace()
        class Obs:
            actual_GET_origins={'origin':'synthetic'}
            def __call__(self,*args):calls.append(args);return {'synthetic':True}
        get=t.GetOnly(Obs());ok('GET route works',get('GET','pulls/212')=={'synthetic':True})
        ok('actual-origin mapping forwarded',get.actual_GET_origins=={'origin':'synthetic'})
        for method,route,body in [('POST','git/trees',{}),('PATCH','git/refs/heads/main',{}),('GET','pulls/213',None),('GET','git/blobs/'+'1'*40,{}),('GET','compare/'+'1'*40+'...'+'g'*40,None)]:
            before=len(calls);refuse('terminal route firewall '+method+' '+route,lambda method=method,route=route,body=body:get(method,route,body));ok('refused before transport '+route,len(calls)==before)
        class Broken:
            def __call__(self,*args):raise ValueError('synthetic uncertainty')
        broken=t.GetOnly(Broken());refuse('GET uncertainty stops',lambda:broken('GET','pulls/212'));refuse('no GET retry after uncertainty',lambda:broken('GET','pulls/212'))
        base=json.loads(baseline_raw);facts=copy.deepcopy(t.FIXED_FACTS)
        progress={**facts,**base,'dated_eligible_total':99};case=copy.deepcopy(facts)
        h=types.SimpleNamespace(phase_facts=lambda:copy.deepcopy(t.FIXED_FACTS),decode=t.decode,BASELINE_PIN=t.BASELINE_PIN,
            source_baseline=lambda:json.loads(baseline_raw),hexid=lambda x:type(x) is str and re.fullmatch('[0-9a-f]{40}',x) is not None,
            QUEUE_POLICY='PARENT_AND_C_WHOLE_QUEUE_FIXED_R_FOREIGN_ROWS_ONLY_OWN_EXACT')
        row_globals={'need':t.need,'re':re,'MAX_BODY':4_000_000};exec(compile(row_source,'copied_exact_own_queue_row','exec'),row_globals)
        h.own_queue_row=row_globals['own_queue_row'];h.VIEWS=('case.json','case_log.md','progress.json','progress.md','global_log.md')
        ok('accounting exact unchanged lists',t.accounting(h,{'facts':facts},case,progress,base)['dated_eligible_total']==99)
        for field,new in [('fully_completed_count',54),('published_count',38),('last_completed_PR',212),('next_numeric_intake_cursor',212),('goal_complete',True),('completed_eligible_workflow',True),('publication_workflow_completed',True),('publication_ready',True),('advance_to_next_PR_authorized_now',True),('current_PR_open_draft_unmerged',1)]:
            bad=copy.deepcopy(progress);bad[field]=new
            refuse('local conditional facts '+field,lambda bad=bad:t.accounting(h,{'facts':facts},case,bad,base))
        for field in ('fully_completed_eligible_PRs','published_PRs'):
            bad=copy.deepcopy(progress);bad[field][-1]=212
            refuse('count-only membership substitution '+field,lambda bad=bad:t.accounting(h,{'facts':facts},case,bad,base))
            bad=copy.deepcopy(progress);bad[field][0]=True
            refuse('membership Boolean substitution '+field,lambda bad=bad:t.accounting(h,{'facts':facts},case,bad,base))
        bad=copy.deepcopy(progress);bad['dated_eligible_total']=99.0
        refuse('float denominator99',lambda:t.accounting(h,{'facts':facts},case,bad,base))
        # Full dependency-explicit core, actual unchanged descriptor/write/fixture-lock primitives.
        lockpath=program/'ROOT_GLOBAL_FIVE_WRITER.lock';write(lockpath,e.LOCK_BYTES);st=lockpath.stat()
        lockref={'path':'program/ROOT_GLOBAL_FIVE_WRITER.lock','device':st.st_dev,'inode':st.st_ino,**pin(e.LOCK_BYTES)}
        overlay={h.VIEWS[0]:t.enc(case),h.VIEWS[1]:b'synthetic case log\n',h.VIEWS[2]:t.enc(progress),h.VIEWS[3]:b'synthetic progress\n',h.VIEWS[4]:b'synthetic global log\n'}
        for n,raw in overlay.items():write(checkout/n,raw)
        queue_body=b'| unrelated synthetic row |\n'+ownrow[0]
        qoid=hashlib.sha1(b'blob '+str(len(queue_body)).encode()+b'\0'+queue_body).hexdigest()
        origin={'fixture':'actual owned synthetic observer, never native transport'}
        class Pool:
            def get(self,api,oid,wanted=None):
                t.need(oid==qoid,'syntheticOID');t.need(wanted is None or t.exact(t.pin(queue_body),wanted),'synthetic whole body pin');return queue_body
            def origin(self,api,oid):return origin
        q={'policy':h.QUEUE_POLICY,'foreign_rows_may_differ':True,'own_row_pin':t.MAIN_ROW_PIN,
           'observed_QUEUE_oid':qoid,'whole_body_pin':pin(queue_body),'actual_native_body_origin':origin}
        admission={'parent':'1'*40,'parent_tree':'2'*40,'candidate':'3'*40,'tree':'4'*40}
        rt=types.SimpleNamespace(e=e,h=h,admission=admission,overlay=overlay,pool=Pool(),
            m={'facts':facts,'protected_queue_row_pin':t.MAIN_ROW_PIN,'protected_queue':{'mode':'100644','type':'blob','sha':qoid},
               'writer_lock':lockref,'local_views':[{'path':n} for n in h.VIEWS]})
        rt.m.update(expected_changed_paths=sorted(overlay),expected_new_directories=[])
        rt.seed=types.SimpleNamespace(s=types.SimpleNamespace(read_regular=lambda p:(t.readonly(p),{})))
        events=[];rt.refresh=lambda:events.append('runtime refresh')
        observation={'actual_MAIN_observed':'5'*40,'actual_MAIN_tree':'6'*40,'CAS_target':'3'*40,'CAS_target_tree':'4'*40,
            'native_final_ref_UTC':'2026-10-17T00:00:00+00:00',
            'selected_postimage_paths_verified':5,'protected_opaque_attempt_audit_verified':True,'coherent_before_after_ref':True,
            'CAS_or_completion_inferred_from_ancestry':False,'perpetual_or_write_time_Main_equality_claimed':False,
            'fresh_corrected_PR_status_observation':{'HEAD':t.CORRECTED_HEAD,'state':'open','draft':True,'merged':False,'current_status':'already_solved','same_selected_PR_identity':True},
            'Main_QUEUE_observation':q}
        t.native_semantics(rt,None,observation);ok('native queued row and corrected HEAD distinct',True)
        for field,new in [('HEAD','7'*40),('state','closed'),('draft',False),('merged',True),('current_status','claimed_solved'),('same_selected_PR_identity',1)]:
            bad=copy.deepcopy(observation);bad['fresh_corrected_PR_status_observation'][field]=new
            refuse('fresh corrected PR guard '+field,lambda bad=bad:t.native_semantics(rt,None,bad))
        for field,new in [('coherent_before_after_ref',False),('CAS_or_completion_inferred_from_ancestry',True),('perpetual_or_write_time_Main_equality_claimed',True),('selected_postimage_paths_verified',True)]:
            bad=copy.deepcopy(observation);bad[field]=new
            refuse('qualified R observation '+field,lambda bad=bad:t.native_semantics(rt,None,bad))
        sync=a/'ROOT_ADMIN212_SYNC_fixture/ACTUAL_FIVE_SYNC.json';syncraw=t.enc({'facts':facts,'all_five_local_postimages_verified':True});write(sync,syncraw)
        pointer=b/'ROOT_ACTUAL_ADMINISTRATIVE_POINTER.json';pointerraw=t.enc({'sync_path':str(sync),'sync_pin':pin(syncraw)});write(pointer,pointerraw)
        config={'actual_CAS':{'path':str(a/'synthetic_CAS.json'),**pin(b'{}\n')},'pointer':{'path':str(pointer),**pin(pointerraw)},
            'sync':{'path':str(sync),**pin(syncraw)},'source_acceptance':{'path':str(a/'synthetic_source_acceptance.json'),**pin(b'{}\n')},
            'extension_source':None,'extension_acceptance':None,'manifest':row,'logical_gate':row,'admission':row,'Root_gate':row,
            'receipt_name':'ROOT_ACTUAL_ADMINISTRATIVE_SKIP_VERIFICATION_01.json'}
        write(a/'synthetic_CAS.json',b'{}\n')
        class Driver:
            CHECKOUT=checkout
            @staticmethod
            def checked_pointer(rt,cas):events.append('pointer');return pin(t.readonly(pointer))
            @staticmethod
            def local_states(rt,all_post=False):
                t.need(all_post,'only all-post');events.append('all five')
                t.need(not (a/config['receipt_name']).exists(),'No mutable local-five equality after publication')
                for n,raw in overlay.items():t.need(t.readonly(checkout/n)==raw,'local post')
            @staticmethod
            def actual_cas(rt,row,api):
                t.need(not (a/config['receipt_name']).exists(),'No full CAS validation after publication')
                events.append('synthetic actualCAS validation');return {'synthetic_actual_CAS':True}
            @staticmethod
            def verify_immutable(rt,api):
                events.append('full candidate proof');return {'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,'candidate':'3'*40,'tree':'4'*40,
                   'selected_count':5,'changed_leaves':sorted(overlay),'new_directories':[],'deleted_directories':[]}
            @staticmethod
            def main_closure(rt,api):
                t.need(not (a/config['receipt_name']).exists(),'No mutable R proof after publication')
                events.append('coherent actual R');return copy.deepcopy(observation)
        class RefAPI:
            def __call__(self,method,path):
                t.need(method=='GET' and path=='git/ref/heads/main','synthetic GET-only final ref');return {'object':{'sha':'5'*40}}
        api=RefAPI();refresh=lambda:(source_pin,manifest_pin)
        class BadCAS(Driver):
            @staticmethod
            def actual_cas(rt,row,api):raise RuntimeError('synthetic actualCAS refused')
        class BadProof(Driver):
            @staticmethod
            def verify_immutable(rt,api):return {'full_scope_verified':False}
        class BadLocal(Driver):
            @staticmethod
            def local_states(rt,all_post=False):raise RuntimeError('synthetic local third state')
        class MovingR(Driver):
            calls=0
            @staticmethod
            def main_closure(rt,api):
                MovingR.calls+=1;out=copy.deepcopy(observation)
                if MovingR.calls>1:out['actual_MAIN_observed']='7'*40
                return out
        for label,drv in [('actualCAS-failure',BadCAS),('full-proof-failure',BadProof),('local-post-failure',BadLocal),('moving-R',MovingR)]:
            j=e.journal_new('ROOT_ADMIN212_READ_ROOT_TERMINAL_'+label)
            refuse('full core stops '+label,lambda drv=drv,j=j:t.inspect(drv,rt,api,config,refresh,j))
            ok('failed core emits no Root terminal '+label,not (a/config['receipt_name']).exists())
        journal=e.journal_new('ROOT_ADMIN212_READ_ROOT_TERMINAL_fixture')
        result=t.inspect(Driver,rt,api,config,refresh,journal)
        receipt=Path(result['terminal_receipt']['path']);saved=t.decode(receipt.read_bytes())
        ok('separate Root receipt outside B',receipt.parent==a and not receipt.is_relative_to(b))
        ok('exclusive receipt readonly0444',receipt.stat().st_mode&0o777==0o444)
        ok('actual schema exact',saved['schema']==t.RECEIPT_SCHEMA)
        ok('terminal only sets numeric authority',saved['advance_to_next_PR_authorized_now'] is True and saved['next_numeric_intake_cursor']==213 and facts['advance_to_next_PR_authorized_now'] is False)
        ok('no eligible/publication completion',saved['completed_eligible_workflow'] is False and saved['publication_workflow_completed'] is False and saved['publication_ready'] is False and saved['goal_complete'] is False)
        ok('top-level exact membership arrays preserved',saved['fully_completed_eligible_PRs']==base['fully_completed_eligible_PRs'] and saved['published_PRs']==base['published_PRs'] and saved['all53_37_memberships_unchanged'] is True)
        # Real generated bytes from inspect/publication enter the unchanged
        # consumer function. No detached hand-written positive proof is used.
        parser_dir=out/'_intake_parser';parser_dir.mkdir()
        write(parser_dir/'status_only_intake_after_pr212.py',parser_source)
        write(parser_dir/'BASELINE_MEMBERSHIP.json',baseline_raw)
        parser=load('synthetic_unchanged_after212_parser',parser_dir/'status_only_intake_after_pr212.py')
        generated=receipt.read_bytes();consumed=parser.completion_proof(generated,pin(generated))
        ok('generated published record accepted by unchanged intake parser',consumed==saved)
        ok('complete generated-record core has no mutable checks after publication',True)
        ok('consumer import/completion function makes no network calls',parser.REQUESTS==[] and parser.ACTIVE_PR is None)
        ok('three required integration fields present and typed',saved['numeric_advance_conditional_on_actual_Root_terminal'] is False and saved['no_PR_or_publication_actions'] is True and type(saved['protected_body_paths_verified']) is int and saved['protected_body_paths_verified']==0)
        integration={'parser_pin':parser_pin,'generated_record_pin':pin(generated),
          'generated_by':'unchanged repaired inspector inspect core and staged exclusive publisher in own synthetic fixture',
          'consumer':'unchanged completion_proof(actual_generated_bytes,actual_generated_pin)',
          'accepted':True,'actual_native_or_intake_execution':False,'synthetic_only':True}
        for field,bad_value in [('numeric_advance_conditional_on_actual_Root_terminal',True),('no_PR_or_publication_actions',False),('protected_body_paths_verified',False)]:
            bad=copy.deepcopy(saved);bad[field]=bad_value;bad_raw=t.enc(bad)
            refuse('consumer rejects malformed generated-record field '+field,lambda bad_raw=bad_raw:parser.completion_proof(bad_raw,pin(bad_raw)))
        for field in ('numeric_advance_conditional_on_actual_Root_terminal','no_PR_or_publication_actions','protected_body_paths_verified'):
            bad=copy.deepcopy(saved);bad.pop(field);bad_raw=t.enc(bad)
            refuse('consumer rejects omitted generated-record field '+field,lambda bad_raw=bad_raw:parser.completion_proof(bad_raw,pin(bad_raw)))
        ok('proof/source/runtime/local/native guards exercised',all(x in events for x in ('runtime refresh','pointer','all five','full candidate proof','coherent actual R','synthetic actualCAS validation')))
        ok('B journal proof exists', (journal/'ROOT_REPEATED_IMMUTABLE_PROOF.json').is_file())
        refuse('Root receipt cannot overwrite',lambda:t.exclusive_root_receipt(e,receipt,t.enc(saved),lambda:None,lambda:None))
        refuse('old B-only put cannot write Root A',lambda:e.put(a,'SHOULD_NOT_EXIST.json',{}))
        refuse('Root writer refuses B path',lambda:t.exclusive_root_receipt(e,b/receipt.name,t.enc(saved),lambda:None,lambda:None))
        refuse('Root writer refuses alternate receipt name',lambda:t.exclusive_root_receipt(e,a/'ROOT_ACTUAL_ADMINISTRATIVE_SKIP_VERIFICATION_02.json',t.enc(saved),lambda:None,lambda:None))
        bad=copy.deepcopy(config);bad['sync']['sha256']='0'*64
        refuse('externally pinned sync mismatch',lambda:t.pointer_and_posts(Driver,rt,bad))
        bad=copy.deepcopy(config);bad['pointer']['sha256']='0'*64
        refuse('externally pinned pointer mismatch',lambda:t.pointer_and_posts(Driver,rt,bad))
        # Own fixture cleanup permits repeated publisher fault scenarios. The
        # production writer never unlinks/replaces a final-name authority.
        receipt.unlink()
        payload=t.enc({'explicitly_synthetic_publication_fault_probe':True});history=[];foreign={'R':'before'}
        class Ops:
            linked=False
            def fsync(self,fd):return os.fsync(fd)
            def link(self,*args,**kwargs):
                os.link(*args,**kwargs);self.linked=True;foreign['R']='later foreign Main';history.append('published')
            def unlink(self,*args,**kwargs):return os.unlink(*args,**kwargs)
        def mutable_guard():
            ok('final mutable guard sees no published final',not receipt.exists())
            pending=list(a.glob('.pr212-root-terminal-pending-*'))
            ok('final guard sees complete readonly pending',len(pending)==1 and t.readonly(pending[0])==payload)
            history.append('last mutable guard')
        def identities():
            ok('postpublication identity only sees exact final',receipt.read_bytes()==payload)
            history.append('post identity')
        pub=t.exclusive_root_receipt(e,receipt,payload,mutable_guard,identities,local_ops=Ops())
        ok('atomic publication tolerates later foreign Main movement',foreign['R']=='later foreign Main' and pub['post_publication_mutable_guard_performed'] is False)
        ok('last mutable guard precedes publication and identity follows',history.index('last mutable guard')<history.index('published')<history.index('post identity'))
        ok('successful publisher removes own pending',not list(a.glob('.pr212-root-terminal-pending-*')))
        receipt.unlink()
        def fail_guard():raise RuntimeError('synthetic R changed before publish')
        refuse('final mutable failure before link',lambda:t.exclusive_root_receipt(e,receipt,payload,fail_guard,lambda:None))
        ok('guard failure leaves no final authority or pending',not receipt.exists() and not list(a.glob('.pr212-root-terminal-pending-*')))
        class FailPendingFsync(Ops):
            def fsync(self,fd):raise OSError('synthetic pending file durability failure')
        refuse('pending fsync failure is unpublished',lambda:t.exclusive_root_receipt(e,receipt,payload,lambda:None,lambda:None,local_ops=FailPendingFsync()))
        ok('pending durability failure publishes no final authority',not receipt.exists())
        for pending in a.glob('.pr212-root-terminal-pending-*'):pending.unlink()
        class FailPublishedFsync(Ops):
            def fsync(self,fd):
                if self.linked:raise OSError('synthetic post-link directory durability failure')
                return os.fsync(fd)
        try:t.exclusive_root_receipt(e,receipt,payload,lambda:None,lambda:None,local_ops=FailPublishedFsync())
        except t.TerminalPublicationUncertain as error:
            ok('post-link fsync uncertainty typed and explicit',error.details['stage']=='published_directory_fsync' and error.details['exclusive_final_link_returned_success'] is True and error.details['automatic_retry_overwrite_or_unlink_final_forbidden'] is True)
        else:raise AssertionError('Missing post-link uncertainty')
        ok('post-link failure preserves final entry for readonly reconciliation',receipt.read_bytes()==payload)
        refuse('uncertain publication not automatically retried',lambda:t.exclusive_root_receipt(e,receipt,payload,lambda:None,lambda:None))
        receipt.unlink()
        for pending in a.glob('.pr212-root-terminal-pending-*'):pending.unlink()
        class UnknownLink(Ops):
            def link(self,*args,**kwargs):
                os.link(*args,**kwargs);raise OSError('synthetic dispatch returned uncertain after link')
        try:t.exclusive_root_receipt(e,receipt,payload,lambda:None,lambda:None,local_ops=UnknownLink())
        except t.TerminalPublicationUncertain as error:
            ok('uncertain exclusive-link outcome explicit',error.details['stage']=='exclusive_publication' and error.details['exclusive_final_link_returned_success'] is False and error.details['final_file_may_exist'] is True)
        else:raise AssertionError('Missing link outcome uncertainty')
        ok('unknown link leaves exact final for readonly diagnosis',receipt.read_bytes()==payload)
        receipt.unlink()
        for pending in a.glob('.pr212-root-terminal-pending-*'):pending.unlink()
        def fail_identity():raise RuntimeError('synthetic post-publication source/lock identity failure')
        try:t.exclusive_root_receipt(e,receipt,payload,lambda:None,fail_identity)
        except t.TerminalPublicationUncertain as error:
            ok('post-publication identity uncertainty explicit',error.details['stage']=='published_source_lock_identity' and error.details['final_file_may_exist'] is True)
        else:raise AssertionError('Missing identity uncertainty')
        ok('identity uncertainty does not unlink published final',receipt.read_bytes()==payload)
        receipt.unlink()
        for pending in a.glob('.pr212-root-terminal-pending-*'):pending.unlink()
        ok('live production terminal absent by construction',not (CASE/'ROOT_ACTUAL_ADMINISTRATIVE_SKIP_VERIFICATION_01.json').exists())
    return {'schema':'pr212-root-terminal-owned-offline-controls-v1','status':'PASS','check_count':len(checks),'checks':checks,
        'source_pin':pin(src),'primitive_pin':pin(primitive),'baseline_pin':pin(baseline_raw),
        'generated_record_intake_parser_integration':integration,
        'synthetic_only':True,'production_context_or_CLI_executed':False,'actual_native_GETs':0,'production_original_lock_acquired':False,
        'production_Root_receipts_gates_current_five_ref_PR_intake_writes':0,
        'fixture_native_origins_and_CAS_are_explicitly_synthetic':True,'fixture_removed':True,
        'scope':'Own strict semantics/route/writer controls and unchanged descriptor/fixture-lock primitives; not actual Root authority, live API/CAS, complete driver-parser replay, FastAPI implementation or global concurrency certification.'}

if __name__=='__main__':
    result=run();(HERE/'OFFLINE_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','check_count','actual_native_GETs','production_Root_receipts_gates_current_five_ref_PR_intake_writes')},indent=2))
