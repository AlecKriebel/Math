"""Complete only the unperformed push of a verified existing checkpoint commit.

The original operator remains failed. No staging, commit, merge, PR or service
action is possible here. All project executable input bodies are checked locally
before the exact previously reviewed capture function is compiled.
"""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import ast,copy,fcntl,gzip,hashlib,json,os,signal,stat,subprocess,sys,types
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';W=Path(__file__).parent;A=W.parent
B=A/'publication_checkpoint_037_actual_private';S=P/'SHARED_GIT_WINDOW_STATUS.json';CLEAR=W/'ROOT_RECOVERY_CLEARANCE.json'
BASE='2669042ac964d5710972af552df141f7934588af';COMMIT='0a49d5e66a0fb9d4f78c7f3a7f3b30cd77196567';ENDPOINT='https://github.com/AlecKriebel/Math.git'
PLAN=A/'publication_checkpoint_037_preparation/CONTENT_PLAN.json';OLD_SOURCE=A/'root_checkpoint_publication_037.py';BASIS=W/'PRESERVED_FAILED_BASIS.json';OLD_CONTROL=W/'EXACT_OLD_CHECKPOINT_CONTROL.json'
FRAME=P/'audits/pr305_5100034/root_during_peer_pause_20261005/native_integration_preparation/integrate_pr305.py'
utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(Path(p).read_bytes())
def require(v,m):
    if not v:raise RuntimeError(m+'; retain truthful partial outcomes; no automatic mutation retry')
def pin(p):
    p=Path(p);require(p.is_file() and not p.is_symlink(),'literal file');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def names(b):return {x.decode() for x in b.split(b'\0') if x}
def original_native(i):
    j=load(B/(str(i)+'_execution.json'));q=load(B/(str(i)+'_request.json'));start=load(B/(str(i)+'_started.json'))
    require(all(j[k]==v for k,v in q.items()) and all(j[k]==v for k,v in start.items()) and j['cwd']==str(R) and j['automatic_retry'] is False,'original request/start agreement')
    require(type(j['actual_PID']) is int and j['actual_PID']>0 and j['actual_PID']==j['cooperative_process_group'] and datetime.fromisoformat(j['start_UTC'])<=datetime.fromisoformat(j['end_UTC']),'original PID/group/UTC')
    require(j['full_stream_capture_complete'] is True and j['parent_reaped'] is True and j['timeout_cleanup_required'] is False,'original complete capture/cleanup')
    streams={}
    for n in ['stdout','stderr']:
        x=j[n];path=B/(str(i)+'_'+n+'.gz');z=path.read_bytes();b=gzip.decompress(z)
        require(x['path']==str(path) and len(z)==x['stored_bytes'] and sha(z)==x['stored_sha256'] and len(b)==x['logical_bytes'] and sha(b)==x['logical_sha256'],'full original stored/logical stream');streams[n]=b
    require(j['exit_code']==(1 if i==1 else 0),'original honest allowed exits')
    if i==1:require(j['argv'][:4]==['/usr/bin/git','--no-optional-locks','config','--get-regexp'] and not streams['stdout'] and not streams['stderr'],'first permitted no-match config query')
    return j,streams
def main():
    require(not sys.flags.optimize,'optimization forbidden')
    lock=(W/'RECOVERY.lock').open('a+b');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    clear=load(CLEAR);control=load(S);lease=control['descending_302_checkpoint037_push_recovery_lease'];source=pin(__file__);clear_pin=pin(CLEAR)
    require(clear['status']=='PASS_EXISTING_CHECKPOINT037_VERIFIED_PUSH_ONLY_RECOVERY' and clear['unresolved_issues']==[] and clear['push_only_authorized'] is True and clear['original_operator_exit_code']==1 and clear_pin['mode']==0o444,'genuine truthful ROOT recovery approval')
    require(clear['operator']==source and source['mode']==0o444 and clear['existing_commit']==COMMIT and clear['expected_old_remote']==BASE,'exact reviewed recovery source/epoch')
    exact_inputs={str(p) for p in [PLAN,OLD_SOURCE,BASIS,OLD_CONTROL,FRAME,A/'ROOT_CHECKPOINT037_FAILED_BOUNDARY.json',A/'ROOT_ACTUAL_PUBLICATION_AND_TRACKER_ACCEPTANCE.json']}
    require(type(clear['bound_inputs']) is list and len(clear['bound_inputs'])==len(exact_inputs) and {x['path'] for x in clear['bound_inputs']}==exact_inputs,'all seven nonvacuous approved roles before executable project code')
    for x in clear['bound_inputs']:require(pin(x['path'])==x,'every current approved source/input body/mode')
    require(pin(PLAN)['sha256']=='d53016a0a97ee457fbf99edd3139a025032a3d9b9314ddd3fab5693ec054c857' and pin(OLD_SOURCE)['sha256']=='c84239da2769ffc7bc4e6a444f05911d2a0d5703c60e08baa52c673925fbcf4c' and pin(BASIS)['sha256']=='f04b9b0b53619152df0e19315c7af91c707bd0bc47cc687d0ebccf9c3fc278b9' and pin(OLD_CONTROL)['sha256']=='7a9cbd0911f93823ff851a74b364b3cc0b81b55654d52e171ac9af35e1c78ff1','exact preserved failed basis and original bodies')
    review=Path(clear['review_namespace']);require(review==A/'checkpoint037_push_recovery_adversary_02','fresh independent review')
    pins=clear['closed_review_pins'];require(set(pins)=={'REPORT.md','DERIVATION.md','READ_SCOPE_LEDGER.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'},'all exact six closed review roles')
    for name,x in pins.items():require(pin(review/name)==x and x['mode']==0o444,'exact frozen review role')
    require(load(review/'VERDICT.json')['unresolved_issues']==[] and load(review/'VERDICT.json')['execution_authority_granted'] is False,'independent review no authority')
    require(not control['shared_git_writes_paused'] and not control['ascending_pr85_publication_integration_window_granted'] and lease['active'] is True and lease['operator']==source and lease['clearance']==clear_pin and lease['endpoint']==ENDPOINT and lease['existing_commit']==COMMIT and lease['expected_old_remote']==BASE and lease['push_only'] is True,'exact fresh live push-only lease')
    basis=load(BASIS);require(basis['original_outer_exit_code']==1 and basis['unperformed_push'] is True and basis['no_failed_evidence_rewritten'] is True and len(basis['files'])==4289,'truthful nonempty preserved original failure')
    require({x['path'] for x in basis['files']}=={str(x) for x in B.rglob('*') if x.is_file()},'complete original basis coverage')
    for x in basis['files']:require(pin(x['path'])==x,'every4289original evidence body/mode')
    old_records=[original_native(i) for i in range(1,809)];require(not any(x[0]['argv'][2:3]==['push'] for x in old_records),'original push genuinely unperformed')
    require(old_records[310][0]['argv']==['/usr/bin/git','--no-optional-locks','commit','-m','Publish PR302 reviewed spectral consistency note and verified DOI tracker record'] and old_records[310][0]['actual_PID']==22132,'actual original commit role')
    plan=load(PLAN);owned=set(plan['allowed_paths']);require(len(owned)==244 and owned=={x['target'] for x in plan['targets']}|{str(PLAN.relative_to(R))},'exact original244scope')
    expected={x['target']:(R/x['input']['path']).read_bytes() for x in plan['targets']};expected[str(PLAN.relative_to(R))]=PLAN.read_bytes()
    modes={x['target']:int(x['input']['mode'],8) for x in plan['targets']};modes[str(PLAN.relative_to(R))]=0o444
    for x in plan['targets']:
        p=pin(R/x['input']['path']);require((p['bytes'],p['sha256'],oct(p['mode']))==(x['input']['bytes'],x['input']['sha256'],x['input']['mode']),'each original243approved input')
    actual=W/'actual_push_recovery';require(not actual.exists(),'prior or uncertain recovery attempt');actual.mkdir()
    archives=[]
    for i,p in enumerate([Path(__file__),CLEAR,S,*[Path(x) for x in sorted(exact_inputs)]]):
        b=p.read_bytes();q=actual/(str(i)+'_'+p.name+'.source.gz');q.write_bytes(gzip.compress(b,mtime=0));require(gzip.decompress(q.read_bytes())==b,'full recovery prelaunch input');archives.append(dict(input=pin(p),archive=pin(q)))
    (actual/'ATTEMPT.json').write_text(json.dumps(dict(UTC=utc(),actual_recorder_PID=os.getpid(),original_operator_exit_code=1,source=source,clearance=clear_pin,control=pin(S),existing_commit=COMMIT,full_inputs=archives,automatic_retry=False),indent=2)+'\n')
    framebody=FRAME.read_bytes();require(sha(framebody)=='0ea02436c0ac1e0070169df466c34ba141c43291e16515b3fd1cce2135071897','exact previously reviewed capture body before compilation')
    tree=ast.parse(framebody);mainfn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main');node=next(x for x in mainfn.body if isinstance(x,ast.FunctionDef) and x.name=='run');factory=ast.parse('def factory(actual):\n count=0\n return run\n').body[0];factory.body.insert(1,copy.deepcopy(node));module=ast.fix_missing_locations(ast.Module(body=[factory],type_ignores=[]))
    env=dict(Path=Path,datetime=datetime,timezone=timezone,timedelta=timedelta,hashlib=hashlib,json=json,stat=stat,os=os,sys=sys,subprocess=subprocess,gzip=gzip,signal=signal,R=R,g=types.SimpleNamespace(pin=pin),sha=sha,utc=utc,require=require,__file__=str(Path(__file__).resolve()));exec(compile(module,str(FRAME)+'::verified_capture_only','exec'),env);run=env['factory'](actual)
    def git(*args,ok=(0,)):return run(['/usr/bin/git','--no-optional-locks',*args],ok)
    require(not git('config','--get-regexp','^url[.]',ok=(0,1)),'URL-section mappings outside exact endpoint scope')
    require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==COMMIT and git('show','-s','--format=%P',COMMIT).decode().split()==[BASE],'exact existing main commit/parent')
    require(git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==BASE and not git('diff','--cached','--raw','-z') and not (R/'.git/MERGE_HEAD').exists() and not (R/'.git/index.lock').exists(),'fresh expected-old remote/empty index')
    original_changed=names(next(b['stdout'] for j,b in old_records if j['argv']==['/usr/bin/git','--no-optional-locks','diff','--name-only','-z',BASE,COMMIT]));require(names(git('diff','--name-only','-z',BASE,COMMIT))==original_changed and original_changed<=owned,'actual original changed domain')
    for rel,b in expected.items():require((R/rel).read_bytes()==b and stat.S_IMODE((R/rel).stat().st_mode)==modes[rel] and git('show',':'+rel)==b and git('show',COMMIT+':'+rel)==b and git('ls-tree',COMMIT,'--',rel).decode().split()[:3]==['100644','blob',blob(b)],'all244live/index/committed full bodies and correct filesystem modes')
    def baseline(args):return next(b['stdout'] for j,b in old_records if j['argv']==['/usr/bin/git','--no-optional-locks',*args])
    oldindex=baseline(['ls-files','--stage','-z']);oldflags=baseline(['ls-files','-v','-z']);old_dirty=names(baseline(['diff','--name-only','-z','HEAD']))-owned-{str(S.relative_to(R))};current_dirty=names(git('diff','--name-only','-z','HEAD'))-owned-{str(S.relative_to(R))};require(current_dirty==old_dirty,'exact noncontrol foreign dirty scope')
    olddiff=baseline(['diff','--binary','HEAD','--',*sorted(old_dirty|{str(S.relative_to(R))})]);blocks=olddiff.split(b'diff --git ');noncontrol=b''.join(b'diff --git '+x for x in blocks[1:] if not x.startswith(('a/'+str(S.relative_to(R))+' b/').encode()))
    held=load(B/'KNOWN_HELD_AT_ACTUAL_START.json')['files'];require(len(held)==41160,'all41160known-held nonowned rows')
    def exclude(b,stage):return [x for x in b.split(b'\0') if x and (x.split(b'\t',1)[1].decode() if stage else x[2:].decode()) not in owned]
    def stable():
        require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==COMMIT and not git('diff','--cached','--raw','-z'),'existing commit/index drift')
        require(exclude(git('ls-files','--stage','-z'),True)==exclude(oldindex,True) and exclude(git('ls-files','-v','-z'),False)==exclude(oldflags,False),'entire original foreign index/flags')
        require(names(git('diff','--name-only','-z','HEAD'))-owned-{str(S.relative_to(R))}==old_dirty and (git('diff','--binary','HEAD','--',*sorted(old_dirty)) if old_dirty else b'')==noncontrol,'full noncontrol foreign dirty diff')
        for rel,x in held.items():
            q=pin(R/rel);require((q['path'],q['bytes'],q['sha256'],oct(q['mode']))==(x['path'],x['bytes'],x['sha256'],x['mode']),'all41160known-held complete bodies/modes')
    def authorize():
        require(pin(__file__)==source and pin(CLEAR)==clear_pin and load(S)==control and load(CLEAR)==clear,'current exact approval/lease/control')
        for x in clear['bound_inputs']:require(pin(x['path'])==x,'all approved inputs before sole push')
        stable();require(datetime.now(timezone.utc)+timedelta(seconds=75)<=datetime.fromisoformat(lease['expires_UTC']),'push deadline insufficient')
        require(load(S)==control and pin(CLEAR)==clear_pin,'final live approval/control')
    env['authorize']=authorize;stable();authorize();require(git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==BASE,'last remote before sole original unperformed push')
    git('push','--force-with-lease=refs/heads/main:'+BASE,ENDPOINT,COMMIT+':refs/heads/main')
    require(git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==COMMIT,'actual remote after separate recovery push');stable()
    require(load(S)==control and pin(CLEAR)==clear_pin,'control/clearance unchanged before final truthful closure')
    receipt=dict(status='PASS_EXISTING_CHECKPOINT037_COMMIT_VERIFIED_AND_PUSH_COMPLETED_BY_SEPARATE_RECOVERY',UTC=utc(),actual_RECOVERY_recorder_PID=os.getpid(),original_operator_exit_code=1,original_outer_OS_PID=None,original_failure_is_not_reclassified=True,existing_commit=COMMIT,single_parent=BASE,owned_paths=sorted(owned),all244live_index_committed_full_bodies_modes_blobs_verified=True,correct_plan_filesystem_mode='0444',all41160nonowned_known_held_bodies_modes_preserved=True,whole_foreign_index_flags_and_noncontrol_dirty_diff_preserved=True,control_epoch_is_authorized_exception=True,exact_old_control=pin(OLD_CONTROL),no_staging_commit_merge_PR_service_action=True,only_unperformed_descendant_push_completed=True,main_equals_explicit_remote=True,index_empty=True,source=source,clearance=clear_pin,actual_capture_directory=str(actual),automatic_retry=False,DOI='10.5281/zenodo.23157237',tracker_range="'Math Puzzles'!A26:D26",estimates_percent=dict(publication_checkpoint=100,PR302_workflow=85))
    q=P/'checkpoint_302_publication_037_recovery_receipt.json'
    with q.open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
    (actual/'EXACT_PRE_CLOSURE_CONTROL.json').write_text(json.dumps(control,indent=2)+'\n')
    closed=copy.deepcopy(control);closed.update(utc=utc(),shared_git_writes_paused=False,descending_writer_window_released=True,descending_shared_git_writes_abstained=True,reason='PR302 publication checkpoint037 existing commit verified and sole unperformed push completed by separate recovery; original outer remains exit1; new exact authorization required for native integration',local_main_at_resume=COMMIT,remote_main_at_resume=COMMIT)
    closed['descending_302_publication_checkpoint_lease'].update(active=False,original_operator_exit_code=1,original_operator_completed_successfully=False,existing_commit_verified_and_pushed_by_separate_recovery=True)
    closed['descending_302_checkpoint037_push_recovery_lease'].update(active=False,completed=True,closed_UTC=utc(),actual_checkpoint=COMMIT)
    S.write_text(json.dumps(closed,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
