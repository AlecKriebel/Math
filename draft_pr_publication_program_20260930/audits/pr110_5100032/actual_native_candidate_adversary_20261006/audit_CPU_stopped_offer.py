#!/usr/bin/env python3
"""Independent full raw custody of kernel-stopped private offer; no approval/process launches."""
import pathlib,types,os,json,datetime,stat
W=pathlib.Path(__file__).resolve().parent
v=types.ModuleType('continued_custody_verification');v.__file__=str(W/'verify_actual_candidate.py')
exec(compile(pathlib.Path(v.__file__).read_bytes(),v.__file__,'exec'),v.__dict__)
def main():
    began=v.now();p=v.obj(v.regular(v.PACKET));D=v.A/'native_post_assess_carryforward_v2_20261006';candidate=D/'workspaces'/('candidate_'+v.PACKET_SHA[:16]);old=v.A/'native_execution_programs_v1/workspaces'/('candidate_'+v.PACKET_SHA[:16]);outerdir=v.A/'actual_operations/root_actual_post_assess_carryforward_20261006'
    start=v.obj(v.regular(candidate/'START.json'));outer=v.obj(v.regular(outerdir/'execution.json'));launch=v.obj(v.regular(outerdir/'LAUNCH.json'));gate_b=v.regular(D/'ROOT_CARRYFORWARD_GATE.json');g=v.obj(gate_b)
    v.check(not any((candidate/x).exists() for x in ['CANDIDATE_RECEIPT.json','DIFF.txt','FAILURE.json']), 'Kernel-stopped attempt has no approval/DIFF/synthetic FAILURE')
    # Local expected contract facts below are gate/start fields, never a fabricated candidate receipt.
    r={'integration_inputs_pin':g['integration_inputs_pin'],'original_assessed_main_parent':p['main_parent'],'main_parent':'e0a94b93520610553c001f265f210f959b591c2c','stopped_continuation_inventory_pin':g['stopped_continuation_inventory_pin'],'operator_PID':59213,'actual_continuation_PID':59213,'native_assess_actual_PID':23360,'successful_existing_worker_PID':23360,'failed_original_operator_PID':23224,'UTC':outer['UTC_end']}
    v.check(outer['schema']=='pr110-actual-bounded-native-carryforward-launch/v1' and outer['action']=='continuation' and outer['actual_continuation_custody_path']==str(candidate) and outer['packet_sha256']==v.PACKET_SHA,'Actual new continuation outer target')
    v.check(outer['config_pin']==v.pin(gate_b) and start['root_gate_pin']==v.pin(gate_b) and gate_b==v.canon(g),'Actual full canonical startup root gate')
    for k in ['program_pin','action_program_pin','packet_pin','adversary_pin','seed_inventory_pin','failed_run_root_authentication_pin','outer_launcher_pin','root_preexecution_review_pin','integration_inputs_pin','stopped_continuation_inventory_pin']:v.audit(g[k])
    v.check(g['schema']=='pr110-post-assess-carryforward-commission/v1' and g['actual_review'] is True and g['clearance'] is True and g['required_findings']==[] and all(g[k] is False for k in ['template_only','fixture','simulated']),'Genuine actual root authorization without fixture/template')
    ad=v.obj(v.audit(g['adversary_pin']));v.check(ad['program_pin']==g['program_pin'] and ad['action_program_pin']==g['action_program_pin'] and ad['outer_launcher_pin']==g['outer_launcher_pin'] and ad['seed_inventory_pin']==g['seed_inventory_pin'] and ad['packet_sha256']==v.PACKET_SHA and ad['clearance'] is True and ad['future_candidate_approved'] is False,'Actual independent narrow preexecution review precedes output review')
    v.check(v.stamp(ad['UTC'])<=v.stamp(g['UTC'])<=v.stamp(outer['UTC_start']) and v.stamp(outer['UTC_start'])-v.stamp(g['UTC'])<datetime.timedelta(minutes=30),'Fresh separate actual authorization chronology')
    integration=v.obj(v.audit(g['integration_inputs_pin']));v.check(r['integration_inputs_pin']==ad['integration_inputs_pin']==g['integration_inputs_pin'] and r['original_assessed_main_parent']==p['main_parent'] and r['main_parent']==integration['main_parent'],'Actual current/history baseline distinction')
    v.check(r['stopped_continuation_inventory_pin']==g['stopped_continuation_inventory_pin'],'Actual second stop inventory binding')
    p={**p,'main_parent':integration['main_parent'],'native_baseline':integration['native_baseline']}
    env=p['runtime']['python_environment'];argv=['/usr/bin/env','-i']+[k+'='+env[k] for k in ['PATH','LC_ALL','LANG','TZ']]
    if '__CF_USER_TEXT_ENCODING' in env:argv+=['__CF_USER_TEXT_ENCODING='+env['__CF_USER_TEXT_ENCODING']]
    argv+=[p['runtime']['binaries']['python']['resolved_absolute_path'],'-E','-S','-B','-P',str(D/'post_assess_carryforward.py'),str(D/'ROOT_CARRYFORWARD_GATE.json')]
    v.check(outer['argv']==argv and outer['cwd']==str(v.C) and outer['environment_sha256']==v.sha(v.canon(env)),'Exact actual initial physical Python -ESBP argv/cwd/clean environment')
    v.check(start['argv']==argv[-2:] and start['cwd']==str(v.C) and start['environment_sha256']==outer['environment_sha256'] and start['program_pin']==g['program_pin'],'Actual continuation start corresponds to observed outer launch')
    v.check(outer['child_PID']==r['operator_PID']==r['actual_continuation_PID']==start['actual_continuation_PID'] and r['native_assess_actual_PID']==r['successful_existing_worker_PID']==23360 and r['failed_original_operator_PID']==23224 and start['existing_worker_PID']==23360 and start['reassessment_executed'] is False,'Actual new operator distinguished from old worker and failed old operator')
    v.check(all(launch[k]==outer[k] for k in launch),'Actual durable pre-wait outer launch fields')
    v.check(outer['exit_code']==-24 and outer['reaped'] is True and outer['termination_reason'] is None and outer['pending_actual_signal'] is None and outer['streams_fully_drained'] is True and outer['all_recorded_groups_absence_confirmed'] is True and outer['cleanup_errors']==[],'SIGXCPU-stopped bounded outer full streams/reap/group custody')
    v.check(outer['whole_launch_deadline_seconds']==300 and outer['elapsed_monotonic_seconds']<300 and outer['kernel_SIGKILL_before_child_registration_complete_containment_claimed'] is False,'Actual wall limit and honest containment boundary')
    v.check(outer['outer_source_pin']=={k:g['outer_launcher_pin'][k] for k in ['bytes','sha256']} and outer['outer_source_pin']==v.pin(v.regular(v.A/'publication_build_v1/record_native_carryforward.py')),'Actual exact reviewed outer source')
    for stream in ['stdout','stderr']:
        s=outer[stream];b=v.regular(outerdir/s['path'],s);v.check(v.pin(b)=={'bytes':s['observed_bytes'],'sha256':s['observed_sha256']} and s['body_custody']=='full_actual_raw_CLI_stream','Full real outer raw stream')
        v.check(b==b'', 'Both full stopped raw operator streams empty; no fabricated success')
    ancestry_bytes=0;ps_pids=set();observed_descendants=set()
    for i,q in enumerate(outer['actual_ancestry_probes']):
        rb=v.regular(outerdir/'ancestry'/(str(i)+'.execution.json'));rq=v.obj(rb);ancestry_bytes+=len(rb);v.check(all(q[k]==rq[k] for k in rq),'Actual ancestry raw receipt corresponds to outer')
        v.check(q['argv']==['/bin/ps','-axo','pid=,ppid=,pgid='] and q['cwd']==str(v.C) and q['environment_sha256']==v.sha(v.canon(env)) and q['exit_code']==0 and q['reaped'] is True and q['termination_reason'] is None and q['streams_fully_drained'] is True,'Actual successful clean bounded ps probe')
        v.check(q['ps_executable_pin']==outer['ps_executable_pin'] and v.stamp(q['UTC_end'])-v.stamp(q['UTC_start'])<datetime.timedelta(seconds=4),'Actual ps byte pin and bounded probe duration')
        ps_pids.add(q['actual_PID'])
        for stream in ['stdout','stderr']:
            s=q[stream];body=v.regular(outerdir/s['path'],s);ancestry_bytes+=len(body);v.check(s['full_raw_body'] is True and v.pin(body)=={'bytes':s['observed_bytes'],'sha256':s['observed_sha256']},'Actual full raw ancestry stream')
            if stream=='stderr':v.check(body==b'','Actual ps stderr empty')
        rows=[tuple(map(int,line.split())) for line in v.regular(outerdir/q['stdout']['path']).splitlines() if line.strip()];known={outer['child_PID']};again=True
        while again:
            again=False
            for pid,ppid,pgid in rows:
                if ppid in known and pid not in known:known.add(pid);again=True
        v.check(sorted(known-{outer['child_PID']})==q['descendant_PIDs'],'Independent actual observed ancestry calculation');observed_descendants.update(known-{outer['child_PID']})
    v.check(len(ps_pids)==len(outer['actual_ancestry_probes'])<=160 and ancestry_bytes==outer['ancestry_retained_total_bytes']<=16*1024*1024,'Actual ancestry process uniqueness/count/aggregate accounting')
    journal=v.obj(v.regular(candidate/'PROCESS_JOURNAL.json'));starts=v.obj(v.regular(candidate/'PROCESS_LAUNCHES.json'));records=journal['records'];v.check(journal['actual_operator_PID']==starts['actual_operator_PID']==r['operator_PID'] and len(records)==len(starts['launches'])==21,'All21 actual new completed child journals and launch records')
    pids={q['actual_PID'] for q in records};v.check(len(pids)==21 and pids<=set(outer['recorded_PGIDs']) and pids.isdisjoint({23224,23360}) and ps_pids<=set(outer['recorded_PGIDs']),'Distinct actual new direct children registered in outer')
    rt=p['runtime'];gb=[rt['binaries']['git']['resolved_absolute_path'],'-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-c','credential.helper=','-c','commit.gpgsign=false','-c','gc.auto=0'];ge={**env,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_SYSTEM':'/dev/null','GIT_OPTIONAL_LOCKS':'0','GIT_NO_REPLACE_OBJECTS':'1','GIT_TERMINAL_PROMPT':'0'};he={**env,'GH_CONFIG_DIR':rt['gh_config_directory'],'GH_HOST':'github.com','GH_PROMPT_DISABLED':'1','GH_PAGER':'','GH_BROWSER':'/usr/bin/false','GH_EDITOR':'/usr/bin/false','GH_NO_UPDATE_NOTIFIER':'1'}
    def preflights():return [(gb+['symbolic-ref','--short','HEAD'],ge,b'main\n'),(gb+['rev-parse','HEAD'],ge,(p['main_parent']+'\n').encode()),(gb+['ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main'],ge,(p['main_parent']+'\trefs/heads/main\n').encode()),(gb+['diff','--cached','--name-only','-z'],ge,b''),(gb+['write-tree'],ge,None),(gb+['rev-parse','HEAD^{tree}'],ge,None),([rt['binaries']['gh']['resolved_absolute_path'],'pr','view','https://github.com/AlecKriebel/Math/pull/110','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body,mergeCommit,mergedAt,url'],he,None)]
    contracts=preflights()+[(gb+['show',p['main_parent']+':'+s['path']],ge,None) for s in p['native_baseline'].values()]+[(gb+['diff','--name-status','--no-renames','-z',r['original_assessed_main_parent'],p['main_parent']],ge,v.audit(integration['Git_delta_pin'])),(gb+['show',r['original_assessed_main_parent']+':unsolved_math_prioritization/QUEUE.md'],ge,v.audit(integration['original_QUEUE_pin']))];tree_outputs=[];PR_outputs=[]
    for i,(q,s,(expected,childenv,known)) in enumerate(zip(records,starts['launches'],contracts)):
        v.check(q['argv']==expected and q['cwd']==str(v.C) and q['environment_sha256']==v.sha(v.canon(childenv)),'Each actual child exact readonly contract')
        v.check(q['exit_code']==0 and q['reaped'] is True and q['process_group_absence_confirmed'] is True and q['fully_drained'] is True and q['termination_reason'] is None and q['error'] is None,'Each actual child successful full capture/reap/group absence')
        v.check(all(s[k]==q[k] for k in ['argv','cwd','environment_sha256','UTC_start']) and s['PID']==q['actual_PID'] and s['state']=='reaped','Actual before-wait durable registration matches real child')
        v.check(v.stamp(outer['UTC_start'])<=v.stamp(start['UTC'])<=v.stamp(q['UTC_start'])<=v.stamp(q['UTC_end'])<=v.stamp(r['UTC'])<=v.stamp(outer['UTC_end']),'Complete actual operator/child/receipt chronology')
        for kind in ['stdout','stderr']:
            x=q['streams'][kind];body=v.regular(candidate/x['retained_file'],x['retained']);observed=x['observed']
            if kind=='stderr':v.check(body==b'' and observed==v.pin(b'') and x['full'] is True,'Actual direct child stderr empty/full')
            elif i==20:
                spec=integration['original_QUEUE_pin'];v.check(observed=={k:spec[k] for k in ['bytes','sha256']} and x['complete_body_retained_in_immutable_Git']==r['original_assessed_main_parent']+':unsolved_math_prioritization/QUEUE.md' and body==v.audit(spec)[:4096],'Actual full observed historical Queue body and honest prefix')
            elif 7<=i<19:
                name=list(p['native_baseline'])[i-7];baseline=p['native_baseline'][name];v.check(observed=={k:baseline[k] for k in ['bytes','sha256']} and x['complete_body_retained_in_immutable_Git']==p['main_parent']+':'+baseline['path'] and len(body)==min(observed['bytes'],4096),'Actual full Git baseline stream hash/count with honestly labelled prefix')
            else:
                v.check(x['full'] is True and observed==v.pin(body),'Full dynamic actual response retained')
                if known is not None:v.check(body==known,'Actual dynamic response equals reviewed expected value')
                if i in [4,5,25,26]:tree_outputs.append(body)
                if i in [6,27]:
                    pr=v.obj(body);v.check(pr['number']==110 and pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==v.HEAD and pr['headRefName']=='dot/math-5100032' and pr['baseRefName']=='main','Actual original draft PR identity readback');PR_outputs.append(pr)
    v.check(len(tree_outputs)==2 and len(set(tree_outputs))==1 and len(tree_outputs[0].strip())==40,'Complete original clean index/tree exact before and after')
    v.check(len(PR_outputs)==1,'Exactly one original draft PR readback before stopped diff')
    rootraw=v.regular(v.A/'ROOT_ACTUAL_CPU_STOP_AUTHENTICATION_20261006.json');root=v.obj(rootraw)
    v.check(root['actual_child_PID']==59213 and root['actual_exit_code']==-24 and root['completed_readonly_children']==21 and root['workspace_nonexportable'] is True,'Root stopped observations independently agree')
    inventory=[]
    for f in sorted(candidate.rglob('*')):
        st=f.lstat();v.check(stat.S_ISDIR(st.st_mode) or (stat.S_ISREG(st.st_mode) and st.st_nlink==1),'Regular stopped workspace nodes')
        if stat.S_ISREG(st.st_mode):inventory.append({'path':str(f.relative_to(candidate)),**v.regular(f,retain=False)})
    v.check(inventory==root['full_inventory'] and len(inventory)==129 and sum(x['path'].startswith('offer/') for x in inventory)==84,'Full immutable129 files/all84 complete scoped offers')
    expectedfiles={'START.json','PROCESS_JOURNAL.json','PROCESS_LAUNCHES.json'}|{str(i)+'.'+kind+'.bin' for i in range(21) for kind in ['stdout','stderr']}|{x['path'] for x in inventory if x['path'].startswith('offer/')}
    v.check({x['path'] for x in inventory}==expectedfiles,'Full stop file accounting; no hidden worker/reassessment')
    seed=v.obj(v.audit(g['seed_inventory_pin']));seedpath=pathlib.Path(seed['source_workspace'])
    for spec in seed['files']:v.regular(seedpath/spec['path'],spec,retain=False)
    v.check({str(f.relative_to(seedpath)) for f in seedpath.rglob('*') if f.is_file()}=={x['path'] for x in seed['files']} and len(seed['files'])==61,'Original native failed run still exact')
    stopped=v.obj(v.audit(g['stopped_continuation_inventory_pin']));stoppedpath=pathlib.Path(stopped['source_workspace'])
    for spec in stopped['files']:v.regular(stoppedpath/spec['path'],spec,retain=False)
    v.check({str(f.relative_to(stoppedpath)) for f in stoppedpath.rglob('*') if f.is_file()}=={x['path'] for x in stopped['files']} and len(stopped['files'])==10,'Earlier remote-main failure still exact')
    source=v.regular(D/'post_assess_carryforward.py').decode();v.check(source.index("a.atomic(workspace/'offer'/name,b)") < source.index('diff=rr.full_diff(current_before,alloffers,a.PREFIX)') < source.index("a.main_preflight(cap,packet['runtime'],current_main)",source.index('diff=rr.full_diff')),'Exact post84-offer/pre-final7-reads bottleneck source location')
    result={'schema':'pr110-independent-CPU-stopped-private-offer-custody/v1','UTC_start':began,'UTC_end':v.now(),'actual_reviewer_PID':os.getpid(),'checks':v.checks,'root_stop_authentication_pin':v.pin(rootraw),'outer_receipt_pin':v.pin(v.regular(outerdir/'execution.json')),'actual_operator_PID':59213,'actual_outer_PID':59205,'actual_exit_code':-24,'full_raw_completed_readonly_children':21,'full_raw_ancestry_probes':len(ps_pids),'full_inventory':inventory,'all84_offers_complete':True,'all_recorded_groups_absence_confirmed':True,'original_failed61_and_remote_stop10_byte_exact':True,'DIFF_candidate_receipt_and_FAILURE_absent':True,'stopped_workspace_nonexportable':True,'exact_failure_location_inferred_from_all84_offers_and_21_child_journal':'rr.full_diff after offer write before final seven readonly checks','kernel_signal_prevented_FAILURE_writer':True,'future_candidate_approved':False,'reviewer_native_assess_calls':0,'reviewer_Git_mutations':0,'reviewer_service_calls':0,'verification_source_pin':v.pin(pathlib.Path(__file__).read_bytes())}
    v.save('CPU_STOP_CUSTODY_RESULT.json',result);print(json.dumps({k:z for k,z in result.items() if k!='full_inventory'}))
if __name__=='__main__':main()
