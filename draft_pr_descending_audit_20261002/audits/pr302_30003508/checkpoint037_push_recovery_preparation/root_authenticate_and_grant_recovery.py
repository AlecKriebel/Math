"""ROOT read-only authentication and fresh one-push authorization; no Git writer."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import gzip,hashlib,json,os,signal,stat,subprocess,sys,uuid
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';W=Path(__file__).parent;A=W.parent
V=A/'checkpoint037_push_recovery_adversary_02';B=A/'publication_checkpoint_037_actual_private';S=P/'SHARED_GIT_WINDOW_STATUS.json'
PLAN=A/'publication_checkpoint_037_preparation/CONTENT_PLAN.json';OLD=A/'root_checkpoint_publication_037.py'
FRAME=P/'audits/pr305_5100034/root_during_peer_pause_20261005/native_integration_preparation/integrate_pr305.py'
BASE='2669042ac964d5710972af552df141f7934588af';COMMIT='0a49d5e66a0fb9d4f78c7f3a7f3b30cd77196567';ENDPOINT='https://github.com/AlecKriebel/Math.git'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(Path(p).read_bytes())
def require(v,m):
    if not v:raise RuntimeError(m)
def pin(p):
    p=Path(p);require(p.is_file() and not p.is_symlink(),'literal file');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def body(x):
    p=Path(x['path']);q=pin(p);require(q['bytes']==x['bytes'] and q['sha256']==x['sha256'],'complete body');return p.read_bytes()
def names(b):return {x.decode() for x in b.split(b'\0') if x}
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def native(p):
    x=load(p);q=load(p.parent/'request.json');started=load(p.parent/'started.json')
    require(all(x[k]==v for k,v in q.items()) and all(x[k]==v for k,v in started.items()),'review request/start/completion agreement')
    require(type(x['actual_PID']) is int and x['actual_PID']>0 and x['parent_reaped'] and x['full_capture'],'review genuine captured PID/full stream')
    a=x.get('start_UTC',x.get('started_UTC'));require(datetime.fromisoformat(a)<=datetime.fromisoformat(x['end_UTC']),'review actual interval')
    for n in ['stdout','stderr']:
        z=body(dict(path=x[n]['path'],bytes=x[n]['stored_bytes'],sha256=x[n]['stored_sha256']));b=gzip.decompress(z)
        require(len(b)==x[n]['logical_bytes'] and sha(b)==x[n]['logical_sha256'],'full review logical stream')
    if 'reviewer' in x:
        b=gzip.decompress((p.parent/'source.py.gz').read_bytes());require(len(b)==x['reviewer']['bytes'] and sha(b)==x['reviewer']['sha256'],'full review prelaunch source')
    else:
        require(sha((V/'test_config_normalization.py').read_bytes())==x['source_sha256'] and x['fixture_only'],'literal isolated native config fixture')
    return dict(receipt=pin(p),actual_PID=x['actual_PID'],exit_code=x['exit_code'],argv=x['argv'])
def main():
    require(not sys.flags.optimize,'optimization');oldcontrol=S.read_bytes();require(oldcontrol==(W/'EXACT_OLD_CHECKPOINT_CONTROL.json').read_bytes(),'old control epoch')
    controls=load(S);require(not controls['shared_git_writes_paused'] and not controls['ascending_pr85_publication_integration_window_granted'],'no peer grant or pause')
    clearpath=W/'ROOT_RECOVERY_CLEARANCE.json';require(not clearpath.exists(),'no prior authorization')
    roles=['REPORT.md','DERIVATION.md','READ_SCOPE_LEDGER.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'];closed={n:pin(V/n) for n in roles}
    require(all(x['mode']==0o444 for x in closed.values()),'all six frozen closed review roles')
    require(closed['OUTPUT_MANIFEST.json']['sha256']=='6d4b4d2057dfc125e3c7cc6cd872d96929dac396fdb6ec998f86eed94e14f8cc' and closed['CLOSURE_SEAL.json']['sha256']=='385cce5e9bcee3e7289454134806d7d274852b9be5fa66d05427ae820364eead','exact announced fresh closure')
    manifest=load(V/'OUTPUT_MANIFEST.json');seal=load(V/'CLOSURE_SEAL.json');rows=manifest['files']
    actual={str(p.relative_to(V)) for p in V.rglob('*') if p.is_file()};listed={x.get('relative_path',str(Path(x['path']).relative_to(V))) for x in rows}
    require(len(listed)==len(rows) and actual==listed|{'OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'},'whole noncircular closed review inventory')
    for x in rows:require(pin(x['path'])=={k:x[k] for k in ['path','bytes','sha256','mode']} and x['mode']==0o444,'every closed review complete body/mode')
    require(all(stat.S_IMODE(p.stat().st_mode)==0o555 for p in [V,*[q for q in V.rglob('*') if q.is_dir()]]),'every closed review directory frozen')
    require(seal['output_manifest']==closed['OUTPUT_MANIFEST.json'],'seal exact manifest')
    verdict=load(V/'VERDICT.json');require(verdict['unresolved_issues']==verdict['mandatory_issues']==verdict['nonmandatory_issues']==[] and not verdict['execution_authority_granted'],'genuine closed clear independent disposition')
    require(verdict['candidate_source_sha256']=='a8ad4e0a9e42c8b9a6619eabd55b65b8bb969f25de8376a5a3f5aa66fca05fbc' and verdict['original_operator_exit_code']==1 and verdict['original_outer_OS_PID'] is None,'exact source/truthful failed boundary')
    source=pin(W/'push_verified_existing_commit.py');require(source['sha256']==verdict['candidate_source_sha256'] and source['mode']==0o444,'concrete recovery exact source')
    reviewcaptures=[native(p) for p in sorted(V.rglob('execution.json')) if 'synthetic_guard_fixtures' not in str(p)]
    require(len(reviewcaptures)==17 and sum(x['exit_code']==1 for x in reviewcaptures)==1 and all(x['exit_code'] in (0,1) for x in reviewcaptures),'complete actual reviewer native child history')
    cases=load(V/'ISOLATED_GUARD_RESULTS.json');require(cases['candidate']==source and cases['synthetic_approval_fixtures_not_ROOT_authority'] and len(cases['cases'])==41 and all(x['accepted']==x['positive_expected'] and x['synthetic_fixture'] and x['actual_Git_PR_service_calls']==0 for x in cases['cases']),'all41 exact guard cases with qualified synthetic scope')
    basis=load(W/'PRESERVED_FAILED_BASIS.json');require(len(basis['files'])==4289 and basis['original_outer_exit_code']==1 and basis['unperformed_push'],'truthful preserved complete failure')
    require({x['path'] for x in basis['files']}=={str(p) for p in B.rglob('*') if p.is_file()},'whole failed evidence domain')
    for x in basis['files']:require(pin(x['path'])==x,'every4289complete failed evidence body/mode')
    records=[]
    for i in range(1,809):
        x=load(B/f'{i}_execution.json');q=load(B/f'{i}_request.json');start=load(B/f'{i}_started.json')
        require(all(x[k]==v for k,v in q.items()) and all(x[k]==v for k,v in start.items()) and x['actual_PID']==x['cooperative_process_group'] and x['actual_PID']>0 and x['full_stream_capture_complete'] and x['parent_reaped'] and not x['timeout_cleanup_required'],'full808 original native request/start/completion')
        require(x['operator']['sha256']==pin(OLD)['sha256'] and x['exit_code']==(1 if i==1 else 0) and datetime.fromisoformat(x['start_UTC'])<=datetime.fromisoformat(x['end_UTC']),'original exact source/outcome/interval')
        streams={}
        for n in ['stdout','stderr']:
            z=body(dict(path=x[n]['path'],bytes=x[n]['stored_bytes'],sha256=x[n]['stored_sha256']));b=gzip.decompress(z);require(len(b)==x[n]['logical_bytes'] and sha(b)==x[n]['logical_sha256'],'entire original stored/logical stream');streams[n]=b
        require(not streams['stderr'] and x['argv'][2]!='push','no old push and complete benign children')
        if i==1:require(not streams['stdout'] and x['argv'][2]=='config','permitted empty config exit1')
        records.append((x,streams))
    require(records[310][0]['actual_PID']==22132 and records[310][0]['argv'][2]=='commit','genuine successful original commit')
    plan=load(PLAN);owned=set(plan['allowed_paths']);require(len(owned)==244 and len(plan['targets'])==243,'exact244scope')
    expected={x['target']:(R/x['input']['path']).read_bytes() for x in plan['targets']};expected[str(PLAN.relative_to(R))]=PLAN.read_bytes()
    modes={x['target']:int(x['input']['mode'],8) for x in plan['targets']};modes[str(PLAN.relative_to(R))]=0o444
    archives=load(V/'INDEPENDENT_FAILED_CUSTODY_AND_NATIVE_READBACK.json')['full_original_prelaunch_archives'];require(len(archives)==245,'all245complete original prelaunch bodies')
    for x in archives:require(gzip.decompress(body(x['archive']))==body(x['logical']),'complete archived original input')
    require(gzip.decompress((B/'FRAMEWORK_FULL_PRELAUNCH.py.gz').read_bytes())==FRAME.read_bytes() and sha(FRAME.read_bytes())=='0ea02436c0ac1e0070169df466c34ba141c43291e16515b3fd1cce2135071897','whole source-pinned capture framework')
    cap=W/'root_fresh_grant_readonly';cap.mkdir(exist_ok=False)
    def run(label,argv,input=None,ok=(0,)):
        q=cap/label;q.mkdir();request=dict(argv=argv,cwd=str(R),requested_UTC=utc(),source=pin(__file__),automatic_retry=False)
        if input is not None:(q/'stdin.gz').write_bytes(gzip.compress(input,mtime=0));request['stdin']=dict(bytes=len(input),sha256=sha(input),stored=pin(q/'stdin.gz'))
        (q/'request.json').write_text(json.dumps(request,indent=2)+'\n');(q/'source.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0))
        proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);start=dict(**request,actual_PID=proc.pid,start_UTC=utc());(q/'started.json').write_text(json.dumps(start,indent=2)+'\n')
        timeout=False
        try:out,err=proc.communicate(input,timeout=55)
        except subprocess.TimeoutExpired:timeout=True;os.killpg(proc.pid,signal.SIGKILL);out,err=proc.communicate(timeout=5)
        streams={}
        for n,b in [('stdout',out),('stderr',err)]:
            f=q/(n+'.gz');f.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(f),logical_bytes=len(b),logical_sha256=sha(b))
        (q/'execution.json').write_text(json.dumps(dict(**start,end_UTC=utc(),exit_code=proc.returncode,timed_out=timeout,parent_reaped=True,streams=streams),indent=2)+'\n');require(not timeout and proc.returncode in ok,'ROOT fresh read-only command failure');return out
    def git(label,*args,**kw):return run(label,['/usr/bin/git','--no-optional-locks',*args],**kw)
    require(not git('url','config','--get-regexp','^url[.]',ok=(0,1)),'URL configuration scope')
    require(git('branch','branch','--show-current')==b'main\n' and git('head','rev-parse','HEAD').decode().strip()==COMMIT and git('remote','ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==BASE,'exact fresh main/remote')
    require(git('parent','show','-s','--format=%P',COMMIT).decode().split()==[BASE] and names(git('changed','diff','--name-only','-z',BASE,COMMIT))==owned,'single parent exact244changed')
    require(not git('staged','diff','--cached','--raw','-z') and not (R/'.git/MERGE_HEAD').exists() and not (R/'.git/index.lock').exists(),'empty index/no incomplete merge')
    index=git('index','ls-files','--stage','-z');flags=git('flags','ls-files','-v','-z');tree=git('tree','ls-tree','-r','-z',COMMIT,'--',*sorted(owned))
    entries={x.split(b'\t',1)[1].decode():x.split(b'\t',1)[0].decode().split() for x in index.split(b'\0') if x};trees={x.split(b'\t',1)[1].decode():x.split(b'\t',1)[0].decode().split() for x in tree.split(b'\0') if x}
    require(set(trees)==owned,'all244committed table domain')
    for rel,b in expected.items():require((R/rel).read_bytes()==b and pin(R/rel)['mode']==modes[rel] and entries[rel]==['100644',blob(b),'0'] and trees[rel]==['100644','blob',blob(b)],'all244live/index/committed mode/blob pins')
    queries=[f'{prefix}:{p}' for prefix in ['',COMMIT] for p in sorted(owned)];batch=git('full_blobs','cat-file','--batch',input=('\n'.join(queries)+'\n').encode());offset=0
    for query in queries:
        end=batch.index(b'\n',offset);header=batch[offset:end].decode().split();require(len(header)==3 and header[1]=='blob','full batch header');n=int(header[2]);b=batch[end+1:end+1+n];offset=end+n+2
        require(b==expected[query.split(':',1)[1]] and header[0]==blob(b) and batch[end+n+1:end+n+2]==b'\n','every488whole blob');
    require(offset==len(batch),'no full blob trailing bytes')
    def baseline(args):return next(b['stdout'] for x,b in records if x['argv']==['/usr/bin/git','--no-optional-locks',*args])
    def exclude(b,stage):return [x for x in b.split(b'\0') if x and (x.split(b'\t',1)[1].decode() if stage else x[2:].decode()) not in owned]
    require(exclude(index,True)==exclude(baseline(['ls-files','--stage','-z']),True) and exclude(flags,False)==exclude(baseline(['ls-files','-v','-z']),False),'whole foreign index/flags')
    dirty=names(git('dirty','diff','--name-only','-z','HEAD'));olddirty=names(baseline(['diff','--name-only','-z','HEAD']))-owned;require(dirty-owned==olddirty,'whole old foreign dirty scope before new lease')
    require(git('foreign_diff','diff','--binary','HEAD','--',*sorted(olddirty))==baseline(['diff','--binary','HEAD','--',*sorted(olddirty)]),'all old foreign binary diff before new lease')
    held=load(B/'KNOWN_HELD_AT_ACTUAL_START.json')['files'];require(len(held)==41160,'exact41160nonownedheld')
    for rel,x in held.items():require(pin(R/rel)==dict(path=x['path'],bytes=x['bytes'],sha256=x['sha256'],mode=int(x['mode'],8)),'all41160nonownedfullbodies/modes')
    processes=run('processes',['/bin/ps','-axo','pid=,ppid=,pgid=,command=']);require(not any(b'root_checkpoint_publication_037.py' in line or b'push_verified_existing_commit.py' in line for line in processes.splitlines()),'no surviving original/recovery writer')
    require(S.read_bytes()==oldcontrol,'control held throughout ROOT reconciliation')
    inputs=[PLAN,OLD,W/'PRESERVED_FAILED_BASIS.json',W/'EXACT_OLD_CHECKPOINT_CONTROL.json',FRAME,A/'ROOT_CHECKPOINT037_FAILED_BOUNDARY.json',A/'ROOT_ACTUAL_PUBLICATION_AND_TRACKER_ACCEPTANCE.json']
    stamp=utc();decision=dict(status='PASS_EXISTING_CHECKPOINT037_VERIFIED_PUSH_ONLY_RECOVERY',UTC=stamp,actual_ROOT_recorder_PID=os.getpid(),ROOT_source=pin(__file__),operator=source,existing_commit=COMMIT,expected_old_remote=BASE,original_operator_exit_code=1,original_outer_OS_PID=None,original_failure_reclassified=False,unresolved_issues=[],push_only_authorized=True,bound_inputs=[pin(p) for p in inputs],review_namespace=str(V),closed_review_pins=closed,full_closed_review_files_authenticated=len(rows)+2,actual_review_native_captures_authenticated=reviewcaptures,exact_AST_fixture_cases=41,all4289failed_custody_bodies_modes_authenticated=True,all808original_native_captures_authenticated=True,original_zero_exit_children=807,original_allowed_empty_config_nonzero_children=1,all245original_prelaunch_full_bodies_authenticated=True,all244live_index_commit_full_bodies_modes_blobs_verified=True,known_nonowned_held_complete_bodies_modes_preserved=41160,whole_foreign_index_flags_dirty_diff_preserved_before_control_epoch=True,no_staging_commit_merge_fetch_PR_or_service_authority=True,old_failed_checkpoint_lease_deactivated_in_new_epoch=True,peer85_native_acceptance_checkpoint_remain_PENDING=True,estimates_percent=dict(PR302_workflow=85,recovery_review=100,recovery_push=0))
    with clearpath.open('x') as f:json.dump(decision,f,indent=2);f.write('\n')
    clearpath.chmod(0o444);(W/'EXACT_PRE_RECOVERY_GRANT_CONTROL.json').write_bytes(oldcontrol)
    lease=dict(token=str(uuid.uuid4()),active=True,scope='Only existing verified checkpoint037 commit push and truthful closure',operator=source,clearance=pin(clearpath),endpoint=ENDPOINT,existing_commit=COMMIT,expected_old_remote=BASE,push_only=True,created_UTC=stamp,expires_UTC=(datetime.now(timezone.utc)+timedelta(minutes=18)).isoformat())
    controls['descending_302_publication_checkpoint_lease'].update(active=False,original_operator_exit_code=1,original_operator_completed_successfully=False,unperformed_push_pending_separate_reviewed_recovery=True)
    controls.update(utc=stamp,shared_git_writes_paused=False,descending_writer_window_released=False,descending_shared_git_writes_abstained=False,reason='ROOT exact fresh reviewed existing-commit checkpoint037 push-only recovery; no native PR or service scope')
    controls['descending_302_checkpoint037_push_recovery_lease']=lease;require(S.read_bytes()==oldcontrol,'exact live old epoch before scope grant');S.write_text(json.dumps(controls,indent=2)+'\n')
    print(json.dumps(dict(status=decision['status'],actual_ROOT_recorder_PID=os.getpid(),closed_review_files=decision['full_closed_review_files_authenticated'],token=lease['token'],expires_UTC=lease['expires_UTC'],clearance=pin(clearpath),control=pin(S)),indent=2))
if __name__=='__main__':main()
