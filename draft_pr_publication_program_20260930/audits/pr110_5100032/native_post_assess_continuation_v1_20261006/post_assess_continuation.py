#!/usr/bin/env python3
"""Future commissioned continuation of one successful existing native assess.

Never calls queue.assess, edits the old workspace, exports to main, or writes
services. The sole validator repair permits native-generated clear_holds:{}.
"""
import sys, os
ENV={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'}
if sys.platform=='darwin':ENV['__CF_USER_TEXT_ENCODING']='0x'+format(os.getuid(),'X')+':0x0:0x0'
if __name__=='__main__' and (dict(os.environ)!=ENV or not(sys.flags.ignore_environment and sys.flags.no_site
        and sys.flags.dont_write_bytecode and getattr(sys.flags,'safe_path',False))):
    raise SystemExit('Physical pinned Python -E -S -B -P and exact clean initial environment required.')
import ast, copy, datetime, hashlib, json, pathlib, resource, shutil, signal, stat, types
A=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr110_5100032')
C=A.parents[2];D=A/'native_post_assess_continuation_v1_20261006'
OLD=A/'native_execution_programs_v1/workspaces/candidate_d9eb646c1dd70e89'
PACKET_SHA='d9eb646c1dd70e891cc44bcaa5de2b62fc0c5a6eabdf2d487a148c3d3cc02281'
MAIN='f9f840d21305bdc353d151abe8dd5c51b6a27dd6'
PROTOCOL_SHA='5111652d104c70aa81880426f449fd4ca1c1c15c5f4847db1acfca5924f67056'
def need(x,m):
    if not x:raise ValueError(m)
def canon(x):return (json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def hp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load_module(name,body,path):
    m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m
    exec(compile(body,str(path),'exec'),m.__dict__);return m
def startup_read(path,cap,spec=None):
    # No local code is imported before unique-link, no-follow full source custody.
    path=pathlib.Path(path);need(path.is_absolute() and '..' not in path.parts,'Canonical absolute input')
    fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
    try:
        for part in path.parent.parts[1:]:
            nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
        child=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=fd)
        try:
            first=os.fstat(child);need(stat.S_ISREG(first.st_mode) and first.st_nlink==1 and first.st_size<=cap,'Bounded unique regular input')
            parts=[];count=0
            while b:=os.read(child,65536):
                count+=len(b);need(count<=cap,'Input grew beyond cap');parts.append(b)
            last=os.fstat(child);need((first.st_dev,first.st_ino,first.st_size,first.st_mtime_ns)==(last.st_dev,last.st_ino,last.st_size,last.st_mtime_ns),'Input drift')
            body=b''.join(parts)
            if spec is not None:need(hp(body)=={k:spec[k] for k in ['bytes','sha256']},'Full source/input pin mismatch')
            return body
        finally:os.close(child)
    finally:os.close(fd)
def audit(spec,cap=8*1024*1024):
    need(set(spec)=={'path','bytes','sha256'},'Exact audit pin')
    rel=pathlib.PurePosixPath(spec['path']);need(not rel.is_absolute() and '..' not in rel.parts and str(rel)==spec['path'],'Nonescaping audit path')
    return startup_read(A/rel,cap,spec)

def corrected_protocol(strict,body,path):
    """All unchanged functions come from the separately loaded immutable source."""
    p=load_module('pr110_continuation_scoped_protocol',body,path)
    def exact_generated_empty_clear_holds(before,after,overlay):
        need('clear_holds' not in before[p.K] and 'clear_holds' not in overlay,
             'This correction applies only to absent baseline/overlay clear_holds')
        need(type(after[p.K].get('clear_holds')) is dict and after[p.K]['clear_holds']=={},
             'Only an exactly empty native-generated clearance map is allowed')
        target={k:v for k,v in after[p.K].items() if k!='clear_holds'}
        # The view is only for validation. Actual output bytes and ledger keep {}.
        strict.validate_assessments(before,{**after,p.K:target},overlay)
    p.validate_assessments=exact_generated_empty_clear_holds
    return p

def original_preconditions(rr,runner_source,packet,w,p,approvals):
    """Re-execute the immutable runner's complete pre-worker input validators.

    Select exactly the contiguous original AST block from its `expected` packet
    key set through inputs.finish(), before caps/workspace creation. This avoids
    duplicating or weakening any source/service/cache/offer guard and cannot
    select the native-assess launch. Original actual gate chronology stays
    historical; the separate new root commission controls this continuation.
    """
    tree=ast.parse(runner_source)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='execute')
    def assignment(n,name):return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)
    starts=[i for i,n in enumerate(fn.body) if assignment(n,'expected')]
    ends=[i for i,n in enumerate(fn.body) if assignment(n,'caps')]
    need(len(starts)==len(ends)==1 and starts[0]<ends[0],'Exact immutable pre-worker validator block')
    args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=x) for x in ['packet','w','p','approvals']],
        vararg=None,kwonlyargs=[],kw_defaults=[],kwarg=None,defaults=[])
    result=['offer_bodies','original','doi','selected','package_bytes','cache','overlay','note','parent_limits']
    new=ast.FunctionDef(name='_continuation_original_preconditions',args=args,
        body=copy.deepcopy(fn.body[starts[0]:ends[0]])+[ast.Return(value=ast.Tuple(elts=[ast.Name(id=x,ctx=ast.Load()) for x in result],ctx=ast.Load()))],
        decorator_list=[],returns=None,type_comment=None,type_params=[])
    mod=ast.fix_missing_locations(ast.Module(body=[new],type_ignores=[]))
    exec(compile(mod,rr.__file__+'::immutable_pre_worker_block','exec'),rr.__dict__)
    return rr._continuation_original_preconditions(packet,w,p,approvals)

def verify_seed(a,seed):
    need(seed['schema']=='pr110-failed-successful-worker-seed-inventory/v1' and seed['source_workspace']==str(OLD)
         and seed['original_packet_sha256']==PACKET_SHA and seed['successful_existing_worker_PID']==23360
         and seed['preserved_failed_operator_PID']==23224 and seed['file_count']==61,'Exact successful-worker failed seed')
    names=set();total=0
    for spec in seed['files']:
        rel=a.relpath(spec['path']);need(spec['path'] not in names,'Duplicate seed member');names.add(spec['path'])
        measured=a.read(OLD/rel,32*1024*1024,spec,retain=False);total+=measured['bytes']
    found=set()
    def walk(root):
        for entry in os.scandir(root):
            info=entry.stat(follow_symlinks=False);path=pathlib.Path(entry.path)
            if stat.S_ISDIR(info.st_mode):walk(path)
            else:
                need(stat.S_ISREG(info.st_mode) and info.st_nlink==1,'Unsafe seed member')
                found.add(str(path.relative_to(OLD)));need(len(found)<=61,'Unexpected seed additions')
    fd=a.dirfd(OLD);os.close(fd);walk(OLD)
    need(found==names and total==seed['total_bytes'],'Whole old workspace inventory preserved')
    return {spec['path']:spec for spec in seed['files']}

def main():
    need(len(sys.argv)==2,'One fresh absolute root continuation commission required')
    gate_path=pathlib.Path(sys.argv[1]);need(gate_path.is_relative_to(A),'Gate belongs to effort')
    raw=startup_read(gate_path,512*1024);g=json.loads(raw)
    need(raw==canon(g) and g['schema']=='pr110-post-assess-continuation-commission/v1' and g['role']=='root'
         and g['actual_review'] is True and g['clearance'] is True and g['required_findings']==[]
         and all(g[k] is False for k in ['template_only','fixture','simulated']),'Actual root continuation commission')
    need(datetime.timedelta(0)<=datetime.datetime.fromisoformat(now())-datetime.datetime.fromisoformat(g['UTC'])<=datetime.timedelta(minutes=30),'Fresh continuation commission')
    need(g['successful_existing_worker_and_failure_independently_authenticated'] is True and
         g['narrow_empty_clear_holds_only'] is True and g['no_reassessment_authorized'] is True,'Root actual narrow continuation decision')
    need(A/pathlib.PurePosixPath(g['program_pin']['path'])==pathlib.Path(__file__) and audit(g['program_pin'],128*1024)==startup_read(__file__,128*1024),'Exact executing continuation source')
    phase_body=audit(g['action_program_pin'],128*1024)
    need(A/pathlib.PurePosixPath(g['action_program_pin']['path'])==D/'native_acceptance_actions_v2.py','Fixed reviewed phase v2 source')
    a=load_module('pr110_continued_phase_actions',phase_body,D/'native_acceptance_actions_v2.py')
    ad_body=audit(g['adversary_pin']);ad=a.loads(ad_body)
    need(ad['schema']=='pr110-post-assess-continuation-adversary/v1' and ad['actual_review'] is True and
         ad['clearance'] is True and ad['required_findings']==[] and ad['template_only'] is False
         and ad.get('fixture',False) is False and ad.get('simulated',False) is False
         and ad['program_pin']==g['program_pin'] and ad['action_program_pin']==g['action_program_pin']
         and ad['packet_sha256']==PACKET_SHA and ad['seed_inventory_pin']==g['seed_inventory_pin']
         and a.timestamp(ad['UTC'])<=a.timestamp(g['UTC']),'Fresh exact-source/seed continuation adversary')
    packet_raw=audit(g['packet_pin']);need(hp(packet_raw)['sha256']==PACKET_SHA,'Immutable original actual packet')
    packet=a.loads(packet_raw);need(packet['main_parent']==MAIN,'Original actual main parent')
    family={name:audit(spec,128*1024) for name,spec in packet['program_files'].items()}
    need(hp(family['protocol.py'])['sha256']==PROTOCOL_SHA,'Unchanged immutable pure protocol')
    w=load_module('pr110_continuation_worker_helpers',family['native_worker.py'],A/'native_execution_programs_v1/native_worker.py')
    rr=load_module('pr110_continuation_runner_helpers',family['native_runner.py'],A/'native_execution_programs_v1/native_runner.py')
    strict=load_module('pr110_continuation_strict_protocol',family['protocol.py'],A/'native_execution_programs_v1/protocol.py')
    p=corrected_protocol(strict,family['protocol.py'],A/'native_execution_programs_v1/protocol.py')
    seed=a.loads(audit(g['seed_inventory_pin']));seedpins=verify_seed(a,seed)
    need(a.read(OLD/'EXECUTION_INPUTS.json')==packet_raw,'Seed original packet byte equality')
    auth_body=audit(g['failed_run_root_authentication_pin']);auth=a.loads(auth_body)
    need(auth['schema']=='pr110-root-failed-native-run-authentication/v1' and auth['packet_sha256']==PACKET_SHA
         and auth['actual_worker_PID']==23360 and auth['actual_runner_PID']==23224
         and all(auth[k] is True for k in ['actual_assess_once_success_authenticated','all12_actual_output_fullbodies_authenticated',
             'all17_children_reaped_and_groups_absent','all26_ancestry_full_raw_streams_authenticated',
             'safe_scope_stop_authenticated','target_delta_only_reviewed_at_and_empty_clear_holds','narrow_correction_pure_scope_replay_passed'])
         and auth['native_export_executed'] is False,'Root actual failed-run custody prerequisite')
    for spec in auth['checked_artifacts']:audit(spec)
    fail=a.loads(a.read(OLD/'FAILURE.json',65536,seedpins['FAILURE.json']))
    need(fail['operator_PID']==23224 and fail['packet_sha256']==PACKET_SHA and fail['error_type']=='ValueError'
         and fail['error']=='Target assessment changed beyond reviewed metadata' and fail['candidate_must_not_be_exported'] is True,'Preserved exact scope failure')
    approvals={}
    for role,name in [('root','ROOT_COMMISSION.json'),('adversary','PREEXEC_ADVERSARY.json')]:
        b=a.read(OLD/name,128*1024,seedpins[name]);v=a.loads(b)
        need(v['schema']=='pr110-concrete-native-commission/v1' and v['role']==role and v['actual_review'] is True
             and v['clearance'] is True and v['packet_sha256']==PACKET_SHA and v['main_parent']==MAIN
             and v['program_hashes']=={n:hp(bd)['sha256'] for n,bd in family.items()},'Actual historical commissioning source correspondence')
        approvals[role]=(v,b)
    need(approvals['root'][0]['adversary_sha256']==hp(approvals['adversary'][1])['sha256'],'Historical root/adversary full body binding')
    offers,original,doi,selected,package_bytes,cache,overlay,note,parent_limits=original_preconditions(rr,family['native_runner.py'],packet,w,p,approvals)
    need(doi==a.DOI and selected==a.RANGE,'Original actual publication/tracker retained')
    control_raw=a.read(OLD/'WORKER_CONTROL.json',512*1024,seedpins['WORKER_CONTROL.json']);control=a.loads(control_raw)
    result_raw=a.read(OLD/'WORKER_RESULT.json',128*1024,seedpins['WORKER_RESULT.json']);result=a.loads(result_raw)
    journal=a.loads(a.read(OLD/'PROCESS_JOURNAL.json',128*1024,seedpins['PROCESS_JOURNAL.json']))
    processes=journal['processes'];matches=[x for x in processes if x['PID']==23360]
    need(len(processes)==17 and len(matches)==1 and journal['operator_PID']==23224,'Actual unique existing worker process')
    process=matches[0]
    expected_argv=[packet['runtime']['binaries']['python']['resolved_absolute_path'],'-E','-S','-B','-P',str(OLD/'native_worker.py'),'--control',str(OLD/'WORKER_CONTROL.json')]
    need(process['argv']==expected_argv and process['cwd']==str(OLD) and process['environment_sha256']==hp(canon(ENV))['sha256']
         and process['exit_code']==0 and process['reaped'] is True and process['process_group_absence_confirmed'] is True
         and process['termination_reason'] is None and process['streams_fully_drained'] is True,'Actual old successful child custody')
    for k,s in process['streams'].items():
        b=a.read(OLD/s['retained_path'],4096)
        need(hp(b)=={'bytes':s['bytes'],'sha256':s['sha256']} and len(b)==s['observed_bytes']
             and hp(b)['sha256']==s['observed_sha256'],'Existing worker full actual raw streams')
    need(result['actual_worker_PID']==23360 and result['outcome']=='success' and result['native_assess_call_attempted'] is True
         and result['native_assess_completed'] is True and result['packet_sha256']==PACKET_SHA
         and result['control_sha256']==hp(control_raw)['sha256'] and rr.same(result['validated_control'],control),'Actual old successful control/result correspondence')
    need(result['startup']=={'PID':23360,'argv':[str(OLD/'native_worker.py'),'--control',str(OLD/'WORKER_CONTROL.json')],
         'cwd':str(OLD),'environment_sha256':process['environment_sha256'],'Python_ignore_environment':True,
         'Python_no_site':True,'Python_no_bytecode':True,'Python_safe_path':True},'Actual old worker exact startup correspondence')
    need(control['schema']=='pr110-native-worker-control/v1' and control['fixture'] is False and control['packet_sha256']==PACKET_SHA
         and control['backend']==str(OLD/'private_native_backend') and control['resources']==packet['resources']
         and control['caps']==w.derive_caps(packet['native_baseline'],packet['resources'])
         and control['SQL_cache']==cache['absolute_path'] and control['SQL_pin']==cache['pin']
         and control['revision']==p.REV and control['record_count']==15458,'Actual old control source/cache/resource graph')
    need(result['limits']['requested']==packet['resources'] and result['limits']['enforced']=={
         'RLIMIT_CPU':[packet['resources']['cpu_seconds']]*2,'RLIMIT_FSIZE':[packet['resources']['file_size_bytes']]*2,
         'RLIMIT_NOFILE':[packet['resources']['open_files']]*2} and result['limits']['memory']['hard_memory_limit_claimed'] is False,'Actual applied worker resource readbacks')
    need(p.stamp(process['UTC_start'])<=p.stamp(result['UTC_start'])<=p.stamp(result['UTC_end'])<=p.stamp(process['UTC_end'])<=p.stamp(fail['UTC']),'Successful worker precedes actual scope failure')
    after={n:a.read(OLD/'private_native_backend'/n,32*1024*1024,result['output_pins'][n]) for n in p.NATIVE}
    need(set(result['output_pins'])==set(p.NATIVE),'Full exact actual twelve-output map')
    # Only now create a new candidate; the source workspace is never written.
    workspace=D/'workspaces'/('candidate_'+PACKET_SHA[:16]);cap=a.Capture(workspace,whole_seconds=packet['parent_policy']['deadline_seconds'])
    fd=a.dirfd(workspace);os.fchmod(fd,0o700);os.close(fd)
    def terminated(sig,frame):
        if a.SPAWN_CRITICAL:a.PENDING_SIGNAL=sig;return
        raise SystemExit('Actual continuation '+signal.Signals(sig).name)
    signal.signal(signal.SIGTERM,terminated);signal.signal(signal.SIGINT,terminated)
    def watch():
        count=0;size=0
        for path in workspace.rglob('*'):
            st=path.lstat();need(stat.S_ISDIR(st.st_mode) or (stat.S_ISREG(st.st_mode) and st.st_nlink==1),'Safe continuation outputs')
            if stat.S_ISREG(st.st_mode):count+=1;size+=st.st_size;need(st.st_size<=packet['resources']['file_size_bytes'],'Per-file native cap')
        need(count<=packet['parent_policy']['file_count_cap'] and size<=packet['parent_policy']['allocation_cap'],'Continuation file/allocation cap')
        reserve=sum(packet['parent_policy'][x] for x in ['headroom_bytes','commit_reserve_bytes','runtime_reserve_bytes'])
        free=shutil.disk_usage(D).free;need(free>=reserve,'Continuation actual space/reserves')
        return {'files':count,'bytes':size,'free_bytes':free}
    try:
        a.save(workspace/'START.json',{'UTC':now(),'actual_continuation_PID':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),
            'environment_sha256':hp(canon(ENV))['sha256'],'program_pin':g['program_pin'],'root_gate_pin':hp(raw),
            'seed_inventory_pin':g['seed_inventory_pin'],'existing_worker_PID':23360,'reassessment_executed':False})
        a.main_preflight(cap,packet['runtime'],MAIN);a.live_pr(cap,packet['runtime'],draft=True)
        need(not os.path.lexists(C/a.PREFIX),'Live target still absent')
        before={}
        for name,spec in packet['native_baseline'].items():
            b=a.git(cap,packet['runtime'],'show',MAIN+':'+spec['path']);need(hp(b)=={k:spec[k] for k in ['bytes','sha256']},'Actual full native preimage pin');before[name]=b
            if os.path.lexists(C/spec['path']):a.read(C/spec['path'],spec=spec,retain=False)
            watch()
        event=p.imported_baseline(packet['import_UTC'],p.ORIGINAL_ROW_SHA,p.ORIGINAL_LOG_SHA)
        pre_assess=dict(before)
        pre_assess['state.json']=(json.dumps({**p.loads(before['state.json']),p.K:event},ensure_ascii=False,indent=2)+'\n').encode()
        pre_assess['history.jsonl']=before['history.jsonl']+json.dumps(event,ensure_ascii=False).encode()+b'\n'
        pre_assess['assessment.json']=canon({**p.loads(before['assessments.json'])[p.K],**overlay})
        need(control['pre_assess_pins']=={n:hp(b) for n,b in pre_assess.items()},'Independently reconstructed exact thirteen pre-assess pins')
        a.read(OLD/'private_native_backend/assessment.json',65536,control['pre_assess_pins']['assessment.json'],retain=False)
        # Reuse unchanged ledger, catalog, CSV, campaign, summary and effort guards.
        scoped,drift=p.scoped_outputs(before,after,overlay,event,note,doi)
        need({n:hp(b) for n,b in scoped.items()}==auth['proposed_derived_pins'],'Independent continuation agrees with root pure replay')
        scoped=rr.format_scoped_json(before,scoped,p)
        generated={'IMPORT_BASELINE.json':canon(event),'HISTORICAL_DESK_ASSESSMENT.json':canon(p.loads(before['assessments.json'])[p.K]),
          'assessment.json':canon(p.loads(after['assessments.json'])[p.K]),
          'PUBLICATION_EVIDENCE.json':canon({'schema':'pr110-published-native-candidate-evidence/v1','original_head':p.HEAD,'review_hash':p.REVIEW,
              'statement_hash':p.STATEMENT,'DOI':doi,'Sheet_range':selected,'package_manifest_sha256':hp(package_bytes)['sha256'],
              'packet_sha256':PACKET_SHA,'original_budget':'2/5','new_central_proof_search_turns':0,'prior_report_pin':p.PRIOR_PIN,'literal_native_status':'claimed_solved'}),
          'ACCEPTANCE_EVIDENCE.json':canon({'schema':'pr110-reviewed-full-resolution-native-continuation-candidate/v1',
              'accepted_mathematical_full_resolution':True,'actual_Zenodo_and_GWS_independently_authenticated_by_root':True,
              'native_status':'claimed_solved','turns_used':2,'original_structured_ledger_present':False,'packet_sha256':PACKET_SHA,
              'successful_existing_worker_PID':23360,'actual_continuation_PID':os.getpid(),'native_assess_calls_during_continuation':0,
              'empty_clear_holds_generated_metadata_only':True,'holds_cleared':False,'candidate_only':True,
              'live_native_acceptance_executed':False,'native_export_executed':False,'fresh_candidate_review_required':True}),
          'README.md':('# 5100032 focal antipedal equality\n\nLiteral original claimed_solved2/5; all17 original bodies and the nonempty prior preserved. '
              'One dated import does not recreate historical structured events. No additional proof-search turn. '
              'A successful existing native assess (worker23360) is continued after a guard omitted native-generated clear_holds:{}; '
              'the map is empty, supplies no clearance evidence and clears no hold. No reassessment. The failed workspace remains intact and nonexportable. '
              'This new candidate awaits independent review and actual export. Published proof: https://doi.org/'+doi+'\n').encode(),
          'RESEARCH_LOG.md':('# PR110 native continuation log\n\n'+now()+': Private native candidate95%, actual workflow80%. '
              'Reused successful worker23360 output; corrected only empty native-generated clear_holds metadata; retained failed workspace and all remaining immutable guards. '
              'No reassessment, extra proof turn, hold clearance or live acceptance/export.\n').encode()}
        alloffers={**offers,**{'unsolved_math_prioritization/'+n:b for n,b in scoped.items()},**{a.PREFIX+n:b for n,b in generated.items()}}
        need(all(a.PREFIX+n not in offers for n in generated),'No source/generated offer collision')
        size=sum(len(b) for b in alloffers.values());need(size+2*1024*1024<=packet['parent_policy']['allocation_cap'],'Exact continuation offer allocation')
        need(shutil.disk_usage(D).free>=size+sum(packet['parent_policy'][x] for x in ['headroom_bytes','commit_reserve_bytes','runtime_reserve_bytes']),'Full offer and reserves before copying')
        affected=[]
        for name,b in alloffers.items():
            a.atomic(workspace/'offer'/name,b);a.read(workspace/'offer'/name,spec=hp(b),retain=False)
            old=before.get(name.split('/',1)[1]) if name in a.DERIVED else None
            affected.append({'path':name,'before':None if old is None else hp(old),'after':hp(b)});watch()
        diff=rr.full_diff(before,alloffers,a.PREFIX);a.atomic(workspace/'DIFF.txt',diff)
        a.main_preflight(cap,packet['runtime'],MAIN);a.live_pr(cap,packet['runtime'],draft=True)
        rr.validate_runtime(packet['runtime'],w,p)
        w.check_cache(cache['absolute_path'],cache['pin'],p.REV,15458,original['source_record.json'],original['prior_imported_report.json'])
        for name,spec in packet['raw_source_pins'].items():w.read_file('/Users/alec/Documents/Math/unsolved_math_prioritization/cache/'+name,128*1024*1024,spec,retain=False)
        for spec in packet['input_files']:audit(spec)
        for spec in packet['native_baseline'].values():
            if os.path.lexists(C/spec['path']):a.read(C/spec['path'],spec=spec,retain=False)
        verify_seed(a,seed);need(len(cap.records)<=packet['parent_policy']['max_processes'],'Original actual process count cap')
        usage=resource.getrusage(resource.RUSAGE_SELF)
        receipt={'schema':'pr110-actual-post-assess-continuation-candidate/v1','UTC':now(),'operator_PID':os.getpid(),
            'packet_sha256':PACKET_SHA,'main_parent':MAIN,'original_head':p.HEAD,'native_assess_actual_PID':23360,
            'successful_existing_worker_PID':23360,'failed_original_operator_PID':23224,'actual_continuation_PID':os.getpid(),
            'native_status':'claimed_solved','turns_used':2,'new_central_proof_search_turns':0,'nonempty_prior_preserved':True,
            'source_workspace':str(OLD),'seed_inventory_pin':g['seed_inventory_pin'],'source_failure_pin':hp(a.read(OLD/'FAILURE.json')),
            'source_worker_result_pin':hp(result_raw),'failed_run_root_authentication_pin':g['failed_run_root_authentication_pin'],
            'continuation_program_pin':g['program_pin'],'continuation_action_program_pin':g['action_program_pin'],
            'native_assess_calls_during_continuation':0,'empty_clear_holds_generated_metadata_only':True,'holds_cleared':False,
            'original_failure_preserved':True,'unrelated_projection_drift_restored':drift,'affected_paths':affected,'DIFF_pin':hp(diff),
            'capacity_before_final_receipt':watch(),'parent_limits':parent_limits,'original_worker_resource_usage':result['resource_usage'],
            'continuation_resource_usage':{'user_CPU_seconds':usage.ru_utime,'system_CPU_seconds':usage.ru_stime,
                'maximum_RSS':usage.ru_maxrss,'maximum_RSS_units':'bytes' if sys.platform=='darwin' else 'kilobytes','hard_memory_limit_claimed':False},
            'native_export_executed':False,'Git_mutations':0,'service_writes':0,'fresh_candidate_adversary_and_root_review_required':True}
        a.atomic(workspace/'CANDIDATE_RECEIPT.json',canon(receipt));watch()
        print(json.dumps({'candidate':str(workspace),'packet_sha256':PACKET_SHA,'actual_continuation_PID':os.getpid(),
            'successful_existing_worker_PID':23360,'native_assess_calls_during_continuation':0,'affected_paths':len(affected),'native_export_executed':False}))
    except BaseException as e:
        a.save(workspace/'FAILURE.json',{'schema':'pr110-actual-continuation-failure/v1','UTC':now(),'operator_PID':os.getpid(),
            'error_type':type(e).__name__,'error':str(e)[:800],'original_failure_preserved':True,'source_workspace':str(OLD),
            'reassessment_executed':False,'native_export_executed':False,'candidate_must_not_be_exported':True})
        raise
if __name__=='__main__':main()
