from pathlib import Path
D=Path(__file__).resolve().parent
p=D/'offline_guards.py'
s=p.read_text()
a=s.index('def run():')
controls="""def proof_reapprove(f):
 write(f.base/'ROOT_ACTUAL_READY_VERIFICATION_01.json',f.verification)
 f.adoption['approved_actual_ready_verification_pin']=c.pin(f.base/'ROOT_ACTUAL_READY_VERIFICATION_01.json');f.write_adoption()
def addendum_reapprove(f,value):
 write(f.addendum_path,value);f.adoption['approved_operations_contract_addendum_pin']=c.pin(f.addendum_path)
 write(f.adoption_path,f.adoption);c.configure_authority(f.adoption_path.name,c.pin(f.adoption_path))
def rejects_before_transport(f,expected,name):
 pub,k,h=publisher(f)
 try:pub.invoke('stage')
 except (RuntimeError,KeyError,FileNotFoundError,TypeError,ValueError) as error:
  check(expected in str(error),name+' rejects at intended guard: '+expected)
 else:raise RuntimeError('False acceptance: '+name)
 check(not k.calls and not h.calls and not (f.base/'private_operations').exists(),name+' no transport or mutation marker')

def compatibility_controls():
 with fixture() as f:
  absent=('QUEUE_native_original_PR_unchanged','bounded_priority_audit_complete','qualified_attributed_note_editorially_cleared')
  check(all(n not in f.acceptance for n in absent),'actual lifecycle layout excludes mythical and nonaliased editorial top-level fields')
  check(f.acceptance['facts']['bounded_priority_audit_complete'] is True and f.acceptance['facts']['qualified_attributed_note_editorially_cleared'] is True,'actual nested editorial qualifications present')
  context=f.context()
  check(set(c.context_pin(context))=={'gate_pin','ready_pointer_pin','ready_acceptance_pin','checkpoint_commit','package_seal','package','manifest_pin'},'seven-field downstream context unchanged')
  check(context['ready_acceptance_pin']==c.pin(f.checkpoint/'ACCEPTANCE.json'),'real emitted missing-flag receipt layout passes with exact independent synthetic proof')
 # Authority-independent corruptions must reject before reading untrusted JSON.
 for field in ('approved_actual_ready_verification_pin','approved_operations_contract_addendum_pin','dispatcher_pin'):
  with fixture() as f:
   f.adoption.pop(field);f.write_adoption()
   rejects_before_transport(f,'pin absent','missing mandatory '+field)
 with fixture() as f:
  (f.base/'ROOT_ACTUAL_READY_VERIFICATION_01.json').unlink()
  rejects_before_transport(f,'Missing/nonsealed file','missing independent Root proof')
 with fixture() as f:
  f.verification['accepted']=False;write(f.base/'ROOT_ACTUAL_READY_VERIFICATION_01.json',f.verification)
  rejects_before_transport(f,'Pinned JSON bytes changed','unapproved substituted proof under unchanged adoption')
 with fixture() as f:
  write(f.addendum_path,c.read(f.addendum_path)|{'accepted':False})
  rejects_before_transport(f,'Pinned JSON bytes changed','unapproved substituted addendum under unchanged adoption')
 with fixture() as f:
  f.adoption['approved_actual_ready_verification_pin']['sha256']='0'*64;f.write_adoption()
  rejects_before_transport(f,'Pinned JSON bytes changed','adopted rehash does not match proof bytes')
 proof_cases=[('schema','wrong','identity/scope'),('evidence_scope','LOCAL_AUTHOR_PREPARATION','identity/scope'),('PR',205,'identity/scope')]
 proof_cases += [(name,False,'flag missing: '+name) for name in ('accepted','actual_ready90_fully_accepted_synced_and_pointer_verified','ready_candidate_changed_paths_exclude_QUEUE_and_all_native_attempts','original_native_custody_retained','every_selected_identity_checked_at_actual_observed_MAIN','all_overlay_body_identities_verified','full_foreign_tree_scope_preserved','all_three_actual_steps_and_six_alias_cleanups_verified')]
 proof_cases += [(name,True,'unsupported action: '+name) for name in ('actual_original_PR_merged','actual_publication','actual_tracker','advance')]
 proof_cases += [(name,value,'counters/phase differ: '+name) for name,value in [('completed_count',49),('published_count',33),('cursor',207),('case_completion_estimate_percent',100)]]
 proof_cases += [(name,dict(bytes=1,sha256='0'*64),'pointer/acceptance/map/gate cross-binding') for name in ('actual_ready_pointer_pin','actual_acceptance_pin','actual_selected_map_file_pin','actual_publication_gate_pin')]
 proof_cases += [(name,'0'*40,'checkpoint/MAIN') for name in ('checkpoint_commit','actual_main_observed')]
 proof_cases += [('selected_files',True,'selected-map count/digest'),('actual_selected_map_sha256','0'*64,'selected-map count/digest'),('ready_candidate_changed_path_count',True,'changed-path count'),('ready_candidate_changed_path_count',0,'changed-path count'),('actual_original_PR_head','0'*40,'original PR differs'),('actual_original_PR_is_draft',False,'original PR differs'),('actual_original_PR_state','closed','original PR differs')]
 for field,value,expected in proof_cases:
  with fixture() as f:
   f.verification[field]=value;proof_reapprove(f)
   rejects_before_transport(f,expected,'rehash/reapprove semantically false proof '+field)
 for mode in ('missing','extra','duplicate','wrong mode','nonregular','wrong identity','boolean bytes','identity extra'):
  with fixture() as f:
   records=f.verification['all_five_local_readonly_native_postimages']
   if mode=='missing':records.pop()
   elif mode=='extra':records.append(copy.deepcopy(records[0]))
   elif mode=='duplicate':records[-1]=copy.deepcopy(records[0])
   elif mode=='wrong mode':records[0]['mode']='0o644'
   elif mode=='nonregular':records[0]['regular']=1
   elif mode=='wrong identity':records[0]['identity']['sha256']='0'*64
   elif mode=='boolean bytes':records[0]['identity']['bytes']=True
   else:records[0]['identity']['unapproved']=True
   proof_reapprove(f)
   rejects_before_transport(f,'native postimage','five-view '+mode)
 for name,value,expected in [('original_native_custody_retained',False,'Incomplete actual full-scope acceptance'),('original_native_custody_retained',None,'Incomplete actual full-scope acceptance'),('actual_original_PR_head','0'*40,'original draft HEAD/state'),('actual_original_PR_is_draft',False,'original draft HEAD/state'),('actual_original_PR_state','closed','original draft HEAD/state')]:
  with fixture() as f:
   if value is None:f.acceptance.pop(name)
   else:f.acceptance[name]=value
   f.write_acceptance();rejects_before_transport(f,expected,'actual schema custody/originalPR '+name+str(value))
 for field,value,expected in [('bounded_priority_audit_complete',False,'facts not accepted'),('qualified_attributed_note_editorially_cleared',False,'facts not accepted'),('priority_clearance_scope','novelty','qualified-priority scope'),('priority_novelty_clearance',True,'Unsupported actual ready fact'),('fully_completed_count',True,'counters/phase'),('NEW_whole_package_reviews_completed',1,'review count')]:
  with fixture() as f:
   f.facts[field]=value;f.write_acceptance()
   rejects_before_transport(f,expected,'nested actual ready fact '+field)
 for field,value,expected in [('schema','wrong','identity/scope'),('evidence_scope','LOCAL_AUTHOR_PREPARATION','identity/scope'),('PR',205,'identity/scope'),('accepted',False,'identity/scope'),('original_head','0'*40,'identity/scope'),('publication_gate_pin',dict(bytes=1,sha256='0'*64),'gate/ready/proof'),('actual_ready_pointer_pin',dict(bytes=1,sha256='0'*64),'gate/ready/proof'),('actual_ready_verification_pin',dict(bytes=1,sha256='0'*64),'gate/ready/proof'),('source_family','publication_operations_preparation_01','source/dispatcher'),('sources',{},'source/dispatcher'),('dispatcher_pin',dict(bytes=1,sha256='0'*64),'source/dispatcher')]:
  with fixture() as f:
   addendum=c.read(f.addendum_path);addendum[field]=value;addendum_reapprove(f,addendum)
   rejects_before_transport(f,expected,'rehashed unqualified addendum '+field)
 for field in ('scientific_package_metadata_uploads_unchanged','prior_native_selected_original07_files_preserved','operations_sources_approved_after_original_ready_checkpoint','not_a_new_scientific_or_priority_clearance','no_advance_or_completion_granted','executed_current_sources_claimed_present_in_original_ready_map'):
  with fixture() as f:
   addendum=c.read(f.addendum_path);addendum[field]=not addendum[field];addendum_reapprove(f,addendum)
   rejects_before_transport(f,'qualifier missing' if field!='executed_current_sources_claimed_present_in_original_ready_map' else 'must not be claimed','postready scope '+field)
 with fixture() as f:
  oldproof=copy.deepcopy(f.verification);f.acceptance['main_observed']='e'*40;f.pointer['main_observed']='e'*40;f.write_acceptance()
  f.verification=oldproof;proof_reapprove(f)
  rejects_before_transport(f,'pointer/acceptance/map/gate cross-binding','old proof reapproved against fresh different ready pointer')
 with fixture() as f:
  # Replacing all proof contents and internal digests grants nothing under the old adoption.
  original=c.pin(f.adoption_path);f.verification['checkpoint_commit']='f'*40
  write(f.base/'ROOT_ACTUAL_READY_VERIFICATION_01.json',f.verification)
  check(c.pin(f.adoption_path)==original,'fully substituted proof leaves external adoption fixed')
  rejects_before_transport(f,'Pinned JSON bytes changed','fully rehashed independent proof substitution')

"""
s=s[:a]+controls+s[a:]
s=s.replace("def run():\n # Every", "def run():\n compatibility_controls()\n # Every")
p.write_text(s)
