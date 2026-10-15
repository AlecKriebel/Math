"""ROOT full actual native custody, original preservation and current acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';N=Path(__file__).parent;A=N.parent;D=N/'actual_native_integration';O=N/'actual_native_outer';S=P/'SHARED_GIT_WINDOW_STATUS.json'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(Path(p).read_bytes())
def require(v,m):
 if not v:raise RuntimeError(m)
def pin(p):
 p=Path(p);require(p.is_file() and not p.is_symlink(),'literal artifact');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def body(x):
 b=Path(x['path']).read_bytes();require(len(b)==x['bytes'] and sha(b)==x['sha256'],'complete stored body');return b
def names(b):return {x.decode() for x in b.split(b'\0') if x}
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def main():
 require(not sys.flags.optimize,'optimization');source=pin(N/'integrate_pr302.py');plan=load(N/'CONTENT_PLAN.json');owned=set(plan['allowed_paths']);receipt=load(N/'ROOT_ACTUAL_NATIVE_MERGE_VERIFICATION.json');commit=receipt['actual_merge'];base=plan['starting_main'];head=plan['original_head']
 require(source['sha256']=='f9ab8413e4af4a3d93cd2f4fc72615b47bfef07d328e828c3bb78439d5ef95ff' and source['mode']==0o444 and receipt['status']=='PASS_PR302_EXACT_ORIGINAL_HEAD_NATIVE_MERGE_AND_PRESENT_DAY_ACCEPTANCE' and len(owned)==34,'exact accepted-source actual native success scope')
 outer=load(O/'execution.json');req=load(O/'request.json');start=load(O/'started.json');require(all(outer[k]==v for k,v in req.items()) and all(outer[k]==v for k,v in start.items()) and outer['exit_code']==0 and outer['parent_reaped'] and outer['full_capture_complete'] and not outer['timed_out'] and outer['exception_after_Popen'] is None,'complete genuine outer native result')
 for x in outer['full_prelaunch_inputs']:
  b=gzip.decompress(body(x['stored']));require(len(b)==x['source']['bytes'] and sha(b)==x['source']['sha256'],'whole outer prelaunch body')
 raw={}
 for name,x in outer['streams'].items():
  b=gzip.decompress(body(x['stored']));require(len(b)==x['logical_bytes'] and sha(b)==x['logical_sha256'],'whole outer stored/logical stream');raw[name]=b
 require(not raw['stderr'] and json.loads(raw['stdout'])==receipt and outer['actual_PID']==receipt['actual_ROOT_recorder_PID'],'actual native outer result/receipt/PID')
 attempt=load(D/'ATTEMPT.json');require(attempt['source']==source and attempt['actual_ROOT_recorder_PID']==outer['actual_PID'],'actual native attempt identity')
 for x in attempt['full_prelaunch_inputs']:
  b=gzip.decompress(body(x['archive']));require(len(b)==x['input']['bytes'] and sha(b)==x['input']['sha256'],'every whole native prelaunch input')
 records=[];numbered={int(p.name.split('_')[0]) for p in D.glob('*_execution.json')};require(numbered==set(range(1,len(numbered)+1)) and len(numbered)>180,'complete nonempty actual native capture domain')
 for i in sorted(numbered):
  e=load(D/f'{i}_execution.json');q=load(D/f'{i}_request.json');started=load(D/f'{i}_started.json')
  require(all(e[k]==v for k,v in q.items()) and all(e[k]==v for k,v in started.items()) and e['operator']==source and e['cwd']==str(R) and e['actual_PID']==e['cooperative_process_group'] and e['actual_PID']>0,'all actual native request/start/completion/source/PID')
  require(e['full_stream_capture_complete'] and e['parent_reaped'] and not e['timeout_cleanup_required'] and datetime.fromisoformat(e['start_UTC'])<=datetime.fromisoformat(e['end_UTC']),'complete native streams/cleanup/interval')
  require(e['exit_code']==(1 if i==1 else (e['exit_code'] if e['argv'][2:3]==['merge'] else 0)) and e['exit_code'] in (0,1),'allowed config no-match or actual merge conflict; all other zero outcomes')
  streams={}
  for name,x in [('stdout',e['stdout']),('stderr',e['stderr'])]:
   z=Path(x['path']).read_bytes();b=gzip.decompress(z);require(len(z)==x['stored_bytes'] and sha(z)==x['stored_sha256'] and len(b)==x['logical_bytes'] and sha(b)==x['logical_sha256'],'entire native stored/logical stream');streams[name]=b
  records.append((e,streams))
 writers=[e for e,b in records if e['argv'][0]=='/usr/bin/git' and e['argv'][2] in ['fetch','merge','add','commit','push']];require([x['argv'][2] for x in writers]==['fetch','merge','add','commit','push'],'one each exact native writer, no automatic replay')
 require(writers[0]['argv'][3:]==['--no-tags','--no-write-fetch-head',plan['endpoint'],'refs/pull/302/head'] and writers[1]['argv'][3:]==['--no-ff','--no-commit',head] and writers[4]['argv'][3:]==['--force-with-lease=refs/heads/main:'+base,plan['endpoint'],commit+':refs/heads/main'],'exact original fetch/merge/expected-old descendant push')
 edits=[e for e,b in records if e['argv'][:3]==['/opt/homebrew/bin/gh','pr','edit']];require(len(edits)==1 and edits[0]['argv'][3]=='302','exact one target PR annotation')
 def baseline(args):return next(b['stdout'] for e,b in records if e['argv']==['/usr/bin/git','--no-optional-locks',*args])
 oldqueue=baseline(['show',base+':unsolved_math_prioritization/QUEUE.md']);oldstate=baseline(['show',base+':unsolved_math_prioritization/state.json']);oldhistory=baseline(['show',base+':unsolved_math_prioritization/history.jsonl'])
 snapshot=load(A/'snapshot_manifest.json');prefix='unsolved_math_prioritization/attempts/30003508';expected={x['path']:(A/'snapshot'/x['path']).read_bytes() for x in snapshot['files'] if x['path'].startswith(prefix+'/')};require(len(expected)==28,'exact original28 full expected bodies');expected.update({prefix+'/'+n:(N/'payloads'/n).read_bytes() for n in ['acceptance.json','CURRENT_RESULT.md','CURRENT_PRIORITY.md']})
 queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();state=(R/'unsolved_math_prioritization/state.json').read_bytes();history=(R/'unsolved_math_prioritization/history.jsonl').read_bytes();expected.update({'unsolved_math_prioritization/QUEUE.md':queue,'unsolved_math_prioritization/state.json':state,'unsolved_math_prioritization/history.jsonl':history});require(set(expected)==owned and queue==(N/'payloads/QUEUE_AFTER.md').read_bytes(),'all34 full expected roles/current QUEUE')
 row=lambda b:next(x for x in b.splitlines(keepends=True) if b'| 30003508 /' in x);bc=row(oldqueue).split(b'|');ac=row(queue).split(b'|');require([i for i in range(14) if bc[i]!=ac[i]]==[8,9,11,12] and oldqueue.replace(row(oldqueue),b'',1)==queue.replace(row(queue),b'',1),'four target QUEUE cells and all foreign literal bytes')
 event=json.loads(state)['30003508'];require(event['status']=='preprint_published' and event['turns_used']==2 and event['turn_limit']==5 and event['evidence']['new_central_proof_search_turns']==0 and event['evidence']['historical_transitions_asserted'] is False and event['evidence']['original_head']==head,'present-day current event preserves author budget/history')
 cut=len(oldstate.rstrip())-1;insert=(b',' if json.loads(oldstate) else b'')+b'\n'+json.dumps('30003508').encode()+b': '+json.dumps(event,sort_keys=True).encode();require(state==oldstate[:cut]+insert+oldstate[cut:] and history==oldhistory+json.dumps(event,sort_keys=True).encode()+b'\n','all foreign state/history literal bytes and exactly one current event')
 cap=N/'root_actual_native_readback';cap.mkdir(exist_ok=False)
 def run(label,argv):
  q=cap/label;q.mkdir();request=dict(argv=argv,cwd=str(R),requested_UTC=utc(),source=pin(__file__),automatic_retry=False);(q/'request.json').write_text(json.dumps(request,indent=2)+'\n');(q/'source.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0));proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);started=dict(**request,actual_PID=proc.pid,start_UTC=utc());(q/'started.json').write_text(json.dumps(started,indent=2)+'\n');out,err=proc.communicate(timeout=55);streams={}
  for n,b in [('stdout',out),('stderr',err)]:
   p=q/(n+'.gz');p.write_bytes(gzip.compress(b,mtime=0));streams[n]=dict(stored=pin(p),logical_bytes=len(b),logical_sha256=sha(b))
  (q/'execution.json').write_text(json.dumps(dict(**started,end_UTC=utc(),exit_code=proc.returncode,parent_reaped=True,streams=streams),indent=2)+'\n');require(proc.returncode==0 and not err,'actual ROOT read-only result');return out
 def git(label,*args):return run(label,['/usr/bin/git','--no-optional-locks',*args])
 require(git('branch','branch','--show-current')==b'main\n' and git('head','rev-parse','HEAD').decode().strip()==commit and git('parents','show','-s','--format=%P',commit).decode().split()==[base,head],'fresh main and exact original second parent')
 require(git('remote','ls-remote',plan['endpoint'],'refs/heads/main').split()[0].decode()==commit and names(git('changed','diff','--name-only','-z',base,commit))==owned and not git('staged','diff','--cached','--raw','-z'),'fresh exact remote/domain/empty index')
 for rel,b in expected.items():require((R/rel).read_bytes()==b and pin(R/rel)['mode']==0o644 and git('blob_'+str(len(rel))+'_'+sha(rel.encode())[:10],'show',commit+':'+rel)==b and git('mode_'+sha(rel.encode())[:12],'ls-tree',commit,'--',rel).decode().split()[:3]==['100644','blob',blob(b)],'each34 whole current/committed native body/mode/blob')
    oldindex=baseline(['ls-files','--stage','-z']);oldflags=baseline(['ls-files','-v','-z']);index=git('index','ls-files','--stage','-z');flags=git('flags','ls-files','-v','-z');exclude=lambda b,stage:[x for x in b.split(b'\0') if x and (x.split(b'\t',1)[1].decode() if stage else x[2:].decode()) not in owned];require(exclude(index,True)==exclude(oldindex,True) and exclude(flags,False)==exclude(oldflags,False),'entire foreign index/flags')
 entries={x.split(b'\t',1)[1].decode():x.split(b'\t',1)[0].decode().split() for x in index.split(b'\0') if x}
 require(all(entries[rel]==['100644',blob(b),'0'] for rel,b in expected.items()),'all34 complete expected index blob/mode/stage identities')
 dirty=names(baseline(['diff','--name-only','-z','HEAD']));require(names(git('dirty','diff','--name-only','-z','HEAD'))-owned==dirty and git('diff','diff','--binary','HEAD','--',*sorted(dirty))==baseline(['diff','--binary','HEAD','--',*sorted(dirty)]),'whole foreign dirty binary diff')
 held=[x for x in load(N/'KNOWN_HELD_BASELINE.json')['files'] if str(Path(x['path']).relative_to(R)) not in owned and x['path']!=str(S)]
 for x in held:require(pin(x['path'])==x,'all known nonowned held complete bodies/modes')
 pr=json.loads(run('PR',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/302']));require(pr['merged'] is True and pr['merge_commit_sha']==commit and pr['head']['sha']==head and pr['merged_at']==receipt['merged_at'],'fresh GitHub exact original merge status')
 result=dict(status='ROOT_ACCEPTS_ACTUAL_PR302_ORIGINAL_HEAD_NATIVE_INTEGRATION',UTC=utc(),actual_ROOT_recorder_PID=os.getpid(),ROOT_source=pin(__file__),actual_native_outer_execution=pin(O/'execution.json'),actual_native_PID=outer['actual_PID'],actual_native_exit_code=0,actual_merge=commit,parents=[base,head],original_head=head,original_author_budget='2/5',original28full_bodies_modes_blobs_preserved=True,all34live_index_committed_full_bodies_modes_blobs_verified=True,owned_paths=sorted(owned),all_actual_native_captures_authenticated=[dict(execution=pin(D/f'{i}_execution.json'),actual_PID=e['actual_PID'],argv=e['argv'],exit_code=e['exit_code']) for i,(e,b) in enumerate(records,1)],all_outer_and_native_full_prelaunch_sources_inputs_and_streams_authenticated=True,only_four_target_QUEUE_cells_changed=True,all_foreign_QUEUE_state_history_literal_bytes_preserved=True,exact_one_present_day_event_imported=True,historical_transitions_asserted=False,new_central_proof_search_turns=0,whole_foreign_index_flags_dirty_binary_diff_preserved=True,known_nonowned_held_count=len(held),all_known_nonowned_held_complete_bodies_modes_preserved=True,fresh_main_equals_explicit_remote=True,index_empty=True,GitHub_exact_original_head_merge_confirmed=True,merged_at=pr['merged_at'],DOI=receipt['DOI'],tracker_range=receipt['tracker_range'],no_new_Zenodo_or_tracker_action=True,global_descending_completion_checkpoint_pending=True,estimates_percent=dict(PR302_workflow=95,native_integration=100))
 out=A/'ROOT_ACTUAL_NATIVE_INTEGRATION_ACCEPTANCE.json'
 with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 out.chmod(0o444);print(json.dumps(dict(status=result['status'],actual_ROOT_recorder_PID=os.getpid(),actual_merge=commit,native_captures=len(records),acceptance=pin(out)),indent=2))
if __name__=='__main__':main()
