"""Prepared exact-original-head merge after verified publication; never retry blindly."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json,stat,os,sys,subprocess,gzip,importlib.util,signal
if sys.flags.optimize:raise RuntimeError('Optimized execution is forbidden.')
D=Path(__file__).resolve().parent.parent;R=Path('/Users/alec/Documents/Math');A=D.parent;P=A.parent.parent
sys.path.insert(0,str(D/'publication_preparation'))
import submission_gate as g
from public_identity import identity,resolution_binding
HEAD='cc083024dbd00de06ad444cd4070f51f60d209eb';PREFIX='problems/5100034_focal_pedal_equality';QUEUE='unsolved_math_prioritization/QUEUE.md'
utc=lambda:datetime.now(timezone.utc).isoformat();sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(Path(p).read_bytes())
def require(v,msg):
 if not v:raise RuntimeError(msg+'; preserve partial state, inspect, and do not repeat mutation.')
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def row(b):
 found=[x for x in b.splitlines(keepends=True) if b'| 5100034 /' in x];require(len(found)==1 and len(found[0].split(b'|'))==14,'Exact target row missing');return found[0]
def names(b):return {x.decode() for x in b.split(b'\0') if x}
def main():
 lock=g.acquire();lease=g.window();control=load(P/'SHARED_GIT_WINDOW_STATUS.json');require(lease.get('git_authorized') is True,'This lease does not authorize Git integration')
 ownclear=load(D/'ROOT_PR305_NATIVE_INTEGRATION_CLEARANCE.json')
 require(ownclear['status']=='PASS_EXACT_PR305_NATIVE_INTEGRATION_OPERATOR' and ownclear['unresolved_mandatory_findings']==0,'Closed native-operator review missing')
 require(ownclear['operator']==g.pin(Path(__file__)),'Native operator source drift')
 for absolute,e in ownclear['closed_review_evidence'].items():require(g.pin(absolute)==e,'Native review evidence drift')
 require(ownclear['acceptance_preparation']==g.pin(D/'ROOT_ACCEPTANCE_PREPARED.md') and ownclear['snapshot_manifest']==g.pin(A/'snapshot_manifest.json'),'Accepted input drift')
 actual=D/'native_integration_actual';require(not actual.exists(),'Existing native attempt must be reconciled')
 actual.mkdir();(actual/'ATTEMPT.json').write_text(json.dumps({'UTC':utc(),'automatic_retry':False,'phase':'STARTED_OUTCOME_UNCERTAIN_UNTIL_FINAL_RECEIPT','operator':g.pin(Path(__file__)),'lease_token':lease['token']},indent=2)+'\n')
 count=0
 def run(argv,ok=(0,),input=None):
  nonlocal count
  count+=1;label=str(count);pre=actual/(label+'_request.json');require(not pre.exists(),'Prior command marker exists')
  spec={'argv':[str(x) for x in argv],'cwd':str(R),'start_UTC':utc(),'operator':g.pin(Path(__file__)),'automatic_retry':False};pre.write_text(json.dumps(spec,indent=2)+'\n')
  writer=(spec['argv'][0]=='/usr/bin/git' and len(spec['argv'])>2 and spec['argv'][2] in {'fetch','merge','add','commit','push'}) or spec['argv'][:3]==['/opt/homebrew/bin/gh','pr','edit']
  proc=None;out=err=None;complete=reaped=cleanup_attempted=False
  def kill_group():
   try:os.killpg(proc.pid,signal.SIGKILL)
   except ProcessLookupError:pass
  def contain(known=None):
   kill_group()
   if known is not None:out,err,complete=known
   else:
    try:out,err=proc.communicate(timeout=5);complete=True
    except subprocess.TimeoutExpired as failure:out,err=failure.output or b'',failure.stderr or b'';complete=False
   reaped=False
   try:proc.wait(timeout=1);reaped=True
   except subprocess.TimeoutExpired:pass
   return out,err,complete,reaped
  if writer:authorize()
  # One exception boundary covers EVERY operation after Popen, through return.
  # Success also kills any remaining cooperative helpers with closed pipes.
  try:
   proc=subprocess.Popen(spec['argv'],cwd=R,stdin=subprocess.PIPE if input is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'))
   spec['actual_PID']=proc.pid;spec['cooperative_process_group']=proc.pid
   (actual/(label+'_started.json')).write_text(json.dumps(spec,indent=2)+'\n')
   try:
    out,err=proc.communicate(input,timeout=55);code=proc.returncode;complete=reaped=True
    kill_group();cleanup_attempted=True
    spec.update(timeout_cleanup_required=False,whole_cooperative_group_SIGKILL_sent=True,remaining_cooperative_helpers_contained_after_parent_completion=True)
   except subprocess.TimeoutExpired:
    out,err,complete,reaped=contain();code=124;cleanup_attempted=True
    spec.update(timeout_cleanup_required=True,whole_cooperative_group_SIGKILL_sent=True)
   spec.update(end_UTC=utc(),exit_code=code,full_stream_capture_complete=complete,parent_reaped=reaped)
   for k,b in [('stdout',out),('stderr',err)]:
    stored=gzip.compress(b,6,mtime=0);path=actual/(label+'_'+k+'.gz')
    with path.open('xb') as f:f.write(stored);f.flush();os.fsync(f.fileno())
    require(gzip.decompress(path.read_bytes())==b,'Full stream storage round-trip failed');spec[k]={'path':str(path),'logical_bytes':len(b),'logical_sha256':sha(b),'stored_bytes':len(stored),'stored_sha256':sha(stored)}
   (actual/(label+'_execution.json')).write_text(json.dumps(spec,indent=2)+'\n')
   require(complete and reaped,'Capture or process cleanup incomplete')
   require(code in ok,'Command failed '+str(argv[0]))
   return out
  except BaseException:
   if proc is not None:
    if cleanup_attempted:kill_group()
    else:out,err,complete,reaped=contain((out,err,complete) if out is not None else None)
    interrupted=dict(spec,end_UTC=utc(),exit_code=proc.returncode,capture_exception=True,full_stream_capture_complete=complete,parent_reaped=reaped,whole_cooperative_group_SIGKILL_sent=True,outcome_uncertain=True,no_automatic_retry=True)
    try:
     for k,b in [('stdout',out),('stderr',err)]:
      stored=gzip.compress(b,6,mtime=0);path=actual/(label+'_interrupted_'+k+'.gz')
      with path.open('xb') as f:f.write(stored);f.flush();os.fsync(f.fileno())
      interrupted[k]=dict(path=str(path),logical_bytes=len(b),logical_sha256=sha(b),stored_bytes=len(stored),stored_sha256=sha(stored))
     (actual/(label+'_interrupted.json')).write_text(json.dumps(interrupted,indent=2)+'\n')
    except OSError:pass
   raise
 def git(*args,input=None,ok=(0,)):return run(['/usr/bin/git','--no-optional-locks',*args],ok,input)
 def pr():return json.loads(run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/305']))
 original=load(A/'snapshot_manifest.json');require(original['head']==HEAD and original['original_submitted_status']=='claimed_solved' and original['original_author_turn_count']=='1/5' and len(original['files'])==30,'Original intake drift')
 oldfiles=[e for e in original['files'] if e['path'].startswith(PREFIX+'/')];require(len(oldfiles)==29,'Original packet scope drift')
 pub=load(g.OUT/'inspect_published_receipt.json');public=load(g.OUT/'PUBLIC_RECORD_VERIFICATION.json');tracker=load(g.OUT/'TRACKER_COMPLETE.json');identity(pub);resolution_binding(public['doi_resolution'],pub['id'])
 require(pub['state']=='published' and pub['environment']=='production' and public['status']=='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES','Actual public result missing')
 require(public['record_id']==pub['id'] and public['doi']==tracker['doi']==pub['doi'] and len(public['all_file_bytes'])==2 and len(public['all_reviewed_metadata_keys_compared'])==11,'Publication identity or metadata mismatch')
 require(all(x['entire_public_download_equals_reviewed_local_file'] for x in public['all_file_bytes']),'Public file mismatch')
 require(tracker['status']=='PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK' and tracker['gid']==1254632077 and tracker['spreadsheetId']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and tracker['all_prior_rows_unchanged'] and tracker['exact_one_target_row_in_whole_postscan'] and tracker['whole_before_after_rows_equal_plus_exact_one_new_row'],'Actual tracker completion missing')
 require(load(D/'ROOT_ACTUAL_PUBLIC_EVIDENCE_READBACK.json')['status']=='PASS_PR305_ACTUAL_FULL_PUBLIC_EVIDENCE_AUTHENTICATED_BEFORE_TRACKER','ROOT full recent public evidence readback missing')
 current=base=lease['main'];require(git('rev-parse','HEAD').decode().strip()==base and git('branch','--show-current')==b'main\n','Baseline main differs')
 require(not git('diff','--cached','--raw','-z') and not (R/'.git/MERGE_HEAD').exists(),'Index or merge is busy')
 info=pr();require(info['state']=='open' and info['draft'] and info['head']['sha']==HEAD and info['base']['ref']=='main','Original PR identity changed')
 files=json.loads(run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/305/files?per_page=100']));require(len(files)==30 and {(x['filename'],x['sha']) for x in files}=={(x['path'],x['git_blob_sha']) for x in original['files']},'Incoming PR file identity changed')
 require(not (R/PREFIX).exists(),'Original destination already exists')
 gate_input_body=g.pin(D/'ROOT_ACCEPTANCE_PREPARED.md');prepared=(D/'ROOT_ACCEPTANCE_PREPARED.md').read_text();require(prepared.count('PREPARATION ONLY:')==1,'Current acceptance preparation shape')
 note=prepared.split('PREPARATION ONLY:')[0]+'Accepted after two successive NEW whole-preprint reviews, all required round01 corrections, a clean round02 review and ROOT reproduction. No unresolved required mathematical findings remain.\n\nActual publication: '+pub['doi_url']+'; record '+pub['record_url']+'. All eleven reviewed metadata values and both complete public files were checked. Exactly one tracker row '+tracker['updatedRange']+' was appended and read back, preserving all prior43-column formula rows.\n\n- [Research note](publication/focal-pedal-ratios-note.pdf)\n- [Portable source and verification archive](publication/focal-pedal-ratios-verification.zip)\n- [Exact deposit metadata](publication/zenodo-deposit.json)\n'
 extra={PREFIX+'/CURRENT_ACCEPTANCE.md':note.encode()}
 for n in ['focal-pedal-ratios-note.pdf','focal-pedal-ratios-verification.zip','zenodo-deposit.json']:extra[PREFIX+'/publication/'+n]=(g.O/n).read_bytes()
 owned={e['path'] for e in original['files']}|set(extra);require(len(owned)==34,'Owned domain changed')
 raw=(R/QUEUE).read_bytes();require(raw==git('show',base+':'+QUEUE),'Native QUEUE dirty');old=row(raw);cells=old.split(b'|');require(cells[8].strip()==b'queued' and cells[9].strip()==b'0/5','Native target baseline changed')
 newcells=cells[:];newcells[8]=b' claimed_solved ';newcells[9]=b' 1/5 ';newcells[11]=b' Accepted source E and stronger common phase-independent multiplier M for strict confocal-elliptic signed convex/star billiards; exact triangle disproves C. Prior observation, even symmetry, conditional old N3 consequence and established methods credited; bounded priority, extensive AI use, unrefereed. Research note and verification archive published after repaired round01 and clean new whole-review02; original29 bodies and author1/5 preserved. ';newcells[12]=(' '+pub['doi_url']+' ').encode();new=b'|'.join(newcells)
 require([i for i,(x,y) in enumerate(zip(cells,newcells)) if x!=y]==[8,9,11,12],'Unapproved target-cell change');after=raw.replace(old,new,1);require(after.replace(new,b'',1)==raw.replace(old,b'',1),'Foreign QUEUE bytes changed')
 index=git('ls-files','--stage','-z');flags=git('ls-files','-v','-z');dirty=names(git('diff','--name-only','-z','HEAD'));require(not dirty&owned,'Owned tracked file dirty')
 def exclude(b):return b'\0'.join(x for x in b.split(b'\0') if x and (x.split(b'\t',1)[-1].decode() if b'\t' in x else x[2:].decode()) not in owned)
 foreign={p:g.pin(R/p) for p in dirty};diff=git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b''
 def stable():
  require(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==current,'Local head drift')
  require({p:g.pin(R/p) for p in dirty}==foreign and names(git('diff','--name-only','-z','HEAD'))-owned==dirty,'Foreign dirty body/mode/scope changed')
  require((git('diff','--binary','HEAD','--',*sorted(dirty)) if dirty else b'')==diff,'Foreign binary diff changed')
  require(exclude(git('ls-files','--stage','-z'))==exclude(index) and exclude(git('ls-files','-v','-z'))==exclude(flags),'Full foreign logical index/flags changed')
 def authorize():
  g.current_clearance();g.operational_clearance();s=load(P/'SHARED_GIT_WINDOW_STATUS.json');l=load(D/'ROOT_FINAL_WRITE_LEASE.json')
  require(s==control and not s['shared_git_writes_paused'] and s['descending_shared_write_lease']['token']==l['token']==lease['token'] and l==lease,'Write lease/control changed')
  require(datetime.now(timezone.utc)+timedelta(seconds=75)<=datetime.fromisoformat(lease['expires_utc']),'Lease deadline insufficient for command, cleanup and capture')
  require(g.safe_endpoints()==(lease['fetch_endpoint'],lease['push_endpoint']),'Endpoint changed');require(g.pin(Path(__file__))==ownclear['operator'] and g.pin(D/'ROOT_ACCEPTANCE_PREPARED.md')==gate_input_body,'Source or preparation changed');stable()
  # These are the final reads before the caller's actual writer: slow prior
  # validation cannot extend the authority, and control drift is rejected.
  final_s=load(P/'SHARED_GIT_WINDOW_STATUS.json');final_l=load(D/'ROOT_FINAL_WRITE_LEASE.json')
  require(final_s==control and not final_s['shared_git_writes_paused'] and final_s['descending_shared_write_lease']['token']==lease['token'] and final_l==lease,'Final write lease/control changed')
  require(datetime.now(timezone.utc)+timedelta(seconds=75)<=datetime.fromisoformat(lease['expires_utc']),'Final lease no longer covers55s execution plus bounded cleanup/capture')
 authorize();git('fetch','--no-tags','--no-write-fetch-head',lease['fetch_endpoint'],'refs/pull/305/head');require(pr()['head']['sha']==HEAD,'Head changed during fetch')
 common=git('merge-base',base,HEAD).decode().strip();require(names(git('diff','--name-only','-z',common,HEAD))=={e['path'] for e in original['files']},'Local incoming scope changed')
 for e in original['files']:
  b=git('show',HEAD+':'+e['path']);require(len(b)==e['bytes'] and sha(b)==e['sha256'] and blob(b)==e['git_blob_sha'],'Original body/blob changed');require(git('ls-tree',HEAD,'--',e['path']).decode().split()[:3]==['100644','blob',e['git_blob_sha']],'Original Git mode changed')
 body=note.replace('(publication/','(https://github.com/AlecKriebel/Math/blob/main/'+PREFIX+'/publication/')+'\nThe exact original PRhead '+HEAD+' and historical source/review packet remain unchanged. Current acceptance and published package qualify and supersede the historical summaries.\n';bodyfile=actual/'PR_BODY.md';bodyfile.write_text(body)
 authorize();run(['/opt/homebrew/bin/gh','pr','edit','305','--repo','AlecKriebel/Math','--title','Resolve focal pedal area ratio equality for closed elliptic billiards','--body-file',str(bodyfile)]);fresh=pr();require(fresh['body']==body and fresh['head']['sha']==HEAD,'PR metadata readback differs')
 authorize();run(['/usr/bin/git','--no-optional-locks','merge','--no-ff','--no-commit',HEAD],ok=(0,1));require(names(git('diff','--name-only','--diff-filter=U','-z'))<={QUEUE} and (R/'.git/MERGE_HEAD').read_text().strip()==HEAD,'Unexpected merge conflict/state')
 authorize();(R/QUEUE).write_bytes(after);git('add','--',QUEUE)
 for rel,b in extra.items():
  p=R/rel;require(not p.exists() and not p.is_symlink(),'New publication destination exists')
  authorize();p.parent.mkdir(parents=True,exist_ok=True)
  authorize();p.write_bytes(b)
  authorize();p.chmod(0o644)
 git('add','--',*sorted(extra));require(names(git('diff','--cached','--name-only','-z'))==owned and not git('diff','--name-only','--diff-filter=U','-z'),'Merge staged domain differs')
 expected={e['path']:(A/'snapshot'/e['path']).read_bytes() for e in oldfiles};expected.update(extra);expected[QUEUE]=after
 for rel,b in expected.items():require(git('show',':'+rel)==b and git('ls-files','--stage','--',rel).decode().split()[:3]==['100644',blob(b),'0'],'Staged body/mode/blob differs')
 authorize();git('commit','-m','Accept PR305 focal-pedal equality and publish reviewed research note');current=git('rev-parse','HEAD').decode().strip()
 require(git('show','-s','--format=%P',current).decode().split()==[base,HEAD] and names(git('diff','--name-only','-z',base,current))==owned,'Merge parents/domain changed')
 for rel,b in expected.items():require(git('show',current+':'+rel)==b and git('ls-tree',current,'--',rel).decode().split()[:3]==['100644','blob',blob(b)] and (R/rel).read_bytes()==b and stat.S_IMODE((R/rel).stat().st_mode)==0o644,'Committed/native body/mode/blob differs')
 authorize();git('merge-base','--is-ancestor',base,current);require(git('ls-remote',lease['fetch_endpoint'],'refs/heads/main').split()[0].decode()==base,'Remote main moved')
 git('push','--force-with-lease=refs/heads/main:'+base,lease['push_endpoint'],current+':refs/heads/main');require(git('ls-remote',lease['fetch_endpoint'],'refs/heads/main').split()[0].decode()==current,'Push readback differs')
 fresh=pr();require(fresh['merged'] and fresh['merged_at'] and fresh['head']['sha']==HEAD and fresh['merge_commit_sha']==current,'GitHub exact merge readback missing')
 require(not git('diff','--cached','--raw','-z'),'Final index not empty');stable();g.current_clearance();g.operational_clearance()
 receipt={'UTC':utc(),'status':'PASS_PR305_EXACT_ORIGINAL_HEAD_MERGED_PUBLISHED_TRACKER_VERIFIED','PR':305,'original_head':HEAD,'actual_merge':current,'parents':[base,HEAD],'merged_at':fresh['merged_at'],'owned_paths':sorted(owned),'original29_bodies_modes_blobs_preserved':True,'original_author_history':'1/5','queue_only_cells':[8,9,11,12],'foreign_queue_bytes_preserved':True,'whole_foreign_logical_index_flags_dirty_bodies_modes_preserved':True,'main_branch_retained':True,'index_empty':True,'DOI':pub['doi'],'record_url':pub['record_url'],'tracker_range':tracker['updatedRange'],'mathematics_percent':100,'bounded_priority_percent':100,'PR_workflow_percent':100,'no_external_human_review':True,'extensive_AI_use':True,'historical_firstness_certified':False,'global_descending_inventory_checkpoint_pending':True,'root_actual_capture_directory':str(actual)}
 (D/'ROOT_PR305_ACTUAL_MERGE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
