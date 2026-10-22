"""Inactive after214 semantic controls: pure parser and synthetic observers only.
Never main(), gh, actual intake, actual terminal publication or production effect.
Published synthetic producer integration is recorded separately, not fabricated here.
"""
from pathlib import Path
import ast,base64,copy,hashlib,json,os,sys,tempfile,types
BASE=Path(__file__).absolute().parent
def run():
 p=BASE/'status_only_intake_after_pr214.py';h=types.ModuleType('intake');h.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),h.__dict__)
 checks=[]
 def yes(value,label):
  if type(value)is not bool or not value:raise RuntimeError(label)
  checks.append(label)
 def no(call,label):
  try:call()
  except (RuntimeError,ValueError,TypeError,KeyError,OSError):checks.append(label)
  else:raise RuntimeError('Expected refusal '+label)
 prior=os.environ.get('GH_HOST');os.environ['GH_HOST']='hostile.invalid'
 try:yes(h.api_argv(215,'pulls/215')==[h.GH,'api','--hostname','github.com','--method','GET','repos/AlecKriebel/Math/pulls/215'],'explicit_hostname_ignores_hostile_GH_HOST')
 finally:
  if prior is None:os.environ.pop('GH_HOST',None)
  else:os.environ['GH_HOST']=prior
 for route in ('pulls/216','git/refs/heads/main','pulls/215/merge','https://hostile.invalid','issues/215/comments'):
  no(lambda route=route:h.api_argv(215,route),'unlisted_route_'+route)
 for pr in (True,214,10001):no(lambda pr=pr:h.api_argv(pr,'pulls/'+str(pr)),'strict_PR_bounds_'+str(pr))
 yes(h.api_argv(10000,'pulls/10000')[5]=='GET','fixed_max10000_retained')
 no(lambda:h.decode(b'{"a":1,"a":2}'),'duplicate_JSON_refused')
 no(lambda:h.decode(b'{"a":NaN}'),'nonfinite_JSON_refused')
 no(lambda:h.decode(b'{"a":1e9999}'),'overflow_JSON_refused')
 baseline=json.loads((BASE/'BASELINE_MEMBERSHIP.json').read_bytes());yes(h.pin((BASE/'BASELINE_MEMBERSHIP.json').read_bytes())==h.BASELINE_PIN,'exact_accepted853B_baseline53_37')
 flags=["accepted","completed","completed_eligible_workflow","publication_workflow_completed","publication_ready","advance_to_next_PR_authorized_now","actual_original_PR_merged","adopted_existing_publication","no_new_provider_publication_or_tracker_append","all_five_local_files_match_actual_checkpoint","full_scope_verified","all_selected_native_bodies_verified","actual_Root_expected_SHA_force_false_ref_update_and_native_readback","original_stable_writer_lock_held_exact","foreign_native_tuples_preserved","coherent_before_after_ref","source_gates_verified"]
 falseflags=["goal_complete","numeric_advance_conditional_on_actual_Root_terminal","CAS_or_completion_inferred_from_ancestry","perpetual_or_write_time_Main_equality_claimed"]
 proof={'schema':'pr214-root-actual-completion-verification-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','synthetic_parser_fixture_only_not_operational_authority':True,'PR':214,'workflow_percent':100,'fully_completed_count':54,'published_count':38,'last_completed_PR':214,'next_numeric_intake_cursor':215,
  'original_eligible_status':'claimed_solved','current_status':'claimed_solved','current_head':'95ba37055ebf1e7b4f9d76aa43816c9978c7bce8','original_merge_commit':'4abf30daa991860a275b3d25745159852757ad35','existing_publication_DOI':'10.5281/zenodo.23390551','existing_tracker_range':"'Math Puzzles'!A105:D105",
  'fully_completed_eligible_PRs':baseline['fully_completed_eligible_PRs']+[214],'published_PRs':baseline['published_PRs']+[214],
  'candidate':'a'*40,'CAS_target':'a'*40,'tree':'b'*40,'CAS_target_tree':'b'*40,'actual_MAIN_observed':'a'*40,'actual_MAIN_tree':'b'*40,'selected_postimage_paths_verified':200,'protected_body_paths_verified':0,'native_final_ref_UTC':'2026-10-17T23:00:00Z','terminal_observation_boundary':'Synthetic parser fixture only',
  **dict.fromkeys(flags,True),**dict.fromkeys(falseflags,False)}
 enc=lambda v:(json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
 def verify(v):
  r=enc(v);return h.completion_proof(r,h.pin(r))
 yes(verify(proof)['next_numeric_intake_cursor']==215,'synthetic_parser54_38_last214_cursor215')
 for key in flags:
  for value in (False,1,None):
   bad={**proof,key:value};no(lambda bad=bad:verify(bad),'true_exact_'+key+'_'+str(value))
 for key in falseflags:
  for value in (True,0,None):
   bad={**proof,key:value};no(lambda bad=bad:verify(bad),'false_exact_'+key+'_'+str(value))
 for key,value in (('PR',True),('workflow_percent',100.0),('fully_completed_count',53),('fully_completed_count',54.0),('published_count',37),('last_completed_PR',211),('next_numeric_intake_cursor',214),('next_numeric_intake_cursor',216),('original_eligible_status','already_solved'),('current_status','already_solved'),('current_head','0'*40),('original_merge_commit','0'*40),('existing_publication_DOI','10.5281/zenodo.0'),('existing_tracker_range',"'Math Puzzles'!A106:D106")):
  bad={**proof,key:value};no(lambda bad=bad:verify(bad),'fixed_fact_refused_'+key+'_'+str(value))
 for schema in ('pr212-root-actual-administrative-skip-verification-v1','pr211-root-actual-completion-verification-v1','pr214-root-completion-model-acceptance-v1','pr214-source-only-preparation-v1'):
  bad={**proof,'schema':schema};no(lambda bad=bad:verify(bad),'source_or_old_terminal_schema_'+schema)
 for scope in ('PLANNED_ROOT_RECEIPT','SOURCE_PREPARATION_ONLY','CONDITIONAL_MODEL_NOT_ACTUAL_ACCEPTANCE'):
  bad={**proof,'evidence_scope':scope};no(lambda bad=bad:verify(bad),'nonactual_scope_'+scope)
 for key in ('fully_completed_eligible_PRs','published_PRs'):
  for mode in ('old_baseline','add212','add213','replace211','duplicate214','reverse','float','bool','missing'):
   bad=copy.deepcopy(proof)
   if mode=='old_baseline':bad[key]=baseline[key]
   elif mode=='add212':bad[key][-1]=212
   elif mode=='add213':bad[key][-1]=213
   elif mode=='replace211':bad[key][-2]=212
   elif mode=='duplicate214':bad[key].append(214)
   elif mode=='reverse':bad[key].reverse()
   elif mode=='float':bad[key][0]=float(bad[key][0])
   elif mode=='bool':bad[key][0]=True
   else:del bad[key]
   no(lambda bad=bad:verify(bad),'memberships_only214_'+key+'_'+mode)
 raw=enc(proof);no(lambda:h.completion_proof(raw,{'bytes':len(raw),'sha256':'0'*64}),'external_exact_terminal_pin')
 descendant={**proof,'actual_MAIN_observed':'d'*40,'actual_MAIN_tree':'e'*40}
 yes(verify(descendant)['actual_MAIN_observed']!=proof['candidate'],'qualified_actual_C_not_R_supported')
 for key,value in (('CAS_target','f'*40),('CAS_target_tree','f'*40),('candidate','bad'),('actual_MAIN_tree','bad'),('selected_postimage_paths_verified',True),('selected_postimage_paths_verified',0),('protected_body_paths_verified',0.0),('native_final_ref_UTC',''),('terminal_observation_boundary','')):
  bad={**descendant,key:value};no(lambda bad=bad:verify(bad),'native_C_R_boundary_'+key)
 old=BASE.parents[1]/'ordered_intakes_after_PR212_20261017/preparation_01/status_only_intake_after_pr212.py';oldraw=old.read_bytes()
 yes(h.pin(oldraw)=={'bytes':24760,'sha256':'0292388c3722d04cb2c11108d409c14759b61a370b0478fbbef41c92e19349eb'},'exact_accepted_after212_source')
 oldast=ast.parse(oldraw);newast=ast.parse(p.read_bytes());f=lambda t:{n.name:ast.dump(n,include_attributes=False)for n in t.body if isinstance(n,ast.FunctionDef)};x,y=f(oldast),f(newast)
 unchanged=sorted(set(x)-{'api_argv','completion_proof','main'});yes(set(x)==set(y) and len(unchanged)==17 and all(x[n]==y[n]for n in unchanged),'all17_inherited_status_custody_transport_functions_AST_identical')
 source=ast.unparse(next(n for n in newast.body if isinstance(n,ast.FunctionDef)and n.name=='main'))
 yes(source.index('completion_proof(')<source.index('preserved_status(')<source.index('current_custody('),'actual_prior_gate_before_original_QUEUE_before_current_metadata')
 yes('range(215, num)'in source and 'if num == 215:'in source and "'prior_actual_completion_terminal_pin'"in source and "'previous_skip_pin'"in source and "'STATUS_ONLY_SKIP_UNTOUCHED'"in source,'first215_no_predecessor_and_complete_contiguous_skip_chain')
 yes("'date_partition_used_for_HEAD_selection': False"in source and "'original_author_turns_and_model_effort_unverified': True"in source and 'firstness or priority is inferred'in source,'no_date_author_turn_priority_or_opening_transaction_inference')
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
 original_pr={'number':215,'head':{'sha':head,'ref':dated['headRefName']},'title':pid+': synthetic target','state':'open','draft':True,'merged':False,'commits':1,'created_at':'synthetic','updated_at':'synthetic','merge_commit_sha':None,'merged_at':None,'body':'opaque metadata only'}
 history={'pulls/215/commits?page=1&per_page=100':[{'sha':head,'parents':[{'sha':parent}]}],'issues/215/timeline?page=1&per_page=100':[{'event':'committed','sha':head}]}
 def current_fetch(route):
  if route=='pulls/215':return copy.deepcopy(original_pr)
  if route.startswith('compare/'):return {'status':'ahead','merge_base_commit':{'sha':head}}
  return copy.deepcopy(history[route])
 before,custody=h.current_custody(215,dated,original,None,current_fetch);yes(custody['unchanged_linear_and_timeline_checks_passed'],'unchanged_open_strong_linear_timeline_positive')
 history['issues/215/timeline?page=1&per_page=100'].append({'event':'head_ref_force_pushed'});no(lambda:h.current_custody(215,dated,original,None,current_fetch),'unchanged_open_forcepush_refused');history['issues/215/timeline?page=1&per_page=100'].pop()
 original_pr['head']['sha']=newhead;history['pulls/215/commits?page=1&per_page=100']=[{'sha':newhead,'parents':[{'sha':head},{'sha':parent}]}]
 no(lambda:h.current_custody(215,dated,original,None,current_fetch),'changed_HEAD_requires_explicit_extension')
 before,custody=h.current_custody(215,dated,original,newhead,current_fetch);yes(custody['mode']=='explicit_descendant_status_custody' and custody['full_changed_head_artifact_custody_required_before_math'],'explicit_changed_HEAD_is_custody_only')
 original_pr.update(state='closed',merged=True,draft=False,merge_commit_sha='4'*40,merged_at='synthetic actual metadata fixture')
 no(lambda:h.current_custody(215,dated,original,None,current_fetch),'already_merged_requires_explicit_extension')
 before,custody=h.current_custody(215,dated,original,newhead,current_fetch);yes(custody['already_merged'] and custody['full_changed_head_artifact_custody_required_before_math'],'explicit_already_merged_descendant_supported_without_PR_effect')
 no(lambda:h.current_custody(215,dated,original,'0'*40,current_fetch),'explicit_HEAD_mismatch_refused')
 def wrong_ancestry(route):return {'status':'diverged','merge_base_commit':{'sha':'0'*40}} if route.startswith('compare/') else current_fetch(route)
 no(lambda:h.current_custody(215,dated,original,newhead,wrong_ancestry),'changed_HEAD_nonancestor_refused')
 h.fresh_pr(215,dated,before,current_fetch);yes(True,'fresh_unchanged_metadata_positive')
 original_pr['updated_at']='changed';no(lambda:h.fresh_pr(215,dated,before,current_fetch),'fresh_metadata_change_refused')
 with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=BASE) as tmp:
  f=Path(tmp)/'registry.json';f.write_bytes(b'synthetic');f.chmod(0o644);yes(h.regular(f,False)==b'synthetic','existing644_registry_readonly_pin_compatible');no(lambda:h.regular(f),'immutable_receipt_requires444')


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
  h.TREES.clear();no(lambda:h.preserved_status(bad_dated,bad_fetch),'malformed_original_'+mode)
 original_pr['updated_at']='opaque date';before=copy.deepcopy(original_pr);h.fresh_pr(215,dated,before,current_fetch)
 yes(before['head']['sha']==newhead and original['head']==head,'timestamps_do_not_reselect_original_HEAD')
 original_pr['head']['sha']='not_native_oid';no(lambda:h.current_custody(215,dated,original,newhead,current_fetch),'malformed_current_HEAD')
 with tempfile.TemporaryDirectory(prefix='_synthetic_',dir=BASE)as tmp:
  p0=Path(tmp)/'ordinary';p0.write_bytes(b'synthetic');p0.chmod(0o444);symlink=Path(tmp)/'symlink';symlink.symlink_to(p0);no(lambda:h.regular(symlink),'symlink_immutable_input')
 out=h.bounded_get([sys.executable,'-E','-S','-B','-P','-c','print("synthetic")']);yes(out.stdout==b'synthetic\n' and out.returncode==0,'harmless_owned_bounded_transport_child')
 no(lambda:h.bounded_get([sys.executable,'-E','-S','-B','-P','-c','import os;os.write(2,b"x"*100000)']),'bounded_stderr_overflow_reaps_owned_child')
 return {'schema':'after214-inactive-consumer-semantic-controls-v1','status':'PASS','check_count':len(checks),'checks':checks,'source_pin':h.pin((BASE/'status_only_intake_after_pr214.py').read_bytes()),'unchanged_inherited_functions':17,'main_or_actual_intake_executions':0,'live_native_or_provider_calls':0,'actual_Root_gate_or_receipt_created':False,'Goal_API_status_modified':False,'scientific_or_next_cursor_authority_inferred':False,'generated_published_producer_integration':'Required separate receipt; not inferred from these parser fixtures'}
if __name__=='__main__':
 if not(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Use -E -S -B -P')
 print(json.dumps(run(),sort_keys=True,indent=2))

