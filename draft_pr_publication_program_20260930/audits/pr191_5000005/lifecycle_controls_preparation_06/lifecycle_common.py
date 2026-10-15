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
OP_CLEARANCE='ROOT_OPERATIONAL_LIFECYCLE_CLEARANCE.json'
CASE_PROJECTION='ROOT_CASE_SCIENTIFIC_PROJECTION.json'
CASE_BASELINE='ROOT_CASE_BASELINE.json';CASE_LOG_BASELINE='ROOT_CASE_LOG_BASELINE.md'
CASE_PROTECTED_KEYS={'PR','problem_id','original_head','original_QUEUE_status','original_effort','mathematical_clearance','priority_clearance','goal_complete','original_source_scope','mathematical_scope','literal_imported_conjunction','bounded_priority_audit_complete','current_primary_overlap_verified','novelty_clearance','qualified_credited_note_route_authorized','current_proof','current_proof_SHA256','scientific_package_ready'}
CASE_FACTUAL_KEYS={'publication_gate_SHA256','UTC','status','case_percent','publication_ready','completed','published','fully_completed_count','published_count','remaining_required_steps','whole_package_reviews','whole_package_reviews_complete','first_whole_package_review_active','Zenodo_published','actual_Zenodo_published','DOI','tracker_updated','actual_tracker_updated','tracker_range','original_PR_merged','actual_original_PR_merged','PR_closed','case_completion_requires_actual_factual_postimage_acceptance','retired_operational_aliases_PR191','operational_lifecycle_audit_active','operational_required_repairs','operational_lifecycle_audit_status','operational_clearance_receipt','operational_clearance_gate_sha256'}
CASE_FACTUAL_KEYS.update({'historical_case_baseline_PR191','whole_package_review_active','whole_package_reviews_pending','successive_NEW_whole_package_reviews_complete','publication_clearance','completed_new_whole_package_reviews','whole_package_review_status','actual_factual_checkpoint_accepted','completion_metadata_checkpoint_pending_at_snapshot','next_intake_requires_actual_completion_receipt','next_numeric_intake_cursor','conditional_next_numeric_intake_cursor','advance_to_next_PR_authorized_now','last_completed_actual_final_receipt','conditional_last_completed_actual_final_receipt'})
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
 safe_rel(g['native_final_template']);safe_rel(g['native_complete_template']);operational_clearance(g);case_projection(g);case_baselines(g)
 return g
def case_scientific_projection(current_case):
 """Pure Root constructor: no gate, process, filesystem or service action."""
 require(CASE_PROTECTED_KEYS<=set(current_case),'Trusted case lacks scientific projection fields')
 require((current_case['PR'],current_case['problem_id'],current_case['original_head'])==(PR,PROBLEM,HEAD),'Trusted case projection identity')
 return {'schema':'PR191_CASE_SCIENTIFIC_PROJECTION_V1','PR':PR,'original_head':HEAD,'protected_values':{k:copy.deepcopy(current_case[k]) for k in sorted(CASE_PROTECTED_KEYS)},'allowed_other_case_keys':sorted(set(current_case)-CASE_PROTECTED_KEYS)}

def case_projection(g):
 require(CASE_PROJECTION in g['public_case_pins'],'Trusted Root case scientific projection absent');match(inside(CASE_PROJECTION),g['public_case_pins'][CASE_PROJECTION]);j=read(inside(CASE_PROJECTION))
 require(set(j)=={'schema','PR','original_head','protected_values','allowed_other_case_keys'} and j['schema']=='PR191_CASE_SCIENTIFIC_PROJECTION_V1' and (j['PR'],j['original_head'])==(PR,HEAD) and set(j['protected_values'])==CASE_PROTECTED_KEYS,'Case scientific projection schema/identity differs')
 allowed=j['allowed_other_case_keys'];require(isinstance(allowed,list) and all(isinstance(k,str) for k in allowed) and len(allowed)==len(set(allowed)) and not CASE_PROTECTED_KEYS&set(allowed),'Case projection allowed-key schema differs')
 v=j['protected_values'];require((v['PR'],v['problem_id'],v['original_head'],v['original_QUEUE_status'],v['original_effort'],v['current_proof'],v['current_proof_SHA256'])==(PR,PROBLEM,HEAD,'claimed_solved','2/5',g['current_proof']['path'],g['current_proof']['sha256']),'Case scientific projection proof/identity drift')
 require(all(v[k] is x for k,x in [('mathematical_clearance',True),('priority_clearance',False),('goal_complete',False),('novelty_clearance',False),('qualified_credited_note_route_authorized',True),('bounded_priority_audit_complete',True),('current_primary_overlap_verified',True),('scientific_package_ready',True)]),'Case scientific projection authority/priority drift');return j

def operational_bindings(g):
 receipt=read(inside(OP_CLEARANCE));review=receipt['independent_adversary_review'];return [review[k] for k in ['report','seal','root_authentication']]
def operational_clearance(g):
 require(OP_CLEARANCE in g['public_case_pins'],'Trusted Root operational clearance absent from gate');match(inside(OP_CLEARANCE),g['public_case_pins'][OP_CLEARANCE]);j=read(inside(OP_CLEARANCE))
 require(j.get('status')=='ROOT_AUTHENTICATED_OPERATIONAL_LIFECYCLE_CLEARANCE' and (j.get('PR'),j.get('original_head'))==(PR,HEAD) and j.get('all_required_findings_globally_resolved') is True and j.get('outstanding_required_repairs')==[],'Root operational clearance false/stale/unfinished');valid_stamp(j.get('UTC'))
 require(j.get('runtime_pins')=={n:{k:v for k,v in pin(inside(n)).items() if k!='git_blob'} for n in CONTROL_FILES},'Operational clearance runtime identities differ')
 review=j.get('independent_adversary_review',{});require(review.get('disposition')=='PASS' and {'report','seal','root_authentication'}<=set(review),'Final independent operational review not PASS')
 paths=[]
 for x in operational_bindings(g):match_path(x);paths.append(x['path'])
 require(len(set(paths))==3,'Distinct final operational review evidence required');return j

def canonical_json(value):return json.dumps(value,sort_keys=True,separators=(',',':'))
def derive_operational_aliases(value,g,stamp,gate_sha256,programme=False):
 """Pure approved retirement of current operational aliases."""
 valid_stamp(stamp);j=copy.deepcopy(value);old={k:copy.deepcopy(v) for k,v in j.items() if k.startswith('operational_') or k.startswith('current_operational_')}
 if old:j.setdefault('retired_operational_aliases_PR191',[]).append({'UTC':stamp,'values':old})
 for k in old:j.pop(k,None)
 prefix='current_' if programme else '';j.update({prefix+'operational_lifecycle_audit_active':False,prefix+'operational_required_repairs':[],prefix+'operational_lifecycle_audit_status':'FINAL_CLEAN_ROOT_AUTHENTICATED',prefix+'operational_clearance_receipt':{'path':'audits/pr191_5000005/'+OP_CLEARANCE,**g['public_case_pins'][OP_CLEARANCE]},prefix+'operational_clearance_gate_sha256':gate_sha256});return j

def normalize_operational(j,g,programme=False):
 operational_clearance(g);result=derive_operational_aliases(j,g,now(),pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],programme);j.clear();j.update(result);return j

def match_path(x):p=inside(x['path']);match(p,x);return p
_helpers=None
def helpers():
 global _helpers
 if _helpers is None:
  gate();require_runtime();require(sys.dont_write_bytecode,'Invoke operational scripts with Python -B')
  p=A.parent/'pr190_5000007/prepare_final_scoped_merge.py'
  spec=importlib.util.spec_from_file_location('audited_native_objects_for_191',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  m.m.TREE_CACHE_PATH=A/'lifecycle_private/IMMUTABLE_TREE_CACHE.json';_helpers=m
 return _helpers
def original_ready(draft=None):
 p=helpers().api('pulls/'+str(PR));require(p['head']['sha']==HEAD and p['state']=='open' and not p['merged'],'Original head/open state drift')
 if draft is not None:require(p['draft'] is draft,'PR draft/ready state drift')
 return p
_runtime=None

def require_runtime():
 require(_runtime is not None,'External observations require explicit production entrypoint or injected test services');return _runtime

def production_entrypoint(function,*args):
 """The sole default path enabling real process/helper/service actions."""
 global _runtime
 require(_runtime is None and sys.dont_write_bytecode,'Use an explicit Python -B production entrypoint');gate()
 _runtime={'runner':subprocess.run,'inspect':lambda g:observe_publication(g,subprocess.run),'tracker':gws}
 try:return function(*args)
 finally:_runtime=None

def publication_identity(z):return {k:z[k] for k in ['environment','id','state','doi','doi_url','record_url','files']}
def validate_publication(g,z):
 require(z.get('state')=='published' and z.get('environment')=='production' and type(z.get('id')) is int and z['id']>0,'Actual production publication absent')
 require(re.fullmatch(r'10\.[0-9]{4,9}/\S+',z.get('doi') or '') and z.get('doi_url')=='https://doi.org/'+z['doi'] and z.get('record_url')=='https://zenodo.org/records/'+str(z['id']),'Actual DOI/record identity invalid')
 require(z.get('gate_sha256')==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Publication belongs to another gate');require(valid_stamp(z.get('verified_utc'))<=valid_stamp(now()),'Published observation is in the future')
 require(type(z.get('receipt_saved')) is bool and isinstance(z.get('metadata_normalizations'),list) and isinstance(z.get('doi_resolution'),dict) and z['doi_resolution'].get('status') in ['not_checked','resolved','not_resolved','unavailable'],'Exact kit published receipt fields absent')
 expected={g['paper_files'][k]:(g['payloads'][g['paper_files'][k]]['bytes'],g['payloads'][g['paper_files'][k]].get('sha256',g['payloads'][g['paper_files'][k]].get('SHA256'))) for k in ['pdf','source','support']}
 require(isinstance(z.get('files'),list) and len(z['files'])==3 and all(set(x)=={'name','size','sha256'} and type(x['size']) is int for x in z['files']) and {x['name']:(x['size'],x['sha256']) for x in z['files']}==expected,'Publication exact uploaded file pins absent/different');return z

def exact_binding(path):return {'path':path,**{k:v for k,v in pin(A/path).items() if k!='git_blob'}}
def publication(g=None):
 g=g or gate();z=validate_publication(g,read(A/'ZENODO_PUBLICATION_READBACK.json'));stage=read(A/'ZENODO_STAGE_READBACK.json');require(stage.get('id')==z['id'] and stage.get('gate_sha256')==z['gate_sha256'],'Staged/published record ID/gate continuity drift');e=read(A/'ZENODO_PUBLICATION_EVIDENCE.json')
 require(e.get('source')=='EXACT_KIT_PUBLISHED_OUTPUT' and e.get('command') in ['publish','inspect'] and e.get('gate_sha256')==z['gate_sha256'] and e.get('receipt')==exact_binding('ZENODO_PUBLICATION_READBACK.json') and e.get('manifest')==g['payloads'][g['paper_files']['metadata']],'Exact kit publication evidence binding drift')
 require(e.get('published_output')==z,'Kit output/publication receipt disagreement')
 observed=validate_publication(g,require_runtime()['inspect'](g));require(publication_identity(observed)==publication_identity(z),'Fresh exact-kit published identity differs from local acceptance');return z

def tracker_row(g,z):
 proposal=read(match_path(g['tracker_row_proposal']));require(set(proposal)<={'original_problem','solution_chat_url','notes'} and {'original_problem','notes'}<=set(proposal),'Reviewed tracker proposal schema')
 row=[proposal['original_problem'],proposal.get('solution_chat_url',''),z['doi_url'],proposal['notes']];require(all(isinstance(v,str) for v in row) and row[0] and row[3],'Tracker proposal values');return row

def own_range(rng):
 require(isinstance(rng,str),'Invalid own-row range');m=re.fullmatch(r"'?Math Puzzles'?!A([0-9]+):D([0-9]+)",rng);require(m and int(m[1])==int(m[2]) and int(m[1])>=2,'Invalid own-row range');return int(m[1])

def foreign_retained(before,after):
 cursor=iter(after);return all(any(candidate==row for candidate in cursor) for row in before)
def tracker_baseline(g,z):
 p=A/'lifecycle_private/TRACKER_FOREIGN_BASELINE.json';j=read(p);require(j.get('gate_sha256')==z['gate_sha256'] and j.get('DOI')==z['doi'] and j.get('spreadsheet_id')==SID and j.get('gid')==GID and j.get('tab')==TAB and isinstance(j.get('rows'),list) and all(isinstance(row,list) for row in j['rows']),'Private tracker foreign baseline identity/schema drift');return j

def observe_tracker(call,g,z,row,rng):
 baseline=tracker_baseline(g,z)['rows']
 for observation in [1,2]:
  target=call('spreadsheet','get',{'spreadsheetId':SID,'fields':'spreadsheetId,sheets(properties(sheetId,title))'});require(target['spreadsheetId']==SID and [v['properties']['title'] for v in target['sheets'] if v['properties']['sheetId']==GID]==[TAB],'Fresh tracker sheet/gid/tab drift')
  actual=call('values','get',{'spreadsheetId':SID,'range':rng,'valueRenderOption':'UNFORMATTED_VALUE'});require(actual.get('values')==[row],'Fresh trusted own-row drift')
  full=call('values','get',{'spreadsheetId':SID,'range':"'Math Puzzles'!A:D",'valueRenderOption':'UNFORMATTED_VALUE'});rows=full.get('values',[]);require(rows and rows[0]==HEADER,'Fresh trusted tracker header drift');hits=[i for i,r in enumerate(rows,1) if any(z['doi'] in str(v) for v in r)]
  require(hits==[own_range(rng)] and rows[hits[0]-1]==row,'Fresh trusted tracker DOI uniqueness/row drift');foreign=[r for r in rows if not any(z['doi'] in str(v) for v in r)]
  require(foreign_retained(baseline,foreign),'Fresh tracker pre-existing foreign rows changed; reconcile without repair')

def validate_tracker(g,z,tr):
 row=tracker_row(g,z);rng=tr.get('range');own_range(rng)
 require(tr.get('status')=='TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED' and tr.get('DOI')==z['doi'] and (tr.get('spreadsheet_id'),tr.get('gid'),tr.get('tab'))==(SID,GID,TAB) and type(tr.get('actual_fresh_reads')) is int and tr['actual_fresh_reads']==2 and tr.get('row')==row and tr.get('gate_sha256')==z['gate_sha256'],'Exact tracker acceptance/proposal assertion drift');valid_stamp(tr.get('UTC'))
 names=['TARGET_VALIDATION.json','ROW_READBACK_1.json','ROW_READBACK_2.json','POSTAPPEND_UNIQUENESS_1.json','POSTAPPEND_UNIQUENESS_2.json'];expected={n:exact_binding('sheets_tracking/'+n) for n in names}
 require(tr.get('evidence')==expected and tr.get('private_foreign_baseline')=={k:v for k,v in pin(A/'lifecycle_private/TRACKER_FOREIGN_BASELINE.json').items() if k!='git_blob'} and tr.get('proposal')==g['tracker_row_proposal'],'Tracker evidence/proposal pins absent/different')
 target=read(A/'sheets_tracking/TARGET_VALIDATION.json');require((target.get('spreadsheet_id'),target.get('gid'),target.get('tab'),target.get('header'))==(SID,GID,TAB,HEADER),'Tracker target evidence differs');times=[valid_stamp(target.get('UTC'))]
 for i in [1,2]:
  r=read(A/f'sheets_tracking/ROW_READBACK_{i}.json');u=read(A/f'sheets_tracking/POSTAPPEND_UNIQUENESS_{i}.json');times.extend([valid_stamp(r.get('UTC')),valid_stamp(u.get('UTC'))])
  require(r.get('range')==rng and r.get('values')==[row] and u.get('range')==rng and u.get('DOI')==z['doi'] and u.get('own_row')==row and type(u.get('matching_DOI_rows')) is int and u['matching_DOI_rows']==1 and u.get('preexisting_foreign_rows_retained') is True,'Tracker own-read/uniqueness evidence disagreement')
 require(times==sorted(times) and times[0]>=valid_stamp(z['verified_utc']) and times[-1]<=valid_stamp(tr['UTC'])<=valid_stamp(now()),'Tracker evidence timestamp order/future drift');return row

def published_tracked():
 g=gate();z=publication(g);tr=read(A/'TRACKER_ACCEPTANCE.json');row=validate_tracker(g,z,tr);observe_tracker(require_runtime()['tracker'],g,z,row,tr['range']);return g,z,tr
def sanitize_zenodo(j):
 return {k:j[k] for k in ['environment','id','state','doi','doi_url','record_url','files','metadata_normalizations','doi_resolution','receipt_saved','verified_utc'] if k in j}
def kit_call(g,cmd,runner,confirm_id=None,check_doi=False):
 private=A/'lifecycle_private';private.mkdir(exist_ok=True);args=[PY,'-E','-S','-B','-P',str(R/'zenodo_deposit_tool/zenodo.py'),cmd,str(A/g['package_name']/g['paper_files']['metadata'])]
 if cmd=='publish':args+=['--confirm-id',str(confirm_id)]
 if check_doi:args+=['--check-doi']
 r=runner(args,cwd=R,capture_output=True,timeout=300);(private/('ZENODO_'+cmd+'.stdout')).write_bytes(r.stdout);(private/('ZENODO_'+cmd+'.stderr')).write_bytes(r.stderr)
 require(r.returncode==0,'Uploader result unconfirmed; reconcile existing state; no blind retry');j=json.loads(r.stdout);require(j.get('environment')=='production','Wrong Zenodo environment');return j

def observe_publication(g,runner):
 j=sanitize_zenodo(kit_call(g,'inspect',runner,check_doi=True))|{'gate_sha256':pin(A/'ROOT_PUBLICATION_GATE.json')['sha256']};return validate_publication(g,j)

def save_published(g,j,command):
 out=sanitize_zenodo(j)|{'gate_sha256':pin(A/'ROOT_PUBLICATION_GATE.json')['sha256']};validate_publication(g,out);write(A/'ZENODO_PUBLICATION_READBACK.json',out)
 write(A/'ZENODO_PUBLICATION_EVIDENCE.json',{'source':'EXACT_KIT_PUBLISHED_OUTPUT','command':command,'gate_sha256':out['gate_sha256'],'receipt':exact_binding('ZENODO_PUBLICATION_READBACK.json'),'manifest':g['payloads'][g['paper_files']['metadata']],'published_output':out});return out

def run_zenodo(action,confirm_id=None,runner=None):
 g=gate();require(action in ['check','stage','inspect','publish','inspect-published'],'Unknown action');runner=runner or require_runtime()['runner']
 if action in ['stage','publish']:original_ready()
 private=A/'lifecycle_private';private.mkdir(exist_ok=True)
 def call(cmd):return kit_call(g,cmd,runner,confirm_id,action=='inspect-published' or cmd=='publish')
 marker=private/'ZENODO_STAGE_ATTEMPT_STARTED.json'
 if action=='stage':
  if marker.exists():
   require(read(marker).get('gate_sha256')==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Stage marker belongs to another gate; reconcile existing state')
   current=call('inspect')
   if read(marker).get('id') is not None:require(current['id']==read(marker)['id'],'Existing draft ID drift')
   if current['state']=='published':return save_published(g,current,'inspect')
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
 if j.get('state')=='published':
  if action=='publish':require(j['id']==st['id'],'Published record differs from actual staged ID')
  out=save_published(g,j,'publish' if action=='publish' and current['state']!='published' else 'inspect')
 return out
def gws(resource,method,params,body=None,runner=None):
 runner=runner or require_runtime()['runner']
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
 row=tracker_row(g,z)
 require(all(isinstance(c,str) for c in row) and row[0] and row[3],'Reviewed tracker proposal schema')
 full=call('values','get',{'spreadsheetId':SID,'range':"'Math Puzzles'!A:D",'valueRenderOption':'UNFORMATTED_VALUE'})
 require(full.get('values',[[]])[0]==HEADER,'Full read/header drift')
 baseline_path=A/'lifecycle_private/TRACKER_FOREIGN_BASELINE.json';foreign_before=[r for r in full['values'] if not any(z['doi'] in str(v) for v in r)]
 if baseline_path.exists():require(foreign_retained(tracker_baseline(g,z)['rows'],foreign_before),'Pre-existing private tracker baseline changed; reconcile before append')
 else:write(baseline_path,{'gate_sha256':z['gate_sha256'],'DOI':z['doi'],'spreadsheet_id':SID,'gid':GID,'tab':TAB,'rows':foreign_before})

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
 evidence={n:exact_binding('sheets_tracking/'+n) for n in ['TARGET_VALIDATION.json','ROW_READBACK_1.json','ROW_READBACK_2.json','POSTAPPEND_UNIQUENESS_1.json','POSTAPPEND_UNIQUENESS_2.json']};out={'UTC':now(),'evidence':evidence,'private_foreign_baseline':{k:v for k,v in pin(baseline_path).items() if k!='git_blob'},'proposal':g['tracker_row_proposal'],'status':'TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED','spreadsheet_id':SID,'gid':GID,'tab':TAB,'range':rng,'DOI':z['doi'],'row':row,'actual_fresh_reads':2,'gate_sha256':z['gate_sha256']};write(A/'TRACKER_ACCEPTANCE.json',out);return out
def normalize_programme(j,g,intake,phase,stamp,gate_sha256):
 require(phase in [95,100] and j['current_PR']==PR,'Wrong phase/case');expected=(39,23,190) if phase==95 else (40,24,191)
 require((j['fully_completed_count'],j['published_count'],j['last_completed_PR'])==expected,'Programme census drift')
 obsolete=['actual_factual_checkpoint_accepted','active_checkpoint_commit','last_completed_writer_operation_finished','read_only_next_case','next_intake_requires_actual_completion_receipt_and_explicit_writer_release']
 archive=obsolete+['program_snapshot_semantics','program_snapshot_authority_condition','remaining_current_step','next_step','active_checkpoint_acceptance_receipt','latest_ordered_intake_record'];old={k:copy.deepcopy(j[k]) for k in archive if k in j}
 if old:j.setdefault('retired_live_aliases_PR191',[]).append({'UTC':stamp,'phase':phase,'values':old})
 for k in obsolete:j.pop(k,None)
 require(j['dated_eligible_total']==99,'Dated denominator drift');j['fully_completed_fraction_percent']=round(100*j['fully_completed_count']/99,2);j['workflow_estimate_percent']=j['fully_completed_fraction_percent']
 require(intake['PR']==PR and intake['original_head']==HEAD and re.fullmatch('[0-9a-f]{40}',intake['checkpoint_commit']),'Actual intake identity drift')
 j.update(workflow_estimate_definition=f"{j['fully_completed_count']}/dated99 completed,{j['published_count']} published; dated denominator is not a fresh eligibility census.",last_completed_actual_final_receipt='audits/pr190_5000007/ROOT_FINAL_FACTUAL_ACCEPTANCE.json',conditional_last_completed_actual_final_receipt='audits/pr191_5000005/ROOT_FINAL_FACTUAL_ACCEPTANCE.json',actual_factual_checkpoint_accepted=False,last_actual_intake_checkpoint_commit=intake['checkpoint_commit'],last_actual_intake_checkpoint_release='audits/pr191_5000005/INTAKE_CHECKPOINT_ACCEPTANCE.json',latest_ordered_intake_record='status_intakes_after_pr190/PR191_ORIGINAL_STATUS_INTAKE.json',next_intake_requires_actual_completion_receipt=True,next_intake_requires_explicit_writer_release=False,peer_pause_or_exclusive_writer_window_assumed=False,next_eligible_PR_after_current_completion=None,next_eligible_order_requires_fresh_status_check=True,next_numeric_intake_cursor=PR,conditional_next_numeric_intake_cursor=NEXT,conditional_next_intake_requires_actual_factual_acceptance=True,advance_to_next_PR_authorized_now=False,persistent_goal_complete=False,current_original_head=HEAD,current_original_budget='2/5',current_problem_id=PROBLEM,current_mathematical_result_valid=True,current_mathematical_scope=CLAIM,current_priority_clearance=False,current_historical_firstness_or_guaranteed_novelty_certified=False,current_source_author_authenticated_erratum=False,current_source_unique_intent_certified=False,current_publication_gate='audits/pr191_5000005/ROOT_PUBLICATION_GATE.json',current_current_proof='audits/pr191_5000005/'+g['current_proof']['path'],current_whole_package_review_input='audits/pr191_5000005/'+g['review_input']['path'],current_publication_package_review_round=len(g['whole_package_reviews']),current_publication_package_review_status='Successive NEW full-package reviews complete; last clean',current_present_open_status_verified=False)
 receipt='ROOT_ACTUAL_MERGE_ACCEPTANCE.json' if phase==95 else 'ROOT_FINAL_FACTUAL_ACCEPTANCE.json'
 j['active_checkpoint_acceptance_receipt']='audits/pr191_5000005/'+receipt;j['program_snapshot_authority_condition']='Effective only after actual current-tree full-scope acceptance in '+j['active_checkpoint_acceptance_receipt']+('; actual factual completion required before intake192.' if phase==95 else '; actual factual acceptance required before intake192.')
 j['remaining_current_step']='PR191 original-head merge/current-tree acceptance and factual completion; only then intake192.' if phase==95 else 'None for PR191 after actual factual acceptance; original-status-only intake192 next.';j['next_step']=j['remaining_current_step'];j['completion_metadata_checkpoint_pending_at_snapshot']=True
 j=derive_operational_aliases(j,g,stamp,gate_sha256,True)
 j['program_snapshot_semantics']='Actual credited PR191 note publication and tracker accepted; '+('39completed/23published remain, original-head merge and factual acceptance pending.' if phase==95 else 'Original-head merge accepted;40completed/24published factual postimage is effective only after actual current-MAIN factual acceptance before intake192.')+' No firstness, novelty, present openness or independence certification; broader goal active.'
 return j
def normalize(j,phase):
 g=gate();return normalize_programme(copy.deepcopy(j),g,read(A/'INTAKE_CHECKPOINT_ACCEPTANCE.json'),phase,now(),pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'])
def factual_sentence(z,tr,merged):return 'The successive NEW whole-package review loop is complete and final clean. Exact note '+z['doi_url']+' is actually published and tracker '+tr['range']+' was verified twice. Original-head merge '+('was actually accepted; final factual MAIN acceptance follows separately.' if merged else 'remains pending at this preparation.')+' Extensive AI; unrefereed.'
def valid_stamp(value):
 require(isinstance(value,str) and re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?\+00:00',value),'Invalid UTC factual timestamp schema')
 try:stamp=datetime.datetime.fromisoformat(value)
 except ValueError:raise RuntimeError('Invalid UTC factual timestamp value')
 require(stamp.utcoffset()==datetime.timedelta(0),'Non-UTC factual timestamp');return stamp

def encoded(value):return (json.dumps(value,indent=2)+'\n').encode()
def derive_native(g,z,tr,baseline,timestamps,merged=False):
 """Pure full-byte postimage from approved pending bytes and factual inputs."""
 require(set(timestamps)==({'published','merged'} if merged else {'published'}),'Factual generation timestamp keys')
 valid_stamp(timestamps['published'])
 if merged:require(valid_stamp(timestamps['merged'])>=valid_stamp(timestamps['published']),'Factual timestamps out of order')
 files=dict(baseline)
 for accepted in ([False,True] if merged else [False]):
  stamp=timestamps['merged' if accepted else 'published']
  common={'UTC':stamp,'whole_package_reviews_complete':True,'publication_ready':True,'actual_Zenodo_published':True,'actual_published':True,'actual_DOI':z['doi'],'actual_tracker_updated':True,'actual_tracker_range':tr['range'],'actual_original_PR_merged':accepted,'case_percent':100 if accepted else 95,'snapshot_semantics':'Actual publication/tracker facts; original-head merge '+('accepted' if accepted else 'pending at this preparation')+'; factual MAIN adoption requires separate actual acceptance.'}
  updates={'whole_package_reviews_pending':False,'successive_NEW_whole_package_reviews_complete':True,'publication_clearance':True,'publication_and_tracker_actions_not_yet_performed':False,'not_an_approval':False,'completed_new_whole_package_reviews':len(g['whole_package_reviews'])}
  for n in g['native_json_status_paths']:
   j=json.loads(files[n])
   for k,v in common.items():
    if k in j:j[k]=v
   for k,v in updates.items():
    if k in j:j[k]=v
   if n=='PUBLICATION.json':j.update(UTC=stamp,kind='ACTUAL_PUBLISHED_TRACKED_CREDITED_NOTE',package=g['package_name'],paper=g['paper_files']['pdf'],source=g['paper_files']['source'],support=g['paper_files']['support'],metadata=g['paper_files']['metadata'],actual_DOI=z['doi'],actual_Zenodo_published=True,actual_tracker_range=tr['range'],actual_original_PR_merged=accepted,whole_package_review_status='Successive NEW whole-package reviews completed; final clean',gate_sha256=z['gate_sha256'])
   if n=='PUBLICATION_PACKAGE_PLAN.json':j.update(package_case_relative=CASE+g['package_name']+'/',planned_files=[g['paper_files'][k] for k in ['pdf','source','support']],actual_published=True,actual_DOI=z['doi'],publication_ready=True)
   if n=='review/WHOLE_PACKAGE_REVIEW_STATUS.json':j.update(status='SUCCESSIVE_NEW_COMPLETE_PACKAGE_REVIEWS_FINAL_CLEAN',not_an_approval=False,completed_new_whole_package_reviews=len(g['whole_package_reviews']),paper_science_and_current_native_template_require_review=False)
   files[n]=encoded(j)
  factual=factual_sentence(z,tr,accepted)
  for n,pending in g['native_text_status_replacements'].items():
   text=files[n].decode();old=factual_sentence(z,tr,False) if accepted else pending
   require(text.count(old)==1,'Nonunique approved native factual sentence');files[n]=text.replace(old,factual).encode()
  files['RESEARCH_LOG.md']=files['RESEARCH_LOG.md']+('\n'+stamp+' — '+factual+' Original effort2/5 retained. '+('40/24 factual postimage requires actual MAIN acceptance.' if accepted else '39completed/23published until actual factual acceptance.')+'\n').encode()
 return files

def case_baselines(g):
 for n in [CASE_BASELINE,CASE_LOG_BASELINE]:require(n in g['public_case_pins'],'Trusted current-case/log baseline absent '+n);match(inside(n),g['public_case_pins'][n])
 baseline=read(inside(CASE_BASELINE));require(canonical_json(case_scientific_projection(baseline))==canonical_json(case_projection(g)),'Case baseline/scientific projection differs');valid_stamp(g['UTC']);require(valid_stamp(g['UTC'])<=valid_stamp(now()),'Ready gate timestamp is in the future');(inside(CASE_LOG_BASELINE)).read_bytes().decode();return baseline,(inside(CASE_LOG_BASELINE)).read_bytes()

def ready_case_log_suffix(stamp):
 valid_stamp(stamp);return '\n'+stamp+' — PR191 workflow90%: successive NEW whole-package science and operational reviews are final clean; Root authenticated exact controls and issued the qualified-note publication gate. No actual publication, DOI, tracker update, original-head merge, factual MAIN acceptance or intake192.39/23 unchanged.\n'

def derive_case_ready(baseline,g,gate_sha256):
 """Pure full ready90 case; historical source is retained, never inherited as live authority."""
 stamp=g['UTC'];valid_stamp(stamp);j={k:copy.deepcopy(baseline[k]) for k in sorted(CASE_PROTECTED_KEYS)};j['historical_case_baseline_PR191']={'source':CASE_BASELINE,'values':copy.deepcopy(baseline)}
 j.update(UTC=stamp,status='TWO_CLEAN_SCIENCE_REVIEWS_AND_FRESH_OPERATIONAL_REVIEW_COMPLETE_READY_FOR_AUTHORIZED_PUBLICATION',case_percent=90,completed=39,published=23,fully_completed_count=39,published_count=23,publication_ready=True,publication_gate_SHA256=gate_sha256,whole_package_reviews=g['whole_package_reviews'],whole_package_reviews_complete=True,first_whole_package_review_active=False,whole_package_review_active=False,whole_package_reviews_pending=False,successive_NEW_whole_package_reviews_complete=True,publication_clearance=True,completed_new_whole_package_reviews=len(g['whole_package_reviews']),whole_package_review_status='Successive NEW full-package reviews complete; last clean',Zenodo_published=False,actual_Zenodo_published=False,DOI=None,tracker_updated=False,actual_tracker_updated=False,tracker_range=None,original_PR_merged=False,actual_original_PR_merged=False,PR_closed=False,actual_factual_checkpoint_accepted=False,completion_metadata_checkpoint_pending_at_snapshot=True,next_intake_requires_actual_completion_receipt=True,next_numeric_intake_cursor=PR,conditional_next_numeric_intake_cursor=NEXT,advance_to_next_PR_authorized_now=False,last_completed_actual_final_receipt='audits/pr190_5000007/ROOT_FINAL_FACTUAL_ACCEPTANCE.json',conditional_last_completed_actual_final_receipt='audits/pr191_5000005/ROOT_FINAL_FACTUAL_ACCEPTANCE.json',remaining_required_steps='Actual exact-kit publication/DOI, unique tracker row, original-head merge and factual MAIN acceptance before192.')
 return derive_operational_aliases(j,g,stamp,gate_sha256)

def derive_case_stage(baseline,g,z,tr,factual_timestamps,phase,gate_sha256):
 require(phase in [95,100],'Unsupported current case stage');j=derive_case_ready(baseline,g,gate_sha256)
 require(set(factual_timestamps)==({'published','merged'} if phase==100 else {'published'}),'Case stage timestamp keys differ')
 for current_phase in ([95,100] if phase==100 else [95]):
  merged=current_phase==100;stamp=factual_timestamps['merged' if merged else 'published'];valid_stamp(stamp)
  j.update(UTC=stamp,status='ACTUAL_NOTE_PUBLISHED_TRACKED_'+('MERGE_ACCEPTED_FACTUAL_POSTIMAGE_PENDING' if merged else 'ORIGINAL_HEAD_MERGE_PENDING'),case_percent=current_phase,completed=40 if merged else 39,published=24 if merged else 23,fully_completed_count=40 if merged else 39,published_count=24 if merged else 23,Zenodo_published=True,actual_Zenodo_published=True,DOI=z['doi'],tracker_updated=True,actual_tracker_updated=True,tracker_range=tr['range'],original_PR_merged=merged,actual_original_PR_merged=merged,PR_closed=merged,case_completion_requires_actual_factual_postimage_acceptance=True,remaining_required_steps='Actual factual MAIN acceptance before intake192.' if merged else 'Original-head MAIN merge/full current-tree acceptance and factual completion before intake192.')
  j=derive_operational_aliases(j,g,stamp,gate_sha256)
 return j

def case_log_stage_suffix(z,tr,stamp,phase):
 valid_stamp(stamp);return '\n'+stamp+' — PR191 workflow'+str(phase)+'%: '+factual_sentence(z,tr,phase==100)+' '+('40/24 factual postimage requires separate actual MAIN acceptance.' if phase==100 else '39completed/23published remain until separate actual factual acceptance.')+' No intake192 until actual factual MAIN acceptance and next own receipt checkpoint.\n'

def derive_case_log(baseline_bytes,g,z,tr,factual_timestamps,phase):
 require(phase in [90,95,100] and isinstance(baseline_bytes,bytes),'Case log derivation input');out=baseline_bytes+ready_case_log_suffix(g['UTC']).encode()
 if phase==90:require(factual_timestamps=={},'Ready case log has no actual stage times');return out
 require(set(factual_timestamps)==({'published','merged'} if phase==100 else {'published'}),'Case log stage timestamp keys differ')
 out+=case_log_stage_suffix(z,tr,factual_timestamps['published'],95).encode()
 if phase==100:out+=case_log_stage_suffix(z,tr,factual_timestamps['merged'],100).encode()
 return out

def pending_native_bytes(g):
 manifest=read(match_path(g['native_pending_manifest']));T=inside('integration_preparation/'+g['native_pending_template']);require(inventory(T)==set(manifest['files']),'Pending native inventory drift')
 for n,x in manifest['files'].items():match(T/n,x)
 return {n:(T/n).read_bytes() for n in manifest['files']}

def prepare_native(merged=False):
 g,z,tr=published_tracked();I=A/'integration_preparation';name=g['native_complete_template'] if merged else g['native_final_template'];T=I/name
 if T.exists():
  cur=current_native(g,merged,(z,tr));baseline,log_baseline=case_baselines(g);require(canonical_json(read(A/'CURRENT_CASE_STATUS.json'))==canonical_json(derive_case_stage(baseline,g,z,tr,cur['factual_timestamps'],100 if merged else 95,z['gate_sha256'])) and (A/'RESEARCH_LOG.md').read_bytes()==derive_case_log(log_baseline,g,z,tr,cur['factual_timestamps'],100 if merged else 95),'Interrupted existing case/log generation; reconcile');return cur
 if merged:
  a=read(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json');require(a['PR_merged'] and a['every_selected_identity_checked_at_actual_observed_MAIN'],'Accepted actual merge absent')
  prior=current_native(g,False,(z,tr));baseline,log_baseline=case_baselines(g);require(canonical_json(read(A/'CURRENT_CASE_STATUS.json'))==canonical_json(derive_case_stage(baseline,g,z,tr,prior['factual_timestamps'],95,z['gate_sha256'])) and (A/'RESEARCH_LOG.md').read_bytes()==derive_case_log(log_baseline,g,z,tr,prior['factual_timestamps'],95),'Source95 case/log is not its exact approved generation');times={**prior['factual_timestamps'],'merged':now()}
 else:
  baseline,log_baseline=case_baselines(g);require(canonical_json(read(A/'CURRENT_CASE_STATUS.json'))==canonical_json(derive_case_ready(baseline,g,z['gate_sha256'])) and (A/'RESEARCH_LOG.md').read_bytes()==derive_case_log(log_baseline,g,z,tr,{},90),'Source90 case/log is not its exact approved generation');times={'published':now()}
 pending=pending_native_bytes(g);expected=derive_native(g,z,tr,pending,times,merged);T.mkdir(exist_ok=False)
 for n,b in expected.items():
  path=T/n;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b);path.chmod(0o444)
 changed=sorted(JSON_FACTS|TEXT_FACTS|{'RESEARCH_LOG.md'});cur={'UTC':now(),'current_template':name,'files':{n:pin(T/n) for n in expected},'original_head':HEAD,'gate_sha256':z['gate_sha256'],'actual_DOI':z['doi'],'actual_tracker_range':tr['range'],'factual_timestamps':times,'reviewed_scientific_bytes_preserved':True,'only_declared_factual_paths_changed':changed,'actual_original_PR_merged':merged,'MAIN_updated_by_preparation':False};write(I/'CURRENT_TEMPLATE.json',cur);write(I/(name+'_MANIFEST.json'),cur)
 case=derive_case_stage(baseline,g,z,tr,times,100 if merged else 95,z['gate_sha256']);write(A/'CURRENT_CASE_STATUS.json',case);(A/'RESEARCH_LOG.md').write_bytes(derive_case_log(log_baseline,g,z,tr,times,100 if merged else 95));return cur

def expected_native_receipt(cur,g,z,tr,merged):
 name=g['native_complete_template'] if merged else g['native_final_template']
 require(set(cur)=={'UTC','current_template','files','original_head','gate_sha256','actual_DOI','actual_tracker_range','factual_timestamps','reviewed_scientific_bytes_preserved','only_declared_factual_paths_changed','actual_original_PR_merged','MAIN_updated_by_preparation'},'Native generation receipt schema differs')
 require(cur['current_template']==name and cur['original_head']==HEAD and cur['gate_sha256']==z['gate_sha256'] and cur['actual_DOI']==z['doi'] and cur['actual_tracker_range']==tr['range'],'Native generation factual binding drift')
 valid_stamp(cur['UTC']);require(cur['actual_original_PR_merged'] is merged and cur['reviewed_scientific_bytes_preserved'] is True and cur['MAIN_updated_by_preparation'] is False and set(cur['only_declared_factual_paths_changed'])==JSON_FACTS|TEXT_FACTS|{'RESEARCH_LOG.md'},'Native generation receipt assertions drift')
 expected=derive_native(g,z,tr,pending_native_bytes(g),cur['factual_timestamps'],merged);legal_fact_time(cur['factual_timestamps']['published'],z,tr,95);legal_fact_time(cur['UTC'],z,tr,100 if merged else 95);require(valid_stamp(cur['UTC'])>=valid_stamp(cur['factual_timestamps']['merged' if merged else 'published']),'Native receipt predates its factual transformation')
 if merged:legal_fact_time(cur['factual_timestamps']['merged'],z,tr,100)
 require(set(cur['files'])==set(expected),'Native current inventory incomplete/differs from manifest')
 for n,b in expected.items():require(cur['files'][n]==byte_pin(b),'Native generation pin differs from deterministic expected bytes '+n)
 return expected

def byte_pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def current_native(g,merged=False,facts=None):
 z,tr=facts if facts is not None else published_tracked()[1:];cur=read(A/'integration_preparation/CURRENT_TEMPLATE.json');expected=expected_native_receipt(cur,g,z,tr,merged);T=inside('integration_preparation/'+cur['current_template'])
 require(inventory(T)==set(expected),'Native current inventory incomplete/differs from manifest');require((A/'integration_preparation/CURRENT_TEMPLATE.json').read_bytes()==(A/'integration_preparation'/(cur['current_template']+'_MANIFEST.json')).read_bytes(),'Current native companion manifest differs from pointer')
 for n,b in expected.items():require((T/n).read_bytes()==b,'Unapproved full native byte/JSON/text/log transformation '+n)
 return cur

def verify_prepared_native(h,g,z,tr,r,merged=False):
 pointer=CASE+'integration_preparation/CURRENT_TEMPLATE.json';b=h.body_at(pointer,r['commit']);require(byte_pin(b)==r['selected_files'][pointer],'Prepared native pointer identity differs');cur=json.loads(b);expected=expected_native_receipt(cur,g,z,tr,merged)
 manifest=CASE+'integration_preparation/'+cur['current_template']+'_MANIFEST.json';mb=h.body_at(manifest,r['commit']);require(mb==b and byte_pin(mb)==r['selected_files'][manifest],'Native companion manifest differs from independently checked pointer')
 for n,content in expected.items():
  x=byte_pin(content)
  for path in [NATIVE+n,CASE+'integration_preparation/'+cur['current_template']+'/'+n]:require(r['selected_files'][path]==x,'Prepared native bytes differ from exact approved factual derivation '+path)
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
def merge_message(z):return 'Merge PR191: credited parity-selected signed-angle law and literal counterexamples; '+z['doi_url']
def factual_message(z):return 'Record PR191 factual40/24 completion; actual acceptance required before192; '+z['doi_url']
def operative_message(z,parents,digest):
 require(len(parents) in [1,2] and (len(parents)==1 or parents[1]==HEAD),'Unexpected operative commit parent schema')
 return (merge_message(z) if len(parents)==2 else factual_message(z))+'\n\nPR191 selected-map SHA256: '+digest

def verify_prepared(h,r,parents):
 require(r.get('original_head')==HEAD and r.get('gate_sha256')==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Preparation head/gate binding drift')
 co=h.api('git/commits/'+r['commit']);require(co['tree']['sha']==r['tree'] and [x['sha'] for x in co['parents']]==parents,'Prepared tree/parent drift')
 parent_tree=h.api('git/commits/'+parents[0])['tree']['sha'];require(r['parent_tree']==parent_tree,'Receipt parent tree differs from actual first parent')
 digest=selected_digest(r['selected_files']);g=gate();z=validate_publication(g,read(A/'ZENODO_PUBLICATION_READBACK.json'));require(r.get('selected_map_sha256')==digest and co.get('message')==operative_message(z,parents,digest),'Exact approved operative commit message/map binding drift')
 h.m.m.h.warm_selected_directories([parent_tree,r['tree']],r['selected_files'])
 for n,x in r['selected_files'].items():require(h.lookup(r['tree'],n)==('100644','blob',x['git_blob']),'Prepared selected identity drift')
 changed={n for n,x in r['selected_files'].items() if h.lookup(parent_tree,n)!=('100644','blob',x['git_blob'])};require(set(r['changed_paths'])==changed and h.changed_leaves(parent_tree,r['tree'])==changed,'Full-tree foreign scope drift')
 return co
def scope_names(g):
 files=read(match_path(g['native_pending_manifest']))['files'];names=set(g['public_case_paths'])|set(g['public_case_pins'])|set(CONTROL_FILES)|{'ROOT_PUBLICATION_GATE.json','PR_METADATA_REQUEST.json','PR_METADATA_ACCEPTANCE.json','ZENODO_LOCAL_CHECK.json','ZENODO_STAGE_READBACK.json','ZENODO_DRAFT_READBACK.json','ZENODO_PUBLICATION_READBACK.json','ZENODO_PUBLICATION_EVIDENCE.json','ZENODO_POSTPUBLICATION_INSPECTION.json','TRACKER_ACCEPTANCE.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','FINAL_MAIN_SCOPE.json','ORIGINAL_FILE_MANIFEST.json','INTAKE_CHECKPOINT_ACCEPTANCE.json','ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json','integration_preparation/CURRENT_TEMPLATE.json','integration_preparation/'+g['native_final_template']+'_MANIFEST.json'}
 names.update([g['current_proof']['path'],g['native_pending_manifest']['path'],g['review_input']['path'],g['pr_metadata_proposal']['path'],g['tracker_row_proposal']['path']]);names.update(x['path'] for x in review_bindings(g));names.update(x['path'] for x in operational_bindings(g));names.update(g['package_name']+'/'+n for n in g['payloads']);names.update('integration_preparation/'+g['native_final_template']+'/'+n for n in files);names.update('sheets_tracking/'+n for n in ['TARGET_VALIDATION.json','ROW_READBACK_1.json','ROW_READBACK_2.json','POSTAPPEND_UNIQUENESS_1.json','POSTAPPEND_UNIQUENESS_2.json']);return names
def trusted_case_pins(g,names):
 """Independent selected expectations, derived from Root authority and local bound inputs."""
 expected={}
 def add(n,x):
  actual=match(inside(n),x)
  if n in expected:require(expected[n]==actual,'Conflicting trusted case source pins '+n)
  expected[n]=actual
 for n,x in g['public_case_pins'].items():add(n,x)
 for n,x in g['payloads'].items():add(g['package_name']+'/'+n,x)
 for x in [g[k] for k in ['current_proof','native_pending_manifest','review_input','pr_metadata_proposal','tracker_row_proposal']]+review_bindings(g)+operational_bindings(g):add(x['path'],x)
 for n,x in operational_clearance(g)['runtime_pins'].items():add(n,x)
 add('ROOT_PUBLICATION_GATE.json',pin(A/'ROOT_PUBLICATION_GATE.json'))
 # These three live factual paths intentionally change after the accepted merge.
 # Their native/prepared postimages are checked independently, not against new local phase100 bytes.
 mutable={'CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json'}
 for n in set(names)-mutable:add(n,pin(inside(n)))
 return {CASE+n:x for n,x in expected.items()}

def verify_merge_scope(h,g,r,accepted=False):
 verify_prepared(h,r,[r['expected_main'],HEAD]);require_merge_scope(g,r)
 b=h.body_at(CASE+'FINAL_MAIN_SCOPE.json',r['commit']);require(b==(A/'FINAL_MAIN_SCOPE.json').read_bytes(),'Local/immutable prepared scope bytes differ');scope=json.loads(b)
 x=r['selected_files'][CASE+'FINAL_MAIN_SCOPE.json'];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Immutable scope byte/hash binding drift')
 require(scope['PR']==PR and scope['original_head']==HEAD and scope['gate_sha256']==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'Immutable scope identity/gate drift')
 actual=set(scope['case_paths']);mandatory=scope_names(g);optional={'sheets_tracking/'+n for n in ['APPEND_REQUEST.json','APPEND_ATTEMPT_STARTED.json','APPEND_RESPONSE.json']};require(len(actual)==len(scope['case_paths']) and mandatory<=actual<=mandatory|optional,'Immutable scope omits/adds intended case paths')
 native=read(match_path(g['native_pending_manifest']))['files'];expected={CASE+n for n in actual}|{NATIVE+n for n in native}|{PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}|{'unsolved_math_prioritization/QUEUE.md'}
 require(len(set(scope['selected_MAIN_paths']))==len(scope['selected_MAIN_paths']) and set(scope['selected_MAIN_paths'])==expected==set(r['selected_files']),'Exact immutable selected MAIN scope differs')
 for n,x in trusted_case_pins(g,actual).items():require(r['selected_files'].get(n)==x,'Selected immutable case identity differs from trusted gate/source '+n)
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
def derive_programme_stage(before,g,z,tr,phase,stamp,intake,gate_sha256,merge_commit=None):
 require(phase in [95,100],'Unsupported programme stage');valid_stamp(stamp);j=copy.deepcopy(before)
 for key,count in [('fully_completed_eligible_PRs',39),('published_PRs',23)]:
  old=before[key];require(isinstance(old,list) and all(type(v) is int for v in old) and len(old)==len(set(old))==count and PR not in old,'True-parent programme sets differ')
 require((j['fully_completed_count'],j['published_count'],j['last_completed_PR'],j['current_PR'])==(39,23,190,191),'Current programme ownership/census drift')
 if phase==100:
  require(PR not in j['fully_completed_eligible_PRs'] and PR not in j['published_PRs'],'Already counted');j['fully_completed_eligible_PRs'].append(PR);j['published_PRs'].append(PR)
  require(len(set(j['fully_completed_eligible_PRs']))==len(j['fully_completed_eligible_PRs'])==40 and len(set(j['published_PRs']))==len(j['published_PRs'])==24,'Unique factual census')
  j.setdefault('historical_completion_snapshots_PR191',[]).append({'UTC':stamp,'prior_PR':190,'values':{k:copy.deepcopy(v) for k,v in before.items() if k.startswith('last_completed_') or k.startswith('last_published_')}})
  j.update(fully_completed_count=40,published_count=24,last_completed_PR=PR,last_published_PR=PR,last_completed_original_head=HEAD,last_completed_original_budget='2/5',last_completed_original_QUEUE_status='claimed_solved',last_completed_DOI=z['doi'],last_published_DOI=z['doi'],last_completed_merge_commit=merge_commit,last_completed_tracker_range=tr['range'],last_completed_record='audits/pr191_5000005/WORKFLOW_COMPLETION.json',last_completed_outcome='published_credited_parity_selected_signed_law_and_literal_counterexamples');j['skipped_before_last_completion']=j.get('skipped_since_last_completion',[]);j['skipped_since_last_completion']=[]
 j.update(UTC=stamp,updated_UTC=stamp,current_PR=PR,current_status='PUBLISHED_TRACKED_'+('ORIGINAL_HEAD_MERGED_FACTUAL_ACCEPTANCE_REQUIRED' if phase==100 else 'ORIGINAL_HEAD_MERGE_PENDING'),current_PR_workflow_percent=phase,current_workflow_estimate_percent=phase,current_mathematics_cleared=True,current_bounded_priority_audit_complete=True,current_publication_ready=True,current_publication_package_reviews_complete=True,current_publication_package_reviews_required=False,current_Zenodo_published=True,current_DOI=z['doi'],current_tracker_updated=True,current_tracker_range=tr['range'],current_original_PR_merged=phase==100,current_closed=phase==100,current_record='audits/pr191_5000005/CURRENT_CASE_STATUS.json',current_remaining_required_steps='Actual factual MAIN acceptance before intake192.' if phase==100 else 'Original-head merge/full current-tree acceptance and factual completion before intake192.')
 return normalize_programme(j,g,intake,phase,stamp,gate_sha256)
def progress(j,g,z,tr,phase):
 stamp=now();merge=read(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')['merge_commit'] if phase==100 else None
 return derive_programme_stage(j,g,z,tr,phase,stamp,read(A/'INTAKE_CHECKPOINT_ACCEPTANCE.json'),z['gate_sha256'],merge)
def legal_fact_time(value,z,tr,phase):
 stamp=valid_stamp(value);lower=max(valid_stamp(z['verified_utc']),valid_stamp(tr['UTC']))
 if phase==100:lower=max(lower,valid_stamp(read(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')['UTC']))
 require(lower<=stamp<=valid_stamp(now()),'Actual factual timestamp outside accepted evidence/current-clock interval');return stamp

def programme_suffix(phase):return ' — '+('PR191 workflow95%, exact credited note published/tracked; merge and factual acceptance pending;39/23 unchanged.' if phase==95 else 'PR191 factual40/24 postimage; actual factual MAIN acceptance required before192.')+'\n'

def workflow_values(z,tr,merge):return {'PR':PR,'original_head':HEAD,'original_effort':'2/5','status':'FACTUAL_COMPLETE_POSTIMAGE_REQUIRES_ACTUAL_MAIN_ACCEPTANCE','fully_completed_count':40,'published_count':24,'case_percent':100,'goal_complete':False,'DOI':z['doi'],'tracker_range':tr['range'],'actual_merge_commit':merge,'next_original_status_intake':NEXT,'claim':CLAIM}

def validate_case_stage(case,g,z,tr,phase,factual_timestamps):
 baseline,_=case_baselines(g);expected=derive_case_stage(baseline,g,z,tr,factual_timestamps,phase,z['gate_sha256']);legal_fact_time(case.get('UTC'),z,tr,phase)
 require(canonical_json(case)==canonical_json(expected),'Complete current case stage projection differs')

def validate_programme_stage(before,after,g,z,tr,phase,merge=None):
 stamp=after.get('UTC');require(legal_fact_time(stamp,z,tr,phase)<=legal_fact_time(after.get('updated_UTC'),z,tr,phase),'Programme UTC is later than updated_UTC')
 expected=derive_programme_stage(before,g,z,tr,phase,stamp,read(A/'INTAKE_CHECKPOINT_ACCEPTANCE.json'),z['gate_sha256'],merge)
 require(canonical_json(after)==canonical_json(expected),'Complete programme stage projection differs')

def verify_stage_postimage(h,g,z,tr,r,phase,merge=None):
 if phase==95:
  q='unsolved_math_prioritization/QUEUE.md';expected=queue_update(h.body_at(q,r['expected_main']).decode(),h.body_at(q,HEAD).decode(),h.body_at(q,ORIGINAL_BASE).decode(),z['doi'],z['doi_url']).encode();require(h.body_at(q,r['commit'])==expected and r['selected_files'].get(q)==byte_pin(expected),'Prepared QUEUE differs from exact true-parent/original-head/BASE transformation')
 before=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',r['expected_main']));after=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',r['commit']));case=json.loads(h.body_at(CASE+'CURRENT_CASE_STATUS.json',r['commit']));cur=json.loads(h.body_at(CASE+'integration_preparation/CURRENT_TEMPLATE.json',r['commit']));expected_native_receipt(cur,g,z,tr,phase==100);validate_programme_stage(before,after,g,z,tr,phase,merge);validate_case_stage(case,g,z,tr,phase,cur['factual_timestamps']);_,log_baseline=case_baselines(g);require(h.body_at(CASE+'RESEARCH_LOG.md',r['commit'])==derive_case_log(log_baseline,g,z,tr,cur['factual_timestamps'],phase),'Complete current case log stage projection differs')
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:
  prior=h.body_at(PREFIX+n,r['expected_main']);current=h.body_at(PREFIX+n,r['commit']);require(current.startswith(prior+b'\n'),'Programme dated history prefix changed');added=current[len(prior)+1:].decode();suffix=programme_suffix(phase);require(added.endswith(suffix),'Programme current factual prose differs');stamp=added[:-len(suffix)];legal_fact_time(stamp,z,tr,phase);require(stamp==after['UTC'],'Programme current prose and JSON stage timestamps differ')

 if phase==100:
  for n in ['SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json']:require(r['selected_files'].get(CASE+n)==pin(A/n),'Factual original merge authority receipt identity differs '+n)
  workflow=json.loads(h.body_at(CASE+'WORKFLOW_COMPLETION.json',r['commit']));legal_fact_time(workflow.get('UTC'),z,tr,100);require(set(workflow)=={'UTC'}|set(workflow_values(z,tr,merge)) and all(type(workflow.get(k)) is type(v) and workflow.get(k)==v for k,v in workflow_values(z,tr,merge).items()),'Exact workflow completion factual schema/values differ')

def integration_prepare(gen):
 g,z,tr=published_tracked();p=original_ready(False);require_metadata(g,z,tr,p)
 require(re.fullmatch('merge_preparation_[a-z0-9_]+',gen),'Generation name');h=helpers();e=h.api('git/ref/heads/main')['object']['sha'];plan=read(A/'FINAL_MAIN_SCOPE.json');require(plan['gate_sha256']==z['gate_sha256'],'Scope gate drift');out=A/'integration_preparation'/gen;out.mkdir(exist_ok=False)
 q='unsolved_math_prioritization/QUEUE.md';before=h.body_at(q,e).decode();original=h.body_at(q,HEAD).decode();base=h.body_at(q,ORIGINAL_BASE).decode();write(out/'QUEUE.md',queue_update(before,original,base,z['doi'],z['doi_url']))
 j=progress(json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',e)),g,z,tr,95);write(out/'CURRENT_PROGRESS.json',j)
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:write(out/n,h.body_at(PREFIX+n,e).decode()+'\n'+j['UTC']+programme_suffix(95))
 cur=current_native(g,False);native=A/'integration_preparation'/cur['current_template']
 overlay={CASE+n:inside(n) for n in plan['case_paths']};overlay.update({NATIVE+n:native/n for n in cur['files']});overlay.update({PREFIX+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']});overlay[q]=out/'QUEUE.md';require(set(overlay)==set(plan['selected_MAIN_paths']),'Exact final scope drift')
 r=prepare_tree(h,e,overlay,[e,HEAD],merge_message(z),'SCOPED_MERGE_PREPARATION.json');verify_merge_scope(h,g,r);verify_stage_postimage(h,g,z,tr,r,95);original_ready(False);return r
def integration_accept():
 g,z,tr=published_tracked();h=helpers();r=read(A/'SCOPED_MERGE_PREPARATION.json');scope_sha=verify_merge_scope(h,g,r);verify_prepared_native(h,g,z,tr,r,False);verify_stage_postimage(h,g,z,tr,r,95);actual=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+actual)['status'] in ['identical','ahead'],'Prepared merge not on MAIN');selected_current(h,actual,r['selected_files'],r['tree']);p=h.api('pulls/'+str(PR));require(p['merged'] and p['state']=='closed' and p['head']['sha']==HEAD,'Original PR merge not accepted')
 cur=read(A/'integration_preparation/CURRENT_TEMPLATE.json');reads=[NATIVE+n for n in g['native_proof_paths']]+[CASE+g['package_name']+'/'+n for n in g['paper_files'].values()]
 for n in reads:
  b=h.body_at(n,actual);x=r['selected_files'][n];require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh scientific body drift')
 out={'UTC':now(),'PR':PR,'status':'ACTUAL_ORIGINAL_HEAD_TWO_PARENT_MERGE_FULL_SCOPE_CURRENT_IDENTITIES_ACCEPTED','PR_merged':True,'original_head':HEAD,'gate_sha256':r['gate_sha256'],'merge_commit':r['commit'],'merge_tree':r['tree'],'scope_sha256':scope_sha,'selected_map_sha256':r['selected_map_sha256'],'main_observed':actual,'every_selected_identity_checked_at_actual_observed_MAIN':True,'selected_files':len(r['selected_files']),'parents':[r['expected_main'],HEAD],'DOI':z['doi'],'factual_completion_pending':True};write(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',out);return out
def factual_paths(g):
 files=read(match_path(g['native_pending_manifest']))['files'];names=['SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json','WORKFLOW_COMPLETION.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json','integration_preparation/'+g['native_complete_template']+'_MANIFEST.json'];names+=['integration_preparation/'+g['native_complete_template']+'/'+n for n in files]
 return {CASE+n for n in names}|{NATIVE+n for n in files}|{PREFIX+n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
def factual_prepare(gen):
 g,z,tr=published_tracked();a=read(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json');require(a['PR_merged'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and a['original_head']==HEAD,'Actual accepted merge absent');h=helpers();p=h.api('pulls/'+str(PR));require(p['merged'] and p['state']=='closed' and p['head']['sha']==HEAD,'Original PR completion drift')
 require(re.fullmatch('factual_preparation_[a-z0-9_]+',gen),'Generation name');e=h.api('git/ref/heads/main')['object']['sha'];merged=read(A/'SCOPED_MERGE_PREPARATION.json');verify_merge_scope(h,g,merged,True);verify_prepared_native(h,g,z,tr,merged,False);verify_stage_postimage(h,g,z,tr,merged,95);require(h.api('compare/'+merged['commit']+'...'+e)['status'] in ['identical','ahead'],'Original accepted merge not on factual parent');selected_current(h,e,merged['selected_files'],merged['tree']);j=progress(json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',e)),g,z,tr,100)
 cur=prepare_native(True);case=read(A/'CURRENT_CASE_STATUS.json');case.update(completed=40,published=24,fully_completed_count=40,published_count=24,case_completion_requires_actual_factual_postimage_acceptance=True);write(A/'CURRENT_CASE_STATUS.json',case)
 write(A/'WORKFLOW_COMPLETION.json',{'UTC':now(),**workflow_values(z,tr,a['merge_commit'])})
 out=A/'integration_preparation'/gen;out.mkdir(exist_ok=False);write(out/'CURRENT_PROGRESS.json',j)
 for n in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:write(out/n,h.body_at(PREFIX+n,e).decode()+'\n'+j['UTC']+programme_suffix(100))
 names=['SCOPED_MERGE_PREPARATION.json','ROOT_ACTUAL_MERGE_ACCEPTANCE.json','WORKFLOW_COMPLETION.json','CURRENT_CASE_STATUS.json','RESEARCH_LOG.md','integration_preparation/CURRENT_TEMPLATE.json','integration_preparation/'+cur['current_template']+'_MANIFEST.json'];names+=['integration_preparation/'+cur['current_template']+'/'+n for n in cur['files']]
 overlay={CASE+n:inside(n) for n in names};overlay.update({NATIVE+n:A/'integration_preparation'/cur['current_template']/n for n in cur['files']});overlay.update({PREFIX+n:out/n for n in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']});plan=read(A/'FINAL_MAIN_SCOPE.json');require(set(overlay)==factual_paths(g) and set(overlay)<=set(plan['selected_MAIN_paths']+plan['factual_additional_paths']),'Outside exact factual scope')
 r=prepare_tree(h,e,overlay,[e],factual_message(z),'FINAL_FACTUAL_PREPARATION.json');verify_stage_postimage(h,g,z,tr,r,100,a['merge_commit']);return r
def factual_accept():
 g,z,tr=published_tracked();h=helpers();r=read(A/'FINAL_FACTUAL_PREPARATION.json');verify_prepared(h,r,[r['expected_main']]);verify_prepared_native(h,g,z,tr,r,True);verify_stage_postimage(h,g,z,tr,r,100,read(A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')['merge_commit']);actual=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+actual)['status'] in ['identical','ahead'],'Factual commit not on MAIN');merged=read(A/'SCOPED_MERGE_PREPARATION.json');verify_merge_scope(h,g,merged,True);verify_prepared_native(h,g,z,tr,merged,False);verify_stage_postimage(h,g,z,tr,merged,95);require(h.api('compare/'+merged['commit']+'...'+actual)['status'] in ['identical','ahead'],'Original accepted merge not on actual MAIN');require(set(r['selected_files'])==factual_paths(g),'Exact factual selected scope drift');combined={**merged['selected_files'],**r['selected_files']};selected_current(h,actual,combined,r['tree'])
 for n,x in r['selected_files'].items():
  b=h.body_at(n,actual);require(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'Fresh factual body drift')
 p=h.api('pulls/'+str(PR));require(p['merged'] and p['state']=='closed' and p['head']['sha']==HEAD,'Original PR completion drift')
 out={'UTC':now(),'PR':PR,'status':'ACTUAL_FACTUAL_COMPLETION_MAIN_PARENT_FULL_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED','factual_commit':r['commit'],'main_observed':actual,'sole_parent':r['expected_main'],'combined_expected_current_identities_checked':len(combined),'every_selected_identity_checked_at_actual_observed_MAIN':True,'fully_completed_count':40,'published_count':24,'case_percent':100,'goal_complete':False,'next_original_status_intake':NEXT,'next_numeric_intake_cursor_authorized_after_this_acceptance':NEXT,'subsequent_status_only_intake_authorized':True,'live_programme_cursor_update_requires_next_own_checkpoint':True,'separate_selfreceipt_publication_required_at_next_own_checkpoint':True};write(A/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json',out);return out
