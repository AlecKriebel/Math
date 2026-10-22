"""PR203 source/math45 checkpoint; native objects only, never a ref move."""
from pathlib import Path
import datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent;P=A.parent.parent
PREFIX='draft_pr_publication_program_20260930/';CASE=PREFIX+'audits/pr203_5100011/';PREVIOUS=PREFIX+'audits/pr201_5100014/'
PRIOR=P/'audits/pr201_5100014/publication_lifecycle_01/completion100_01'
HEAD='8edca9d773c085adb4ed0611357a7a2957e3395d';Q='unsolved_math_prioritization/QUEUE.md'
MUTABLE={PREFIX+x for x in ['CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md']}
def read(p):return json.loads(p.read_bytes())
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def save(p,b):
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
def load():
 f=P/'audits/pr201_5100014/publication_lifecycle_01/finish201.py';s=importlib.util.spec_from_file_location('completed201_lowlevel',f);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);c,h,rv,n=v.load();h.m.TREE_CACHE_PATH=A/'MATH_PRIVATE_TREE_CACHE.json';return c,h,rv
def baseline(c):
 r=read(PRIOR/'PREPARATION.json');a=read(PRIOR/'ACCEPTANCE.json');x=read(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
 assert pin((PRIOR/'ACCEPTANCE.json').read_bytes())=={'bytes':1636,'sha256':'9d6c23ec88334eb88553dfe7f70aa629bf36143a678fbaa21591c89fcb541606'}
 assert a['accepted'] and a['completion_metadata_accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN']
 assert r['commit']==a['checkpoint_commit']=='0c0ef219dd5aa4547ad7ee47ac1ab5b08ca232f0' and len(r['selected_files'])==a['selected_files']==2960
 assert r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='899483aceb752476b19db7be18c13ac484907380da6b2cefe7fbad3b597e53f6'
 assert pin((PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file']=={'bytes':886374,'sha256':'6161ab215c25d304128820245432bc8bb1b257f2eaccf1d81367bd70dac13899'}
 assert x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])
 assert (a['fully_completed_count'],a['published_count'],a['last_completed_PR'],a['advance_to_next_PR_authorized_now'])==(45,29,201,True)
 return {**r,'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}
def original(h):
 p=h.api('pulls/203');assert p['head']['sha']==HEAD and p['state']=='open' and p['draft'] is True and p['merged'] is False
 assert p['created_at']==p['updated_at']=='2026-10-01T05:24:27Z'
 return p
def queue_reconcile(c,h,base,parent):
 old=h.body_at(Q,base['commit']);new=h.body_at(Q,parent);assert c.byte_pin(old)==base['selected_files'][Q]
 protected={n.split('/')[2] for n in base['selected_files'] if n.startswith('unsolved_math_prioritization/attempts/')};protected.add('5100011')
 ol=old.splitlines(keepends=True);nl=new.splitlines(keepends=True);assert len(ol)==len(nl);changes=[]
 for i,(x,y) in enumerate(zip(ol,nl)):
  if x==y:continue
  def ident(b):
   z=b.decode().split('|');assert len(z)==14 and z[1].strip().isdigit();return z[2].strip().split(' / ')[0]
  pid=ident(x);assert ident(y)==pid and pid not in protected;changes.append({'one_based_line':i+1,'foreign_problem_id':pid,'old_line':pin(x),'new_line':pin(y)})
 assert [x for x in ol if b'| 5100011 / AMR-050-0011 |' in x]==[x for x in nl if b'| 5100011 / AMR-050-0011 |' in x]
 return {**base['selected_files'],Q:c.byte_pin(new)},{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_actual_commit':base['commit'],'observed_actual_MAIN':parent,'scope':'Authenticate concurrent foreign QUEUE bytes only, without mathematical endorsement. Own checkpoint never writes QUEUE.','old_QUEUE':c.byte_pin(old),'current_QUEUE':c.byte_pin(new),'protected_own_native_problem_ids':sorted(protected),'foreign_changed_rows':changes,'all_other_QUEUE_bytes_identical':True,'all_protected_own_QUEUE_rows_identical':True}
def overlay(h,parent,stamp):
 gp=A/'ROOT_MATHEMATICAL_GATE_01.json';assert pin(gp.read_bytes())=={'bytes':16740,'sha256':'15190ef47b165ff03b67a9808a45cdb9a38c40c37399c01f79cc8bbb75a2e85a'}
 g=read(gp);assert g['source_and_mathematical_gate_accepted'] and not g['priority_clearance'] and not g['publication_ready'] and g['case_percent']==45;out={}
 def add(rel,x=None):
  f=A/rel;assert not Path(rel).is_absolute() and '..' not in Path(rel).parts and f.is_file() and not f.is_symlink() and f.stat().st_mode&0o777==0o444,rel
  b=f.read_bytes()
  if x is not None:assert pin(b)==x,rel
  out[CASE+rel]=b
 for rel,x in g['safe_files'].items():add(rel,x)
 add(gp.name);add('ROOT_MATHEMATICAL_ACCEPTANCE_01.json',{'bytes':1425,'sha256':'0fb03032e844ded73ad98a755c747aeeb766ff1606b7411fda5bee014255bbda'})
 add('science_checkpoint_01/checkpoint_math203.py')
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json','FOREIGN_QUEUE_RECONCILIATION.json']:
  f=PRIOR/name;assert f.stat().st_mode&0o777==0o444;out[PREVIOUS+'publication_lifecycle_01/completion100_01/'+name]=f.read_bytes()
 intake=P/'ordered_intakes_after_PR201_20261016'
 for name in ['status_only_intake.py','RESEARCH_LOG.md','PR202_ORIGINAL_STATUS_INTAKE.json','PR203_ORIGINAL_STATUS_INTAKE.json']:
  f=intake/name;assert f.is_file() and not f.is_symlink() and f.stat().st_mode&0o777==0o444
  out[PREFIX+'ordered_intakes_after_PR201_20261016/'+name]=f.read_bytes()
 assert out[PREFIX+'ordered_intakes_after_PR201_20261016/PR203_ORIGINAL_STATUS_INTAKE.json']==out[CASE+'ORIGINAL_STATUS_INTAKE.json']
 custody=read(A/'ORIGINAL_SUBMISSION_CUSTODY.json');assert custody['original_head']==HEAD and custody['original_QUEUE_status']=='claimed_solved' and len(custody['files'])==18
 for rel,x in custody['files'].items():
  b=out[CASE+'original_submitted_head/'+rel];assert pin(b)=={k:x[k] for k in ['bytes','sha256']} and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
 families=[x['manifest'].split('/')[0] for x in g['new_family_audits']]
 status='SCOPED_MATHEMATICS_AND_SOURCE_ACCEPTED_DEEP_PRIORITY_ACTIVE'
 remain='Finish bounded deep exact-target and classical/general-theorem priority audits, determine honest contribution/editorial scope, then manuscript/package and NEW whole-package review-repair loop. Exact Zenodo publication/tracker, original-HEAD-safe merge and actual factual completion remain before204.'
 claim=g['strongest_verified_claim'];warning='arXiv2004.12497v11 Table3p6 / journal Table3p346 k203,a: signed original A times arbitrary-fixed-M original-side pedal area, N0mod4. The printed table does not say least/primitive. Explicit least-period theorem verified; unrestricted repeated-list interpretation false, with exact doubled-6 nominal12 counterexample. Dated question marks are not present-day openness or priority.'
 case={'UTC':stamp,'PR':203,'problem_id':5100011,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_effort':'Original turn records report two substantive author turns (2/5), three precreation commits; actual model/reasoning effort unverified. Later audits are not original author effort.','original_QUEUE_effort_cell':'2/5','status':status,'case_percent':45,'exact_claim':claim,'source_provenance_warning':warning,'original_archive_files':18,'original_native_bytes':59989,'independent_mathematical_families':families,'independent_mathematical_families_active':False,'independent_mathematical_families_complete':4,'independent_family_statuses':g['new_family_audits'],'direct_Euclidean_universal_route':'PARTIAL/BLOCKED at A*B0 and A*C for N>=8; complete N4 and exact boundary controls; route35percent, audit100percent','mathematical_clearance':True,'mathematical_result_valid':True,'source_contract_clearance':True,'mathematical_gate':'ROOT_MATHEMATICAL_GATE_01.json','original_optimized_checker_enforcement':0,'original_optimized_false_identities_accepted':True,'Root_fresh_exact_controls_each_mode':282,'priority_audit_active':True,'priority_audit_complete':False,'priority_clearance':False,'historical_novelty_or_firstness_established':False,'independent_discovery_certified':False,'publication_ready':False,'whole_publication_package_reviews_complete':False,'actual_Zenodo_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'actual_factual_MAIN_accepted':False,'completed':False,'fully_completed_count':45,'published_count':29,'last_completed_PR':201,'remaining_required_steps':remain,'next_numeric_intake_cursor':203,'conditional_next_numeric_intake_cursor':204,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
 out[CASE+'CURRENT_CASE_STATUS.json']=enc(case)
 log=(A/'RESEARCH_LOG_INITIAL.md').read_bytes()+('\n'+stamp+' — Math/source checkpoint45%: original18 files59989B remain unchanged. Source-first independent plans and four completed adversarial family audits accepted by Root; full all-N analytic and flag-curve mechanisms verified. Direct Euclidean route remains blocked at35% for general N, with exact N4 proof; physical computations are noninterval diagnostics. Source table omits least period; unrestricted repeated list false. Original ordinary replay bytes match; -O removes assertions while advertised counts survive and false identities pass. Fresh exception checks and Root282exact checks per mode pass. Deep priority active; no novelty, publication or next-PR authority.45completed/29published,last201.\n').encode()
 out[CASE+'RESEARCH_LOG.md']=log
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_completed'],p['advance_to_next_PR_authorized_now'])==(201,45,29,201,True,True)
 retired=[k for k in p if k.startswith(('current_','next_','conditional_','program_snapshot_')) or k in ['advance_to_next_PR_authorized_now','remaining_current_step','next_step','latest_ordered_intake_record','latest_ordered_intake_records']]
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':201,'prior_phase':'actual_completed_before203_original_intake','values':{k:p[k] for k in retired}})
 for k in retired:p.pop(k,None)
 skip=read(intake/'PR202_ORIGINAL_STATUS_INTAKE.json');assert not skip['eligible'] and skip['original_QUEUE_status']=='queued'
 p['skipped_since_last_completion']=[{'PR':202,'original_QUEUE_status':'queued','action':'STATUS_ONLY_SKIPPED_UNTOUCHED','record':'ordered_intakes_after_PR201_20261016/PR202_ORIGINAL_STATUS_INTAKE.json'}]
 p.update(UTC=stamp,updated_UTC=stamp,current_PR=203,current_problem_id=5100011,current_original_head=HEAD,current_original_QUEUE_status='claimed_solved',current_original_budget=case['original_effort'],current_PR_workflow_percent=45,current_workflow_estimate_percent=45,current_status=status,current_completed=False,current_closed=False,current_original_PR_state='open',current_original_PR_merged=False,current_original_PR_open_draft=True,current_mathematical_clearance=True,current_mathematics_cleared=True,current_mathematical_result_valid=True,current_independent_mathematical_audit_active=False,current_independent_mathematical_audit_families=4,current_independent_mathematical_audit_families_complete=4,current_independent_mathematical_audit_names=families,current_independent_family_statuses=g['new_family_audits'],current_direct_Euclidean_general_route=case['direct_Euclidean_universal_route'],current_source_contract_clearance=True,current_source_provenance_warning=warning,current_mathematical_gate='audits/pr203_5100011/ROOT_MATHEMATICAL_GATE_01.json',current_priority_audit_active=True,current_priority_audit_families=['pr203_priority_exact_target_01','pr203_priority_classical_01','Root_exact_and_general_primary_checks'],current_priority_clearance=False,current_priority_audit_complete=False,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_publication_ready=False,current_publication_package=None,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=False,current_Zenodo_published=False,current_DOI=None,current_tracker_updated=False,current_tracker_range=None,current_actual_factual_checkpoint_accepted=False,current_record='audits/pr203_5100011/CURRENT_CASE_STATUS.json',current_exact_claim=claim,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,next_numeric_intake_cursor=203,conditional_next_numeric_intake_cursor=204,advance_to_next_PR_authorized_now=False,next_intake_requires_actual_completion_receipt=True,next_intake_requires_actual_completed_PR=203,next_status_only_intake_performed=False,latest_ordered_intake_record='ordered_intakes_after_PR201_20261016/PR203_ORIGINAL_STATUS_INTAKE.json',latest_ordered_intake_records=['ordered_intakes_after_PR201_20261016/PR202_ORIGINAL_STATUS_INTAKE.json','ordered_intakes_after_PR201_20261016/PR203_ORIGINAL_STATUS_INTAKE.json'],persistent_goal_complete=False,goal_work_continuing=True,program_snapshot_semantics='PR201 actually completed45completed/29published,last201. PR202 original queued status-only skipped untouched. PR203 original claimed_solved2of5/18-file custody frozen; mathematical/source gate accepted for explicit leastN0mod4 signed original-side every-M theorem. Unrestricted repeated-list reading false. Four audit families completed with direct Euclidean general route honestly partial; original -O assertion failure disclosed. Deep priority active; no novelty/publication/merge clearance,cursor203/conditional204/advancefalse.',program_snapshot_authority_condition='Math45 postimage effective only after actual true-parent/fullforeignscope/everyselectedidentity acceptance. No priority, publication, merge or next-intake authority.')
 out[PREFIX+'CURRENT_PROGRESS.json']=enc(p)
 note='\n'+stamp+' — PR203 math45%: original claimed_solved2/5, HEAD8edca9d773c085adb4ed0611357a7a2957e3395d and18files59989B archived unchanged. Four NEW distinct mathematical families plus Root proof/source/code/282exact-controls-each-mode checks accepted. Explicit primitive leastN0mod4 signed original-side-line every-fixed-M theorem verified; source table does not print least and doubled6 nominal12 gives exact false-extension control. General direct Euclidean route partial35%, not an extra universal proof. Original unchanged ordinary replays match; -O advertises all counts but enforces0 and accepts deliberately false identities; fresh exception controls reject in both modes. Deep priority active; no firstness/publication clearance. PR202 queued status-only skipped untouched.45completed/29published,last201,cursor203/conditional204/advancefalse; goal active.\n'
 for name in ['CURRENT_PROGRESS.md','RESEARCH_LOG.md']:out[PREFIX+name]=h.body_at(PREFIX+name,parent)+note.encode()
 return out
def selected(c,b,out):
 for k,z in out.items():
  assert k.startswith(CASE) or k in MUTABLE or k.startswith(PREVIOUS+'publication_lifecycle_01/completion100_01/') or k.startswith(PREFIX+'ordered_intakes_after_PR201_20261016/'),k
  if k in b and k not in MUTABLE:assert c.byte_pin(z)==b[k],k
 assert Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in out)
 return {**b,**{k:c.byte_pin(z) for k,z in out.items()}}
def message(d):return 'Record PR203 scoped mathematics and source gate45; deep priority active\n\nLeast N0mod4 signed original-side pedal product for every fixed M verified. Repeated-list limitation and optimized-checker enforcement defect disclosed.45completed/29published,last201;202 queued skipped untouched. No novelty/publication clearance.\nPR203 mathematical selected-map SHA256: '+d
def verify(c,h,r,ex):
 assert r['selected_files']==ex and r['selected_map_sha256']==c.selected_digest(ex)
 co=h.api('git/commits/'+r['commit']);assert [x['sha'] for x in co['parents']]==[r['expected_main']] and co['tree']['sha']==r['tree'] and co['message']==message(c.selected_digest(ex))
 assert h.api('git/commits/'+r['expected_main'])['tree']['sha']==r['parent_tree'];h.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],ex)
 for k,x in ex.items():assert h.lookup(r['tree'],k)==('100644','blob',x['git_blob']),k
 changes={k for k,x in ex.items() if h.lookup(r['parent_tree'],k)!=('100644','blob',x['git_blob'])}
 assert changes==h.changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']) and changes<=set(r['overlay_paths'])
 assert Q not in changes and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in changes)
def run(c,h,rv,mode,gen):
 base=baseline(c);dest=D/gen
 if mode=='prepare':
  parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=queue_reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);original(h)
  assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead']
  stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.mkdir();save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',enc(ack))
 else:
  r=read(dest/'PREPARATION.json');ack=read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');parent=r['expected_main'];stamp=r['UTC'];pt=r['parent_tree'];inherited={**base['selected_files'],Q:ack['current_QUEUE']}
 out=overlay(h,parent,stamp);out[CASE+'science_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=selected(c,inherited,out)
 if mode=='prepare':
  tree=h.api('git/trees','POST',{'base_tree':pt,'tree':[{'path':k,'mode':'100644','type':'blob','content':z.decode()} for k,z in sorted(out.items())]})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex)
  r={'UTC':stamp,'PR':203,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in ex.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'MAIN_moved':False}
  save(dest/'PREPARATION.json',enc(r))
 verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha']
 if mode=='prepare':
  pre={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_trueparent_fullforeignscope_everyselectedidentity_verified':True,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'no_QUEUE_native_or_PR_mutation':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':False,'publication_ready':False,'case_percent':45};save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',enc(pre));print(json.dumps({k:r[k] for k in ['expected_main','commit','tree','selected_map_sha256']}|{'observed_main':main,'selected':len(ex),'changed':len(r['changed_paths'])}));return
 assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead']
 actual,post=queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);original(h)
 for k,z in out.items():assert c.byte_pin(z)==ex[k] and h.lookup(tree,k)==('100644','blob',ex[k]['git_blob'])
 body=enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
 accepted={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':203,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':False,'priority_audit_active':True,'publication_ready':False,'case_percent':45,'fully_completed_count':45,'published_count':29,'last_completed_PR':201,'next_numeric_intake_cursor':203,'advance_to_next_PR_authorized_now':False,'goal_complete':False}
 save(dest/'ACCEPTANCE.json',enc(accepted));print(json.dumps(accepted))
if __name__=='__main__':
 assert sys.dont_write_bytecode and not sys.flags.optimize
 c,h,rv=load();run(c,h,rv,sys.argv[1],sys.argv[2])
