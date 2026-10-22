"""Offline source controls only: never main(), gh, actual intake or actual212 gate.
Synthetic administrative dictionaries are never written as Root terminal receipts.
"""
from pathlib import Path
import ast,base64,copy,hashlib,json,os,sys,tempfile,types
BASE=Path(__file__).absolute().parent

def run():
 p=BASE/'status_only_intake_after_pr212.py';h=types.ModuleType('intake');h.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),h.__dict__)
 checks=[]
 def yes(value,label):
  if type(value) is not bool or not value:raise RuntimeError(label)
  checks.append(label)
 def no(call,label):
  try:call()
  except (RuntimeError,ValueError,TypeError,KeyError,OSError):checks.append(label)
  else:raise RuntimeError('Expected refusal '+label)
 prior=os.environ.get('GH_HOST');os.environ['GH_HOST']='hostile.invalid'
 try:yes(h.api_argv(213,'pulls/213')==[h.GH,'api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/pulls/213'],'explicit_hostname_ignores_hostile_GH_HOST')
 finally:
  if prior is None:os.environ.pop('GH_HOST',None)
  else:os.environ['GH_HOST']=prior
 for route in ('pulls/214','git/refs/heads/main','pulls/213/merge','https://hostile.invalid','issues/213/comments'):
  no(lambda route=route:h.api_argv(213,route),'unlisted_route_refused_'+route)
 no(lambda:h.api_argv(212,'pulls/212'),'preceding_cursor212_refused')
 no(lambda:h.api_argv(True,'pulls/213'),'boolean_PR_refused')
 no(lambda:h.decode(b'{"a":1,"a":2}'),'duplicate_JSON_refused')
 no(lambda:h.decode(b'{"a":NaN}'),'nonfinite_JSON_refused')
 baseline=json.loads((BASE/'BASELINE_MEMBERSHIP.json').read_bytes())
 yes(h.pin((BASE/'BASELINE_MEMBERSHIP.json').read_bytes())==h.BASELINE_PIN,'frozen53_37_baseline_pin')
 flags=('accepted','administrative_checkpoint_complete','advance_to_next_PR_authorized_now','all_five_local_files_match_actual_checkpoint','full_scope_verified','all_selected_native_bodies_verified','actual_Root_expected_SHA_force_false_ref_update_and_native_readback','original_stable_writer_lock_held_exact','foreign_native_tuples_preserved','coherent_before_after_ref','all53_37_memberships_unchanged','current_PR_open_draft_unmerged','no_PR_or_publication_actions')
 falseflags=('goal_complete','completed_eligible_workflow','publication_workflow_completed','publication_ready','original_eligibility_rewritten_or_erased','numeric_advance_conditional_on_actual_Root_terminal','CAS_or_completion_inferred_from_ancestry','perpetual_or_write_time_Main_equality_claimed')
 proof={'schema':'pr212-root-actual-administrative-skip-verification-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','synthetic_only_not_an_actual_receipt':True,'PR':212,'administrative_checkpoint_percent':100,'fully_completed_count':53,'published_count':37,'last_completed_PR':211,'next_numeric_intake_cursor':213,
  'candidate':'a'*40,'CAS_target':'a'*40,'tree':'b'*40,'CAS_target_tree':'b'*40,'actual_MAIN_observed':'a'*40,'actual_MAIN_tree':'b'*40,
  'selected_postimage_paths_verified':271,'protected_body_paths_verified':0,'native_final_ref_UTC':'2026-10-17T22:00:00Z','terminal_observation_boundary':'Synthetic qualified dated fixture only',
  'original_eligible_status':'claimed_solved','current_corrected_status':'already_solved','disposition':'ADMINISTRATIVE_ADVANCE_CORRECTED_NONCLAIMED_DRAFT_UNTOUCHED',
  **baseline,**dict.fromkeys(flags,True),**dict.fromkeys(falseflags,False)}
 enc=lambda o:(json.dumps(o,sort_keys=True,indent=2)+'\n').encode()
 def verify(value):
  raw=enc(value);return h.completion_proof(raw,h.pin(raw))
 yes(verify(proof)['next_numeric_intake_cursor']==213,'synthetic_actual_admin_terminal53_37_last211_cursor213')
 yes('completed' not in proof and 'actual_original_PR_merged' not in proof,'positive_requires_neither_completed_PR212_nor_merge_true')
 for key in flags:
  bad={**proof,key:1};no(lambda bad=bad:verify(bad),'true_boolean_exact_'+key)
 for key in falseflags:
  bad={**proof,key:0};no(lambda bad=bad:verify(bad),'false_boolean_exact_'+key)
 for key,value in (('PR',True),('administrative_checkpoint_percent',100.0),('fully_completed_count',54),('fully_completed_count',53.0),('published_count',38),('last_completed_PR',212),('next_numeric_intake_cursor',212),('next_numeric_intake_cursor',214),('completed',True),('actual_original_PR_merged',True),('original_PR_already_merged',True),('original_eligible_status','already_solved'),('current_corrected_status','claimed_solved'),('administrative_checkpoint_complete',False),('advance_to_next_PR_authorized_now',False),('numeric_advance_conditional_on_actual_Root_terminal',True)):
  bad={**proof,key:value};no(lambda bad=bad:verify(bad),'administrative_fact_refused_'+key+'_'+str(value))
 for schema in ('pr211-root-actual-completion-verification-v1','pr212-root-conservative-administrative-disposition-v1','pr212-root-administrative-logical-packet-acceptance-v1','pr212-conditional-administrative-logical-packet-v1','pr212-preliminary-terminal'):
  bad={**proof,'schema':schema};no(lambda bad=bad:verify(bad),'nonterminal_schema_refused_'+schema)
 for scope in ('CONDITIONAL_MODEL_NOT_ACTUAL_ACCEPTANCE','SOURCE_PREPARATION_ONLY','PLANNED_ROOT_RECEIPT'):
  bad={**proof,'evidence_scope':scope};no(lambda bad=bad:verify(bad),'nonactual_scope_refused_'+scope)
 for field in ('fully_completed_eligible_PRs','published_PRs'):
  for alteration in ('missing','duplicate','reordered','replaced_by212','float','boolean'):
   bad=copy.deepcopy(proof)
   if alteration=='missing':del bad[field]
   elif alteration=='duplicate':bad[field][-1]=bad[field][-2]
   elif alteration=='reordered':bad[field]=list(reversed(bad[field]))
   elif alteration=='replaced_by212':bad[field][-1]=212
   elif alteration=='float':bad[field][0]=float(bad[field][0])
   else:bad[field][0]=True
   no(lambda bad=bad:verify(bad),'exact_membership_'+field+'_'+alteration)
 raw=enc(proof);no(lambda:h.completion_proof(raw,{'bytes':len(raw),'sha256':'0'*64}),'external_terminal_pin_refused')
 descendant={**proof,'actual_MAIN_observed':'d'*40,'actual_MAIN_tree':'e'*40}
 yes(verify(descendant)['actual_MAIN_observed']!=proof['candidate'],'qualified_actual_C_not_R_terminal_supported')
 for key,value in (('CAS_target','f'*40),('CAS_target_tree','f'*40),('candidate','bad'),('actual_MAIN_tree','bad'),('selected_postimage_paths_verified',True),('selected_postimage_paths_verified',0),('protected_body_paths_verified',0.0),('native_final_ref_UTC',''),('terminal_observation_boundary','')):
  bad={**descendant,key:value};no(lambda bad=bad:verify(bad),'qualified_native_admin_terminal_'+key+'_refused')
 actual211=BASE.parents[1]/'audits/pr211_5100063/ROOT_ACTUAL_COMPLETION_VERIFICATION_01.json'
 oldterminal=h.regular(actual211);yes(h.pin(oldterminal)=={'bytes':9799,'sha256':'8acd4bb99e504f4fe59b9c28a91b8fdcfc5a71502b3b0f54cb98070a29467477'},'old211_actual_terminal_frozen_input_pin')
 no(lambda:h.completion_proof(oldterminal,h.pin(oldterminal)),'actual_old211_completion_cannot_authorize213')
 previous=BASE.parents[1]/'ordered_intakes_after_PR211_20261017/preparation_01/status_only_intake_after_pr211.py'
 oldraw=previous.read_bytes();yes(h.pin(oldraw)=={'bytes':22876,'sha256':'998468a6d21ab9424334dc3ee8352dcdb29967c6e19291e432faddaeaa888675'},'previous_after211_source_unchanged_exact_pin')
 oldast=ast.parse(oldraw);newast=ast.parse(p.read_bytes())
 oldfunc={n.name:ast.dump(n,include_attributes=False) for n in oldast.body if isinstance(n,ast.FunctionDef)}
 newfunc={n.name:ast.dump(n,include_attributes=False) for n in newast.body if isinstance(n,ast.FunctionDef)}
 unchanged=sorted(set(oldfunc)-{'api_argv','completion_proof','main'})
 yes(set(oldfunc)==set(newfunc) and len(unchanged)==17 and all(oldfunc[n]==newfunc[n] for n in unchanged),'all17_status_custody_transport_functions_AST_identical')
 mainfunc=next(n for n in newast.body if isinstance(n,ast.FunctionDef) and n.name=='main')
 source=ast.unparse(mainfunc)
 yes(source.index('completion_proof(')<source.index('preserved_status(')<source.index('current_custody('),'prior_admin_terminal_gate_before_any_original_or_current_request')
 yes("'date_partition_used_for_HEAD_selection': False" in source and "'original_author_turns_and_model_effort_unverified': True" in source and 'firstness or priority is inferred' in source,'timestamps_not_HEAD_selection_first_public_or_author_effort_proof')
 pid='5100099';head='1'*40;newhead='3'*40;parent='2'*40
 def fixture(status):
  cells=['']*14;cells[1]=' synthetic ';cells[2]=' '+pid+' / SYNTHETIC ';cells[8]=' '+status+' ';cells[9]=' 1/5 '
  row=('|'.join(cells)+'\n').encode();body=b'synthetic queue header\n'+row;blob=h.native('blob',body)
  def tree(rows):
   raw=b''.join(mode.lstrip('0').encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid) for name,mode,kind,oid in rows);oid=h.native('tree',raw)
   return oid,{'sha':oid,'truncated':False,'tree':[{'path':n,'mode':m,'type':t,'sha':s} for n,m,t,s in rows]}
  inner,innerv=tree([('QUEUE.md','100644','blob',blob)]);root,rootv=tree([('unsolved_math_prioritization','040000','tree',inner)])
  dated={'state':'OPEN','isDraft':True,'headRefOid':head,'headRefName':'dot/math-'+pid,'status_projection':{'target_ambiguity':False,'git_blob_oid':blob,'whole_QUEUE_bytes':len(body),'whole_QUEUE_sha256':h.pin(body)['sha256'],'targets':[{'problem_id':pid,'code':cells[2].strip(),'status':status,'turns':'1/5','selected_row_sha256':hashlib.sha256(row[:-1]).hexdigest()}]}}
  objects={'git/commits/'+head:{'sha':head,'tree':{'sha':root},'parents':[{'sha':parent}]},'git/trees/'+root:rootv,'git/trees/'+inner:innerv,'git/blobs/'+blob:{'sha':blob,'encoding':'base64','size':len(body),'content':base64.b64encode(body).decode()}};requests=[]
  def fetch(route):requests.append(route);return copy.deepcopy(objects[route])
  return dated,objects,requests,fetch
 dated,objects,requests,fetch=fixture('already_solved');skipped=h.preserved_status(dated,fetch)
 yes(not skipped['eligible'] and skipped['status']=='already_solved' and all(r.startswith('git/') for r in requests),'nonclaimed_status_authenticated_without_PR_history_or_math')
 for status in ('unsolved','solved','Claimed_solved'):
  dated,objects,requests,fetch=fixture(status);skipped=h.preserved_status(dated,fetch)
  yes(not skipped['eligible'] and all(r.startswith('git/') for r in requests),'exact_nonclaimed_skip_'+status)
 dated,objects,requests,fetch=fixture('claimed_solved');original=h.preserved_status(dated,fetch);yes(original['eligible'],'exact_claimed_solved_status_only_eligible')
 bad_dated=copy.deepcopy(dated);bad_dated['status_projection']['targets'].append(copy.deepcopy(bad_dated['status_projection']['targets'][0]))
 no(lambda:h.preserved_status(bad_dated,fetch),'ambiguous_native_target_refused_before_current_PR')

 bad_dated=copy.deepcopy(dated);bad_dated['status_projection']['targets'][0]['turns']='2/5';no(lambda:h.preserved_status(bad_dated,fetch),'preserved_effort_change_refused')
 original_pr={'number':213,'head':{'sha':head,'ref':dated['headRefName']},'title':pid+': synthetic target','state':'open','draft':True,'merged':False,'commits':1,'created_at':'synthetic','updated_at':'synthetic','merge_commit_sha':None,'merged_at':None,'body':'opaque metadata only'}
 history={'pulls/213/commits?page=1&per_page=100':[{'sha':head,'parents':[{'sha':parent}]}],'issues/213/timeline?page=1&per_page=100':[{'event':'committed','sha':head}]}
 def current_fetch(route):
  if route=='pulls/213':return copy.deepcopy(original_pr)
  if route.startswith('compare/'):return {'status':'ahead','merge_base_commit':{'sha':head}}
  return copy.deepcopy(history[route])
 before,custody=h.current_custody(213,dated,original,None,current_fetch);yes(custody['unchanged_linear_and_timeline_checks_passed'],'unchanged_open_strong_linear_timeline_positive')
 history['issues/213/timeline?page=1&per_page=100'].append({'event':'head_ref_force_pushed'});no(lambda:h.current_custody(213,dated,original,None,current_fetch),'unchanged_open_forcepush_refused');history['issues/213/timeline?page=1&per_page=100'].pop()
 original_pr['head']['sha']=newhead;history['pulls/213/commits?page=1&per_page=100']=[{'sha':newhead,'parents':[{'sha':head},{'sha':parent}]}]
 no(lambda:h.current_custody(213,dated,original,None,current_fetch),'changed_HEAD_requires_explicit_extension')
 before,custody=h.current_custody(213,dated,original,newhead,current_fetch);yes(custody['mode']=='explicit_descendant_status_custody' and custody['full_changed_head_artifact_custody_required_before_math'],'explicit_changed_HEAD_is_custody_only')
 original_pr.update(state='closed',merged=True,draft=False,merge_commit_sha='4'*40,merged_at='synthetic actual metadata fixture')
 no(lambda:h.current_custody(213,dated,original,None,current_fetch),'already_merged_requires_explicit_extension')
 before,custody=h.current_custody(213,dated,original,newhead,current_fetch);yes(custody['already_merged'] and custody['full_changed_head_artifact_custody_required_before_math'],'explicit_already_merged_descendant_supported_without_PR_effect')
 no(lambda:h.current_custody(213,dated,original,'0'*40,current_fetch),'explicit_HEAD_mismatch_refused')
 def wrong_ancestry(route):return {'status':'diverged','merge_base_commit':{'sha':'0'*40}} if route.startswith('compare/') else current_fetch(route)
 no(lambda:h.current_custody(213,dated,original,newhead,wrong_ancestry),'changed_HEAD_nonancestor_refused')
 h.fresh_pr(213,dated,before,current_fetch);yes(True,'fresh_unchanged_metadata_positive')
 original_pr['updated_at']='changed';no(lambda:h.fresh_pr(213,dated,before,current_fetch),'fresh_metadata_change_refused')
 with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=BASE) as tmp:
  f=Path(tmp)/'registry.json';f.write_bytes(b'synthetic');f.chmod(0o644);yes(h.regular(f,False)==b'synthetic','existing644_registry_readonly_pin_compatible');no(lambda:h.regular(f),'immutable_receipt_requires444')

 # Additional malformed original immutable metadata stays fail-closed.
 for mode in ('commit_sha','two_parents','truncated_tree','wrong_blob_size','wrong_blob_sha'):
  bad_dated,bad_objects,bad_requests,bad_fetch=fixture('claimed_solved')
  if mode=='commit_sha':bad_objects['git/commits/'+head]['sha']='0'*40
  elif mode=='two_parents':bad_objects['git/commits/'+head]['parents'].append({'sha':'5'*40})
  elif mode=='truncated_tree':
   route=next(r for r in bad_objects if r.startswith('git/trees/'));bad_objects[route]['truncated']=True
  else:
   route=next(r for r in bad_objects if r.startswith('git/blobs/'))
   if mode=='wrong_blob_size':bad_objects[route]['size']+=1
   else:bad_objects[route]['sha']='0'*40
  h.TREES.clear();no(lambda:h.preserved_status(bad_dated,bad_fetch),'malformed_original_native_'+mode)
 # Metadata dates are compared opaquely; they never choose original HEAD or assert first-public time.
 original_pr['updated_at']='opaque timestamp';before=copy.deepcopy(original_pr);h.fresh_pr(213,dated,before,current_fetch)
 yes(before['head']['sha']==newhead and original['head']==head,'metadata_dates_do_not_reselect_original_HEAD')
 original_pr['head']['sha']='not_native_oid';no(lambda:h.current_custody(213,dated,original,newhead,current_fetch),'malformed_current_HEAD_refused')
 with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=BASE) as tmp:
  f=Path(tmp)/'ordinary';f.write_bytes(b'synthetic');f.chmod(0o444)
  link=Path(tmp)/'symlink';link.symlink_to(f);no(lambda:h.regular(link),'symlink_receipt_refused')
 output=h.bounded_get([sys.executable,'-E','-S','-B','-P','-c','print("synthetic")']);yes(output.stdout==b'synthetic\n' and output.returncode==0,'bounded_transport_owned_child_positive_no_provider')
 no(lambda:h.bounded_get([sys.executable,'-E','-S','-B','-P','-c','import os; os.write(2,b"x"*100000)']),'bounded_stderr_overflow_stops_and_reaps_owned_child')
 return {'schema':'after212-inactive-intake-source-controls-v1','status':'PASS','checks':checks,'check_count':len(checks),'source_pin':h.pin(p.read_bytes()),'main_or_intake_executions':0,'provider_calls':0,'actual212_terminal_or_Root_gate_created':False,'actual213_or_native_requests':0,'current_views_locks_native_PRs_or_shared_files_modified':False,'native_observers_synthetic_only':True,'old_actual211_terminal_rejected_as_pinned_data_only':True,'unchanged_inherited_function_count':len(unchanged)}
if __name__=='__main__':
 if not(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Use python3 -E -S -B -P')
 print(json.dumps(run(),sort_keys=True,indent=2))

