"""ROOT full closed native review custody and exact original-head scope grant."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import gzip,hashlib,json,os,stat,subprocess,sys,uuid
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';N=Path(__file__).parent;A=N.parent;V=A/'native_integration_adversary_01';S=P/'SHARED_GIT_WINDOW_STATUS.json'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(Path(p).read_bytes())
def require(v,m):
 if not v:raise RuntimeError(m)
def pin(p):
 p=Path(p);require(p.is_file() and not p.is_symlink(),'literal artifact');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def body(x):
 b=Path(x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'entire historical body; terminal archive mode qualified separately');return b
def main():
 require(not sys.flags.optimize,'optimization');source=pin(N/'integrate_pr302.py');planpin=pin(N/'CONTENT_PLAN.json');plan=load(N/'CONTENT_PLAN.json')
 require(source['sha256']=='2dd3f08d52e68aed4b7a66ceea7092681e0f4e05fc5d9c7eb0c1df2757166003' and planpin['sha256']=='baea4aabf70a814f184826433ab0d62b7fc5dc8177cebaa9d80ed5d43fa6f97c' and source['mode']==planpin['mode']==0o444,'exact immutable concrete source/plan')
 prerequisite=N/'ROOT_PRE_NATIVE_READBACK_v02.json';require(pin(prerequisite)['sha256']=='4c7715cb75a2dcec7bf75c981a8b2b410504598d3d2fe46ba6ee8268af3df9bc' and pin(prerequisite)['mode']==0o444,'genuine full ROOT preparation adjudication')
 pre=load(prerequisite);require(pre['source']==source and pre['plan']==planpin and pre['full24bound_inputs']==plan['bound_inputs'] and pre['no_native_or_service_write'] and not pre['execution_authority_granted'],'nonexecuting ROOT source/publication/tracker/current-source check')
 require(len(plan['bound_inputs'])==len({x['path'] for x in plan['bound_inputs']})==24,'all24unique full prerequisite roles')
 for x in plan['bound_inputs']:require(pin(x['path'])==x,'each current complete approved input body/mode')
 names=['REPORT.md','DERIVATION.md','READ_SCOPE_LEDGER.md','VERDICT.json','OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'];closed={n:pin(V/n) for n in names};require(all(x['mode']==0o444 for x in closed.values()),'six complete frozen closed-review roles')
 require(closed['OUTPUT_MANIFEST.json']['bytes']==198687 and closed['OUTPUT_MANIFEST.json']['sha256']=='d5b770a37abadd98d4b0023228e3fc5a618aa4846e303223bbe4e11b3d508354' and closed['CLOSURE_SEAL.json']['bytes']==2837 and closed['CLOSURE_SEAL.json']['sha256']=='39302c43cc9de997067d90610a0073d4473e6b2b0f87e37580b5ae31df8373cc','exact announced closed native review')
 manifest=load(V/'OUTPUT_MANIFEST.json');seal=load(V/'CLOSURE_SEAL.json');rows=manifest['files'];expected=set()
 for x in rows:
  path=Path(x['path']);path=path if path.is_absolute() else V/path;require(path.is_relative_to(V),'closed payload stays in review namespace');relative=str(path.relative_to(V));require(relative not in expected,'no duplicate closed payload');expected.add(relative)
  require(pin(path)==dict(path=str(path),bytes=x['bytes'],sha256=x['sha256'],mode=x['mode']) and x['mode']==0o444,'each complete terminal review body/mode')
 actual={str(p.relative_to(V)) for p in V.rglob('*') if p.is_file()};require(actual==expected|{'OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'} and len(expected)>30,'nonvacuous whole noncircular closure inventory')
 require(all(stat.S_IMODE(p.stat().st_mode)==0o555 for p in [V,*[q for q in V.rglob('*') if q.is_dir()]]),'all closed directories0555');require(seal['manifest']==closed['OUTPUT_MANIFEST.json'] and seal['required_review_roles']=={n:closed[n] for n in names[:4]} and seal['operator']==source and seal['plan']==planpin and seal['unresolved_issues']==[] and seal['execution_authority_granted'] is False,'exact closure manifest and all primary roles')
 verdict=load(V/'VERDICT.json');require(verdict['unresolved_issues']==[] and verdict['execution_authority_granted'] is False and verdict['operator']==source and verdict['plan']==planpin,'exact current-source independent clear/nonauthorizing disposition')
 # All full own sources, requests, started PIDs and completed raw streams are
 # authenticated, including the retained failed probes and corrected errata.
 captures=[]
 for p in sorted((V/'actual_readonly').glob('*/execution.json')):
  e=load(p);q=load(p.parent/'request.json');started=load(p.parent/'started.json')
  require(all(e[k]==v for k,v in q.items()) and e['read_only'] and e['timed_out'] is False,'genuine full read-only native request/completion')
  require(started['actual_PID']==e['actual_PID'] and type(e['actual_PID']) is int and e['actual_PID']>0 and started['argv']==e['argv'] and started['cwd']==e['cwd'],'own native captured PID/argv/cwd agreement')
  require(datetime.fromisoformat(e['requested_UTC'])<=datetime.fromisoformat(started['start_UTC'])<=datetime.fromisoformat(e['end_UTC']),'actual own time interval')
  for x in e['sources']:
   b=gzip.decompress(body(x['copy']));require(len(b)==x['source']['bytes'] and sha(b)==x['source']['sha256'],'entire own historical prelaunch source body')
  for name in ['stdout','stderr']:
   x=e['streams'][name];b=gzip.decompress(body(x['stored']));require(len(b)==x['logical_bytes'] and sha(b)==x['logical_sha256'],'whole own stored/logical streams')
  captures.append(dict(execution=pin(p),actual_PID=e['actual_PID'],actual_recorder_PID=e['actual_recorder_PID'],argv=e['argv'],returncode=e['returncode'],streams=e['streams']))
 require(len(captures)>=19,'whole historical and final actual review-capture history')
 proposal=load(N/'PROPOSED_NATIVE_SCOPE.json');old=S.read_bytes();require(proposal['live_control_before_future_grant']==pin(S) and proposal['operator']==source and proposal['plan']==planpin,'actual closed old control epoch and prepared geometry')
 control=load(S);require(not control['shared_git_writes_paused'] and not control['ascending_pr85_publication_integration_window_granted'] and control['ascending_pr85_publication_integration_window_aborted_inactive'] and not control['descending_302_publication_checkpoint_lease']['active'] and control['descending_302_publication_checkpoint_lease']['original_operator_completed_successfully'] is False and not control['descending_302_checkpoint037_push_recovery_lease']['active'] and control['descending_302_checkpoint037_push_recovery_lease']['completed'],'old peer revoked and truthful failed-checkpoint/recovery scopes closed')
 require(plan['starting_main']=='0a49d5e66a0fb9d4f78c7f3a7f3b30cd77196567' and plan['original_head']=='eb6e0e999521d84a65f9857d338cad76b84d30db' and plan['original_author_budget']=='2/5' and len(plan['allowed_paths'])==34,'exact original/head/base/path count')
 cap=N/'root_native_grant_fresh_readonly';cap.mkdir(exist_ok=False)
 def run(label,argv):
  q=cap/label;q.mkdir();request=dict(argv=argv,cwd=str(R),requested_UTC=utc(),source=pin(__file__),automatic_retry=False);(q/'request.json').write_text(json.dumps(request,indent=2)+'\n');(q/'source.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0));proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);started=dict(**request,actual_PID=proc.pid,start_UTC=utc());(q/'started.json').write_text(json.dumps(started,indent=2)+'\n');out,err=proc.communicate(timeout=55);streams={}
  for n,b in [('stdout',out),('stderr',err)]:
   z=q/(n+'.gz');z.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(z),logical_bytes=len(b),logical_sha256=sha(b))
  (q/'execution.json').write_text(json.dumps(dict(**started,end_UTC=utc(),exit_code=proc.returncode,parent_reaped=True,streams=streams),indent=2)+'\n');require(proc.returncode==0 and not err,'fresh grant read-only result');return out
 require(run('branch',['/usr/bin/git','--no-optional-locks','branch','--show-current'])==b'main\n' and run('head',['/usr/bin/git','--no-optional-locks','rev-parse','HEAD']).decode().strip()==plan['starting_main'],'fresh actual main')
 require(run('remote',['/usr/bin/git','--no-optional-locks','ls-remote',plan['endpoint'],'refs/heads/main']).split()[0].decode()==plan['starting_main'],'fresh explicit remote')
 require(not run('staged',['/usr/bin/git','--no-optional-locks','diff','--cached','--raw','-z']) and not (R/'.git/MERGE_HEAD').exists() and not (R/'.git/index.lock').exists(),'fresh empty index/no merge')
 pr=json.loads(run('PR',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/302']));require(pr['head']['sha']==plan['original_head'] and pr['state']=='open' and pr['draft'] and pr['base']['ref']=='main','fresh exact original draft')
 require(S.read_bytes()==old,'old control held through ROOT review/grant readback');clearpath=N/'ROOT_NATIVE_INTEGRATION_CLEARANCE.json';require(not clearpath.exists(),'no previous native clearance')
 stamp=utc();decision=dict(status='PASS_EXACT_PR302_NATIVE_ORIGINAL_HEAD_AND_PRESENT_DAY_ACCEPTANCE',UTC=stamp,actual_ROOT_recorder_PID=os.getpid(),ROOT_source=pin(__file__),operator=source,plan=planpin,original_head=plan['original_head'],original_author_budget='2/5',starting_main=plan['starting_main'],allowed_paths=plan['allowed_paths'],unresolved_issues=[],native_execution_authorized=True,review_namespace=str(V),closed_review_pins=closed,all_closed_review_files_authenticated=len(actual),all_actual_review_captures_authenticated=captures,full_ROOT_preparation_source_publication_tracker_identity_and_snapshot_readback=pin(prerequisite),all24current_complete_input_bodies_modes_verified=True,old_failed_checkpoint_recovery_truthfully_closed=True,peer85_native_acceptance_checkpoint_remain_PENDING=True,no_Zenodo_or_GWS_mutation_authorized=True,historical_transitions_asserted=False,new_central_proof_search_turns=0,estimates_percent=dict(PR302_workflow=85,native_review=100,native_execution=0))
 with clearpath.open('x') as f:json.dump(decision,f,indent=2);f.write('\n')
 clearpath.chmod(0o444);(N/'EXACT_PRE_NATIVE_GRANT_CONTROL.json').write_bytes(old)
 lease=dict(token=str(uuid.uuid4()),active=True,git_authorized=True,scope='Exact original-head PR302 native integration and present-day acceptance only',operator=source,plan=planpin,clearance=pin(clearpath),endpoint=plan['endpoint'],starting_main=plan['starting_main'],original_head=plan['original_head'],allowed_paths=plan['allowed_paths'],created_UTC=stamp,expires_UTC=(datetime.now(timezone.utc)+timedelta(minutes=24)).isoformat(),no_Zenodo_or_tracker_mutation=True)
 control.update(utc=stamp,shared_git_writes_paused=False,descending_writer_window_released=False,descending_shared_git_writes_abstained=False,reason='ROOT exact independently reviewed original-head PR302 native merge and present-day acceptance only; no new paper/DOI/tracker action');control['descending_302_native_integration_lease']=lease;require(S.read_bytes()==old,'final live old control before exact native grant');S.write_text(json.dumps(control,indent=2)+'\n')
 print(json.dumps(dict(status=decision['status'],actual_ROOT_recorder_PID=os.getpid(),closed_review_files=len(actual),token=lease['token'],expires_UTC=lease['expires_UTC'],clearance=pin(clearpath),control=pin(S)),indent=2))
if __name__=='__main__':main()
