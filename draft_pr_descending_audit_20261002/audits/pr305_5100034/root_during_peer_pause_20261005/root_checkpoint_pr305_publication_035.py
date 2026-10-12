"""One exact scoped completion checkpoint; reviewed capture AST and fresh lease."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import ast,json,hashlib,stat,os,sys,subprocess,gzip,signal,copy
if sys.flags.optimize:raise RuntimeError('Optimized checkpoint forbidden')
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent;R=P.parent
sys.path.insert(0,str(D/'publication_preparation'));import submission_gate as g
SOURCE=Path(__file__).resolve();PLAN=D/'completion_preparation/FINAL_EXECUTION_PLAN.json'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
names=lambda b:{x.decode() for x in b.split(b'\0') if x}
def require(v,msg):
 if not v:raise RuntimeError(msg+'; preserve partial state and reconcile without repeating mutation.')
def main():
 lock=g.acquire();lease=g.window();control=load(P/'SHARED_GIT_WINDOW_STATUS.json');sourcepin=g.pin(SOURCE);planpin=g.pin(PLAN)
 require(lease.get('git_authorized') and lease.get('checkpoint_authorized') and lease['checkpoint_plan']==planpin and lease['checkpoint_operator']==sourcepin,'Exact checkpoint authority missing')
 require(load(D/'ROOT_PR305_POST_MERGE_CUSTODY.json')['status']=='PASS_ROOT_PR305_ACTUAL_MERGE_FULL_NATIVE_CUSTODY','Actual native custody missing')
 plan=load(PLAN);base=current=lease['main'];require(base=='b3eaf7561c83b37881eec11f5972396dbad9575d' and plan['actual_merge']==base and plan['unresolved_packet_findings']==0,'Checkpoint baseline or packet verdict changed')
 for absolute,e in plan['closed_packet_review_evidence'].items():require(g.pin(absolute)==e,'Packet evidence drift')
 targets=plan['targets'];owned={e['target'] for e in targets}|{str(PLAN.relative_to(R))};require(len(owned)==len(targets)+1,'Duplicated target')
 expected={e['target']:(R/e['input']['path']).read_bytes() for e in targets};expected[str(PLAN.relative_to(R))]=PLAN.read_bytes()
 actual=D/'checkpoint035_actual_private';require(not actual.exists(),'Previous checkpoint attempt exists');actual.mkdir()
 (actual/'ATTEMPT.json').write_text(json.dumps(dict(UTC=utc(),automatic_retry=False,source=sourcepin,plan=planpin,lease_token=lease['token']),indent=2)+'\n')
 # Compile the exact already-reviewed nested capture function without launching
 # the original merge or altering any of its function AST nodes.
 framework=D/'native_integration_preparation/integrate_pr305.py';require(g.pin(framework)['sha256']=='0ea02436c0ac1e0070169df466c34ba141c43291e16515b3fd1cce2135071897','Capture framework changed')
 tree=ast.parse(framework.read_bytes());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');node=next(n for n in fn.body if isinstance(n,ast.FunctionDef) and n.name=='run')
 factory=ast.parse('def factory(actual):\n count=0\n return run\n').body[0];factory.body.insert(1,copy.deepcopy(node));module=ast.fix_missing_locations(ast.Module(body=[factory],type_ignores=[]))
 environment=dict(Path=Path,datetime=datetime,timezone=timezone,timedelta=timedelta,hashlib=hashlib,json=json,stat=stat,os=os,sys=sys,subprocess=subprocess,gzip=gzip,signal=signal,R=R,g=g,sha=sha,utc=utc,require=require,__file__=str(SOURCE))
 exec(compile(module,str(framework)+'::unchanged_capture_AST','exec'),environment);run=environment['factory'](actual)
 def git(*args):return run(['/usr/bin/git','--no-optional-locks',*args])
 require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==base,'Initial local main differs')
 require(not git('diff','--cached','--raw','-z') and not (R/'.git/MERGE_HEAD').exists(),'Initial shared index busy')
 index=git('ls-files','--stage','-z');flags=git('ls-files','-v','-z');dirty=names(git('diff','--name-only','-z','HEAD'))-owned
 foreign={p:g.pin(R/p) for p in dirty};diff=git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b''
 exclude=lambda b:b'\0'.join(x for x in b.split(b'\0') if x and (x.split(b'\t',1)[-1].decode() if b'\t' in x else x[2:].decode()) not in owned)
 def stable():
  require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==current,'Current local main drift')
  require(names(git('diff','--name-only','-z','HEAD'))-owned==dirty and {p:g.pin(R/p) for p in dirty}==foreign,'Foreign dirty body/mode/scope drift')
  require((git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b'')==diff,'Foreign diff drift')
  require(exclude(git('ls-files','--stage','-z'))==exclude(index) and exclude(git('ls-files','-v','-z'))==exclude(flags),'Foreign full logical index/flags drift')
 def inputs():
  require(g.pin(SOURCE)==sourcepin and g.pin(PLAN)==planpin,'Checkpoint source/plan drift')
  for e in targets:
   p=R/e['input']['path'];q=g.pin(p);require(q['bytes']==e['input']['bytes'] and q['sha256']==e['input']['sha256'] and int(q['mode'],8)==e['input']['mode'],'Selected input drift')
 def authorize():
  g.current_clearance();g.operational_clearance();inputs()
  require(g.safe_endpoints()==(lease['fetch_endpoint'],lease['push_endpoint']),'Endpoint drift')
  stable()
  require(load(P/'SHARED_GIT_WINDOW_STATUS.json')==control and load(D/'ROOT_FINAL_WRITE_LEASE.json')==lease and not control['shared_git_writes_paused'],'Final authority/control drift')
  require(datetime.now(timezone.utc)+timedelta(seconds=75)<=datetime.fromisoformat(lease['expires_utc']),'Final checkpoint deadline insufficient')
 environment['authorize']=authorize
 inputs();require(git('ls-remote',lease['fetch_endpoint'],'refs/heads/main').split()[0].decode()==base,'Remote moved before writes')
 proposals=[e for e in targets if e['input']['path']!=e['target']]
 require(len(proposals)==5,'Only five current progress mappings are permitted')
 for e in proposals:
  p=R/e['target'];old=e['original_target'];require(not p.is_symlink(),'Proposal target symlink');require((not p.exists()) if old is None else (g.pin(p)['bytes']==old['bytes'] and g.pin(p)['sha256']==old['sha256'] and int(g.pin(p)['mode'],8)==old['mode']),'Current global proposal baseline drift')
 for e in proposals:
  p=R/e['target'];authorize();p.write_bytes(expected[e['target']]);authorize();p.chmod(e['input']['mode'])
 authorize();git('add','--',*sorted(owned));staged=names(git('diff','--cached','--name-only','-z'))
 require(staged<=owned and {e['target'] for e in proposals}<=staged,'Staged scope differs')
 stagedrows={}
 for line in git('ls-files','--stage','-z').split(b'\0'):
  if line:
   meta,p=line.split(b'\t',1);stagedrows[p.decode()]=meta.decode().split()
 for rel,b in expected.items():
  require(git('show',':'+rel)==b and stagedrows[rel]==['100644',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),'0'],'Selected staged full body/mode/blob differs')
 authorize();git('commit','-m','Record completed PR305 focal-pedal review and published preprint');current=git('rev-parse','HEAD').decode().strip()
 require(git('show','-s','--format=%P',current).decode().split()==[base] and names(git('diff','--name-only','-z',base,current))==staged,'Checkpoint parents/scope differs')
 for rel,b in expected.items():
  mode=0o644 if rel==str(PLAN.relative_to(R)) else next(e['input']['mode'] for e in targets if e['target']==rel)
  require(git('show',current+':'+rel)==b and (R/rel).read_bytes()==b and stat.S_IMODE((R/rel).stat().st_mode)==mode,'Committed/current whole body or filesystem mode differs')
  require(git('ls-tree',current,'--',rel).decode().split()[:3]==['100644','blob',hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()],'Committed mode/blob differs')
 authorize();git('merge-base','--is-ancestor',base,current);require(git('ls-remote',lease['fetch_endpoint'],'refs/heads/main').split()[0].decode()==base,'Remote moved before exact descendant push')
 git('push','--force-with-lease=refs/heads/main:'+base,lease['push_endpoint'],current+':refs/heads/main')
 require(git('ls-remote',lease['fetch_endpoint'],'refs/heads/main').split()[0].decode()==current,'Final exact remote differs');stable();inputs();g.current_clearance();g.operational_clearance();require(not git('diff','--cached','--raw','-z'),'Final index not empty')
 receipt=dict(UTC=utc(),status='PASS_PR305_EXACT_SCOPED_COMPLETION_CHECKPOINT_PUSHED',parent=base,commit=current,allowlist_paths=len(owned),actual_changed_paths=len(staged),selected_live_staged_committed_full_body_mode_blob_verified=True,whole_foreign_logical_index_flags_dirty_bodies_modes_diff_preserved=True,explicit_expected_old_descendant_fast_forward_push=True,index_empty=True,remote_main_exact=True,math_percent=100,bounded_priority_percent=100,PR_workflow_percent=100,completed_by_descending=27,published_by_descending=8,DOI='10.5281/zenodo.23149775',tracker_range="'Math Puzzles'!A24:D24",no_duplicate_publication_or_tracker_action=True,persistent_goal_complete=False,plan=planpin,source=sourcepin,actual_capture_directory=str(actual),postcommit_receipt_intentionally_excluded_from_own_commit=True)
 out=P/'checkpoint_305_publication_completion_035_receipt.json';require(not out.exists(),'Existing postcommit receipt');out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
