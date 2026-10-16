"""Inert small PR193 final-receipt adapter; Root alone executes/adopts it."""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,re,sys
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr193_30004563/';HEAD='b9a399eeac816dbb8f0e50e81b498c26e5acef81'
FACTUAL=A/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json';MERGE=A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json'
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def read(p):return json.loads(Path(p).read_bytes())
def pin(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def encoded(j):return (json.dumps(j,indent=2)+'\n').encode()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fresh(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def module(name,p):
 s=importlib.util.spec_from_file_location(name,p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);return v

def load():
 i=read(D/'SOURCE_INPUTS.json')
 for name,x in i['preimport_pins'].items():require(pin(P/name)==x,'Approved source changed before import '+name)
 m=module('frozen_own193_completion_derivations',A/'main_completion_preparation_01/complete_main193.py');c,h,n=m.load();h.m.TREE_CACHE_PATH=A/'ACTUAL_COMPLETION_PRIVATE_TREE_CACHE.json';q=module('accepted_native193',A/'native_actual_completion_preparation_01/derive_actual_completion193.py');return m,c,h,n,q

def sources():
 i=read(D/'SOURCE_INPUTS.json');out={}
 for name,x in i['public_files'].items():
  p=P/name;require(not Path(name).is_absolute() and '..' not in Path(name).parts and p.resolve().is_relative_to(P.resolve()) and not p.is_symlink() and not any(t in name.lower() for t in ['private_sources/','private_work/','cache','__pycache__']),'Nonpublic source');require(pin(p)==x,'Pinned reconciliation source drift '+name);out[PREFIX+name]=p.read_bytes()
 for x in read(D/'FINAL_SEAL.json')['manifest']:require(pin(D/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Own source seal drift')
 for name in read(D/'PUBLIC_SAFE_ALLOWLIST.json')['files']:
  p=D/name;require(p.parent==D and p.is_file() and not p.is_symlink(),'Unsafe own artifact');out[PREFIX+D.relative_to(P).as_posix()+'/'+name]=p.read_bytes()
 return out

def row_id(line):
 cells=line.split('|');v=cells[2].strip().split() if len(cells)>3 else []
 return int(v[0]) if v and v[0].isdigit() else None

def reviewed_current_base(m,c,h,base,f,main,current):
 spec=read(D/'SOURCE_INPUTS.json')['inherited_queue_gate'];path=A/spec['path'];require(pin(path)=={k:spec[k] for k in ['bytes','sha256']},'Reviewed foreign QUEUE gate changed');g=read(path)
 require(g['historical_factual_main']==f['main_observed'] and g['historical_queue_pin']==base[m.QUEUE] and g['unchanged_own_problem_id']==30004563 and g['Root_full_diff_read'] is True and g['all_other_selected_identities_unchanged'] is True and g['mutation_performed'] is False,'Reviewed QUEUE inheritance authority differs')
 old=h.body_at(m.QUEUE,f['main_observed']);new=h.body_at(m.QUEUE,g['observed_main']);require(c.byte_pin(old)==g['historical_queue_pin'] and c.byte_pin(new)==g['current_queue_pin'],'Historical/reviewed current QUEUE body pin differs');before=old.decode().splitlines(keepends=True);after=new.decode().splitlines(keepends=True);require(len(before)==len(after),'Foreign QUEUE line inventory changed')
 delta=[{'problem_id':row_id(a),'before':a,'after':b} for a,b in zip(before,after) if a!=b];require(delta==g['exact_changed_lines'] and [x['problem_id'] for x in delta]==g['changed_foreign_problem_ids'] and len(delta)>0 and all(x['problem_id']!=30004563 and x['problem_id']==row_id(x['after']) for x in delta),'QUEUE changes exceed exact Root-reviewed foreign lines');own=[v for v in before if row_id(v)==30004563];require(len(own)==1 and own==[v for v in after if row_id(v)==30004563],'Own published193 QUEUE row changed')
 inherited={**base,m.QUEUE:g['current_queue_pin']};require(len(inherited)==len(base) and {name for name in base if base[name]!=inherited[name]}=={m.QUEUE},'More than QUEUE changed in inherited baseline');require(c.selected_current(h,g['observed_main'],inherited,g['observed_tree'])==g['observed_tree'] and h.api('compare/'+f['factual_commit']+'...'+g['observed_main'])['status'] in ['identical','ahead'],'Reviewed MAIN tree/full inherited identities differ')
 if current:c.selected_current(h,main,inherited,g['observed_tree'])
 return inherited

def prior(m,c,h,n,current=True):
 """Full95/100 reconstruction without any old95 PR metadata gate/context."""
 sources();i=read(D/'SOURCE_INPUTS.json');require(pin(FACTUAL)==i['actual_factual_receipt'] and pin(MERGE)==i['actual_merge_receipt'],'Prior genuine receipt pin changed');a=read(MERGE);f=read(FACTUAL);r95=read(m.generation(a['generation'])/'PREPARATION.json');r100=read(P/i['factual_preparation_path'])
 d95,o95,merged,_=m.reconstructed95(c,h,n,r95);g,z,t=m.external()
 require(a['accepted'] is True and a['PR']==193 and a['original_head']==HEAD and a['merge_commit']==r95['commit'] and a['parents']==[r95['expected_main'],HEAD] and a['tree']==r95['tree'] and a['preparation']==pin(m.generation(a['generation'])/'PREPARATION.json') and a['selected_files']==len(merged) and a['selected_map_sha256']==c.selected_digest(merged) and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True and a['DOI']==z['doi'] and a['tracker_range']==t['range'],'Actual original merge authority differs')
 require(c.selected_current(h,a['main_observed'],merged,r95['tree'])==a['actual_tree'] and h.api('compare/'+r95['commit']+'...'+a['main_observed'])['status'] in ['identical','ahead'],'Actual95 receipt observed tree/selected identities differ')
 require(r100['actual_merge_receipt']==pin(MERGE) and r100['original_merge_generation']==a['generation'],'Factual preparation receipt/source mismatch');c.selected_current(h,r100['expected_main'],merged,r95['tree']);d100=m.derive100(c,n,d95,a,r100['UTC']);require(r100['native_inventory']==d100['native_inventory'],'Native100 prepared inventory differs');o100=m.out_for(c,h,d100,100,r100['expected_main'],r100['UTC'],a);expected=m.selected(c,merged,o100,100);m.verify_stage(c,h,r100,expected,o100,100,z)
 require(f['accepted'] is True and f['status']=='ACTUAL_PR193_FACTUAL100_FULL_PARENT_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED' and f['PR']==193 and f['original_head']==HEAD and f['factual_commit']==r100['commit'] and f['sole_parent']==r100['expected_main'] and f['original_merge_commit']==r95['commit'] and f['selected_files']==len(expected) and f['selected_map_sha256']==c.selected_digest(expected) and f['every_selected_identity_checked_at_actual_observed_MAIN'] is True and f['actual_original_PR_merged'] is True and f['actual_factual_MAIN_accepted'] is True and (f['fully_completed_count'],f['published_count'],f['last_completed_PR'],f['case_percent'])==(41,25,193,100) and f['DOI']==z['doi'] and f['tracker_range']==t['range'] and f['goal_complete'] is False and m.utc(r100['UTC'])<=m.utc(f['UTC'])<=m.utc(now()),'Genuine full factual acceptance differs')
 historical=c.selected_current(h,f['main_observed'],expected,r100['tree']);require(historical==f['actual_tree'] and h.api('compare/'+r100['commit']+'...'+f['main_observed'])['status'] in ['identical','ahead'],'Receipt observed factual tree/ancestry differs');main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r100['commit']+'...'+main)['status'] in ['identical','ahead'],'Actual factual checkpoint not on MAIN')
 inherited=reviewed_current_base(m,c,h,expected,f,main,current)
 return f,a,r100,d100,o100,inherited,main

def accepted(m,c,q,d100,f,stamp):
 require(m.utc(f['UTC'])<=m.utc(stamp)<=m.utc(now()),'Accepted reconciliation date outside prior-receipt/current interval');d=q.derive_actual_completion(phase100=d100,factual_acceptance={'receipt_bytes':FACTUAL.read_bytes(),'receipt_pin':pin(FACTUAL)},factual_utc=stamp);require(d['phase']=='actual_accepted_completion' and d['original_head']==HEAD and d['no_mutation_performed'] is True and set(d['native_files'])==set(d100['native_files']) and d['native_inventory']=={name:c.byte_pin(b) for name,b in d['native_files'].items()},'Accepted native full inventory differs');require(set(d['native_updates'])==m.FACTUAL_NATIVE and d['native_update_inventory']=={name:c.byte_pin(b) for name,b in d['native_updates'].items()} and all(d['native_files'][name]==b for name,b in d100['native_files'].items() if name not in m.FACTUAL_NATIVE),'Accepted native changed scientific/published/custody bytes');return d

def pr_actual(h,d,merge):
 p=h.api('pulls/193');require(p['head']['sha']==HEAD and p['state']=='closed' and p['merged'] is True and p['merge_commit_sha']==merge['merge_commit'] and p['title']==d['PR_title'] and p['body']==d['PR_body'],'Closed original193/actual accepted PR metadata differs; Root applies exact final metadata separately');return p

def projections(o100,stamp,f,gen):
 """Actual prior factual receipt is authority; this checkpoint does not attest itself."""
 j=copy.deepcopy(json.loads(o100[CASE+'CURRENT_CASE_STATUS.json']));p=copy.deepcopy(json.loads(o100[PREFIX+'CURRENT_PROGRESS.json']));w=copy.deepcopy(json.loads(o100[CASE+'WORKFLOW_COMPLETION.json']));receipt='audits/pr193_30004563/ROOT_FINAL_FACTUAL_ACCEPTANCE.json';own='audits/pr193_30004563/actual_completion_reconciliation_preparation_01/generation_'+gen+'/CHECKPOINT_ACCEPTANCE.json';condition='This final postimage becomes effective only after its actual true-parent/full-delta/all-current-identities checkpoint acceptance. Prior genuine factual100 receipt proves193 completion; Root may run194 status-only intake only after this own checkpoint receipt exists.'
 retired={k:copy.deepcopy(v) for k,v in j.items() if k.startswith('factual_postimage_') or k in ['status','completed','actual_factual_MAIN_accepted','actual_factual_checkpoint_accepted','completion_metadata_checkpoint_pending_at_snapshot','next_numeric_intake_cursor','conditional_next_numeric_intake_cursor','advance_to_next_PR_authorized_now','remaining_required_steps']};j['historical_prospective100_case_fields']={'UTC':stamp,'values':retired}
 for k in retired:j.pop(k,None)
 j.update(UTC=stamp,status='ACTUAL_PUBLISHED_TRACKED_MERGED_FACTUAL_ACCEPTED_COMPLETED',completed=True,actual_factual_MAIN_accepted=True,actual_factual_checkpoint_accepted=True,completion_metadata_checkpoint_pending_at_snapshot=False,actual_final_factual_acceptance_receipt=receipt,actual_final_factual_acceptance_sha256=pin(FACTUAL)['sha256'],actual_accepted_factual_commit=f['factual_commit'],next_numeric_intake_cursor=194,conditional_next_numeric_intake_cursor=194,advance_to_next_PR_authorized_now=True,next_status_only_intake_requires_actual_checkpoint_acceptance=True,reconciliation_checkpoint_receipt=own,program_snapshot_authority_condition=condition,remaining_required_steps='Current193 complete. Separate numeric194 status-only intake may follow actual own checkpoint acceptance; broader programme goal remains active.')
 require((p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['dated_eligible_total'])==(41,25,193,99) and len(set(p['fully_completed_eligible_PRs']))==len(p['fully_completed_eligible_PRs'])==41 and len(set(p['published_PRs']))==len(p['published_PRs'])==25 and 193 in p['fully_completed_eligible_PRs'] and 193 in p['published_PRs'],'Actual prior41/25 unique census differs')
 retired={k:copy.deepcopy(v) for k,v in p.items() if k.startswith(('current_','next_','conditional_','actual_factual_','active_checkpoint_','program_snapshot_')) or k in ['completion_metadata_checkpoint_pending_at_snapshot','remaining_current_step','next_step','last_completed_actual_final_receipt_pending']};p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':193,'prior_phase':'prospective100_before_actual_receipt_reconciliation','values':retired})
 for k in retired:p.pop(k,None)
 p.update(UTC=stamp,updated_UTC=stamp,current_PR=193,current_problem_id=30004563,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_budget='2/5',current_PR_workflow_percent=100,current_workflow_estimate_percent=100,current_status='ACTUAL_COMPLETED_PUBLISHED_TRACKED_MERGED_FACTUAL_MAIN_ACCEPTED',current_completed=True,current_closed=True,current_original_PR_merged=True,current_original_PR_open_draft=False,current_mathematical_clearance=True,current_mathematics_cleared=True,current_mathematical_result_valid=True,current_independent_mathematical_audit_families_complete=3,current_independent_mathematical_audit_active=False,current_priority_clearance=True,current_priority_clearance_scope=j['priority_clearance_scope'],current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_publication_ready=True,current_publication_package_reviews_complete=True,current_NEW_whole_publication_package_reviews_completed=2,current_NEW_whole_publication_package_review_active=False,current_Zenodo_published=True,current_DOI=f['DOI'],current_tracker_updated=True,current_tracker_range=f['tracker_range'],current_actual_factual_checkpoint_accepted=True,current_actual_factual_MAIN_accepted=True,current_actual_factual_commit=f['factual_commit'],current_actual_merge_commit=f['original_merge_commit'],current_record='audits/pr193_30004563/CURRENT_CASE_STATUS.json',current_final_factual_acceptance_receipt=receipt,actual_factual_checkpoint_accepted=True,completion_metadata_checkpoint_pending_at_snapshot=False,last_completed_actual_final_receipt=receipt,last_completed_actual_final_receipt_sha256=pin(FACTUAL)['sha256'],next_numeric_intake_cursor=194,conditional_next_numeric_intake_cursor=194,advance_to_next_PR_authorized_now=True,next_status_only_intake_performed=False,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=193,next_status_only_intake_requires_actual_checkpoint_acceptance=True,active_checkpoint_acceptance_receipt=own,program_snapshot_authority_condition=condition,program_snapshot_semantics='Current193 actually complete from prior genuine factual receipt,41completed/25published,last193,41.4percent of dated99. Native/current completion metadata reconciled; next194 status-only release effective only after this own checkpoint actual acceptance. Historical firstness remains unestablished; broader goal active.',current_remaining_required_steps='None for193 result. Separate194 status-only intake after actual own checkpoint acceptance.',remaining_current_step='Separate194 status-only intake after this own checkpoint actual acceptance.',next_step='After actual own checkpoint receipt, perform194 original-status intake only; new eligible work requires its own review.',fully_completed_fraction_percent=41.4,workflow_estimate_percent=41.4,workflow_estimate_definition='41/dated99 completed,25 published; dated denominator is not a fresh eligibility census.',peer_pause_or_exclusive_writer_window_assumed=False,persistent_goal_complete=False)
 w.update(UTC=stamp,schema='PR193_ACTUAL_COMPLETION_RECORDED_FROM_PRIOR_ROOT_RECEIPT_V1',completed=True,actual_factual_MAIN_accepted=True,factual_acceptance_receipt_pending=False,prior_actual_factual_acceptance=receipt,prior_actual_factual_acceptance_sha256=pin(FACTUAL)['sha256'],actual_accepted_factual_commit=f['factual_commit'],next_numeric_intake_cursor=194,conditional_next_numeric_intake_cursor=194,advance_to_next_PR_authorized_now=True,next_status_only_intake_requires_actual_checkpoint_acceptance=True,reconciliation_checkpoint_receipt=own,program_snapshot_authority_condition=condition)
 require(j['goal_complete'] is False and w['goal_complete'] is False,'Broader programme falsely completed');return j,p,w

def overlay(m,c,h,q,d100,o100,f,parent,stamp,gen):
 d=accepted(m,c,q,d100,f,stamp);j,p,w=projections(o100,stamp,f,gen);out=sources();out.update(d['native_updates']);out[CASE+'CURRENT_CASE_STATUS.json']=encoded(j);out[PREFIX+'CURRENT_PROGRESS.json']=encoded(p);out[CASE+'WORKFLOW_COMPLETION.json']=encoded(w)
 note='\n'+stamp+' — PR193 actually completed from prior factual acceptance '+f['factual_commit']+' ('+pin(FACTUAL)['sha256']+'), published '+f['DOI']+', tracker '+f['tracker_range']+', original-HEAD merge '+f['original_merge_commit']+'. Native/PR current prose and completion flags now reflect that genuine prior acceptance, preserving all science/publication/original19/QUEUE bytes.41completed/25published,last193,41.4percent of dated99; historical novelty/firstness unestablished. Cursor194/advance release is effective only after this own checkpoint actual current-tree acceptance; no194 intake performed here, broader goal active.\n'
 for name in [CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[name]=h.body_at(name,parent)+note.encode()
 return d,out

def selected(m,c,base,out):
 allowed=m.MUTABLE|m.FACTUAL_NATIVE|{CASE+'WORKFLOW_COMPLETION.json'}
 for name,b in out.items():
  require(name.startswith(CASE) or name in allowed,'Unowned final reconciliation overlay')
  if name in base and name not in allowed:require(c.byte_pin(b)==base[name],'Protected factual identity changed '+name)
 require(m.QUEUE not in out,'QUEUE must remain unchanged');return {**base,**{name:c.byte_pin(b) for name,b in out.items()}}

def message(f,digest):return 'Record PR193 actual completed metadata from prior factual receipt;41completed/25published\n\n'+f['DOI']+'; scientific/package/original/QUEUE bytes preserved; actual native completion metadata reconciled.194 status-only intake only after own actual checkpoint acceptance; broader goal active.\nPR193 actual-completion selected-map SHA256: '+digest

def verify(m,c,h,r,expected,out,f):
 require(r['overlay_paths']==sorted(out) and m.QUEUE not in r['changed_paths'],'Final exact overlay/QUEUE scope differs');m.verify_object(c,h,r,[r['expected_main']],expected,message(f,c.selected_digest(expected)))

def generation(gen):require(re.fullmatch('[a-z0-9_]{1,48}',gen),'Use fresh bounded generation');return D/('generation_'+gen)

def prepare(m,c,h,n,q,gen):
 f,a,r100,d100,o100,base,parent=prior(m,c,h,n,True);stamp=now();d,out=overlay(m,c,h,q,d100,o100,f,parent,stamp,gen);pr_actual(h,d,a);dest=generation(gen);dest.mkdir(exist_ok=False);expected=selected(m,c,base,out);pt=h.api('git/commits/'+parent)['tree']['sha'];tree=h.api('git/trees','POST',{'base_tree':pt,'tree':m.entries(c,h,out)});digest=c.selected_digest(expected);co=h.api('git/commits','POST',{'message':message(f,digest),'tree':tree['sha'],'parents':[parent]});h.m.m.h.warm_selected_directories([pt,tree['sha']],expected);changed=sorted(name for name,x in expected.items() if h.lookup(pt,name)!=('100644','blob',x['git_blob']));r={'UTC':stamp,'expected_main':parent,'parent_tree':pt,'tree':tree['sha'],'commit':co['sha'],'selected_files':expected,'selected_map_sha256':digest,'overlay_paths':sorted(out),'changed_paths':changed,'actual_factual_receipt':pin(FACTUAL),'native_update_inventory':d['native_update_inventory'],'MAIN_moved':False};fresh(dest/'PREPARATION.json',encoded(r));verify(m,c,h,r,expected,out,f);pr_actual(h,d,a);require(h.api('git/ref/heads/main')['object']['sha']==parent,'MAIN advanced; preserve generation/retry fresh');print(json.dumps({'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected':len(expected),'changed':len(changed),'MAIN_moved':False}))

def accept(m,c,h,n,q,gen):
 r=read(generation(gen)/'PREPARATION.json');f,a,r100,d100,o100,base,main=prior(m,c,h,n,False);require(r['actual_factual_receipt']==pin(FACTUAL),'Prepared genuine factual receipt drift');c.selected_current(h,r['expected_main'],base,r100['tree']);d,out=overlay(m,c,h,q,d100,o100,f,r['expected_main'],r['UTC'],gen);require(r['native_update_inventory']==d['native_update_inventory'],'Accepted native update inventory differs');expected=selected(m,c,base,out);verify(m,c,h,r,expected,out,f);require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Final reconciliation not on MAIN');tree=m.current_bodies(c,h,main,expected,out)
 for name,b in d['native_files'].items():
  if name not in out:require(h.body_at(name,main)==b,'Fresh full accepted native body differs '+name)
 require(c.byte_pin(h.body_at(m.QUEUE,main))==base[m.QUEUE],'QUEUE byte/hash/blob drift');pr_actual(h,d,a);result={'UTC':now(),'PR':193,'original_head':HEAD,'accepted':True,'status':'ACTUAL_PR193_FINAL_RECEIPT_NATIVE_METADATA_RECONCILIATION_CHECKPOINT_ACCEPTED','checkpoint_commit':r['commit'],'sole_parent':r['expected_main'],'main_observed':main,'actual_tree':tree,'selected_files':len(expected),'selected_map_sha256':c.selected_digest(expected),'prior_actual_factual_receipt':pin(FACTUAL),'prior_actual_factual_commit':f['factual_commit'],'every_selected_identity_checked_at_actual_observed_MAIN':True,'current_native_completion_flags_and_PR_metadata_actual':True,'QUEUE_science_publication_original19_unchanged':True,'fully_completed_count':41,'published_count':25,'last_completed_PR':193,'case_percent':100,'next_numeric_intake_cursor':194,'advance_to_next_PR_authorized_now':True,'next_status_only_intake_authorized':True,'next_intake_performed':False,'goal_complete':False};fresh(generation(gen)/'CHECKPOINT_ACCEPTANCE.json',encoded(result));print(json.dumps(result))

if __name__=='__main__':
 require(sys.dont_write_bytecode,'Use Python -B');require(len(sys.argv)==3 and sys.argv[1] in ['prepare','accept'],'Usage: reconcile_completion193.py prepare|accept fresh_generation');m,c,h,n,q=load();(prepare if sys.argv[1]=='prepare' else accept)(m,c,h,n,q,sys.argv[2])
