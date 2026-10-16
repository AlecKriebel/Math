"""PR201 reviewed publication-ready checkpoint; no ref/deposit/PR mutation."""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,sys
D=Path(__file__).resolve().parent;A=D.parent
f=A/'priority_checkpoint_01/checkpoint_priority201.py';s=importlib.util.spec_from_file_location('priority201_current',f);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);m=v.m;Q=v.Q
PRIOR=A/'priority_checkpoint_01/priority60_02'
def load():
 c,h,rv=v.load();h.m.TREE_CACHE_PATH=A/'READY_PRIVATE_TREE_CACHE.json';return c,h,rv
def baseline(c):
 r=m.read(PRIOR/'PREPARATION.json');a=m.read(PRIOR/'ACCEPTANCE.json');x=m.read(PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json')
 assert a['accepted'] and a['every_selected_identity_checked_at_actual_observed_MAIN'] and r['commit']==a['checkpoint_commit']=='73c95cc5bf46afd8ddc86d9d563d0801be0799dc'
 assert len(r['selected_files'])==a['selected_files']==2357 and r['selected_map_sha256']==a['selected_map_sha256']==c.selected_digest(r['selected_files'])=='aa15355115952a1ae2aecde4933ecbe73643950b8f1b06a1b4a79750dceea97f'
 assert m.pin((PRIOR/'ACCEPTANCE_CURRENT_SELECTED_MAP.json').read_bytes())==a['actual_current_map_file'] and x['selected_map_sha256']==a['actual_current_selected_map_sha256']==c.selected_digest(x['selected_files'])
 return {**r,'commit':a['main_observed'],'tree':a['actual_tree'],'selected_files':x['selected_files'],'selected_map_sha256':x['selected_map_sha256']}
def overlay(h,parent,stamp):
 gp=A/'ROOT_PUBLICATION_GATE_01.json';g=m.read(gp);assert gp.stat().st_mode&0o777==0o444 and g['publication_ready_gate_accepted'] and g['whole_package_review_loop_complete'] and not g['historical_priority_established'];assert len(g['whole_package_review_events'])>=2 and g['whole_package_review_events'][-1]['reviewed_package_seal']==g['package_seal'] and g['fresh_final_review_after_documented_editorial_repairs'];out={}
 def add(rel,x=None):
  assert not Path(rel).is_absolute() and '..' not in Path(rel).parts;f=A/rel;assert f.is_file() and not f.is_symlink() and f.stat().st_mode&0o777==0o444,rel;b=f.read_bytes()
  if x is not None:assert m.pin(b)==x,rel
  out[m.CASE+rel]=b
 add(gp.name)
 for rel,x in g['package_safe_files'].items():add(g['package']+'/'+rel,x)
 for ev in g['whole_package_review_events']:
  assert ev['verdict'] in ['CLEANPASS','REPAIRS_REQUIRED']
  for n,x in ev['safe_files'].items():add(ev['directory']+'/'+n,x)
  add(ev['Root_acceptance_file'],ev['Root_acceptance_pin'])
 for rel,x in g['other_safe_files'].items():add(rel,x)
 for n in ['PREPARATION.json','ROOT_PRE_MOVE_VERIFICATION.json','ACCEPTANCE.json','ACCEPTANCE_CURRENT_SELECTED_MAP.json','FOREIGN_QUEUE_RECONCILIATION.json']:add('priority_checkpoint_01/priority60_02/'+n)
 add('publication_checkpoint_01/checkpoint_ready201.py')
 status='NEW_POST_REPAIR_WHOLE_PACKAGE_REVIEW_CLEAN_ATTRIBUTED_FLAG_PROOF_READY';remain='Publish exact reviewed3-file set with repository Zenodo kit; verify actual DOI/metadata/downloads, GWS tracker row, original-HEAD-safe merge and actual factual completion before202.'
 case=json.loads(h.body_at(m.CASE+'CURRENT_CASE_STATUS.json',parent));assert (case['PR'],case['case_percent'],case['original_head'])==(201,60,m.HEAD)
 case.update(UTC=stamp,status=status,case_percent=90,publication_ready=True,whole_publication_package_reviews_complete=True,NEW_whole_package_review_active=False,NEW_whole_package_reviews_completed=len(g['whole_package_review_events']),whole_package_review_loop_complete=True,whole_package_review_events=g['whole_package_review_events'],publication_gate=gp.name,publication_package=g['package'],historical_priority_established=False,historical_novelty_or_firstness_established=False,remaining_required_steps=remain)
 out[m.CASE+'CURRENT_CASE_STATUS.json']=m.enc(case)
 p=json.loads(h.body_at(m.PREFIX+'CURRENT_PROGRESS.json',parent));assert (p['current_PR'],p['fully_completed_count'],p['published_count'],p['last_completed_PR'],p['current_PR_workflow_percent'])==(201,44,28,200,60)
 p.setdefault('historical_current_case_snapshots',[]).append({'UTC':stamp,'PR':201,'prior_phase':60,'values':{k:x for k,x in p.items() if k.startswith('current_')}})
 p.update(UTC=stamp,updated_UTC=stamp,current_status=status,current_PR_workflow_percent=90,current_workflow_estimate_percent=90,current_publication_ready=True,current_publication_package=g['package'],current_publication_package_reviews_complete=True,current_NEW_whole_publication_package_reviews_completed=len(g['whole_package_review_events']),current_NEW_whole_publication_package_review_active=False,current_whole_package_review_loop_complete=True,current_whole_package_review_events=g['whole_package_review_events'],current_publication_gate='audits/pr201_5100014/'+gp.name,current_historical_novelty_or_firstness_established=False,current_independent_discovery_certified=False,current_remaining_required_steps=remain,remaining_current_step=remain,next_step=remain,current_source_provenance_warning='Scoped primitive leastN2mod4 signed every-M outer-pedal theorem. Exact Ferudun DOI23087221/23088516 theorem, six formula and repetition caveat credited, along with Steiner/Chavez and established methods. Historical firstness, independence and theorem/method novelty unestablished. Source table does not print primitive.',program_snapshot_semantics='PR201 attributed alternative proof ready after fresh post-repair whole-package review. Exact contemporary theorem and classical methods credited; no firstness/independence/novelty certificate. Publication/tracker/integration remain;44completed/28published,last200,cursor201/advancefalse.',program_snapshot_authority_condition='This ready90 postimage effective only after actual trueparent/fullforeignscope/everyselectedidentity acceptance. No actual publication or202 authority.')
 assert not p['current_completed'] and not p['advance_to_next_PR_authorized_now'] and not p['current_Zenodo_published'];out[m.PREFIX+'CURRENT_PROGRESS.json']=m.enc(p)
 note='\n'+stamp+' — PR201 ready90percent: first NEW whole-package adversary reviewed entire v1 and found a promised original-archive omission. Root repaired the complete package; a NEW adversary reviewed the entire final '+g['package']+' after all repairs and returned CLEANPASS. Root proof/source/code/replay/metadata/file/ZIP/visual checks accepted. Exact contemporary theorem/formulas/caveat and classical methods credited; no theorem novelty, firstness or certified independence. Exact3-file metadata kit check accepted; actual DOI/tracker/merge/factual completion remain.44completed/28published,last200,cursor201/advancefalse; goal active.\n'
 for rel in [m.CASE+'RESEARCH_LOG.md',m.PREFIX+'CURRENT_PROGRESS.md',m.PREFIX+'RESEARCH_LOG.md']:out[rel]=h.body_at(rel,parent)+note.encode()
 return out
def message(d):return 'PR201 attributed outer-pedal flag-curve proof ready90\n\nFirst whole-package review repaired; fresh final review clean. Exact contemporary theorem and classical methods credited. No firstness or independence certification.\nPR201 ready selected-map SHA256: '+d
def verify(c,h,r,ex):
 assert r['selected_files']==ex and r['selected_map_sha256']==c.selected_digest(ex);co=h.api('git/commits/'+r['commit']);assert [x['sha'] for x in co['parents']]==[r['expected_main']] and co['tree']['sha']==r['tree'] and co['message']==message(c.selected_digest(ex));assert h.api('git/commits/'+r['expected_main'])['tree']['sha']==r['parent_tree'];h.m.m.h.warm_selected_directories([r['parent_tree'],r['tree']],ex)
 for k,x in ex.items():assert h.lookup(r['tree'],k)==('100644','blob',x['git_blob']),k
 changes={k for k,x in ex.items() if h.lookup(r['parent_tree'],k)!=('100644','blob',x['git_blob'])};assert changes==h.changed_leaves(r['parent_tree'],r['tree'])==set(r['changed_paths']) and changes<=set(r['overlay_paths']) and Q not in changes and not any(k.startswith('unsolved_math_prioritization/attempts/') for k in changes)
def tree_entries(c,h,out):
 entries=[]
 for k,b in sorted(out.items()):
  if k.endswith(('.pdf','.zip')):
   sha=h.api('git/blobs','POST',{'encoding':'base64','content':base64.b64encode(b).decode()})['sha'];assert sha==c.byte_pin(b)['git_blob'];entries.append({'path':k,'mode':'100644','type':'blob','sha':sha})
  else:entries.append({'path':k,'mode':'100644','type':'blob','content':b.decode()})
 return entries
def run(c,h,rv,mode,gen):
 b=baseline(c);dest=D/gen
 if mode=='prepare':
  parent=h.api('git/ref/heads/main')['object']['sha'];inherited,ack=v.v.queue_reconcile(c,h,b,parent);pt=c.selected_current(h,parent,inherited,b['tree']);m.original(h);assert h.api('compare/'+b['commit']+'...'+parent)['status'] in ['identical','ahead'];stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();dest.mkdir();m.save(dest/'FOREIGN_QUEUE_RECONCILIATION.json',m.enc(ack))
 else:
  r=m.read(dest/'PREPARATION.json');ack=m.read(dest/'FOREIGN_QUEUE_RECONCILIATION.json');parent=r['expected_main'];stamp=r['UTC'];pt=r['parent_tree'];inherited={**b['selected_files'],Q:ack['current_QUEUE']}
 out=overlay(h,parent,stamp);out[m.CASE+'publication_checkpoint_01/'+gen+'/FOREIGN_QUEUE_RECONCILIATION.json']=(dest/'FOREIGN_QUEUE_RECONCILIATION.json').read_bytes();ex=m.selected(c,inherited,out)
 if mode=='prepare':
  tree=h.api('git/trees','POST',{'base_tree':pt,'tree':tree_entries(c,h,out)})['sha'];co=h.api('git/commits','POST',{'tree':tree,'parents':[parent],'message':message(c.selected_digest(ex))})['sha'];h.m.m.h.warm_selected_directories([pt,tree],ex);r={'UTC':stamp,'PR':201,'expected_main':parent,'parent_tree':pt,'tree':tree,'commit':co,'selected_files':ex,'selected_map_sha256':c.selected_digest(ex),'overlay_paths':sorted(out),'changed_paths':sorted(k for k,x in ex.items() if h.lookup(pt,k)!=('100644','blob',x['git_blob'])),'MAIN_moved':False};m.save(dest/'PREPARATION.json',m.enc(r))
 verify(c,h,r,ex);main=h.api('git/ref/heads/main')['object']['sha']
 if mode=='prepare':
  m.save(dest/'ROOT_PRE_MOVE_VERIFICATION.json',m.enc({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'Root_verified':True,'expected_main':parent,'observed_MAIN':main,'commit':r['commit'],'exact_trueparent_fullforeignscope_allselectedidentities_verified':True,'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'case_percent':90,'publication_ready':True}));print(json.dumps({k:r[k] for k in ['expected_main','commit','tree','selected_map_sha256']}|{'observed_main':main,'selected':len(ex),'changed':len(r['changed_paths'])}));return
 assert h.api('compare/'+r['commit']+'...'+main)['status'] in ['identical','ahead'];actual,post=v.v.queue_reconcile(c,h,r,main);tree=c.selected_current(h,main,actual,r['tree']);m.original(h)
 for k,z in out.items():assert c.byte_pin(z)==ex[k] and h.lookup(tree,k)==('100644','blob',ex[k]['git_blob'])
 body=m.enc({'selected_files':actual,'selected_map_sha256':c.selected_digest(actual),'foreign_QUEUE_reconciliation_after_checkpoint':post});m.save(dest/'ACCEPTANCE_CURRENT_SELECTED_MAP.json',body);a={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':201,'accepted':True,'checkpoint_commit':r['commit'],'sole_parent':parent,'main_observed':main,'actual_tree':tree,'selected_files':len(ex),'selected_map_sha256':r['selected_map_sha256'],'actual_current_selected_map_sha256':c.selected_digest(actual),'actual_current_map_file':m.pin(body),'every_selected_identity_checked_at_actual_observed_MAIN':True,'all_overlay_body_identities_verified':True,'full_foreign_tree_scope_preserved':True,'QUEUE_native_original_PR_unchanged':True,'publication_ready':True,'actual_publication_verified':False,'historical_firstness_independence_established':False,'case_percent':90,'fully_completed_count':44,'published_count':28,'last_completed_PR':200,'next_numeric_intake_cursor':201,'advance_to_next_PR_authorized_now':False,'goal_complete':False};m.save(dest/'ACCEPTANCE.json',m.enc(a));print(json.dumps(a))
if __name__=='__main__':
 assert sys.dont_write_bytecode;c,h,rv=load();run(c,h,rv,sys.argv[1],sys.argv[2])
