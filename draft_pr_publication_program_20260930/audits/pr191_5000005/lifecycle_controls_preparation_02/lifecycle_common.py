"""PROPOSED PR191 controls. Import is inert; all operational entrypoints are gated.

Install beside ROOT_PUBLICATION_GATE.json only after Root review. Never run from
this proposal folder against production. Use Python -B; native API helpers load
lazily after gate validation. No local Git operations or ref updates are provided.
"""
from pathlib import Path
import base64,copy,datetime,hashlib,importlib.util,json,re,shutil,subprocess,sys
A=Path(__file__).resolve().parent
PR=191;PROBLEM=5000005;HEAD='a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe';NEXT=192
ORIGINAL_BASE='cebdd3818a49a3e8bb2be4664a810b6b53a15c5e'
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr191_5000005/';NATIVE='unsolved_math_prioritization/attempts/5000005/'
SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';GID=1254632077;TAB='Math Puzzles';HEADER=['Original Problem','Solution Chat URL','DOI','Notes']
REPO='AlecKriebel/Math';R=Path('/Users/alec/Documents/Math');PY='/opt/homebrew/opt/python@3.14/bin/python3.14';GWS='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
CLAIM='The imported global bare-A0/signed-rule conjunction is false for every n>=5. The explicitly parity-selected K_PS signed law and first-vertex existence hold for all n>=3 with actual admissible angles and even ell for even n. Ferudun DOI10.5281/zenodo.23267641 already gives the exact theorem, convention repair and overlapping mechanisms; classical inputs are credited. No novelty, firstness, current openness, authenticated author erratum or independent-discovery certification. Extensive AI; unrefereed; no conventional human peer review.'
JSON_FACTS={'CURRENT_RESULT.json','readiness.json','PUBLICATION.json','PUBLICATION_PACKAGE_PLAN.json','ROOT_SCOPE_RECORD.json','review/WHOLE_PACKAGE_REVIEW_STATUS.json','review/NEW_MATH_AND_PRIORITY_AUDITS.json','review/review_manifest.json'}
TEXT_FACTS={'README.md','review/REVIEW.md'}
CONTROL_FILES=['lifecycle_common.py','campaign_aliases.py','run_zenodo_step.py','record_tracker.py','prepare_native_final_01.py','prepare_pr_metadata_request.py','prepare_final_main_scope.py','prepare_final_scoped_merge.py','prepare_factual_completion.py']
def require(x,msg):
 if not x:raise RuntimeError(msg)
def now():return datetime.datetime.now(datetime.UTC).isoformat()
def read(p):return json.loads(Path(p).read_text())
def pin(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def write(p,value):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():p.chmod(0o644)
 p.write_text(value if isinstance(value,str) else json.dumps(value,indent=2)+'\n')
def safe_rel(n):
 require(isinstance(n,str) and n and not Path(n).is_absolute() and '..' not in Path(n).parts,'Unsafe relative path')
 require(not any(x in n.lower() for x in ['private','chrome','__pycache__','.zenodo','preappend_fresh_read','raw_http','headers','access_token']),'Private/cache/raw path forbidden '+n)
 return n
def inside(n):
 n=safe_rel(n);p=A/n;require(p.resolve().is_relative_to(A.resolve()),'Path escapes case')
 require(not any(q.is_symlink() for q in [p,*p.parents] if q.is_relative_to(A)),'Symlink in selected path')
 return p
def match(p,x):
 actual=pin(p);digest=x.get('sha256',x.get('SHA256'));require(re.fullmatch('[0-9a-f]{64}',digest or '') is not None,'Invalid SHA256')
 require(actual['sha256']==digest and actual['bytes']==x['bytes'],'Bound bytes drift '+str(p));return actual
def review_bindings(g):return [entry[k] for entry in g['whole_package_reviews'] for k in ['report','seal','root_authentication']]
def inventory(T):
 paths=list(T.rglob('*'));require(not any(p.is_symlink() for p in paths),'Symlink in native inventory');return {p.relative_to(T).as_posix() for p in paths if p.is_file()}
def approved_media(g,n):
 if Path(n).suffix.lower() not in ['.pdf','.png','.jpg','.jpeg','.zip']:return
 actual=pin(inside(n));approved=[g['payloads'][g['paper_files'][k]] for k in ['pdf','support']]
 require(any(actual['sha256']==x.get('sha256',x.get('SHA256')) and actual['bytes']==x['bytes'] for x in approved),'Unapproved body/derivative/archive '+n)
def gate():
 g=read(A/'ROOT_PUBLICATION_GATE.json')
 require(g.get('schema')=='PR191_LIFECYCLE_GATE_V1' and g.get('status')=='READY_FOR_AUTHORIZED_PUBLICATION','Final Root gate absent/unrecognized')
 require((g['PR'],g['original_head'])==(PR,HEAD),'Wrong original PR/head')
 require(g['qualified_note_route_authorized'] is True and g['historical_priority_clearance'] is False and g['all_required_findings_globally_resolved'] is True,'Qualified route/review gate')
 reviews=g['whole_package_reviews'];require(isinstance(reviews,list) and len(reviews)>=2 and all(isinstance(x,dict) and {'reviewer_id','disposition','authoritative','report','seal','root_authentication'}<=set(x) for x in reviews),'Per-review report/seal/authentication schema required')
 require(all(isinstance(x['reviewer_id'],str) and x['reviewer_id'] and x['authoritative'] is True and x['disposition'] in ['PASS','REPAIR_REQUIRED'] for x in reviews),'Authoritative review identities/dispositions required')
 require(len({x['reviewer_id'] for x in reviews})==len(reviews) and reviews[-1]['disposition']=='PASS' and g['last_review_required_repairs']==0,'Distinct successive reviewers/latest clean required')
 require(all(len({x[k]['path'] for x in reviews})==len(reviews) for k in ['report','seal','root_authentication']) and all(len({x[k]['path'] for k in ['report','seal','root_authentication']})==3 for x in reviews),'Distinct per-review evidence paths required')
 for x in review_bindings(g):match(inside(x['path']),x)
 P=inside(g['package_name']);require(P.is_dir(),'Package absent')
 require(set(g['paper_files'].values())<=set(g['payloads']) and set(g['paper_files'])=={'pdf','source','support','metadata'},'Paper role schema')
 for n,x in g['payloads'].items():match(inside(g['package_name']+'/'+safe_rel(n)),x)
 z=read(P/g['paper_files']['metadata']);require(isinstance(z['files'],list) and len(z['files'])==3,'Exact three upload payloads required')
 require({x.get('name',Path(x['path']).name) for x in z['files']}=={g['paper_files'][k] for k in ['pdf','source','support']},'Upload file set differs from roles')
 for x in z['files']:
  require(safe_rel(x['path']) in g['payloads'] and (P/x['path']).resolve().is_relative_to(P.resolve()),'Upload path outside frozen payloads')
 match(inside(g['current_proof']['path']),g['current_proof'])
 nm=read(match_path(g['native_pending_manifest']));require(nm['current_template']==g['native_pending_template'],'Native predecessor manifest mismatch')
 files=nm['files'];require(isinstance(files,dict) and files,'Native manifest schema')
 T=inside('integration_preparation/'+g['native_pending_template'])
 require(inventory(T)==set(files),'Pending native inventory differs from manifest')
 for n,x in files.items():
  require(not (T/safe_rel(n)).is_symlink() and (T/n).resolve().is_relative_to(T.resolve()),'Native symlink/path escape');match(T/n,x)
 require(g['native_proof_paths'] and all(n in files and pin(T/n)['sha256']==g['current_proof']['sha256'] for n in g['native_proof_paths']),'Native/current proof identity')
 require(set(g['native_json_status_paths'])==JSON_FACTS & set(files),'Declare every known live JSON alias')
 require(set(g['native_text_status_replacements'])==TEXT_FACTS & set(files),'Declare reviewed factual text replacements')
 for n,old in g['native_text_status_replacements'].items():require(isinstance(old,str) and old and (T/n).read_text().count(old)==1,'Nonunique factual status text '+n)
 original=read(A/'ORIGINAL_FILE_MANIFEST.json');require(original['original_head']==HEAD and len(original['files'])==16,'Original16 custody')
 for x in original['files']:
  n=Path(x['path']).relative_to(NATIVE);match(T/'ORIGINAL_SUBMISSION'/n,x)
 for k in ['pr_metadata_proposal','tracker_row_proposal','review_input']:match_path(g[k])
 require(isinstance(g['public_case_pins'],dict),'Immutable public scope pins required')
 for n,x in g['public_case_pins'].items():match(inside(n),x);approved_media(g,n)
 for n in g['public_case_paths']:inside(n);approved_media(g,n)
 require(g['native_final_template'].startswith('native_template_final_') and g['native_complete_template'].startswith('native_template_complete_'),'Native generations')
 safe_rel(g['native_final_template']);safe_rel(g['native_complete_template'])
 return g
def match_path(x):p=inside(x['path']);match(p,x);return p
_helpers=None
def helpers():
 global _helpers
 if _helpers is None:
  gate();require(sys.dont_write_bytecode,'Invoke operational scripts with Python -B')
  p=A.parent/'pr190_5000007/prepare_final_scoped_merge.py'
  spec=importlib.util.spec_from_file_location('audited_native_objects_for_191',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  m.m.TREE_CACHE_PATH=A/'lifecycle_private/IMMUTABLE_TREE_CACHE.json';_helpers=m
 return _helpers
def original_ready(draft=None):
 p=helpers().api('pulls/'+str(PR));require(p['head']['sha']==HEAD and p['state']=='open' and not p['merged'],'Original head/open state drift')
 if draft is not None:require(p['draft'] is draft,'PR draft/ready state drift')
 return p
def publication(g=None):
 g=g or gate();z=read(A/'ZENODO_PUBLICATION_READBACK.json')
 require(z['state']=='published' and z['environment']=='production' and isinstance(z['id'],int) and z['id']>0,'Actual production publication absent')
 require(re.fullmatch(r'10\.[0-9]{4,9}/\S+',z['doi'] or '') and z['doi_url']=='https://doi.org/'+z['doi'],'Actual DOI invalid')
 require(z['gate_sha256']==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Publication belongs to another gate')
 expected={g['paper_files'][k]:(g['payloads'][g['paper_files'][k]]['bytes'],g['payloads'][g['paper_files'][k]].get('sha256',g['payloads'][g['paper_files'][k]].get('SHA256'))) for k in ['pdf','source','support']}
 require(isinstance(z.get('files'),list) and len(z['files'])==3 and {x['name']:(x['size'],x['sha256']) for x in z['files']}==expected,'Publication exact uploaded file pins absent/different')
 return z
def published_tracked():
 g=gate();z=publication(g);tr=read(A/'TRACKER_ACCEPTANCE.json')
 require(tr['status']=='TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED' and tr['DOI']==z['doi'] and (tr['spreadsheet_id'],tr['gid'],tr['tab'])==(SID,GID,TAB) and tr['actual_fresh_reads']==2,'Actual tracker acceptance absent')
 require(tr['gate_sha256']==z['gate_sha256'],'Tracker gate binding drift');return g,z,tr
def sanitize_zenodo(j):
 return {k:j[k] for k in ['environment','id','state','doi','doi_url','record_url','files','metadata_normalizations','doi_resolution','receipt_saved'] if k in j}
def run_zenodo(action,confirm_id=None,runner=subprocess.run):
 g=gate();require(action in ['check','stage','inspect','publish','inspect-published'],'Unknown action')
 if action in ['stage','publish']:original_ready()
 private=A/'lifecycle_private';private.mkdir(exist_ok=True)
 def call(cmd):
  args=[PY,'-E','-S','-B','-P',str(R/'zenodo_deposit_tool/zenodo.py'),cmd,str(A/g['package_name']/g['paper_files']['metadata'])]
  if cmd=='publish':args+=['--confirm-id',str(confirm_id)]
  if action=='inspect-published':args+=['--check-doi']
  r=runner(args,cwd=R,capture_output=True,timeout=300);(private/('ZENODO_'+cmd+'.stdout')).write_bytes(r.stdout);(private/('ZENODO_'+cmd+'.stderr')).write_bytes(r.stderr)
  require(r.returncode==0,'Uploader result unconfirmed; reconcile existing state; no blind retry')
  j=json.loads(r.stdout);require(j.get('environment')=='production','Wrong Zenodo environment');return j
 marker=private/'ZENODO_STAGE_ATTEMPT_STARTED.json'
 if action=='stage':
  if marker.exists():
   require(read(marker).get('gate_sha256')==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Stage marker belongs to another gate; reconcile existing state')
   current=call('inspect')
   if current['state']=='published':current.update(gate_sha256=pin(A/'ROOT_PUBLICATION_GATE.json')['sha256']);write(A/'ZENODO_PUBLICATION_READBACK.json',sanitize_zenodo(current)|{'gate_sha256':current['gate_sha256']});return current
   if read(marker).get('id') is not None:require(current['id']==read(marker)['id'],'Existing draft ID drift')
  else:write(marker,{'UTC':now(),'gate_sha256':pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'automatic_second_creation_forbidden':True})
 if action=='publish':
  st=read(A/'ZENODO_STAGE_READBACK.json');require(str(st['id'])==str(confirm_id) and st['gate_sha256']==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Exact actual staged ID/gate required')
  current=call('inspect');require(current['id']==st['id'],'Existing draft ID drift')
  if current['state']=='published':j=current
  else:
   attempt=private/'ZENODO_PUBLISH_ATTEMPT_STARTED.json';require(not attempt.exists(),'Earlier publication outcome requires explicit reconciliation; no second POST')
   write(attempt,{'UTC':now(),'id':st['id'],'gate_sha256':st['gate_sha256']});j=call('publish')
 else:j=call('inspect' if action=='inspect-published' else action)
 out=sanitize_zenodo(j)|{'gate_sha256':pin(A/'ROOT_PUBLICATION_GATE.json')['sha256']}
 filename={'check':'ZENODO_LOCAL_CHECK.json','stage':'ZENODO_STAGE_READBACK.json','inspect':'ZENODO_DRAFT_READBACK.json','publish':'ZENODO_PUBLICATION_READBACK.json','inspect-published':'ZENODO_POSTPUBLICATION_INSPECTION.json'}[action]
 write(A/filename,out)
 if action=='stage':write(marker,{'UTC':now(),'id':j['id'],'gate_sha256':out['gate_sha256'],'automatic_second_creation_forbidden':True})
 if j.get('state')=='published':write(A/'ZENODO_PUBLICATION_READBACK.json',out)
 return out
def gws(resource,method,params,body=None,runner=subprocess.run):
 args=[GWS,'sheets','spreadsheets']+(['values'] if resource=='values' else [])+[method,'--params',json.dumps(params)]
 if body is not None:args+=['--json',json.dumps(body)]
 r=runner(args,capture_output=True,timeout=90);require(r.returncode==0,'GWS outcome unconfirmed; inspect existing state before retry');return json.loads(r.stdout)
def record_tracker(call=gws):
 g=gate();z=publication(g);D=A/'sheets_tracking';D.mkdir(exist_ok=True)
 if (A/'TRACKER_ACCEPTANCE.json').exists():
  write(A/'lifecycle_private/TRACKER_ACCEPTANCE_PREVIOUS.json',read(A/'TRACKER_ACCEPTANCE.json'));(A/'TRACKER_ACCEPTANCE.json').unlink()
 target=call('spreadsheet','get',{'spreadsheetId':SID,'fields':'spreadsheetId,sheets(properties(sheetId,title))'})
 require(target['spreadsheetId']==SID and [s['properties']['title'] for s in target['sheets'] if s['properties']['sheetId']==GID]==[TAB],'Actual sheet/gid/tab mismatch')
 header=call('values','get',{'spreadsheetId':SID,'range':"'Math Puzzles'!A1:D1",'valueRenderOption':'UNFORMATTED_VALUE'})
 require(header.get('values')==[HEADER],'Actual tracker header mismatch')
 write(D/'TARGET_VALIDATION.json',{'spreadsheet_id':SID,'gid':GID,'tab':TAB,'header':HEADER,'UTC':now()})
 proposal=read(match_path(g['tracker_row_proposal']));row=[proposal['original_problem'],proposal.get('solution_chat_url',''),z['doi_url'],proposal['notes']]
 require(all(isinstance(c,str) for c in row) and row[0] and row[3],'Reviewed tracker proposal schema')
 full=call('values','get',{'spreadsheetId':SID,'range':"'Math Puzzles'!A:D",'valueRenderOption':'UNFORMATTED_VALUE'})
 require(full.get('values',[[]])[0]==HEADER,'Full read/header drift')
 hits=[i for i,r in enumerate(full['values'],1) if any(z['doi'] in str(c) for c in r)]
 require(len(hits)<=1,'Duplicate DOI rows; no append')
 if hits:
  i=hits[0];require(full['values'][i-1]==row,'False or conflicting existing DOI match; no append');rng=f"'Math Puzzles'!A{i}:D{i}"
 else:
  marker=D/'APPEND_ATTEMPT_STARTED.json';require(not marker.exists(),'Unknown earlier append outcome; no automatic second write')
  params={'spreadsheetId':SID,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True};body={'majorDimension':'ROWS','values':[row]}
  write(D/'APPEND_REQUEST.json',{'params':params,'body':body});write(marker,{'UTC':now(),'DOI':z['doi'],'automatic_second_write_forbidden':True})
  r=call('values','append',params,body);u=r['updates'];rng=u['updatedRange'];m=re.fullmatch(r"'?Math Puzzles'?!A([0-9]+):D([0-9]+)",rng)
  require(m and m[1]==m[2] and u['updatedRows']==1 and u['updatedColumns']==4,'Unexpected append response dimensions/range')
  write(D/'APPEND_RESPONSE.json',{'updatedRange':rng,'updatedRows':1,'updatedColumns':4})
 for i in [1,2]:
  actual=call('values','get',{'spreadsheetId':SID,'range':rng,'valueRenderOption':'UNFORMATTED_VALUE'});require(actual.get('values')==[row],'Fresh own row read differs');write(D/f'ROW_READBACK_{i}.json',{'range':rng,'values':[row],'UTC':now()})
  target=call('spreadsheet','get',{'spreadsheetId':SID,'fields':'spreadsheetId,sheets(properties(sheetId,title))'});require(target['spreadsheetId']==SID and [s['properties']['title'] for s in target['sheets'] if s['properties']['sheetId']==GID]==[TAB],'Postappend target sheet/gid/tab drift')
  post=call('values','get',{'spreadsheetId':SID,'range':"'Math Puzzles'!A:D",'valueRenderOption':'UNFORMATTED_VALUE'});postrows=post.get('values',[]);require(postrows and postrows[0]==HEADER,'Postappend header drift')
  hits_after=[j for j,r in enumerate(postrows,1) if any(z['doi'] in str(v) for v in r)];require(len(hits_after)==1 and postrows[hits_after[0]-1]==row,'Postappend duplicate/conflicting DOI rows; reconcile without deleting rows')
  target_match=re.fullmatch(r"'?Math Puzzles'?!A([0-9]+):D([0-9]+)",rng);require(target_match and int(target_match[1])==int(target_match[2])==hits_after[0],'Own tracker row moved after readbacks; reconcile')
  before_foreign=[r for r in full['values'] if not any(z['doi'] in str(v) for v in r)];after_foreign=[r for r in postrows if not any(z['doi'] in str(v) for v in r)];cursor=iter(after_foreign)
  require(all(any(candidate==r for candidate in cursor) for r in before_foreign),'Pre-existing foreign row content/order changed; reconcile without automatic repair')
  write(D/f'POSTAPPEND_UNIQUENESS_{i}.json',{'UTC':now(),'range':rng,'DOI':z['doi'],'own_row':row,'matching_DOI_rows':1,'preexisting_foreign_rows_retained':True})
 out={'UTC':now(),'status':'TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED','spreadsheet_id':SID,'gid':GID,'tab':TAB,'range':rng,'DOI':z['doi'],'row':row,'actual_fresh_reads':2,'gate_sha256':z['gate_sha256']};write(A/'TRACKER_ACCEPTANCE.json',out);return out
def normalize(j,phase):
 require(phase in [95,100] and j['current_PR']==PR,'Wrong phase/case');expected=(39,23,190) if phase==95 else (40,24,191)
 require((j['fully_completed_count'],j['published_count'],j['last_completed_PR'])==expected,'Programme census drift')
 obsolete=['actual_factual_checkpoint_accepted','active_checkpoint_commit','last_completed_writer_operation_finished','read_only_next_case','next_intake_requires_actual_completion_receipt_and_explicit_writer_release']
 archive=obsolete+['program_snapshot_semantics','program_snapshot_authority_condition','remaining_current_step','next_step','active_checkpoint_acceptance_receipt','latest_ordered_intake_record'];old={k:copy.deepcopy(j[k]) for k in archive if k in j}
 if old:j.setdefault('retired_live_aliases_PR191',[]).append({'UTC':now(),'phase':phase,'values':old})
 for k in obsolete:j.pop(k,None)
 require(j['dated_eligible_total']==99,'Dated denominator drift');j['fully_completed_fraction_percent']=round(100*j['fully_completed_count']/99,2);j['workflow_estimate_percent']=j['fully_completed_fraction_percent']
 intake=read(A/'INTAKE_CHECKPOINT_ACCEPTANCE.json');require(intake['PR']==PR and intake['original_head']==HEAD and re.fullmatch('[0-9a-f]{40}',intake['checkpoint_commit']),'Actual intake identity drift');g=gate()
 j.update(workflow_estimate_definition=f"{j['fully_completed_count']}/dated99 completed,{j['published_count']} published; dated denominator is not a fresh eligibility census.",last_completed_actual_final_receipt='audits/'+('pr190_5000007' if phase==95 else 'pr191_5000005')+'/ROOT_FINAL_FACTUAL_ACCEPTANCE.json',last_actual_intake_checkpoint_commit=intake['checkpoint_commit'],last_actual_intake_checkpoint_release='audits/pr191_5000005/INTAKE_CHECKPOINT_ACCEPTANCE.json',latest_ordered_intake_record='status_intakes_after_pr190/PR191_ORIGINAL_STATUS_INTAKE.json',next_intake_requires_actual_completion_receipt=True,next_intake_requires_explicit_writer_release=False,peer_pause_or_exclusive_writer_window_assumed=False,next_eligible_PR_after_current_completion=None,next_eligible_order_requires_fresh_status_check=True,next_numeric_intake_cursor=NEXT,advance_to_next_PR_authorized_now=phase==100,persistent_goal_complete=False,current_original_head=HEAD,current_original_budget='2/5',current_problem_id=PROBLEM,current_mathematical_result_valid=True,current_mathematical_scope=CLAIM,current_priority_clearance=False,current_historical_firstness_or_guaranteed_novelty_certified=False,current_source_author_authenticated_erratum=False,current_source_unique_intent_certified=False,current_publication_gate='audits/pr191_5000005/ROOT_PUBLICATION_GATE.json',current_current_proof='audits/pr191_5000005/'+g['current_proof']['path'],current_whole_package_review_input='audits/pr191_5000005/'+g['review_input']['path'],current_publication_package_review_round=len(g['whole_package_reviews']),current_publication_package_review_status='Successive NEW full-package reviews complete; last clean',current_present_open_status_verified=False)
 receipt='ROOT_ACTUAL_MERGE_ACCEPTANCE.json' if phase==95 else 'ROOT_FINAL_FACTUAL_ACCEPTANCE.json'
 j['active_checkpoint_acceptance_receipt']='audits/pr191_5000005/'+receipt;j['program_snapshot_authority_condition']='Effective only after actual current-tree full-scope acceptance in '+j['active_checkpoint_acceptance_receipt']+('; actual factual completion required before intake192.' if phase==95 else '; actual factual acceptance required before intake192.')
 j['remaining_current_step']='PR191 original-head merge/current-tree acceptance and factual completion; only then intake192.' if phase==95 else 'None for PR191 after actual factual acceptance; original-status-only intake192 next.';j['next_step']=j['remaining_current_step'];j['completion_metadata_checkpoint_pending_at_snapshot']=phase==95
 j['program_snapshot_semantics']='Actual credited PR191 note publication and tracker accepted; '+('39completed/23published remain, original-head merge and factual acceptance pending.' if phase==95 else 'Original-head merge accepted;40completed/24published factual postimage is effective only after actual current-MAIN factual acceptance before intake192.')+' No firstness, novelty, present openness or independence certification; broader goal active.'
 return j
def factual_sentence(z,tr,merged):return 'The successive NEW whole-package review loop is complete and final clean. Exact note '+z['doi_url']+' is actually published and tracker '+tr['range']+' was verified twice. Original-head merge '+('was actually accepted; final factual MAIN acceptance follows separately.' if merged else 'remains pending at this preparation.')+' Extensive AI; unrefereed.'
def native_status(T,g,z,tr,merged=False):
 stamp=now();common={'UTC':stamp,'whole_package_reviews_complete':True,'publication_ready':True,'actual_Zenodo_published':True,'actual_published':True,'actual_DOI':z['doi'],'actual_tracker_updated':True,'actual_tracker_range':tr['range'],'actual_original_PR_merged':merged,'case_percent':100 if merged else 95,'snapshot_semantics':'Actual publication/tracker facts; original-head merge '+('accepted' if merged else 'pending at this preparation')+'; factual MAIN adoption requires separate actual acceptance.'}
 updates={'whole_package_reviews_pending':False,'successive_NEW_whole_package_reviews_complete':True,'publication_clearance':True,'publication_and_tracker_actions_not_yet_performed':False,'not_an_approval':False,'completed_new_whole_package_reviews':len(g['whole_package_reviews'])}
 changed=[]
 for n in g['native_json_status_paths']:
  old=read(T/n);j=copy.deepcopy(old)
  for k,v in common.items():
   if k in j:j[k]=v
  for k,v in updates.items():
   if k in j:j[k]=v
  if n=='PUBLICATION.json':j.update(UTC=stamp,kind='ACTUAL_PUBLISHED_TRACKED_CREDITED_NOTE',package=g['package_name'],paper=g['paper_files']['pdf'],source=g['paper_files']['source'],support=g['paper_files']['support'],metadata=g['paper_files']['metadata'],actual_DOI=z['doi'],actual_Zenodo_published=True,actual_tracker_range=tr['range'],actual_original_PR_merged=merged,whole_package_review_status='Successive NEW whole-package reviews completed; final clean',gate_sha256=pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'])
  if n=='PUBLICATION_PACKAGE_PLAN.json':j.update(package_case_relative=CASE+g['package_name']+'/',planned_files=[g['paper_files'][k] for k in ['pdf','source','support']],actual_published=True,actual_DOI=z['doi'],publication_ready=True)
  if n=='review/WHOLE_PACKAGE_REVIEW_STATUS.json':j.update(status='SUCCESSIVE_NEW_COMPLETE_PACKAGE_REVIEWS_FINAL_CLEAN',not_an_approval=False,completed_new_whole_package_reviews=len(g['whole_package_reviews']),paper_science_and_current_native_template_require_review=False)
  write(T/n,j);changed.append(n)
 factual=factual_sentence(z,tr,merged)
 for n,needle in g['native_text_status_replacements'].items():
  s=(T/n).read_text()
  if not merged:require(s.count(needle)==1,'Reviewed factual sentence drift');s=s.replace(needle,factual)
  else:previous=factual_sentence(z,tr,False);require(s.count(previous)==1,'Nonunique generated95 factual sentence');s=s.replace(previous,factual)
  write(T/n,s);changed.append(n)
 write(T/'RESEARCH_LOG.md',(T/'RESEARCH_LOG.md').read_text()+'\n'+stamp+' — '+factual+' Original effort2/5 retained. '+('40/24 factual postimage requires actual MAIN acceptance.' if merged else '39completed/23published until actual factual acceptance.')+'\n');changed.append('RESEARCH_LOG.md')
 return changed
def prepare_native(merged=False):
 g,z,tr=published_tracked();I=A/'integration_preparation'
 if merged:
  a=read(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json');require(a['PR_merged'] and a['every_selected_identity_checked_at_actual_observed_MAIN'],'Accepted actual merge absent')
  current=read(I/'CURRENT_TEMPLATE.json');src=I/current['current_template'];old=current['files'];name=g['native_complete_template']
 else:
  manifest=read(match_path(g['native_pending_manifest']));src=I/g['native_pending_template'];old=manifest['files'];name=g['native_final_template']
 T=I/name
 if T.exists():
  cur=current_native(g,merged);require(cur['current_template']==name and cur['actual_original_PR_merged'] is merged,'Existing generation differs')
  case=read(A/'CURRENT_CASE_STATUS.json');require(case['original_PR_merged'] is merged and case['DOI']==z['doi'],'Interrupted existing native generation; reconcile factual case')
  require(read(T/'PUBLICATION.json')['gate_sha256']==z['gate_sha256'],'Existing native generation belongs to another gate');return cur
 for n,x in old.items():match(src/n,x)
 shutil.copytree(src,T);changed=native_status(T,g,z,tr,merged)
 for n,x in old.items():
  if n not in changed:match(T/n,x)
 original=read(A/'ORIGINAL_FILE_MANIFEST.json')
 for x in original['files']:match(T/'ORIGINAL_SUBMISSION'/Path(x['path']).relative_to(NATIVE),x)
 files={n:pin(T/n) for n in old}
 for n in files:(T/n).chmod(0o444)
 cur={'UTC':now(),'current_template':name,'files':files,'original_head':HEAD,'reviewed_scientific_bytes_preserved':True,'only_declared_factual_paths_changed':changed,'actual_original_PR_merged':merged,'MAIN_updated_by_preparation':False};write(I/'CURRENT_TEMPLATE.json',cur);write(I/(name+'_MANIFEST.json'),cur)
 case=read(A/'CURRENT_CASE_STATUS.json');case.update(UTC=now(),status='ACTUAL_NOTE_PUBLISHED_TRACKED_'+('MERGE_ACCEPTED_FACTUAL_POSTIMAGE_PENDING' if merged else 'ORIGINAL_HEAD_MERGE_PENDING'),case_percent=100 if merged else 95,publication_ready=True,whole_package_reviews_complete=True,whole_package_reviews=g['whole_package_reviews'],first_whole_package_review_active=False,Zenodo_published=True,DOI=z['doi'],tracker_updated=True,tracker_range=tr['range'],original_PR_merged=merged,PR_closed=merged,current_proof=g['current_proof']['path'],current_proof_SHA256=g['current_proof']['sha256'],remaining_required_steps='Actual factual MAIN acceptance before intake192.' if merged else 'Original-head MAIN merge/full current-tree acceptance and factual completion before intake192.');write(A/'CURRENT_CASE_STATUS.json',case)
 write(A/'RESEARCH_LOG.md',(A/'RESEARCH_LOG.md').read_text()+'\n'+now()+' — '+case['status']+'; science/original16 preserved; broader goal active.\n');return cur
def current_native(g,merged=False):
 cur=read(A/'integration_preparation/CURRENT_TEMPLATE.json');name=g['native_complete_template'] if merged else g['native_final_template'];require(cur['current_template']==name,'Native current generation drift')
 pending=read(match_path(g['native_pending_manifest']))['files'];require(set(cur['files'])==set(pending),'Native selected file set is incomplete')
 T=inside('integration_preparation/'+name);require(inventory(T)==set(cur['files']),'Current native inventory differs from manifest');factual=JSON_FACTS|TEXT_FACTS|{'RESEARCH_LOG.md'}
 for n,x in cur['files'].items():
  match(T/safe_rel(n),x)
  if n not in factual:match(T/n,pending[n])
 return cur
def require_merge_scope(g,r):
 native=read(match_path(g['native_pending_manifest']))['files']
 mandatory={NATIVE+n for n in native}|{CASE+g['package_name']+'/'+n for n in g['payloads']}
 require(mandatory<=set(r['selected_files']),'Merge map omits reviewed native/package files')
def metadata_expected(g,z,tr):
 p=read(match_path(g['pr_metadata_proposal']));require(set(p)=={'title','body_before_publication'} and all(isinstance(x,str) and x for x in p.values()),'Reviewed metadata proposal schema')
 body=p['body_before_publication'].rstrip()+'\n\nPublished credited note: ['+z['doi']+']('+z['doi_url']+'). Successive NEW whole-package reviews completed; final clean. Actual tracker '+tr['range']+' verified by two fresh reads. Original-head MAIN merge follows separately. All16 original artifacts remain byte-exact in ORIGINAL_SUBMISSION; historical effort2/5 retained. '+CLAIM+'\n'
 return {'expected_original_head':HEAD,'request':{'repository_full_name':REPO,'pr_number':PR,'title':p['title'],'body':body},'gate_sha256':z['gate_sha256']}
def metadata_request():
 g,z,tr=published_tracked();out={'UTC':now(),'state':'PREPARED_METADATA_NOT_SENT',**metadata_expected(g,z,tr)};write(A/'PR_METADATA_REQUEST.json',out);return out
def require_metadata(g,z,tr,p):
 request=read(A/'PR_METADATA_REQUEST.json');expected=metadata_expected(g,z,tr);require(all(request[k]==v for k,v in expected.items()),'Prepared PR metadata/gate drift')
 require(p['title']==expected['request']['title'] and p['body']==expected['request']['body'],'Actual PR metadata differs from final reviewed request')
 a=read(A/'PR_METADATA_ACCEPTANCE.json');require(a['status']=='ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED' and a['PR']==PR and a['original_head']==HEAD and a['gate_sha256']==z['gate_sha256'] and a['request_sha256']==pin(A/'PR_METADATA_REQUEST.json')['sha256'],'Metadata acceptance binding drift')
def selected_current(h,main,selected,reference=None):
 tree=h.api('git/commits/'+main)['tree']['sha'];h.m.m.h.warm_selected_directories([reference or tree,tree],selected)
 for n,x in selected.items():require(h.lookup(tree,n)==('100644','blob',x['git_blob']),'Selected current MAIN identity drift '+n)
 return tree
def selected_digest(selected):
 require(all(set(x)=={'bytes','sha256','git_blob'} for x in selected.values()),'Selected pin schema differs')
 return hashlib.sha256(json.dumps(selected,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def verify_prepared(h,r,parents):
 require(r.get('original_head')==HEAD and r.get('gate_sha256')==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Preparation head/gate binding drift')
 co=h.api('git/commits/'+r['commit']);require(co['tree']['sha']==r['tree'] and [x['sha'] for x in co['parents']]==parents,'Prepared tree/parent drift')
 parent_tree=h.api('git/commits/'+parents[0])['tree']['sha'];require(r['parent_tree']==parent_tree,'Receipt parent tree differs from actual first parent')
 digest=selected_digest(r['selected_files']);marker='PR191 selected-map SHA256: '+digest;require(r.get('selected_map_sha256')==digest and co.get('message','').splitlines().count(marker)==1,'Immutable commit selected-map binding drift')
 h.m.m.h.warm_selected_directories([parent_tree,r['tree']],r['selected_files'])
 for n,x in r['selected_files'].items():require(h.lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Prepared selected identity drift')
 changed={n for n,x in r['selected_files'].items() if h.lookup(parent_tree,n)!=('100644','blob',x['git_blob'])};require(set(r['changed_paths'])==changed and h.changed_leaves(parent_tree,r['tree'])==changed,'Full-tree foreign scope drift')
 return co
def scope_names(g):
 files=read(match_path(g['native_pending_manifest']))['files'];names=set(g['public_case_paths'])|set(g['public_case_pins'])|set(CONTROL_FILES)|{'ROOT_PUBLICATION_GATE.json','PR_METADATA_REQUEST.json','PR_METADATA_ACCEPTANCE.json','ZENODO_LOCAL_CHECK.json','ZENODO_STAGE_READBACK.json','ZENODO_DRAFT_READBACK.json','ZENODO_PUBLICATION_READBACK.json','ZENODO_POSTPUBLICATION_INSPECTION.json','TRACKER_ACCEPTANCE.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','FINAL_MAIN_SCOPE.json','ORIGINAL_FILE_MANIFEST.json','INTAKE_CHECKPOINT_ACCEPTANCE.json','ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json','integration_preparation/CURRENT_TEMPLATE.json','integration_preparation/'+g['native_final_template']+'_MANIFEST.json'}
 names.update([g['current_proof']['path'],g['native_pending_manifest']['path'],g['review_input']['path'],g['pr_metadata_proposal']['path'],g['tracker_row_proposal']['path']]);names.update(x['path'] for x in review_bindings(g));names.update(g['package_name']+'/'+n for n in g['payloads']);names.update('integration_preparation/'+g['native_final_template']+'/'+n for n in files);names.update('sheets_tracking/'+n for n in ['TARGET_VALIDATION.json','ROW_READBACK_1.json','ROW_READBACK_2.json','POSTAPPEND_UNIQUENESS_1.json','POSTAPPEND_UNIQUENESS_2.json']);return names
def verify_merge_scope(h,g,r,accepted=False):
 verify_prepared(h,r,[r['expected_main'],HEAD]);require_merge_scope(g,r)
 b=h.body_at(CASE+'FINAL_MAIN_SCOPE.json',r['commit']);require(b==(A/'FINAL_MAIN_SCOPE.json').read_bytes(),'Local/immutable prepared scope bytes differ');scope=json.loads(b)
 x=r['selected_files'][CASE+'FINAL_MAIN_SCOPE.json'];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Immutable scope byte/hash binding drift')
 require(scope['PR']==PR and scope['original_head']==HEAD and scope['gate_sha256']==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Immutable scope identity/gate drift')
 actual=set(scope['case_paths']);mandatory=scope_names(g);optional={'sheets_tracking/'+n for n in ['APPEND_REQUEST.json','APPEND_ATTEMPT_STARTED.json','APPEND_RESPONSE.json']};require(len(actual)==len(scope['case_paths']) and mandatory<=actual<=mandatory|optional,'Immutable scope omits/adds intended case paths')
 native=read(match_path(g['native_pending_manifest']))['files'];expected={CASE+n for n in actual}|{NATIVE+n for n in native}|{PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}|{'unsolved_math_prioritization/QUEUE.md'}
 require(len(set(scope['selected_MAIN_paths']))==len(scope['selected_MAIN_paths']) and set(scope['selected_MAIN_paths'])==expected==set(r['selected_files']),'Exact immutable selected MAIN scope differs')
 scope_sha=hashlib.sha256(b).hexdigest()
 if accepted:
  a=read(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json');require(a['PR_merged'] and a['original_head']==HEAD and a['gate_sha256']==r['gate_sha256'] and a['merge_commit']==r['commit'] and a['merge_tree']==r['tree'] and a['selected_map_sha256']==r['selected_map_sha256'] and a['scope_sha256']==scope_sha,'Original accepted merge/scope binding drift')
 return scope_sha
def prepare_tree(h,e,overlay,parents,message,receipt):
 parent=h.api('git/commits/'+e);pins={n:pin(p) for n,p in overlay.items()};entries=[]
 for n,p in overlay.items():
  b=p.read_bytes();entry={'path':n,'mode':'100644','type':'blob'}
  try:entry['content']=b.decode()
  except UnicodeDecodeError:
   blob=h.api('git/blobs','POST',{'content':base64.b64encode(b).decode(),'encoding':'base64'});require(blob['sha']==pins[n]['git_blob'],'Binary blob drift');entry['sha']=blob['sha']
  entries.append(entry)
 tree=h.api('git/trees','POST',{'base_tree':parent['tree']['sha'],'tree':entries});h.m.m.h.warm_selected_directories([parent['tree']['sha'],tree['sha']],pins)
 changed={n for n,x in pins.items() if h.lookup(parent['tree']['sha'],n)!=('100644','blob',x['git_blob'])};require(h.changed_leaves(parent['tree']['sha'],tree['sha'])==changed,'Full-tree foreign scope drift')
 for n,x in pins.items():require(h.lookup(tree['sha'],n)==('100644','blob',x['git_blob']),'Prepared selected identity drift')
 digest=selected_digest(pins);co=h.api('git/commits','POST',{'message':message+'\n\nPR191 selected-map SHA256: '+digest,'tree':tree['sha'],'parents':parents});r={'UTC':now(),'expected_main':e,'parent_tree':parent['tree']['sha'],'tree':tree['sha'],'commit':co['sha'],'original_head':HEAD,'gate_sha256':pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'selected_files':pins,'selected_map_sha256':digest,'changed_paths':sorted(changed),'no_ref_moved_by_this_preparation':True,'peer_pause_or_exclusive_writer_window_assumed':False};verify_prepared(h,r,parents)
 if (A/receipt).exists():
  prior=read(A/receipt);require(re.fullmatch('[A-Za-z0-9_-]+',prior['commit']),'Invalid previous preparation identity');archive=A/'integration_preparation/receipt_history'/(Path(receipt).stem+'_'+prior['commit']+'.json')
  if archive.exists():require(read(archive)==prior,'Previous preparation history collision')
  else:write(archive,prior);archive.chmod(0o444)
 write(A/receipt,r);require(h.api('git/ref/heads/main')['object']['sha']==e,'MAIN advanced; do not adopt stale candidate');return r
def queue_update(before,original,base,doi,url):
 def rows(s):return [l for l in s.splitlines() if '| 5000005 /' in l]
 current,orig,old=rows(before),rows(original),rows(base);require(len(current)==len(orig)==len(old)==1 and orig[0].split('|')[8].strip()=='claimed_solved','Original QUEUE eligibility/identity')
 require(orig[0].split('|')[9].strip()=='2/5','Original effort drift');require(current[0] in [orig[0],old[0]],'Foreign target-row drift');cells=current[0].split('|');require(len(cells)==14,'QUEUE schema')
 cells[8]=' claimed_solved ';cells[9]=' 2/5 ';cells[10]=' https://github.com/AlecKriebel/Math/pull/191 ';cells[11]=' '+CLAIM+' ';cells[12]=' ['+doi+']('+url+') ';after=before.replace(current[0],'|'.join(cells))
 require(len(before.splitlines())==len(after.splitlines()) and sum(x!=y for x,y in zip(before.splitlines(),after.splitlines()))==1,'Foreign QUEUE row delta');return after
def final_scope():
 g,z,tr=published_tracked();cur=current_native(g,False)
 p=original_ready(False);require_metadata(g,z,tr,p)
 names=scope_names(g)-{'FINAL_MAIN_SCOPE.json'}
 for n in ['APPEND_REQUEST.json','APPEND_ATTEMPT_STARTED.json','APPEND_RESPONSE.json']:
  if (A/'sheets_tracking'/n).is_file():names.add('sheets_tracking/'+n)
 for n in names:
  require(inside(n).is_file(),'Missing own public scope file '+n)
  approved_media(g,n)
 names.add('FINAL_MAIN_SCOPE.json');selected={CASE+n for n in names}|{NATIVE+n for n in cur['files']}|{PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}|{'unsolved_math_prioritization/QUEUE.md'}
 additional={CASE+n for n in ['SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json','WORKFLOW_COMPLETION.json','integration_preparation/'+g['native_complete_template']+'_MANIFEST.json']}
 additional.update(CASE+'integration_preparation/'+g['native_complete_template']+'/'+n for n in cur['files'])
 out={'UTC':now(),'PR':PR,'original_head':HEAD,'case_paths':sorted(names),'selected_MAIN_paths':sorted(selected),'factual_additional_paths':sorted(additional),'native_files':len(cur['files']),'foreign_paths_preserved':True,'gate_sha256':z['gate_sha256']};write(A/'FINAL_MAIN_SCOPE.json',out);return out
def progress(j,g,z,tr,phase):
 require((j['fully_completed_count'],j['published_count'],j['last_completed_PR'],j['current_PR'])==(39,23,190,191),'Current programme ownership/census drift')
 if phase==100:
  require(PR not in j['fully_completed_eligible_PRs'] and PR not in j['published_PRs'],'Already counted');j['fully_completed_eligible_PRs'].append(PR);j['published_PRs'].append(PR)
  require(len(set(j['fully_completed_eligible_PRs']))==len(j['fully_completed_eligible_PRs'])==40 and len(set(j['published_PRs']))==len(j['published_PRs'])==24,'Unique factual census')
  j.update(fully_completed_count=40,published_count=24,last_completed_PR=PR,last_published_PR=PR,last_completed_original_head=HEAD,last_completed_original_budget='2/5',last_completed_original_QUEUE_status='claimed_solved',last_completed_DOI=z['doi'],last_published_DOI=z['doi'],last_completed_merge_commit=read(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')['merge_commit'],last_completed_tracker_range=tr['range'],last_completed_record='audits/pr191_5000005/WORKFLOW_COMPLETION.json',last_completed_outcome='published_credited_parity_selected_signed_law_and_literal_counterexamples');j['skipped_before_last_completion']=j.get('skipped_since_last_completion',[]);j['skipped_since_last_completion']=[]
 j.update(UTC=now(),updated_UTC=now(),current_PR=PR,current_status='PUBLISHED_TRACKED_'+('ORIGINAL_HEAD_MERGED_FACTUAL_ACCEPTANCE_REQUIRED' if phase==100 else 'ORIGINAL_HEAD_MERGE_PENDING'),current_PR_workflow_percent=phase,current_workflow_estimate_percent=phase,current_mathematics_cleared=True,current_bounded_priority_audit_complete=True,current_publication_ready=True,current_publication_package_reviews_complete=True,current_publication_package_reviews_required=False,current_Zenodo_published=True,current_DOI=z['doi'],current_tracker_updated=True,current_tracker_range=tr['range'],current_original_PR_merged=phase==100,current_closed=phase==100,current_record='audits/pr191_5000005/CURRENT_CASE_STATUS.json',current_remaining_required_steps='Actual factual MAIN acceptance before intake192.' if phase==100 else 'Original-head merge/full current-tree acceptance and factual completion before intake192.')
 return normalize(j,phase)
def integration_prepare(gen):
 g,z,tr=published_tracked();p=original_ready(False);require_metadata(g,z,tr,p)
 require(re.fullmatch('merge_preparation_[a-z0-9_]+',gen),'Generation name');h=helpers();e=h.api('git/ref/heads/main')['object']['sha'];plan=read(A/'FINAL_MAIN_SCOPE.json');require(plan['gate_sha256']==z['gate_sha256'],'Scope gate drift');out=A/'integration_preparation'/gen;out.mkdir(exist_ok=False)
 q='unsolved_math_prioritization/QUEUE.md';before=h.body_at(q,e).decode();original=h.body_at(q,HEAD).decode();base=h.body_at(q,ORIGINAL_BASE).decode();write(out/'QUEUE.md',queue_update(before,original,base,z['doi'],z['doi_url']))
 j=progress(json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',e)),g,z,tr,95);write(out/'CURRENT_PROGRESS.json',j)
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:write(out/n,h.body_at(PREFIX+n,e).decode()+'\n'+now()+' — PR191 workflow95%, exact credited note published/tracked; merge and factual acceptance pending;39/23 unchanged.\n')
 cur=current_native(g,False);native=A/'integration_preparation'/cur['current_template']
 overlay={CASE+n:inside(n) for n in plan['case_paths']};overlay.update({NATIVE+n:native/n for n in cur['files']});overlay.update({PREFIX+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']});overlay[q]=out/'QUEUE.md';require(set(overlay)==set(plan['selected_MAIN_paths']),'Exact final scope drift')
 r=prepare_tree(h,e,overlay,[e,HEAD],'Merge PR191: credited parity-selected signed-angle law and literal counterexamples; '+z['doi_url'],'SCOPED_MERGE_PREPARATION.json');verify_merge_scope(h,g,r);original_ready(False);return r
def integration_accept():
 g,z,tr=published_tracked();h=helpers();r=read(A/'SCOPED_MERGE_PREPARATION.json');scope_sha=verify_merge_scope(h,g,r);actual=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+actual)['status'] in ['identical','ahead'],'Prepared merge not on MAIN');selected_current(h,actual,r['selected_files'],r['tree']);p=h.api('pulls/'+str(PR));require(p['merged'] and p['state']=='closed' and p['head']['sha']==HEAD,'Original PR merge not accepted')
 cur=read(A/'integration_preparation/CURRENT_TEMPLATE.json');reads=[NATIVE+n for n in g['native_proof_paths']]+[CASE+g['package_name']+'/'+n for n in g['paper_files'].values()]
 for n in reads:
  b=h.body_at(n,actual);x=r['selected_files'][n];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh scientific body drift')
 out={'UTC':now(),'PR':PR,'status':'ACTUAL_ORIGINAL_HEAD_TWO_PARENT_MERGE_FULL_SCOPE_CURRENT_IDENTITIES_ACCEPTED','PR_merged':True,'original_head':HEAD,'gate_sha256':r['gate_sha256'],'merge_commit':r['commit'],'merge_tree':r['tree'],'scope_sha256':scope_sha,'selected_map_sha256':r['selected_map_sha256'],'main_observed':actual,'every_selected_identity_checked_at_actual_observed_MAIN':True,'selected_files':len(r['selected_files']),'parents':[r['expected_main'],HEAD],'DOI':z['doi'],'factual_completion_pending':True};write(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',out);return out
def factual_paths(g):
 files=read(match_path(g['native_pending_manifest']))['files'];names=['SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json','WORKFLOW_COMPLETION.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json','integration_preparation/'+g['native_complete_template']+'_MANIFEST.json'];names+=['integration_preparation/'+g['native_complete_template']+'/'+n for n in files]
 return {CASE+n for n in names}|{NATIVE+n for n in files}|{PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
def factual_prepare(gen):
 g,z,tr=published_tracked();a=read(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json');require(a['PR_merged'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['original_head']==HEAD,'Actual accepted merge absent');h=helpers();p=h.api('pulls/'+str(PR));require(p['merged'] and p['state']=='closed' and p['head']['sha']==HEAD,'Original PR completion drift')
 require(re.fullmatch('factual_preparation_[a-z0-9_]+',gen),'Generation name');e=h.api('git/ref/heads/main')['object']['sha'];merged=read(A/'SCOPED_MERGE_PREPARATION.json');verify_merge_scope(h,g,merged,True);require(h.api('compare/'+merged['commit']+'...'+e)['status'] in ['identical','ahead'],'Original accepted merge not on factual parent');selected_current(h,e,merged['selected_files'],merged['tree']);j=progress(json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',e)),g,z,tr,100)
 cur=prepare_native(True);case=read(A/'CURRENT_CASE_STATUS.json');case.update(completed=40,published=24,fully_completed_count=40,published_count=24,case_completion_requires_actual_factual_postimage_acceptance=True);write(A/'CURRENT_CASE_STATUS.json',case)
 write(A/'WORKFLOW_COMPLETION.json',{'UTC':now(),'PR':PR,'original_head':HEAD,'original_effort':'2/5','status':'FACTUAL_COMPLETE_POSTIMAGE_REQUIRES_ACTUAL_MAIN_ACCEPTANCE','fully_completed_count':40,'published_count':24,'case_percent':100,'goal_complete':False,'DOI':z['doi'],'tracker_range':tr['range'],'actual_merge_commit':a['merge_commit'],'next_original_status_intake':NEXT,'claim':CLAIM})
 out=A/'integration_preparation'/gen;out.mkdir(exist_ok=False);write(out/'CURRENT_PROGRESS.json',j)
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:write(out/n,h.body_at(PREFIX+n,e).decode()+'\n'+now()+' — PR191 factual40/24 postimage; actual factual MAIN acceptance required before192.\n')
 names=['SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json','WORKFLOW_COMPLETION.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json','integration_preparation/'+cur['current_template']+'_MANIFEST.json'];names+=['integration_preparation/'+cur['current_template']+'/'+n for n in cur['files']]
 overlay={CASE+n:inside(n) for n in names};overlay.update({NATIVE+n:A/'integration_preparation'/cur['current_template']/n for n in cur['files']});overlay.update({PREFIX+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']});plan=read(A/'FINAL_MAIN_SCOPE.json');require(set(overlay)==factual_paths(g) and set(overlay)<=set(plan['selected_MAIN_paths']+plan['factual_additional_paths']),'Outside exact factual scope')
 return prepare_tree(h,e,overlay,[e],'Record PR191 factual40/24 completion; actual acceptance required before192','FINAL_FACTUAL_PREPARATION.json')
def factual_accept():
 g,z,tr=published_tracked();h=helpers();r=read(A/'FINAL_FACTUAL_PREPARATION.json');verify_prepared(h,r,[r['expected_main']]);actual=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+actual)['status'] in ['identical','ahead'],'Factual commit not on MAIN');merged=read(A/'SCOPED_MERGE_PREPARATION.json');verify_merge_scope(h,g,merged,True);require(h.api('compare/'+merged['commit']+'...'+actual)['status'] in ['identical','ahead'],'Original accepted merge not on actual MAIN');require(set(r['selected_files'])==factual_paths(g),'Exact factual selected scope drift');combined={**merged['selected_files'],**r['selected_files']};selected_current(h,actual,combined,r['tree'])
 for n,x in r['selected_files'].items():
  b=h.body_at(n,actual);require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh factual body drift')
 p=h.api('pulls/'+str(PR));require(p['merged'] and p['state']=='closed' and p['head']['sha']==HEAD,'Original PR completion drift')
 out={'UTC':now(),'PR':PR,'status':'ACTUAL_FACTUAL_COMPLETION_MAIN_PARENT_FULL_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED','factual_commit':r['commit'],'main_observed':actual,'sole_parent':r['expected_main'],'combined_expected_current_identities_checked':len(combined),'every_selected_identity_checked_at_actual_observed_MAIN':True,'fully_completed_count':40,'published_count':24,'case_percent':100,'goal_complete':False,'next_original_status_intake':NEXT,'separate_selfreceipt_publication_required_at_next_own_checkpoint':True};write(A/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json',out);return out
