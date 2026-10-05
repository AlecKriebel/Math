"""Checkpoint PR301 verified mathematics and qualified priority findings; no native PR or service action.

All executable project input and closed-review roles are authenticated locally
before the unchanged capture function is compiled. Preserve uncertain outcomes.
"""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import ast,copy,fcntl,gzip,hashlib,json,os,signal,stat,subprocess,sys,types
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';W=Path(__file__).parent;A=W.parent
PLAN=W/'CONTENT_PLAN.json';CLEAR=W/'ROOT_CHECKPOINT040_CLEARANCE.json';S=P/'SHARED_GIT_WINDOW_STATUS.json'
FRAME=P/'audits/pr305_5100034/root_during_peer_pause_20261005/native_integration_preparation/integrate_pr305.py'
ENDPOINT='https://github.com/AlecKriebel/Math.git';utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(Path(p).read_bytes())
def require(v,m):
    if not v:raise RuntimeError(m+'; preserve actual partial state and reconcile read-only; no automatic mutation retry')
def pin(p):
    p=Path(p);require(p.is_file() and not p.is_symlink(),'literal file');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def names(b):return {x.decode() for x in b.split(b'\0') if x}
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def main():
    require(not sys.flags.optimize,'optimization forbidden');lock=(W/'ACTUAL_WRITER.lock').open('a+b');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    plan=load(PLAN);clear=load(CLEAR);control=load(S);lease=control['descending_301_partial_checkpoint040_lease'];source=pin(__file__);planpin=pin(PLAN)
    require(clear['status']=='PASS_EXACT_PR301_PARTIAL_RESEARCH_CHECKPOINT040' and clear['unresolved_issues']==[] and clear['checkpoint_only_authorized'] is True and pin(CLEAR)['mode']==0o444,'genuine frozen ROOT checkpoint clearance')
    require(clear['source']==source and clear['plan']==planpin and source['mode']==planpin['mode']==0o444,'exact immutable source/plan')
    roles=[FRAME,A/'ROOT_CORRECTED_MATHEMATICAL_ACCEPTANCE.json',A/'ROOT_PRIORITY_ADJUDICATION.json',A/'snapshot_manifest.json',A/'ROOT_FRESH_PRIORITY_ADVERSARY_REPRODUCTION.json',A/'checkpoint_039_preparation/KNOWN_HELD_BASELINE.json']
    require(type(plan['bound_inputs']) is list and len(plan['bound_inputs'])==len(roles) and {x['path'] for x in plan['bound_inputs']}=={str(p) for p in roles},'all six nonvacuous prerequisite roles')
    for x in plan['bound_inputs']:require(pin(x['path'])==x,'every complete prerequisite before project AST')
    review=Path(clear['review_namespace']);require(review==A/'checkpoint040_adversary_01','fresh independent checkpoint review')
    closed=clear['closed_review_pins'];require(set(closed)=={'REPORT.md','DERIVATION.md','READ_SCOPE_LEDGER.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'},'six exact frozen review roles')
    for name,x in closed.items():require(pin(review/name)==x and x['mode']==0o444,'exact closed checkpoint review')
    require(load(review/'VERDICT.json')['unresolved_issues']==[] and load(review/'VERDICT.json')['execution_authority_granted'] is False,'review clear and nonauthorizing')
    require(not control['shared_git_writes_paused'] and not control['ascending_pr85_publication_integration_window_granted'] and lease['active'] and lease['source']==source and lease['plan']==planpin and lease['clearance']==pin(CLEAR) and lease['endpoint']==ENDPOINT,'exact active checkpoint-only lease')
    require(load(roles[1])['status']=='ROOT_ACCEPTS_PR301_CORRECTED_V02_MATHEMATICS_ONLY' and load(roles[2])['status']=='PASS_PRIORITY_ADJUDICATION_BROAD_NEW_RESOLUTION_DEFEATED_CREDITED_CORRECTION_REQUIRED' and load(roles[4])['status']=='PASS_FRESH_PRIORITY_ADVERSARY_CUSTODY_AND_EXACT_CONTROL_REPRODUCTION','current accepted mathematics, qualified priority adjudication and fresh reproduced priority adversary')
    require(load(roles[3])['head']=='125d90fa3f5a4f90b813fec7a7c0f1918914d885' and load(roles[3])['original_submitted_status']=='claimed_solved','exact eligible original')
    require(plan['mathematics_accepted'] and plan['priority_adjudication_accepted'] and plan['no_completion_or_publication_count_increment'] and plan['no_PR_or_preprint_or_Zenodo_or_tracker_action'],'credited scientific checkpoint; correction review/publication pending')
    base=current=plan['starting_main'];require(base=='73300d9223ca6175983c78cb2370f99ffdd4b59c' and lease['starting_main']==base,'exact completed prior epoch')
    targets=plan['targets'];owned=set(plan['allowed_paths']);require(type(targets) is list and targets and len(targets)==len({x['target'] for x in targets}) and len(owned)==len(plan['allowed_paths']) and owned=={x['target'] for x in targets}|{str(PLAN.relative_to(R))} and lease['allowed_paths']==plan['allowed_paths'],'exact nonempty literal checkpoint domain')
    require(all(not Path(x['target']).is_absolute() and '..' not in Path(x['target']).parts and (R/x['target']).is_relative_to(P) for x in targets),'only descending audit namespace')
    def inputs():
        require(pin(__file__)==source and pin(PLAN)==planpin and load(CLEAR)==clear,'current exact source/plan/ROOT approval')
        for x in plan['bound_inputs']:require(pin(x['path'])==x,'all six actual prerequisite body/mode pins')
        for x in targets:require(pin(x['input']['path'])==x['input'],'each selected complete input')
    inputs();expected={x['target']:Path(x['input']['path']).read_bytes() for x in targets};expected[str(PLAN.relative_to(R))]=PLAN.read_bytes();modes={x['target']:x['input']['mode'] for x in targets};modes[str(PLAN.relative_to(R))]=0o444
    actual=W/'actual_checkpoint040';require(not actual.exists(),'previous/uncertain checkpoint attempt');actual.mkdir();archives=[]
    for i,p in enumerate(dict.fromkeys([Path(__file__),PLAN,CLEAR,S,*roles,*[Path(x['input']['path']) for x in targets]])):
        b=p.read_bytes();q=actual/(str(i)+'_'+p.name+'.source.gz');q.write_bytes(gzip.compress(b,mtime=0));require(gzip.decompress(q.read_bytes())==b,'complete prelaunch body');archives.append(dict(input=pin(p),archive=pin(q)))
    (actual/'ATTEMPT.json').write_text(json.dumps(dict(UTC=utc(),actual_ROOT_recorder_PID=os.getpid(),source=source,plan=planpin,full_inputs=archives,automatic_retry=False,outcome='STARTED_UNCERTAIN_UNTIL_FINAL_RECEIPT'),indent=2)+'\n')
    body=FRAME.read_bytes();require(sha(body)=='0ea02436c0ac1e0070169df466c34ba141c43291e16515b3fd1cce2135071897','exact capture framework before compilation');tree=ast.parse(body);mainfn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main');node=next(x for x in mainfn.body if isinstance(x,ast.FunctionDef) and x.name=='run');factory=ast.parse('def factory(actual):\n count=0\n return run\n').body[0];factory.body.insert(1,copy.deepcopy(node));module=ast.fix_missing_locations(ast.Module(body=[factory],type_ignores=[]))
    env=dict(Path=Path,datetime=datetime,timezone=timezone,timedelta=timedelta,hashlib=hashlib,json=json,stat=stat,os=os,sys=sys,subprocess=subprocess,gzip=gzip,signal=signal,R=R,g=types.SimpleNamespace(pin=pin),sha=sha,utc=utc,require=require,__file__=str(Path(__file__).resolve()));exec(compile(module,str(FRAME)+'::exact_capture_only','exec'),env);run=env['factory'](actual)
    def git(*args,ok=(0,)):return run(['/usr/bin/git','--no-optional-locks',*args],ok)
    require(not git('config','--get-regexp','^url[.]',ok=(0,1)),'URL mappings outside endpoint scope')
    require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==base and git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==base,'exact main/remote epoch')
    require(not git('diff','--cached','--raw','-z') and not (R/'.git/MERGE_HEAD').exists() and not (R/'.git/index.lock').exists(),'busy initial index/merge')
    index=git('ls-files','--stage','-z');flags=git('ls-files','-v','-z');dirty=names(git('diff','--name-only','-z','HEAD'))-owned;foreign={x:pin(R/x) for x in dirty};diff=git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b''
    def exclude(b,stage):return [x for x in b.split(b'\0') if x and (x.split(b'\t',1)[1].decode() if stage else x[2:].decode()) not in owned]
    heldrows=load(roles[-1])['files'];require(len(heldrows)==len({x['path'] for x in heldrows})==41253,'complete known-held path baseline')
    held=[x for x in heldrows if str(Path(x['path']).relative_to(R)) not in owned and x['path']!=str(S)]
    def held_stable():
        for x in held:require(pin(x['path'])==x,'every complete nonowned held body/mode')
    def stable():
        require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==current,'current checkpoint epoch')
        require(names(git('diff','--name-only','-z','HEAD'))-owned==dirty and {x:pin(R/x) for x in dirty}==foreign and (git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b'')==diff,'whole foreign dirty bodies/modes/diff')
        require(exclude(git('ls-files','--stage','-z'),True)==exclude(index,True) and exclude(git('ls-files','-v','-z'),False)==exclude(flags,False),'entire foreign index/flags')
    def authorize():
        inputs();require(load(S)==control and pin(CLEAR)==lease['clearance'],'exact current control/clearance');stable()
        require(datetime.now(timezone.utc)+timedelta(seconds=75)<=datetime.fromisoformat(lease['expires_UTC']),'checkpoint deadline buffer')
        require(load(S)==control and load(CLEAR)==clear,'final current control/approval')
    env['authorize']=authorize;held_stable()
    for x in targets:
        if x['input']['path']==str(R/x['target']):continue
        p=R/x['target'];old=x['original_target'];require((not p.exists() and not p.is_symlink()) if old is None else pin(p)==old,'full old prepared target baseline')
    for x in targets:
        if x['input']['path']==str(R/x['target']):continue
        p=R/x['target'];authorize();p.write_bytes(expected[x['target']]);p.chmod(modes[x['target']])
    authorize();git('add','--',*sorted(owned));staged=names(git('diff','--cached','--name-only','-z'));require(staged and staged<=owned,'nonempty exact staged subset')
    for rel,b in expected.items():require(git('show',':'+rel)==b and git('ls-files','--stage','--',rel).decode().split()[:3]==['100644',blob(b),'0'],'all full staged bodies/modes/blobs')
    held_stable();authorize();git('commit','-m','Checkpoint PR301 verified mathematics and qualified prior-algorithm priority finding');current=git('rev-parse','HEAD').decode().strip()
    require(git('show','-s','--format=%P',current).decode().split()==[base] and names(git('diff','--name-only','-z',base,current))==staged,'actual single-parent checkpoint domain')
    for rel,b in expected.items():require(git('show',current+':'+rel)==b and git('ls-tree',current,'--',rel).decode().split()[:3]==['100644','blob',blob(b)] and (R/rel).read_bytes()==b and pin(R/rel)['mode']==modes[rel],'every committed/live full body and correct filesystem mode including frozen plan0444')
    held_stable();authorize();git('merge-base','--is-ancestor',base,current);require(git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==base,'last expected-old remote')
    git('push','--force-with-lease=refs/heads/main:'+base,ENDPOINT,current+':refs/heads/main');require(git('ls-remote',ENDPOINT,'refs/heads/main').split()[0].decode()==current,'actual remote checkpoint readback');stable();held_stable();inputs()
    for rel,b in expected.items():require((R/rel).read_bytes()==b and pin(R/rel)['mode']==modes[rel] and git('show',':'+rel)==b and git('ls-files','--stage','--',rel).decode().split()[:3]==['100644',blob(b),'0'] and git('show',current+':'+rel)==b and git('ls-tree',current,'--',rel).decode().split()[:3]==['100644','blob',blob(b)],'final postpush every owned live/index/commit complete body/mode/blob')
    require(not git('diff','--cached','--raw','-z') and load(S)==control,'final empty index/control')
    receipt=dict(status='PASS_PR301_PARTIAL_RESEARCH_CHECKPOINT040_PUSHED',UTC=utc(),actual_ROOT_recorder_PID=os.getpid(),parent=base,commit=current,source=source,plan=planpin,owned_paths=sorted(owned),actual_changed_paths=sorted(staged),all_selected_live_index_committed_full_bodies_modes_blobs_verified=True,correct_plan_filesystem_mode='0444',whole_foreign_index_flags_dirty_bodies_modes_diff_preserved=True,known_nonowned_held_count=len(held),all_known_nonowned_held_complete_bodies_modes_preserved=True,main_equals_explicit_remote=True,index_empty=True,no_native_PR_or_DOI_or_tracker_action=True,automatic_retry=False,actual_capture_directory=str(actual),estimates_percent=dict(PR301_mathematical_review=100,PR301_bounded_priority_audit=100,PR301_workflow=60,checkpoint040=100),postcommit_receipt_intentionally_outside_own_commit=True)
    out=P/'checkpoint_301_partial_040_receipt.json'
    with out.open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
    (actual/'EXACT_PRE_CLOSURE_CONTROL.json').write_text(json.dumps(control,indent=2)+'\n');closed=copy.deepcopy(control);closed.update(utc=utc(),shared_git_writes_paused=False,descending_writer_window_released=True,descending_shared_git_writes_abstained=True,reason='PR301 mathematics and qualified priority checkpoint040 pushed and read back; corrected packet review/publication pending; fresh exact authorization required for any new write',local_main_at_resume=current,remote_main_at_resume=current)
    closed['descending_301_partial_checkpoint040_lease'].update(active=False,completed=True,closed_UTC=utc(),actual_checkpoint=current);S.write_text(json.dumps(closed,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
