"""Inactive Root PR239 completion terminal inspector; import has no effects.

Preparation does not invoke this CLI. Later actual Root use requires separately
pinned source acceptance, logical/admission/CAS evidence and actual five sync.
Only native GET routes exist here. Root alone may issue the exclusive external
terminal receipt after the original stable lock and all factual checks succeed.
"""
import argparse,datetime,hashlib,json,math,os,re,stat,sys,types
from pathlib import Path

BASE=Path(__file__).absolute().parent
A=BASE.parent
B=BASE
CHECKOUT=A.parents[2]
DRIVER_PIN={'bytes': 45277, 'sha256': '457714f6a263efb7fc048acc1a6bed825664698d816caf7ffbeaaa52edf184a6'}
RECEIPT_SCHEMA='pr239-root-actual-completion-verification-v1'
SOURCE_SCHEMA='pr239-root-terminal-inspector-source-acceptance-v1'
BASELINE_PIN={'bytes': 889, 'sha256': '36258fde3b9a95d4ed8baf7aebff34030a25267b92b08d58256ebac2404b52ce'}
FIXED_FACTS={'active_PR': 239, 'phase': 'completion100', 'workflow_percent': 100, 'completed': True, 'fully_completed_count': 56, 'published_count': 40, 'last_completed_PR': 239, 'next_numeric_intake_cursor': 240, 'goal_complete': False, 'completed_eligible_workflow': True, 'publication_workflow_completed': True, 'publication_ready': True, 'original_eligible_status': 'claimed_solved', 'current_status': 'claimed_solved', 'current_head': '7f17eef77c52b2d9b2ec3ad0803c016267fa6496', 'new_publication_workflow': True, 'adopted_existing_publication': False, 'no_new_provider_publication_or_tracker_append': False, 'numeric_advance_conditional_on_actual_Root_terminal': True, 'advance_to_next_PR_authorized_now': False}

def need(value,message):
    if type(value) is not bool or not value:raise RuntimeError(message)

def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) in (list,tuple):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def enc(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def decode(raw):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'Duplicate JSON key');out[k]=v
        return out
    def finite(s):
        value=float(s);need(math.isfinite(value),'Nonfinite JSON number');return value
    return json.loads(raw,object_pairs_hook=pairs,parse_float=finite,
                      parse_constant=lambda s:need(False,'Nonfinite JSON constant'))

def bytepin(row):
    need(type(row) is dict and set(row)=={'bytes','sha256'} and type(row['bytes']) is int
         and 0<row['bytes']<=4_000_000 and type(row['sha256']) is str
         and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'Exact bounded typed byte pin')
    return row

def checked_ref(row,case=A):
    need(type(row) is dict and set(row)=={'path','bytes','sha256'} and type(row['path']) is str,
         'Exact externally supplied file reference')
    p=Path(row['path'])
    need(p.is_absolute() and p.is_relative_to(case) and p.resolve()==p,'Canonical case-owned reference')
    bytepin({k:row[k] for k in ('bytes','sha256')})
    return p

def readonly(path,cap=4_000_000,checkout=CHECKOUT):
    """Stable no-follow readonly0444 source/evidence read; no implicit path discovery."""
    need(path.is_absolute() and path.is_relative_to(checkout) and path.resolve()==path,
         'Canonical checkout-owned readonly input')
    handles=[];fd=None
    try:
        root=Path('/');parent=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        handles.append((root,parent,os.fstat(parent)))
        for part in path.parent.parts[1:]:
            root=root/part;parent=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent)
            handles.append((root,parent,os.fstat(parent)))
        fd=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent)
        before=os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444
             and 0<=before.st_size<=cap,'Bounded readonly0444 regular input')
        with os.fdopen(fd,'rb',closefd=False) as stream:raw=stream.read(cap+1)
        after,linked=os.fstat(fd),path.lstat()
        fields=lambda q:(q.st_dev,q.st_ino,q.st_size,q.st_mtime_ns,q.st_ctime_ns)
        need(fields(before)==fields(after)==fields(linked) and stat.S_ISREG(linked.st_mode)
             and stat.S_IMODE(linked.st_mode)==0o444 and len(raw)==after.st_size,'Input changed during descriptor read')
        for p,descriptor,initial in handles:
            x,y=os.fstat(descriptor),p.lstat()
            need(stat.S_ISDIR(y.st_mode) and (x.st_dev,x.st_ino)==(y.st_dev,y.st_ino)==(initial.st_dev,initial.st_ino),
                 'Readonly ancestor identity changed')
        return raw
    finally:
        if fd is not None:os.close(fd)
        for p,descriptor,initial in reversed(handles):os.close(descriptor)

def raw_ref(row,case=A):
    raw=readonly(checked_ref(row,case))
    need(exact(pin(raw),{k:row[k] for k in ('bytes','sha256')}),'Externally pinned body differs')
    return raw

def source_closure():
    source=readonly(Path(__file__).absolute())
    raw=readonly(BASE/'SOURCE_MANIFEST.json');m=decode(raw)
    need(type(m) is dict and m.get('schema')=='pr239-completion-source-manifest-v1'
         and m.get('source_only') is True and m.get('self_excluded') is True,'Terminal source-only closure')
    rows=m.get('files')
    need(type(rows) is list and 3<=len(rows)<=20 and all(type(r) is dict for r in rows),'Finite terminal source rows')
    names=[r.get('path') for r in rows]
    need(all(type(n) is str and Path(n).name==n and n not in ('','.', '..','SOURCE_MANIFEST.json','EXTERNAL_SEAL.json') for n in names)
         and names==sorted(names) and len(names)==len(set(names)),'Sorted positive basename-only closure')
    for r in rows:
        need(set(r)=={'path','bytes','sha256'},'Exact source row fields')
        need(exact(pin(readonly(BASE/r['path'])),bytepin({k:r[k] for k in ('bytes','sha256')})),'Terminal source row changed')
    need({'path':Path(__file__).name,**pin(source)} in rows,'Inspector absent from own source closure')
    return pin(source),pin(raw)

def transport_policy(config):
    ext=config.get('extension_source');gate=config.get('extension_acceptance')
    need((ext is None)==(gate is None),'Extension source and separate acceptance supplied together')
    if ext is not None:
        checked_ref(ext);checked_ref(gate)
    return {'operation':'terminal','mode':'approved-driver-api' if ext is None else 'separately-accepted-extension',
            'extension_source':ext,'extension_acceptance':gate}

def check_source_acceptance(value,source_pin,manifest_pin,policy):
    expected={'schema':SOURCE_SCHEMA,'evidence_scope':'ACTUAL_ROOT_RECEIPT_SOURCE_ONLY','PR':239,
       'accepted':True,'terminal_source_pin':source_pin,'terminal_source_manifest_pin':manifest_pin,
       'approved_driver_pin':DRIVER_PIN,'receipt_schema':RECEIPT_SCHEMA,
       'Root_full_source_read':True,'independent_source_review_accepted':True,
       'transport_policy':policy,'source_acceptance_is_not_actual_terminal_or_numeric_authority':True}
    need(type(value) is dict and all(k in value and exact(value[k],v) for k,v in expected.items()),
         'Separate exact typed Root terminal-source/transport acceptance required')

def context(config):
    need(type(config) is dict and set(config)=={'manifest','logical_gate','admission','Root_gate','actual_CAS',
       'pointer','sync','source_acceptance','extension_source','extension_acceptance','journal','receipt_name'},
       'Exact terminal configuration fields')
    for key in ('manifest','logical_gate','admission','Root_gate','actual_CAS','pointer','sync','source_acceptance'):
        checked_ref(config[key])
    need(config['pointer']['path']==str(B/'ROOT_ACTUAL_COMPLETION100_POINTER.json'),'Only original actual pointer path')
    need(type(config['journal']) is str and re.fullmatch('ROOT_COMPLETE239_READ_ROOT_TERMINAL_[A-Za-z0-9_-]{1,35}',config['journal']) is not None,
         'Fresh bounded read-only Root terminal journal')
    need(type(config['receipt_name']) is str and config['receipt_name']=='ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json',
         'Exact external Root terminal receipt basename')
    policy=transport_policy(config)
    def refresh():
        own,manifest=source_closure()
        check_source_acceptance(decode(raw_ref(config['source_acceptance'])),own,manifest,policy)
        return own,manifest
    own,manifest=refresh()
    path=B/'completion_checkpoint.py';raw=readonly(path)
    need(exact(pin(raw),DRIVER_PIN),'Approved pinned PR239 driver differs')
    driver=types.ModuleType('Root_PR239_terminal_approved_driver');driver.__file__=str(path)
    exec(compile(raw,str(path),'exec'),driver.__dict__)
    seed=driver.Seed(config['manifest'],config['logical_gate'])
    rt=driver.Runtime(seed,config['admission'],config['Root_gate'])
    need(rt.m['phase']=='completion100','Separate final phase100 only;95 cannot publish actual terminal')
    need(exact(seed.source_pin,DRIVER_PIN),'Seed did not bind approved driver')
    if config['extension_source'] is not None:
        extpath=checked_ref(config['extension_source']);ext_raw=raw_ref(config['extension_source'])
        ext=types.ModuleType('Root_PR239_terminal_explicit_extension');ext.__file__=str(extpath)
        exec(compile(ext_raw,str(extpath),'exec'),ext.__dict__)
        need(callable(getattr(ext,'bind_runtime',None)) and callable(getattr(ext,'make_readonly_api',None)),
             'Pinned extension lacks explicit reviewed interface')
        rt=ext.bind_runtime(driver,rt,config['extension_acceptance'],'terminal')
        factory=lambda journal:ext.make_readonly_api(driver,rt,journal)
    else:factory=lambda journal:rt.e.API(rt.h,journal,mutate=False)
    return driver,rt,factory,refresh

class GetOnly:
    """Terminal-local route firewall retaining the actual API's raw blob origins."""
    def __init__(self,observer):self.observer=observer;self.failed=False
    @property
    def actual_GET_origins(self):return getattr(self.observer,'actual_GET_origins',{})
    def __call__(self,method,path,body=None):
        need(not self.failed,'Terminal observer stopped after uncertainty')
        allowed=path in ('git/ref/heads/main','pulls/239') or (type(path) is str and re.fullmatch(
          r'git/(?:commits|trees|blobs)/[0-9a-f]{40}|compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}',path) is not None)
        need(method=='GET' and body is None and allowed,'Terminal native GET-only routes')
        try:return self.observer('GET',path)
        except BaseException:self.failed=True;raise

def accounting(h,m,case,progress,baseline):
    need(exact(h.phase_facts(),FIXED_FACTS) and exact(m['facts'],FIXED_FACTS),'Approved conditional completion facts differ')
    for value in (case,progress):
        need(type(value) is dict and all(k in value and exact(value[k],v) for k,v in FIXED_FACTS.items()),
             'Exact typed conditional five-post completion facts')
        need(value.get('conditional_proposal_only') is True,'Five proposals cannot be Root actual terminal authority')
    need(type(progress.get('dated_eligible_total')) is int and progress['dated_eligible_total']==99,'Dated denominator99')
    need(type(baseline) is dict and set(baseline)=={'fully_completed_eligible_PRs','published_PRs'},'Exact baseline fields')
    for key,count in (('fully_completed_eligible_PRs',55),('published_PRs',39)):
        arr=baseline[key]
        need(type(arr) is list and len(arr)==count and all(type(x) is int for x in arr)
             and arr==sorted(set(arr)) and all(n not in arr for n in range(219,240))
             and exact(progress.get(key),arr+[239]),'Exact55/39 baseline plus239 only')
    return {'old_memberships':baseline,'new_memberships':{k:v+[239] for k,v in baseline.items()},
            'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs']+[239],
            'published_PRs':baseline['published_PRs']+[239],'dated_eligible_total':99}

def native_semantics(rt,api,observation):
    h=rt.h
    need(type(observation) is dict and observation.get('coherent_before_after_ref') is True
         and observation.get('CAS_or_completion_inferred_from_ancestry') is False
         and observation.get('perpetual_or_write_time_Main_equality_claimed') is False,
         'Coherent qualified actual R closure required')
    need(h.hexid(observation.get('actual_MAIN_observed')) and h.hexid(observation.get('actual_MAIN_tree'))
         and exact(observation.get('CAS_target'),rt.admission['candidate'])
         and exact(observation.get('CAS_target_tree'),rt.admission['tree'])
         and type(observation.get('selected_postimage_paths_verified')) is int
         and observation['selected_postimage_paths_verified']==len(rt.overlay)
         and type(observation.get('protected_body_paths_verified')) is int
         and observation['protected_body_paths_verified']==len(rt.m['protected_bodies'])
         and observation.get('protected_opaque_attempt_audit_verified') is True,'Exact C/R/root/closure association')
    pr=observation.get('fresh_merged_PR_status_observation')
    wanted={'HEAD':h.CURRENT,'state':'closed','draft':False,'merged':True,'current_status':'claimed_solved',
            'original_merge_commit':h.merge_identity(rt.m)['merge_candidate'],'same_selected_PR_identity':True}
    need(type(pr) is dict and all(k in pr and exact(pr[k],v) for k,v in wanted.items()),
         'Actually merged claimed_solved PR239 must match earlier Root merge95 CAS')
    queue=observation.get('Main_QUEUE_observation')
    need(type(queue) is dict and queue.get('policy')==h.QUEUE_POLICY and queue.get('foreign_rows_may_differ') is True
         and exact(queue.get('own_row_pin'),rt.m['protected_queue_row_pin']),
         'Exact preserved fresh-parent own Main row and qualified foreign-row policy')
    oid=queue.get('observed_QUEUE_oid');need(h.hexid(oid),'Actual whole MainQUEUE native OID')
    raw=rt.pool.get(api,oid,queue['whole_body_pin']);row,cells=h.own_queue_row(raw)
    need(exact(pin(row),rt.m['protected_queue_row_pin']),'Actual full native MainQUEUE own row differs')
    need(exact(rt.pool.origin(api,oid),queue['actual_native_body_origin']),'Actual full QUEUE GET origin')
    return queue

def pointer_and_posts(driver,rt,config):
    h=rt.h
    observed_pin=driver.checked_pointer(rt,config['actual_CAS'])
    pointer_raw=raw_ref(config['pointer']);need(exact(pin(pointer_raw),observed_pin),'External actual pointer pin differs')
    pointer=h.decode(pointer_raw)
    need(pointer['sync_path']==config['sync']['path'] and exact(pointer['sync_pin'],{k:config['sync'][k] for k in ('bytes','sha256')}),
         'Separate externally pinned actual sync association')
    sync_raw=raw_ref(config['sync']);sync=h.decode(sync_raw)
    need(exact(sync.get('facts'),FIXED_FACTS) and sync.get('all_five_local_postimages_verified') is True,
         'Actual sync facts/post condition differs')
    driver.local_states(rt,all_post=True)
    need(len(rt.m['local_views'])==5 and [r['path'] for r in rt.m['local_views']]==list(h.VIEWS),
         'Exactly ordered five local views')
    files=[];bodies={}
    for row in rt.m['local_views']:
        raw,identity=rt.seed.s.read_regular(driver.CHECKOUT/row['path'])
        need(type(raw) is bytes and raw==rt.overlay[row['path']],'Full local five postimage bytes differ')
        files.append({'path':row['path'],'postimage':pin(raw)});bodies[row['path']]=raw
    need(exact(h.BASELINE_PIN,BASELINE_PIN),'Exact accepted55/39 baseline pin required')
    lists=accounting(h,rt.m,h.decode(bodies[h.VIEWS[0]]),h.decode(bodies[h.VIEWS[2]]),h.source_baseline())
    return observed_pin,pin(sync_raw),files,lists

class TerminalPublicationUncertain(RuntimeError):
    """Local publication/durability uncertainty; never a retry/overwrite instruction."""
    def __init__(self,path,pending,stage,published,error):
        self.details={'schema':'pr239-root-terminal-local-publication-uncertainty-v1',
          'path':str(path),'pending_path':str(pending),'stage':stage,
          'exclusive_final_link_returned_success':published,'exception_type':type(error).__name__,
          'final_file_may_exist':True,'local_durability_or_identity_unconfirmed':True,
          'automatic_retry_overwrite_or_unlink_final_forbidden':True,
          'required_next_step':'Root read-only reconcile exact final/pending bytes, mode, inode and durability before separately deciding acceptance; file presence alone is insufficient.'}
        super().__init__(json.dumps(self.details,sort_keys=True))

def exclusive_root_receipt(e,path,raw,final_guard,identity_guard,*,local_ops=None):
    """Fsync pending bytes, final mutable guard, exclusive atomic publish.

    After publication only file/descriptor/source/held-lock identity is checked.
    local_ops is a dependency-explicit owned-fixture fault seam, unused by CLI.
    """
    need(type(raw) is bytes and len(raw)<=4_000_000 and path.parent==A
         and path.name=='ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json',
         'Only bounded external Root terminal receipt allowed')
    ops=os if local_ops is None else local_ops
    pending=path.with_name('.pr239-root-terminal-pending-'+str(os.getpid())+'-'+os.urandom(16).hex())
    attempted=False;published=False;stage='pending_create';pending_identity=None
    with e.ParentHandle(path) as parent:
        parent.check()
        try:os.stat(path.name,dir_fd=parent.fd,follow_symlinks=False)
        except FileNotFoundError:pass
        else:raise FileExistsError('Fixed Root terminal already exists; read-only reconciliation required')
        try:
            fd=os.open(pending.name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444,dir_fd=parent.fd)
            try:
                with os.fdopen(fd,'wb',closefd=False) as stream:
                    need(stream.write(raw)==len(raw),'Short pending Root receipt write')
                    stream.flush();os.fchmod(fd,0o444);stage='pending_file_fsync';ops.fsync(fd)
                s=os.fstat(fd);pending_identity=(s.st_dev,s.st_ino)
            finally:os.close(fd)
        except BaseException as error:
            raise RuntimeError('Unpublished pending preparation/durability failed; no final-name dispatch attempted; inspect own pending read-only: '+str(pending)) from error
        try:
            parent.check();need(readonly(pending)==raw,'Full readonly pending receipt readback differs')
            stage='pending_directory_fsync';ops.fsync(parent.fd)
            stage='final_mutable_guard';final_guard()
            parent.check()
            entry=os.stat(pending.name,dir_fd=parent.fd,follow_symlinks=False)
            need(stat.S_ISREG(entry.st_mode) and stat.S_IMODE(entry.st_mode)==0o444
                 and (entry.st_dev,entry.st_ino)==pending_identity and readonly(pending)==raw,
                 'Pending bytes/mode/inode changed before exclusive publication')
            stage='exclusive_publication';attempted=True
            ops.link(pending.name,path.name,src_dir_fd=parent.fd,dst_dir_fd=parent.fd,follow_symlinks=False)
            published=True
            stage='published_directory_fsync';ops.fsync(parent.fd)
            stage='published_file_readback';parent.check()
            entry=os.stat(path.name,dir_fd=parent.fd,follow_symlinks=False)
            need(stat.S_ISREG(entry.st_mode) and stat.S_IMODE(entry.st_mode)==0o444
                 and (entry.st_dev,entry.st_ino)==pending_identity and readonly(path)==raw,
                 'Published receipt bytes/mode/inode readback differs')
            stage='published_source_lock_identity';identity_guard()
            stage='pending_cleanup';ops.unlink(pending.name,dir_fd=parent.fd)
            stage='cleanup_directory_fsync';ops.fsync(parent.fd)
            parent.check();stage='final_source_lock_identity';identity_guard()
            return {'exclusive_atomic_publication':True,'final_directory_fsync_completed':True,
                    'pending_removed':True,'post_publication_mutable_guard_performed':False}
        except BaseException as error:
            if attempted:
                raise TerminalPublicationUncertain(path,pending,stage,published,error) from None
            # No final-name dispatch was attempted: only this own pending inode
            # can be removed. Failure here leaves an unissued pending file only.
            try:
                entry=os.stat(pending.name,dir_fd=parent.fd,follow_symlinks=False)
                need((entry.st_dev,entry.st_ino)==pending_identity,'Pending inode changed before cleanup')
                ops.unlink(pending.name,dir_fd=parent.fd);ops.fsync(parent.fd);parent.check()
            except BaseException as cleanup:
                raise RuntimeError('Unpublished pending cleanup/durability uncertain; no final-name publication was attempted; reconcile pending read-only: '+str(pending)) from cleanup
            raise

def terminal_record(rt,config,source_pin,manifest_pin,actual,proof,proof_path,proof_pin,
                    pointer_pin,sync_pin,files,lists,observation,queue,journal,source_checks):
    """Production record constructor; called only after inspect's executed checks.

    Dependency-explicit constructor permits synthetic byte integration through
    the real consumer without publishing or asserting any actual completion.
    """
    h=rt.h
    need(rt.m['phase']=='completion100','Only final100 can construct actual terminal')
    h.merge_identity(rt.m);h.publication_identity(rt.m)
    need(type(source_checks) is int and source_checks>=2,'Executed repeated exact source/gate refreshes required')
    need(actual.get('actual_Root_MCP_CAS_performed') is True
         and actual.get('actual_tool_success_and_readback_accepted') is True
         and actual.get('original_lock_held_across_actual_Root_CAS') is True
         and actual.get('unknown_outcome') is False,'Actual Root CAS and same-live-lock evidence required')
    need(proof.get('full_scope_verified') is True and proof.get('all_selected_native_bodies_verified') is True
         and proof.get('foreign_native_tuples_preserved') is True
         and exact(proof.get('candidate'),rt.admission['candidate']) and exact(proof.get('tree'),rt.admission['tree']),
         'Actual immutable proof result required')
    need(exact(lists['new_memberships'],h.completion_memberships())
         and exact(lists['old_memberships'],h.source_baseline()),'Exact old/new membership evidence')
    for key in ('coherent_before_after_ref',):
        need(observation.get(key) is True,'Actual coherent native closure required')
    for key in ('CAS_or_completion_inferred_from_ancestry','perpetual_or_write_time_Main_equality_claimed'):
        need(observation.get(key) is False,'Qualified observation boundary required')
    need(exact(observation.get('CAS_target'),rt.admission['candidate'])
         and exact(observation.get('CAS_target_tree'),rt.admission['tree'])
         and type(observation.get('selected_postimage_paths_verified')) is int
         and observation['selected_postimage_paths_verified']==len(rt.overlay)
         and type(observation.get('protected_body_paths_verified')) is int
         and observation['protected_body_paths_verified']==len(rt.m['protected_bodies']),
         'Exact observed selected/protected body counts and aliases')
    checks={'refreshes_completed_before_record':source_checks,'terminal_source_pin':source_pin,
        'terminal_source_manifest_pin':manifest_pin,'terminal_source_acceptance':config['source_acceptance'],
        'logical_gate':config['logical_gate'],'admission_acceptance':config['Root_gate'],
        'case_ready_receipt':rt.m['evidence_references']['case_ready'],
        'native_identity_receipt':rt.m['native_identity_receipt'],'transport_policy':transport_policy(config),
        'all_exact_pins_and_gates_rechecked_successfully':True}
    verified=(type(checks['refreshes_completed_before_record']) is int
              and checks['refreshes_completed_before_record']>=2
              and checks['all_exact_pins_and_gates_rechecked_successfully'] is True)
    return {'schema':RECEIPT_SCHEMA,'evidence_scope':'ACTUAL_ROOT_RECEIPT',
        'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':239,'problem_id':'30001321',
        'accepted':True,'completed':True,'phase':'completion100','new_publication_workflow':True,'workflow_percent':100,'completed_eligible_workflow':True,
        'publication_workflow_completed':True,'publication_ready':True,
        'fully_completed_count':56,'published_count':40,'last_completed_PR':239,
        'next_numeric_intake_cursor':240,'advance_to_next_PR_authorized_now':True,'goal_complete':False,
        'numeric_advance_conditional_on_actual_Root_terminal':False,
        'original_eligible_status':'claimed_solved','current_status':'claimed_solved',
        'current_head':h.CURRENT,'original_merge_commit':h.merge_identity(rt.m)['merge_candidate'],'actual_original_PR_merged':True,
        'adopted_existing_publication':False,'no_new_provider_publication_or_tracker_append':False,
        'new_publication_verified':True,'new_tracker_append_verified':True,
        'publication_DOI':h.publication_identity(rt.m)['doi'],'tracker_range':h.publication_identity(rt.m)['range'],
        'publication_record_id':h.publication_identity(rt.m)['record_id'],
        'actual_publication_receipt':rt.m['evidence_references']['publication'],
        'actual_tracker_receipt':rt.m['evidence_references']['tracker'],
        'actual_merge95_receipt':rt.m['evidence_references']['merge'],
        'parent':rt.admission['parent'],'parent_tree':rt.admission['parent_tree'],
        'candidate':rt.admission['candidate'],'tree':rt.admission['tree'],**observation,
        'terminal_source_pin':source_pin,'terminal_source_manifest_pin':manifest_pin,
        'terminal_source_acceptance':config['source_acceptance'],'protocol_pin':DRIVER_PIN,
        'logical_manifest':config['manifest'],'logical_gate':config['logical_gate'],
        'admission':config['admission'],'admission_acceptance':config['Root_gate'],
        'actual_CAS_acceptance':config['actual_CAS'],'transport_policy':transport_policy(config),
        'actual_Root_expected_SHA_force_false_ref_update_and_native_readback':True,
        'actual_CAS_was_separate_Root_operation':True,'this_action_native_POSTs':0,'this_action_ref_or_PR_mutations':0,
        'actual_pointer':config['pointer'],'actual_pointer_pin':pointer_pin,'actual_sync':config['sync'],
        'actual_sync_pin':sync_pin,'actual_Root_terminal_native_journal':str(journal),
        'actual_Root_repeated_immutable_verification':{'path':str(proof_path),**proof_pin},
        'all_five_local_files_match_actual_checkpoint':True,'files':files,
        'old_memberships':lists['old_memberships'],'new_memberships':lists['new_memberships'],
        'fully_completed_eligible_PRs':lists['fully_completed_eligible_PRs'],'published_PRs':lists['published_PRs'],
        'only239_added_to_exact55_39_baseline':True,'dated_eligible_denominator':99,
        'denominator_is_not_current_repository_census':True,'original_stable_writer_lock_held_exact':True,
        'all_selected_native_bodies_verified':True,'full_scope_verified':True,'foreign_native_tuples_preserved':True,
        'source_gates_verified':verified,'source_gate_checks':checks,
        'selected_file_count':len(rt.overlay),'selected_bytes':sum(len(x) for x in rt.overlay.values()),
        'changed_leaf_count':len(proof['changed_leaves']),'new_directory_count':len(proof['new_directories']),
        'deleted_directory_count':0,'whole_phase100_parent_and_candidate_QUEUE_tuple_preserved':rt.m['protected_queue'],
        'actual_R_QUEUE_whole_body_authenticated':True,'own_Main_QUEUE_row_pin':rt.m['protected_queue_row_pin'],
        'R_foreign_QUEUE_rows_may_differ':True,'Main_QUEUE_observation':queue,
        'opaque_attempt_audit_preserved':True,
        'numeric_intake_authority_boundary':'Only this separately executed actual Root terminal authorizes numeric240. Conditional five proposals, sync, ancestry and source gates alone do not.',
        'terminal_observation_boundary':'UTC is preparation time for a dated jointly checked local-five/coherent R/root. Fsynced pending bytes precede the same-state full mutable guard and exclusive final publication; afterwards only file/source/held-lock identity checks run. C and R remain separate. No perpetual/current-at-write-time Main equality, ancestry-derived CAS or distributed atomic transaction is claimed.',
        'publication_order':'pending full-write/file-fsync/directory-fsync; final full mutable guard; exclusive final-name link; file/lock/source identity afterwards',
        'protected_body_count_boundary':'Exact explicit protected body count only; other existing scientific and audit trees are preserved opaquely by mode/type/OID.',
        'native_body_authentication':'Full actual native GET envelopes and origins within this observer invocation; cached bytes rehashed with fresh path/mode/OID associations. No new-network-GET count inferred.'}


def inspect(driver,rt,api,config,refresh_source,journal):
    """Dependency-explicit core; fixtures may test it without production execution."""
    e,h=rt.e,rt.h
    with e.WriterLock(rt.m['writer_lock']) as lock:
        lock.check();source_pin,manifest_pin=refresh_source();rt.refresh();source_checks=1
        actual=driver.actual_cas(rt,config['actual_CAS'],api)
        proof=driver.verify_immutable(rt,api)
        need(proof.get('full_scope_verified') is True and proof.get('all_selected_native_bodies_verified') is True
             and proof.get('foreign_native_tuples_preserved') is True
             and exact(proof.get('candidate'),rt.admission['candidate']) and exact(proof.get('tree'),rt.admission['tree']),
             'Full immutable candidate proof required')
        need(type(proof.get('selected_count')) is int and proof['selected_count']==len(rt.overlay)
             and exact(proof.get('changed_leaves'),sorted(rt.m['expected_changed_paths']))
             and exact(proof.get('new_directories'),sorted(rt.m['expected_new_directories']))
             and exact(proof.get('deleted_directories'),[]),'Complete exact immutable candidate scope/count required')
        e.put(journal,'ROOT_REPEATED_IMMUTABLE_PROOF.json',proof)
        proof_path=journal/'ROOT_REPEATED_IMMUTABLE_PROOF.json';proof_pin=pin(enc(proof))
        need(exact(pin(readonly(proof_path)),proof_pin),'Actual repeated immutable proof write differs')
        pointer_pin,sync_pin,files,lists=pointer_and_posts(driver,rt,config)
        observation=driver.main_closure(rt,api);queue=native_semantics(rt,api,observation)
        def guard():
            nonlocal source_checks
            lock.check();sp,mp=refresh_source();need(exact(sp,source_pin) and exact(mp,manifest_pin),'Terminal source closure changed')
            rt.refresh();source_checks+=1;now=driver.actual_cas(rt,config['actual_CAS'],api)
            need(exact(now,actual),'Actual Root CAS acceptance changed')
            need(exact(pin(readonly(proof_path)),proof_pin),'Actual immutable proof record changed')
            pp,ss,ff,ll=pointer_and_posts(driver,rt,config)
            need(exact((pp,ss,ff,ll),(pointer_pin,sync_pin,files,lists)),'Actual pointer/sync/local facts changed')
            current=driver.main_closure(rt,api);native_semantics(rt,api,current)
            need(current['actual_MAIN_observed']==observation['actual_MAIN_observed']
                 and current['actual_MAIN_tree']==observation['actual_MAIN_tree'],'R moved; explicit new readonly reconciliation required')
            need(api('GET','git/ref/heads/main')['object']['sha']==observation['actual_MAIN_observed'],'Final actual R changed')
            lock.check()
        def identity_guard():
            # No native API, Main equality, pointer or current-five read here.
            # These are immutable source/envelope identities and held lock only.
            lock.check();sp,mp=refresh_source()
            need(exact(sp,source_pin) and exact(mp,manifest_pin),'Terminal source closure changed after publication')
            rt.refresh();raw_ref(config['actual_CAS']);lock.check()
        guard()
        record=terminal_record(rt,config,source_pin,manifest_pin,actual,proof,proof_path,proof_pin,
                               pointer_pin,sync_pin,files,lists,observation,queue,journal,source_checks)
        path=A/config['receipt_name']
        publication=exclusive_root_receipt(e,path,enc(record),guard,identity_guard)
        return {'terminal_receipt':{'path':str(path),**pin(enc(record))},'actual_MAIN_observed':observation['actual_MAIN_observed'],
                'actual_MAIN_tree':observation['actual_MAIN_tree'],'CAS_target':rt.admission['candidate'],
                'fully_completed_count':56,'published_count':40,'last_completed_PR':239,
                'next_numeric_intake_cursor':240,'completed_eligible_workflow':True,
                'publication_ready':True,'goal_complete':False,'publication':publication}

def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
         and sys.flags.safe_path and not sys.flags.optimize,'Use ordinary Python -E -S -B -P without optimization')
    parser=argparse.ArgumentParser(description=__doc__)
    names=('manifest','logical-gate','admission','Root-gate','actual-CAS','pointer','sync','source-acceptance')
    optional=('extension-source','extension-acceptance')
    for name in names+optional:
        parser.add_argument('--'+name,required=name in names)
        parser.add_argument('--'+name+'-bytes',type=int,required=name in names)
        parser.add_argument('--'+name+'-sha256',required=name in names)
    parser.add_argument('--journal',required=True)
    parser.add_argument('--receipt-name',default='ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json')
    args=parser.parse_args();config={}
    for name in names+optional:
        k=name.replace('-','_');path=getattr(args,k);length=getattr(args,k+'_bytes');sha=getattr(args,k+'_sha256')
        need((path is None)==(length is None)==(sha is None),'Every supplied reference needs all three exact fields')
        config[k]=None if path is None else {'path':path,'bytes':length,'sha256':sha}
    config.update(journal=args.journal,receipt_name=args.receipt_name)
    driver,rt,factory,refresh=context(config)
    journal=rt.e.journal_new(config['journal']);api=GetOnly(factory(journal))
    result=inspect(driver,rt,api,config,refresh,journal)
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
