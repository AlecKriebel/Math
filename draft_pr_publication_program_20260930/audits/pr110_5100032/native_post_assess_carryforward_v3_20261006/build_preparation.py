"""Narrow preparation builder. No live continuation, Git or service mutation."""
import pathlib,json,types,sys,os,stat,hashlib,datetime
D=pathlib.Path(__file__).parent;A=D.parent;F2=A/'native_post_assess_carryforward_v2_20261006'
def mod(name,path):
 m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m;exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
a=mod('preparation_custody_reader',F2/'native_acceptance_actions_v3.py')
def ap(path):return {'path':str(path.relative_to(A)),**a.pin(a.read(path,32*1024*1024))}
def put(name,v):a.atomic(D/name,a.canonical(v) if not isinstance(v,(str,bytes)) else v.encode() if isinstance(v,str) else v)
W=F2/'workspaces/candidate_d9eb646c1dd70e89';R=A/'actual_operations/root_actual_post_assess_carryforward_20261006'
files=[]
for p in sorted(W.rglob('*')):
 st=p.lstat();a.need(stat.S_ISDIR(st.st_mode) or (stat.S_ISREG(st.st_mode) and st.st_nlink==1),'Unique safe stopped member')
 if stat.S_ISREG(st.st_mode):files.append({'path':str(p.relative_to(W)),**a.pin(a.read(p,32*1024*1024))})
outer=[]
for p in sorted(R.rglob('*')):
 st=p.lstat();a.need(stat.S_ISDIR(st.st_mode) or (stat.S_ISREG(st.st_mode) and st.st_nlink==1),'Unique safe outer custody member')
 if stat.S_ISREG(st.st_mode):outer.append(ap(p))
e=a.loads(a.read(R/'execution.json'));j=a.loads(a.read(W/'PROCESS_JOURNAL.json'))
a.need(len(files)==129 and sum(x['path'].startswith('offer/') for x in files)==84 and len(j['records'])==21,'Exact stopped actual custody counts')
a.need(e['child_PID']==59213 and e['exit_code']==-24 and e['reaped'] is True and e['all_recorded_groups_absence_confirmed'] is True and e['streams_fully_drained'] is True and e['cleanup_errors']==[],'Actual kernel CPU stop, reap and bounded outer cleanup')
a.need(all(not os.path.lexists(W/n) for n in ['FAILURE.json','DIFF.txt','CANDIDATE_RECEIPT.json']),'Stopped candidate remains incomplete; no invented failure')
inv={'schema':'pr110-preserved-CPU-limit-stop-inventory/v1','UTC':a.now(),'actual_inventory_reader_PID':os.getpid(),'source_workspace':str(W),'actual_stopped_continuation_PID':59213,'actual_outer_operator_PID':59205,'original_packet_sha256':'d9eb646c1dd70e891cc44bcaa5de2b62fc0c5a6eabdf2d487a148c3d3cc02281','file_count':len(files),'offer_count':84,'total_bytes':sum(x['bytes'] for x in files),'files':files,'outer_execution_pin':ap(R/'execution.json'),'outer_launcher_source_pin':ap(A/'publication_build_v1/record_native_carryforward.py'),'checked_artifacts':outer,'actual_exit_code':-24,'actual_elapsed_seconds':e['elapsed_monotonic_seconds'],'existing_readonly_children':21,'partial_offer_must_not_be_exported':True,'DIFF_present':False,'candidate_receipt_present':False,'FAILURE_present':False,'failure_receipt_invented':False,'native_assess_calls_during_stopped_continuation':0,'live_export_executed':False,'preservation_only':True}
put('STOPPED_CPU_CONTINUATION_INVENTORY.json',inv)
# Copy sealed scientific title/body without changing their claims.
for n in ['accepted_title.txt','accepted_body.md']:
 if (F2/n).exists():put(n,a.read(F2/n))
phase=a.read(F2/'native_acceptance_actions_v3.py').decode().replace("F = A / 'native_post_assess_carryforward_v2_20261006'","F = A / 'native_post_assess_carryforward_v3_20261006'")
method='''def verify_stopped_CPU_continuation(spec):
    item=loads(audit(spec));root=A/'native_post_assess_carryforward_v2_20261006/workspaces/candidate_d9eb646c1dd70e89'
    need(A/relpath(spec['path'])==F/'STOPPED_CPU_CONTINUATION_INVENTORY.json'
         and item['schema']=='pr110-preserved-CPU-limit-stop-inventory/v1'
         and item['source_workspace']==str(root) and item['actual_stopped_continuation_PID']==59213
         and item['actual_outer_operator_PID']==59205 and item['file_count']==129 and item['offer_count']==84
         and item['original_packet_sha256']=='d9eb646c1dd70e891cc44bcaa5de2b62fc0c5a6eabdf2d487a148c3d3cc02281',
         'Exact previous CPU-stop custody')
    names=set();total=0
    for entry in item['files']:
        relpath(entry['path']);need(entry['path'] not in names,'Unique CPU-stop member');names.add(entry['path'])
        measured=read(root/entry['path'],32*1024*1024,entry,retain=False);total+=measured['bytes']
    actual=set()
    for path in root.rglob('*'):
        st=path.lstat();need(stat.S_ISDIR(st.st_mode) or (stat.S_ISREG(st.st_mode) and st.st_nlink==1),'Safe CPU-stop member')
        if stat.S_ISREG(st.st_mode):actual.add(str(path.relative_to(root)))
    need(actual==names and total==item['total_bytes'] and sum(x.startswith('offer/') for x in names)==84
         and all(not os.path.lexists(root/n) for n in ['FAILURE.json','DIFF.txt','CANDIDATE_RECEIPT.json']),
         'All129 stopped bodies unchanged and incomplete')
    need(item['partial_offer_must_not_be_exported'] is True and item['failure_receipt_invented'] is False
         and item['DIFF_present'] is False and item['candidate_receipt_present'] is False and item['FAILURE_present'] is False
         and type(item['native_assess_calls_during_stopped_continuation']) is int
         and item['native_assess_calls_during_stopped_continuation']==0 and item['live_export_executed'] is False,
         'No fabricated failure or completed candidate')
    for entry in item['checked_artifacts']:audit(entry)
    outer=loads(audit(item['outer_execution_pin']));launcher=audit(item['outer_launcher_source_pin'],128*1024)
    need(outer['schema']=='pr110-actual-bounded-native-carryforward-launch/v1'
         and outer['child_PID']==59213 and outer['actual_operator_PID']==59205 and outer['exit_code']==-24
         and outer['reaped'] is True and outer['streams_fully_drained'] is True
         and outer['all_recorded_groups_absence_confirmed'] is True and outer['cleanup_errors']==[]
         and outer['whole_launch_deadline_seconds']==300 and outer['actual_continuation_custody_path']==str(root)
         and outer['outer_source_pin']==pin(launcher),'Actual CPU signal/reap/bounded outer custody')
    journal=loads(read(root/'PROCESS_JOURNAL.json'))
    need(journal['actual_operator_PID']==59213 and len(journal['records'])==21
         and all(x['exit_code']==0 and x['reaped'] is True and x['fully_drained'] is True
                 and x['process_group_absence_confirmed'] is True and x['cwd']==str(C)
                 for x in journal['records']),'Previous21 readonly children complete')
    return item

'''
a.need(phase.count('def load_gate(path,action):')==1,'Unique gate insertion')
phase=phase.replace('def load_gate(path,action):',method+'def load_gate(path,action):')
needle="    verify_stopped_continuation(r['stopped_continuation_inventory_pin'])\n"
extra="""    need(gate['stopped_CPU_continuation_inventory_pin']==r['stopped_CPU_continuation_inventory_pin']
         and ad['stopped_CPU_continuation_inventory_pin']==r['stopped_CPU_continuation_inventory_pin'],
         'CPU-stop inventory bound by candidate/adversary/root')
    verify_stopped_CPU_continuation(r['stopped_CPU_continuation_inventory_pin'])
    need(gate['linear_diff_program_pin']==r['linear_diff_program_pin']
         and ad['linear_diff_program_pin']==r['linear_diff_program_pin']
         and A/relpath(r['linear_diff_program_pin']['path'])==F/'linear_full_diff.py',
         'Exact linear DIFF source bound by candidate/adversary/root')
    audit(r['linear_diff_program_pin'],128*1024)
    need(r['diff_algorithm']=='linear-single-replacement-hunk-with-three-context-lines'
         and r['original_resource_policy_unchanged'] is True
         and r['parent_limits']['requested']==original_packet['resources']
         and r['parent_limits']['enforced']=={
             'RLIMIT_CPU':[original_packet['resources']['cpu_seconds']]*2,
             'RLIMIT_FSIZE':[original_packet['resources']['file_size_bytes']]*2,
             'RLIMIT_NOFILE':[original_packet['resources']['open_files']]*2},
         'Original worker/continuation resource policy remains unchanged')
"""
a.need(phase.count(needle)==1,'Unique candidate continuation guard');phase=phase.replace(needle,needle+extra)
put('native_acceptance_actions_v4.py',phase)
src=a.read(F2/'post_assess_carryforward.py').decode().replace("D=A/'native_post_assess_carryforward_v2_20261006'","D=A/'native_post_assess_carryforward_v3_20261006'").replace('native_acceptance_actions_v3.py','native_acceptance_actions_v4.py')
src=src.replace("'Fixed reviewed phase v2 source'","'Fixed reviewed phase v4 source'")
needle="    a=load_module('pr110_continued_phase_actions',phase_body,D/'native_acceptance_actions_v4.py')\n"
extra="""    need(A/pathlib.PurePosixPath(g['linear_diff_program_pin']['path'])==D/'linear_full_diff.py',
         'Fixed reviewed linear DIFF source')
    linear_body=audit(g['linear_diff_program_pin'],128*1024)
    linear=load_module('pr110_linear_review_diff',linear_body,D/'linear_full_diff.py')
    need(g['original_resource_policy_unchanged'] is True,'No resource-policy extension')
"""
a.need(src.count(needle)==1,'Unique phase module insertion');src=src.replace(needle,needle+extra)
needle="         and ad['stopped_continuation_inventory_pin']==g['stopped_continuation_inventory_pin']\n"
extra="""         and ad['stopped_CPU_continuation_inventory_pin']==g['stopped_CPU_continuation_inventory_pin']
         and ad['linear_diff_program_pin']==g['linear_diff_program_pin']
         and ad['original_resource_policy_unchanged'] is True
"""
a.need(src.count(needle)==1,'Unique adversary source binding');src=src.replace(needle,needle+extra)
needle="    a.verify_stopped_continuation(g['stopped_continuation_inventory_pin'])\n"
a.need(src.count(needle)==1,'Unique initial stop guard');src=src.replace(needle,needle+"    a.verify_stopped_CPU_continuation(g['stopped_CPU_continuation_inventory_pin'])\n")
src=src.replace("Both stopped workspaces remain intact and nonexportable. ","All three stopped workspaces remain intact and nonexportable. ")
src=src.replace("diff=rr.full_diff(current_before,alloffers,a.PREFIX)","diff=linear.full_diff(current_before,alloffers,a.PREFIX)")
needle="verify_seed(a,seed);a.verify_stopped_continuation(g['stopped_continuation_inventory_pin']);"
a.need(src.count(needle)==1,'Unique final preservation guard');src=src.replace(needle,"verify_seed(a,seed);a.verify_stopped_continuation(g['stopped_continuation_inventory_pin']);a.verify_stopped_CPU_continuation(g['stopped_CPU_continuation_inventory_pin']);")
needle="            'integration_inputs_pin':g['integration_inputs_pin'],'stopped_continuation_inventory_pin':g['stopped_continuation_inventory_pin'],'original_head':p.HEAD,'native_assess_actual_PID':23360,\n"
extra="""            'stopped_CPU_continuation_inventory_pin':g['stopped_CPU_continuation_inventory_pin'],
            'linear_diff_program_pin':g['linear_diff_program_pin'],
            'diff_algorithm':'linear-single-replacement-hunk-with-three-context-lines',
            'original_resource_policy_unchanged':True,'preserved_CPU_limit_stop_PID':59213,
"""
a.need(src.count(needle)==1,'Unique receipt binding');src=src.replace(needle,needle+extra)
put('post_assess_carryforward_v3.py',src)
put('.gitignore','workspaces/\ncontrols/\n')
print(json.dumps({'newfolder':str(D),'inventory_files':len(files),'outer_artifacts':len(outer),'source':ap(D/'post_assess_carryforward_v3.py'),'phase':ap(D/'native_acceptance_actions_v4.py'),'helper':ap(D/'linear_full_diff.py'),'stop_inventory':ap(D/'STOPPED_CPU_CONTINUATION_INVENTORY.json')}))
