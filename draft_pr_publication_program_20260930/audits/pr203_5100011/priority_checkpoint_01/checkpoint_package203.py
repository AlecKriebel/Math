"""PR203 sealed package75 checkpoint. FIRST entire-package review active; no ref mutation."""
from pathlib import Path
import datetime,importlib.util,json,sys,atexit
D=Path(__file__).resolve().parent;A=D.parent
sp=importlib.util.spec_from_file_location('math203_native_primitives',A/'science_checkpoint_01/checkpoint_math203.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
Q=v.Q;CASE=v.CASE;PREFIX=v.PREFIX;HEAD=v.HEAD
PRIOR=A/'priority_checkpoint_01/priority60_01'
def load():
 c,h,rv=v.load();atexit.unregister(h.m.persist_authenticated_tree_cache);return c,h,rv
def baseline(c):
 r=v.read(PRIOR/'PREPARATION.json');a=v.read(PRIOR/'ACCEPTANCE.json');x=v.read(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
 assert a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and r['commit']==a['checkpoint_commit']=='f82822ecd2864931efc23ca64e09192c4e69108b'
 assert len(r['selected_files'])==a['selected_files']==3078 and r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='9b08e457b61a9611821d8c4b457ee0e065c8ec06dd4741ed9fdc568134c5f88a'
 assert v.pin((PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file']=={'bytes':920286,'sha256':'ed1e6fd036356a38b5967cd7bcfff1260e3acf37440a4553d2c9555cd5878c43'}
 assert x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])
 return {**r,'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}
def overlay(h,parent,stamp):
 P=A/'publication_package_v1';sp=P/'PACKAGE_SEAL.json'
 assert v.pin(sp.read_bytes())=={'bytes':21091,'sha256':'d8bf1dbb37175a2b8799f81564d2f742f04f942628d6463f32af30adb0db0bd6'}
 g=v.read(sp);assert not g['publication_ready'] and not g['whole_package_review_loop_complete'];out={}
 for rel,x in g['package_files_excluding_this_seal'].items():
  q=P/rel;b=q.read_bytes();assert v.pin(b)==x and not q.is_symlink() and q.stat().st_mode&0o777==0o444
  out[CASE+'publication_package_v1/'+rel]=b
 out[CASE+'publication_package_v1/PACKAGE_SEAL.json']=sp.read_bytes()
 def add(rel):
  q=A/rel;assert q.is_file() and not q.is_symlink() and q.stat().st_mode&0o777==0o444;out[CASE+rel]=q.read_bytes()
 for rel in ['ROOT_PDF_VISUAL_QA_V1.json','ROOT_ZENODO_KIT_CHECK_V1.json','priority_checkpoint_01/checkpoint_package203.py']:add(rel)
 for q in sorted((A/'portable_reproduction_v1').iterdir()):
  if q.is_file():add(str(q.relative_to(A)))
 for name in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json','FOREIGN_QUEUE_RECONCILIATION.json','LOCAL_GLOBAL_FIVE_SYNC.json']:add('priority_checkpoint_01/priority60_01/'+name)
 status='ATTRIBUTED_COMPLETE_PACKAGE_SEALED_FIRST_NEW_WHOLE_PACKAGE_ADVERSARY_ACTIVE'
 remain='Complete first NEW entire-package adversary audit; repair every issue globally, then NEW independent entire-package audit and repeat until clean. Only then exact Zenodo publication/tracker/original-HEAD-safe merge and factual completion before204.'
 case=json.loads(h.body_at(CASE+'CURRENT_CASE_STATUS.json',parent));assert (case['PR'],case['case_percent'],case['original_head'])==(203,60,HEAD)
 case.update(UTC=stamp,status=status,case_percent=75,publication_package='publication_package_v1',publication_package_seal=v.pin(sp.read_bytes()),publication_ready=False,whole_publication_package_reviews_complete=False,NEW_whole_package_review_active=True,NEW_whole_package_reviews_completed=0,whole_package_review_loop_complete=False,active_whole_package_adversary='pr203_whole_package_adversary_01',remaining_required_steps=remain)
 out[CASE+'CURRENT_CASE_STATUS.json']=v.enc(case)
 p=json.loads(h.body_at(PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(203,45,29,201,60)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':203,'prior_phase':60,'values':{k:z for k,z in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=75,current_workflow_estimate_percent=75,current_publication_package='publication_package_v1',current_publication_package_seal=v.pin(sp.read_bytes()),current_publication_ready=False,current_publication_package_reviews_complete=False,current_NEW_whole_publication_package_reviews_completed=0,current_NEW_whole_publication_package_review_active=True,current_active_whole_package_adversary='pr203_whole_package_adversary_01',current_whole_package_review_loop_complete=False,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,program_snapshot_semantics='PR203 attributed incidence-curve note and complete107-entry verification ZIP sealed;7-pagePDF visually checked, exact portable normal/O/mutation/guard/original ordinary byte replays and local Zenodo-kit check passed. Exact Ferudun theorem/classical methods credited; no novelty/firstness/independence certificate. FIRST NEW whole-package adversary active; mandatory fresh review loop pending.45completed/29published,last201,cursor203/advancefalse.',program_snapshot_authority_condition='Package75 postimage effective only after actual trueparent/fullforeignscope/everyselectedidentity acceptance. Package is review-ready, not publication-ready; no deposit, tracker, merge or204 authority.')
 assert not p['current_completed'] and not p['advance_to_next_PR_authorized_now'];out[PREFIX+'CURRENT_PROGRESS.json']=v.enc(p)
 note='\n'+stamp+' — PR203 package75%: publication_package_v1 sealed with7-pagePDF87468B,TeX22349B,verificationZIP232392B/107entries/106manifestpins, all18 original files, exact attributed metadata and local-kit check. Root final all7pages QA and portable default ordinary/O, true wrong8to9 coefficient rejection, guardfail normal/O, unchanged original ordinary byte replays accepted. Exact contemporary theorem/classical methods prominently credited, chronology qualified, signed leastN0mod4 scope retained. FIRST NEW entire-package adversary pr203_whole_package_adversary_01 active; repair/fresh-independent-entire-review loop remains. No publication readiness or actual DOI/tracker/merge.45completed/29published,last201,cursor203/advancefalse; goal active.\n'
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
def message(d):return 'PR203 attributed package75 sealed; first NEW whole-package adversary active\n\nScoped signed original-side pedal product. Exact contemporary theorem and classical methods credited; no novelty/firstness/independence claim.107-entry verification archive includes18 original files. Review loop pending, no publication.\nPR203 selected-map SHA256: '+d
v.message=message
def run(c,h,rv,mode,gen):
 base=baseline(c);dest=D/gen
 if mode=='prepare':
  parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=v.queue_reconcile(c,h,base,parent);pt=c.selected_current(h,parent,inherited,base['tree']);v.original(h)
  assert h.api('compare/'+base['commit']+'...'+parent)['status'] in ['identical','ahead']
  stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.mkdir();v.save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',v.enc(ack))
 else:
  r=v.read(dest/'PREPARATION.json');ack=v.read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');parent=r['expected_main'];stamp=r['UTC'];pt=r['parent_tree'];inherited={**base['selected_files'],Q:ack['current_QUEUE']}
 out=overlay(h,parent,stamp);out[CASE+'priority_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=selected(c,inherited,out)
 if mode=='prepare':
  tree=h.api('git/trees','POST',{'base_tree':pt,'tree':entries(c,h,out)})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex)
  r={'UTC':stamp,'PR':203,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in ex.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};v.save(dest/'PREPARATION.json',v.enc(r))
 v.verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha']
 if mode=='prepare':
  pre={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'commit':r['commit'],'expected_main':parent,'observed_MAIN':main,'exact_trueparent_fullforeignscope_everyselectedidentity_verified':True,'selected_files':len(ex),'selected_map_sha256':c.selected_digest(ex),'no_QUEUE_native_or_PR_mutation':True,'mathematical_clearance':True,'source_contract_clearance':True,'bounded_priority_audit_complete':True,'qualified_attributed_note_editorially_cleared':True,'historical_firstness_independence_certified':False,'publication_ready':False,'case_percent':75};v.save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',v.enc(pre));print(json.dumps({k:r[k] for k in ['expected_main','commit','tree','selected_map_sha256']}|{'observed_main':main,'selected':len(ex),'changed':len(r['changed_paths'])}));return
 assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];actual,post=v.queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);v.original(h)
 for k,z in out.items():assert c.byte_pin(z)==ex[k] and h.lookup(tree,k)==('100644','blob',ex[k]['git_blob'])
 body=v.enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});v.save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body)
 accepted={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':203,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':v.pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':True,'bounded_priority_audit_complete':True,'qualified_attributed_note_editorially_cleared':True,'historical_firstness_independence_established':False,'publication_ready':False,'case_percent':75,'fully_completed_count':45,'published_count':29,'last_completed_PR':201,'next_numeric_intake_cursor':203,'advance_to_next_PR_authorized_now':False,'goal_complete':False};v.save(dest/'ACCEPTANCE.json',v.enc(accepted));print(json.dumps(accepted))
if __name__=='__main__':
 assert sys.dont_write_bytecode and not sys.flags.optimize
 c,h,rv=load();run(c,h,rv,sys.argv[1],sys.argv[2])

