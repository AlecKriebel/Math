"""Owned pure changed-case controls; never live transport, Runtime, Seed or project lock."""
import ast,copy,hashlib,json,types,sys,re
from pathlib import Path
BASE=Path(__file__).absolute().parent
def module(name,file):
 m=types.ModuleType(name);m.__file__=str(BASE/file)
 exec(compile((BASE/file).read_bytes(),m.__file__,'exec'),m.__dict__);return m
def enc(o):return (json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def main():
 h=module('controlled239','native239_model.py');q=module('controlled_driver239','completion_checkpoint.py')
 t=module('controlled_terminal239','ROOT_TERMINAL_INSPECTION.py');u=module('controlled_consumer239','completion_consumer.py')
 results=[]
 def yes(name,fn):
  value=fn();h.need(value is not False,name);results.append({'name':name,'result':'PASS'})
 def no(name,fn):
  try:fn()
  except (RuntimeError,KeyError,ValueError,TypeError,IndexError):results.append({'name':name,'result':'EXPECTED_REFUSAL'});return
  raise RuntimeError('Unexpected acceptance: '+name)
 # Exact historical memberships and independent phase semantics.
 yes('baseline55/39',lambda:len(h.source_baseline()['fully_completed_eligible_PRs'])==55 and len(h.source_baseline()['published_PRs'])==39)
 for phase,count,pub,last,cursor in [('merge95',55,39,218,239),('completion100',56,40,239,240)]:
  f=h.phase_facts(phase)
  yes(phase+' counter facts',lambda f=f,count=count,pub=pub,last=last,cursor=cursor:f['fully_completed_count']==count and f['published_count']==pub and f['last_completed_PR']==last and f['next_numeric_intake_cursor']==cursor)
  yes(phase+' has no actual advance',lambda f=f:f['advance_to_next_PR_authorized_now'] is False and f['numeric_advance_conditional_on_actual_Root_terminal'] is True and f['goal_complete'] is False)
 yes('skipped219..238 never memberships',lambda:all(n not in h.completion_memberships()['fully_completed_eligible_PRs'] for n in range(219,239)))
 yes('only239 added',lambda:all(h.completion_memberships()[k]==v+[239] for k,v in h.source_baseline().items()))
 yes('strict nested types',lambda:not h.exact({'n':[239]},{'n':[239.0]}))
 no('old/adoption phase',lambda:h.phase_facts('adoption100'))
 ident={'name':'Alec Kriebel','email':'me@aleckriebel.com','date':'2026-10-18T03:00:00Z'}
 for phase in ('merge95','completion100'):
  m={'phase':phase,'commit_author':ident,'commit_committer':ident,'commit_message':h.commit_message(phase)}
  parents=h.commit_parents(m,'1'*40);req,oid=h.commit_request(m,'2'*40,parents)
  yes(phase+' ordered parents',lambda parents=parents,phase=phase:parents==(['1'*40,h.CURRENT] if phase=='merge95' else ['1'*40]))
  no(phase+' wrong parent count',lambda m=m,parents=parents:h.commit_request(m,'2'*40,parents[:1] if phase=='merge95' else parents+[h.CURRENT]))
  no(phase+' H first parent',lambda m=m:h.commit_request(m,'2'*40,[h.CURRENT]))
  for bad in ('Closes #239\n','Fixes https://github.com/AlecKriebel/Math/pull/239\n','Resolves #239\n'):
   no(phase+' no auto-close '+bad.split()[0],lambda m=m,bad=bad:h.commit_request({**m,'commit_message':bad},'2'*40,parents))
  yes(phase+' exact readback',lambda m=m:h.commit_message_readback(m['commit_message'],m['commit_message']) is not None)
  yes(phase+' exactly1LF normalized',lambda m=m:h.commit_message_readback(m['commit_message'],m['commit_message'][:-1]) is not None)
  no(phase+' whitespace mutation',lambda m=m:h.commit_message_readback(m['commit_message'],m['commit_message'][:-1]+' '))
  no(phase+' empty parents',lambda m=m:h.commit_request(m,'2'*40,[]))
 # Exact admission validation executes without constructing operational Seed/Runtime.
 for phase in ('merge95','completion100'):
  logical={'phase':phase,'commit_message':h.commit_message(phase),'commit_author':{k:ident[k] for k in ('name','email')},
   'commit_committer':{k:ident[k] for k in ('name','email')},'retired_candidates':[]}
  seed=types.SimpleNamespace(h=h,logical=logical,source_pin=h.pin(b'source'),source_manifest_pin=h.pin(b'sm'),
   manifest_pin=h.pin(b'm'),logical_gate_pin=h.pin(b'g'))
  parents=h.commit_parents(logical,'1'*40)
  cm={**logical,'commit_author':ident,'commit_committer':ident}
  unused,oid=h.commit_request(cm,'2'*40,parents)
  admission={'schema':'pr239-completion-parent-admission-v1','PR':239,
   'evidence_scope':'FACTUAL_PARENT_ADMISSION_REQUIRES_ROOT_ACCEPTANCE','protocol_pin':seed.source_pin,
   'source_manifest_pin':seed.source_manifest_pin,'logical_manifest_pin':seed.manifest_pin,
   'logical_gate_pin':seed.logical_gate_pin,'facts':h.phase_facts(phase),'body_proof_policy':h.BODY_POLICY,
   'QUEUE_policy':h.QUEUE_POLICY,'parent':'1'*40,'parent_tree':'4'*40,'created_UTC':ident['date'],
   'commit_author':ident,'commit_committer':ident,'commit_message':logical['commit_message'],'parents':parents,
   'tree':'2'*40,'candidate':oid,'candidate_journal':'ROOT_COMPLETE239_CANDIDATE_SYNTHETIC'}
  yes(phase+' exact typed canonical admission',lambda:q.checked_admission(seed,admission)['expected_candidate']==oid)
  for key,value in [('parents',list(reversed(parents)) if len(parents)>1 else parents+[h.CURRENT]),
   ('candidate','f'*40),('facts',h.phase_facts('completion100' if phase=='merge95' else 'merge95')),
   ('candidate_journal','ROOT_COMPLETE218_CANDIDATE_OLD')]:
   no(phase+' admission rejects '+key,lambda key=key,value=value:q.checked_admission(seed,{**admission,key:value}))
 yes('two phase pointers distinct',lambda:q.pointer_name({'phase':'merge95'})!=q.pointer_name({'phase':'completion100'}))
 old=b'preserved historical log\n';r95=old+h.phase_marker('merge95')+b'\n';r100=r95+b'dated conditional terminal proposal\n'+h.phase_marker('completion100')+b'\n'
 yes('95 marker',lambda:h.markdown_current(r95,'merge95',True))
 yes('actual append95 to100',lambda:h.markdown_current(r100,'completion100',True))
 yes('all pre95/95 bytes retained',lambda:r100.startswith(r95) and r95.startswith(old))
 for bad in (r100+h.phase_marker('completion100')+b'\n',r100+b'<!-- PR239_NATIVE_PHASE_FACTS-->\n',r100+b'<!-- PR239_NATIVE_PHASE_FACTS\tbad -->\n',r100+b'old stale text\n',h.phase_marker('completion100')+b'\n'):
  no('append history malformed/stale '+str(len(bad)),lambda bad=bad:h.markdown_current(bad,'completion100',True))
 own=b'|239|30001321 / OWR-4081-005|a|b|c|d|e|claimed_solved|3/5|f|g|h|\n';pre=own.replace(b'claimed_solved|3/5',b'queued|0/5')
 yes('canonical own3/5',lambda:h.own_queue_row(own)[0]==own)
 for bad in [b' '+own,b'  '+own,b'   '+own,b'\t'+own,own.replace(b'30001321',b'\x6030001321\x60'),own.replace(b'30001321',b'[30001321](url)'),own.replace(b'|h|',b'|h|extra|'),own[1:]]:
  no('ambiguous own row '+str(len(bad)),lambda bad=bad:h.own_queue_row(own+bad))
 m={'phase':'merge95','queue_pre_row_pin':h.pin(pre),'protected_queue_row_pin':h.pin(own)}
 yes('foreign QUEUE unchanged95',lambda:h.queue_transition(b'foreign\n'+pre,b'foreign\n'+own,m))
 no('foreign QUEUE mutation95',lambda:h.queue_transition(b'foreign\n'+pre,b'changed\n'+own,m))
 no('false1/5 post',lambda:h.queue_transition(pre,own.replace(b'3/5',b'1/5'),m))
 m100={**m,'phase':'completion100','queue_pre_row_pin':h.pin(own)}
 yes('QUEUE100 byte unchanged',lambda:h.queue_transition(own,own,m100))
 no('QUEUE100 rewrite',lambda:h.queue_transition(pre,own,m100))
 for path in ('ROOT_COMPLETE239_CANDIDATE_X/raw.json','nested/ROOT_COMPLETE218_READ_X/receipt.json','_private/a.json','packet/a.json','runtime/a.json','raw/a.json','x.pdf','x.zip'):
  no('public scope '+path,lambda path=path:h.need(h.public_path(h.CASE+path),'Forbidden path'))
 yes('explicit public authored artifact',lambda:h.public_path(h.CASE+'review/final_report.json'))
 for path in ('proof.pdf','source.zip','image.png'):
  yes('science suffix refuses '+path,lambda path=path:not h.science_path(h.ATTEMPT+'/'+path))
 yes('science finite TeX allowed',lambda:h.science_path(h.ATTEMPT+'/paper.tex'))
 yes('all32 inventory finite',lambda:len(h.submitted_inventory())==32 and sum(x['bytes'] for x in h.submitted_inventory())==113228)
 yes('all32 archives exact locations',lambda:len(h.original_archives())==32 and all(p.startswith(h.CASE+'submitted_snapshot_01/') for p in h.original_archives()))
 # Owned synthetic Root receipt representations exercise exact production validators.
 name=sys.argv[1] if len(sys.argv)==2 else '_synthetic_controls_01'
 h.need(re.fullmatch('_synthetic_controls_[0-9]{2}',name) is not None,'Only explicit owned fixture namespace')
 fixture=BASE/name
 h.need(not fixture.exists(),'One-use synthetic output must be absent');fixture.mkdir()
 def save(name,value):
  raw=enc({**value,'SYNTHETIC_FIXTURE_NOT_ACTUAL_ROOT_AUTHORITY':True});p=fixture/(name+'.json')
  with p.open('xb') as f:h.need(f.write(raw)==len(raw),'Short fixture write')
  p.chmod(0o444);return {'path':str(p),**h.pin(raw)}
 pub={'schema':'pr239-root-actual-publication-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,'accepted':True,
  'published':True,'actual_submitted_record_verified_by_top_level_kit':True,'public_body_downloads_SHA256_verified':True,
  'new_publication':True,'unknown_outcome':False,'record_id':999999999,'doi':'10.5281/zenodo.999999999',
  'files':[{'name':'synthetic.pdf','size':2,'sha256':'a'*64},{'name':'synthetic.zip','size':3,'sha256':'b'*64}]}
 pubref=save('publication',pub)
 track={'schema':'pr239-root-actual-tracker-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,'accepted':True,
  'appended_once':True,'native_readback_verified':True,'fresh_duplicate_check_accepted':True,'publication_receipt':pubref,
  'spreadsheet_id':h.SPREADSHEET,'tab':'Math Puzzles','row':['30001321 synthetic','synthetic','https://doi.org/'+pub['doi'],'https://github.com/AlecKriebel/Math/pull/239'],"range":"'Math Puzzles'!A999:D999"}
 tref=save('tracker',track);em={'evidence_references':{'publication':pubref,'tracker':tref}}
 yes('actual-shaped new publication/tracker relation',lambda:h.publication_identity(em)['record_id']==999999999)
 for key,value in [('new_publication',False),('unknown_outcome',True),('doi','10.5281/zenodo.23387774'),('schema','pr218-root-actual-publication-v1')]:
  rr=save('bad_pub_'+key,{**pub,key:value});no('pub mismatch '+key,lambda rr=rr:h.publication_identity({'evidence_references':{'publication':rr,'tracker':tref}}))
 for key,value in [('appended_once',False),('row',['30001321','','https://doi.org/wrong','https://github.com/AlecKriebel/Math/pull/239']),('range',"'Math Puzzles'!A999:D998")]:
  rr=save('bad_track_'+key,{**track,key:value});no('tracker mismatch '+key,lambda rr=rr:h.publication_identity({'evidence_references':{'publication':pubref,'tracker':rr}}))
 casreq=save('merge_request',{'tool':'NativeMCP.github_update_ref','owner':'AlecKriebel','repo':'Math','ref':'heads/main','expected_sha':'1'*40,'sha':'3'*40,'force':False})
 casres=save('merge_response',{'isError':False,'structuredContent':{'success':True}})
 cas={'schema':'pr239-root-completion-actual-CAS-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,'accepted':True,
  'candidate':'3'*40,'tree':'4'*40,'parent':'1'*40,'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,
  'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False,'facts':h.phase_facts('merge95'),'actual_tool_request':casreq,'actual_tool_response':casres}
 casref=save('merge_CAS',cas)
 merge={'schema':'pr239-root-actual-original-pr-merge-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,'accepted':True,
  'actual_original_PR_merged':True,'actual_original_head':h.CURRENT,'actual_original_PR_state':'closed','actual_original_PR_is_draft':False,
  'merge95_full_scope_and_all_selected_bodies_verified':True,'merge95_all_five_verified':True,
  'actual_Root_expected_SHA_force_false_CAS_and_readback_accepted':True,'merge_candidate':'3'*40,'merge_tree':'4'*40,'parent':'1'*40,
  'ordered_parents':['1'*40,h.CURRENT],'actual_CAS_acceptance':casref}
 merger=save('merge',merge);em['phase']='completion100';em['evidence_references']['merge']=merger
 yes('actual-shaped separate merge95 receipt',lambda:h.merge_identity(em)['merge_candidate']=='3'*40)
 no('adoption one-parent merge95',lambda:h.merge_identity({**em,'evidence_references':{**em['evidence_references'],'merge':save('bad_merge',{**merge,'ordered_parents':['1'*40]})}}))
 ready={'schema':'pr239-root-actual-ready-PR-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,'accepted':True,'actual_PR_ready_for_review':True,
  'actual_draft':False,'actual_merged':False,'actual_state':'open','actual_original_head':h.CURRENT,'final_body_pin':h.pin(h.compact('synthetic').encode()),'final_title':'30001321: synthetic ready'}
 rr=save('ready',ready);em['evidence_references']['ready']=rr;em['current_PR_opaque_body_pin']=ready['final_body_pin']
 pr={'number':239,'title':ready['final_title'],'draft':False,'body':'synthetic','state':'open','merged':False,'head':{'sha':h.CURRENT,'ref':'dot/math-30001321'},'base':{'ref':'main'}}
 yes('ready open before95',lambda:h.validate_pr_metadata(pr,{**em,'phase':'merge95'}))
 no('draft is not ready',lambda:h.validate_pr_metadata({**pr,'draft':True},{**em,'phase':'merge95'}))
 no('unmerged cannot become100 via ancestry',lambda:h.validate_pr_metadata(pr,em))
 merged={**pr,'state':'closed','merged':True,'merged_at':'synthetic dated observation','merge_commit_sha':'3'*40}
 yes('100 actual merged C1',lambda:h.validate_pr_metadata(merged,em))
 no('wrong actual merge',lambda:h.validate_pr_metadata({**merged,'merge_commit_sha':'5'*40},em))
 no('95 closed beforeeffect',lambda:h.validate_pr_metadata(merged,{**em,'phase':'merge95','expected_candidate':'3'*40}))
 yes('95 immutable proof can observe exact completed C1',lambda:h.validate_pr_metadata(merged,{**em,'phase':'merge95','expected_candidate':'3'*40},allow_post=True))
 no('95 postclosure cannot stillopen',lambda:h.validate_pr_metadata(pr,{**em,'phase':'merge95','expected_candidate':'3'*40},post=True))
 gate_evidence={**em['evidence_references']}
 gate_m={**em,'native_identity_receipt':rr}
 case_gate={'schema':'pr239-root-case-ready-publication-acceptance-v1','evidence_scope':'ACTUAL_ROOT_RECEIPT','PR':239,
  'accepted':True,'mathematical_review_accepted':True,'priority_review_accepted':True,
  'two_distinct_fresh_whole_package_reviews_accepted':True,'final_package_frozen':True,
  'actual_new_publication_and_unique_tracker_append_verified':True,'actual_ready_PR_verified':True,
  'original_and_current_claimed_solved_3of5_preserved':True,'ordered239_intake_and234_bridge_accepted':True,
  'native_identity_receipt':rr,'current_head':h.CURRENT,'evidence_references':{k:v for k,v in gate_evidence.items() if k not in ('case_ready','merge')},
  'numeric_advance_authorized_by_this_file':False,'phase95_cumulative_publication_membership_held_at39':True}
 yes('future Root case-ready exact contract',lambda:h.validate_ready_value(gate_m,gate_evidence,case_gate))
 for key in ('mathematical_review_accepted','priority_review_accepted','two_distinct_fresh_whole_package_reviews_accepted',
  'actual_new_publication_and_unique_tracker_append_verified','actual_ready_PR_verified','ordered239_intake_and234_bridge_accepted'):
  no('missing Root gate '+key,lambda key=key:h.validate_ready_value(gate_m,gate_evidence,{k:v for k,v in case_gate.items() if k!=key}))
 # Production constructor -> exact bytes -> real new-publication consumer; not full inspect/runtime/CAS execution.
 rt=types.SimpleNamespace(h=h,m={**em,'facts':h.phase_facts(),'protected_bodies':[],'protected_queue':{'mode':'100644','type':'blob','sha':'6'*40},
  'protected_queue_row_pin':h.pin(own),'native_identity_receipt':rr},admission={'parent':'7'*40,'parent_tree':'8'*40,'candidate':'9'*40,'tree':'a'*40},
  overlay={'synthetic.txt':b'synthetic\n'})
 rt.m['evidence_references'].update({'case_ready':rr})
 cfg={k:rr for k in ('source_acceptance','logical_gate','Root_gate','manifest','admission','actual_CAS','pointer','sync')}
 cfg.update(extension_source=None,extension_acceptance=None)
 actual={'actual_Root_MCP_CAS_performed':True,'actual_tool_success_and_readback_accepted':True,'original_lock_held_across_actual_Root_CAS':True,'unknown_outcome':False}
 proof={'full_scope_verified':True,'all_selected_native_bodies_verified':True,'foreign_native_tuples_preserved':True,
  'candidate':'9'*40,'tree':'a'*40,'changed_leaves':['synthetic.txt'],'new_directories':[]}
 obs={'coherent_before_after_ref':True,'CAS_or_completion_inferred_from_ancestry':False,'perpetual_or_write_time_Main_equality_claimed':False,
  'CAS_target':'9'*40,'CAS_target_tree':'a'*40,'actual_MAIN_observed':'b'*40,'actual_MAIN_tree':'c'*40,
  'selected_postimage_paths_verified':1,'protected_body_paths_verified':0,'native_final_ref_UTC':'SYNTHETIC_ONLY'}
 lists={'old_memberships':h.source_baseline(),'new_memberships':h.completion_memberships(),**h.completion_memberships()}
 def construct(**kwargs):
  return t.terminal_record(rt,cfg,h.pin(b'terminal'),h.pin(b'manifest'),kwargs.get('actual',actual),proof,fixture/'synthetic_proof.json',
   h.pin(b'proof'),h.pin(b'pointer'),h.pin(b'sync'),[],lists,obs,{},fixture,kwargs.get('source_checks',2))
 record=construct();raw=enc(record)
 yes('production constructor→real consumer bytes',lambda:u.completion_proof(raw,h.pin(raw))['next_numeric_intake_cursor']==240)
 saved=save('CONSTRUCTOR_ONLY_TERMINAL_BYTES',record)
 no('unverified source checks',lambda:construct(source_checks=1))
 no('unknown CAS outcome',lambda:construct(actual={**actual,'unknown_outcome':True}))
 for key,value in [('adopted_existing_publication',True),('next_numeric_intake_cursor',219),('published_count',39),
  ('fully_completed_count',55),('current_head','d'*40),('new_publication_verified',False),('source_gates_verified',False),
  ('actual_Root_expected_SHA_force_false_ref_update_and_native_readback',False),('publication_DOI','10.5281/zenodo.1')]:
  bad=enc({**record,key:value});no('consumer rejects '+key,lambda bad=bad:u.completion_proof(bad,h.pin(bad)))
 bad=copy.deepcopy(record);bad['new_memberships']['fully_completed_eligible_PRs'].append(234)
 no('consumer rejects skip as completion',lambda:u.completion_proof(enc(bad),h.pin(enc(bad))))
 # Exact inherited safety functions are checked by full AST; no production effects.
 old=BASE.parents[1]/'pr218_30006020/native_completion_preparation_01'
 for file,names in {'completion_checkpoint.py':['local_states','reserve_candidate_oid','wait_actual_CAS_reference','hold_CAS'],
                   'concurrent_get_extension.py':['validate_blob','collect_workers'],
                   'ROOT_TERMINAL_INSPECTION.py':['exclusive_root_receipt','inspect']}.items():
  x=ast.parse((BASE/file).read_bytes());y=ast.parse((old/file).read_bytes())
  def get(tree,name):return next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
  # Namespaced schemas inside hold/inspect differ only PR literal; compare normalized source AST.
  for name in names:
   left=ast.unparse(get(x,name)).replace('239','218');right=ast.unparse(get(y,name))
   if name=='inspect':left=left.replace("'fully_completed_count': 56","'fully_completed_count': 55").replace("'published_count': 40","'published_count': 39").replace("'next_numeric_intake_cursor': 240","'next_numeric_intake_cursor': 219")
   yes('inherited AST '+file+':'+name,lambda left=left,right=right:ast.dump(ast.parse(left),include_attributes=False)==ast.dump(ast.parse(right),include_attributes=False))
 return {'schema':'pr239-source-only-control-results-v1','source_preparation_percent':100,'scope':'PURE_CHANGED_CASE_AND_CONSTRUCTOR_CONSUMER_ONLY',
  'passed':len(results),'results':results,'constructor_only_bytes':saved,
  'limits':['No full inspect, operational Seed/Runtime, source gate acceptance, native/API transport, actual CAS, original lock or current five executed.',
   'All Root-shaped fixtures are labelled synthetic, live only in the owned _synthetic_controls_01 and confer no real authority.',
   'The unchanged inspect/exclusive publisher are AST-compared; full end-to-end operational fixture remains independent review work.'],
  'case_completion_claimed':False,'network_Git_provider_PR_ref_original_lock_current_five_effects':False}
if __name__=='__main__':
 result=main();raw=enc(result);path=BASE/('OFFLINE_CONTROL_RESULTS_'+sys.argv[1][-2:]+'.json') if len(sys.argv)==2 else BASE/'OFFLINE_CONTROL_RESULTS.json'
 with path.open('xb') as f:f.write(raw)
 path.chmod(0o444);print(json.dumps({'passed':result['passed'],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}))
