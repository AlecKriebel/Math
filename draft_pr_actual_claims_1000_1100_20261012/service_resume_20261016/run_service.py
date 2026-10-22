"""Ordered, explicit publication steps with intent/read-back reconciliation.

Uses only the repository's native Zenodo kit, Google Workspace CLI and gh.
An uncertain mutation stops for read-back; it is never silently repeated.
"""
import argparse,datetime,hashlib,json,os,subprocess,sys,fcntl,tempfile
from pathlib import Path
D=Path(__file__).resolve().parent.parent; R=Path(__file__).resolve().parent; REPO=D.parent
GWS='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'; GH='/opt/homebrew/bin/gh'
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'; GID=1254632077
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):return json.loads(p.read_text())
def need(c,s):
 if not c:raise RuntimeError(s)
def atomic_text(p,value):
 fd,name=tempfile.mkstemp(prefix='.service-',dir=p.parent)
 try:
  with os.fdopen(fd,'w')as f:f.write(value);f.flush();os.fsync(f.fileno())
  os.replace(name,p)
  directory_fd=os.open(p.parent,os.O_RDONLY)
  try:os.fsync(directory_fd)
  finally:os.close(directory_fd)
 finally:
  if os.path.exists(name):os.unlink(name)
def save(p,v):atomic_text(p,json.dumps(v,indent=2)+'\n')
def ident(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('pr',type=int);parser.add_argument('step',choices=['plan','stage','publish','track','merge','complete']);args=parser.parse_args();n=args.pr
 cfg=read(R/f'PR{n}_SERVICE_CONFIG.json');A=D/cfg['audit_folder'];O=A/'service_receipts_20261016';O.mkdir(exist_ok=True)
 lock=(O/'process.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 if args.step=='complete':
  completion_lock=(R/'global_completion_state.lock').open('a');fcntl.flock(completion_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 manifest=D/cfg['manifest'];seal=D/cfg['final_seal'];need(ident(manifest)==cfg['manifest_identity'] and ident(seal)==cfg['final_seal_identity'],'Reviewed native input/final seal changed')
 for r in cfg['files']:need(ident(D/r['path'])=={k:r[k] for k in ['bytes','sha256']},'Reviewed publication bytes changed')
 metadata=read(manifest)['metadata'];need(hashlib.sha256(json.dumps(metadata,sort_keys=True,separators=(',',':')).encode()).hexdigest()==cfg['metadata_sha256'],'Metadata changed')
 need(cfg['fresh_complete_reviews']>=2,'Two complete whole-package reviews required')
 state=read(D/'STATE.json')
 if args.step!='plan':need(state['next_pr']==n or (args.step=='complete' and n in state['completed_prs']),'Ascending cursor does not permit this PR')
 def cmd(label,argv,timeout=180):
  try:p=subprocess.run(list(map(str,argv)),cwd=REPO,capture_output=True,text=True,timeout=timeout)
  except subprocess.TimeoutExpired as exc:
   def text(v):return v.decode(errors='replace')if isinstance(v,bytes)else(v or '')
   event={'label':label,'utc':now(),'argv':list(map(str,argv)),'cwd':str(REPO),'exit_code':None,'outcome':'TIMEOUT_UNCONFIRMED','stdout':text(exc.stdout),'stderr':text(exc.stderr)}
   ledger=O/'COMMANDS.jsonl';atomic_text(ledger,(ledger.read_text()if ledger.exists()else'')+json.dumps(event)+'\n');raise
  row={'utc':now(),'argv':list(map(str,argv)),'cwd':str(REPO),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
  ledger=O/'COMMANDS.jsonl';atomic_text(ledger,(ledger.read_text()if ledger.exists()else'')+json.dumps({'label':label,**row})+'\n')
  return p
 def good(p,s):
  need(p.returncode==0,s+': '+p.stderr);return json.loads(p.stdout)
 def ghget(path,label):return good(cmd(label,[GH,'api','repos/AlecKriebel/Math/'+path]),'GitHub read failed')
 def live(label):
  d=ghget('pulls/'+str(n),label);save(O/(label+'.json'),d);need(d['number']==n and d['head']['sha']==cfg['head'],'PR identity/head changed after review');need(d['base']['ref']=='main' and d['base']['repo']['full_name'].casefold()=='aleckriebel/math','PR base must remain this repository main');return d
 def native(action,label,extra=()):
  p=cmd(label,[sys.executable,'-B',REPO/'zenodo_deposit_tool/zenodo.py',action,manifest,*extra]);save(O/(label+'_RESPONSE.json'),{'utc':now(),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
 def inspection(label):return good(native('inspect',label,['--check-doi']),'Native remote inspection failed')
 def published(label):
  d=inspection(label);need(d['state']=='published' and d['environment']=='production' and d['title']==cfg['title'],'Exact publication not confirmed');need(d['doi_url']=='https://doi.org/'+d['doi'],'DOI URL differs');save(O/'PUBLICATION_VERIFIED.json',d);return d
 def intent(name,value):
  p=O/name;need(not p.exists(),'Previous mutation intent exists: reconcile its outcome before another request');save(p,{'utc':now(),**value})
 if args.step=='plan':
  local=good(native('check','LOCAL_CHECK'),'Native local check');need(local['title']==cfg['title'],'Different title');print(json.dumps({'status':'PLAN_ONLY_LOCAL_PASS','pr':n,'files':local['files'],'no_service_mutation':True}));return
 if args.step=='stage':
  d=live('PR_BEFORE_STAGE');need(d['state']=='open' and not d['merged'],'PR no longer open')
  key=hashlib.sha256(str(manifest.resolve()).encode()).hexdigest()[:24];sp=REPO/'.zenodo-state'/(key+'-production.json')
  if sp.exists():
   observed=inspection('EXISTING_NATIVE_STATE_INSPECT');need(observed['state']=='ready_to_publish','Existing native record already published; reconcile next steps');save(O/'STAGE_VERIFIED.json',observed);print(json.dumps({'status':'EXISTING_READY_DRAFT_VERIFIED','id':observed['id']}));return
  intent('STAGE_INTENT.json',{'manifest':str(manifest),'head':cfg['head'],'metadata_sha256':cfg['metadata_sha256'],'files':cfg['files']})
  p=native('stage','STAGE')
  if p.returncode:
   need(sp.exists(),'Stage outcome may be ambiguous with no saved ID. Account reconciliation required; do not restage.')
  observed=inspection('STAGE_READBACK');need(observed['state']=='ready_to_publish','Staged draft not ready');save(O/'STAGE_VERIFIED.json',observed);print(json.dumps({'status':'READY_DRAFT_VERIFIED','pr':n,'id':observed['id']}));return
 if args.step=='publish':
  d=live('PR_BEFORE_PUBLISH');need(d['state']=='open' and not d['merged'],'PR no longer open')
  observed=inspection('PREPUBLICATION_INSPECT')
  if observed['state']=='published':save(O/'PUBLICATION_VERIFIED.json',observed);print(json.dumps({'status':'ALREADY_PUBLISHED_VERIFIED','doi':observed['doi']}));return
  need(observed['state']=='ready_to_publish','Draft not verified');intent('PUBLISH_INTENT.json',{'id':observed['id'],'head':cfg['head'],'files':cfg['files'],'metadata_sha256':cfg['metadata_sha256']})
  p=native('publish','PUBLISH',['--confirm-id',str(observed['id'])]);out=published('POSTPUBLICATION_INSPECT');print(json.dumps({'status':'PUBLICATION_VERIFIED','pr':n,'doi':out['doi'],'record_url':out['record_url'],'doi_resolution':out.get('doi_resolution'),'publish_command_exit':p.returncode}));return
 def sheet(resource,method,params,body=None):
  argv=[GWS,'sheets','spreadsheets',*resource,method,'--params',json.dumps(params)]
  if body is not None:argv.extend(['--json',json.dumps(body)])
  return cmd('GWS_'+method,argv,120)
 def fresh_tracker(pub,label):
  tabs=good(sheet([],'get',{'spreadsheetId':SHEET,'fields':'spreadsheetId,sheets.properties'}),'Fresh tracker tab lookup');selected=[s['properties']for s in tabs['sheets']if s['properties']['sheetId']==GID];need(len(selected)==1,'Fresh tracker gid missing');title=selected[0]['title'];rng="'"+title.replace("'","''")+"'!A:D"
  rows=good(sheet(['values'],'get',{'spreadsheetId':SHEET,'range':rng}),'Fresh tracker read').get('values',[]);need(rows and rows[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'Fresh tracker headers changed')
  expected=[cfg['tracker_original_problem'],'',pub['doi_url'],cfg['tracker_notes']];matches=[(i+1,r)for i,r in enumerate(rows)if len(r)>2 and str(r[2]).removeprefix('https://doi.org/')==pub['doi']]
  need(len(matches)==1 and matches[0][1]==expected,'Fresh tracker exact unique DOI/full-row check failed')
  record={'utc':now(),'gid':GID,'sheet_title':title,'sheet_row':matches[0][0],'doi':pub['doi'],'values':expected,'read_back_exact':True};save(O/(label+'.json'),record);save(O/'TRACKER_VERIFIED.json',record);return record
 if args.step=='track':
  pub=published('ZENODO_BEFORE_TRACKER');tabs=good(sheet([],'get',{'spreadsheetId':SHEET,'fields':'spreadsheetId,sheets.properties'}),'Tracker tabs');selected=[s['properties']for s in tabs['sheets']if s['properties']['sheetId']==GID];need(len(selected)==1,'Tracker gid missing');title=selected[0]['title'];rng="'"+title.replace("'","''")+"'!A:D";params={'spreadsheetId':SHEET,'range':rng}
  row=[cfg['tracker_original_problem'],'',pub['doi_url'],cfg['tracker_notes']]
  def matches():
   rows=good(sheet(['values'],'get',params),'Tracker read').get('values',[]);need(rows and rows[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'Tracker columns changed');return[(i+1,r)for i,r in enumerate(rows)if len(r)>2 and str(r[2]).removeprefix('https://doi.org/')==pub['doi']]
  found=matches()
  if not found:
   intent('TRACKER_APPEND_INTENT.json',{'spreadsheetId':SHEET,'gid':GID,'range':rng,'valueInputOption':'RAW','values':[row],'doi':pub['doi']})
   p=sheet(['values'],'append',{**params,'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},{'majorDimension':'ROWS','values':[row]});save(O/'TRACKER_APPEND_RESPONSE.json',{'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});found=matches()
  need(len(found)==1 and found[0][1]==row,'Tracker outcome not exactly confirmed; no automatic repeat')
  save(O/'TRACKER_VERIFIED.json',{'utc':now(),'gid':GID,'sheet_title':title,'sheet_row':found[0][0],'doi':pub['doi'],'values':row,'read_back_exact':True});print(json.dumps({'status':'TRACKER_EXACT_ROW_VERIFIED','pr':n,'row':found[0][0],'doi':pub['doi']}));return
 if args.step=='merge':
  pub=published('ZENODO_BEFORE_MERGE');tracker=read(O/'TRACKER_VERIFIED.json');need(tracker['doi']==pub['doi'] and tracker['read_back_exact'],'Verified tracker required');d=live('PR_BEFORE_ACCEPTANCE')
  if not d['merged']:
   need(d['state']=='open','PR closed without merge')
   need(not(O/'MERGE_INTENT.json').exists(),'Earlier merge intent remains unconfirmed: no additional PR mutation is permitted')
   body='## Accepted result and published preprint\n\n**'+cfg['title']+'**, Alec Kriebel. Published paper and verification package: '+pub['doi_url']+' ('+pub['record_url']+').\n\n'+metadata['description']+'\n\n## Accepted scope and review\n\n'+cfg['accepted_scope']+'\n\n'+cfg['limitations']+'\n\nThe result is accepted at the exact audited head `'+cfg['head']+'`. '+str(cfg['fresh_complete_reviews'])+' fresh independent complete AI whole-package reviews were completed, with the final review finding zero actionable issues. Subsequent bounded administrative adoption is recorded in the current external ROOT final seal; earlier status/counter/hold fields remain dated history. Prior mathematical results and proof dependencies are credited. Historical novelty and worldwide current openness are unestablished. AI tools were used extensively; this is an unrefereed preprint, without conventional human peer review or formal proof certification.\n\nThe repository Zenodo uploader verified the exact reviewed metadata and PDF/support bytes. The Google Workspace CLI recorded the DOI/details in the requested tracker with exact read-back. No GitHub release is created. Current audit and publication receipts: `'+cfg['audit_folder']+'`.\n\n<details>\n<summary>Preserved original PR description: dated submission history</summary>\n\n'+d['body']+'\n\n</details>\n'
   payload=O/'PR_UPDATE_PAYLOAD.json'
   if not payload.exists():save(payload,{'title':cfg['pr_title'],'body':body})
   desired=read(payload);need(desired['title']==cfg['pr_title'] and pub['doi_url']in desired['body'] and cfg['head']in desired['body'],'Saved first-write PR payload identity mismatch')
   if d['title']!=desired['title'] or d['body']!=desired['body']:
    intent('PR_UPDATE_INTENT.json',{'payload':ident(payload),'head':cfg['head'],'DOI':pub['doi']})
    p=cmd('PR_UPDATE',[GH,'api','--method','PATCH','repos/AlecKriebel/Math/pulls/'+str(n),'--input',payload]);save(O/'PR_UPDATE_RESPONSE.json',{'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});d=live('PR_AFTER_ACCEPTANCE');need(d['title']==desired['title'] and d['body']==desired['body'],'PR update not confirmed; read back before another write')
   if d['draft']:
    intent('PR_READY_INTENT.json',{'head':cfg['head'],'DOI':pub['doi']})
    p=cmd('PR_READY',[GH,'pr','ready',str(n),'--repo','AlecKriebel/Math']);d=live('PR_AFTER_READY');need(d['draft'] is False,'Ready state not confirmed')
   tracker=fresh_tracker(pub,'TRACKER_IMMEDIATELY_BEFORE_MERGE');d=live('PR_IMMEDIATELY_BEFORE_MERGE');need(not d['merged'] and d['state']=='open' and not d['draft'],'PR state changed immediately before merge')
   intent('MERGE_INTENT.json',{'head':cfg['head'],'method':'merge','DOI':pub['doi'],'tracker_row':tracker['sheet_row']})
   p=cmd('PR_MERGE',[GH,'pr','merge',str(n),'--repo','AlecKriebel/Math','--merge','--match-head-commit',cfg['head']]);save(O/'PR_MERGE_RESPONSE.json',{'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});d=live('PR_AFTER_MERGE')
  need(d['merged'] is True and d['state']=='closed','Merge outcome unconfirmed; no repeat');commit=ghget('commits/'+d['merge_commit_sha'],'MERGE_COMMIT');parents=[p['sha']for p in commit['parents']];need(cfg['head']in parents,'Merge did not include exact audited head as parent');tracker=fresh_tracker(pub,'TRACKER_AFTER_VERIFIED_MERGE')
  save(O/'MERGE_VERIFIED.json',{'utc':now(),'pr':n,'head':cfg['head'],'merge_commit':d['merge_commit_sha'],'merged_at':d['merged_at'],'actual_merge_parents':parents,'exact_audited_head_parent':True,'doi':pub['doi'],'tracker_row':tracker['sheet_row']});print(json.dumps({'status':'EXACT_HEAD_MERGE_VERIFIED','pr':n,'merge_commit':d['merge_commit_sha']}));return
 if args.step=='complete':
  pub=published('FINAL_ZENODO_INSPECT');tracker=fresh_tracker(pub,'TRACKER_FINAL_COMPLETION_READBACK');merge=read(O/'MERGE_VERIFIED.json');d=live('FINAL_PR_READBACK');need(d['merged'] and d['merge_commit_sha']==merge['merge_commit'] and merge['head']==cfg['head'] and tracker['doi']==pub['doi'],'Complete workflow evidence mismatch')
  event_path=O/'COMPLETION_EVENT.json'
  if not event_path.exists():save(event_path,{'utc':now(),'pr':n,'doi':pub['doi'],'head':cfg['head'],'merge_commit':merge['merge_commit'],'metadata_sha256':cfg['metadata_sha256']})
  event=read(event_path);need(event['pr']==n and event['doi']==pub['doi'] and event['head']==cfg['head'] and event['merge_commit']==merge['merge_commit'] and event['metadata_sha256']==cfg['metadata_sha256'],'Durable completion event mismatch')
  state=read(D/'STATE.json');accepted={'timestamp_utc':event['utc'],'pr':n,'problem_id':cfg['problem_id'],'mathematical_outcome':cfg['accepted_scope'],'published':True,'doi':pub['doi'],'doi_resolves':pub.get('doi_resolution',{}).get('status')=='resolved','record_url':pub['record_url'],'tracker_gid':GID,'tracker_row':tracker['sheet_row'],'tracker_exact_readback':True,'merged':True,'merge_commit':merge['merge_commit'],'merged_at':merge['merged_at'],'audited_and_merged_head':cfg['head'],'scope':cfg['limitations'],'AI_used_extensively':True,'unrefereed':True,'human_peer_review':False,'immutable_package_unchanged_since_publication':True,'original_stage_records_unchanged':True,'QUEUE_not_used_as_acceptance_source':True,'fresh_whole_package_reviews':cfg['fresh_complete_reviews'],'final_review_actionable_issues':0,'files':cfg['files'],'priority_novelty_worldwide_openness':'UNKNOWN','metadata_normalizations':pub.get('metadata_normalizations',[])}
  for old in state['accepted_results']:
   if old['pr']==n:need(old['doi']==pub['doi'] and old['audited_and_merged_head']==cfg['head'] and old['merge_commit']==merge['merge_commit'],'Conflicting earlier completion')
  state['completed_prs']=sorted(set(state['completed_prs']+[n]));state['accepted_results']=[r for r in state['accepted_results']if r['pr']!=n]+[accepted];state['publications']=[r for r in state['publications']if r['pr']!=n]+[{k:accepted[k]for k in ['pr','doi','record_url','scope','published','tracker_row','merged','merge_commit']}]
  for k in ['clean_preprint_ready_pending_prior_cursor_prs','preprint_preparation_prs','fresh_package_review_pending_prs','clean_preprint_finalization_pending_prs','root_preprint_review_pending_prs','root_terminal_admin_adoption_pending_prs']:
   if isinstance(state.get(k),list):state[k]=[v for v in state[k]if v!=n]
  remaining=[p for p in state['candidate_full_claim_prs']if p not in state['completed_prs']];state['next_pr']=min(remaining)if remaining else None;state['phase']='ordered_publication_tracking_exact_head_merges'if remaining else 'all18_candidate_workflows_complete_83_partial_prior_exclusions';state['estimated_completion_percent']=70+round(30*(len(state['completed_prs'])-4)/14);state['updated_utc']=now();state['last_goal_turn_classification']='PROGRESS_CONFIRMED_PUBLICATION_TRACKER_AND_EXACT_HEAD_MERGE'
  registry=read(D/'CLAIM_REGISTRY.json');registry['updated_utc']=now();matched=[]
  for row in registry['records']:
   if row['pr']==n:row.update({'workflow_outcome':'PUBLISHED_TRACKED_EXACT_HEAD_MERGED','root_disposition':'ACCEPTED_SCOPED_RESULT_PRIORITY_UNESTABLISHED','doi':pub['doi'],'record_url':pub['record_url'],'tracker_row':tracker['sheet_row'],'merge_commit':merge['merge_commit'],'updated_utc':now(),'publication_ready':True,'published':True,'current_workflow_receipt':str((O/'MERGE_VERIFIED.json').relative_to(D))});matched.append(row)
  need(len(matched)==1,'Registry PR must exist exactly once');save(D/'CLAIM_REGISTRY.json',registry)
  marker='[EXTERNAL_COMPLETION_PR_'+str(n)+']'
  log=D/'RESEARCH_LOG.md';text=log.read_text()
  if marker not in text:atomic_text(log,text+'\n'+event['utc']+' — Overall completion estimate'+str(state['estimated_completion_percent'])+'%. PR'+str(n)+' published '+pub['doi']+', exact tracker row'+str(tracker['sheet_row'])+', exact audited head merged '+merge['merge_commit']+'. Native metadata/files verified; DOI resolution '+str(pub.get('doi_resolution',{}).get('status'))+'. Earlier original/stage bytes unchanged. Priority/novelty/current worldwide openness UNKNOWN and openly qualified. Next ascending candidate '+str(state['next_pr'])+'. '+marker+'\n')
  overview=D/'README.md';text=overview.read_text()
  if marker not in text:atomic_text(overview,text+'\nPublication checkpoint '+event['utc']+': #'+str(n)+' [preprint]('+pub['doi_url']+'), tracker row'+str(tracker['sheet_row'])+', exact-head merge`'+merge['merge_commit']+'`; overall'+str(state['estimated_completion_percent'])+'%. Next candidate'+str(state['next_pr'])+'. '+marker+'\n')
  # The cursor advances only AFTER registry and both navigation/log records.
  # Every rerun reconciles them, including a legacy already-completed state.
  save(D/'STATE.json',state);save(O/'COMPLETION_RECONCILED.json',{'utc':now(),'event':ident(event_path),'registry_current_entry':matched[0],'state_saved_last':True,'log_and_overview_markers_present':True})
  print(json.dumps({'status':'WORKFLOW_COMPLETED','pr':n,'doi':pub['doi'],'next_pr':state['next_pr'],'completion_percent':state['estimated_completion_percent']}));return
if __name__=='__main__':main()
