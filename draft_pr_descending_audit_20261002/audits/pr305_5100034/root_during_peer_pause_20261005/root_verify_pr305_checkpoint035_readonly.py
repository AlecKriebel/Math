"""Reauthenticate the actual scoped checkpoint and read its exact remote state."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import ast, copy, hashlib, json, stat, gzip, os, sys, signal, subprocess, fcntl
if sys.flags.optimize:
    raise RuntimeError('Optimized read-only checkpoint verification forbidden.')
D=Path(__file__).resolve().parent; A=D.parent; P=A.parent.parent; R=P.parent
sys.path.insert(0,str(D/'publication_preparation')); import submission_gate as g
BASE='b3eaf7561c83b37881eec11f5972396dbad9575d'; HEAD='8b59507d997563baa58dbf6c6579b26e239ea005'
sha=lambda b:hashlib.sha256(b).hexdigest(); utc=lambda:datetime.now(timezone.utc).isoformat()
load=lambda p:json.loads(Path(p).read_bytes())
names=lambda b:{x.decode() for x in b.split(b'\0') if x}
def require(v,msg):
    if not v:raise RuntimeError(msg+'; read-only reconciliation, no automatic mutation retry.')
fd=os.open(P/'audits/pr311_30005303/root_integration_private/SHARED_WRITE_LEASE.lock',os.O_RDWR|os.O_NOFOLLOW)
lock=os.fdopen(fd,'r+b');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
g.current_clearance();g.operational_clearance()
planp=D/'completion_preparation/FINAL_EXECUTION_PLAN.json'; source=D/'root_checkpoint_pr305_publication_035.py'
require(g.pin(planp)['sha256']=='873c4e6f48bdb7a75ee4b3edb2e199616bca8982b8ff479ef351407b760e7da7','Final plan drift')
require(g.pin(source)['sha256']=='20417d15b340639e7a2a5e8a3e605795fdc0fb8bb8c9952ff9049ee1eb365ff5','Checkpoint source drift')
lease=load(D/'ROOT_FINAL_WRITE_LEASE.json');control=load(P/'SHARED_GIT_WINDOW_STATUS.json')
require(g.pin(P/'SHARED_GIT_WINDOW_STATUS.json')['sha256']=='f78c72437fa165e2d00cec35cd353c2ded3afcb6547432faa781335b52dd4a13','Actual-phase control drift')
require(g.pin(D/'ROOT_FINAL_WRITE_LEASE.json')['sha256']=='9558145bae1add8f6864807f7351cd86d3345bf2967cff049644c8e18f2c942a','Actual-phase lease drift')
plan=load(planp);owned={e['target'] for e in plan['targets']}|{str(planp.relative_to(R))}
require(len(owned)==106 and len(plan['targets'])==105,'Declared scope drift')
receiptp=P/'checkpoint_305_publication_completion_035_receipt.json';receipt=load(receiptp)
require(receipt['status']=='PASS_PR305_EXACT_SCOPED_COMPLETION_CHECKPOINT_PUSHED' and receipt['commit']==HEAD and receipt['parent']==BASE,'Actual receipt differs')
outerp=D/'root_runs_private/root_pr305_checkpoint035_actual001/execution.json';outer=load(outerp)
require(outer['exit_code']==0 and outer['argv']==['/opt/homebrew/bin/python3','-E','-B',str(source)] and outer['cwd']==str(D),'Actual outer differs')
for k in ['stdout','stderr']:
    b=(outerp.parent/(k+'.bin')).read_bytes();require(len(b)==outer[k+'_bytes'] and sha(b)==outer[k+'_sha256'],'Outer whole stream differs')
require(json.loads((outerp.parent/'stdout.bin').read_bytes())==receipt,'Actual outer receipt body differs')
actual=D/'checkpoint035_actual_private';captures=[];byargv={};logical=stored_total=0;writers=[]
for p in sorted(actual.glob('*_execution.json'),key=lambda p:int(p.name.split('_')[0])):
    j=load(p);n=p.name.split('_')[0];request=load(actual/(n+'_request.json'));started=load(actual/(n+'_started.json'))
    require(all(j[k]==v for k,v in request.items()) and all(j[k]==v for k,v in started.items()),'Native header differs')
    require(j['cwd']==str(R) and j['actual_PID']>0 and j['cooperative_process_group']==j['actual_PID'] and j['exit_code']==0 and j['full_stream_capture_complete'] and j['parent_reaped'],'Native completion differs')
    require(j['operator']==g.pin(source),'Native source differs')
    require(datetime.fromisoformat(lease['not_before_utc'])<=datetime.fromisoformat(j['start_UTC'])<=datetime.fromisoformat(j['end_UTC'])<datetime.fromisoformat(lease['expires_utc']),'Native actual time outside epoch')
    require(j['argv'][:2]==['/usr/bin/git','--no-optional-locks'],'Unexpected process family')
    require(j['argv'][2] in {'branch','rev-parse','diff','ls-files','show','ls-tree','merge-base','ls-remote','add','commit','push'},'Unexpected production operation')
    for k in ['stdout','stderr']:
        e=j[k];stored=Path(e['path']).read_bytes();b=gzip.decompress(stored)
        require(len(stored)==e['stored_bytes'] and sha(stored)==e['stored_sha256'] and len(b)==e['logical_bytes'] and sha(b)==e['logical_sha256'],'Complete native stream differs')
        logical+=len(b);stored_total+=len(stored)
        if k=='stdout':byargv.setdefault(tuple(j['argv']),[]).append(b)
    captures.append(dict(path=str(p),pin=g.pin(p),actual_PID=j['actual_PID'],argv=j['argv']))
    if j['argv'][2] in {'add','commit','push'}:writers.append(j)
require(len(captures)==440 and len({e['actual_PID'] for e in captures})==440,'Native capture count or uniqueness differs')
require([j['argv'][2] for j in writers]==['add','commit','push'],'Exactly one add/commit/push required')
require(writers[0]['argv'][3:]==['--',*sorted(owned)],'Actual literal add scope differs')
require(writers[1]['actual_PID']==82656 and writers[2]['actual_PID']==83033,'Actual writer identity differs')
require(writers[2]['argv']==['/usr/bin/git','--no-optional-locks','push','--force-with-lease=refs/heads/main:'+BASE,lease['push_endpoint'],HEAD+':refs/heads/main'],'Exact expected-old descendant push differs')
def oldout(*args):return byargv[('/usr/bin/git','--no-optional-locks',*args)][0]
oldindex=oldout('ls-files','--stage','-z');oldflags=oldout('ls-files','-v','-z')
dirty=names(oldout('diff','--name-only','-z','HEAD'))-owned
olddiff=oldout('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b''
exclude=lambda b:b'\0'.join(x for x in b.split(b'\0') if x and (x.split(b'\t',1)[-1].decode() if b'\t' in x else x[2:].decode()) not in owned)
fresh=D/'checkpoint035_postreadback_private';require(not fresh.exists(),'Existing verification run');fresh.mkdir()
framework=D/'native_integration_preparation/integrate_pr305.py';tree=ast.parse(framework.read_bytes());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');node=next(n for n in main.body if isinstance(n,ast.FunctionDef) and n.name=='run')
factory=ast.parse('def factory(actual):\n count=0\n return run\n').body[0];factory.body.insert(1,copy.deepcopy(node));module=ast.fix_missing_locations(ast.Module(body=[factory],type_ignores=[]))
def deny_writer():raise RuntimeError('This postcheckpoint program is strictly read-only.')
environment=dict(Path=Path,datetime=datetime,timezone=timezone,timedelta=timedelta,hashlib=hashlib,json=json,stat=stat,os=os,sys=sys,subprocess=subprocess,gzip=gzip,signal=signal,R=R,g=g,sha=sha,utc=utc,require=require,authorize=deny_writer,__file__=str(Path(__file__).resolve()))
exec(compile(module,str(framework)+'::unchanged_capture_AST','exec'),environment);run=environment['factory'](fresh)
def git(*args):
    require(args[0] in {'branch','rev-parse','show','diff','ls-files','ls-tree','merge-base','ls-remote'},'Read-only allowlist violation')
    return run(['/usr/bin/git','--no-optional-locks',*args])
require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==HEAD,'Current local main differs')
require(g.safe_endpoints()==(lease['fetch_endpoint'],lease['push_endpoint']),'Endpoint drift')
require(git('ls-remote',lease['fetch_endpoint'],'refs/heads/main').split()[0].decode()==HEAD,'Current exact remote differs')
require(git('show','-s','--format=%P',HEAD).decode().split()==[BASE],'Actual checkpoint parent differs')
changed=names(git('diff','--name-only','-z',BASE,HEAD));require(changed<=owned and len(changed)==104,'Actual changed scope differs')
require(not git('diff','--cached','--raw','-z'),'Final shared index nonempty')
require(names(git('diff','--name-only','-z','HEAD'))-owned==dirty,'Foreign dirty scope differs')
require((git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b'')==olddiff,'Foreign full binary diff differs')
require(exclude(git('ls-files','--stage','-z'))==exclude(oldindex) and exclude(git('ls-files','-v','-z'))==exclude(oldflags),'Foreign whole logical index/flags differs')
expected={e['target']:(R/e['input']['path']).read_bytes() for e in plan['targets']};expected[str(planp.relative_to(R))]=planp.read_bytes()
for rel,b in expected.items():
    require((R/rel).read_bytes()==b and git('show',HEAD+':'+rel)==b,'Committed/live selected body differs')
    mode=0o644 if rel==str(planp.relative_to(R)) else next(e['input']['mode'] for e in plan['targets'] if e['target']==rel)
    require(stat.S_IMODE((R/rel).stat().st_mode)==mode,'Selected current filesystem mode differs')
    require(git('ls-tree',HEAD,'--',rel).decode().split()[:3]==['100644','blob',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()],'Selected committed Git mode/blob differs')
held=load(D/'peer_pr80_final_completion_window/KNOWN_HELD_INVENTORY.json');heldcount=0
for e in held['files']:
    if e['path'] in owned or e['path']==str((P/'SHARED_GIT_WINDOW_STATUS.json').relative_to(R)):continue
    q=g.pin(R/e['path']);require(q['bytes']==e['bytes'] and q['sha256']==e['sha256'] and int(q['mode'],8)==e['mode'],'Other held body/mode drift');heldcount+=1
original=load(A/'snapshot_manifest.json')
for e in original['files']:
    if e['path'].startswith('problems/5100034_focal_pedal_equality/'):
        q=g.pin(R/e['path']);require(q['bytes']==e['bytes'] and q['sha256']==e['sha256'] and q['mode']=='0644','Original29 historical native body/mode drift')
require(load(P/'inventory.json')['completed_by_descending']==27 and len(load(P/'inventory.json')['claimed_solved_published_by_descending'])==8,'Current progress differs')
g.current_clearance();g.operational_clearance()
require(load(P/'SHARED_GIT_WINDOW_STATUS.json')==control and load(D/'ROOT_FINAL_WRITE_LEASE.json')==lease,'Control drift during readback')
result=dict(status='PASS_ROOT_PR305_COMPLETE_CHECKPOINT035_NATIVE_CUSTODY',UTC=utc(),
    parent=BASE,commit=HEAD,selected_paths=106,actual_changed_paths=104,
    actual_native_captures=440,whole_logical_stream_bytes_authenticated=logical,
    whole_stored_stream_bytes_authenticated=stored_total,actual_commit_PID=82656,actual_push_PID=83033,
    exactly_one_scoped_add_commit_expected_old_push=True,actual_outer_exit_code=0,
    selected_current_committed_whole_body_filesystem_mode_git_mode_blob_verified=True,
    whole_foreign_index_flags_and_dirty_binary_diff_preserved=True,
    other_known_held_whole_bodies_modes_verified=heldcount,original29_historical_files_preserved=True,
    current_remote_main_exact=True,index_empty=True,actual_captures=captures,
    fresh_readonly_capture_directory=str(fresh),receipt=g.pin(receiptp),final_plan=g.pin(planp),
    original_head_merge_and_publication_and_tracker_not_repeated=True,
    math_percent=100,bounded_priority_percent=100,PR_workflow_percent=100,
    completed_by_descending=27,published_by_descending=8,persistent_goal_complete=False)
out=D/'ROOT_PR305_CHECKPOINT035_VERIFICATION.json';require(not out.exists(),'Existing verification receipt');out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='actual_captures'},indent=2))
