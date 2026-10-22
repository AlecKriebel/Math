"""PR206 local gate validation and durable records; imports perform no operations."""
import sys
sys.dont_write_bytecode=True
import datetime,hashlib,json,os,pathlib,stat

PR=206
PROBLEM=5100062
PREFIX='draft_pr_publication_program_20260930/audits/pr206_5100062/'
HEAD='488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7'
OWN='publication_operations_preparation_02'
CODES=('ops_common206.py','publisher206.py','tracker206.py','offline_guards.py','run_offline.py')
PRIOR_OVERLAP_DOI='10.5281/zenodo.23096994'
PRIORITY_PIN={'bytes':5297,'sha256':'f81e10f7e0b45659b97080438c7bd7cfdb695d73c3c35e54bf6e14dec2a7f45b'}
CUSTODY_PIN={'bytes':1919,'sha256':'b3f5a5e4489aac7eec1ded4270214de954b6e540aa644df0823db005bf31a9d4'}
_authority=None
KIT_SHA='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca'

def require(ok,message):
 if type(ok) is not bool:raise TypeError('Guard predicate must be an actual bool')
 if not ok:raise RuntimeError(message)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def encoded(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'
def digest(raw):return hashlib.sha256(raw).hexdigest()
def pin(path):
 raw=path.read_bytes();return dict(bytes=len(raw),sha256=digest(raw))
def reject_constant(value):raise RuntimeError('Nonfinite JSON value')
def read(path):return json.loads(path.read_text(),parse_constant=reject_constant)
def read_pinned(path,wanted):
 require(type(wanted) is dict and set(wanted)=={'bytes','sha256'} and type(wanted['bytes']) is int and wanted['bytes']>0 and type(wanted['sha256']) is str and len(wanted['sha256'])==64 and all(x in '0123456789abcdef' for x in wanted['sha256']),'Malformed pinned JSON identity')
 raw=path.read_bytes();require({'bytes':len(raw),'sha256':digest(raw)}==wanted,'Pinned JSON bytes changed before parsing')
 return json.loads(raw,parse_constant=reject_constant)
def child(root,relative):
 require(isinstance(relative,str) and relative and not pathlib.PurePosixPath(relative).is_absolute() and '..' not in pathlib.PurePosixPath(relative).parts,'Unsafe relative path')
 p=root/relative;require(p.resolve()==p,'Symlinked path refused');return p
def regular_pinned_input(path):
 require(path.is_file() and not path.is_symlink() and stat.S_ISREG(path.stat().st_mode),'Missing/nonregular pinned review file: '+str(path))
def sealed(path):
 require(path.is_file() and not path.is_symlink() and stat.S_ISREG(path.stat().st_mode) and stat.S_IMODE(path.stat().st_mode)==0o444,'Missing/nonsealed file: '+str(path))
def native_identity(path):
 raw=path.read_bytes();return dict(bytes=len(raw),sha256=digest(raw),git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())
def fsync_dir(path):
 fd=os.open(path,os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
def private_directory(path):
 require(path.resolve()==path,'Symlinked private directory ancestor refused')
 missing=[];p=path
 while not p.exists():missing.append(p);p=p.parent
 require(p.is_dir() and not p.is_symlink(),'Unsafe private directory parent')
 for q in reversed(missing):q.mkdir(mode=0o700);fsync_dir(q);fsync_dir(q.parent)
 require(path.is_dir() and not path.is_symlink(),'Unsafe private directory')
def durable_json(path,value,readonly=False):
 require(type(readonly) is bool,'Readonly flag must be an actual bool')
 require(path.parent.is_dir() and not path.parent.is_symlink(),'Output parent missing/unsafe')
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:
  data=encoded(value);view=memoryview(data)
  while view:
   n=os.write(fd,view);require(n>0,'Zero durable write');view=view[n:]
  if readonly:os.fchmod(fd,0o444)
  os.fsync(fd)
 finally:os.close(fd)
 fsync_dir(path.parent)
 return path

def upload_names(g):
 names=set(g['intended_upload_files'])
 require(len(names)==3 and all(type(n) is str and n and pathlib.Path(n).name==n and '\\' not in n for n in names) and sorted(pathlib.Path(n).suffix.lower() for n in names)==['.pdf','.tex','.zip'],'Exactly one final gate-pinned PDF, TEX and ZIP basename required')
 return names
def configure_authority(relative,wanted):
 global _authority
 require(isinstance(wanted,dict) and set(wanted)=={'bytes','sha256'} and type(wanted['bytes']) is int and wanted['bytes']>0 and isinstance(wanted['sha256'],str) and len(wanted['sha256'])==64 and all(x in '0123456789abcdef' for x in wanted['sha256']),'Exact explicit Root adoption pin required')
 _authority=(relative,dict(wanted))
def authority(base):
 require(_authority is not None,'Missing explicit fresh Root operations adoption; no operation allowed')
 relative,wanted=_authority;ap=child(base,relative);sealed(ap);a=read_pinned(ap,wanted)
 require(a.get('schema')=='pr206-root-publication-operations-adoption-v1' and a.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and a.get('accepted_preparation_only') is True and a.get('PR')==PR and a.get('original_head')==HEAD,'Root operations source adoption not accepted')
 sources=a.get('sources');require(isinstance(sources,dict) and set(sources)=={OWN+'/'+n for n in CODES},'Exact five operations source pins required')
 here=pathlib.Path(__file__).resolve().parent
 for name,w in sources.items():
  p=child(base,name);sealed(p);require(pin(p)==w and pin(here/pathlib.Path(name).name)==w,'Adopted/current executing operations source changed')
 wanted_gate=a.get('approved_publication_gate_pin')
 require(isinstance(wanted_gate,dict) and set(wanted_gate)=={'bytes','sha256'} and type(wanted_gate['bytes']) is int and wanted_gate['bytes']>0 and isinstance(wanted_gate['sha256'],str) and len(wanted_gate['sha256'])==64 and all(x in '0123456789abcdef' for x in wanted_gate['sha256']),'Actual final gate approval pin absent')
 wanted_ready=a.get('approved_actual_ready_pointer_pin')
 require(isinstance(wanted_ready,dict) and set(wanted_ready)=={'bytes','sha256'} and type(wanted_ready['bytes']) is int and wanted_ready['bytes']>0 and isinstance(wanted_ready['sha256'],str) and len(wanted_ready['sha256'])==64 and all(x in '0123456789abcdef' for x in wanted_ready['sha256']),'Exact independently adopted actual90 pointer pin absent')
 wanted_verification=a.get('approved_actual_ready_verification_pin')
 wanted_addendum=a.get('approved_operations_contract_addendum_pin')
 dispatcher=a.get('dispatcher_pin')
 for value,label in [(wanted_verification,'actual ready verification'),(wanted_addendum,'operations contract addendum'),(dispatcher,'adopted dispatcher')]:
  require(type(value) is dict and set(value)=={'bytes','sha256'} and type(value['bytes']) is int and value['bytes']>0 and type(value['sha256']) is str and len(value['sha256'])==64 and all(x in '0123456789abcdef' for x in value['sha256']),'Exact independently adopted '+label+' pin absent')
 addendum_path=base/'ROOT_PUBLICATION_OPERATIONS_CONTRACT_ADDENDUM_01.json';sealed(addendum_path);addendum=read_pinned(addendum_path,wanted_addendum)
 require(addendum.get('schema')=='pr206-root-postready-operations-contract-addendum-v1' and addendum.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and addendum.get('PR')==PR and addendum.get('accepted') is True and addendum.get('original_head')==HEAD,'Root postready operational addendum identity/scope missing')
 require(addendum.get('publication_gate_pin')==wanted_gate and addendum.get('actual_ready_pointer_pin')==wanted_ready and addendum.get('actual_ready_verification_pin')==wanted_verification,'Addendum gate/ready/proof binding differs')
 require(addendum.get('source_family')==OWN and addendum.get('sources')==sources and addendum.get('dispatcher_pin')==dispatcher,'Addendum source/dispatcher contract differs')
 for field in ('scientific_package_metadata_uploads_unchanged','prior_native_selected_original07_files_preserved','operations_sources_approved_after_original_ready_checkpoint','not_a_new_scientific_or_priority_clearance','no_advance_or_completion_granted'):
  require(addendum.get(field) is True,'Postready contract qualifier missing: '+field)
 require(addendum.get('executed_current_sources_claimed_present_in_original_ready_map') is False,'Current operators must not be claimed in original ready map')
 return {'gate_pin':wanted_gate,'ready_pointer_pin':wanted_ready,'ready_verification_pin':wanted_verification,'operations_contract_addendum_pin':wanted_addendum}

def ready_facts(ac,g):
 # These two editorial qualifications are nested facts, not lifecycle receipt aliases.
 facts=ac.get('facts');require(type(facts) is dict and ac.get('phase')=='ready','Actual ready phase/facts missing')
 for field in ('bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','priority_clearance','publication_ready'):
  require(facts.get(field) is True,'Actual ready facts not accepted: '+field)
 require(facts.get('priority_clearance_scope')=='qualified_attributed_note_only','Actual ready qualified-priority scope changed')
 for field in ('priority_novelty_clearance','historical_firstness_independence_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged','completed','advance_to_next_PR_authorized_now','goal_complete','actual_factual_accepted','actual_merge_accepted'):
  require(facts.get(field) is False,'Unsupported actual ready fact: '+field)
 for field in ('DOI','record_id','tracker_range'):require(facts.get(field) is None,'Premature actual ready publication/operation fact: '+field)
 for field,value in [('case_percent',90),('fully_completed_count',48),('published_count',32),('last_completed_PR',205),('next_numeric_intake_cursor',206)]:
  require(type(facts.get(field)) is int and facts[field]==value,'Actual ready counters/phase differ: '+field)
 require(type(facts.get('NEW_whole_package_reviews_completed')) is int and facts['NEW_whole_package_reviews_completed']==len(g['whole_package_review_events']),'Actual ready review count differs')
 require(facts.get('package')==g['package'] and facts.get('package_seal')==g['package_seal'] and facts.get('Root_publication_gate_pin')==ac['Root_publication_gate_pin'],'Actual ready nested package/gate differs')
 aliases=('Root_publication_gate_pin','package','package_seal','publication_ready','NEW_whole_package_reviews_completed','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','priority_clearance','priority_novelty_clearance','historical_firstness_independence_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged','completed','fully_completed_count','published_count','last_completed_PR','next_numeric_intake_cursor','advance_to_next_PR_authorized_now','goal_complete')
 for field in aliases:require(type(ac.get(field)) is type(facts.get(field)) and ac.get(field)==facts.get(field),'Actual ready fact alias differs: '+field)

def ready_verification(base,approved,r,ac,selected,mp,gp):
 vp=base/'ROOT_ACTUAL_READY_VERIFICATION_01.json';sealed(vp);v=read_pinned(vp,approved['ready_verification_pin'])
 require(v.get('schema')=='pr206-root-actual-ready-verification-v1' and v.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and type(v.get('PR')) is int and v['PR']==PR,'Independent Root actual-ready verification identity/scope differs')
 for field in ('accepted','actual_ready90_fully_accepted_synced_and_pointer_verified','ready_candidate_changed_paths_exclude_QUEUE_and_all_native_attempts','original_native_custody_retained','every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','all_three_actual_steps_and_six_alias_cleanups_verified'):
  require(v.get(field) is True,'Independent ready verification flag missing: '+field)
 for field in ('actual_original_PR_merged','actual_publication','actual_tracker','advance'):require(v.get(field) is False,'Ready verification grants unsupported action: '+field)
 for field,value in [('completed_count',48),('published_count',32),('cursor',206),('case_completion_estimate_percent',90)]:
  require(type(v.get(field)) is int and v[field]==value,'Independent ready verification counters/phase differ: '+field)
 require(v.get('actual_ready_pointer_pin')==approved['ready_pointer_pin'] and v.get('actual_acceptance_pin')==r['acceptance_pin'] and v.get('actual_selected_map_file_pin')==ac['actual_current_map_file']==pin(mp) and v.get('actual_publication_gate_pin')==approved['gate_pin']==pin(gp),'Independent ready verification pointer/acceptance/map/gate cross-binding differs')
 require(v.get('checkpoint_commit')==ac['checkpoint_commit']==r['checkpoint_commit'] and v.get('actual_main_observed')==ac['main_observed']==r['main_observed'],'Independent ready verification checkpoint/MAIN differs')
 require(type(v.get('selected_files')) is int and type(ac.get('selected_files')) is int and v['selected_files']==ac['selected_files']==len(selected) and v.get('actual_selected_map_sha256')==ac['actual_current_selected_map_sha256'],'Independent full selected-map count/digest differs')
 require(type(v.get('ready_candidate_changed_path_count')) is int and 0<v['ready_candidate_changed_path_count']<=len(selected),'Independent changed-path count missing')
 for field in ('actual_original_PR_head','actual_original_PR_is_draft','actual_original_PR_state'):
  require(type(v.get(field)) is type(ac.get(field)) and v.get(field)==ac.get(field),'Independent ready verification original PR differs: '+field)
 paths={PREFIX+'CURRENT_CASE_STATUS.json',PREFIX+'RESEARCH_LOG.md'}|{'draft_pr_publication_program_20260930/'+n for n in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')}
 records=v.get('all_five_local_readonly_native_postimages')
 require(type(records) is list and len(records)==5,'Exactly five independently verified native postimages required')
 seen=set()
 for record in records:
  require(type(record) is dict and set(record)=={'path','identity','mode','regular'} and type(record['path']) is str and record['path'] in paths and record['path'] not in seen and record['mode']=='0o444' and record['regular'] is True,'Malformed/duplicate/nonreadonly native postimage')
  ident=record['identity'];require(type(ident) is dict and set(ident)=={'bytes','sha256','git_blob'} and type(ident['bytes']) is int and ident['bytes']>=0 and all(type(ident[k]) is str and len(ident[k])==n and all(x in '0123456789abcdef' for x in ident[k]) for k,n in [('sha256',64),('git_blob',40)]),'Malformed native postimage identity')
  require(selected.get(record['path'])==ident and encoded(selected[record['path']])==encoded(ident),'Native postimage differs from exact accepted historical map');seen.add(record['path'])
 require(seen==paths,'Native postimage path set differs')
 return vp

def load_context(base):
 """Pure local revalidation. Missing final gate, source adoption or actual ready90 refuses."""
 base=pathlib.Path(base).resolve();approved=authority(base);expected_gate=approved['gate_pin'];gp=base/'ROOT_PUBLICATION_GATE_01.json';sealed(gp);g=read_pinned(gp,expected_gate)
 require(g.get('PR')==PR and g.get('problem_id')==PROBLEM and g.get('original_head')==HEAD,'Wrong gate PR/problem/original HEAD')
 for field in ['publication_ready_gate_accepted','whole_package_review_loop_complete','mathematical_clearance','source_contract_clearance','bounded_priority_audit_complete','current_portable_verifier_accepted','qualified_attributed_note_editorially_cleared']:
  require(g.get(field) is True,'Root final gate not accepted: '+field)
 for field in ['historical_priority_established','theorem_novelty_cleared','formula_novelty_cleared','proof_method_novelty_cleared','first_disclosure_certified','independent_discovery_certified','literal_simultaneity_established','actual_publication_verified','actual_tracker_row_verified','actual_original_PR_merged','current_openness_established']:
  require(g.get(field,False) is False,'Unsupported readiness claim: '+field)
 events=g.get('whole_package_review_events');require(isinstance(events,list) and len(events)>=2,'Two fresh whole-package reviews required')
 require(len({e['directory'] for e in events})==len(events),'Review events are not distinct')
 require(len({e['review_number'] for e in events})==len(events) and len({e['Root_acceptance_file'] for e in events})==len(events),'Review acceptance events are not distinct')
 review_inputs={};repairs=False
 seal_file=g.get('package_seal_file','PACKAGE_SEAL.json')
 for index,e in enumerate(events,1):
  require(e['review_number']==index and e.get('whole_package_scope') is True,'Canonical whole-package review sequence/scope')
  require(isinstance(e['safe_files'],dict) and e['report_file'] in e['safe_files'] and e.get('report_pin')==e['safe_files'][e['report_file']],'Actual fresh whole-review report missing')
  review_dir=child(base,e['directory'])
  for rel,wanted in e['safe_files'].items():
   p=child(review_dir,rel);regular_pinned_input(p);require(pin(p)==wanted,'Whole-review artifact changed');review_inputs[e['directory']+'/'+rel]=p
  accepted=child(base,e['Root_acceptance_file']);regular_pinned_input(accepted);a=read_pinned(accepted,e['Root_acceptance_pin'])
  require(a.get('PR')==PR and a.get('original_head')==HEAD and a.get('review_accepted') is True and a.get('NEW_whole_package_reviews_completed')==index,'Actual Root whole-review acceptance identity')
  ae=a['review_event'];require(all(e.get(k)==val for k,val in ae.items()) and ae['safe_files']==e['safe_files'] and ae['reviewed_package']==e['reviewed_package'] and ae['reviewed_package_seal']==e['reviewed_package_seal'],'Root acceptance does not bind exact review event')
  review_inputs[e['Root_acceptance_file']]=accepted
  prior_seal=child(child(base,e['reviewed_package']),seal_file);sealed(prior_seal);require(pin(prior_seal)==e['reviewed_package_seal'],'Reviewed package seal changed')
  repairs=repairs or e['verdict']!='CLEANPASS' or a.get('review_cycle_repairs_required_now') is not False
 last=events[-1]
 require(last['verdict']=='CLEANPASS' and last.get('open_findings')==0 and last['reviewed_package']==g['package'] and last['reviewed_package_seal']==g['package_seal'] and a.get('review_cycle_repairs_required_now') is False,'Last CLEANPASS does not bind exact final package')
 if repairs:require(g.get('fresh_final_review_after_documented_editorial_repairs') is True,'Documented repairs need fresh final clean review')
 package=child(base,g['package']);safe=g['package_safe_files'];require(isinstance(safe,dict) and safe.get(seal_file)==g['package_seal'],'Final seal missing from safe files')
 actual=[]
 for p in package.rglob('*'):
  require(not p.is_symlink(),'Package symlink refused')
  if p.is_file():actual.append(p.relative_to(package).as_posix())
 require(set(actual)==set(safe),'Package file set differs from final gate')
 inputs={'ROOT_PUBLICATION_GATE_01.json':gp}
 for rel,wanted in safe.items():
  p=child(package,rel);sealed(p);require(pin(p)==wanted,'Package file changed: '+rel);inputs[g['package']+'/'+rel]=p
 names=upload_names(g)
 for name,wanted in g['intended_upload_files'].items():require(safe.get(name)==wanted and pin(package/name)==wanted,'Intended upload changed')
 metadata_file=g.get('metadata_file','zenodo-deposit.json');manifest=child(package,metadata_file);require(metadata_file in safe,'Metadata manifest omitted from final package map');m=read_pinned(manifest,safe[metadata_file])
 require(m.get('metadata')==g['metadata'] and set(m)=={'metadata','files'},'Manifest metadata differs from final gate')
 require(len(m['files'])==3 and all(set(x)=={'path'} for x in m['files']) and {x['path'] for x in m['files']}==names,'Manifest upload list differs')
 require(type(g['metadata'].get('title')) is str and bool(g['metadata']['title']),'Final exact title absent')
 description=g['metadata'].get('description')
 require(type(description) is str and 'Ferudun' in description and PRIOR_OVERLAP_DOI in description,'Exact overlapping theorem must be credited in final metadata')
 creators=g['metadata'].get('creators',[])
 require(any(x.get('name')=='Kriebel, Alec' and x.get('orcid')=='0009-0001-9320-500X' for x in creators),'Alec ORCID metadata missing')
 other=g.get('other_safe_files');require(isinstance(other,dict) and bool(other),'Final supporting input map absent')
 for rel,wanted in other.items():
  require(rel!='ROOT_PUBLICATION_GATE_01.json' and not any(x.startswith('private_') or x in ('__pycache__','.venv','site-packages') for x in pathlib.PurePosixPath(rel).parts) and not rel.endswith(('.pyc','.pyo')) and 'ACCEPTANCE_CURRENT_SELECTED_MAP' not in rel,'Unsafe supporting input scope')
  p=child(base,rel);regular_pinned_input(p);require(pin(p)==wanted,'Supporting input changed: '+rel);inputs[rel]=p
 for required,pinned in [('ROOT_PRIORITY_EDITORIAL_GATE_01.json',PRIORITY_PIN),('ROOT_ACTUAL_CUSTODY_VERIFICATION_01.json',CUSTODY_PIN)]:
  require(required in inputs and pin(inputs[required])==pinned,'Accepted original custody/priority fact pin absent or changed: '+required)
 for role in ('mathematics','priority','portable','package','visual'):
  ref=g['preparation_receipts'][role];require(set(ref)=={'path','bytes','sha256'} and ref['path'] in inputs and pin(inputs[ref['path']])=={k:ref[k] for k in ('bytes','sha256')},'Root preparation receipt role missing: '+role)
 inputs.update(review_inputs)
 rp=base/'ROOT_ACTUAL_READY_CHECKPOINT.json';sealed(rp);r=read_pinned(rp,approved['ready_pointer_pin'])
 require(r.get('schema')=='pr206-lifecycle-actual-pointer-v1' and r.get('PR')==PR and r.get('phase')=='ready' and r.get('Root_recorded_only_after_actual_full_scope_acceptance') is True,'Actual PR206 ready pointer missing')
 checkpoint=child(base,r['directory']);ap=checkpoint/'ACCEPTANCE.json';sealed(ap);ac=read_pinned(ap,r['acceptance_pin'])
 require(pin(ap)==r['acceptance_pin'] and ac.get('schema')=='pr206-lifecycle-actual-acceptance-v1' and ac.get('PR')==PR and ac.get('original_head')==HEAD and ac.get('case_percent')==90 and ac.get('Root_publication_gate_pin')==pin(gp),'Ready90 acceptance identity/gate mismatch')
 for field in ['accepted','every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','original_native_custody_retained','mathematical_clearance','source_contract_clearance','priority_clearance','publication_ready']:
  require(ac.get(field) is True,'Incomplete actual full-scope acceptance: '+field)
 require(ac.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and ac.get('actual_original_PR_head')==HEAD and ac.get('actual_original_PR_is_draft') is True and ac.get('actual_original_PR_state')=='open','Independent actual90 original draft HEAD/state evidence missing')
 ready_facts(ac,g)
 require(ac.get('historical_firstness_independence_established') is False,'Historical-priority qualification changed')
 require(ac.get('package')==g['package'] and ac.get('package_seal')==g['package_seal'],'Ready90 final package mismatch')
 require(ac['checkpoint_commit']==r['checkpoint_commit'] and ac['main_observed']==r['main_observed'],'Actual ready commit/MAIN mismatch')
 mp=checkpoint/'ACCEPTANCE_CURRENT_SELECTED_MAP.json';sealed(mp);mapped=read_pinned(mp,ac['actual_current_map_file']);selected=mapped['selected_files']
 map_digest=digest(json.dumps(selected,sort_keys=True,separators=(',',':')).encode())
 require(len(selected)==ac['selected_files'] and map_digest==mapped['selected_map_sha256']==ac['actual_current_selected_map_sha256'],'Accepted selected map mismatch')
 ready_verification(base,approved,r,ac,selected,mp,gp)
 for rel,p in inputs.items():require(selected.get(PREFIX+rel)==native_identity(p),'Actual ready map does not bind exact input: '+rel)
 return dict(base=base,gate_path=gp,gate=g,package=package,manifest=manifest,gate_pin=pin(gp),ready_pointer_pin=pin(rp),ready_acceptance_pin=pin(ap),checkpoint_commit=r['checkpoint_commit'],package_seal=g['package_seal'])

def context_pin(context):
 return {k:context[k] for k in ['gate_pin','ready_pointer_pin','ready_acceptance_pin','checkpoint_commit','package_seal']}|{'package':context['gate']['package'],'manifest_pin':pin(context['manifest'])}
def same_context(base,wanted):
 c=load_context(base);require(context_pin(c)==wanted,'Gate/ready/package changed during operation');return c
def publication_receipt(context):
 p=context['base']/'ROOT_PUBLICATION_RECEIPT.json';sealed(p);r=read(p);g=context['gate']
 require(r.get('schema')=='pr206-root-publication-receipt-v1' and r.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT','Publication receipt schema/scope differs')
 for key in ['actual_publication_verified','metadata_exact_verified','all_three_public_download_SHA256_verified']:require(r.get(key) is True,'Publication not actually verified: '+key)
 require(r.get('PR')==PR and r.get('state')=='published' and r.get('gate_sha256')==context['gate_pin']['sha256'] and r.get('package')==g['package'],'Publication not bound to exact gate/package')
 require(r.get('metadata')==g['metadata'] and r.get('package_safe_files')==g['package_safe_files'] and r.get('intended_upload_files')==g['intended_upload_files'] and r.get('original_head')==HEAD and r.get('problem_id')==PROBLEM,'Publication facts lost or changed')
 require(r.get('metadata_normalizations')==[] and len(r.get('verified_public_download_names',[]))==3 and set(r.get('verified_public_download_names',[]))==upload_names(g),'Publication verification incomplete')
 require(r.get('doi_resolution',{}).get('http_status')==200 and r['doi_resolution'].get('status')=='resolved','Actual DOI resolution not verified')
 require(type(r.get('id')) is int and r['id']>0 and r.get('doi')=='10.5281/zenodo.'+str(r['id']) and r.get('doi_url')=='https://doi.org/'+r['doi'],'Missing actual assigned DOI/record ID')
 require(r.get('record_url')=='https://zenodo.org/records/'+str(r['id']),'Publication record URL differs')
 files=r.get('files',[]);require(len(files)==3 and {x['name']:{'bytes':x['size'],'sha256':x['sha256']} for x in files}==g['intended_upload_files'],'Publication files differ from gate')
 require(r.get('context')==context_pin(context),'Publication receipt context mismatch')
 downloads=r.get('public_downloads',[]);require(len(downloads)==3 and {x['name']:{'bytes':x['bytes'],'sha256':x['sha256']} for x in downloads}==g['intended_upload_files'] and all(x['url'].startswith('https://') and x['final_url'].startswith('https://') for x in downloads),'Publication independent download evidence incomplete')
 return p,r
