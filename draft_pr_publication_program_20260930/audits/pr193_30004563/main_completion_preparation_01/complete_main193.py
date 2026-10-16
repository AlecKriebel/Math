"""Inert PR193-only merge95/factual100 proposal; Root alone executes/adopts it."""
from pathlib import Path
import base64,copy,datetime,hashlib,importlib.util,json,re,sys
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr193_30004563/';NATIVE='unsolved_math_prioritization/attempts/30004563/'
HEAD='b9a399eeac816dbb8f0e50e81b498c26e5acef81';QUEUE='unsolved_math_prioritization/QUEUE.md'
PRIOR=A/'publication_checkpoint_preparation_01/checkpoint_publication01'
WORKFLOW=CASE+'WORKFLOW_COMPLETION.json';MERGE_RECEIPT=A/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json'
PROG=['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']
MUTABLE={PREFIX+n for n in PROG}|{CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md'}
FACTUAL_NATIVE={NATIVE+n for n in ['CURRENT_PROOF.md','README.md','SOURCE_AUDIT.md','source_manifest.json','readiness.json','continuity.json','PUBLICATION.json','FINAL_DISPOSITION.md','RESEARCH_LOG.md','frozen_artifacts.json']}
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def read(p):return json.loads(Path(p).read_bytes())
def encoded(j):return (json.dumps(j,indent=2)+'\n').encode()
def pin(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def utc(s):
 require(isinstance(s,str),'UTC string required');t=datetime.datetime.fromisoformat(s.replace('Z','+00:00'));require(t.utcoffset()==datetime.timedelta(0),'UTC offset required');return t

def fresh(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def load():
 i=read(D/'SOURCE_INPUTS.json')
 for n,x in i['utility_pins'].items():require(pin(P/n)==x,'Approved low-level utility drift '+n)
 c=module('lowlevel191_only',P/'audits/pr191_5000005/lifecycle_common.py');h=module('native_objects193',P/'audits/pr190_5000007/prepare_final_scoped_merge.py');h.m.TREE_CACHE_PATH=A/'MAIN_COMPLETION_PRIVATE_TREE_CACHE.json'
 n=module('native_derivation193',A/'native_integration_preparation_02/derive_native193.py');return c,h,n

def sources():
 i=read(D/'SOURCE_INPUTS.json');out={}
 for name,x in i['public_files'].items():
  p=P/name;require(not Path(name).is_absolute() and '..' not in Path(name).parts and p.resolve().is_relative_to(P.resolve()) and not p.is_symlink() and not any(v in name.lower() for v in ['private_sources/','private_work/','cache','__pycache__']),'Nonpublic source path');require(pin(p)==x,'Pinned source drift '+name);out[PREFIX+name]=p.read_bytes()
 for x in read(D/'FINAL_SEAL.json')['manifest']:require(pin(D/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Completion source seal drift')
 for name in read(D/'PUBLIC_SAFE_ALLOWLIST.json')['files']:
  p=D/name;require(p.parent==D and p.is_file() and not p.is_symlink(),'Unsafe own source');out[PREFIX+D.relative_to(P).as_posix()+'/'+name]=p.read_bytes()
 return out

def external():
 i=read(D/'SOURCE_INPUTS.json');g=read(A/'ROOT_PUBLICATION_GATE.json');z=read(A/'ROOT_PUBLICATION_RECEIPT.json');t=read(A/'ROOT_TRACKER_RECEIPT.json');inspect=read(A/'ZENODO_PUBLISHED_INSPECT_01.json')
 for name,x in i['actual_receipts'].items():require(pin(A/name)==x,'Actual Root receipt drift '+name)
 require(g['PR']==193 and g['original_head']==HEAD and g['publication_ready'] is True and len(g['whole_package_reviews'])==2 and len({r['reviewer_id'] for r in g['whole_package_reviews']})==2 and all(r['disposition']=='CLEAN_PASS' for r in g['whole_package_reviews']),'Root final scientific gate differs')
 gate_sha=pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'];require(gate_sha==i['publication_gate_sha256'] and z['gate_sha256']==t['gate_sha256']==inspect['gate_sha256']==gate_sha and z['PR']==t['PR']==inspect['PR']==193 and z['original_head']==HEAD,'Actual original/gate binding differs')
 require(z['state']==inspect['state']=='published' and z['metadata_exact_verified'] is True and inspect['metadata_exact_verified'] is True and z['environment']==inspect['environment']=='production' and z['doi']==t['doi']==inspect['doi']=='10.5281/zenodo.23392409' and z['doi_url']=='https://doi.org/'+z['doi'] and z['doi_resolution']['status']==inspect['doi_resolution']['status']=='resolved' and z['doi_resolution']['http_status']==inspect['doi_resolution']['http_status']==200,'Actual exact published DOI evidence differs')
 expected={name:(g['package_files'][name]['bytes'],g['package_files'][name]['sha256']) for name in ['five_centers.pdf','five_centers.tex','verification-package.zip']}
 require(len(z['files'])==len(inspect['files'])==3 and {f['name']:(f['size'],f['sha256']) for f in z['files']}=={f['name']:(f['size'],f['sha256']) for f in inspect['files']}==expected,'Actual three published bodies differ')
 require(t['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and t['gid']==1254632077 and t['tab']=='Math Puzzles' and t['range']=="'Math Puzzles'!A106:D106" and t['header']==['Original Problem','Solution Chat URL','DOI','Notes'] and isinstance(t['values'],list) and len(t['values'])==1 and len(t['values'][0])==4 and all(isinstance(x,str) for x in t['values'][0]) and t['values'][0][2]==z['doi_url'] and t['append_performed'] is True and t['own_row_readback_verified'] is True and t['actual_fresh_reads']==2 and t['foreign_rows_retained'] is True,'Actual own tracker target/row/two reads differs')
 return g,z,t

def publication_message(digest):return 'Record PR193 reviewed publication85% checkpoint;40completed/24published\n\nTwo NEW clean package reviews; qualified priority only, historical firstness unestablished. No actual publication/tracker/QUEUE/native/PR changes or194 intake.\nPR193 publication selected-map SHA256: '+digest

def verify_object(c,h,r,parents,expected,message):
 require(r['selected_files']==expected and r['selected_map_sha256']==c.selected_digest(expected),'Exact selected map changed/pruned');co=h.api('git/commits/'+r['commit']);pt=h.api('git/commits/'+r['expected_main'])['tree']['sha'];require(co['tree']['sha']==r['tree'] and pt==r['parent_tree'] and [x['sha'] for x in co['parents']]==parents and co['message']==message,'Actual parents/tree/operative message differ');h.m.m.h.warm_selected_directories([pt,r['tree']],expected)
 for name,x in expected.items():require(h.lookup(r['tree'],name)==('100644','blob',x['git_blob']),'Selected prepared identity differs '+name)
 changed={name for name,x in expected.items() if h.lookup(pt,name)!=('100644','blob',x['git_blob'])};require(changed==set(r['changed_paths'])==h.changed_leaves(pt,r['tree']) and changed<=set(r['overlay_paths']),'Actual full-tree foreign/undeclared delta')

def baseline(c,h,current=False):
 sources();g,z,t=external();i=read(D/'SOURCE_INPUTS.json');r=read(PRIOR/'PUBLICATION_CHECKPOINT_PREPARATION.json');a=read(PRIOR/'PUBLICATION_CHECKPOINT_ACCEPTANCE.json');pm=read(PRIOR/'ROOT_PRE_MOVE_VERIFICATION.json')
 require((r['commit'],r['expected_main'],r['tree'],len(r['selected_files']))==(i['publication_checkpoint_commit'],i['publication_checkpoint_parent'],i['publication_checkpoint_tree'],1150),'Accepted publication preparation differs');verify_object(c,h,r,[r['expected_main']],r['selected_files'],publication_message(c.selected_digest(r['selected_files'])))
 require(a['status']=='ACTUAL_PR193_PUBLICATION85_TRUE_PARENT_FULL_DELTA_ALL_CURRENT_IDENTITIES_ACCEPTED' and a['checkpoint_commit']==a['main_observed']==r['commit'] and a['sole_parent']==r['expected_main'] and a['actual_tree']==r['tree'] and a['selected_files']==1150 and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True and a['QUEUE_written'] is False and (a['fully_completed_count'],a['published_count'],a['case_percent'])==(40,24,85),'Actual1150 publication acceptance differs')
 require(pm['commit']==r['commit'] and pm['expected_main']==r['expected_main'] and pm['tree']==r['tree'] and pm['selected']==1150 and pm['QUEUE_changed'] is False and pm['MAIN_moved'] is False,'Root publication pre-move acceptance differs');c.selected_current(h,a['main_observed'],r['selected_files'],r['tree']);main=h.api('git/ref/heads/main')['object']['sha'];require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Accepted publication checkpoint not on MAIN')
 require(c.byte_pin((D/'CASE_BASELINE85.json').read_bytes())==r['selected_files'][CASE+'CURRENT_CASE_STATUS.json'] and c.byte_pin((D/'CASE_LOG_BASELINE85.md').read_bytes())==r['selected_files'][CASE+'RESEARCH_LOG.md'],'Immutable85 case/log baselines differ')
 if current:c.selected_current(h,main,r['selected_files'],r['tree'])
 return r,a,main,g,z,t

def original(h,derived,merged=False):
 p=h.api('pulls/193');require(p['head']['sha']==HEAD and p['merged'] is merged and p['state']==('closed' if merged else 'open') and p['title']==derived['PR_title'] and p['body']==derived['PR_body'],'Original PR head/state/exact metadata differs')
 if not merged:require(p['draft'] is False,'Root must apply exact metadata and mark ready before preparation')
 return p

def derive95(c,h,n,parent,stamp):
 g,z,t=external();q=h.body_at(QUEUE,parent);require(utc(stamp)>=max(utc(z['UTC']),utc(t['UTC']),utc(read(A/'ZENODO_PUBLISHED_INSPECT_01.json')['UTC']),utc(read(A/'ROOT_PR_METADATA_READY_ACCEPTANCE_01.json')['UTC'])) and utc(stamp)<=utc(now()),'Native95 stamp outside actual evidence/current interval')
 d=n.derive_phase95(receipt_pins={'publication':pin(A/'ROOT_PUBLICATION_RECEIPT.json'),'tracker':pin(A/'ROOT_TRACKER_RECEIPT.json')},fresh_main={'branch':'main','commit':parent,'QUEUE':q,'QUEUE_pin':{k:c.byte_pin(q)[k] for k in ['bytes','sha256']},'verified_utc':stamp,'merge_gate_authorized':True},factual_utc=stamp)
 require(d['phase']==95 and d['original_head']==HEAD and d['fresh_MAIN_parent']==parent and d['no_mutation_performed'] is True and d['native_inventory']=={name:c.byte_pin(b) for name,b in sorted(d['native_files'].items())},'Native95 exact derivation/inventory differs')
 before=q.decode().splitlines(keepends=True);after=d['QUEUE_postimage'].decode().splitlines(keepends=True);changes=[(x,y) for x,y in zip(before,after) if x!=y];require(len(before)==len(after) and len(changes)==1 and '| 30004563 /' in changes[0][0] and '| 30004563 /' in changes[0][1],'QUEUE foreign row/inventory changed');old,new=[x.rstrip('\n').split('|') for x in changes[0]];require(len(old)==len(new)==14 and all(old[j]==new[j] for j in range(14) if j not in [8,9,10,11,12]) and old[8].strip()=='queued' and old[9].strip()=='0/5' and new[8].strip()=='claimed_solved' and new[9].strip()=='2/5','Only exact fresh queued0/5 own target cells8..12 may change')
 return d

SCIENCE_KEYS=['PR','problem_id','original_head','original_QUEUE_status','original_effort','mathematical_clearance','priority_clearance','original_files_preserved','exact_primary_target','mathematical_result_valid','mathematical_gate','priority_audit_complete','priority_clearance_scope','qualified_note_priority_gate','historical_novelty_or_firstness_established','exact_claim','scope_exclusions']
def case_status(stage,stamp,z,t,merge=None):
 b=read(D/'CASE_BASELINE85.json');j={k:copy.deepcopy(b[k]) for k in SCIENCE_KEYS};j['historical_case_baseline85']=b
 j.update(UTC=stamp,status='ACTUAL_PUBLISHED_TRACKED_MERGE_PENDING' if stage==95 else 'FACTUAL100_POSTIMAGE_ACTUAL_MAIN_ACCEPTANCE_PENDING',case_percent=stage,publication_ready=True,whole_publication_package_reviews_complete=True,new_whole_publication_package_reviews_completed=2,current_publication_package='publication_package_v2/',publication_gate='ROOT_PUBLICATION_GATE.json',actual_Zenodo_published=True,DOI=z['doi'],DOI_URL=z['doi_url'],actual_tracker_updated=True,tracker_range=t['range'],actual_original_PR_merged=stage==100,original_PR_closed=stage==100,completed=False,factual_postimage_completion_proposed=stage==100,actual_factual_MAIN_accepted=False,actual_factual_checkpoint_accepted=False,completion_metadata_checkpoint_pending_at_snapshot=True,fully_completed_count=40 if stage==95 else 41,published_count=24 if stage==95 else 25,last_completed_PR=191 if stage==95 else 193,actual_initial_intake_checkpoint_accepted=True,actual_initial_intake_checkpoint=b['actual_initial_intake_checkpoint'],next_numeric_intake_cursor=193,conditional_next_numeric_intake_cursor=194,advance_to_next_PR_authorized_now=False,goal_complete=False,remaining_required_steps='Actual original-HEAD merge then separate factual100 and actual acceptance; own receipt checkpoint before194 intake.' if stage==95 else 'Actual full-current-MAIN factual acceptance, then separate own actual-receipt/native reconciliation checkpoint before194 status-only intake.')
 if stage==100:j.update(actual_merge_acceptance='ROOT_ACTUAL_MERGE_ACCEPTANCE.json',actual_merge_commit=merge['merge_commit'])
 return j

def programme(before,stage,stamp,z,t,merge=None):
 require((before['current_PR'],before['fully_completed_count'],before['published_count'],before['last_completed_PR'],before['next_numeric_intake_cursor'])==(193,40,24,191,193),'True-parent current193/census differs');require(len(set(before['fully_completed_eligible_PRs']))==len(before['fully_completed_eligible_PRs'])==40 and len(set(before['published_PRs']))==len(before['published_PRs'])==24 and 193 not in before['fully_completed_eligible_PRs'] and 193 not in before['published_PRs'],'True-parent unique census differs');j=copy.deepcopy(before)
 retired={k:copy.deepcopy(v) for k,v in before.items() if k.startswith(('current_','conditional_','next_','actual_factual_','active_checkpoint_','program_snapshot_')) or k in ['remaining_current_step','next_step','completion_metadata_checkpoint_pending_at_snapshot','completion_receipt_checkpoint_effective_after_actual_current_MAIN_acceptance','latest_ordered_intake_record']};j.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':193,'prior_phase':85 if stage==95 else 95,'values':retired})
 for k in retired:j.pop(k,None)
 j.update(UTC=stamp,updated_UTC=stamp,current_PR=193,current_problem_id=30004563,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_budget='2/5',current_PR_workflow_percent=stage,current_workflow_estimate_percent=stage,current_status='ACTUAL_PUBLISHED_TRACKED_ORIGINAL_HEAD_MERGE_PENDING' if stage==95 else 'FACTUAL100_POSTIMAGE_ACTUAL_ACCEPTANCE_PENDING',current_mathematical_clearance=True,current_mathematics_cleared=True,current_mathematical_result_valid=True,current_independent_mathematical_audit_active=False,current_counterexample_claim_under_NEW_independent_audit=False,current_independent_mathematical_audit_families_complete=3,current_priority_clearance=True,current_priority_clearance_scope=read(D/'CASE_BASELINE85.json')['priority_clearance_scope'],current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_publication_ready=True,current_publication_package_reviews_complete=True,current_NEW_whole_publication_package_reviews_completed=2,current_NEW_whole_publication_package_review_active=False,current_publication_package='audits/pr193_30004563/publication_package_v2/',current_publication_gate='audits/pr193_30004563/ROOT_PUBLICATION_GATE.json',current_Zenodo_published=True,current_DOI=z['doi'],current_tracker_updated=True,current_tracker_range=t['range'],current_original_PR_merged=stage==100,current_original_PR_open_draft=False,current_closed=stage==100,current_completed=False,current_factual_postimage_completion_proposed=stage==100,current_actual_factual_checkpoint_accepted=False,actual_factual_checkpoint_accepted=False,completion_metadata_checkpoint_pending_at_snapshot=True,current_record='audits/pr193_30004563/CURRENT_CASE_STATUS.json',next_numeric_intake_cursor=193,conditional_next_numeric_intake_cursor=194,conditional_next_intake_requires_actual_factual_acceptance=True,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=193,advance_to_next_PR_authorized_now=False,next_status_only_intake_performed=False,next_intake_requires_explicit_writer_release=False,current_remaining_required_steps='Actual original-HEAD merge and separate factual100/current-tree acceptance, then own receipt reconciliation before194.' if stage==95 else 'Actual factual current-tree acceptance and own receipt/native reconciliation before194 status-only intake.',remaining_current_step='Actual merge/factual acceptance remains required.' if stage==95 else 'Factual postimage prepared; actual acceptance and own receipt reconciliation remain required.',next_step='Complete current193 actual acceptance and receipt checkpoint before194.',program_snapshot_authority_condition='Current phase facts are effective only after actual parent/full-delta/all-current-identities acceptance; next194 remains conditional.',program_snapshot_semantics='Actual credited alpha16 at-least-five crossing-allowed note published/tracked, historical novelty/firstness unestablished. Two NEW whole-package reviews clean. Cursor193/conditional194/advancefalse; broader goal active.',persistent_goal_complete=False)
 if stage==100:
  prior_last={k:copy.deepcopy(v) for k,v in before.items() if k.startswith(('last_completed_','last_published_'))};j.setdefault('historical_prior_completion_metadata',[]).append({'UTC':stamp,'PR':191,'fully_completed_count':40,'published_count':24,'values':prior_last})
  for key in prior_last:j.pop(key,None)
  j['fully_completed_eligible_PRs']=before['fully_completed_eligible_PRs']+[193];j['published_PRs']=before['published_PRs']+[193];j.update(fully_completed_count=41,published_count=25,last_completed_PR=193,last_completed_PR_workflow_percent=100,last_completed_original_head=HEAD,last_completed_original_QUEUE_status='claimed_solved',last_completed_original_budget='2/5',last_completed_mathematical_result_valid=True,last_completed_priority_clearance=True,last_completed_priority_clearance_scope=read(D/'CASE_BASELINE85.json')['priority_clearance_scope'],last_completed_outcome='published_credited_at_least_five_crossing_allowed_alpha16_counterexample',last_completed_DOI=z['doi'],last_completed_merge_commit=merge['merge_commit'],last_completed_tracker_range=t['range'],last_completed_record='audits/pr193_30004563/WORKFLOW_COMPLETION.json',last_completed_historical_firstness_or_guaranteed_novelty_certified=False,last_completed_actual_final_receipt_pending=True,last_completed_bounded_priority_audit_complete=True,last_completed_source_author_authenticated_erratum=False,last_completed_source_unique_intent_certified=False,last_completed_DOI_file_identity_verified=True,last_published_PR=193,last_published_DOI=z['doi'],last_published_tracker_range=t['range'],current_actual_merge_commit=merge['merge_commit'],conditional_PR193_final_receipt='audits/pr193_30004563/ROOT_FINAL_FACTUAL_ACCEPTANCE.json')
 require(j['dated_eligible_total']==99,'Dated denominator changed; require review');fraction=round(100*j['fully_completed_count']/j['dated_eligible_total'],1);j.update(fully_completed_fraction_percent=fraction,workflow_estimate_percent=fraction,workflow_estimate_definition=str(j['fully_completed_count'])+'/dated'+str(j['dated_eligible_total'])+' completed,'+str(j['published_count'])+' published; dated denominator is not a fresh eligibility census.',peer_pause_or_exclusive_writer_window_assumed=False)
 return j

def out_for(c,h,d,stage,parent,stamp,merge=None):
 g,z,t=external();out=sources();out.update(d['native_files']);out[CASE+'CURRENT_CASE_STATUS.json']=encoded(case_status(stage,stamp,z,t,merge));note='\n'+stamp+' — PR193 workflow'+str(stage)+'%: '+z['doi_url']+' actually published; tracker '+t['range']+' verified. Original claimed_solved2/5 preserved. At least five outgoing centers, crossings allowed; proper embeddings/exact total/global maximum/alpha<1 excluded. Old curve family credited; historical novelty/firstness/independence unestablished. '+('Original-HEAD merge and separate factual acceptance pending,40completed/24published.' if stage==95 else 'Original-HEAD merge actually accepted; factual41completed/25published postimage requires actual current-MAIN acceptance and next own receipt/native reconciliation.')+' Cursor193/conditional194/advancefalse; broader goal active.\n';case_prefix=(D/'CASE_LOG_BASELINE85.md').read_bytes()
 if stage==100:
  prior_stamp=read(generation(merge['generation'])/'PREPARATION.json')['UTC']
  prior_note='\n'+prior_stamp+' — PR193 workflow95%: '+z['doi_url']+' actually published; tracker '+t['range']+' verified. Original claimed_solved2/5 preserved. At least five outgoing centers, crossings allowed; proper embeddings/exact total/global maximum/alpha<1 excluded. Old curve family credited; historical novelty/firstness/independence unestablished. Original-HEAD merge and separate factual acceptance pending,40completed/24published. Cursor193/conditional194/advancefalse; broader goal active.\n';case_prefix+=prior_note.encode()
 out[CASE+'RESEARCH_LOG.md']=case_prefix+note.encode()
 before=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));out[PREFIX+'CURRENT_PROGRESS.json']=encoded(programme(before,stage,stamp,z,t,merge))
 for name in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:out[PREFIX+name]=h.body_at(PREFIX+name,parent)+note.encode()
 workflow={'schema':'PR193_ACTUAL_DISPOSITION_FACTUAL_POSTIMAGE_V1','PR':193,'original_head':HEAD,'original_status':'claimed_solved','original_effort':'2/5','UTC':stamp,'phase':stage,'DOI':z['doi'],'tracker_range':t['range'],'published':True,'tracked':True,'whole_package_reviews_complete':True,'actual_original_PR_merged':stage==100,'actual_factual_MAIN_accepted':False,'factual_acceptance_receipt_pending':True,'fully_completed_count':40 if stage==95 else 41,'published_count':24 if stage==95 else 25,'last_completed_PR':191 if stage==95 else 193,'next_numeric_intake_cursor':193,'conditional_next_numeric_intake_cursor':194,'advance_to_next_PR_authorized_now':False,'historical_novelty_or_firstness_established':False,'goal_complete':False}
 if stage==95:out[QUEUE]=d['QUEUE_postimage']
 else:out[CASE+'ROOT_ACTUAL_MERGE_ACCEPTANCE.json']=MERGE_RECEIPT.read_bytes();workflow['actual_merge_commit']=merge['merge_commit']
 out[WORKFLOW]=encoded(workflow);return out

def selected(c,before,out,stage):
 allowed=MUTABLE|{WORKFLOW,QUEUE} if stage==95 else MUTABLE|FACTUAL_NATIVE|{WORKFLOW}
 for name,b in out.items():
  require(name.startswith(CASE) or name.startswith(NATIVE) or name in MUTABLE or (stage==95 and name==QUEUE),'Unowned completion overlay')
  if name in before and name not in allowed:require(c.byte_pin(b)==before[name],'Protected selected identity changed '+name)
 return {**before,**{name:c.byte_pin(b) for name,b in out.items()}}

def operative(stage,z,digest):return ('Merge original PR193: credited five-center alpha16 note; ' if stage==95 else 'Record PR193 factual41/25 postimage; actual acceptance required; ')+z['doi_url']+'\n\nPR193 phase'+str(stage)+' exact selected-map SHA256: '+digest

def verify_stage(c,h,r,expected,out,stage,z):
 require(r['phase']==stage and r['overlay_paths']==sorted(out),'Phase/overlay scope differs');parents=[r['expected_main'],HEAD] if stage==95 else [r['expected_main']];verify_object(c,h,r,parents,expected,operative(stage,z,c.selected_digest(expected)))
 if stage==100:require(QUEUE not in out and QUEUE not in r['changed_paths'],'Factual stage must not change QUEUE')

def entries(c,h,out):
 result=[]
 for name,b in sorted(out.items()):
  x={'path':name,'mode':'100644','type':'blob'}
  try:x['content']=b.decode()
  except UnicodeDecodeError:
   require(name.endswith('/five_centers.pdf') or name.endswith('/verification-package.zip'),'Unapproved binary');blob=h.api('git/blobs','POST',{'content':base64.b64encode(b).decode(),'encoding':'base64'});require(blob['sha']==c.byte_pin(b)['git_blob'],'Native binary blob mismatch');x['sha']=blob['sha']
  result.append(x)
 return result

def create(c,h,parent,out,expected,stage,stamp,dest,extra):
 _,z,_=external();pt=h.api('git/commits/'+parent)['tree']['sha'];tree=h.api('git/trees','POST',{'base_tree':pt,'tree':entries(c,h,out)});digest=c.selected_digest(expected);parents=[parent,HEAD] if stage==95 else [parent];co=h.api('git/commits','POST',{'message':operative(stage,z,digest),'tree':tree['sha'],'parents':parents});h.m.m.h.warm_selected_directories([pt,tree['sha']],expected);changed=sorted(name for name,x in expected.items() if h.lookup(pt,name)!=('100644','blob',x['git_blob']));r={'UTC':stamp,'phase':stage,'expected_main':parent,'parent_tree':pt,'tree':tree['sha'],'commit':co['sha'],'selected_files':expected,'selected_map_sha256':digest,'overlay_paths':sorted(out),'changed_paths':changed,'MAIN_moved':False,**extra};fresh(dest/'PREPARATION.json',encoded(r));verify_stage(c,h,r,expected,out,stage,z);require(h.api('git/ref/heads/main')['object']['sha']==parent,'MAIN advanced; preserve generation/retry fresh');print(json.dumps({'phase':stage,'expected_main':parent,'commit':r['commit'],'tree':r['tree'],'selected':len(expected),'changed':len(changed),'MAIN_moved':False}));return r

def generation(gen):require(re.fullmatch('[a-z0-9_]{1,48}',gen),'Use fresh bounded generation');return D/('generation_'+gen)

def prepare95(c,h,n,gen):
 prior,a,parent,g,z,t=baseline(c,h,True);stamp=now();d=derive95(c,h,n,parent,stamp);original(h,d);dest=generation(gen);dest.mkdir(exist_ok=False);out=out_for(c,h,d,95,parent,stamp);expected=selected(c,prior['selected_files'],out,95);create(c,h,parent,out,expected,95,stamp,dest,{'native_inventory':d['native_inventory'],'prior_publication_preparation':pin(PRIOR/'PUBLICATION_CHECKPOINT_PREPARATION.json')});original(h,d)

def reconstructed95(c,h,n,r):
 prior,a,main,g,z,t=baseline(c,h,False);require(r['prior_publication_preparation']==pin(PRIOR/'PUBLICATION_CHECKPOINT_PREPARATION.json'),'Original publication preparation changed');c.selected_current(h,r['expected_main'],prior['selected_files'],prior['tree']);d=derive95(c,h,n,r['expected_main'],r['UTC']);require(r['native_inventory']==d['native_inventory'],'Native95 inventory changed');out=out_for(c,h,d,95,r['expected_main'],r['UTC']);expected=selected(c,prior['selected_files'],out,95);verify_stage(c,h,r,expected,out,95,z);return d,out,expected,main

def current_bodies(c,h,main,expected,out):
 tree=c.selected_current(h,main,expected)
 for name,b in out.items():require(h.body_at(name,main)==b,'Fresh actual postimage body differs '+name)
 g,_,_=external()
 for name,x in g['package_files'].items():require(c.byte_pin(h.body_at(CASE+'publication_package_v2/'+name,main))==expected[CASE+'publication_package_v2/'+name],'Fresh reviewed package body differs '+name)
 return tree

def accept95(c,h,n,gen):
 r=read(generation(gen)/'PREPARATION.json');d,out,expected,main=reconstructed95(c,h,n,r);require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Two-parent merge not on MAIN');p=original(h,d,True);require(p['merge_commit_sha']==r['commit'],'GitHub reported a different merge commit; reconcile before accepting');tree=current_bodies(c,h,main,expected,out);g,z,t=external();result={'UTC':now(),'PR':193,'original_head':HEAD,'accepted':True,'status':'ACTUAL_ORIGINAL_HEAD_TWO_PARENT_MERGE_FULL_SCOPE_ALL_CURRENT_IDENTITIES_ACCEPTED','merge_commit':r['commit'],'parents':[r['expected_main'],HEAD],'tree':r['tree'],'actual_tree':tree,'main_observed':main,'preparation':pin(generation(gen)/'PREPARATION.json'),'generation':gen,'selected_files':len(expected),'selected_map_sha256':c.selected_digest(expected),'every_selected_identity_checked_at_actual_observed_MAIN':True,'DOI':z['doi'],'tracker_range':t['range'],'gate_sha256':pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'],'PR_closed':True,'PR_merged':True,'reported_merge_commit':p['merge_commit_sha'],'case_percent':95,'fully_completed_count':40,'published_count':24,'factual_completion_pending':True,'goal_complete':False};fresh(MERGE_RECEIPT,encoded(result));print(json.dumps(result))

def actual_merge(c,h,n):
 b=MERGE_RECEIPT.read_bytes();a=json.loads(b);r=read(generation(a['generation'])/'PREPARATION.json');d,out,expected,main=reconstructed95(c,h,n,r);g,z,t=external();require(a['PR']==193 and a['original_head']==HEAD and a['accepted'] is True and a['merge_commit']==r['commit'] and a['parents']==[r['expected_main'],HEAD] and a['tree']==r['tree'] and a['preparation']==pin(generation(a['generation'])/'PREPARATION.json') and a['selected_files']==len(expected) and a['selected_map_sha256']==c.selected_digest(expected) and a['DOI']==z['doi'] and a['tracker_range']==t['range'] and a['gate_sha256']==pin(A/'ROOT_PUBLICATION_GATE.json')['sha256'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] is True and utc(r['UTC'])<=utc(a['UTC'])<=utc(now()),'Actual merge receipt/map/facts differ');require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Original merge absent from MAIN');p=original(h,d,True);require(p['merge_commit_sha']==r['commit'],'Reported merge changed; reconcile before factual continuation');return a,r,d,out,expected,main

def derive100(c,n,d95,a,stamp):
 require(utc(a['UTC'])<=utc(stamp)<=utc(now()),'Factual100 stamp outside actual merge/current interval');d=n.derive_phase100(phase95=d95,merge_acceptance={'receipt_bytes':MERGE_RECEIPT.read_bytes(),'receipt_pin':pin(MERGE_RECEIPT)},factual_utc=stamp);require(d['phase']==100 and set(d['native_files'])==set(d95['native_files']) and d['native_inventory']=={name:c.byte_pin(b) for name,b in sorted(d['native_files'].items())},'Native100 exact inventory differs');changed={name for name in d['native_files'] if d['native_files'][name]!=d95['native_files'][name]};require(changed<=FACTUAL_NATIVE,'Factual100 changed scientific/original/published bytes');return d

def prepare100(c,h,n,gen):
 a,m,d95,o95,merged,parent=actual_merge(c,h,n);c.selected_current(h,parent,merged,m['tree']);stamp=now();d=derive100(c,n,d95,a,stamp);dest=generation(gen);dest.mkdir(exist_ok=False);out=out_for(c,h,d,100,parent,stamp,a);expected=selected(c,merged,out,100);create(c,h,parent,out,expected,100,stamp,dest,{'native_inventory':d['native_inventory'],'original_merge_generation':a['generation'],'actual_merge_receipt':pin(MERGE_RECEIPT)})

def accept100(c,h,n,gen):
 r=read(generation(gen)/'PREPARATION.json');a,m,d95,o95,merged,main=actual_merge(c,h,n);require(r['actual_merge_receipt']==pin(MERGE_RECEIPT) and r['original_merge_generation']==a['generation'],'Factual preparation actual merge binding differs');c.selected_current(h,r['expected_main'],merged,m['tree']);d=derive100(c,n,d95,a,r['UTC']);require(r['native_inventory']==d['native_inventory'],'Native100 inventory changed');out=out_for(c,h,d,100,r['expected_main'],r['UTC'],a);expected=selected(c,merged,out,100);g,z,t=external();verify_stage(c,h,r,expected,out,100,z);require(h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'],'Factual100 commit absent from MAIN');tree=current_bodies(c,h,main,expected,out);original(h,d95,True);result={'UTC':now(),'PR':193,'original_head':HEAD,'accepted':True,'status':'ACTUAL_PR193_FACTUAL100_FULL_PARENT_SCOPE_COMBINED_CURRENT_IDENTITIES_ACCEPTED','factual_commit':r['commit'],'sole_parent':r['expected_main'],'original_merge_commit':m['commit'],'main_observed':main,'actual_tree':tree,'selected_files':len(expected),'selected_map_sha256':c.selected_digest(expected),'every_selected_identity_checked_at_actual_observed_MAIN':True,'DOI':z['doi'],'tracker_range':t['range'],'fully_completed_count':41,'published_count':25,'last_completed_PR':193,'case_percent':100,'actual_original_PR_merged':True,'actual_factual_MAIN_accepted':True,'next_own_actual_receipt_native_reconciliation_checkpoint_required':True,'conditional_next_numeric_intake_cursor':194,'next_status_only_intake_authorized_after_own_receipt_checkpoint':True,'goal_complete':False};fresh(A/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json',encoded(result));print(json.dumps(result))

if __name__=='__main__':
 require(sys.dont_write_bytecode,'Use Python -B');require(len(sys.argv)==3 and sys.argv[1] in ['prepare95','accept95','prepare100','accept100'],'Usage: complete_main193.py prepare95|accept95|prepare100|accept100 fresh_generation');c,h,n=load();{'prepare95':prepare95,'accept95':accept95,'prepare100':prepare100,'accept100':accept100}[sys.argv[1]](c,h,n,sys.argv[2])
