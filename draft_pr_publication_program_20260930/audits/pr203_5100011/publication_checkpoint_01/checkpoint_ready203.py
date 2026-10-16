"""PR203 actual readiness checkpoint; requires final Root entire-package gate. No ref mutation."""
from pathlib import Path
import datetime,importlib.util,json,sys,atexit
if sys.flags.optimize:raise RuntimeError('Publication operations require ordinary Python; optimization removes assertions')
D=Path(__file__).resolve().parent;A=D.parent
sp=importlib.util.spec_from_file_location('math203_native_primitives',A/'science_checkpoint_01/checkpoint_math203.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
Q=v.Q;CASE=v.CASE;PREFIX=v.PREFIX;HEAD=v.HEAD
PRIOR=A/'priority_checkpoint_01/review80_01'
def load():
 c,h,rv=v.load();atexit.unregister(h.m.persist_authenticated_tree_cache);return c,h,rv
def baseline(c):
 r=v.read(PRIOR/'PREPARATION.json');a=v.read(PRIOR/'ACCEPTANCE.json');x=v.read(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
 assert a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and r['commit']==a['checkpoint_commit']=='b4f36bd65af808c3ef3c6d70bc759ede9566ac9a'
 assert len(r['selected_files'])==a['selected_files']==3353 and r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='12f1b3b96b860fa778f88d6e6f07f71ca9d3a0bcf0ff24a4e15f2077106adb30'
 assert v.pin((PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file']=={'bytes':1007043,'sha256':'f0cc4c75865992145337fdc0ed5a08e578391328f72afbb21105f9229f73f21c'}
 assert x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])
 return {**r,'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}
def overlay(h,parent,stamp):
 gp=A/'ROOT_PUBLICATION_GATE_01.json';g=v.read(gp)
 assert gp.stat().st_mode&0o777==0o444 and g['publication_ready_gate_accepted'] and g['whole_package_review_loop_complete'] and not g['historical_priority_established']
 assert len(g['whole_package_review_events'])>=2 and g['whole_package_review_events'][-1]['verdict']=='CLEANPASS' and g['whole_package_review_events'][-1]['reviewed_package_seal']==g['package_seal'] and g['fresh_final_review_after_documented_editorial_repairs']
 out={}
 def add(rel,x=None):
  assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
  p=A/rel;assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444
  b=p.read_bytes()
  if x is not None:assert v.pin(b)==x,rel
  out[CASE+rel]=b
 add(gp.name)
 for rel,x in g['package_safe_files'].items():add(g['package']+'/'+rel,x)
 for event in g['whole_package_review_events']:
  for rel,x in event['safe_files'].items():add(event['directory']+'/'+rel,x)
  add(event['Root_acceptance_file'],event['Root_acceptance_pin'])
 for rel,x in g['other_safe_files'].items():add(rel,x)
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json','FOREIGN_QUEUE_RECONCILIATION.json','LOCAL_GLOBAL_FIVE_SYNC.json']:add('priority_checkpoint_01/review80_01/'+name)
 add('publication_checkpoint_01/checkpoint_ready203.py')
 status='TWO_NEW_ENTIRE_PACKAGE_REVIEWS_CLEAN_ATTRIBUTED_ORIGINAL_PEDAL_FLAG_PROOF_READY'
 remain='Publish exact reviewed3-file set using repository Zenodo kit, verify metadata/public SHA256/DOI resolver, append and read back GWS tracker, original-HEAD-safe merge, actual factual and completion checkpoints before204.'
 case=json.loads(h.body_at(CASE+'CURRENT_CASE_STATUS.json',parent));assert (case['PR'],case['case_percent'],case['original_head'])==(203,80,HEAD)
 case.update(UTC=stamp,status=status,case_percent=90,publication_ready=True,whole_publication_package_reviews_complete=True,NEW_whole_package_review_active=False,NEW_whole_package_reviews_completed=len(g['whole_package_review_events']),whole_package_review_loop_complete=True,whole_package_review_events=g['whole_package_review_events'],active_whole_package_adversary=None,publication_gate=gp.name,publication_package=g['package'],publication_package_seal=g['package_seal'],historical_priority_established=False,historical_novelty_or_firstness_established=False,remaining_required_steps=remain)
 out[CASE+'CURRENT_CASE_STATUS.json']=v.enc(case)
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(203,45,29,201,80)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':203,'prior_phase':80,'values':{k:z for k,z in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=90,current_workflow_estimate_percent=90,current_publication_ready=True,current_publication_package=g['package'],current_publication_package_seal=g['package_seal'],current_publication_package_reviews_complete=True,current_NEW_whole_publication_package_reviews_completed=len(g['whole_package_review_events']),current_NEW_whole_publication_package_review_active=False,current_active_whole_package_adversary=None,current_whole_package_review_loop_complete=True,current_whole_package_review_events=g['whole_package_review_events'],current_publication_gate='audits/pr203_5100011/'+gp.name,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,current_source_provenance_warning='Signed original-side pedal product for proper confocal ellipses, explicit leastN0mod4, every fixed finite realM, primitive stars/reversal/zero/negative. Exact Ferudun DOI23400541 theorem/strategy and classical methods credited. Table does not print least period; nominal repeated-list reading false. Object dates do not certify firstness or independence.',program_snapshot_semantics='PR203 attributed incidence-curve proof ready after two NEW entire-package reviews, first CLEANPASS and optional clarifications in v2 followed by NEW complete final review CLEANPASS. Root proof/source/code/ZIP/metadata/visual acceptance complete. Exact contemporary theorem and classical methods credited; no novelty/firstness/independence certificate.45completed/29published,last201,cursor203/advancefalse.',program_snapshot_authority_condition='Ready90 postimage effective only after actual trueparent/fullforeignscope/everyselectedidentity acceptance. Actual Zenodo/tracker/merge/completion remain; no204 authority.')
 assert not p['current_completed'] and not p['advance_to_next_PR_authorized_now'] and not p['current_Zenodo_published'];out[PREFIX+'CURRENT_PROGRESS.json']=v.enc(p)
 note='\n'+stamp+' — PR203 ready90%: FIRST NEW entire-v1 review CLEANPASS without substantive issue. Two optional P3 clarity improvements propagated into v2; SECOND NEW reviewer independently audited entire final v2 from scratch and returned CLEANPASS. Root accepted exact proof/source/metadata/custody/portable enforcement and all7 final PDF pages; final package and exact kit3-file set pinned. Exact Ferudun theorem/method and classical sources credited, chronology qualified; no novelty/firstness/certified independence. Actual DOI/tracker/original-HEAD-safe merge/factual completion remain.45completed/29published,last201,cursor203/advancefalse; goal active.\n'
 for rel in [CASE+'RESEARCH_LOG.md',PREFIX+'CURRENT_PROGRESS.md',PREFIX+'RESEARCH_LOG.md']:out[rel]=h.body_at(rel,parent)+note.encode()
 return out
def selected(c,b,out):
 for k,z in out.items():
  assert k.startswith(CASE) or k in v.MUTABLE,k
  if k in b and k not in v.MUTABLE and k not in {CASE+'CURRENT_CASE_STATUS.json',CASE+'RESEARCH_LOG.md'}:assert c.byte_pin(z)==b[k],k
 assert Q not in out and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in out)
 return {**b,**{k:c.byte_pin(z) for k,z in out.items()}}
def entries(c,h,out):
 import base64
 result=[]
 for k,b in sorted(out.items()):
  if k.endswith(('.pdf','.zip')):
   sha=h.api('git/blobs','POST',{'encoding':'base64','content':base64.b64encode(b).decode()})['sha'];assert sha==c.byte_pin(b)['git_blob'];result.append({'path':k,'mode':'100644','type':'blob','sha':sha})
  else:result.append({'path':k,'mode':'100644','type':'blob','content':b.decode()})
 return result
def message(d):return 'PR203 ready90: attributed original-side pedal flag-curve proof\n\nTwo NEW entire-package reviews clean, exact contemporary theorem and classical methods credited; no firstness/independence certificate. Publication remains pending.\nPR203 selected-map SHA256: '+d
v.message=message
def run(c,h,rv,mode,gen):
 base=baseline(c);dest=D/gen
 if mode=='prepare':
  parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=v.queue_reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);v.original(h)
  assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead']
  stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.mkdir();v.save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',v.enc(ack))
 else:
  r=v.read(dest/'PREPARATION.json');ack=v.read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');parent=r['expected_main'];stamp=r['UTC'];pt=r['parent_tree'];inherited={**base['selected_files'],Q:ack['current_QUEUE']}
 out=overlay(h,parent,stamp);out[CASE+'publication_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=selected(c,inherited,out)
 if mode=='prepare':
  tree=h.api('git/trees','POST',{'base_tree':pt,'tree':entries(c,h,out)})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex)
  r={'UTC':stamp,'PR':203,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in ex.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};v.save(dest/'PREPARATION.json',v.enc(r))
 v.verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha']
 if mode=='prepare':
  pre={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_trueparent_fullforeignscope_everyselectedidentity_verified':True,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'no_QUEUE_native_or_PR_mutation':True,'mathematical_clearance':True,'source_contract_clearance':True,'bounded_priority_audit_complete':True,'qualified_attributed_note_editorially_cleared':True,'historical_firstness_independence_certified':False,'publication_ready':True,'actual_publication_verified':False,'case_percent':90};v.save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',v.enc(pre));print(json.dumps({k:r[k] for k in ['expected_main','commit','tree','selected_map_sha256']}|{'observed_main':main,'selected':len(ex),'changed':len(r['changed_paths'])}));return
 assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];actual,post=v.queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);v.original(h)
 for k,z in out.items():assert c.byte_pin(z)==ex[k] and h.lookup(tree,k)==('100644','blob',ex[k]['git_blob'])
 body=v.enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});v.save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
 accepted={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':203,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':v.pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':True,'bounded_priority_audit_complete':True,'qualified_attributed_note_editorially_cleared':True,'historical_firstness_independence_established':False,'publication_ready':True,'actual_publication_verified':False,'case_percent':90,'fully_completed_count':45,'published_count':29,'last_completed_PR':201,'next_numeric_intake_cursor':203,'advance_to_next_PR_authorized_now':False,'goal_complete':False};v.save(dest/'ACCEPTANCE.json',v.enc(accepted));print(json.dumps(accepted))
m=v
tree_entries=entries
if __name__=='__main__':
 assert sys.dont_write_bytecode and not sys.flags.optimize
 c,h,rv=load();run(c,h,rv,sys.argv[1],sys.argv[2])

