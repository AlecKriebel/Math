#!/usr/bin/env python3
"""Independent read-only full stopped/inspect custody and337 immutable Git bodies."""
import pathlib,types,os,json,stat,ast
R=pathlib.Path(__file__).resolve().parent;W=R.parent
v=types.ModuleType('acceptance_independent');v.__file__=str(W/'verify_actual_candidate.py');exec(compile(pathlib.Path(v.__file__).read_bytes(),v.__file__,'exec'),v.__dict__);v.W=R
# Same previously audited bounded immutable Git-body reader, with canonical
# whole repository path rather than the native-folder prefix only.
src=pathlib.Path(v.__file__).read_text();tree=ast.parse(src);node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='git_blob');body=ast.get_source_segment(src,node).replace('def git_blob(p,name):','def whole_git_blob(p,name):').replace("p['main_parent']+':unsolved_math_prioritization/'+name","p['main_parent']+':'+name")
exec(compile(body,'<bounded-whole-repository-read>','exec'),v.__dict__)
A=v.A;C=v.C;commit='f2cc75042ad93167c4126bfc1846fd09ac5c8325';parent='e0a94b93520610553c001f265f210f959b591c2c'
def ap(path):return {'path':str(path.relative_to(A)),**v.regular(path,retain=False)}
def inventory(path):
    out=[]
    for f in sorted(path.rglob('*')):
        st=f.lstat();v.check(stat.S_ISDIR(st.st_mode) or (stat.S_ISREG(st.st_mode) and st.st_nlink==1),'Safe unique-link custody member')
        if stat.S_ISREG(st.st_mode):out.append({'path':str(f.relative_to(path)),**v.regular(f,retain=False)})
    return out

def main():
    began=v.now();p=v.obj(v.regular(v.PACKET));native=v.obj(v.regular(A/'native_post_assess_carryforward_v3_20261006/workspaces/candidate_d9eb646c1dd70e89/CANDIDATE_RECEIPT.json'))
    olddir=A/'actual_acceptance_actions_20261006/pr110_acceptance_commit_20261006';od=A/'actual_operations/root_actual_pr110_acceptance_commit_20261006';cur=A/'actual_acceptance_reconciliation_20261006/inspect'
    oldgate=v.obj(v.regular(A/'actual_action_commissions_20261006/acceptance_commit_ROOT_GATE.json'));origad=v.obj(v.regular(W/'ACTUAL_NATIVE_CANDIDATE_ADVERSARY.json'))
    v.check(oldgate['candidate_receipt_pin']==origad['candidate_receipt_pin']==v.pin(v.regular(A/'native_post_assess_carryforward_v3_20261006/workspaces/candidate_d9eb646c1dd70e89/CANDIDATE_RECEIPT.json')),'Actual original candidate binding remains exact')
    paths={x['path']:x['after'] for x in native['affected_paths']};paths[v.PREFIX+'NATIVE_ACCEPTANCE_RECEIPT.json']=v.pin(v.audit(oldgate['export_receipt_pin']))
    for x in oldgate['additional_checkpoint_pins']:
        v.check(x['path'].startswith(str(A.relative_to(C))+'/') and x['path'] not in paths,'Exact collision-free scoped additional checkpoint');paths[x['path']]={k:x[k] for k in ['bytes','sha256']}
    v.check(len(paths)==337 and len(native['affected_paths'])==84 and len(oldgate['additional_checkpoint_pins'])==252,'Exact prior337 selection')
    full={};view={**p,'main_parent':commit}
    for name,expected in paths.items():
        physical=v.regular(C/name,expected);blob=v.whole_git_blob(view,name);v.check(blob==physical and v.pin(blob)==expected,'Every complete selected physical/Git body independently exact');full[commit+':'+name]=blob
    receipt=v.obj(v.regular(cur/'RECEIPT.json'));start=v.obj(v.regular(cur/'START.json'));inspection=v.obj(v.regular(cur/'PROCESS_JOURNAL.json'));launches=v.obj(v.regular(cur/'PROCESS_LAUNCHES.json'));absence=v.obj(v.regular(cur/'STOPPED_ACTION_FRESH_ABSENCE.json'));ig=v.obj(v.audit(start['gate_pin']))
    v.check(ig['mode']==start['mode']=='inspect' and ig['program_pin']==start['program_pin']==receipt['reconciliation_program_pin']==ap(A/'publication_build_v1/reconcile_acceptance_commit.py'),'Exact actually inspected source and fresh gate')
    v.check(ig['actual_review'] is True and ig['clearance'] is True and ig['required_findings']==[] and v.stamp(ig['UTC'])<=v.stamp(start['UTC'])<=v.stamp(receipt['UTC']),'Actual fresh read-only inspect authorization/chronology')
    v.check(receipt['actual_operator_PID']==start['actual_operator_PID']==inspection['actual_operator_PID']==launches['actual_operator_PID']==87582 and len(inspection['records'])==len(launches['launches'])==349,'All349 actual inspect child receipts/registrations')
    v.check(receipt['commit']==commit and receipt['parent']==parent and receipt['tree']=='a0675450b2f0bbdf4377e3eef38c117074828a39' and receipt['remote_main']==parent and receipt['remote_verified'] is False and receipt['reconciliation_mode']=='inspect' and receipt['recommit_executed'] is False and receipt['new_assess_calls']==0 and receipt['old_outer_full_stream_custody_claimed'] is False,'Honest existing local commit/read-only remote inspect')
    expectedpins=[{'path':n,**paths[n]} for n in sorted(paths)];v.check(receipt['pins']==expectedpins and receipt['changed_paths']==sorted(paths),'Exact full337 receipt scope and all pins')
    env=p['runtime']['python_environment'];rt=p['runtime'];gb=[rt['binaries']['git']['resolved_absolute_path'],'-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-c','credential.helper=','-c','commit.gpgsign=false','-c','gc.auto=0'];ge={**env,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_CONFIG_SYSTEM':'/dev/null','GIT_OPTIONAL_LOCKS':'0','GIT_NO_REPLACE_OBJECTS':'1','GIT_TERMINAL_PROMPT':'0'};he={**env,'GH_CONFIG_DIR':rt['gh_config_directory'],'GH_HOST':'github.com','GH_PROMPT_DISABLED':'1','GH_PAGER':'','GH_BROWSER':'/usr/bin/false','GH_EDITOR':'/usr/bin/false','GH_NO_UPDATE_NOTIFIER':'1'}
    gh=[rt['binaries']['gh']['resolved_absolute_path'],'pr','view','https://github.com/AlecKriebel/Math/pull/110','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body,mergeCommit,mergedAt,url']
    args=[(['symbolic-ref','--short','HEAD'],b'main\n'),(['rev-parse','HEAD'],(commit+'\n').encode()),(['ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main'],(parent+'\trefs/heads/main\n').encode()),(['diff','--cached','--name-only','-z'],b''),(['diff','--name-only','--diff-filter=ACMRTUXB','-z'],b''),(['show','-s','--format=%P',commit],(parent+'\n').encode()),(['show','-s','--format=%B',commit],(oldgate['commit_message']+'\n\n').encode()),(['diff-tree','--no-commit-id','--name-only','-r','-z',commit],None)]
    contracts=[(['/bin/ps','-axo','pid=,ppid=,pgid='],env,None)]+[(gb+a,ge,b) for a,b in args]+[(gb+['show',commit+':'+n],ge,full[commit+':'+n]) for n in sorted(paths)]+[(gb+['rev-parse',commit+'^{tree}'],ge,(receipt['tree']+'\n').encode()),(gb+['write-tree'],ge,(receipt['tree']+'\n').encode()),(gh,he,None)]
    def children(where,records,registrations,contracts,operator_start,operator_end):
        v.check(len(records)==len(contracts),'Exact child contract count')
        for i,(x,s,(argv,e,known)) in enumerate(zip(records,registrations,contracts)):
            v.check(x['argv']==argv and x['cwd']==str(C) and x['environment_sha256']==v.sha(v.canon(e)),'Exact actual child argv/cwd/env')
            v.check(x['exit_code']==0 and x['reaped'] is True and x['fully_drained'] is True and x['process_group_absence_confirmed'] is True and x['termination_reason'] is None and x['error'] is None,'Every completed actual child bounds/fullcapture/reap/group absence')
            v.check(s['PID']==x['actual_PID'] and s['state']=='reaped' and all(s[k]==x[k] for k in ['argv','cwd','environment_sha256','UTC_start']),'Durable registration corresponds to actual child')
            v.check(v.stamp(operator_start)<=v.stamp(x['UTC_start'])<=v.stamp(x['UTC_end'])<=v.stamp(operator_end),'Actual child chronological interval')
            for kind in ['stdout','stderr']:
                q=x['streams'][kind];b=v.regular(where/q['retained_file'],q['retained'])
                if kind=='stderr':v.check(b==b'' and q['full'] is True and q['observed']==v.pin(b),'Exact full child stderr')
                elif q['full']:v.check(q['observed']==v.pin(b) and (known is None or b==known),'Full dynamic child stdout')
                else:
                    ref=q['complete_body_retained_in_immutable_Git'];v.check(ref in full and q['observed']==v.pin(full[ref]) and b==full[ref][:4096],'Full observed committed body hash and honestly retained exact prefix')
    children(cur,inspection['records'],launches['launches'],contracts,start['UTC'],receipt['UTC'])
    ps=v.regular(cur/inspection['records'][0]['streams']['stdout']['retained_file']);rows=[tuple(map(int,x.split())) for x in ps.splitlines() if x.strip()]
    oldj=v.obj(v.regular(olddir/'PROCESS_JOURNAL.json'));oldl=v.obj(v.regular(olddir/'PROCESS_LAUNCHES.json'));outer=v.obj(v.regular(od/'execution.json'));fail=v.obj(v.regular(olddir/'FAILURE.json'));groups=set(outer['recorded_PGIDs'])|{84526}|{x['PID'] for x in oldl['launches']}
    v.check(absence['recorded_groups']==sorted(groups) and absence['all_freshly_absent'] is True and not any(pid==84526 or ppid==84526 or pgid in groups for pid,ppid,pgid in rows),'Full actual fresh ps independently confirms all durable/observed old absence')
    v.check(absence['old_final_child_reap_historically_unconfirmed'] is True and absence['old_outer_full_stream_custody_claimed'] is False and len(oldj['records'])==131 and len(oldl['launches'])==132 and oldl['launches'][-1]['PID']==84786 and oldl['launches'][-1]['state']=='launched_not_yet_reaped','Old incomplete child status remains explicit')
    v.check(outer['streams_fully_drained'] is False and outer['termination_reason']=='outer_exception:RuntimeError' and outer['cleanup_errors']==[{'action':'final_discovery','error':'Bounded real launch journal'}] and outer['exit_code']==1 and fail['error']=='SystemExit: Actual operator SIGTERM','Honest interrupted original outer/inner evidence')
    for kind in ['stdout','stderr']:
        q=outer[kind];b=v.regular(od/q['path'],q);v.check(b==b'' and q['body_custody']=='explicit_truncated_prefix','Empty retained old outer prefixes are not full streams')
    v.check(not any(any(x in r['argv'] for x in ['push','assess']) for r in oldl['launches']) and not (olddir/'LOCAL_RECEIPT.json').exists() and not (olddir/'RECEIPT.json').exists(),'No original push/completed receipt or native assess')
    v.check(oldj['records'][8]['argv']==gb+['add','-f','--']+sorted(paths) and oldj['records'][11]['argv']==gb+['-c','user.name=Alec Kriebel','-c','user.email=me@aleckriebel.com','commit','-m',oldgate['commit_message']],'Original two authorized scoped mutators exact')
    for i,(x,s) in enumerate(zip(oldj['records'],oldl['launches'])):
        v.check(x['cwd']==str(C) and x['exit_code']==0 and x['reaped'] is True and x['fully_drained'] is True and x['process_group_absence_confirmed'] is True and x['error'] is None and x['termination_reason'] is None and s['PID']==x['actual_PID'] and s['state']=='reaped','All131 completed old child custody retained')
        for kind in ['stdout','stderr']:
            q=x['streams'][kind];b=v.regular(olddir/q['retained_file'],q['retained'])
            if q['full']:v.check(q['observed']==v.pin(b),'Full old actual response pin')
            else:
                ref=q['complete_body_retained_in_immutable_Git'];v.check(ref in full and q['observed']==v.pin(full[ref]) and b==full[ref][:4096],'Full old committed actual read observed hash/prefix')
    for i,q in enumerate(outer['actual_ancestry_probes']):
        raw=v.obj(v.regular(od/'ancestry'/(str(i)+'.execution.json')));v.check(all(q[k]==raw[k] for k in raw),'Actual old ancestry receipt body')
        for kind in ['stdout','stderr']:v.regular(od/q[kind]['path'],q[kind])
    v.check(inspection['records'][8]['streams']['stdout']['full'] is True and set(v.regular(cur/'8.stdout.bin').decode().strip('\0').split('\0'))==set(paths),'Full current committed changed path stream')
    v.check(set(v.regular(olddir/'9.stdout.bin').decode().strip('\0').split('\0'))==set(paths),'Exact original staged337 selection')
    pr=v.obj(v.regular(cur/'348.stdout.bin'));v.check(pr['number']==110 and pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==v.HEAD and pr['headRefName']=='dot/math-5100032' and pr['baseRefName']=='main','Actual original draft/head still unchanged')
    result={'schema':'pr110-independent-interrupted-acceptance-reconciliation-audit/v1','UTC_start':began,'UTC_end':v.now(),'actual_reviewer_PID':os.getpid(),'checks':v.checks,'actual_inspect_PID':87582,'actual_inspect_children':349,'all337_full_live_and_immutable_Git_bodies_independently_reproduced':True,'selection_pins':expectedpins,'actual_inspect_receipt_pin':ap(cur/'RECEIPT.json'),'actual_inspect_source_pin':start['program_pin'],'original_phase_completed_children':131,'original_authorized_mutation_children':[84542,84549],'original_durable_registrations':132,'original_last_child_historical_reap_unconfirmed':84786,'original_outer_full_stream_custody_claimed':False,'all_old_groups_freshly_absent_in_actual_full_ps':True,'original_phase_inventory':inventory(olddir),'original_outer_inventory':inventory(od),'actual_inspect_inventory':inventory(cur),'commit':commit,'tree':receipt['tree'],'remote_e0_observed_by_actual_inspect':True,'single_CAS_push_pending':True,'native_assess_calls':0,'reviewer_Git_mutations':0,'reviewer_service_calls':0,'source_pin':v.pin(pathlib.Path(__file__).read_bytes())}
    v.save('RECONCILIATION_AUDIT_RESULT.json',result);v.save('INDEPENDENT_STATIC_GIT_BODY_JOURNAL.json',v.journal);print(json.dumps({k:z for k,z in result.items() if k not in ['selection_pins','original_phase_inventory','original_outer_inventory','actual_inspect_inventory']}))
if __name__=='__main__':main()
